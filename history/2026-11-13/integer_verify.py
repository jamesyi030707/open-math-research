from collections import Counter
B=[0x17e7146801,0x6293dc808,0xf714c2017,0x35dfc802d,0xb1f3485c,0x63e6a0ae,0x65be14f,0x196fc233,0x3e690ce6,0xcb73897]
def bw(u):
 a=0
 for i,b in enumerate(B):
  if u>>i&1:a^=b
 return a.bit_count()
def need(a,s):
 if not a:raise ValueError(s)
def wmsg(t):return ((t&31)<<4)^(1008 if t>>5 else 0)
T=[6,15,20,28,39,46,53,61]
for r,coeff in [(4,[-1,-1,1,1,-1,-1,1,1]),(24,[-1,-1,1,1,1,1,-1,-1])]:
 cols=[v|((int(v in [8,16,24]) if r==4 else int(v not in [8,16,24]))<<5) for v in range(8,32)]+([32,0,0] if r==4 else [32,32,32])
 need(all(bw(2^wmsg(t))==14 for t in T),'required residual weights')
 need(sum(coeff)==0,'balanced equations')
 values=[sum(c*(-1)**((t&v).bit_count()%2) for t,c in zip(T,coeff)) for v in cols]
 need(values==[8 if j==12 else 0 for j in range(27)],'isolated sign')
 print({'r':r,'messages':[2^wmsg(t) for t in T],'coefficients':coeff,'isolated_column_1based':13,'column_label':cols[12],'linear_combination':values,'contradiction':'8 * y_13 = 0 but y_13 is +/-1'})
