#!/usr/bin/env python3
"""
STAGE 2 of the bounded inverse-orbit pilot (declared BEFORE running; amendment disclosed: after stage 1, whose J=92 projection mixed Hmax regimes,
I changed only the projection method, not the caps).
  caps unchanged: node cap 3e8, wall-time cap 90 s per run, memory O(J).  Pilots J = 52,58,65,72,80,86 in order (J=65..148 all have Hmax=1192).
  STOP: first run that hits a cap/guard (INCOMPLETE, proves nothing) or takes >30 s.
  J=92 is attempted ONLY IF the log-linear projection from the last TWO completed runs that share the same Hmax is <= the node cap;
  then it is compared with the EXISTING certificate paradox_cert_J92.json (baseline NOT rescanned; baseline steps = (X-2)*J).
"""
import hashlib, json, os, subprocess, sys, time
SCAN = os.environ["PARADOX_SCAN"]; INV = os.environ["INVERSE_ORBIT"]
NODE_CAP, TIME_CAP = 300_000_000, 90
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
def run_inv(J, cert):
    r = subprocess.run([INV, str(J), str(cert["Hmax"]), f"qmax_J{J}.txt", str(NODE_CAP), str(TIME_CAP), f"inv_hits_J{J}.txt"], capture_output=True, text=True)
    st = dict(kv.split("=") for kv in [l for l in r.stdout.splitlines() if l.startswith("RESULT")][0].split()[1:])
    inv = {tuple(map(int, l.split())) for l in open(f"inv_hits_J{J}.txt")}; base = {tuple(h) for h in cert["hits"]}; s = int(st["status"])
    return dict(J=J, X=cert["X"], Hmax=cert["Hmax"], anchors=int(st["anchors"]), baseline_hits=len(base), baseline_scan_steps=(cert["X"] - 2) * J,
        inv_status={0: "COMPLETE", 1: "INCOMPLETE(node cap)", 2: "INCOMPLETE(time cap)", 3: "ABORTED(overflow guard)"}[s], inv_nodes=int(st["nodes"]),
        inv_unique_candidates_leaf_tests=int(st["leaf_tests"]), inv_leaf_inner_steps=int(st["leaf_inner"]), inv_hit_triples=int(st["hit_triples"]),
        inv_seconds=float(st["seconds"]), inv_maxrss_kb=int(st["maxrss_kb"]), pruned_P2=int(st["pruned_P2"]), inv_equals_baseline=(inv == base),
        inv_subset_of_baseline=(inv <= base), inv_hits_sha256=sha(f"inv_hits_J{J}.txt"), baseline_cert_sha256=sha(f"paradox_cert_J{J}.json")), s
rows, done = [], []
for J in (52, 58, 65, 72, 80, 86):
    subprocess.run([sys.executable, "paradox_gen.py", str(J)], check=True, capture_output=True, env=os.environ)
    cert = json.load(open(f"paradox_cert_J{J}.json"))
    t = time.time(); subprocess.run([SCAN, str(J), str(cert["X"]), f"qmax_J{J}.txt"], capture_output=True, check=True); tb = time.time() - t
    row, s = run_inv(J, cert); row["baseline_scan_seconds"] = round(tb, 4); rows.append(row); print(json.dumps(row))
    if s: print("STOP: cap/guard hit -> INCOMPLETE"); break
    done.append((J, row["inv_nodes"], row["Hmax"]))
    if row["inv_seconds"] > 30: print("STOP: >30 s"); break
proj = None; same = [d for d in done if d[2] == 1192]
if len(same) >= 2:
    (J1, N1, _), (J2, N2, _) = same[-2], same[-1]; g = (N2 / N1) ** (1 / (J2 - J1)); proj = N2 * g ** (92 - J2)
    print(f"same-Hmax growth/J = {g:.4f}; projected nodes at J=92 = {proj:.3g} (cap {NODE_CAP:.0e})")
    if proj <= NODE_CAP:
        cert = json.load(open("paradox_cert_J92.json"))
        row, s = run_inv(92, cert); row["baseline_scan_seconds"] = "not rerun (existing certificate)"; rows.append(row); print(json.dumps(row))
    else: print("J=92 NOT run (projection above cap)")
json.dump(dict(node_cap=NODE_CAP, time_cap_s=TIME_CAP, rows=rows, projected_nodes_J92=proj, source_sha256=sha("inverse_orbit.c"), driver_sha256=sha("inverse_orbit_stage2.py")),
          open("inverse_pilot_stage2_results.json", "w"), indent=1)
