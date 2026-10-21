import './style.css';
import leftFixture from '../../fixtures/left.json';
import rightFixture from '../../fixtures/right.json';
import policyFixture from '../../fixtures/policy.json';
import meta from '../../fixtures/source.json';
import {validateSource,validatePolicy,derive,manual,checkResult,type Source,type Policy} from './domain';
import {boot,el,value,cell,json,exportJSON} from './shell';
import {lockArgs} from './wallet';
import {parsePublicJSON} from './public-json';
const workspace='<section class="card"><p class="eyebrow">ONE-TO-ONE RECONCILIATION</p><h2>Find the largest admissible pairing</h2><span id="viewMode" class="tag">Local synthetic preview</span><p>Maximize matched rows, then minimize exact mismatch cost. Equal optima use the ASCII assignment vector. An admissible first choice can block a better global match.</p><div id="score" class="score"></div><div class="split"><section><h3>Left records</h3><div id="leftTable" class="table-wrap"></div></section><section><h3>Right records</h3><div id="rightTable" class="table-wrap"></div></section></div><h3>Admissibility and exact cost grid</h3><p class="small">Category and unit must agree, then both tolerances must hold. Outlined cells are the canonical optimum.</p><div id="costGrid" class="table-wrap"></div><h3>Matched and unmatched rows</h3><div id="matches" class="table-wrap"></div><p id="unmatched"></p><details><summary>Full result witness</summary><pre id="result"></pre></details></section><section class="card"><h2>Try a manual pairing</h2><p class="small">Local explanation only. Each right row may be used once. No assignment is submitted to the contract.</p><div id="manualChoices"></div><p id="manualStatus" role="status"></p><button id="useOptimum" class="secondary">Use canonical optimum locally</button></section><section class="card"><h2>Edit and export synthetic inputs</h2><p class="small">Each side0..8 rows; ASCII identifiers, integer values and abstract ticks. Changed previews must be separately published.</p><div class="split"><label>Left JSON<textarea id="leftJson" spellcheck="false"></textarea></label><label>Right JSON<textarea id="rightJson" spellcheck="false"></textarea></label></div><label>Tolerance and cost policy<textarea id="policyJson" spellcheck="false"></textarea></label><button id="applyPreview" class="secondary">Validate local preview</button><div class="pair"><button id="exportLeft" class="secondary">Export left bytes</button><button id="exportRight" class="secondary">Export right bytes</button></div><pre id="exportInfo"></pre></section>';
const fields='<label>Published left commit URL<input id="sourceUrl" placeholder="Publish left.json first"></label><label>Left byte SHA256<input id="sourceSha" value="'+meta.sources['left.json'].sha256+'"></label><label>Published right commit URL<input id="rightUrl" placeholder="Publish right.json first"></label><label>Right byte SHA256<input id="rightSha" value="'+meta.sources['right.json'].sha256+'"></label><p class="small">Open freezes the policy in the policy JSON editor and the two public source hashes. Local preview edits do not publish.</p>';
const app=boot('SpecPair','pair','Globally reconcile two declared record lists with exact admissibility and cost. A pairing does not prove identity, physical delivery or real-world equivalence.',workspace,fields,()=>{
 const a=lockArgs(value('recordId'),value('sourceUrl'),value('sourceSha')),b=lockArgs(value('recordId'),value('rightUrl'),value('rightSha')),p=validatePolicy(parsePublicJSON(el<HTMLTextAreaElement>('policyJson').value));
 return [a[0],a[1],a[2],b[1],b[2],json(p)];
});
let sources:Source[]=[validateSource(leftFixture),validateSource(rightFixture)],policy:Policy=validatePolicy(policyFixture),mode='Local synthetic preview',vector:number[]=[];
function table(id:string,s:Source){
 const t=document.createElement('table'),h=document.createElement('tr');for(const label of ['ID','Category','Unit','Value','Tick'])cell(h,label,'th');t.append(h);
 for(const r of s.records){const row=document.createElement('tr');for(const text of [r.id,r.category,r.unit,String(r.value),String(r.tick)])cell(row,text);t.append(row);}el(id).replaceChildren(t);
}
function render(){
 const r=derive(sources,policy);el('viewMode').textContent=mode;el('score').replaceChildren();
 for(const [label,text] of [['Decision',r.decision],['Matched',String(r.matched_count)],['Exact cost',String(r.total_cost)],['Assignment',r.assignment_vector.join(' · ')||'[]']]){const box=document.createElement('div');cell(box,label,'small');cell(box,text,'strong');el('score').append(box);}
 table('leftTable',sources[0]);table('rightTable',sources[1]);const grid=document.createElement('table'),head=document.createElement('tr');cell(head,'Left / right','th');for(const b of sources[1].records)cell(head,b.id,'th');grid.append(head);
 r.grid.forEach((line,i)=>{const row=document.createElement('tr');cell(row,sources[0].records[i].id,'th');line.forEach((c,j)=>{const td=cell(row,c.admissible?String(c.cost):c.reason);td.className=(c.admissible?'allowed':'blocked')+(r.assignment_vector[i]===j?' matched':'');td.title='value delta '+c.value_delta+', tick delta '+c.tick_delta;});grid.append(row);});el('costGrid').replaceChildren(grid);
 const matched=document.createElement('table');for(const p of r.pairs){const row=document.createElement('tr');for(const text of [p.left+' → '+p.right,'Δvalue '+p.value_delta,'Δtick '+p.tick_delta,'cost '+p.cost])cell(row,text);matched.append(row);}el('matches').replaceChildren(matched);
 el('unmatched').textContent='Unmatched left: '+(r.unmatched_left.join(', ')||'none')+' · right: '+(r.unmatched_right.join(', ')||'none')+'. EMPTY/NO_MATCH are explicit abstract outcomes.';el('result').textContent=json(r);
 if(vector.length!==sources[0].records.length)vector=[...r.assignment_vector];el('manualChoices').replaceChildren();
 sources[0].records.forEach((a,i)=>{const label=document.createElement('label');label.textContent=a.id+' → ';const select=document.createElement('select');select.setAttribute('aria-label','Manual target for '+a.id);sources[1].records.forEach((b,j)=>{const opt=document.createElement('option');opt.value=String(j);opt.textContent=b.id;select.append(opt);});const none=document.createElement('option');none.value=String(sources[1].records.length);none.textContent='Unmatched';select.append(none);select.value=String(vector[i]);select.addEventListener('change',()=>{vector[i]=Number(select.value);render();});label.append(select);el('manualChoices').append(label);});
 try{const x=manual(sources,policy,vector);el('manualStatus').textContent='Manual: '+x.matched_count+' matches, cost '+x.total_cost+'; '+(x.canonical?'canonical optimum':'differs from the canonical optimum')+'. Local only.';}catch(e){el('manualStatus').textContent=e instanceof Error?e.message:'Invalid manual pairing.';}
}
function editors(){el<HTMLTextAreaElement>('leftJson').value=json(sources[0]);el<HTMLTextAreaElement>('rightJson').value=json(sources[1]);el<HTMLTextAreaElement>('policyJson').value=json(policy);}
el('useOptimum').addEventListener('click',()=>{vector=[...derive(sources,policy).assignment_vector];render();});
el('applyPreview').addEventListener('click',()=>app.run(async()=>{
 const next=[validateSource(parsePublicJSON(el<HTMLTextAreaElement>('leftJson').value)),validateSource(parsePublicJSON(el<HTMLTextAreaElement>('rightJson').value))],p=validatePolicy(parsePublicJSON(el<HTMLTextAreaElement>('policyJson').value));
 app.clear();sources=next;policy=p;vector=[];mode='Edited local preview · unpublished';editors();render();app.log('Preview updated. Publish exact exported source bytes separately.');
}));
for(const [button,name,index] of [['exportLeft','left.json',0],['exportRight','right.json',1]] as const)el(button).addEventListener('click',()=>app.run(async()=>{el('exportInfo').textContent=await exportJSON(name,sources[index]);app.log('Exported public synthetic JSON only. No publication or write.');}));
app.hooks(record=>{
 if(!Array.isArray(record.sources)||record.sources.length!==2)throw Error('Two complete source snapshots required.');
 const next=record.sources.map(validateSource),p=validatePolicy(record.policy);if(record.result!==null)checkResult(next,p,record.result);
 sources=next;policy=p;vector=[];mode=record.status==='REVOKED'?'Historical chain result · REVOKED':record.result===null?'Loaded source · local optimum preview':'Verified loaded chain reconciliation';editors();render();
},()=>{mode='Local preview · no current chain context';el('viewMode').textContent=mode;});
editors();render();app.refresh();
