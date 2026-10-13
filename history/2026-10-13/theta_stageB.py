#!/usr/bin/env python3
"""
STAGE B of the Theta-pruning pilot (caps DECLARED BEFORE RUNNING): <= 25,000,000 states (reverse nodes) per run, <= 60 s wall per run, <= 256 MB peak RSS; exceeding => INCOMPLETE.
Stage A (theta_pilot.py, caps 5M states) found J=65 INCOMPLETE at the 5M cap; stage B raises only the state cap, runs Theta mode (stage-B binary, regression-identical to stage A at J=46,58)
at J = 65, 72, 80, 92.  Mode 0 (yesterday's pruning) is re-run ONLY at J=72 (logged 53.5M nodes, reference cap 6e7) to dump its candidate set; at J=65 the stage-A mode-0 candidate file is reused.
The unpruned billion-node J=92 traversal and the J=300 scan are NOT repeated.  Baseline = preserved certificates (hash-checked); the forward C scan is only RE-TIMED (<=0.05 s) for a wall-time comparison.
"""
import hashlib, json, os, subprocess, time
B = os.environ["THETA_BIN_B"]; SCAN = os.environ["PARADOX_SCAN"]; CAP, TCAP, MEM = 25_000_000, 60, 262144
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
logged = {}
for f in ("inverse_pilot_results.json", "inverse_pilot_stage2_results.json"):
    for r in json.load(open(f))["rows"]: logged[r["J"]] = r
logged[92] = json.load(open("inverse_pilot_stage3_J92_results.json"))
def run(mode, J, cert, cap):
    h, c = f"theta_hits_m{mode}_J{J}_B.txt", f"theta_cand_m{mode}_J{J}_B.txt"
    t = time.time(); r = subprocess.run([B, str(mode), str(J), str(cert["Hmax"]), f"qmax_J{J}.txt", str(cap), str(TCAP), h, c], capture_output=True, text=True); wall = time.time() - t
    out = r.stdout.splitlines(); st = dict(kv.split("=") for kv in [l for l in out if l.startswith("RESULT")][0].split()[1:])
    dt = [int(x) for x in [l for l in out if l.startswith("DEPTH_TOTAL")][0].split()[1:]]; de = [int(x) for x in [l for l in out if l.startswith("DEPTH_ESSENTIAL")][0].split()[1:]]
    return dict(st=st, hits={tuple(map(int, l.split())) for l in open(h)}, cand={int(l) for l in open(c)}, dt=dt, de=de, wall=wall, hsha=sha(h), csha=sha(c))
rows = []
for J in (65, 72, 80, 92):
    cert = json.load(open(f"paradox_cert_J{J}.json")); assert sha(f"paradox_cert_J{J}.json") == logged[J]["baseline_cert_sha256"]
    base = {tuple(x) for x in cert["hits"]}; yest = {tuple(map(int, l.split())) for l in open(f"inv_hits_J{J}.txt")}
    assert yest == base and sha(f"inv_hits_J{J}.txt") == logged[J]["inv_hits_sha256"]
    t = time.time(); subprocess.run([SCAN, str(J), str(cert["Hmax"] and cert["X"]), f"qmax_J{J}.txt"], capture_output=True, check=True); tscan = time.time() - t
    b = run(1, J, cert, CAP); st = b["st"]; comp = st["status"] == "0"
    cand0 = None; m0nodes = None
    if J == 65: cand0 = {int(l) for l in open("theta_cand_m0_J65.txt")}
    if J == 72:
        a = run(0, J, cert, 60_000_000); cand0 = a["cand"]; m0nodes = int(a["st"]["nodes"])
        assert m0nodes == logged[72]["inv_nodes"] and a["hits"] == base
    row = dict(J=J, X=cert["X"], Hmax=cert["Hmax"], anchors=int(st["anchors"]), baseline_scan_steps=(cert["X"] - 2) * J, baseline_scan_wall_s=round(tscan, 4), baseline_hits=len(base),
        logged_unpruned_nodes=logged[J]["inv_nodes"], theta_status="COMPLETE" if comp else {"1": "INCOMPLETE(state cap)", "2": "INCOMPLETE(time cap)", "3": "ABORTED(guard)"}[st["status"]],
        theta_nodes=int(st["nodes"]), node_reduction_vs_unpruned=round(logged[J]["inv_nodes"] / max(1, int(st["nodes"])), 2), theta_candidates=len(b["cand"]),
        theta_hit_triples=int(st["hit_triples"]), distinct_hit_starts=len({t_[0] for t_ in b["hits"]}), theta_hits_equal_baseline=(b["hits"] == base),
        candidates_subset_of_unpruned=(None if cand0 is None else b["cand"] <= cand0), candidates_equal_unpruned=(None if cand0 is None else b["cand"] == cand0),
        essential_nodes=int(st["essential_nodes"]), nodes_per_essential=round(int(st["nodes"]) / max(1, int(st["essential_nodes"])), 1),
        table_states=int(st["table_states"]), table_seconds=float(st["tbl_seconds"]), total_seconds=float(st["seconds"]), dfs_seconds=round(float(st["seconds"]) - float(st["tbl_seconds"]), 4),
        maxrss_kb=int(st["maxrss_kb"]), within_mem_cap=int(st["maxrss_kb"]) <= MEM, wall_ratio_theta_over_baseline=round(float(st["seconds"]) / max(tscan, 1e-9), 1),
        depth_total=b["dt"], depth_essential=b["de"], hits_sha256=b["hsha"], cand_sha256=b["csha"])
    rows.append(row); print(json.dumps({k: v for k, v in row.items() if not k.startswith("depth_")}))
json.dump(dict(caps=dict(states=CAP, seconds=TCAP, mem_kb=MEM), rows=rows, source_sha256=sha("inverse_orbit_theta.c"), driver_sha256=sha("theta_stageB.py")), open("theta_stageB_results.json", "w"), indent=1)
