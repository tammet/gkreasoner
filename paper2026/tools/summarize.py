#!/usr/bin/env python3
"""summarize.py: compute the tables of the part READMEs from the parts' results files.

Every table of a part README stands between the lines `<!-- table NAME -->` and `<!-- end table -->`. This
script computes each table again from the CSV files of the folder.

  python3 tools/summarize.py PART            print the tables of one part (for example O1_tweety; "." is the
                                             first page)
  python3 tools/summarize.py --check         compare every table of every README with a fresh computation
  python3 tools/summarize.py --help          this text

Exit status 0 means that every table equals its computation. Python 3.9 or later, no other package.
"""
import csv
import gzip
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import gkline as GL  # noqa: E402

csv.field_size_limit(1 << 30)
_CACHE = {}


def rows(part, name="results.csv"):
  """the rows of a CSV file of a part; a large file is stored compressed as NAME.gz"""
  key = (part, name)
  if key not in _CACHE:
    p = os.path.join(ROOT, part, name)
    if not os.path.exists(p) and os.path.exists(p + ".gz"):
      f = gzip.open(p + ".gz", "rt", newline="")
    else:
      f = open(p, newline="")
    with f:
      _CACHE[key] = list(csv.DictReader(f, delimiter="\t" if name.endswith(".tsv") else ","))
  return _CACHE[key]


def table(head, body):
  out = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
  for r in body:
    out.append("| " + " | ".join(str(x) for x in r) + " |")
  return "\n".join(out)


def n(x):
  return "{:,}".format(x)


def short(v, digits=4):
  """a value of four shares written short: (.396, .56, 0, .044)"""
  x = GL.read_value(v)
  if x is None:
    return v or "-"
  return "(" + ", ".join(dec(y, digits) for y in x) + ")"


def dec(y, digits=6):
  s = ("%." + str(digits) + "f") % float(y)
  s = s.rstrip("0").rstrip(".") if "." in s else s
  if s.startswith("0."):
    s = s[1:]
  if s in ("", "-0"):
    s = "0"
  return s


def secs(r):
  return (r["time_s"] + " s") if r.get("time_s") else "limit"


def gk_cell(r, digits=4, show_by=True):
  """one gk answer: value; complete or not; the method that answered; the time, or "limit" for a run that did
  not end by itself"""
  if not r:
    return "-"
  if not r["value"]:
    return "no value: " + (r["first_limit"] or r["note"] or "none")
  parts = [short(r["value"], digits)]
  if r["complete"] == "yes":
    parts.append("complete")
  elif r["complete"] == "no":
    parts.append("not complete")
  if show_by and r["method"] == "default" and r["answered_by"]:
    parts.append("by the %s method" % r["answered_by"])
  parts.append(secs(r))
  return ", ".join(parts)


def pick(rs, **kw):
  out = [r for r in rs if all(r.get(k) == v for k, v in kw.items())]
  return out[0] if out else None


def GK():
  """the name and version of gk in this folder's rows"""
  for r in rows("O1_tweety"):
    if r["system"].startswith("gk ") and r["run_id"]:
      return r["system"]
  return "gk"


def pick_gk(rs, **kw):
  out = [r for r in rs if r["system"].startswith("gk ") and all(r.get(k) == v for k, v in kw.items())]
  return out[0] if out else None


def pick_tool(rs, **kw):
  out = [r for r in rs if r["system"].startswith("mcref") and all(r.get(k) == v for k, v in kw.items())]
  return out[0] if out else None


def rng(xs):
  xs = sorted(float(x) for x in xs if x not in (None, ""))
  if not xs:
    return "-"
  a, b = dec(xs[0], 2), dec(xs[-1], 2)
  return (a + " s") if a == b else ("%s to %s s" % (a, b))


# ================================================================ O1_tweety

STAGES = [("1", "stage1"), ("2", "stage2"), ("3a", "stage3a"), ("3b", "stage3b"), ("4, from stage 2", "stage4_2"),
          ("4, from stage 3a", "stage4_3a"), ("4, from stage 3b", "stage4_3b")]


def t_o1_stages():
  rs = rows("O1_tweety")
  body = []
  for label, st in STAGES:
    g = [r for r in rs if r["stage"] == st and r["system"].startswith("gk") and r["limit_s"] == "10"]
    t = pick_tool(rs, stage=st)
    d = pick(g, method="default")
    body.append([label, short(d["target"]), gk_cell(d), gk_cell(pick(g, method="exact")),
                 gk_cell(pick(g, method="general")), short(t["value"]) + ", " + t["class"] if t else "not run"])
  return table(["stage", "calculated value", "the default", "the exact method", "the general method", "the tool"], body)


def t_o1_lineage():
  rs = [r for r in rows("O1_tweety") if r["stage"].startswith("stage4") and r["method"] == "default"]
  body = []
  for st in ("stage4_2", "stage4_3a", "stage4_3b"):
    for lim in ("2", "10", "60"):
      r = pick(rs, stage=st, limit_s=lim)
      body.append([r["input"].split("/")[-1], lim + " s", short(r["value"]), r["class"], r["ended_by_itself"],
                   r["first_limit"] or "-"])
  return table(["input", "limit", "value of the default", "against the calculated value", "ended by itself",
                "first limit"], body)


def t_o1_others():
  rs = [r for r in rows("O1_tweety") if not r["system"].startswith(("gk", "mcref", "s(CASP)"))]
  body = [[r["stage"], r["system"], r["outcome"], r["value"] or "-", r["relation"] or "-"] for r in rs]
  return table(["stage", "system", "outcome", "what the system printed", "relation of the encoding"], body)


def t_o1_scasp():
  """s(CASP) on the crisp counterparts of stage 4"""
  runs = {r["run_id"]: r for r in rows("O1_tweety", "runs.tsv")}
  body = []
  for r in rows("O1_tweety"):
    if r["system"].startswith("s(CASP)"):
      run = runs.get(r["run_id"], {})
      kind, enc = r["note"].split(" run: ", 1)
      body.append([kind, r["input"].split("/scasp/", 1)[-1], r["question"], enc,
                   "%s s, %s GB" % (run.get("time_cap_s", ""), run.get("memory_cap", "").rstrip("G")), r["outcome"],
                   secs(r) if r["time_s"] or r["ended_by_itself"] != "yes" else "not recorded"])
  return table(["run", "input", "question", "encoding", "limits", "outcome", "time"], body)



def is_gk(r):
  return r["system"].startswith("gk ")


def is_tool(r):
  return r["system"].startswith("mcref")


RIGHT = ("equal", "meets the target", "complete and equal", "label reproduced", "the published conclusion holds",
         "exhaustive search: complete and equal", "general: equal to the tool", "equal to the tool",
         "equal to the calculated value", "right label")


def right(r):
  c = r.get("class") or ""
  return c in RIGHT or c.startswith("equal") or c.endswith("; equal")


def count(rs, pred=None):
  return sum(1 for r in rs if pred is None or pred(r))


def cause(r):
  return (r.get("first_limit") or "").split(":")[0] or "-"


# ================================================================ O2_record

def t_o2_classes():
  rs = [r for r in rows("O2_record") if is_gk(r)]
  classes = []
  for r in rs:
    if r["class"] not in classes:
      classes.append(r["class"])
  body = []
  for c in sorted(classes):
    body.append([c] + [n(count(rs, lambda r: r["class"] == c and r["method"] == m))
                       for m in ("default", "general", "exact")])
  body.append(["all answers"] + [n(count(rs, lambda r: r["method"] == m)) for m in ("default", "general", "exact")])
  return table(["class of the answer", "the default", "the general method", "the exact method"], body)


def t_o2_limited():
  rs = [r for r in rows("O2_record") if is_gk(r) and r["tool_limit"] == "yes"]
  body = [[r["input"].split("/")[-1], r["question"], r["method"], short(r["value"]), short(r["target"]), r["class"]]
          for r in rs]
  return table(["input", "answer", "method", GK(), "the tool's value", "class"], body)


def t_o2_sets():
  rs = rows("O2_record", "inputs.csv")
  sets = {}
  for r in rs:
    sets.setdefault(r["set"], []).append(r["source"])
  body = []
  for k in sorted(sets):
    srcs = sorted(set(sets[k]))
    desc = srcs[0] if len(srcs) == 1 else "%s; and %d other sources" % (srcs[0], len(srcs) - 1)
    body.append([k, n(len(sets[k])), desc])
  body.append(["all", n(len(rs)), ""])
  return table(["set", "inputs", "where they come from"], body)


def t_o2_declined():
  rs = rows("O2_record", "declined.csv")
  c = {}
  for r in rs:
    c[r["tool_reason"]] = c.get(r["tool_reason"], 0) + 1
  body = [[k, n(v)] for k, v in sorted(c.items(), key=lambda x: (-x[1], x[0]))]
  body.append(["all", n(len(rs))])
  return table(["why the tool declines the input", "inputs"], body)


def t_o2_declined_default():
  rs = rows("O2_record", "declined.csv")
  c = {}
  for r in rs:
    k = r["default_outcome"] + ((", " + r["default_branch"]) if r["default_branch"] else "")
    c[k] = c.get(k, 0) + 1
  body = [[k, n(v)] for k, v in sorted(c.items(), key=lambda x: (-x[1], x[0]))]
  return table(["the default on the declined inputs: what answered", "inputs"], body)


def median(xs):
  xs = sorted(xs)
  if not xs:
    return None
  k = len(xs)
  return xs[k // 2] if k % 2 else (xs[k // 2 - 1] + xs[k // 2]) / 2.0


def t_o2_time():
  rs = [r for r in rows("O2_record") if is_gk(r)]
  body = []
  for m in ("default", "general", "exact"):
    runs = {}
    for r in rs:
      if r["method"] == m:
        runs[r["run_id"]] = r
    ended = [float(r["time_s"]) for r in runs.values() if r["time_s"]]
    body.append([m, n(len(runs)), n(len(ended)), dec(median(ended), 2) + " s" if ended else "-",
                 dec(max(ended), 2) + " s" if ended else "-"])
  return table(["method", "runs", "ended by themselves", "median time of these", "largest time of these"], body)


def t_o2_general():
  """the general method's record on the collection, by the kind of the tool's value"""
  rs = [r for r in rows("O2_record") if is_gk(r) and r["method"] == "general"]
  def k(r):
    c, kind = r["class"], r["target_kind"]
    if c.startswith("the tool's value has a stated limit"):
      return ("equal to a value of the tool with a stated limit of its proof search" if c.endswith("equal to the tool")
              else "another value than a value of the tool with a stated limit of its proof search")
    if c == "equal to the tool" and kind.startswith("exact"):
      return "equal to an exact value of the tool"
    if c == "equal to the tool" and kind.startswith("sampled"):
      return "within the sampling bound of a sampled value of the tool"
    if c == "another value":
      return "another value"
    if c.startswith("not listed"):
      return "an answer of the collection that gk does not list"
    return "no value of the tool, or no answer named"
  order = ["equal to an exact value of the tool", "within the sampling bound of a sampled value of the tool",
           "equal to a value of the tool with a stated limit of its proof search",
           "another value than a value of the tool with a stated limit of its proof search", "another value",
           "an answer of the collection that gk does not list", "no value of the tool, or no answer named"]
  body = [[o, n(count(rs, lambda r: k(r) == o))] for o in order]
  body.append(["all answers", n(len(rs))])
  return table(["the general method on the collection", "answers"], body)


# ================================================================ O3_families

def t_o3_families():
  rs = [r for r in rows("O3_families") if is_gk(r) and r["target"] and not r["strategy"]]
  fams = []
  for r in rs:
    if r["family"] not in fams:
      fams.append(r["family"])
  body = []
  for f in fams:
    x = [r for r in rs if r["family"] == f]
    d = [r for r in x if r["method"] == "default"]
    g = [r for r in x if r["method"] == "general"]
    e = [r for r in x if r["method"] == "exact"]
    kinds = sorted({r["target_kind"].split(":")[0] for r in d})
    body.append([f, n(len(d)), "; ".join(kinds),
                 "%s (exact %s, general %s)" % (n(count(d, right)), n(count(d, lambda r: right(r) and r["answered_by"] == "exact")),
                                               n(count(d, lambda r: right(r) and r["answered_by"] == "general"))),
                 n(count(g, right)), "%s / %s" % (n(count(e, right)), n(count(e, lambda r: r["complete"] == "yes")))])
  return table(["family", "inputs", "kind of target", "the default meets the target (answered by)",
                "the general method meets", "the exact method meets / complete"], body)


def t_o3_strategies():
  rs = [r for r in rows("O3_families") if is_gk(r) and r["strategy"]]
  body = [[r["input"].split("/")[-2] + "/" + r["input"].split("/")[-1], r["strategy"], short(r["value"]),
           short(r["target"]) if r["target"] else "-", r["class"] or "-", r["ended_by_itself"]] for r in rs]
  return table(["input", "strategy", "value", "target", "against the target", "ended by itself"], body)


def t_o3_problog():
  rs = rows("O3_families")
  body = []
  for r in rs:
    if r["system"].startswith("ProbLog"):
      g = pick(rs, input=r["input"], method="default")
      body.append([r["input"].split("/")[-1], r["question"], gk_cell(g, 6), r["value"], secs(r)])
  return table(["input", "question", GK() + ", the default", "ProbLog 2.3.0", "ProbLog's time"], body)


def lim_cells(rs):
  """the cells of one row of the table of limits: the exact method, the general method, the default"""
  e = [r for r in rs if r["method"] == "exact"]
  g = [r for r in rs if r["method"] == "general"]
  d = [r for r in rs if r["method"] == "default"]

  def ex(xs):
    if not xs:
      return "not run"
    nc = count(xs, lambda r: (r["first_limit"] or "").startswith("not covered"))
    nv = count(xs, lambda r: not r["value"] and not (r["first_limit"] or "").startswith("not covered"))
    rt = count(xs, right)
    cp = [r for r in xs if r["complete"] == "yes"]
    parts = ["%s of %s right" % (n(rt), n(len(xs))), "%s complete" % n(len(cp))]
    if cp:
      parts.append(rng([r["time_s"] for r in cp]))
    if nc:
      parts.append("%s not covered" % n(nc))
    if nv:
      parts.append("no value on %s" % n(nv))
    return ", ".join(parts)

  def ge(xs):
    if not xs:
      return "not run"
    ended = [r for r in xs if r["ended_by_itself"] == "yes"]
    out = "%s of %s right, %s ended by themselves" % (n(count(xs, right)), n(len(xs)), n(len(ended)))
    if ended:
      out += " (" + rng([r["time_s"] for r in ended]) + ")"
    return out

  def de(xs):
    if not xs:
      return "not run"
    return "%s of %s right; answered by the exact method %s, by the general method %s" % (
      n(count(xs, right)), n(len(xs)), n(count(xs, lambda r: r["answered_by"] == "exact")),
      n(count(xs, lambda r: r["answered_by"] == "general")))
  return [ex(e), ge(g), de(d)]


def o3_sel(families=None, inputs=None, part="O3_families", **kw):
  rs = [r for r in rows(part) if is_gk(r) and not r.get("strategy") and r.get("limit_s", "10") in ("10", "")]
  out = []
  for r in rs:
    name = r["input"].split("/")[-1]
    if families and r.get("family") not in families:
      continue
    if inputs and name not in inputs:
      continue
    if all(r.get(k) == v for k, v in kw.items()):
      out.append(r)
  return out


LIMIT_ROWS_A = [
  ("8 grids with a target (ProbLog)", lambda: [r for r in o3_sel(["grids"]) if r["target"]]),
  ("a chain of 1,000 defaults; trees of 364 and 2,047 nodes", lambda: o3_sel(["chains_trees"])),
  ("the route with contrary reports, 5 to 200 links (part O14)",
   lambda: [r for r in rows("O14_routes") if is_gk(r) and r["family"] == "route_opp"
            and r["method"] in ("exact", "general")]),
]
LIMIT_ROWS_B = [
  ("the university base plus one certain contradiction about a new individual, variant (a) (part O15)",
   lambda: [r for r in rows("O15_contradiction") if is_gk(r) and r["version"] == "a"]),
  ("delivery plans of 16 and 32 legs, function terms",
   lambda: o3_sel(["delivery"], ["gk_legs16_control.gkp", "gk_legs16_opposed.gkp", "gk_legs32_control.gkp",
                                 "gk_legs32_opposed.gkp"])),
  ("the Tweety lineage, function terms (part O1)",
   lambda: [r for r in rows("O1_tweety") if is_gk(r) and r["stage"].startswith("stage4") and r["limit_s"] == "10"]),
  ("equipment with equality", lambda: o3_sel(["equipment"])),
  ("Smokers with 5, 8 and 12 persons", lambda: o3_sel(["smokers"])),
  ("4 deep queries on large Bayesian networks",
   lambda: o3_sel(["bn"], ["gk_win95pts_problem1.gkp", "gk_win95pts_pc2prt.gkp", "gk_andes_snode_151.gkp",
                           "gk_andes_snode_74.gkp"])),
  ("cyclic inputs: the ring of 30, the program of 40, argumentation frameworks of 20 and 40 arguments",
   lambda: [r for r in o3_sel(["cyclic"]) if r["input"].split("/")[-1] in (
     "gk_ring30.gkp", "gk_program40.gkp") or "_af20" in r["input"] or "_af40" in r["input"]]),
  ("the route with certain rules and a default, 5, 10 and 20 links (part O14)",
   lambda: [r for r in rows("O14_routes") if is_gk(r) and r["family"] == "rt_mix" and r["method"] in (
     "exact", "general") and r["run_id"].startswith("a4_route/")]),
  ("the exact method outside both classes, 24 inputs (part O20)",
   lambda: [r for r in rows("O20_outside_classes") if is_gk(r) and r["method"] in ("exact", "general", "default")]),
]


def t_o3_limits_a():
  body = [[label] + lim_cells(f()) for label, f in LIMIT_ROWS_A]
  return table(["inputs", "the exact method", "the general method", "the default"], body)


def t_o3_limits_b():
  body = [[label] + lim_cells(f()) for label, f in LIMIT_ROWS_B]
  return table(["inputs", "the exact method", "the general method", "the default"], body)


def t_o3_limits_c():
  rs = [r for r in rows("O6_budget") if r["case"].startswith("does John")]
  body = [[r["limit_s"] + " s", r["method"], short(r["value"]), r["answered_by"], r["ended_by_itself"]] for r in rs]
  return table(["limit", "method", "value", "answered by", "ended by itself"], body)


# ================================================================ O4_quantities

def t_o4_cases():
  rs = rows("O4_quantities")
  body = []
  for r in rs:
    if is_gk(r):
      t = pick_tool(rs, case=r["case"])
      body.append([r["case"], r["question"], short(r["target"]),
                   gk_cell(r) if r["class"] != "not run" else "not run",
                   (short(t["value"]) + ", " + t["class"]) if t else "not run"])
  return table(["case", "question", "calculated value", GK() + ", the default", "the tool"], body)


def t_o4_others():
  rs = [r for r in rows("O4_quantities") if not is_gk(r) and not is_tool(r)]
  body = [[r["case"], r["system"], r["outcome"], r["value"] or "-", r["relation"] or "-"] for r in rs]
  return table(["case", "system or semantics", "outcome", "value", "relation of the encoding"], body)


# ================================================================ O5_comparisons

C1_SYS = ["ProbLog 2.2.10", "PASTA 1.0.1", "plingo 1.1.0", "smProbLog 2.1.0.42", "TweetyProject 1.31",
          "clingo 5.6.2", "DLV 2.1.1 / I-DLV 1.1.6", "s(CASP) 1.1.4"]


def t_o5_table():
  rs = rows("O5_comparisons")
  order = []
  for r in rs:
    if (r["row"], r["input"]) not in order and is_gk(r):
      order.append((r["row"], r["input"]))
  body = []
  for row, inp in order:
    x = [r for r in rs if is_gk(r) and r["row"] == row and r["input"] == inp]
    d = [r for r in x if r["method"] == "default"]
    e = [r for r in x if r["method"] == "exact"]
    t = [r for r in rs if is_tool(r) and r["row"] == row and r["input"] == inp]
    vals = "; ".join(short(r["value"]) for r in d)
    by = d[0]["answered_by"] if d else ""
    comp = "yes" if d and all(r["complete"] == "yes" for r in d) else ("no" if d and d[0]["complete"] else "-")
    ex = "; ".join(short(r["value"]) for r in e) if e and e[0]["value"] else (
      e[0]["first_limit"] if e else "-")
    tool = "; ".join(short(r["value"]) for r in t) if t and t[0]["value"] else (
      (t[0]["note"] or "no value") if t else "declines the input")
    cells = []
    for s in C1_SYS:
      o = [r for r in rs if r["system"] == s and r["row"] == row]
      cells.append(o[0]["outcome"] if o else "-")
    body.append([row, inp.split("/")[-1], vals, by, comp, ex, tool] + cells)
  return table(["row", "input", "the default", "answered by", "complete", "the exact method", "the tool"] +
               [s.split(" ")[0] for s in C1_SYS], body)


# ================================================================ O6_budget

def t_o6_longer():
  """the runs at 600 s: per group and method, the runs that were wrong or without a value at 10 s and how many of
  them are right at 600 s, and the runs of the exact method that were right but not complete at 10 s"""
  rs = rows("O6_budget", "longer_limit.csv")
  keys = []
  for r in rs:
    if (r["group"], r["method"]) not in keys:
      keys.append((r["group"], r["method"]))
  body = []
  for g, m in keys + [("all", "")]:
    x = [r for r in rs if g == "all" or (r["group"] == g and r["method"] == m)]
    bad = [r for r in x if r["target"] and r["right_10s"] != "yes"]
    nc = [r for r in x if r["right_10s"] == "yes" and r["complete_10s"] == "no"]
    body.append([g, m, n(len(x)), n(len(bad)), n(count(bad, lambda r: r["right_600s"] == "yes")), n(len(nc)),
                 n(count(nc, lambda r: r["complete_600s"] == "yes")), n(count(x, lambda r: not r["target"])),
                 n(count(x, lambda r: r["value_10s"] == r["value_600s"])),
                 n(count(x, lambda r: r["ended_600s"] == "yes"))])
  return table(["group", "method", "runs", "wrong or without a value at 10 s", "of these right at 600 s",
                "right but not complete at 10 s", "of these complete at 600 s", "without a target",
                "the same value at 10 s and 600 s", "ended by itself at 600 s"], body)


def t_o6_changed():
  """the runs whose value at 600 s differs from the value at 10 s"""
  rs = [r for r in rows("O6_budget", "longer_limit.csv") if r["value_10s"] != r["value_600s"]]
  body = [["/".join(r["input"].split("/")[-2:]) if r["input"] else "-", r["method"], short(r["target"], 6),
           short(r["value_10s"], 6) if r["value_10s"] else "no value", r["right_10s"] or "-",
           short(r["value_600s"], 6) if r["value_600s"] else "no value", r["right_600s"] or "-",
           r["complete_600s"] or "-"] for r in rs]
  return table(["input", "method", "target", "value at 10 s", "right", "value at 600 s", "right",
                "complete at 600 s"], body)


def o6_runs600():
  """the count of the runs at 600 s (the runs n2/ without the two runs at 10 s)"""
  return n(count(rows("O6_budget", "runs.tsv"), lambda r: r["run_id"].startswith("n2/") and "@10s" not in r["run_id"]))


def t_o6_budget():
  rs = [r for r in rows("O6_budget") if not r["run_id"].startswith("n2/")]
  body = [[r["case"], r["limit_s"] + " s", r["method"], short(r["value"], 6), r["answered_by"],
           r["ended_by_itself"], r["first_limit"] or "-"] for r in rs]
  return table(["input", "limit", "method", "value", "answered by", "ended by itself", "first limit"], body)


# ================================================================ O7_english

def t_o7_cases():
  rs = [r for r in rows("O7_english") if is_gk(r) and r["case"] in ("N2, deepseek", "N4")]
  body = [[r["case"], r["question"], short(r["value"], 6), r["answered_by"], r["ended_by_itself"],
           r["first_limit"] or "-"] for r in rs]
  return table(["case", "question", "value of the default at 10 s", "answered by", "ended by itself",
                "first limit"], body)


def t_o7_pipeline():
  rs = [r for r in rows("O7_english") if is_gk(r) and r["set"]]
  sets = sorted({r["set"] for r in rs})
  body = []
  for s in sets:
    x = {r["run_id"]: r for r in rs if r["set"] == s}.values()
    body.append([s, n(len(x)), n(count(x, lambda r: r["class"] == "right label")),
                 n(count(x, lambda r: r["answered_by"] == "general")),
                 n(count(x, lambda r: r["answered_by"] == "exact")), n(count(x, lambda r: not r["value"]))])
  return table(["set", "tasks", "right labels", "answered by the general method", "by the exact method",
                "no value"], body)


def t_o7_others():
  rs = [r for r in rows("O7_english") if not is_gk(r) and not is_tool(r) and r["system"]]
  body = [[r["case"], r["system"], r["outcome"], r["value"] or "-", (r["note"] or "-")[:90]] for r in rs]
  return table(["case", "system", "outcome", "what the system printed", "note"], body)


# ================================================================ O8_cycles and O11_text_examples

def t_targets(part):
  rs = rows(part)
  ins = []
  for r in rs:
    if r["input"] not in ins:
      ins.append(r["input"])
  body = []
  for i in ins:
    g = [r for r in rs if r["input"] == i and is_gk(r)]
    d = pick(g, method="default") or (g[0] if g else None)
    t = pick_tool(rs, input=i)
    body.append([d["case"], d["question"], d["target"] or "-",
                 gk_cell(d) if d["class"] != "not run" else "not run", d["class"],
                 short(t["value"]) if t else "not run", t["class"].split("; ")[-1] if t else "-"])
  return table(["case", "question", "the stated value", GK() + ", the default", "against the stated value",
                "the tool", "against the stated value"], body)



# ================================================================ O13_conformance

A1_PARTS = ["sets", "keychk", "record", "families"]
A1_CLASSES = [
  ("complete and equal to an exact value of the tool", lambda c: c == "complete and equal"),
  ("complete and within the sampling bound of a sampled value of the tool",
   lambda c: c == "complete and within the sampling bound"),
  ("complete; the tool's value has a stated limit of its proof search",
   lambda c: c.startswith("the tool's value has a stated limit: complete")),
  ("complete and different", lambda c: c == "complete and different"),
  ("complete; no value of the tool", lambda c: c == "complete, no value of the tool"),
  ("not complete", lambda c: c == "not complete"),
  ("not covered", lambda c: c == "not covered"),
  ("answers of the collection that gk does not list, and runs with no named answer",
   lambda c: c.startswith("not listed") or c == "no answer named"),
]


def a1_rows(method):
  return [r for r in rows("O13_conformance") if r["part"] in A1_PARTS and r["method"] == method]


def t_o13_agreement():
  rs = a1_rows("exact")
  body = [["questions"] + [n(count(rs, lambda r: r["part"] == p)) for p in A1_PARTS] + [n(len(rs))]]
  for label, f in A1_CLASSES:
    body.append([label] + [n(count(rs, lambda r: r["part"] == p and f(r["class"]))) for p in A1_PARTS] +
                [n(count(rs, lambda r: f(r["class"])))])
  return table(["the exact method (gk -exact)"] + A1_PARTS + ["all"], body)


def t_o13_recount():
  rs = a1_rows("exact") + a1_rows("default")
  body = []
  for m in ("exact", "default"):
    x = [r for r in rs if r["method"] == m]
    lim = [r for r in x if r["class"].startswith("the tool's value has a stated limit")]
    before = count(x, lambda r: r["class"] in ("complete and equal", "exhaustive search: complete and equal")
                   or (r["class"].startswith("the tool's value has a stated limit") and "complete and equal" in
                       r["class"]))
    after = count(x, lambda r: r["class"] in ("complete and equal", "exhaustive search: complete and equal"))
    sb = count(x, lambda r: "within the sampling bound" in r["class"]
               or (r["class"].startswith("the tool's value has a stated limit") and "equal" in r["class"] and
                   "sampled" in r["target_kind"]))
    sa = count(x, lambda r: r["class"] in ("complete and within the sampling bound",
                                           "exhaustive search: complete and within the sampling bound"))
    body.append([m, n(before), n(after), n(sb), n(sa), n(len(lim))])
  return table(["method", "complete and equal to the tool, counting every value printed as exact",
                "the same, without the values with a stated limit", "within the sampling bound, before",
                "the same, after", "answers that rest on a tool value with a stated limit"], body)


def t_o13_limited():
  rs = [r for r in rows("O13_conformance") if r["part"] in A1_PARTS and
        r["class"].startswith("the tool's value has a stated limit")]
  seen = {}
  for r in rs:
    k = (r["part"], r["input"].split("/")[-1], r["question"], r["target_kind"].split(",")[0])
    seen[k] = seen.get(k, 0) + 1
  body = [[k[0], k[1], k[2], k[3], n(v)] for k, v in sorted(seen.items())]
  return table(["part", "input", "question", "the tool's value", "answers (both methods, all time limits)"], body)


def t_o13_not_complete():
  rs = [r for r in a1_rows("exact") if r["class"] == "not complete"]
  c = {}
  for r in rs:
    k = (cause(r), "value" if r["value"] else "no value")
    c[k] = c.get(k, 0) + 1
  body = [[k[0], k[1], n(v)] for k, v in sorted(c.items(), key=lambda x: (-x[1], x[0]))]
  body.append(["all", "", n(len(rs))])
  return table(["the first limit", "value", "answers"], body)


def t_o13_default():
  rs = a1_rows("default")
  body = []
  for p in A1_PARTS + ["all"]:
    x = [r for r in rs if p == "all" or r["part"] == p]
    body.append([p, n(count(x, lambda r: r["branch"] == "phase 1")), n(count(x, lambda r: r["branch"] == "direct")),
                 n(count(x, lambda r: r["branch"] == "switch"))])
  return table(["part", "the exhaustive search (the exact method)", "the general method at once",
                "the general method after a switch"], body)


def t_o13_default_classes():
  rs = a1_rows("default")
  c = {}
  for r in rs:
    c[r["class"]] = c.get(r["class"], 0) + 1
  body = [[k, n(v)] for k, v in sorted(c.items(), key=lambda x: (-x[1], x[0]))]
  body.append(["all", n(len(rs))])
  return table(["the default against the tool", "answers"], body)


def t_o13_evaluator():
  rs = rows("O13_conformance", "evaluator.csv")
  sets = []
  for r in rs:
    if r["set"] not in sets:
      sets.append(r["set"])
  body = []
  for st in sets + ["all"]:
    x = [r for r in rs if st == "all" or r["set"] == st]
    atoms = sum(int(r["atoms"]) for r in x)
    body.append([st, n(len(x)), n(atoms), n(atoms - sum(int(r["general_differ"]) for r in x)),
                 n(atoms - sum(int(r["exact_differ"]) for r in x)),
                 n(count(x, lambda r: r["exact_all_runs_complete"] == "True"))])
  return table(["set", "inputs", "atoms", "General's evaluator: atoms equal", "Exact's evaluator: atoms equal",
                "inputs with every run of Exact's evaluator complete"], body)


def t_o13_missed():
  rs = rows("O13_conformance", "missed_evidence.csv")
  g = [r for r in rs if r["method"] == "general"]
  e = [r for r in rs if r["method"] == "exact"]
  body = [["the general method", n(len(g)), n(count(g, lambda r: r["beyond_.002"] == "True")),
           n(count(g, lambda r: r["beyond_1e-6"] == "True")), "-", "-"],
          ["the exact method", n(len(e)), n(count(e, lambda r: r["beyond_.002"] == "True")),
           n(count(e, lambda r: r["beyond_1e-6"] == "True")), n(count(e, lambda r: r["complete"] == "True")),
           n(count(e, lambda r: r["complete"] == "True" and r["beyond_1e-6"] == "True"))]]
  return table(["method", "atoms", "differ from the tool beyond .002", "differ beyond 1e-6", "complete",
                "complete and different"], body)


def t_o13_by_time():
  """the general method at two time limits: the answers equal to the tool and the others, by the sign (unfinished
  work that the run reports)"""
  rs = rows("O13_conformance", "general_by_time.csv")
  body = []
  for s in sorted({r["seconds"] for r in rs}, key=float):
    x = [r for r in rs if r["seconds"] == s]
    for cls in ("equal to the tool", "differs from the tool", "no value"):
      y = [r for r in x if r["class"] == cls]
      if not y and cls == "no value":
        continue
      sign = count(y, lambda r: r["unfinished_work"] == "yes")
      body.append(["%s s" % s, cls, n(sign), n(len(y) - sign), n(len(y))])
  return table(["time limit", "answer", "reported unfinished work", "reported none", "all"], body)


NEW_PARTS = (("new", "new inputs, the stored settings"), ("new_larger", "larger inputs"))
NEW_CLASSES = ("complete and equal to an exact tool value", "complete and inside the bound of a sampled tool value",
               "complete and different", "complete, without a tool value", "not complete", "not covered", "no line",
               "no answer", "not run")


def new_rows():
  return [r for r in rows("O13_conformance") if r["part"] in ("new", "new_larger") and is_gk(r)]


def t_o13_new():
  """the check on new inputs: the exact method's answers against the tool, by class"""
  rs = new_rows()
  qs = rows("O13_conformance", "questions_new.csv")
  ins = [len({q["input"] for q in qs if q["group"] == p}) for p, _ in NEW_PARTS]
  with open(os.path.join(ROOT, "O13_conformance", "new_inputs_left_out.json")) as f:
    left = json.load(f)
  lo = [len(left.get(g, [])) for g in ("n1a", "n1b")]
  body = [["inputs"] + [n(x) for x in ins] + [n(sum(ins))],
          ["inputs left out as repeats"] + [n(x) for x in lo] + [n(sum(lo))]]
  body.append(["questions"] + [n(count(rs, lambda r, p=p: r["part"] == p)) for p, _ in NEW_PARTS] + [n(len(rs))])
  body.append(["complete"] + [n(count(rs, lambda r, p=p: r["part"] == p and r["complete"] == "yes"))
                              for p, _ in NEW_PARTS] + [n(count(rs, lambda r: r["complete"] == "yes"))])
  for c in NEW_CLASSES:
    tot = count(rs, lambda r, c=c: r["class"] == c)
    if tot or c == "complete and different":
      body.append([c] + [n(count(rs, lambda r, p=p, c=c: r["part"] == p and r["class"] == c))
                         for p, _ in NEW_PARTS] + [n(tot)])
  return table(["answer"] + [label for _, label in NEW_PARTS] + ["all"], body)


def t_o13_new_generators():
  rs = new_rows()
  gens = sorted({r["set"] for r in rs})
  body = []
  for g in gens:
    x = [r for r in rs if r["set"] == g]
    body.append([g, n(len(x)), n(count(x, lambda r: r["class"] == NEW_CLASSES[0])),
                 n(count(x, lambda r: r["class"].startswith("complete") and r["class"] != NEW_CLASSES[0])),
                 n(count(x, lambda r: r["class"] == "not complete"))])
  return table(["generator", "questions", "complete and equal to an exact tool value", "other complete answers",
                "not complete"], body)


def t_o13_new_limits():
  rs = [r for r in new_rows() if r["class"] == "not complete"]
  c = {}
  for r in rs:
    k = (r["first_limit"] or "none").split(":")[0]
    c[k] = c.get(k, 0) + 1
  body = [[k, n(v)] for k, v in sorted(c.items(), key=lambda x: (-x[1], x[0]))]
  body.append(["all", n(len(rs))])
  return table(["the first limit", "answers"], body)


def t_o13_pairs():
  rs = [r for r in rows("O13_conformance") if r["part"] == "pairs" and is_gk(r)]
  body = [["pairs", n(len(rs))], ["complete", n(count(rs, lambda r: r["complete"] == "yes"))]]
  for c in NEW_CLASSES:
    tot = count(rs, lambda r, c=c: r["class"] == c)
    if tot or c == "complete and different":
      body.append([c, n(tot)])
  return table(["answer", "pairs"], body)


def t_o13_kinds():
  rs = [r for r in rows("O13_conformance") if r["part"] == "kinds"]
  kinds = []
  for r in rs:
    if r["set"] not in kinds:
      kinds.append(r["set"])
  body = []
  for k in kinds:
    g = pick(rs, set=k, method="general")
    e = pick(rs, set=k, method="exact")
    t = [r for r in rs if r["set"] == k and is_tool(r)]
    body.append([k, g["question"], short(g["value"]), g["ended_by_itself"], short(e["value"]),
                 e["complete"], short(t[0]["value"]) if t else "-"])
  return table(["kind", "question", "the general method", "ended by itself", "the exact method", "complete",
                "the tool"], body)


# ================================================================ O14_routes

def t_o14_routes():
  rs = [r for r in rows("O14_routes") if is_gk(r) and r["run_id"].startswith("a4_route/")]
  keys = []
  for r in rs:
    if (r["family"], r["links"]) not in keys:
      keys.append((r["family"], r["links"]))
  body = []
  for f, k in keys:
    x = [r for r in rs if r["family"] == f and r["links"] == k]
    t = x[0]["target"]
    cells = []
    for m in ("exact", "exact, ground first", "general"):
      r = pick(x, method=m)
      cells.append(gk_cell(r, 6) + ("" if not r or not r["value"] else ", " + r["class"]))
    body.append([f, k, short(t, 6)] + cells)
  return table(["family", "links", "calculated value", "the exact method", "the exact method, ground first",
                "the general method"], body)


def t_o14_opposed():
  rs = [r for r in rows("O14_routes") if r["family"] == "route_opp"]
  body = []
  for k in sorted({r["links"] for r in rs}, key=int):
    x = [r for r in rs if r["links"] == k]
    e = pick(x, method="exact")
    gf = pick(x, method="exact, ground first")
    g = pick(x, method="general")
    t = [r for r in x if is_tool(r)]
    body.append([k, short(x[0]["target"], 6), gk_cell(e, 6) if e else "-", gk_cell(gf, 6) if gf else "-",
                 gk_cell(g, 6) if g else "-", (short(t[0]["value"], 6) + ", " + t[0]["class"]) if t else "-"])
  return table(["links", "calculated value", "the exact method", "the exact method, ground first",
                "the general method", "the tool"], body)


def t_o14_grounding():
  rs = rows("O14_routes")
  body = []
  for r in rs:
    if r["system"].startswith("clingo"):
      e = pick(rs, family="route_c1b", links=r["links"], method="exact")
      body.append([r["links"], n(int(r["grounder_instances"])), n(int(r["all_triples"])),
                   n(int(e["ground_statements"])) if e and e["ground_statements"] else "-",
                   n(int(e["ground_full"])) if e and e["ground_full"] else "-"])
  return table(["links", "instances of the recursive rule that clingo's grounder writes",
                "all triples of constants", "ground statements that the exact method forms",
                "ground statements of the full grounding"], body)


def t_o14_problog():
  rs = [r for r in rows("O14_routes") if r["system"].startswith("ProbLog")]
  body = []
  for r in rs:
    g = pick(rows("O14_routes"), family=r["family"], links=r["links"], method="exact")
    body.append([r["family"], r["links"], r["value"], secs(r), gk_cell(g, 6) if g else "not run"])
  return table(["family", "links", "ProbLog 2.3.0", "ProbLog's time", GK() + ", the exact method"], body)


def t_o14_university():
  rs = [r for r in rows("O14_routes") if is_gk(r) and r["family"] in ("university", "grids")]
  ins = []
  for r in rs:
    if r["input"] not in ins:
      ins.append(r["input"])
  body = []
  for i in ins:
    x = [r for r in rs if r["input"] == i]
    e = pick(x, method="exact")
    gf = pick(x, method="exact, ground first")
    g = pick(x, method="general")
    gs = "%s of %s" % (n(int(e["ground_statements"])), n(int(e["ground_full"]))) if e and e["ground_statements"] else "-"
    body.append([i.split("/")[-1], gs, gk_cell(e, 6), gk_cell(gf, 6), gk_cell(g, 6)])
  return table(["input", "ground statements formed, of the full grounding", "the exact method",
                "the exact method, ground first", "the general method"], body)


# ================================================================ O15_contradiction

def t_o15_gk():
  rs = [r for r in rows("O15_contradiction") if is_gk(r)]
  body = []
  for m in ("default", "general", "exact"):
    for v in ("a", "b"):
      x = [r for r in rs if r["method"] == m and r["version"] == v]
      kept = count(x, lambda r: r["same_as_base"] == "True")
      body.append([m, "(%s)" % v, n(len(x)), n(kept), n(len(x) - kept),
                   n(count(x, lambda r: r["complete"] == "yes")) if m != "general" else "no mark",
                   "exact %s, general %s" % (n(count(x, lambda r: r["answered_by"] == "exact")),
                                             n(count(x, lambda r: r["answered_by"] == "general"))),
                   n(count(x, lambda r: r["ended_by_itself"] == "yes"))])
  return table(["method", "variant", "queries", "value kept", "value changed", "complete", "answered by",
                "ended by itself"], body)


def t_o15_changed():
  rs = [r for r in rows("O15_contradiction") if is_gk(r)]
  body = []
  for r in rs:
    if r["same_as_base"] == "False":
      b = [x for x in rs if x["method"] == r["method"] and x["base"] == r["base"] and x["question"] == r["question"]
           and x["version"] == "base"]
      body.append([r["base"], r["question"], r["method"], gk_cell(b[0], 6) if b else "-", gk_cell(r, 6),
                   r["first_limit"] or "-"])
  return table(["base", "question", "method", "on the base", "on variant (a)", "first limit"], body)


def t_o15_others():
  rs = [r for r in rows("O15_contradiction") if not is_gk(r)]
  keys = []
  for r in rs:
    first = "first generated file" if r["outcome"] == "generated encoding rejected" else (
      "corrected file" if r["system"].startswith("PASTA") else "")
    k = (r["system"] + ((", " + first) if first else ""), r["version"], r["outcome"])
    if k not in keys:
      keys.append(k)
  body = []
  for sname, v, o in keys:
    x = [r for r in rs if (r["system"] + ((", " + ("first generated file" if r["outcome"] ==
         "generated encoding rejected" else ("corrected file" if r["system"].startswith("PASTA") else "")))
         if r["system"].startswith("PASTA") else "")) == sname and r["version"] == v and r["outcome"] == o]
    body.append([sname, v, o, n(len(x)), (x[0]["note"] or "-")[:110]])
  return table(["system", "version", "outcome", "queries", "detail of the first"], body)


# ================================================================ O16_function_terms

def t_o16_delivery():
  rs = rows("O16_function_terms")
  plans = []
  for r in rs:
    if r["plan"].startswith("gk_legs") and r["plan"] not in plans:
      plans.append(r["plan"])
  body = []
  for pl in plans:
    g = pick_gk(rs, plan=pl)
    cells = []
    for sname in ("ProbLog 2.3.0", "smProbLog 2.1.0.42", "plingo 1.1.0", "PASTA 1.0.1"):
      o = pick(rs, plan=pl, system=sname)
      cells.append((o["outcome"] + ((" " + o["value"]) if o["value"] else "")) if o else "-")
    body.append([pl, short(g["target"], 6), gk_cell(g, 6)] + cells)
  return table(["plan", "calculated value", GK() + ", the default", "ProbLog", "smProbLog", "plingo", "PASTA"], body)


def t_o16_flat():
  rs = [r for r in rows("O16_function_terms") if r["plan"].startswith("deliv_")]
  body = []
  for pl in sorted({r["plan"] for r in rs}):
    g = pick_gk(rs, plan=pl)
    t = pick_tool(rs, plan=pl)
    body.append([pl, short(g["target"], 6), gk_cell(g, 6), (short(t["value"], 6) + ", " + t["class"]) if t else "-"])
  return table(["input", "calculated value", "the exact method", "the tool"], body)


def t_o16_complete():
  rs = rows("O16_function_terms", "complete_with_function_terms.csv")
  c = {}
  for r in rs:
    k = r["kind"] + ", " + r["group"]
    c[k] = c.get(k, 0) + 1
  body = [[k, n(v)] for k, v in sorted(c.items())]
  body.append(["all", n(len(rs))])
  return table(["kind of input, group of runs", "complete answers on inputs with a function term"], body)


# ================================================================ O17_boardgameqa

def t_o17_labels():
  rs = [r for r in rows("O17_boardgameqa") if is_gk(r) and r["run_id"].startswith("c6_gk_crisp/")]
  body = []
  for st in ("d1", "d2", "d3"):
    x = [r for r in rs if r["set"] == st]
    k1 = [r for r in x if r["knowledge_test_1"] == "no"]
    k2 = [r for r in x if r["knowledge_test_2"] == "no"]
    kn = [r for r in x if r["knowledge_test_1"] != "no"]
    body.append(["depth " + st[1], n(len(x)), n(count(x, lambda r: r["answered_by"] == "exact")),
                 n(count(x, lambda r: r["complete"] == "yes")), n(count(x, right)),
                 "%s of %s" % (n(count(k1, right)), n(len(k1))), "%s of %s" % (n(count(k2, right)), n(len(k2))),
                 "%s of %s" % (n(count(kn, right)), n(len(kn)))])
  x = rs
  k1 = [r for r in x if r["knowledge_test_1"] == "no"]
  k2 = [r for r in x if r["knowledge_test_2"] == "no"]
  kn = [r for r in x if r["knowledge_test_1"] != "no"]
  body.append(["all", n(len(x)), n(count(x, lambda r: r["answered_by"] == "exact")),
               n(count(x, lambda r: r["complete"] == "yes")), n(count(x, right)),
               "%s of %s" % (n(count(k1, right)), n(len(k1))), "%s of %s" % (n(count(k2, right)), n(len(k2))),
               "%s of %s" % (n(count(kn, right)), n(len(kn)))])
  return table(["set", "examples", "answered by the exact method", "complete", "labels reproduced",
                "reproduced, without the examples that need knowledge by test 1",
                "the same, by test 1 or test 2", "reproduced among the examples of test 1"], body)


def t_o17_nine():
  rs = [r for r in rows("O17_boardgameqa") if is_gk(r) and r["run_id"].startswith("c6_gk_crisp/") and
        r["knowledge_test_1"] == "no" and r["class"] == "another label"]
  body = [["depth %s, example %s" % (r["set"][1], r["index"]), r["label"], r["gk_label"], r["cause"]] for r in rs]
  return table(["example", "label of the release", "gk's label", "the cause"], body)


def t_o17_conf():
  rs = [r for r in rows("O17_boardgameqa") if is_gk(r) and r["run_id"].startswith("c6_gk_conf/")]
  t = [r for r in rs if r["target"]]
  body = [[n(len(rs)), n(count(rs, lambda r: r["complete"] == "yes")), n(len(t)),
           n(count(t, lambda r: r["class"] == "equal"))]]
  return table(["inputs with confidences", "complete answers", "inputs with a value of the tool",
                "gk equal to the tool's exact value"], body)


def t_o17_order():
  """the conflicting pairs of rules that only the conversion's ranks order (ranks.json)"""
  import json as _json
  d = _json.load(open(os.path.join(ROOT, "O17_boardgameqa", "ranks.json")))
  both = [k for k, v in d.items() if v.get("pairs_both_can_apply")]
  rs = rows("O17_boardgameqa")
  var = [r for r in rs if r["run_id"].startswith("e4_bgqa/")]
  same = []
  for k in both:
    st, ix = k.split("/")
    conv = [r for r in rs if r["run_id"] == "c6_gk_crisp/" + k]
    if var and conv:
      same.append(short(var[0]["value"]) == short(conv[0]["value"]))
  body = [[n(len(d)), n(len(both)), n(count(same, lambda x: x)) + " of " + n(len(same))]]
  return table(["examples with a conflicting pair that only the conversion's ranks order",
                "of these, with a pair whose two rules can both apply",
                "the variant with equal ranks gives the same answer as the converted input"], body)


# ================================================================ O18_lifschitz

def t_o18():
  rs = rows("O18_lifschitz")
  keys = []
  for r in rs:
    if (r["problem"], r["conclusion"]) not in keys:
      keys.append((r["problem"], r["conclusion"]))
  body = []
  for p_, c in keys:
    x = [r for r in rs if r["problem"] == p_ and r["conclusion"] == c]
    cells = []
    for m in ("exact", "general", "default"):
      r = pick(x, method=m)
      cells.append((gk_cell(r) if r["value"] else (r["first_limit"] or "no value")) + "; " + r["class"] if r else "-")
    t = [r for r in x if is_tool(r)]
    cells.append((short(t[0]["value"]) + "; " + t[0]["class"]) if t and t[0]["value"] else (
      t[0]["note"] if t else "-"))
    body.append([p_, c] + cells)
  return table(["problem", "published conclusion", "the exact method", "the general method", "the default",
                "the tool"], body)


def t_o18_count():
  rs = rows("O18_lifschitz")
  keys = sorted({(r["problem"], r["conclusion"]) for r in rs})
  d = [pick(rs, problem=p_, conclusion=c, method="default") for p_, c in keys]
  return table(["published conclusions", "that hold under the default", "that hold under the exact method"],
               [[n(len(keys)), n(count(d, lambda r: r["class"] == "the published conclusion holds")),
                 n(count([pick(rs, problem=p_, conclusion=c, method="exact") for p_, c in keys],
                         lambda r: r["class"] == "the published conclusion holds"))]])


# ================================================================ O19_defeasible_logic

def t_o19():
  rs = rows("O19_defeasible_logic")
  keys = []
  for r in rs:
    if (r["family"], r["size"]) not in keys:
      keys.append((r["family"], r["size"]))
  body = []
  for f, sz in keys:
    x = [r for r in rs if r["family"] == f and r["size"] == sz]
    cells = []
    for m in ("exact", "general", "default"):
      r = pick(x, method=m)
      if not r:
        cells.append("-")
        continue
      v = r["verdict"] + (", complete" if r["complete"] == "yes" else "")
      if r["method"] == "default" and r["answered_by"]:
        v += ", by the %s method" % r["answered_by"]
      cells.append(v + ", " + secs(r) if r["value"] else (r["note"] or "no value"))
    sp = [r for r in x if r["system"].startswith("SPINdle")]
    de = [r for r in x if r["system"].startswith("DEFT")]
    cells.append(("%s, %s" % (sp[0]["value"], secs(sp[0]))) if sp else "-")
    if de and de[0]["run_id"]:
      cells.append("%s: %s, %s" % (de[0]["outcome"], de[0]["value"].replace("no answer: ", ""), secs(de[0])))
    else:
      cells.append(de[0]["outcome"] if de else "-")
    body.append([f, sz] + cells)
  return table(["family", "size", "the exact method", "the general method", "the default", "SPINdle 2.2.4",
                "DEFT 1.0.0"], body)


def t_o19_summary():
  rs = rows("O19_defeasible_logic")
  e = [r for r in rs if r["method"] == "exact"]
  sp = [r for r in rs if r["system"].startswith("SPINdle")]
  de = [r for r in rs if r["system"].startswith("DEFT") and r["run_id"]]
  cp = [r for r in e if r["complete"] == "yes"]
  body = [["the exact method", n(len(e)), "%s complete" % n(len(cp)), rng([r["time_s"] for r in cp])],
          ["SPINdle 2.2.4", n(len(sp)), "%s answered" % n(count(sp, lambda r: r["ended_by_itself"] == "yes")),
           rng([r["time_s"] for r in sp])],
          ["DEFT 1.0.0", n(len(de)), "%s answered, %s no answer, %s did not end" % (
            n(count(de, lambda r: r["outcome"] == "another quantity")), n(count(de, lambda r: r["outcome"] == "no answer")),
            n(count(de, lambda r: r["outcome"] == "did not end"))),
           rng([r["time_s"] for r in de if r["outcome"] == "another quantity"])]]
  return table(["system", "theories", "outcome", "times of the runs that ended by themselves"], body)


# ================================================================ O20_outside_classes

def t_o20():
  rs = rows("O20_outside_classes")
  keys = []
  for r in rs:
    if (r["K"], r["D"]) not in keys:
      keys.append((r["K"], r["D"]))
  body = []
  for k, d in keys:
    x = [r for r in rs if r["K"] == k and r["D"] == d]
    cells = []
    for m in ("exact", "exact, ground first", "general", "default"):
      r = pick(x, method=m)
      cells.append((gk_cell(r, 6) if r["value"] else (r["first_limit"] or "no value")) +
                   ("; %s MB" % r["peak_mb_run"] if r["peak_mb_run"] else "") if r else "-")
    t = [r for r in x if is_tool(r)]
    cells.append((short(t[0]["value"], 6) + ("; limit: " + t[0]["first_limit"] if t[0]["first_limit"] else "; " + t[0]["class"])) if t else "-")
    body.append([k, d, short(x[0]["target"], 6)] + cells)
  return table(["K links", "D constants not needed", "calculated value", "the exact method",
                "the exact method, ground first", "the general method", "the default", "the tool"], body)


def t_o20_summary():
  rs = [r for r in rows("O20_outside_classes") if is_gk(r)]
  body = []
  for m in ("exact", "exact, ground first", "general", "default"):
    x = [r for r in rs if r["method"] == m]
    body.append([m, n(len(x)), n(count(x, lambda r: r["complete"] == "yes")), n(count(x, right)),
                 n(count(x, lambda r: r["value"] == "(0, 0, 0, 1)"))])
  return table(["method", "inputs", "complete", "equal to the calculated value", "ignorance (0, 0, 0, 1)"], body)



# ================================================================ every part: what check_gk.py compares

def runs_of(part):
  return rows(part, "runs.tsv")


def t_check(part):
  """the runs of gk and the tool that check_gk.py reruns, and the values that it compares"""
  runs = {r["run_id"]: r for r in runs_of(part) if r["system"].startswith("gk ") or r["system"].startswith("mcref")}
  rs = [r for r in rows(part) if r["run_id"] in runs and GL.read_value(r["value"]) is not None]
  used = [r for r in rs if r["ended_by_itself"] == "no"]
  body = [[n(count(runs.values(), lambda r: r["system"].startswith("gk "))),
           n(count(runs.values(), lambda r: r["system"].startswith("mcref"))),
           n(len({r["run_id"] for r in rs})), n(len(rs)), n(len(used))]]
  return table(["gk runs", "tool runs", "runs with a recorded value", "values compared",
                "of these, on runs that did not end by themselves"], body)



# ================================================================ the first page

def distinct(rs, key="input"):
  return len({r[key] for r in rs if r.get(key)})


def t_builds():
  """the gk runs of each part, by the build of gk that made them (the column system of runs.tsv)"""
  parts = sorted((d for d in os.listdir(ROOT) if os.path.isdir(os.path.join(ROOT, d)) and d[:1] == "O"),
                 key=lambda d: int(re.match(r"O(\d+)", d).group(1)))
  counts = {}
  builds = set()
  for p in parts:
    try:
      rs = rows(p, "runs.tsv")
    except OSError:
      continue
    c = {}
    for r in rs:
      if r["system"].startswith("gk "):
        c[r["system"]] = c.get(r["system"], 0) + 1
        builds.add(r["system"])
    counts[p] = c
  builds = sorted(builds, reverse=True)
  body = [[p] + [n(counts[p].get(b, 0)) for b in builds] for p in parts if p in counts]
  body.append(["all"] + [n(sum(c.get(b, 0) for c in counts.values())) for b in builds])
  return table(["part"] + ["runs of %s" % b for b in builds], body)


def parts_list():
  return sorted((d for d in os.listdir(ROOT) if os.path.isdir(os.path.join(ROOT, d)) and d[:1] == "O"),
                key=lambda d: int(re.match(r"O(\d+)", d).group(1)))


_COST = {}


def rerun_cost(part):
  """(runs, seconds, peak MB) of what check_gk.py --part reruns: every gk and tool run with rows in results.csv.
  A run counts with its recorded time; a run without one (it did not end by itself) counts with its time limit"""
  if part in _COST:
    return _COST[part]
  try:
    runs = {r["run_id"]: r for r in rows(part, "runs.tsv") if r["system"].startswith(("gk ", "mcref"))}
  except OSError:
    _COST[part] = (0, 0.0, 0)
    return _COST[part]
  t = {}
  for r in rows(part):
    if r["run_id"] in runs:
      x = float(r["time_s"]) if r.get("time_s") else None
      if r["run_id"] not in t or (x is not None and (t[r["run_id"]] is None or x > t[r["run_id"]])):
        t[r["run_id"]] = x
  secs, peak = 0.0, 0
  for rid, x in t.items():
    run = runs[rid]
    if x is None:
      x = float(run.get("limit_s") or run.get("time_cap_s") or 10)
    secs += x
    peak = max(peak, int(run.get("peak_mb") or 0))
  _COST[part] = (len(t), secs, peak)
  return _COST[part]


def duration(s):
  if s < 60:
    return "%d s" % max(1, round(s))
  if s < 3600:
    return "%d min" % round(s / 60)
  return "%.1f h" % (s / 3600)


def all_cost():
  c = [rerun_cost(p) for p in parts_list()]
  return sum(x[0] for x in c), sum(x[1] for x in c)


def max_mem():
  best = max(((rerun_cost(p)[2], p) for p in parts_list()), default=(0, ""))
  return best


def mem_capped():
  """the runs at 600 s that ended at the memory limit of their process"""
  try:
    rs = rows("O6_budget", "longer_limit.csv")
  except OSError:
    return "0"
  return n(count(rs, lambda r: "memory limit" in r["end_600s"]))


VALUES_TOP = {"all_runs": lambda: n(all_cost()[0]), "all_time": lambda: duration(all_cost()[1]),
              "mem_capped": mem_capped,
              "max_mem": lambda: "%.1f GB" % (max_mem()[0] / 1024.0), "max_mem_part": lambda: max_mem()[1]}


def t_top():
  o2 = rows("O2_record", "inputs.csv")
  dec_ = rows("O2_record", "declined.csv")
  o3 = [r for r in rows("O3_families") if is_gk(r) and not r["strategy"] and r["method"] == "default"]
  qs = rows("O13_conformance", "questions_sets.csv")
  qk = rows("O13_conformance", "questions_keychk.csv")
  ev = rows("O13_conformance", "evaluator.csv")
  rt = [r for r in rows("O14_routes") if is_gk(r) and r["family"].startswith(("route", "rt_"))]
  links = sorted({int(r["links"]) for r in rt if r["links"]})
  o15 = [r for r in rows("O15_contradiction") if is_gk(r)]
  bg = [r for r in rows("O17_boardgameqa") if r["run_id"].startswith("c6_gk_crisp/")]
  l18 = rows("O18_lifschitz")
  o19 = [r for r in rows("O19_defeasible_logic") if r["method"] == "exact"]
  o20 = [r for r in rows("O20_outside_classes") if r["method"] == "exact"]
  o1 = [r for r in rows("O1_tweety") if is_gk(r) and r["limit_s"] == "10" and r["method"] == "default"]
  o5 = [r for r in rows("O5_comparisons") if is_gk(r) and r["method"] == "default"]
  o7 = [r for r in rows("O7_english") if is_gk(r) and r["set"]]
  scasp = [r for r in rows("O1_tweety") if r["system"].startswith("s(CASP)")]
  o13 = rows("O13_conformance")
  newq = [r for r in o13 if r["part"] in ("new", "new_larger") and is_gk(r)]
  pairs = [r for r in o13 if r["part"] == "pairs" and is_gk(r)]
  body = [
    ["[O1_tweety](O1_tweety/README.md)", "the Tweety stages, with the encodings of the other systems, and s(CASP) "
     "on stage 4", "%s inputs; %s runs of s(CASP)" % (n(distinct(o1)), n(len(scasp))), "written for this paper",
     "Sections 2 and 4; Section 7.2, the Tweety table and s(CASP); Section 7.6"],
    ["[O2_record](O2_record/README.md)", "our collection: inputs written while the method was built",
     "%s inputs; the tool accepts %s" % (n(len(o2) + len(dec_)), n(len(o2))),
     "ours: design probes, documentation examples, published studies, cases restated from the literature, "
     "inputs translated from English by a language model", "Section 7, the table of the test material"],
    ["[O3_families](O3_families/README.md)", "the benchmark families, and the table of limits",
     "%s inputs" % n(distinct(o3)),
     "published: the bnlearn networks, a LUBM-style university base, Smokers, grids; ours: delivery plans, "
     "equipment, cyclic inputs, chains and trees", "Sections 7.1, 7.3, 7.4, 7.5 and 7.6; Appendix C"],
    ["[O4_quantities](O4_quantities/README.md)", "small inputs under the quantities of the compared systems",
     "%s inputs" % n(distinct([r for r in rows("O4_quantities") if is_gk(r)])), "constructed for this paper",
     "Appendix D, the five-inputs table"],
    ["[O5_comparisons](O5_comparisons/README.md)", "the 16 small cases on 9 systems, one encoding per system",
     "%s gk inputs" % n(distinct(o5)), "constructed for this paper",
     "Section 7.2, row D3; Appendix D, the 16-case table; Appendix C"],
    ["[O6_budget](O6_budget/README.md)", "the time budget of the general method, and the runs at 600 s",
     "%s runs of the time budget; %s runs at 600 s" % (
       n(len({r["run_id"] for r in rows("O6_budget") if not r["run_id"].startswith("n2/")})), o6_runs600()),
     "inputs of parts O3, O7, O14, O15, O19 and O20", "Section 7.6, the effect of a longer time limit"],
    ["[O7_english](O7_english/README.md)", "cases translated from English, and the pipeline's tasks",
     "%s tasks" % n(distinct(o7, "run_id")), "ours: translated by a language model", "Section 7.6"],
    ["[O8_cycles](O8_cycles/README.md)", "further examples of cycles",
     "%s inputs" % n(distinct(rows("O8_cycles"))), "written for this paper",
     "Section 7.6, the table of the three methods"],
    ["[O11_text_examples](O11_text_examples/README.md)", "the small examples of the text",
     "%s inputs" % n(distinct(rows("O11_text_examples"))), "written for this paper", "Section 4; Appendix A"],
    ["[O13_conformance](O13_conformance/README.md)", "generated conformance inputs, against the tool, and "
     "further questions on new inputs",
     "%s questions; %s inputs of the evaluator check; %s further questions on new inputs; %s pairs with function "
     "terms" % (n(len(qs) + len(qk)), n(len(ev)), n(len(newq)), n(len(pairs))),
     "generated by our scripts for comparison with the tool", "Sections 7.4 and 7.6"],
    ["[O14_routes](O14_routes/README.md)", "route queries in four families",
     "%s to %s links" % (links[0], links[-1]), "constructed for this paper",
     "Sections 7.1, 7.2, 7.3, 7.5 and 7.6"],
    ["[O15_contradiction](O15_contradiction/README.md)", "the university base with an unrelated contradiction",
     "%s queries on %s bases, each with two variants" % (n(len({(r["base"], r["question"]) for r in o15})),
                                                         n(len({r["base"] for r in o15}))),
     "the university base of part O3, with generated variants", "Sections 7.2 and 7.6"],
    ["[O16_function_terms](O16_function_terms/README.md)", "delivery plans with function terms",
     "%s plans" % n(len({r["plan"] for r in rows("O16_function_terms") if r["plan"].startswith("gk_")})),
     "written for this paper", "not cited in the text"],
    ["[O17_boardgameqa](O17_boardgameqa/README.md)", "BoardgameQA, converted by a script from its formal form",
     "%s test examples" % n(len(bg)),
     "a public benchmark: Kazemi et al., NeurIPS 2023, "
     "<https://storage.googleapis.com/gresearch/BoardgameQA/BoardgameQA.zip>", "Section 7.1"],
    ["[O18_lifschitz](O18_lifschitz/README.md)", "Lifschitz's benchmark problems",
     "%s published conclusions" % n(len({(r["problem"], r["conclusion"]) for r in l18})),
     "the literature: Lifschitz, 1989", "Sections 7.1 and 7.5"],
    ["[O19_defeasible_logic](O19_defeasible_logic/README.md)", "theories of defeasible logic: chains, trees, cascades",
     "%s theories in three forms" % n(len(o19)), "the literature (2001); generated for this paper",
     "Sections 7.1, 7.5 and 7.6"],
    ["[O20_outside_classes](O20_outside_classes/README.md)", "the exact method outside both classes",
     "%s inputs" % n(len(o20)), "constructed for this paper", "Section 7.6, the table of the three methods"],
  ]
  for row in body:
    part = re.search(r"\[(O\d+_\w+)\]", row[0]).group(1)
    runs, secs, _ = rerun_cost(part)
    row += [n(runs), duration(secs)] if runs else ["0", "none: the part has no gk or tool runs of its own"]
  return table(["part", "material", "size", "where it comes from", "where the paper uses it",
                "gk and tool runs that `check_gk.py` reruns", "time with one process"], body)


TABLES = {
  ".": {"material": t_top, "builds": t_builds, "check": lambda: t_check("O18_lifschitz")},
  "O1_tweety": {"stages": t_o1_stages, "lineage": t_o1_lineage, "others": t_o1_others, "scasp": t_o1_scasp},
  "O2_record": {"classes": t_o2_classes, "general": t_o2_general, "limited": t_o2_limited, "sets": t_o2_sets, "time": t_o2_time,
                "declined": t_o2_declined, "declined_default": t_o2_declined_default},
  "O3_families": {"families": t_o3_families, "limits_a": t_o3_limits_a, "limits_b": t_o3_limits_b,
                  "limits_c": t_o3_limits_c, "problog": t_o3_problog, "strategies": t_o3_strategies},
  "O4_quantities": {"cases": t_o4_cases, "others": t_o4_others},
  "O5_comparisons": {"table": t_o5_table},
  "O6_budget": {"budget": t_o6_budget},
  "O7_english": {"cases": t_o7_cases, "pipeline": t_o7_pipeline, "others": t_o7_others},
  "O8_cycles": {"targets": lambda: t_targets("O8_cycles")},
  "O11_text_examples": {"targets": lambda: t_targets("O11_text_examples")},
  "O13_conformance": {"agreement": t_o13_agreement, "recount": t_o13_recount, "limited": t_o13_limited,
                      "not_complete": t_o13_not_complete, "default": t_o13_default,
                      "default_classes": t_o13_default_classes, "evaluator": t_o13_evaluator,
                      "missed": t_o13_missed, "kinds": t_o13_kinds},
  "O14_routes": {"routes": t_o14_routes, "opposed": t_o14_opposed, "grounding": t_o14_grounding,
                 "problog": t_o14_problog, "university": t_o14_university},
  "O15_contradiction": {"gk": t_o15_gk, "changed": t_o15_changed, "others": t_o15_others},
  "O16_function_terms": {"delivery": t_o16_delivery, "flat": t_o16_flat, "complete": t_o16_complete},
  "O17_boardgameqa": {"labels": t_o17_labels, "nine": t_o17_nine, "order": t_o17_order, "conf": t_o17_conf},
  "O18_lifschitz": {"problems": t_o18, "count": t_o18_count},
  "O19_defeasible_logic": {"theories": t_o19, "summary": t_o19_summary},
  "O20_outside_classes": {"cases": t_o20, "summary": t_o20_summary},
}
# the table of the general method by time limit, where the folder holds its runs
if any(os.path.exists(os.path.join(ROOT, "O13_conformance", "general_by_time.csv" + z)) for z in ("", ".gz")):
  TABLES["O13_conformance"]["by_time"] = t_o13_by_time
# values that a README's prose names, computed from the rows ({{V:NAME}} in the text)
VALUES = {"O6_budget": {"runs600": o6_runs600}, ".": VALUES_TOP}
# the tables of the runs at 600 s, where the folder holds them
if os.path.exists(os.path.join(ROOT, "O6_budget", "longer_limit.csv")):
  TABLES["O6_budget"].update({"longer": t_o6_longer, "changed": t_o6_changed})
# the tables of the check on new inputs, where the folder holds its questions
if any(os.path.exists(os.path.join(ROOT, "O13_conformance", "questions_new.csv" + z)) for z in ("", ".gz")):
  TABLES["O13_conformance"].update({"new": t_o13_new, "new_generators": t_o13_new_generators,
                                    "new_limits": t_o13_new_limits, "pairs": t_o13_pairs})


# ================================================================ the command line

# tables that a README holds only in some folders: the builds, for a folder of several builds of gk
OPTIONAL_TABLES = {(".", "builds")}

BLOCK = re.compile(r"<!-- table (\S+) -->\n(.*?)\n<!-- end table -->", re.S)


def compute(part, name):
  if name == "check" and part != ".":
    return t_check(part)
  return TABLES[part][name]()


def check():
  bad = 0
  checked = 0
  for part in sorted(TABLES):
    p = os.path.join(ROOT, part, "README.md")
    text = open(p).read()
    found = BLOCK.findall(text)
    names = {x for x, _ in found}
    for name in TABLES[part]:
      if name not in names and name != "check" and (part, name) not in OPTIONAL_TABLES:
        print("%s: the table %s is missing from the README" % (part, name))
        bad += 1
    for name, body in found:
      checked += 1
      fresh = compute(part, name)
      if fresh.strip() != body.strip():
        print("%s: the table %s differs from its computation" % (part, name))
        bad += 1
  print("%d tables checked, %d differ or are missing" % (checked, bad))
  return 1 if bad else 0


def main():
  if len(sys.argv) > 1 and sys.argv[1] in ("-h", "--help"):
    print(__doc__)
    sys.exit(0)
  if any(a not in TABLES and a != "--check" for a in sys.argv[1:]):
    print(__doc__)
    sys.exit(2)
  if len(sys.argv) > 1 and sys.argv[1] == "--check":
    sys.exit(check())
  parts = sys.argv[1:] or sorted(TABLES)
  for part in parts:
    for name in TABLES[part]:
      print("<!-- table %s -->\n%s\n<!-- end table -->\n" % (name, compute(part, name)))


if __name__ == "__main__":
  main()
