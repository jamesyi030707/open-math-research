// inverse_orbit.c -- bounded inverse-orbit enumeration of paradoxical sequences  P(<=J) = {(n,j): n>=3, j<=J, 3^q<2^j, T^j(n)>=n}.
// T(n)=n/2 (even), (3n+1)/2 (odd).  q = #odd among n,...,T^{j-1}(n).
//
// CONSTRUCTION (all statements proved in inverse_orbit_note.md; nothing below is a heuristic cut):
//  Anchor of a hit (n,j): x0 = a_{s0}, s0 = FIRST index s in [0,j-1] with a_s odd and 3<=a_s<=Hmax (exists: the smallest odd value m_o<=H(j)<=Hmax).
//    * head a_0..a_{s0-1}: every ODD head term is > Hmax (not in [3,Hmax] by minimality of s0; not 1 because then a_j<=2<n).
//    * tail a_{s0}..a_j: a_j = T^t(x0), t=j-s0>=1  (so s0<=j-1<=J-1 and 1<=t<=J-s0).
//  Reverse T edges: preds(v) = {2v} U {(2v-1)/3 if v=2 mod 3}  (the odd pred is odd and > Hmax is REQUIRED for head nodes).
//  Every hit start n is a node at reverse depth d=s0 of the tree rooted at its anchor x0; the node-to-root path is its true orbit, so the
//  leaf test below is EXACT:   (n,j=d+t) is a hit  <=>  n<=T^t(x0)  and  o+sodd[x0][t] <= qmax[d+t]   (o = #odd head terms).
//  Distinct n have distinct (anchor,path) => no duplicates.
// SOUND PRUNINGS (applied to an inverse node v at depth d with o odd-pred edges so far; w=v+1, E-edge: w'=2w-1>=1.5w (w>=2), O-edge: w'=(2/3)w exactly):
//   P1 o > ohi[d] (ohi[d] = max over s0>=d, t of qmax[s0+t]-sodd[x0][t]: a hit needs q<=qmax[j])
//   P2 w*(2/3)^{o'} > cap_d+1, o' = min(J-1-d, ohi[d]-o), cap_d = max_{1<=t<=J-d} T^t(x0)   (the leaf n must be <= cap at its own depth >= d)
//   This is a DEPTH-DEPENDENT bound on INTERMEDIATE nodes; it does NOT cut at X, and uses no 'descent' argument.
// RESOURCE CAPS: node cap, wall-time cap (checked every 2^20 nodes), memory O(J) (DFS) + hits.  If a cap is hit the run is reported INCOMPLETE.
// OVERFLOW GUARDS (explicit, abort => status 3): w>=2^64, o'>60, cap>=2^30 (then w<<o' < 2^124 and (cap+1)*3^o' < 2^125 fit in u128).
// Usage: ./inverse_orbit J Hmax qmax_file node_cap time_cap_s hits_out
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <sys/resource.h>
typedef unsigned __int128 u128;
static int J, Hmax, qmax[1024];
static u128 val[1024], PM[1024], pow3[64];
static int sodd[1024], ohi[1024];
static long long leaf_inner, nodes, leaf_tests, hit_count, node_cap, by_depth[1024], pruned_P1, pruned_P2;
static double time_cap; static int status;      // 0 complete, 1 node cap, 2 time cap, 3 overflow guard
static struct timespec t0;
static FILE *fh;
static double now(void) { struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t); return (t.tv_sec - t0.tv_sec) + 1e-9 * (t.tv_nsec - t0.tv_nsec); }
static u128 x0;

static int prune(u128 v, int d, int o) {
    int ohd = ohi[d];
    if (o > ohd) { pruned_P1++; return 1; }
    int oo = ohd - o, r = J - 1 - d; if (oo > r) oo = r;
    u128 cap = PM[J - d];
    if (cap < 3) { pruned_P2++; return 1; }
    u128 w = v + 1;
    if (oo > 60 || w >= ((u128)1 << 64) || cap >= ((u128)1 << 30)) { status = 3; return 0; }
    if ((w << oo) > (cap + 1) * pow3[oo]) { pruned_P2++; return 1; }
    return 0;
}
static void dfs(u128 v, int d, int o) {
    if (status) return;
    nodes++; by_depth[d]++;
    if (nodes > node_cap) { status = 1; return; }
    if ((nodes & 0xFFFFF) == 0 && now() > time_cap) { status = 2; return; }
    if (v >= 3 && v <= PM[J - d]) {
        leaf_tests++; leaf_inner += J - d;
        for (int t = 1; t <= J - d; t++)
            if (v <= val[t] && o + sodd[t] <= qmax[d + t]) { hit_count++; fprintf(fh, "%llu %d %d\n", (unsigned long long)v, d + t, o + sodd[t]); }
    }
    if (d == J - 1) return;
    u128 w = 2 * v;
    if (!prune(w, d + 1, o)) dfs(w, d + 1, o);
    if (status) return;
    if (v % 3 == 2) {
        u128 u = (2 * v - 1) / 3;
        if (u > (u128)Hmax && !prune(u, d + 1, o + 1)) dfs(u, d + 1, o + 1);
    }
}
int main(int argc, char **argv) {
    if (argc < 7) { fprintf(stderr, "usage\n"); return 2; }
    J = atoi(argv[1]); Hmax = atoi(argv[2]); node_cap = atoll(argv[4]); time_cap = atof(argv[5]);
    FILE *f = fopen(argv[3], "r"); for (int j = 1; j <= J; j++) if (fscanf(f, "%d", &qmax[j]) != 1) return 2; fclose(f);
    fh = fopen(argv[6], "w"); clock_gettime(CLOCK_MONOTONIC, &t0);
    pow3[0] = 1; for (int i = 1; i < 64; i++) pow3[i] = pow3[i - 1] * 3;
    int anchors = 0;
    for (int a = 3; a <= Hmax && !status; a += 2) {
        x0 = a; anchors++;
        u128 x = a; val[0] = a; sodd[0] = 0; PM[0] = 0;
        for (int t = 1; t <= J; t++) { sodd[t] = sodd[t - 1] + (int)(x & 1); x = (x & 1) ? (3 * x + 1) / 2 : x / 2; val[t] = x; PM[t] = (t == 1 || val[t] > PM[t - 1]) ? val[t] : PM[t - 1]; }
        for (int d = 0; d <= J - 1; d++) {          // ohi[d]
            int best = -100000;
            for (int s0 = d; s0 <= J - 1; s0++) for (int t = 1; t <= J - s0; t++) { int v = qmax[s0 + t] - sodd[t]; if (v > best) best = v; }
            ohi[d] = best;
        }
        dfs(a, 0, 0);
    }
    fclose(fh);
    struct rusage ru; getrusage(RUSAGE_SELF, &ru);
    printf("RESULT J=%d Hmax=%d anchors=%d status=%d nodes=%lld leaf_tests=%lld leaf_inner=%lld hit_triples=%lld pruned_P1=%lld pruned_P2=%lld seconds=%.3f maxrss_kb=%ld node_cap=%lld time_cap=%.0f\n",
           J, Hmax, anchors, status, nodes, leaf_tests, leaf_inner, hit_count, pruned_P1, pruned_P2, now(), ru.ru_maxrss, node_cap, time_cap);
    printf("DEPTH_HIST"); for (int d = 0; d < J; d++) printf(" %lld", by_depth[d]); printf("\n");
    return status ? 1 : 0;
}
