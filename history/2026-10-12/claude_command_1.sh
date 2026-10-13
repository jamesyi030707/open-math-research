cd . && python3 - <<'EOF'
p='inverse_orbit.c'; s=open(p).read()
s=s.replace('static long long nodes, leaf_tests, hit_count,','static long long leaf_inner, nodes, leaf_tests, hit_count,')
s=s.replace('        leaf_tests++;\n','        leaf_tests++; leaf_inner += J - d;\n')
s=s.replace('leaf_tests=%lld hit_triples','leaf_tests=%lld leaf_inner=%lld hit_triples')
s=s.replace('nodes, leaf_tests, hit_count, pruned_P1','nodes, leaf_tests, leaf_inner, hit_count, pruned_P1')
open(p,'w').write(s)
EOF
gcc -O2 -Wall -o ./inverse_orbit inverse_orbit.c && echo compiled
cat > inverse_orbit_pilot.py <<'EOF'
#!/usr/bin/env python3
"""
Pilot driver for the bounded inverse-orbit experiment (see inverse_orbit.c and inverse_orbit_note.md).
Pre-declared budget and stopping rule (written BEFORE running):
  per-run caps: node cap 3e8, wall-time cap 90 s, memory O(J) (DFS; maxrss reported);  pilots J = 12,16,20,24,30,36,40,46 in this order;
  STOP RULE: stop increasing J after (a) any run that hits a cap (reported INCOMPLETE), or (b) any completed run taking >20 s, or
             (c) a log-linear projection (last two completed runs) of the NEXT pilot above the node cap.
  J=92 is run ONLY IF the projection from the last two completed pilots is <= the node cap; otherwise it is NOT run (projection reported).
Baseline per pilot J: certificate from paradox_gen.py (scan of [3,X(J)], X from the corrected first-J-iterates definition); the C scan is re-timed
  at these tiny J only.  The J=92 / J=300 baselines are NOT rerun here.
"""
import hashlib, json, os, re, subprocess, sys, time, math
SCAN = os.environ["PARADOX_SCAN"]; INV = os.environ["INVERSE_ORBIT"]
NODE_CAP, TIME_CAP = 300_000_000, 90
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
rows = []; completed = []
for J in (12, 16, 20, 24, 30, 36, 40, 46):
    if completed:
        (J1, N1), (J2, N2) = (completed[-2] if len(completed) > 1 else completed[-1]), completed[-1]
        if J2 > J1 and N1 > 0:
            g = (N2 / N1) ** (1.0 / (J2 - J1)); proj = N2 * g ** (J - J2)
            if proj > NODE_CAP: print(f"STOP before J={J}: projected nodes {proj:.3g} > cap"); break
    subprocess.run([sys.executable, "paradox_gen.py", str(J)], check=True, capture_output=True, env=os.environ)
    cert = json.load(open(f"paradox_cert_J{J}.json")); X, Hmax = cert["X"], cert["Hmax"]; base = {tuple(h) for h in cert["hits"]}
    t = time.time(); subprocess.run([SCAN, str(J), str(X), f"qmax_J{J}.txt"], capture_output=True, check=True); tb = time.time() - t
    r = subprocess.run([INV, str(J), str(Hmax), f"qmax_J{J}.txt", str(NODE_CAP), str(TIME_CAP), f"inv_hits_J{J}.txt"], capture_output=True, text=True)
    line = [l for l in r.stdout.splitlines() if l.startswith("RESULT")][0]; st = dict(kv.split("=") for kv in line.split()[1:])
    hist = [int(x) for x in [l for l in r.stdout.splitlines() if l.startswith("DEPTH_HIST")][0].split()[1:]]
    inv = {tuple(map(int, l.split())) for l in open(f"inv_hits_J{J}.txt")}
    status = int(st["status"])
    equal = (inv == base); subset = inv <= base
    row = dict(J=J, X=X, Hmax=Hmax, baseline_hits=len(base), baseline_scan_steps=(X - 2) * J, baseline_scan_seconds=round(tb, 4),
               inv_status={0: "COMPLETE", 1: "INCOMPLETE(node cap)", 2: "INCOMPLETE(time cap)", 3: "ABORTED(overflow guard)"}[status],
               inv_nodes=int(st["nodes"]), inv_unique_candidates_leaf_tests=int(st["leaf_tests"]), inv_leaf_inner_steps=int(st["leaf_inner"]),
               inv_hit_triples=int(st["hit_triples"]), inv_seconds=float(st["seconds"]), inv_maxrss_kb=int(st["maxrss_kb"]),
               inv_equals_baseline=equal, inv_subset_of_baseline=subset, pruned_P1=int(st["pruned_P1"]), pruned_P2=int(st["pruned_P2"]),
               max_depth_nodes=max(range(len(hist)), key=lambda d: hist[d]), baseline_cert_sha256=sha(f"paradox_cert_J{J}.json"),
               inv_hits_sha256=sha(f"inv_hits_J{J}.txt"))
    rows.append(row); print(json.dumps(row))
    if status == 0:
        completed.append((J, int(st["nodes"])))
        if float(st["seconds"]) > 20: print("STOP: run took >20 s"); break
    else: print("STOP: cap/guard hit; run is INCOMPLETE and proves nothing about completeness"); break
proj92 = None
if len(completed) >= 2:
    (J1, N1), (J2, N2) = completed[-2], completed[-1]; g = (N2 / N1) ** (1.0 / (J2 - J1)); proj92 = N2 * g ** (92 - J2)
    print(f"growth factor per unit J ~ {g:.4f}; projected nodes at J=92 ~ {proj92:.3g}  (node cap {NODE_CAP:.1g}); J=92 {'would be run' if proj92 <= NODE_CAP else 'NOT run'}")
json.dump(dict(node_cap=NODE_CAP, time_cap_s=TIME_CAP, rows=rows, projected_nodes_J92=proj92, source_sha256=sha("inverse_orbit.c"),
               driver_sha256=sha("inverse_orbit_pilot.py")), open("inverse_pilot_results.json", "w"), indent=1)
EOF
export PARADOX_SCAN=./paradox_scan INVERSE_ORBIT=./inverse_orbit
timeout 900 python3 inverse_orbit_pilot.py 2>&1 | tee inverse_pilot_log.txt
