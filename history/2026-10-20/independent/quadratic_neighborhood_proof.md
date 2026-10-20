# A quadratic-neighborhood obstruction for the fixed parent

Date: 2026-10-20. Status: proved necessary condition, with a small exhaustive component. AI-assisted research note; no originality claim. This does not construct an extension or establish global nonexistence of a binary [64,11,27] code.

## Statement

Let E be the specified extended binary BCH [64,10,28] code generated before extension by `0x2759262d5d506d`, in the coordinate labeling reconstructed by the accompanying script. Write E = RM(1,6) + Q, where Q is the three-dimensional space of quadratic quotient representatives. If an odd-weight Boolean truth table f has distance at least 27 from every word of E, then

**d(f, RM(2,6)) >= 13.**

In particular, an odd target cannot be obtained by flipping at most eleven positions of any quadratic Boolean function. Because RM(2,6) has even weights, an odd target's distance from any such function is odd, so a radius-twelve neighborhood is also excluded.

## Walsh conventions and exact calculation

For a Boolean function h on F2^6, set s_h(x)=(-1)^h(x) and W_h(a)=sum_x s_h(x)(-1)^(a dot x). The unnormalized Walsh transform squares to 64 times the identity. Since E contains every affine function added to each q in Q, the distance condition is equivalent to |W_(f+q)(a)| <= 10 for all q,a.

For a quadratic h of alternating bilinear rank rho, put A=2^(6-rho/2). Its Walsh support S has size 2^rho and nonzero values A epsilon(a), where epsilon(a) is a sign on S and zero elsewhere. Inversion gives

sum_a epsilon(a)(-1)^(a dot x) = (64/A) s_h(x).

Let g be any quadratic function, choose q in Q, and take h=g+q and u=f+q. If r=d(f,g)=d(u,h), then the following identity is exact:

sum_a epsilon(a) W_u(a) = (64/A) sum_x s_h(x)s_u(x) = (64/A)(64-2r).

The target upper bound |W_u|<=10 implies that the left side is at most 10|S|. For rho=4 this says 256-8r <= 160, hence r>=12. For rho=2 it gives 128-4r <= 40, hence r>=22. For rho=0 it gives 64-2r <=10, hence r>=27. All quadratic truth tables on six variables have even weight: equivalently, parity of the truth table is its full-degree-six ANF coefficient, which vanishes in degree at most two. Therefore r is odd, strengthening the first two bounds to 13 and 23.

## Why an appropriate non-bent translate always exists

The script reconstructs the actual fixed parent and its affine coordinates, extracts the fifteen homogeneous quadratic coefficients of its three quotient generators, and enumerates all 2^15=32768 homogeneous quadratic forms g. For each, it computes the exact GF(2) ranks of the eight forms g+q. None has all eight ranks equal to six. The minimum ranks 0,2,4 occur for 8,5208,27552 forms respectively. Thus every quadratic g has at least one translate of rank at most four, sufficient for the bound above.

Only homogeneous forms need enumeration. Adding any affine function to g or a quotient representative does not alter its alternating bilinear rank. It merely permutes and changes signs of Walsh coefficients, leaving support size and absolute amplitudes unchanged. The proof identity itself applies to the actual full functions, so it does not assume their affine parts vanish. The reconstructed quotient quadratic masks are 19053,24003,9757, using lexicographically ordered pairs (i,j), 0<=i<j<6.

As a separate exact normalization audit, the script explicitly calculates the full Walsh spectrum and inverse epsilon transform of every one of the 32768 homogeneous forms and checks the formulas above. This is supplementary finite checking; the transform inversion identity supplies the general argument, including arbitrary affine parts.

## Scope and reproducibility

Run `python check_quadratic_neighborhood.py`. It uses only the Python standard library and writes `quadratic_neighborhood_report.json`. The run completed in approximately two seconds. It neither installs a solver nor searches the 2^64 possible f.

This excludes a structured family of attempted constructions near quadratic functions. It does not eliminate the seven surviving aggregate distance distributions, establish that any such distribution is realizable, or determine whether the fixed parent has an admissible odd extension. The Walsh facts and rank method are classical tools; whether this particular packaged restriction has appeared elsewhere has not been established here.
