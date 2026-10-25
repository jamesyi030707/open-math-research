// Exact finite algebra for the specific residual candidate recorded on 2026-10-24.
// Run: node verify_quadratic_rigidity.js
// No dependencies, network, random search, or target-code construction.
// Basis is derived from Grassl's displayed [37,10,14] construction:
// https://www.codetables.de/BKLC/BKLC.php?k=10&n=37&q=2
"use strict";
const basis = ["0x17e7146801","0x6293dc808","0xf714c2017","0x35dfc802d","0xb1f3485c","0x63e6a0ae","0x65be14f","0x196fc233","0x3e690ce6","0xcb73897"];
function popcount(x) { let n=0; while(x) { x &= x-1n; n++; } return n; }
function requireTrue(x, label) { if(!x) throw new Error(label); }
function monomials(u) {
  let row=0n, bit=0n;
  for(let i=0;i<10;i++) row |= BigInt((u>>i)&1) << bit++;
  for(let i=0;i<10;i++) for(let j=i+1;j<10;j++)
    row |= BigInt(((u>>i)&1)*((u>>j)&1)) << bit++;
  return row;
}
const rows=basis.map(BigInt), words=[], minimum=[], histogram={};
for(let u=0;u<1024;u++) {
  let word=0n;
  for(let i=0;i<10;i++) if((u>>i)&1) word ^= rows[i];
  words.push(word);
  const w=popcount(word); histogram[w]=(histogram[w]||0)+1;
  requireTrue(w%2===0,"Residual code must be even");
  if(w===14) minimum.push(u);
}
requireTrue(new Set(words.map(String)).size===1024,"Residual rank");
requireTrue(minimum.length===160,"Minimum-word count");
const coefficientMask=(1n<<55n)-1n, pivots=new Map(), independentMessages=[];
let consistent=true;
for(const u of minimum) {
  let row=monomials(u)|(1n<<55n), inserted=false;
  for(let j=54;j>=0;j--) if((row>>BigInt(j))&1n) {
    if(pivots.has(j)) row ^= pivots.get(j);
    else { pivots.set(j,row); independentMessages.push(u); inserted=true; break; }
  }
  if(!inserted && (row&coefficientMask)===0n && ((row>>55n)&1n)) consistent=false;
}
requireTrue(consistent && pivots.size===55,"Unique quadratic form");
let solution=0n;
for(const [j,row] of [...pivots].sort((a,b)=>a[0]-b[0])) {
  const known=popcount((row&coefficientMask)&solution)%2;
  const rhs=Number((row>>55n)&1n);
  if(known!==rhs) solution |= 1n<<BigInt(j);
}
let mismatches=0;
for(let u=0;u<1024;u++) {
  if(popcount(solution&monomials(u))%2 !== (popcount(words[u])/2)%2) mismatches++;
}
requireTrue(mismatches===0,"Form equals residual half-weight mod 2");
const minSet=new Set(minimum);
let triangles=0;
for(let i=0;i<minimum.length;i++) for(let j=i+1;j<minimum.length;j++) {
  const w=minimum[i]^minimum[j];
  if(w>minimum[j] && minSet.has(w)) triangles++;
}
// Check every minimum-word equation explicitly.
const evaluations=minimum.map(u=>popcount(solution&monomials(u))%2);
requireTrue(evaluations.every(x=>x===1),"All prescribed values");
console.log(JSON.stringify({
  length:37, dimension:10, histogram, minimum_messages:160,
  quadratic_columns:55, evaluation_rank:pivots.size,
  unique_solution_hex:"0x"+solution.toString(16),
  all_message_comparison_count:1024, mismatches,
  xor_triangles:triangles,
  independent_messages:independentMessages,
  claim:"Any distance-27 lift of this specific residual has a doubly-even even subcode; no lift existence or exclusion is asserted."
}, null, 2));
