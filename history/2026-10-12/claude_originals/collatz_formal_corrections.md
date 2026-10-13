# Formal corrections: G6 / theta_r and w_m  (no computation repeated; numbers quoted from theta_and_w_log.txt)

Notation: T(n)=n/2 | (3n+1)/2; a class r mod 2^k fixes a parity word, hence s_j (odd steps among the first j), b_j>=0 and D_j=2^j-3^{s_j} (never 0, j>=1)
with T^j(n)=(3^{s_j} n + b_j)/2^j for all n=r (mod 2^k). sigma(n)=min{j>=1: T^j(n)<n}, tau(n)=min{j: D_j>0 along n's word}, t(n)=sigma(n).

## A. G6 corrected (supersedes the earlier "iff the first threshold passes")
* **G6a (exact class criterion; theorem).** theta_r := min{ b_j/D_j : 1<=j<=k, D_j>0 } (= infinity if no such j). For n in the class: sigma(n) <= k  <=>  n > theta_r.
  Proof: T^j(n)<n <=> D_j>0 and b_j < D_j n; "exists j" <=> n exceeds the minimum of the real numbers b_j/D_j over D_j>0.
* **G6b (first threshold is sufficient only).** Let j* be the least j with D_j>0. If n > b_{j*}/D_{j*} then sigma(n)=j* exactly (D_j<0 for j<j*). Since theta_r <= b_{j*}/D_{j*}, "first threshold passes" implies the theta-criterion. The converse is NOT proved and not claimed:
  an n with n <= b_{j*}/D_{j*} could still descend at a later j<=k. No actual integer exhibiting this is known to me (and none can exist while CST holds, see G6d).
* **G6c (classification, theorem).** "for all n>1: sigma(n)<=k <=> n lies in a covered class mod 2^k" holds iff every covered class has least n>1 greater than its theta_r. ("=>" of the classification is automatic: open classes have D_j<0 for all j<=k, so T^j(n)>n.)
* **G6d (link to Terras' CST, Rozier–Terracol C1).** If a cylinder's least n>1 fails the first-threshold test then T^{j*}(n)>=n with tau(n)=j*, i.e. t(n)>tau(n): a CST counterexample. Conversely a CST counterexample n gives a failing cylinder. So "first threshold passes for all cylinders of all lengths" <=> CST (Rozier–Terracol report CST checked for 2<=n<=2.8e19; their scope is far larger than anything computed here).
* **Logged finite facts (theta_and_w_log.txt, not rerun).** For every k=1..14 both the classification and the first-threshold condition hold; at k=12: 3870 covered classes, max theta = max first-threshold = 319/13 (~24.54), 1481 classes have theta_r strictly below their first threshold (so the theta-criterion is genuinely finer); exact-criterion mismatches for 2<=n<=60000: 0 for all k<=14.

## B. w_m = (3^m-1)/2^v, v=v2(3^m-1), e=v2(m)
* **W1 (Lemma V)** v=1 (m odd); v=2+e (m even). Proof for m even: 3^m-1 = (3^q-1)(3^q+1)(3^{2q}+1)...(3^{2^{e-1}q}+1), m=2^e q: valuations 1, 2 (3^q+1=4 mod 8), and 1 for each of the other e-1 factors (odd square +1 = 2 mod 8): total 2+e. (Same as LTE: v2(x^m-y^m)=v2(x-y)+v2(x+y)+v2(m)-1 for odd x,y, even m.)
* **W2** m,m' in the same layer (v2(m)=v2(m')=e), d=m'-m: v2(w_{m'}-w_m) = 1+v2(d) if e=0; = v2(d)-e if e>=1.
  Proof: w'-w = 3^m (3^d-1)/2^v; d is even so v2(3^d-1)=2+v2(d); subtract v. (For e>=1, v2(d)>=e+1, so the value is >=1, consistent with w,w' odd.) Logged: 14,871 same-layer pairs with m<m'<=300, 0 violations.
* **W3 (exact minimal translation periods; supersedes the retracted claim and the "sufficient, not minimal" remark).** The first L branches of w depend exactly on w mod 2^L (G2: words <-> classes). Hence within a layer W_L(m)=W_L(m') <=> v2(d) >= L-1 (e=0) or v2(d) >= L+e (e>=1).
  Minimal periods: 2^{L-1} (m odd, L>=3), 2^{e+L} (m even, L>=2). Degenerate small L (logged): m odd with L<=2 and m even with L=1 have W_L constant on the layer (period 1), where the formula exponent is not minimal.
  The original unconditional "m mod 2^{L-1}" claim is false: m=2,6 (w=1, 91; W_3=101 vs 110).
* **W4** m odd: 3^m = 3 (mod 8) so w = 1 (mod 4); for m>=3, w>1 and T^2(w)=(3w+1)/4 < w. (m=1: w=1, T^2(1)=1, not <.)
* **W5 (finite fact, k=12).** For e>=1 the map q mod 4096 -> w mod 4096 is a bijection onto the 2048 odd residues (checked for e=1,2); 1822 of them lie in the 3870 certified classes, fraction 911/1024; direct sigma<=12 agrees with class membership for every m!=2 tested (m=2: w=1 is the n=1 exception).
  **Meaning:** this concerns descent of w_m below w_m itself (w_m ~ 1.5^m (2^m-1)), a fixed-L statement; it says nothing about sigma(2^m-1) and nothing about global convergence.
