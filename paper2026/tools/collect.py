#!/usr/bin/env python3
"""Fill the columns stored and measured of every results.tsv from the
stored runs, and compare each stored value with the printed one.

A row of results.tsv names its run in the column run (a run_id of the
part's runs.tsv). This script reads the output of that run, from a run
store made by run_store.py or from the folder raw/ of the full dataset,
and writes into the row:

- stored: the value that the run printed: the four shares of gk or of the
  reference tool, "declined: reason", or what an external tool printed;
- measured: the wall time of the run and, for gk, the searches stopped by
  the budget, the applications, the approximation notes (the output field
  `readings`) and the checkpoint of the value.

It never runs a tool and never changes the store. It reports every row
whose stored value differs from the printed value (column result) at the
printed precision, and every row whose run is not stored. A part folder
with a script make_rows.py also gets the tables that the script builds
(part O2: rows.tsv).

Usage, from the folder that holds bin/, mcref/ and paper2026/:

  python3 paper2026/tools/collect.py --store STORE [PART ...]
  python3 paper2026/tools/collect.py --raw paper2026/raw [PART ...]

With --store, the options --gk, --mcref and --tool must name the same
executables as for run_store.py, because the key of a run contains their
SHA-256. Exit status 0 means: every compared row matches and every named
run is stored.
"""
import argparse, gzip, importlib.util, json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import run_store as RS  # noqa: E402
import gkout as G       # noqa: E402

RESULT_COLUMNS = ("id", "paper", "system", "input", "options", "kind", "relation", "result", "note",
                  "run", "stored", "measured")


def raw_entry(raw, part, run_id):
  d = os.path.join(raw, part, run_id)
  if not os.path.isfile(os.path.join(d, "status.json")):
    return None
  def text(name):
    with gzip.open(os.path.join(d, name), "rt", encoding="utf-8", errors="replace") as f:
      return f.read()
  return {"run": json.load(open(os.path.join(d, "run.json"))),
          "status": json.load(open(os.path.join(d, "status.json"))),
          "stdout": text("stdout.gz"), "stderr": text("stderr.gz"), "out": RS.read_out(d)}


def answers_text(ans):
  if len(ans) == 1:
    return G.shares_text(ans[0][1])
  return "; ".join("%s %s" % (t, G.shares_text(v)) for t, v in ans)


def gk_facts(e):
  st, r = e["status"], G.gk_line(e["stdout"])
  parts = ["%.1f s" % st["elapsed_s"]]
  if st.get("timed_out"):
    parts.append("stopped at the runner's limit")
  if r:
    parts.append("searches stopped %s of %s" % (r.get("tasks_cut", 0), r.get("tasks", 0)))
    parts.append("applications %s" % r.get("applications", 0))
    names = [x[0] for x in r.get("readings") or [] if isinstance(x, list) and x]
    if names:
      counts = {}
      for n in names:
        counts[n] = counts.get(n, 0) + 1
      parts.append("approximation notes: " + ", ".join("%s x%d" % (n, c) if c > 1 else n for n, c in counts.items()))
    else:
      parts.append("no approximation note")
    if r.get("value_from"):
      parts.append("value from " + r["value_from"])
    if r.get("budget_used_ms") is not None:
      parts.append("budget used %d ms" % round(r["budget_used_ms"]))
  return "; ".join(parts)


def checkpoint_values(e):
  """the successive distinct values of gk's checkpoint dumps"""
  out = []
  for name in sorted(e.get("out") or {}):
    try:
      v = (json.loads(e["out"][name]).get("value_c") or {}).get("value")
    except ValueError:
      continue
    if v is not None and (not out or [round(x, 9) for x in v] != [round(x, 9) for x in out[-1]]):
      out.append(v)
  return out


def stored_value(tool, e, row=None):
  """(text of the stored value, list of four-tuples or None, declined?)"""
  st = e["status"]
  if tool == "gk" and "-checkpoints" in ((row or {}).get("options") or ""):
    vs = checkpoint_values(e)
    return "checkpoints: " + "; ".join(G.shares_text([round(x, 6) for x in v]) for v in vs), vs, False
  if tool == "gk":
    ans = G.gk_answers(e["stdout"])
    if ans is None:
      return ("no line {\"recursive\": ...}; exit %s" % st["exit"]) + (", timed out" if st["timed_out"] else ""), None, False
    if not ans:
      r = G.gk_line(e["stdout"]) or {}
      return "no value (%s)" % (r.get("stop") or r.get("search") or "no answer"), [], False
    return answers_text(ans), [v for _, v in ans], False
  if tool == "mcref":
    m = G.mcref_object(e["stdout"])
    if m is None:
      return "no result; exit %s%s" % (st["exit"], ", timed out" if st["timed_out"] else ""), None, False
    if m.get("unsupported"):
      return "declined: " + m["unsupported"], None, True
    ans = G.mcref_answers(e["stdout"])
    return answers_text(ans) if ans else "no answer", [v for _, v in ans or []], False
  if st.get("timed_out"):
    out = " ".join(e["stdout"].split())[:150]
    limit = (row or {}).get("timeout_s") or "the runner's"
    return "stopped at the limit of %s s; %s" % (limit, ("printed: " + out) if out else "no output"), None, False
  out = " | ".join(l.strip() for l in e["stdout"].strip().split("\n") if l.strip())[:300]
  return "exit %s: %s" % (st["exit"], out or "no output"), None, False


def measured(tool, e):
  if tool == "gk":
    return gk_facts(e)
  st = e["status"]
  s = "%.1f s" % st["elapsed_s"]
  if tool == "mcref":
    m = G.mcref_object(e["stdout"]) or {}
    if m.get("samples"):
      s += "; samples %s, seed %s" % (m.get("samples"), m.get("seed"))
    un = [a.get("unstable") for a in m.get("answers") or [] if a.get("unstable")]
    if un:
      s += "; unresolved share " + ", ".join("%g" % x for x in un)
  else:
    s += "; exit %s%s; peak memory %d MB" % (st["exit"], ", timed out" if st["timed_out"] else "",
                                             st["peak_rss_kb"] // 1024)
  return s


def compare(row, tool, values, declined, e):
  kind = row["kind"]
  if tool in ("gk", "mcref") and kind in ("run", "estimate"):
    return "ok" if values and G.matches(row["result"], values) else "DIFF"
  if kind == "declined":
    return "ok" if declined else "DIFF"
  if kind in ("no answer", "failed"):
    st = e["status"]
    ended = st["timed_out"] or st["exit"] != 0 or values == [] or values is None
    return "ok" if ended else "DIFF"
  return "not compared"


def target_check(row, tool, values, e):
  """the stored value against the column target (a hand or semantic
  value): gk at the target's printed precision, mcref within its sampling
  tolerance e = sqrt(ln(8/.05) / (2 n)); a target with fewer numbers than
  the value compares the first shares"""
  exp = G.numbers(row.get("target") or "")
  if not exp or not values:
    return ""
  flat = [x for v in values for x in v][:len(exp)]
  if len(flat) < len(exp):
    return "no value to compare"
  if tool == "mcref":
    m = G.mcref_object(e["stdout"]) or {}
    n = m.get("samples") or 0
    tol = math.sqrt(math.log(8 / 0.05) / (2 * n)) if n else 1.0
    worst = max(abs(x - t) for x, (t, _) in zip(flat, exp))
    return ("within %.4f of the target" if worst <= tol else "OUTSIDE %.4f of the target") % tol + \
      " (largest difference %.4f)" % worst
  # gk prints its shares rounded to 6 decimals: a target printed with more
  # decimals is compared at that precision
  ok = all(abs(x - t) <= max(tol, 5e-7 + 1e-12) for x, (t, tol) in zip(flat, exp))
  return "equals the target" if ok else "DIFFERS from the target"


def load_hook(folder):
  p = os.path.join(folder, "make_rows.py")
  if not os.path.isfile(p):
    return None
  spec = importlib.util.spec_from_file_location("make_rows_" + os.path.basename(folder), p)
  mod = importlib.util.module_from_spec(spec)
  spec.loader.exec_module(mod)
  return mod


def main():
  ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
  ap.add_argument("parts", nargs="*")
  ap.add_argument("--store", default=os.environ.get("PAPER2026_STORE"))
  ap.add_argument("--raw", help="the folder raw/ of the full dataset, in place of a store")
  ap.add_argument("--gk", default=os.path.join(RS.ROOT, "bin", "gk"))
  ap.add_argument("--mcref", default=os.path.join(RS.ROOT, "mcref", "mcref.py"))
  ap.add_argument("--tool", action="append")
  ap.add_argument("--quiet", action="store_true", help="print only the rows that do not match")
  a = ap.parse_args()
  if not a.raw and not a.store:
    sys.exit("give --store STORE or --raw RAW")
  paths = RS.tool_paths(a) if not a.raw else None
  bad = 0
  counts = {}
  for folder in RS.part_folders(a.parts):
    part = os.path.basename(folder)
    runs = {r["run_id"]: r for r in (RS.all_runs([part], paths, quiet=True) if paths else
                                     [dict(x, part=part) for x in RS.run_list(folder)])}
    def entry_of(run_id):
      r = runs.get(run_id)
      if r is None:
        return None
      if a.raw:
        return raw_entry(os.path.abspath(a.raw), part, run_id)
      if not r.get("key"):
        return None
      return RS.read_entry(os.path.abspath(a.store), r["key"])
    path = os.path.join(folder, "results.tsv")
    if os.path.isfile(path):
      cols, rows = RS.read_tsv(path)
      for c in RESULT_COLUMNS:
        if c not in cols:
          cols.append(c)
      for row in rows:
        rid = row.get("run") or ""
        system = (row.get("system") or "").split()[:1]
        if not rid:
          if system and system[0] in ("gk", "mcref") and row["kind"] in ("run", "estimate", "declined"):
            print("NO RUN   %s/%s: a %s row without a run" % (part, row["id"], system[0]))
            bad += 1
          continue
        r = runs.get(rid)
        if r is None:
          print("NO RUN   %s/%s: run %s is not in runs.tsv" % (part, row["id"], rid))
          bad += 1
          continue
        e = entry_of(rid)
        if e is None:
          print("MISSING  %s/%s: run %s is not stored%s" % (part, row["id"], rid,
                                                           " (" + r["missing"] + ")" if r.get("missing") else ""))
          counts["missing"] = counts.get("missing", 0) + 1
          bad += 1
          continue
        text, values, declined = stored_value(r["tool"], e, r)
        row["stored"] = text
        row["measured"] = measured(r["tool"], e)
        verdict = compare(row, r["tool"], values, declined, e)
        if "target" in cols:
          if "target_check" not in cols:
            cols.append("target_check")
          row["target_check"] = target_check(row, r["tool"], values, e)
          if row["target_check"].startswith(("OUTSIDE", "DIFFERS")):
            print("TARGET   %s/%s: target %s; stored %s: %s" % (part, row["id"], row["target"], text,
                                                              row["target_check"]))
        counts[verdict] = counts.get(verdict, 0) + 1
        if verdict == "DIFF":
          bad += 1
        if verdict == "DIFF" or not a.quiet:
          print("%-12s %s/%s: printed %s; stored %s" % (verdict, part, row["id"], row["result"], text))
      with open(path, "w", encoding="utf-8") as f:
        f.write("\t".join(cols) + "\n")
        for row in rows:
          f.write("\t".join((row.get(c) or "").replace("\t", " ").replace("\n", " ") for c in cols) + "\n")
    hook = load_hook(folder)
    if hook:
      bad += hook.build(folder, entry_of, runs)
  print("rows: " + ", ".join("%s %d" % (k, v) for k, v in sorted(counts.items())))
  sys.exit(1 if bad else 0)


if __name__ == "__main__":
  main()
