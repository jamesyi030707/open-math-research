// Scan for paradoxical sequences (Rozier-Terracol Def. 1.1) for the map T(n)=n/2 | (3n+1)/2.
// For each n in [3,X] and each j in [1,J]: let q = number of odd terms among n,...,T^{j-1}(n).
// Report (n, j, q) iff  3^q < 2^j   (encoded as q <= qmax[j], table read from file)  and  T^j(n) >= n.
// Usage: ./paradox_scan J X qmax_table.txt > hits.txt      (qmax_table: one integer per line for j=1..J)
#include <stdio.h>
#include <stdlib.h>
typedef unsigned __int128 u128;
int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage\n"); return 1; }
    int J = atoi(argv[1]); long X = atol(argv[2]);
    int *qmax = calloc(J + 2, sizeof(int));
    FILE *f = fopen(argv[3], "r");
    for (int j = 1; j <= J; j++) if (fscanf(f, "%d", &qmax[j]) != 1) { fprintf(stderr, "bad table\n"); return 1; }
    fclose(f);
    for (long n = 3; n <= X; n++) {
        u128 x = (u128)n; int q = 0;
        for (int j = 1; j <= J; j++) {
            if (x & 1) { q++; x = (3 * x + 1) / 2; } else x = x / 2;
            if (q <= qmax[j] && x >= (u128)n)
                printf("%ld %d %d\n", n, j, q);
        }
    }
    return 0;
}
