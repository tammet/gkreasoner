#!/usr/bin/env python3
"""evaluator_check.py OUT.json @LIST: gk's evaluators on the tool's own applications (the evaluator check of part
O13_conformance).

For every input of LIST (lines "SET<TAB>PATH"), the tool (mcref, in this process, with the settings of its
default command `mcref.py FILE --all-atoms`: proofs of several statements and layers on, cases off, the backbone
variant judge, at most 300,000 cells, the grounding limit 200,000) gives the exact value of every atom and its
applications. The applications go to gk's evaluator alone as a dump (the format gk_dump_v1): head, body,
exceptions, kind, rank, confidence, the rule identities with their confidences, the listed clauses. Two
evaluators, each a separate gk process with GK_DWEVAL_SECONDS=60:
  general  gk -dwevaluatenodes d.json          (General's evaluator)
  exact    gk -exact -dwevaluatenodes d.json   (Exact's evaluator)
The question of a gk run is an atom not yet covered; every node of the reply counts. One gk process at a time.

The environment: MCREF_DIR, the folder of mcref.py; MCREF_GK, the gk binary; CAP (optional), a script
`CAP MEM SECONDS COMMAND` that runs a command under a memory and time limit (the runs used 2 GB and 120 s);
WORK (optional), a folder for the temporary dump.

Writes OUT.json: {input: {"set", "tool": {atom: five}, "apps", "proof_apps", "general": {atom: [five, complete,
limits]}, "exact": {...}, "readings": {"general": [kinds], "exact": [kinds]}, "raw_readings": {...}, "runs": {...},
"tool_s", "status"}}; an input the tool cannot evaluate gets {"$skip": reason}. Resumes from OUT.json.
This is the driver of the runs, with its paths read from the environment."""
import json
import os
import subprocess
import sys
import time

sys.dont_write_bytecode = True
class C:
  """the paths of the run, from the environment"""
  GK = os.environ["MCREF_GK"]
  MC = os.environ.get("MCREF_DIR", "")
  CAP = os.environ.get("CAP", "")
  WORK = os.environ.get("WORK", ".")

MC = os.environ.get("MCREF_DIR", C.MC)
os.environ["MCREF_DIR"] = MC
os.environ["MCREF_GK"] = C.GK
sys.path.insert(0, MC)
import mcref_exact as X  # noqa: E402
from mcref_read import lit_text  # noqa: E402

M = X.mcref
# the settings that mcref.py's main() gives the module with its default command (--rules 8)
M.PROOFS, M.LAYERS, M.RANKS, M.CASES, M.BACKBONE = True, True, False, False, "judge"
TOL = 1e-9
ENV = {k: v for k, v in os.environ.items() if not (k.startswith("GK_") or k.startswith("PYTHON"))}
ENV["GK_DWEVAL_SECONDS"] = "60"


def dump_apps(pr):
  apps = []
  for i, x in enumerate(pr["apps"]):
    rec = {"id": "a%d" % i, "head": lit_text(x.hsign, *x.head), "confidence": "%.17g" % x.conf,
           "kind": "normal" if x.normal else "ordinary", "rank": int(x.rank),
           "body": [lit_text(s, *b) for s, b in x.body], "exceptions": [lit_text(s, *e) for s, e in x.exc],
           "same_atom": False}
    if x.ids:
      r = sorted(x.ids)
      rec["rules"] = ["e%d" % k for k in r]
      rec["rule_conf"] = [float(M.RULE_W[k]) for k in r]
    elif x.rid is not None:
      rec["rules"] = ["e%d" % x.rid]
      rec["rule_conf"] = [float(M.RULE_W[x.rid])]
    if x.cls:
      rec["clauses"] = [[lit_text(s, *a) for s, a in M.CLAUSE_LITS[k]] for k in x.cls]
    apps.append(rec)
  return apps


def gk_nodes(which, apps, q, tmp):
  dp = os.path.join(tmp, "d.json")
  open(dp, "w").write(json.dumps({"@format": "gk_dump_v1", "question": q, "context": 0, "applications": apps,
                                  "loop_marks": [], "priorities": []}, separators=(",", ":")))
  cmd = (["sh", C.CAP, "2G", "120"] if C.CAP else []) + [C.GK] + (["-exact"] if which == "exact" else []) + ["-dwevaluatenodes", dp]
  t0 = time.time()
  try:
    r = subprocess.run(cmd, capture_output=True, text=True, start_new_session=True, env=ENV, timeout=180)
  except subprocess.TimeoutExpired:
    return {q: [None, None, ["timeout", "no reply within 180 s"]]}, [], time.time() - t0
  for line in r.stdout.split("\n"):
    if line.startswith('{"dwevaluate"'):
      d = json.loads(line)["dwevaluate"]
      res = {}
      for nd in d.get("nodes") or []:
        v = nd.get("value")
        val = None if v is None else [float(z) for z in v] + [float(nd.get("unresolved") or 0)]
        res[nd["node"]] = [val, nd.get("complete"), nd.get("limits")]
      if q not in res:
        v = d.get("value")
        res[q] = [None if v is None else [float(z) for z in v] + [float(d.get("unresolved") or 0)], d.get("complete"),
                  d.get("limits") or ([d.get("interrupt"), d.get("interrupt_detail")] if d.get("interrupt") else None)]
      return res, d.get("readings") or [], time.time() - t0
  return {q: [None, None, ["no output", (r.stdout + r.stderr)[-200:]]]}, [], time.time() - t0


def main():
  out_path = sys.argv[1]
  files = []
  for a in sys.argv[2:]:
    lines = [x.rstrip("\n") for x in open(a[1:]) if x.strip()] if a.startswith("@") else [a]
    for x in lines:
      files.append(tuple(x.split("\t")) if "\t" in x else ("", x))
  tmp = os.path.join(C.WORK, "a8_tmp_%d" % os.getpid())
  os.makedirs(tmp, exist_ok=True)
  os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
  out = json.load(open(out_path)) if os.path.exists(out_path) else {}
  n_new = 0
  for setname, f in files:
    if f in out:
      continue
    t0 = time.time()
    try:
      res = X.run(f, max_cells=300000, all_atoms=True)
      if res.get("unsupported") or res.get("too_many_cells"):
        out[f] = {"set": setname, "$skip": str(res.get("unsupported") or res.get("too_many_cells"))[:200]}
        continue
      pr = X.prepare(f, 200000, True)
      if (M.LAST_PROOFS or {}).get("limit"):
        out[f] = {"set": setname, "$skip": "proof limit: %s" % M.LAST_PROOFS.get("limit")}
        continue
    except Exception as e:
      out[f] = {"set": setname, "$error": "%s: %s" % (type(e).__name__, str(e)[:200])}
      continue
    tool_s = time.time() - t0
    tool = {a["atom"]: [round(x, 12) for x in a["value"]] + [round(a.get("unstable", 0), 12)]
            for a in res["atom_values"] if "value" in a and not a["atom"].startswith("$")}
    apps = dump_apps(pr)
    rec = {"set": setname, "tool": tool, "apps": len(apps), "proof_apps": sum(1 for x in pr["apps"] if x.kind == "proof"),
           "clause_apps": sum(1 for x in pr["apps"] if x.cls), "tool_s": round(tool_s, 3), "readings": {},
           "raw_readings": {}, "runs": {}}
    for which in ("general", "exact"):
      got, kinds, raw, nrun, secs = {}, set(), {}, 0, 0.0
      for a in sorted(tool):
        if a in got:
          continue
        r, rd, dt = gk_nodes(which, apps, a, tmp)
        nrun += 1
        secs += dt
        raw[a] = rd
        for x in rd:
          kinds.add(x[0] if isinstance(x, list) else str(x))
        for k, v in r.items():
          if k in tool and k not in got:
            got[k] = v
        if a not in got:
          got[a] = [None, None, ["node not reported"]]
      rec[which] = got
      rec["readings"][which] = sorted(kinds)
      rec["raw_readings"][which] = raw
      rec["runs"][which] = [nrun, round(secs, 3)]
    out[f] = rec
    n_new += 1
    if n_new % 25 == 0:
      json.dump(out, open(out_path + ".part", "w"))
      os.replace(out_path + ".part", out_path)
  json.dump(out, open(out_path + ".part", "w"))
  os.replace(out_path + ".part", out_path)
  try:
    os.remove(os.path.join(tmp, "d.json"))
    os.rmdir(tmp)
  except OSError:
    pass
  nd = {"general": 0, "exact": 0}
  nat = 0
  for f, rec in out.items():
    if "tool" not in rec:
      continue
    for a, v in rec["tool"].items():
      nat += 1
      for which in nd:
        g = rec[which].get(a, [None])[0]
        if g is None or any(abs(x - y) > TOL for x, y in zip(v, g)):
          nd[which] += 1
  print("%s: %d inputs, %d atoms; differ (1e-9): general %d, exact %d; skipped %d" % (
    out_path, len(out), nat, nd["general"], nd["exact"], sum(1 for r in out.values() if "tool" not in r)))


if __name__ == "__main__":
  main()
