#!/usr/bin/env python3
"""
Modest pilot of the Theta-table pruning (theta_pruning_proof.md) against the EXISTING unpruned (P1/P2) inverse-orbit result.
CAPS DECLARED BEFORE RUNNING: <= 5,000,000 states (reverse nodes) per run, <= 60 s wall per run, <= 256 MB peak RSS (maxrss reported); exceeding => INCOMPLETE.
Pilots J = 46, 58, 65.  Mode 0 (yesterday's pruning, verbatim) is re-run only to (i) regress against the logged node counts and (ii) dump its candidate set;
at J=65 its logged count (18.3M) exceeds the 5M-state cap, so there it runs under a separate reference cap of 3e7 (flagged), NOT as a pilot of the new method.
Baseline certificates and yesterday's hit files are the preserved existing artifacts (hash-checked); nothing is rescanned and no J=92/J=300 run is repeated.
"""
import hashlib, json, os, subprocess
INV = os.environ["THETA_BIN"]; NODE_CAP, TIME_CAP, MEM_KB = 5_000_000, 60, 262144
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
logged = {}
for f in ("inverse_pilot_results.json", "inverse_pilot_stage2_results.json"):
    for r in json.load(open(f))["rows"]: logged[r["J"]] = r
def run(mode, J, cert, cap, tag):
    h, c = f"theta_hits_m{mode}_J{J}.txt", f"theta_cand_m{mode}_J{J}.txt"
    r = subprocess.run([INV, str(mode), str(J), str(cert["Hmax"]), f"qmax_J{J}.txt", str(cap), str(TIME_CAP), h, c], capture_output=True, text=True)
    out = r.stdout.splitlines(); st = dict(kv.split("=") for kv in [l for l in out if l.startswith("RESULT")][0].split()[1:])
    dt = [int(x) for x in [l for l in out if l.startswith("DEPTH_TOTAL")][0].split()[1:]]; de = [int(x) for x in [l for l in out if l.startswith("DEPTH_ESSENTIAL")][0].split()[1:]]
    hits = {tuple(map(int, l.split())) for l in open(h)}; cand = {int(l) for l in open(c)}
    return dict(st=st, hits=hits, cand=cand, depth_total=dt, depth_ess=de, tag=tag, hits_sha=sha(h), cand_sha=sha(c))
rows = []
for J in (46, 58, 65):
    cert = json.load(open(f"paradox_cert_J{J}.json")); assert sha(f"paradox_cert_J{J}.json") == logged[J]["baseline_cert_sha256"]
    base = {tuple(x) for x in cert["hits"]}; yest = {tuple(map(int, l.split())) for l in open(f"inv_hits_J{J}.txt")}
    assert sha(f"inv_hits_J{J}.txt") == logged[J]["inv_hits_sha256"] and yest == base
    cap0 = NODE_CAP if J < 65 else 30_000_000
    a = run(0, J, cert, cap0, "reference(P1/P2)" if J == 65 else "P1/P2"); b = run(1, J, cert, NODE_CAP, "Theta")
    sa, sb = a["st"], b["st"]; comp = sb["status"] == "0"
    row = dict(J=J, X=cert["X"], Hmax=cert["Hmax"], baseline_scan_steps=(cert["X"] - 2) * J, baseline_hits=len(base),
        logged_unpruned_nodes=logged[J]["inv_nodes"], mode0_nodes=int(sa["nodes"]), mode0_regression_equal_to_log=(int(sa["nodes"]) == logged[J]["inv_nodes"] and sa["status"] == "0"),
        mode0_hits_equal_baseline=(a["hits"] == base), mode0_candidates=len(a["cand"]), mode0_essential=int(sa["essential_nodes"]), mode0_seconds=float(sa["seconds"]),
        theta_status="COMPLETE" if comp else {"1": "INCOMPLETE(state cap)", "2": "INCOMPLETE(time cap)", "3": "ABORTED(guard)"}[sb["status"]],
        theta_nodes=int(sb["nodes"]), theta_candidates=len(b["cand"]), theta_essential=int(sb["essential_nodes"]), theta_hit_triples=int(sb["hit_triples"]),
        theta_hits_equal_baseline=(b["hits"] == base), theta_candidates_subset_of_mode0=(b["cand"] <= a["cand"]), theta_candidates_equal_mode0=(b["cand"] == a["cand"]),
        essential_equal=(sa["essential_nodes"] == sb["essential_nodes"]), theta_table_states=int(sb["table_states"]), theta_seconds=float(sb["seconds"]), theta_maxrss_kb=int(sb["maxrss_kb"]),
        within_mem_cap=(int(sb["maxrss_kb"]) <= MEM_KB), node_reduction_vs_mode0=round(int(sa["nodes"]) / max(1, int(sb["nodes"])), 3),
        theta_nodes_per_essential=round(int(sb["nodes"]) / max(1, int(sb["essential_nodes"])), 1), mode0_nodes_per_essential=round(int(sa["nodes"]) / max(1, int(sa["essential_nodes"])), 1),
        depth_total_theta=b["depth_total"], depth_essential_theta=b["depth_ess"], hits_sha256_theta=b["hits_sha"], cand_sha256_theta=b["cand_sha"], cand_sha256_mode0=a["cand_sha"])
    rows.append(row); print(json.dumps({k: v for k, v in row.items() if not k.startswith("depth_")}))
json.dump(dict(caps=dict(states=NODE_CAP, seconds=TIME_CAP, mem_kb=MEM_KB), rows=rows, source_sha256=sha("inverse_orbit_theta.c"), driver_sha256=sha("theta_pilot.py")), open("theta_pilot_results.json", "w"), indent=1)
