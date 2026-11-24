/* Node.js standard-library verifier. Run from any working directory. */
'use strict';
const {readFileSync}=require('node:fs');
const {join}=require('node:path');
const get=(file)=>JSON.parse(readFileSync(join(__dirname,file),'utf8'));
const rows=get('witnesses.json');
const cat=get('../2026-11-15/h.json').solutions;
const old=get('../2026-11-23/independent_joint.json');
const pinned=get('../2026-11-23/check.json');
const bsrc=[0x17e7146801n,0x6293dc808n,0xf714c2017n,0x35dfc802dn,0xb1f3485cn,0x63e6a0aen,0x65be14fn,0x196fc233n,0x3e690ce6n,0xcb73897n];

function replay(rows,cat,old,bsrc,pinned){
const C = (i,sw)=>cat[i].columns.map(c=>sw&&((c&1)!==((c>>2)&1))?c^5:c);
const check=(ok,msg)=>{if(!ok)throw Error(msg)};
const wt=(x)=>{x=x-((x>>>1)&0x55555555);x=(x&0x33333333)+((x>>>2)&0x33333333);return (((x+(x>>>4))&0x0f0f0f0f)*0x01010101)>>>24;};
const bw=(msg)=>{let x=0n;for(let i=0;i<10;i++)if(msg>>i&1)x^=bsrc[i];return wt(Number(x&0xffffffffn))+wt(Number(x>>32n));};
const H = a=>Array.from({length:64},(_,t)=>t).filter(t=>bw(a^((t&31)<<4)^(t&32?1008:0))===14);
const wh=(c,t)=>c.reduce((r,v,j)=>r|((wt(t&v)&1)<<j),0);
const h2=H(2),h3=H(3);check(JSON.stringify(h2)===JSON.stringify(pinned.actual_minimum_sections['2']),'H2');
check(JSON.stringify(h3)===JSON.stringify(pinned.actual_minimum_sections['3'])&&h3.join(',')==='0,4,5,10,11,15,18,19,23,25,33,46,54,56,60,61','H3');
const full=(T,c)=>{
  // Split even/odd column positions rather than consecutive positions.
  const I=Array.from({length:27},(_,j)=>j),half=(p)=>T.map(t=>I.filter(j=>(j&1)===p).reduce((r,j,k)=>r|((wt(t&c[j])&1)<<k),0));
  const L=half(0),R=half(1);
  // Tuples as two exact 40-bit integers (8 lanes of 5 bits), then delimited by colon.
  const powers=Array.from({length:8},(_,j)=>32**j);
  const key=(r,x,isRight)=>{
    let a=0,b=0;for(let j=0;j<T.length;j++){
      const n=wt(x^r[j]),q=(isRight?14-n:n)*powers[j&7];
      if(j<8)a+=q;else b+=q;
    }
    return a+':'+b;
  };
  const count=new Map();
  for(let x=0;x<16384;x++){const k=key(L,x,false);count.set(k,(count.get(k)||0)+1);}
  let matches=0;
  for(let x=0;x<8192;x++)matches+=count.get(key(R,x,true))||0;
  return matches;
};
check(rows.length===8,'eight records');
const out=[];const omitted=h3.indexOf(25),omitted2=h3.indexOf(60);
const expected=65535^(1<<omitted)^(1<<omitted2);
const expectedRows=[[19,false,16],[19,true,16],[115,false,14],[115,true,14],[139,false,14],[139,true,14],[163,false,16],[163,true,16]];
for(const [n,[i,sw,k,masks]] of rows.entries()){
  check(JSON.stringify([i,sw,k])===JSON.stringify(expectedRows[n]),'row spec');
  const c=C(i,sw), actual=pinned.controls.find(x=>x.index===i&&x.swap_0_2===sw);
  check(JSON.stringify(c)===JSON.stringify(actual.columns),'columns');
  check(masks.every(m=>Number.isInteger(m)&&m>=0&&m<2**27)&&new Set(masks).size===masks.length,'masks');
  const ww=h3.map(t=>wh(c,t));
  const has=masks.map(m=>ww.reduce((z,w,j)=>z|((wt(m^w)===14?1:0)<<j),0));
  const countWanted=(size)=>{let n=0,missing=[];for(let z=0;z<65536;z++)if(wt(z)===size){if(has.some(w=>(w&z)===z))n++;else missing.push(z);}return {n,missing};};
  const res={i,sw,k,masks:masks.length};
  if(k===16){check(masks.length===16&&has.every((w,j)=>w===(65535^(1<<j))),'exact indexed single deletion');res.size15=countWanted(15);check(res.size15.n===16,'all 15 subsets');}
  else{res.size13=countWanted(13);res.size14=countWanted(14);check(res.size13.n===560&&res.size14.n===119&&res.size14.missing.length===1&&res.size14.missing[0]===expected,'all required subsets');res.bad14=full(h3.filter((_,j)=>expected>>j&1),c);check(res.bad14===0,'subset 14 is not empty');}
  res.bad16=full(h3,c);check(res.bad16===0,'H3 is not empty');
  const a2pub=old['2'].records.find(x=>x.index===i&&x.swapped===sw);
  check(h2.every(t=>wt(wh(c,t)^a2pub.example_mask)===14),'a2 witness');
  res.a2Count=full(h2,c);check(res.a2Count===a2pub.full_H_weight14_count,'a2 count');
  out.push(res);
}
return {h2,h3,positionsOmitted:[omitted,omitted2],expected,out};
}
console.log(JSON.stringify(replay(rows,cat,old,bsrc,pinned),null,2));
