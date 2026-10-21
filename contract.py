# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *
import hashlib,json,re
from datetime import datetime,timezone

def _require(ok: bool,message: str) -> None:
 if not ok:raise gl.vm.UserError('[EXPECTED] '+message)
def _canonical(value) -> str:return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False)
def _now() -> int:
 value=datetime.fromisoformat(gl.message_raw['datetime'].replace('Z','+00:00'))
 if value.tzinfo is None:value=value.replace(tzinfo=timezone.utc)
 delta=value.astimezone(timezone.utc)-datetime(1970,1,1,tzinfo=timezone.utc)
 return delta.days*86400+delta.seconds
def _identifier(value) -> None:_require(isinstance(value,str) and re.fullmatch(r'[A-Za-z][A-Za-z0-9_]{0,23}',value) is not None,'invalid ASCII identifier')
def _integer(value,lo: int,hi: int) -> bool:return type(value) is int and lo<=value<=hi
def _source(url: str,digest: str) -> None:
 pattern=r'https://raw\.githubusercontent\.com/[A-Za-z0-9-]{1,39}/[A-Za-z0-9_.-]{1,100}/[0-9a-f]{40}/[A-Za-z0-9_.~/-]+'
 _require(isinstance(url,str) and len(url)<=512 and re.fullmatch(pattern,url) is not None and all(part not in ('','.','..') for part in url.split('/')[3:]),'canonical commit-pinned URL required')
 _require(isinstance(digest,str) and re.fullmatch(r'[0-9a-f]{64}',digest) is not None,'invalid SHA256')
def _unique(pairs: list) -> dict:
 out={}
 for key,value in pairs:
  _require(key not in out,'duplicate JSON key');out[key]=value
 return out
def _constant(value):raise gl.vm.UserError('[SOURCE] nonfinite JSON constant')
def _parse(body: bytes):
 _require(1<=len(body)<=16384,'source byte bound')
 try:return json.loads(body.decode('utf-8'),object_pairs_hook=_unique,parse_constant=_constant)
 except (ValueError,UnicodeError,RecursionError):raise gl.vm.UserError('[SOURCE] invalid UTF8 JSON')
def _fetch(url: str,digest: str) -> dict:
 response=gl.nondet.web.get(url,headers={'Accept':'application/json'})
 _require(response.status==200 and response.body is not None and 1<=len(response.body)<=16384,'SOURCE unavailable or oversized')
 _require(hashlib.sha256(response.body).hexdigest()==digest,'SOURCE byte SHA256 mismatch')
 return _validate(_parse(response.body))

def _validate(value) -> dict:
 _require(isinstance(value,dict) and set(value)=={'version','records'} and type(value['version']) is int and value['version']==1,'source schema')
 rows=value['records'];_require(isinstance(rows,list) and len(rows)<=8,'0..8 records required');seen=set()
 for row in rows:
  _require(isinstance(row,dict) and set(row)=={'id','category','unit','value','tick'},'record fields')
  for key in ('id','category','unit'):_identifier(row[key])
  _require(row['id'] not in seen,'duplicate record ID');seen.add(row['id'])
  _require(_integer(row['value'],-1000000,1000000) and _integer(row['tick'],0,1000000),'record integer bounds')
 return {'version':1,'records':sorted(rows,key=lambda x:x['id'])}
def _policy(text: str) -> dict:
 _require(isinstance(text,str) and len(text)<=1024,'policy text bound');p=_parse(text.encode('utf-8'))
 _require(isinstance(p,dict) and set(p)=={'value_tolerance','tick_tolerance','value_weight','tick_weight'},'policy fields')
 _require(_integer(p['value_tolerance'],0,2000000) and _integer(p['tick_tolerance'],0,1000000) and _integer(p['value_weight'],1,1000) and _integer(p['tick_weight'],0,1000),'policy integer bounds')
 return p
def _derive(sources: list,policy: dict) -> dict:
 left=sources[0]['records'];right=sources[1]['records'];n=len(left);m=len(right);grid=[]
 for a in left:
  line=[]
  for b in right:
   dv=abs(a['value']-b['value']);dt=abs(a['tick']-b['tick'])
   reason='ADMISSIBLE'
   if a['category']!=b['category']:reason='CATEGORY'
   elif a['unit']!=b['unit']:reason='UNIT'
   elif dv>policy['value_tolerance']:reason='VALUE_TOLERANCE'
   elif dt>policy['tick_tolerance']:reason='TICK_TOLERANCE'
   allowed=reason=='ADMISSIBLE'
   line.append({'left':a['id'],'right':b['id'],'admissible':allowed,'reason':reason,'value_delta':dv,'tick_delta':dt,'cost':policy['value_weight']*dv+policy['tick_weight']*dt if allowed else None})
  grid.append(line)
 memo={}
 def best(i: int,mask: int):
  if i==n:return (0,0,())
  key=(i,mask)
  if key in memo:return memo[key]
  suffix=best(i+1,mask);chosen=(suffix[0],suffix[1],(m,)+suffix[2])
  for j in range(m):
   if mask&(1<<j) or not grid[i][j]['admissible']:continue
   suffix=best(i+1,mask|(1<<j));candidate=(suffix[0]+1,suffix[1]+grid[i][j]['cost'],(j,)+suffix[2])
   if (-candidate[0],candidate[1],candidate[2])<(-chosen[0],chosen[1],chosen[2]):chosen=candidate
  memo[key]=chosen;return chosen
 count,cost,vector=best(0,0);pairs=[];used=set();unmatched=[]
 for i,j in enumerate(vector):
  if j==m:unmatched.append(left[i]['id'])
  else:
   used.add(j);cell=grid[i][j];pairs.append({'left':cell['left'],'right':cell['right'],'value_delta':cell['value_delta'],'tick_delta':cell['tick_delta'],'cost':cell['cost']})
 return {'decision':'EMPTY' if n==0 and m==0 else ('NO_MATCH' if count==0 else 'MATCHED'),'matched_count':count,'total_cost':cost,'assignment_vector':list(vector),'pairs':pairs,'unmatched_left':unmatched,'unmatched_right':[b['id'] for j,b in enumerate(right) if j not in used],'grid':grid}

def _capture(locators: list,policy: dict,binding: dict) -> dict:
 def leader() -> dict:
  sources=[_fetch(locator['url'],locator['sha256']) for locator in locators]
  return {'binding':binding,'sources':sources,'result':None if binding['operation']=='open' else _derive(sources,policy)}
 def validator(proposed: gl.vm.Result) -> bool:
  if not isinstance(proposed,gl.vm.Return):return False
  try:return _canonical(leader())==_canonical(proposed.calldata)
  except Exception:return False
 return gl.vm.run_nondet_unsafe(leader,validator)

class SpecPair(gl.Contract):
 records: TreeMap[str,str]
 def __init__(self):pass
 def _get(self,record_id: str) -> dict:
  _identifier(record_id);_require(record_id in self.records,'unknown record');return json.loads(self.records[record_id])
 def _revision(self,r: dict,revision: int) -> None:_require(type(revision) is int and revision==r['revision'],'stale revision')
 def _owner(self,r: dict) -> None:_require(gl.message.sender_address.as_hex.lower()==r['owner'],'owner only')
 def _binding(self,r: dict,operation: str) -> dict:
  return {'protocol':'SpecPair-v1','chain_id':int(gl.message.chain_id),'contract':gl.message.contract_address.as_hex.lower(),'owner':r['owner'],'record_id':r['record_id'],'locators':r['locators'],'policy':r['policy'],'revision':r['revision'],'operation':operation,'observed_at':_now()}
 def _history(self,r: dict) -> None:
  _require(len(r['history'])<4,'finite history bound');r['history'].append({'status':r['status'],'revision':r['revision'],'at':_now(),'certificate_id':r['certificate_id']})
 def _open(self,record_id: str,locators: list,policy: dict) -> None:
  _identifier(record_id);_require(record_id not in self.records,'record ID already used')
  r={'record_id':record_id,'owner':gl.message.sender_address.as_hex.lower(),'locators':locators,'policy':policy,'status':'OPEN','revision':0,'certificate_id':'','reason':'','sources':[],'result':None,'last_capture':None,'history':[]}
  packet=_capture(locators,policy,self._binding(r,'open'));r['sources']=packet['sources'];r['last_capture']=packet;self._history(r);self.records[record_id]=_canonical(r)
 @gl.public.write
 def open_pair(self,record_id: str,left_url: str,left_sha256: str,right_url: str,right_sha256: str,policy_json: str) -> None:
  _source(left_url,left_sha256);_source(right_url,right_sha256);policy=_policy(policy_json)
  self._open(record_id,[{'url':left_url,'sha256':left_sha256},{'url':right_url,'sha256':right_sha256}],policy)

 @gl.public.write
 def derive_pair(self,record_id: str,expected_revision: int) -> dict:
  r=self._get(record_id);self._revision(r,expected_revision);_require(r['status']=='OPEN','record not OPEN')
  packet=_capture(r['locators'],r['policy'],self._binding(r,'derive'));_require(_canonical(packet['sources'])==_canonical(r['sources']),'source snapshot mismatch')
  r['result']=packet['result'];r['last_capture']=packet;r['certificate_id']=hashlib.sha256(_canonical(packet).encode('utf-8')).hexdigest();r['status']='DERIVED';r['revision']=1;self._history(r);self.records[record_id]=_canonical(r);return r['result']
 @gl.public.write
 def confirm_pair(self,record_id: str,expected_revision: int,certificate_id: str) -> None:
  r=self._get(record_id);self._owner(r);self._revision(r,expected_revision);_require(r['status']=='DERIVED','record not DERIVED');_require(isinstance(certificate_id,str) and certificate_id==r['certificate_id'],'current certificate required')
  packet=_capture(r['locators'],r['policy'],self._binding(r,'confirm'));_require(_canonical(packet['sources'])==_canonical(r['sources']) and _canonical(packet['result'])==_canonical(r['result']),'fresh complete result mismatch')
  r['last_capture']=packet;r['status']='CONFIRMED';r['revision']=2;self._history(r);self.records[record_id]=_canonical(r)
 @gl.public.write
 def revoke_pair(self,record_id: str,expected_revision: int,reason: str) -> None:
  r=self._get(record_id);self._owner(r);self._revision(r,expected_revision);_require(r['status']!='REVOKED','record already revoked');_require(isinstance(reason,str) and reason==reason.strip() and 1<=len(reason)<=160,'reason1..160 trimmed')
  r['status']='REVOKED';r['revision']+=1;r['reason']=reason;self._history(r);self.records[record_id]=_canonical(r)
 @gl.public.view
 def get_pair(self,record_id: str) -> dict:return self._get(record_id)
 @gl.public.view
 def get_configuration(self) -> dict:return {'protocol':'SpecPair-v1','max_records_per_side':8,'max_source_bytes':16384,'real_identity_or_delivery_proved':False}
