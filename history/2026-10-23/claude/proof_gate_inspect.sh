#!/bin/sh
# Proof-pipeline gate, step 1: inspect INSTALLED tools only (no install, no network).
date -u +"inspection time: %Y-%m-%dT%H:%M:%SZ"; uname -sr; echo "PATH=$PATH"
echo "== candidate binaries on PATH (name: path | version attempt)"
for s in roundingsat exact sat4j veripb cakepb cake_pb cadical kissat minisat glucose cryptominisat5 lingeling picosat drat-trim lrat-trim cake_lpr pbchecker clasp; do
  p=$(command -v $s 2>/dev/null); if [ -n "$p" ]; then echo "$s: $p | $($p --version 2>&1 | head -1)"; else echo "$s: NOT FOUND"; fi
done
echo "== python modules"
python3 - <<'PY'
import importlib, sys
print("python", sys.version.split()[0])
for m in ("veripb","pysat","pypblib","pycosat","z3","ortools","roundingsat","exact","pyscipopt","cvxopt"):
    try: mod = importlib.import_module(m); print(m, "FOUND", getattr(mod, "__version__", "?"))
    except Exception as e: print(m, "NOT FOUND")
PY
echo "== pip list (filtered)"; python3 -m pip list 2>/dev/null | grep -i -E "sat|veripb|pb|drat|solver|ortools|z3|cvx|scip|highs|cadical|kissat" || echo "(no matching pip packages)"
echo "== java/toolchain"; (command -v java && java -version 2>&1 | head -2) || echo "java: NOT FOUND"; gcc --version | head -1; command -v make cmake cargo rustc opam ocaml 2>/dev/null || true
echo "== dpkg packages matching sat/proof tools"; dpkg -l 2>/dev/null | grep -i -E "minisat|cadical|kissat|glucose|cryptominisat|picosat|lingeling|drat|veripb|roundingsat|sat4j|clasp" || echo "(none installed via dpkg)"
echo "== filesystem search (depth-limited, 60 s cap) for solver/checker artifacts"
timeout 60 find / -xdev \( -path /proc -o -path /sys -o -path /dev \) -prune -o \( -iname "*roundingsat*" -o -iname "*veripb*" -o -iname "*drat-trim*" -o -iname "*cadical*" -o -iname "*kissat*" -o -iname "*cake_pb*" -o -iname "*cakepb*" -o -iname "*lrat*" -o -iname "*sat4j*" -o -iname "libminisat*" \) -print 2>/dev/null | head -20
echo "find exit code: $?"
echo "== network (expected disabled): "; timeout 8 python3 -c "import urllib.request;print(urllib.request.urlopen('https://pypi.org',timeout=5).status)" 2>&1 | tail -1
