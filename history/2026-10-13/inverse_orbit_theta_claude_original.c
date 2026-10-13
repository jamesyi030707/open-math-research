// inverse_orbit_theta.c (STAGE B: faster, equivalent table build + table timer; stage-A source preserved as inverse_orbit_theta_stageA.c) -- same reverse-edge/anchor enumeration as inverse_orbit.c (see inverse_orbit_note.md, lemmas L1-L5), two prune modes:
//   mode 0 = yesterday's P1/P2 (copied verbatim; regression: node counts must equal the logged ones)
//   mode 1 = Theta-table pruning (theta_pruning_proof.md): per anchor a table Th[d][o] of integer thresholds on w=v+1 computed by an exact integer DP.
// STATE of a reverse node for pruning purposes: (d,o,w) where d = reverse depth, o = #odd-pred edges so far, w=v+1.  The per-anchor memo is the table (d,o)->Theta.
//   Theta[d][o] = max( leaf(d,o), floor(Theta[d+1][o]*7/13) [d>=1; *4/7 at the root d=0], floor(3*Theta[d+1][o+1]/2) ),
//   leaf(d,o)  = max{ val[t]+1 : 1<=t<=J-d, o+sodd[t] <= qmax[d+t], o >= olo(d,t) },  olo(d,t)=ceil((d+log2(x0/val[t]))/log2(3*eta) - 1e-6), eta=1+1/(3(Hmax+1)).
// Both modes count: nodes, unique leaf tests (candidates), hit triples, ESSENTIAL nodes (nodes whose subtree contains a hit = a lower bound on any sound enumeration).
// Caps: node cap, wall-time cap; status 0 complete / 1 node cap / 2 time cap / 3 overflow guard.  Usage:
//   ./inverse_orbit_theta mode J Hmax qmax_file node_cap time_cap hits_out cand_out
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <sys/resource.h>
typedef unsigned __int128 u128;
#define MAXJ 128
#define OM 66
static int mode, J, Hmax, qmax[MAXJ + 2];
static u128 val[MAXJ + 2], PM[MAXJ + 2], pow3[64], Th[MAXJ + 2][OM + 2];
static int sodd[MAXJ + 2], ohi[MAXJ + 2];
static long double lval[MAXJ + 2];
static long long nodes, leaf_tests, hit_count, essential, node_cap, table_states, pruned_a, pruned_b, by_depth[MAXJ], ess_depth[MAXJ];
static double time_cap; static int status;
static struct timespec t0; static FILE *fh, *fc; static u128 x0;
static double now(void) { struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t); return (t.tv_sec - t0.tv_sec) + 1e-9 * (t.tv_nsec - t0.tv_nsec); }

static int prune0(u128 v, int d, int o) {                       // yesterday's P1/P2, verbatim
    int ohd = ohi[d];
    if (o > ohd) { pruned_a++; return 1; }
    int oo = ohd - o, r = J - 1 - d; if (oo > r) oo = r;
    u128 cap = PM[J - d];
    if (cap < 3) { pruned_b++; return 1; }
    u128 w = v + 1;
    if (oo > 60 || w >= ((u128)1 << 64) || cap >= ((u128)1 << 30)) { status = 3; return 0; }
    if ((w << oo) > (cap + 1) * pow3[oo]) { pruned_b++; return 1; }
    return 0;
}
static int prune1(u128 v, int d, int o) {                       // Theta table
    if (o > OM) { pruned_a++; return 1; }
    if (v + 1 > Th[d][o]) { pruned_b++; return 1; }
    return 0;
}
static double tbl_seconds;
static void build_theta(void) {                      // stage-B form: identical table, built by interval updates (verified equal to stage A by regression)
    double ts = now();
    long double lg = log2l(3.0L * (1.0L + 1.0L / (3.0L * (Hmax + 1)))), lx = log2l((long double)x0);
    for (int d = J - 1; d >= 0; d--) {
        u128 leaf[OM + 2]; for (int o = 0; o <= OM; o++) leaf[o] = 0;
        for (int t = 1; t <= J - d; t++) {
            int hi = qmax[d + t] - sodd[t]; if (hi > OM) hi = OM; if (hi < 0) continue;
            long double L = ((long double)d + lx - lval[t]) / lg;
            long long olo = (long long)ceill(L - 1e-6L); if (olo < 0) olo = 0; if (olo > hi) continue;
            for (int o = (int)olo; o <= hi; o++) if (val[t] + 1 > leaf[o]) leaf[o] = val[t] + 1;
        }
        for (int o = 0; o <= OM; o++) {
            u128 E = 0, O = 0;
            if (d < J - 1) {
                E = (d == 0) ? (Th[1][o] * 4) / 7 : (Th[d + 1][o] * 7) / 13;
                if (o + 1 <= OM) O = (3 * Th[d + 1][o + 1]) / 2;
            }
            u128 m = leaf[o]; if (E > m) m = E; if (O > m) m = O;
            if (m >= ((u128)1 << 100)) { status = 3; return; }
            Th[d][o] = m; table_states++;
        }
    }
    tbl_seconds += now() - ts;
}
static int dfs(u128 v, int d, int o) {
    if (status) return 0;
    nodes++; by_depth[d]++;
    if (nodes > node_cap) { status = 1; return 0; }
    if ((nodes & 0xFFFF) == 0 && now() > time_cap) { status = 2; return 0; }
    int found = 0;
    if (v >= 3 && v <= PM[J - d]) {
        leaf_tests++; fprintf(fc, "%llu\n", (unsigned long long)v);
        for (int t = 1; t <= J - d; t++)
            if (v <= val[t] && o + sodd[t] <= qmax[d + t]) { hit_count++; found = 1; fprintf(fh, "%llu %d %d\n", (unsigned long long)v, d + t, o + sodd[t]); }
    }
    if (d < J - 1) {
        u128 w = 2 * v;
        if (!(mode ? prune1(w, d + 1, o) : prune0(w, d + 1, o))) found |= dfs(w, d + 1, o);
        if (status) return found;
        if (v % 3 == 2) {
            u128 u = (2 * v - 1) / 3;
            if (u > (u128)Hmax && !(mode ? prune1(u, d + 1, o + 1) : prune0(u, d + 1, o + 1))) found |= dfs(u, d + 1, o + 1);
        }
    }
    if (found) { essential++; ess_depth[d]++; }
    return found;
}
int main(int argc, char **argv) {
    if (argc < 9) { fprintf(stderr, "usage\n"); return 2; }
    mode = atoi(argv[1]); J = atoi(argv[2]); Hmax = atoi(argv[3]); node_cap = atoll(argv[5]); time_cap = atof(argv[6]);
    FILE *f = fopen(argv[4], "r"); for (int j = 1; j <= J; j++) if (fscanf(f, "%d", &qmax[j]) != 1) return 2; fclose(f);
    if (qmax[J] > 60 || Hmax < 5) { fprintf(stderr, "guard: qmax/Hmax out of supported range\n"); return 2; }
    fh = fopen(argv[7], "w"); fc = fopen(argv[8], "w"); clock_gettime(CLOCK_MONOTONIC, &t0);
    pow3[0] = 1; for (int i = 1; i < 64; i++) pow3[i] = pow3[i - 1] * 3;
    int anchors = 0;
    for (int a = 3; a <= Hmax && !status; a += 2) {
        x0 = a; anchors++;
        u128 x = a; val[0] = a; sodd[0] = 0; PM[0] = 0;
        for (int t = 1; t <= J; t++) { sodd[t] = sodd[t - 1] + (int)(x & 1); x = (x & 1) ? (3 * x + 1) / 2 : x / 2; val[t] = x; lval[t] = log2l((long double)x); PM[t] = (t == 1 || val[t] > PM[t - 1]) ? val[t] : PM[t - 1]; }
        for (int d = 0; d <= J - 1; d++) { int best = -100000; for (int s0 = d; s0 <= J - 1; s0++) for (int t = 1; t <= J - s0; t++) { int v = qmax[s0 + t] - sodd[t]; if (v > best) best = v; } ohi[d] = best; }
        if (mode) { build_theta(); if (status) break; if ((u128)a + 1 > Th[0][0]) continue; }
        dfs(a, 0, 0);
    }
    fclose(fh); fclose(fc);
    struct rusage ru; getrusage(RUSAGE_SELF, &ru);
    printf("RESULT mode=%d J=%d Hmax=%d anchors=%d status=%d nodes=%lld leaf_tests=%lld hit_triples=%lld essential_nodes=%lld pruned_a=%lld pruned_b=%lld table_states=%lld tbl_seconds=%.4f seconds=%.4f maxrss_kb=%ld node_cap=%lld time_cap=%.0f\n",
           mode, J, Hmax, anchors, status, nodes, leaf_tests, hit_count, essential, pruned_a, pruned_b, table_states, tbl_seconds, now(), ru.ru_maxrss, node_cap, time_cap);
    printf("DEPTH_TOTAL"); for (int d = 0; d < J; d++) printf(" %lld", by_depth[d]); printf("\nDEPTH_ESSENTIAL"); for (int d = 0; d < J; d++) printf(" %lld", ess_depth[d]); printf("\n");
    return status ? 1 : 0;
}
