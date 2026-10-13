#!/usr/bin/env python3
"""
STAGE 3 (declared before running; amendment disclosed): J=92 with node cap 2.5e9 (was 3e8 in stages 1-2) and wall-time cap 60 s, memory O(J).
Reason: the stage-2 same-regime projection (1.09e9 nodes, ~15 s, ~15 MB RSS) fits time/memory but exceeded the node cap I had pre-declared.
Baseline = EXISTING certificate paradox_cert_J92.json (not rescanned); baseline steps = (X-2)*J.  If a cap is hit the run is INCOMPLETE and proves nothing.
"""
import hashlib, json, os, subprocess
INV = os.environ["INVERSE_ORBIT"]; J = 92; NODE_CAP = 2_500_000_000; TIME_CAP = 60
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
cert = json.load(open("paradox_cert_J92.json")); base = {tuple(h) for h in cert["hits"]}
r = subprocess.run([INV, str(J), str(cert["Hmax"]), "qmax_J92.txt", str(NODE_CAP), str(TIME_CAP), "inv_hits_J92.txt"], capture_output=True, text=True)
line = [l for l in r.stdout.splitlines() if l.startswith("RESULT")][0]; st = dict(kv.split("=") for kv in line.split()[1:])
inv = {tuple(map(int, l.split())) for l in open("inv_hits_J92.txt")}; s = int(st["status"])
row = dict(J=J, X=cert["X"], Hmax=cert["Hmax"], anchors_processed=int(st["anchors"]), baseline_hits=len(base), baseline_scan_steps=(cert["X"] - 2) * J,
           inv_status={0: "COMPLETE", 1: "INCOMPLETE(node cap)", 2: "INCOMPLETE(time cap)", 3: "ABORTED(overflow guard)"}[s], inv_nodes=int(st["nodes"]),
           inv_unique_candidates_leaf_tests=int(st["leaf_tests"]), inv_leaf_inner_steps=int(st["leaf_inner"]), inv_hit_triples=int(st["hit_triples"]),
           inv_seconds=float(st["seconds"]), inv_maxrss_kb=int(st["maxrss_kb"]), inv_equals_baseline=(inv == base), inv_subset_of_baseline=(inv <= base),
           distinct_hit_starts=len({t[0] for t in inv}), node_cap=NODE_CAP, time_cap_s=TIME_CAP, inv_hits_sha256=sha("inv_hits_J92.txt"),
           baseline_cert_sha256=sha("paradox_cert_J92.json"), source_sha256=sha("inverse_orbit.c"))
print(json.dumps(row)); json.dump(row, open("inverse_pilot_stage3_J92_results.json", "w"), indent=1)
