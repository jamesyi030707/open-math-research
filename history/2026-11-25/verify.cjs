'use strict';
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const assert = require('node:assert/strict');
const here = __dirname;
const file = process.argv[2] || path.join(here, '../2026-11-15/h.json');
const raw = fs.readFileSync(file);
const blob = crypto.createHash('sha1').update('blob ' + raw.length + '\0').update(raw).digest('hex');
assert.equal(blob, '6c2f005c33236b54ed1850f78b7700fcb44b7237');
const {solutions: h} = JSON.parse(raw);
const {integerWitnesses: wt, mod8Certificates: certs} = JSON.parse(fs.readFileSync(path.join(here, 'certificates.json')));
function verify(h, wt) {
const check=(b,msg)=>{if(!b)throw Error(msg)};
const bit=n=>{let r=0;for(;n;n&=n-1)r^=1;return r};
const chi=(t,c)=>1-2*bit(t&c);
const B=[0x17e7146801n,0x6293dc808n,0xf714c2017n,0x35dfc802dn,0xb1f3485cn,0x63e6a0aen,0x65be14fn,0x196fc233n,0x3e690ce6n,0xcb73897n];
const rw=a=>{let w=0n;for(let i=0;i<10;i++)if(a>>i&1)w^=B[i];let n=0;for(;w;w&=w-1n)++n;return n};
const W=t=>((t&31)<<4)^(t&32?1008:0);
const H=Array.from({length:64},(_,t)=>t).filter(t=>rw(3^W(t))===14);
const C=(i,s)=>h[i].columns.map(c=>s?c^(5*bit(c&5)):c);
const lam=H.map(t=>[4,10,15,33].includes(t)?-1:1);
const F=Array.from({length:64},(_,c)=>H.reduce((x,t,k)=>x+lam[k]*chi(t,c),0));
const S=F.flatMap((x,c)=>x?[c]:[]);
check(H.join(',')==='0,4,5,10,11,15,18,19,23,25,33,46,54,56,60,61','H');
check(lam.reduce((a,b)=>a+b)===8 && F.every(x=>[0,8,-8].includes(x))&&S.length===16,'F');
check(F.flatMap((x,c)=>x<0?[c]:[]).join(',')==='10,16,33,59','negative signs');
const parity=[[],[]], totals=[];
for(const i of [19,115,139,163])totals.push([i,...[0,1].map(s=>C(i,s).filter(c=>F[c]!==0).length)]);
for(let s=0;s<2;s++)for(let i=0;i<h.length;i++)if(C(i,s).filter(c=>S.includes(c)).length%2===0)parity[s].push(i);
check(parity[0].length===128 && parity[0].join(',')===parity[1].join(','),'paired parity');
const integer=wt.map(([i,s,sparse])=>{
 const x=Array(27).fill(0);
 for(const [j,z] of sparse){check(Number.isInteger(j)&&j>=0&&j<27&&Number.isInteger(z)&&z>0&&x[j]===0,'sparse input');x[j]=z;}
 const c=C(i,s);
 const weights=H.filter(t=>t!==25&&t!==60).map(t=>c.reduce((sum,v,j)=>sum+bit(t&v)+chi(t,v)*x[j],0));
 check(weights.length===14&&weights.every(a=>a===14)&&x.reduce((a,b)=>a+b)===14&&Math.max(...x)>1,'relaxation');
 return [i,s,Math.max(...x),weights];
});
function solve(A,b,m){
 const mask=m-1,n=A[0].length,N=A.length;
 const R=A.map((r,i)=>[...r.map(a=>a&mask),b[i]&mask,...Array.from({length:N},(_,j)=>+(j===i))]);
 const used=[], D=[]; const cols=Array.from({length:n},(_,j)=>j);
 const div=v=>v?(v&-v):m;
 const certify=(a,k)=>{
   const lam=a.slice(n+1);
   let z=b.reduce((p,q,i)=>p+q*lam[i],0)&mask;
   const K=A[0].map((_,j)=>A.reduce((p,r,i)=>p+r[j]*lam[i],0)&mask);
   check(z%k!==0&&K.every(x=>x%k===0),'negative certificate');
   return {k,lambda:lam,rhs:z};
 };
 for(let r=0;r<N;r++){
   let d=m,i0=r,j0=-1;
   for(let i=r;i<N;i++)for(const j of cols){const q=div(R[i][j]);if(q<d){d=q;i0=i;j0=j;}}
   if(d===m){for(let i=r;i<N;i++)if(R[i][n])return certify(R[i],m);break;}
   [R[r],R[i0]]=[R[i0],R[r]];
   const a=R[r];if(a[n]%d)return certify(a,d);
   const odd=a[j0]/d;
   let inv=1;while((odd*inv&mask)!==1)inv+=2;
   for(let j=0;j<a.length;j++)a[j]=a[j]*inv&mask;
   check(a[j0]===d,'normalize');
   for(let i=r+1;i<N;i++){
     const y=R[i];const k=y[j0]/d;
     check(Number.isInteger(k),'clear');
     if(k)for(let j=0;j<a.length;j++)y[j]=(y[j]-k*a[j])&mask;
   }
   used.push(j0);D.push(d);cols.splice(cols.indexOf(j0),1);
 }
 const x=Array(n).fill(0);
 for(let i=used.length-1;i>=0;i--){
   const a=R[i],d=D[i],v=(a[n]-x.reduce((s,q,j)=>s+q*a[j],0))&mask;
   check(v%d===0,'backsolve');x[used[i]]=v/d;
 }
 check(A.every((r,i)=>((r.reduce((s,z,j)=>s+z*x[j],0)-b[i])&mask)===0),'positive certificate');
 return null;
}
const by={}, overlap={};
for(const m of [4,8,16]){
 const bad=[{},{}],classes=[{},{}];
 for(let s=0;s<2;s++)for(let i=0;i<h.length;i++){
   const c=C(i,s),A=H.map(t=>c.map(x=>chi(t,x))),b=H.map(t=>14-c.reduce((v,x)=>v+bit(t&x),0));
   const z=solve(A,b,m);
   if(z){bad[s][i]=z;classes[s][z.k]=(classes[s][z.k]||0)+1;}
 }
 const sets=bad.map(x=>Object.keys(x).map(Number));by[m]={bad,sets,classes};
 overlap[m]={count:sets.map(a=>a.length),paired:sets[0].join(',')===sets[1].join(','),outsideParity:sets.map((a,s)=>a.filter(i=>!parity[s].includes(i)))};
}
check(overlap[4].count.every(z=>z===0)&&overlap[8].count.every(z=>z===141)&&overlap[16].count.every(z=>z===141),'known modular totals');
check(by[8].sets.every((x,i)=>x.join(',')===by[16].sets[i].join(',')),'stabilization');
return {H,F,S,totals,parity,integer,by,overlap};

}
const r = verify(h, wt);
const eq=(a,b)=>assert.deepEqual(a,b);
eq(r.totals, [[19,8,8],[115,6,6],[139,8,8],[163,6,6]]);
eq(r.S, [0,7,10,13,16,23,26,29,33,36,40,45,50,55,59,62]);
const pop = n=> n===0 ? 0 : 1 + pop(n & (n-1));
const swap = c => c ^ (5*(pop(c&5)%2));
eq(r.S.map(swap).sort((a,b)=>a-b),r.S);
const extra=[0,1,4,5,14,16,17,259,262,263,272,274,275];
for(let o=0;o<2;o++){
 eq(r.overlap[8].outsideParity[o],extra);
 eq(r.by[8].sets[o],r.by[8].sets[0]);
 eq(certs[o].map(x=>x[0]),extra);
 for(const [i,{k,lambda,rhs}] of certs[o]){
  eq(k,8); eq(rhs,4); eq(lambda.length,16);
  const A=r.H.map(t=>h[i].columns.map(c=>(-1)**(pop(t&(o?swap(c):c))%2)));
  const b=A.map(row=>(1+row.reduce((s,x)=>s+x,0))/2);
  const mod=x=>((x%8)+8)%8;
  for(let j=0;j<27;j++) eq(mod(A.reduce((s,row,t)=>s+row[j]*lambda[t],0)),0);
  eq(mod(b.reduce((s,x,t)=>s+x*lambda[t],0)),4);
 }
}
console.log(JSON.stringify({scope:'fixed a=3 q24, original and swapped',controls:r.totals,parity:r.parity.map(x=>x.length),modular:r.overlap,integerWitnesses:r.integer.map(([i,s,m])=>[i,s,m])},null,2));
