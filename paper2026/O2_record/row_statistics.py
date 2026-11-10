#!/usr/bin/env python3
"""Statistics of the agreement between gk and the reference tool on the
rows of rows.tsv (Section 7.1 of the paper), beside the counts of
count_rows.py.

Usage, from this folder or any other:

  python3 row_statistics.py                      items 1 to 4 and 6
  python3 row_statistics.py --cycles             also the kind of cycle of the
                                                 differing rows with a cycle cut
                                                 (reads the inputs with ../../mcref)
  python3 row_statistics.py --store STORE        also item 5, the run times,
  python3 row_statistics.py --raw RAW            from a run store or from the
                                                 folder raw/ of the full dataset

Items:
  1. the separation of the agreeing and the differing resolved rows;
  2. approximation notes and stopped searches against agreement;
  3. agreement by kind of note;
  4. the differing rows with a cycle cut;
  5. the run times of the gk runs;
  6. agreement by set.

A resolved row is a row on which both sides give a value for the same
instance and the tool's unresolved share is 0. Its difference is the
largest of the four differences between gk's share and the tool's share
(column max_difference); a row agrees when the difference is at most the
tool's tolerance (column tolerance). A standard error is sqrt(p(1 - p)/n)
of the share with the largest difference, with p gk's share and n the
tool's 20,000 samples. An approximation note is an entry of the list
`readings` of gk's output (column readings) or a step not represented
(column flags). A search stopped by the budget is a row with a positive
searches_cut; unfinished work is a stopped search or a pending step
(column pending_steps), the reading of the notes table of the paper.
Python 3.8 or later, standard library only (--cycles also uses mcref)."""
import json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DIFFER = ("differ, gk records a reading", "differ, gk used a contrapositive", "differ, gk used a step not represented",
          "differ, no flag")
SETS = ("ab", "examples", "families", "lit", "studies", "demo", "table", "paper", "boundary")
N = 20000
KINDS = [("cycle cut", ("cycle cut",)),
         ("residual variable", ("residual variable represented by a fresh constant",)),
         ("step not represented or proof application", ("step not represented",
                                                        "a proof application with shared evidence")),
         ("self exception", ("self exception",))]


def read(name):
  lines = open(os.path.join(HERE, name), encoding="utf-8").read().rstrip("\n").split("\n")
  cols = lines[0].split("\t")
  return [dict(zip(cols, l.split("\t"))) for l in lines[1:]]


def shares(text):
  return [float(x) for x in text.strip("[]").split(",")] if text else None


def names(r):
  """the approximation notes of a row: the names of its readings, and a step not represented"""
  out = []
  for item in filter(None, r["readings"].split("; ")):
    out.append(item.rsplit(" x", 1)[0] if item.rsplit(" x", 1)[-1].isdigit() else item)
  if "step not represented" in r["flags"].split("; "):
    out.append("step not represented")
  return out


def diff_se(r):
  g, m = shares(r["gk"]), shares(r["mcref"])
  k = max(range(4), key=lambda i: abs(g[i] - m[i]))
  d = abs(g[k] - m[k])
  p = g[k]
  se = math.sqrt(p * (1 - p) / N) if 0 < p < 1 else None
  return d, k, se


def pct(xs, q):
  """the q-th percentile, the nearest-rank method"""
  xs = sorted(xs)
  return xs[max(0, math.ceil(q / 100 * len(xs)) - 1)]


def median(xs):
  xs = sorted(xs)
  n = len(xs)
  return xs[n // 2] if n % 2 else (xs[n // 2 - 1] + xs[n // 2]) / 2


def se_text(d, se):
  return "%.1f standard errors" % (d / se) if se else "gk's share is 0 or 1; no standard error"


def item1(agree, differ):
  print("1. Separation over the %d resolved rows (%d agree, %d differ)" % (len(agree) + len(differ), len(agree),
                                                                          len(differ)))
  a = max(agree, key=lambda r: float(r["max_difference"]))
  b = min(differ, key=lambda r: float(r["max_difference"]))
  for label, r in (("largest difference among the agreeing rows", a), ("smallest difference among the differing rows", b)):
    d, k, se = diff_se(r)
    print("   %s: %.4f (%s), %s %s, share %d, gk %s, tool %s" % (label, d, se_text(d, se), r["input"], r["answer"], k + 1,
                                                                 r["gk"], r["mcref"]))
  print("   the %d differences in ascending order: %s" % (len(differ), ", ".join(
    "%.4f" % float(r["max_difference"]) for r in sorted(differ, key=lambda r: float(r["max_difference"])))))
  ad = [float(r["max_difference"]) for r in agree]
  print("   agreeing rows with difference exactly 0: %d" % sum(1 for x in ad if x == 0))
  print("   agreeing rows: median difference %.4f, 90th percentile %.4f, largest %.4f" % (median(ad), pct(ad, 90),
                                                                                         max(ad)))


def stopped(r):
  return int(r["searches_cut"] or 0) > 0


def unfinished(r):
  return stopped(r) or int(r.get("pending_steps") or 0) > 0


def item2(agree, differ):
  print("\n2. Approximation notes against agreement (the notes table: unfinished work)")
  print("   %-52s %6s %6s" % ("", "agree", "differ"))
  def cell(rs, f):
    return sum(1 for r in rs if f(r))
  lines = [("no approximation note, no unfinished work", lambda r: not names(r) and not unfinished(r)),
           ("no approximation note, unfinished work listed", lambda r: not names(r) and unfinished(r)),
           ("an approximation note", lambda r: bool(names(r))),
           ("  the same with a stopped search alone:", None),
           ("no approximation note, every search ended", lambda r: not names(r) and not stopped(r)),
           ("no approximation note, a search stopped by the budget", lambda r: not names(r) and stopped(r))]
  for label, f in lines:
    if f is None:
      print("   " + label)
      continue
    print("   %-52s %6d %6d" % (label, cell(agree, f), cell(differ, f)))


def item3(agree, differ):
  print("\n3. Agreement by kind of approximation note (a row with several kinds counts under each)")
  known = {n for _k, ns in KINDS for n in ns}
  other = sorted({n for r in agree + differ for n in names(r)} - known)
  print("   %-46s %6s %6s" % ("kind", "agree", "differ"))
  for label, ns in KINDS + [(n, (n,)) for n in other]:
    print("   %-46s %6d %6d" % (label, sum(1 for r in agree if set(names(r)) & set(ns)),
                                sum(1 for r in differ if set(names(r)) & set(ns))))
  shared = {"self exception", "rank zero as equal rank"}
  only = lambda r: bool(names(r)) and set(names(r)) <= shared
  print("   rows whose notes are only self exception or rank zero as equal rank: %d agree, %d differ"
        % (sum(1 for r in agree if only(r)), sum(1 for r in differ if only(r))))


def cycle_kinds(path):
  """the kinds of the cycle groups that the question depends on, read with
  the reference tool's own functions: across signs, through exception
  literals only, or mixed (a cycle through body literals of one sign, with
  or without an exception literal inside)"""
  sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "mcref")))
  import mcref as M  # noqa: E402
  from mcref_read import read_input  # noqa: E402
  inp = read_input(path, 200000, [])
  apps, _dropped = M.orient(inp.ground)
  byhead = {}
  for x in apps:
    byhead.setdefault(x.head, []).append(x)
  qs, qp, qargs = inp.question
  starts = [k for k in byhead if k[0] == qp] if inp.qvars else [(qp, qargs)]
  rel = M.closure(starts, byhead)
  order = sorted(rel, key=lambda k: (M.atom_text(*k), k[1] is None))
  idx = {k: i for i, k in enumerate(order)}
  n = len(order)
  byatom = [[] for _ in range(n)]
  for x in apps:
    if x.head in idx:
      byatom[idx[x.head]].append((x.hsign, 1.0 - x.conf, [(idx[a], M.POS if s == 0 else M.NEG) for s, a in x.body],
                                  [(idx[a], M.POS if s == 0 else M.NEG) for s, a in x.exc], x.normal, x.rank))
  live = {(M.POS if sg == 0 else M.NEG, idx[a]) for sg, a in M.reachable(apps) if a in idx}
  byatom = [[x for x in byatom[h] if all((sg, j) in live for j, sg in x[2])] for h in range(n)]
  deps = [sorted({j for x in byatom[h] for j, _s in x[2] + x[3]}) for h in range(n)]
  kinds = []
  for nodes, _out, _inner, cyclic in M.build_comps(deps, n):
    if not cyclic:
      continue
    members = set(nodes)
    if M.is_cross_sign(nodes, byatom):
      kinds.append("across signs")
      continue
    bdeps = [sorted({j for x in byatom[h] for j, _s in x[2] if j in members}) if h in members else [] for h in range(n)]
    body_cycle = any(len(c) > 1 or c[0] in bdeps[c[0]] for c in M.components(bdeps, n) if c[0] in members)
    kinds.append("mixed" if body_cycle else "through exception literals only")
  return kinds


def item4(differ, cycles):
  rows = [r for r in differ if "cycle cut" in names(r)]
  print("\n4. The %d differing rows with a cycle cut" % len(rows))
  for r in rows:
    line = "   %s, %s: gk %s, tool %s" % (r["input"], r["answer"], r["gk"], r["mcref"])
    if cycles:
      ks = cycle_kinds(os.path.join(HERE, r["input"]))
      kind = ks[0] if len(set(ks)) == 1 else ("several groups: " + ", ".join(sorted(set(ks))) if ks else "no cycle group")
      g, m = shares(r["gk"]), shares(r["mcref"])
      c5b = kind == "through exception literals only" and g[0] > m[0]
      line += "; cycle: %s%s" % (kind, "; of the kind of row C5b" if c5b else "")
    print(line)


def item5(rows, store, raw):
  sys.path.insert(0, os.path.join(HERE, "..", "tools"))
  import run_store as RS  # noqa: E402
  if raw:
    def entry(run_id):
      d = os.path.join(raw, "O2_record", run_id)
      if not os.path.isfile(os.path.join(d, "status.json")):
        return None
      return {"run": json.load(open(os.path.join(d, "run.json"))), "status": json.load(open(os.path.join(d, "status.json")))}
  else:
    class A:
      gk = os.path.join(RS.ROOT, "bin", "gk")
      mcref = os.path.join(RS.ROOT, "mcref", "mcref.py")
      tool = None
    keys = {r["run_id"]: r["key"] for r in RS.all_runs(["O2"], RS.tool_paths(A), quiet=True)}
    def entry(run_id):
      return RS.read_entry(store, keys[run_id])
  seen, times, loads, stopped, missing = set(), [], [], 0, 0
  for r in rows:
    if r["gk_run"] in seen or not r["gk_run"]:
      continue
    seen.add(r["gk_run"])
    e = entry(r["gk_run"])
    if e is None:
      missing += 1
      continue
    times.append(e["status"]["elapsed_s"])
    loads.append(float(e["run"]["load_before"][0]))
  for inp in {r["input"] for r in rows}:
    if any(int(r["searches_cut"] or 0) > 0 for r in rows if r["input"] == inp):
      stopped += 1
  print("\n5. The %d gk runs (%d not found): median %.2f s, 90th percentile %.2f s, largest %.2f s, total %.0f s; "
        "%d runs with a search stopped by the budget" % (len(times), missing, median(times), pct(times, 90), max(times),
                                                          sum(times), stopped))
  print("   the load average (1 minute) before each run: median %.2f, largest %.2f" % (median(loads), max(loads)))


def item6(rows):
  print("\n6. By set")
  print("   %-10s %6s %6s" % ("set", "agree", "differ"))
  for s in SETS + ("total",):
    rs = rows if s == "total" else [r for r in rows if r["set"] == s]
    print("   %-10s %6d %6d" % (s, sum(1 for r in rs if r["class"] == "agree with recursive"),
                              sum(1 for r in rs if r["class"] in DIFFER)))


def main():
  a = sys.argv[1:]
  rows = read("rows.tsv")
  agree = [r for r in rows if r["class"] == "agree with recursive"]
  differ = [r for r in rows if r["class"] in DIFFER]
  item1(agree, differ)
  item2(agree, differ)
  item3(agree, differ)
  item4(differ, "--cycles" in a)
  if "--store" in a or "--raw" in a:
    item5(rows, a[a.index("--store") + 1] if "--store" in a else None, a[a.index("--raw") + 1] if "--raw" in a else None)
  item6(rows)


if __name__ == "__main__":
  main()
