from pathlib import Path
import copy,hashlib,json,re
import pytest
from gltest.direct import create_address
ROOT=Path(__file__).parents[1]
META=json.loads((ROOT/'fixtures/source.json').read_bytes())
FILES={name:(ROOT/'fixtures'/name).read_bytes() for name in META['sources']}
SHA=lambda b:hashlib.sha256(b).hexdigest()

def build(vm,deploy):
 vm.warp('2026-10-21T00:00:00Z');c=deploy(str(ROOT/'contract.py'),sdk_version='v0.2.12')
 assert hasattr(c,'get_configuration'),'Public contract behavior not implemented'
 return c

def body(value):return (json.dumps(value,separators=(',',':'))+'\n').encode()
def serve(vm,name,data):vm.mock_web(re.escape(META['sources'][name]['test_url']),{'status':200,'body':data.decode('utf-8')})

POLICY=json.loads(FILES['policy.json'])
def open_record(vm,c,left=None,right=None,policy=None):
 a=FILES['left.json'] if left is None else body(left);b=FILES['right.json'] if right is None else body(right)
 serve(vm,'left.json',a);serve(vm,'right.json',b)
 c.open_pair('demo',META['sources']['left.json']['test_url'],SHA(a),META['sources']['right.json']['test_url'],SHA(b),json.dumps(POLICY if policy is None else policy))
def get(c):return c.get_pair('demo')
def row(i,v=0,t=0,category='sample',unit='ticks'):return {'id':i,'category':category,'unit':unit,'value':v,'tick':t}
def source(rows):return {'version':1,'records':rows}

def test_owner_cas_permissionless_derive_terminal_revoke_and_permanent_id(direct_vm,direct_deploy):
 c=build(direct_vm,direct_deploy);open_record(direct_vm,c);owner=get(c)['owner'];outsider=create_address('outsider')
 with direct_vm.prank(outsider):
  with direct_vm.expect_revert('owner'):c.confirm_pair('demo',0,'b'*64)
  c.derive_pair('demo',0)
  with direct_vm.expect_revert('owner'):c.revoke_pair('demo',1,'withdraw')
 d=get(c);assert d['status']=='DERIVED' and d['revision']==1 and len(d['certificate_id'])==64
 with direct_vm.expect_revert('revision'):c.confirm_pair('demo',0,d['certificate_id'])
 with direct_vm.expect_revert('certificate'):c.confirm_pair('demo',1,'0'*64)
 c.confirm_pair('demo',1,d['certificate_id']);assert get(c)['status']=='CONFIRMED' and get(c)['revision']==2
 with direct_vm.expect_revert():c.derive_pair('demo',2)
 direct_vm.clear_mocks();c.revoke_pair('demo',2,'Synthetic record withdrawn');d=get(c)
 assert d['owner']==owner and d['status']=='REVOKED' and d['revision']==3 and len(d['history'])==4
 with direct_vm.expect_revert():c.revoke_pair('demo',3,'again')
 with direct_vm.expect_revert():open_record(direct_vm,c)

def test_independent_validator_refetches_bytes_and_rejects_complete_forged_packet(direct_vm,direct_deploy):
 c=build(direct_vm,direct_deploy);open_record(direct_vm,c);c.derive_pair('demo',0);assert direct_vm.run_validator() is True
 packet=copy.deepcopy(get(c)['last_capture']);packet['binding']['record_id']='other';assert direct_vm.run_validator(leader_result=packet) is False
 packet=copy.deepcopy(get(c)['last_capture']);packet['result']['decision']='FABRICATED';assert direct_vm.run_validator(leader_result=packet) is False
 direct_vm.clear_mocks()
 for name,data in FILES.items():
  if name!='policy.json':serve(direct_vm,name,data+b' ')
 assert direct_vm.run_validator() is False

def test_failed_confirmation_source_unavailable_preserves_revision(direct_vm,direct_deploy):
 c=build(direct_vm,direct_deploy);open_record(direct_vm,c);c.derive_pair('demo',0);d=get(c);direct_vm.clear_mocks()
 with direct_vm.expect_revert():c.confirm_pair('demo',1,d['certificate_id'])
 assert get(c)==d

@pytest.mark.parametrize('repo',['.','..','%2e'])
def test_namespace_dot_repository_rejected_before_fetch(direct_vm,direct_deploy,repo):
 c=build(direct_vm,direct_deploy);url='https://raw.githubusercontent.com/example/'+repo+'/'+'a'*40+'/input.json'
 with direct_vm.expect_revert('commit-pinned'):c.open_pair('bad',url,'b'*64,url,'b'*64,json.dumps(POLICY))

def test_exact_fixture_metadata_and_zero_constructor_api(direct_vm,direct_deploy):
 for name,data in FILES.items():assert SHA(data)==META['sources'][name]['sha256'] and len(data)==META['sources'][name]['bytes'] and META['sources'][name]['public_url'] is None
 c=build(direct_vm,direct_deploy);assert c.get_configuration()['protocol']=='SpecPair'+'-v1'

def test_source_duplicate_keys_nonfinite_hash_drift_and_response_bounds(direct_vm,direct_deploy):
 c=build(direct_vm,direct_deploy)
 for data in [b'{"version":1,"version":1}',b'{"version":NaN}',b'x',b'{}',b' '*16385]:
  direct_vm.clear_mocks();serve(direct_vm,'left.json',data);serve(direct_vm,'right.json',FILES['right.json'])
  with direct_vm.expect_revert():c.open_pair('bad',META['sources']['left.json']['test_url'],SHA(data),META['sources']['right.json']['test_url'],SHA(FILES['right.json']),json.dumps(POLICY))

def test_global_maximum_cardinality_beats_greedy_and_complete_witness(direct_vm,direct_deploy):
 c=build(direct_vm,direct_deploy);open_record(direct_vm,c);r=c.derive_pair('demo',0)
 assert r['decision']=='MATCHED' and r['matched_count']==2 and r['total_cost']==2 and r['assignment_vector']==[1,0,3]
 assert [(p['left'],p['right'],p['cost']) for p in r['pairs']]==[('L1','R2',1),('L2','R1',1)]
 assert r['unmatched_left']==['L3'] and r['unmatched_right']==['R3'] and len(r['grid'])==3

def test_minimum_cost_after_cardinality_and_ascii_assignment_tie(direct_vm,direct_deploy):
 c=build(direct_vm,direct_deploy);open_record(direct_vm,c,source([row('b',3),row('A',0)]),source([row('d',2),row('C',1)]),{**POLICY,'value_tolerance':3});r=c.derive_pair('demo',0)
 assert r['matched_count']==2 and r['total_cost']==2 and r['assignment_vector']==[0,1]

def test_equal_cost_canonical_tie_prefers_earliest_left_right_indices(direct_vm,direct_deploy):
 c=build(direct_vm,direct_deploy);open_record(direct_vm,c,source([row('b'),row('A')]),source([row('d'),row('C')]),POLICY);r=c.derive_pair('demo',0)
 assert r['assignment_vector']==[0,1] and [(x['left'],x['right']) for x in r['pairs']]==[('A','C'),('b','d')]

@pytest.mark.parametrize('left,right,decision',[([],[],'EMPTY'),([{'id':'a','category':'x','unit':'u','value':0,'tick':0}],[],'NO_MATCH')])
def test_empty_and_no_match_are_explicit(direct_vm,direct_deploy,left,right,decision):
 c=build(direct_vm,direct_deploy);open_record(direct_vm,c,source(left),source(right));r=c.derive_pair('demo',0)
 assert r['decision']==decision and r['matched_count']==0 and r['total_cost']==0

@pytest.mark.parametrize('change',['bool','float','duplicate_id','unknown','category','tick','value','too_many','version_bool'])
def test_strict_record_boundaries(direct_vm,direct_deploy,change):
 s=source([row('a')])
 if change=='bool':s['records'][0]['value']=True
 if change=='float':s['records'][0]['value']=1.0
 if change=='duplicate_id':s['records'].append(row('a'))
 if change=='unknown':s['records'][0]['extra']=1
 if change=='category':s['records'][0]['category']='bad category'
 if change=='tick':s['records'][0]['tick']=-1
 if change=='value':s['records'][0]['value']=1000001
 if change=='too_many':s['records']=[row('r'+str(i)) for i in range(9)]
 if change=='version_bool':s['version']=True
 c=build(direct_vm,direct_deploy)
 with direct_vm.expect_revert():open_record(direct_vm,c,s)

@pytest.mark.parametrize('field,value',[('value_tolerance',True),('value_weight',0),('tick_weight',-1),('tick_tolerance',1000001),('extra',1)])
def test_locked_policy_is_strict_and_integer_bounded(direct_vm,direct_deploy,field,value):
 c=build(direct_vm,direct_deploy)
 with direct_vm.expect_revert():open_record(direct_vm,c,policy={**POLICY,field:value})

def test_tick_and_unit_admissibility_and_weighted_integer_cost(direct_vm,direct_deploy):
 c=build(direct_vm,direct_deploy);open_record(direct_vm,c,source([row('a',-2,10)]),source([row('b',1,12),row('c',-2,10,unit='other')]),{**POLICY,'value_tolerance':3,'tick_tolerance':2,'value_weight':5,'tick_weight':3});r=c.derive_pair('demo',0)
 assert r['matched_count']==1 and r['total_cost']==21 and r['pairs'][0]['value_delta']==3 and r['pairs'][0]['tick_delta']==2 and r['unmatched_right']==['c']

def test_eight_by_eight_resource_bound_and_canonical_assignment(direct_vm,direct_deploy):
 c=build(direct_vm,direct_deploy);open_record(direct_vm,c,source([row('l'+str(i)) for i in range(8)]),source([row('r'+str(i)) for i in range(8)]));r=c.derive_pair('demo',0)
 assert r['matched_count']==8 and r['assignment_vector']==list(range(8)) and r['total_cost']==0

def test_validator_rejects_complete_feasible_but_globally_suboptimal_shape(direct_vm,direct_deploy):
 c=build(direct_vm,direct_deploy);open_record(direct_vm,c);c.derive_pair('demo',0)
 packet=copy.deepcopy(get(c)['last_capture']);r=packet['result']
 r['matched_count']=1;r['total_cost']=1;r['assignment_vector']=[0,3,3]
 r['pairs']=[{'left':'L1','right':'R1','value_delta':1,'tick_delta':0,'cost':1}]
 r['unmatched_left']=['L2','L3'];r['unmatched_right']=['R2','R3']
 assert direct_vm.run_validator(leader_result=packet) is False
