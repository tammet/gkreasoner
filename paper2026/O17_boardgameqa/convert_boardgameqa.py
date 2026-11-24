#!/usr/bin/env python3
"""convert_boardgameqa.py RELEASE.zip OUT: convert the test examples of BoardgameQA-Main-depth1, -depth2 and -depth3
into gk input, and mark the examples whose label needs knowledge that the theory does not state (the first test).

The release: https://storage.googleapis.com/gresearch/BoardgameQA/BoardgameQA.zip (CC BY), from Kazemi et al.,
"BoardgameQA: A Dataset for Natural Language Reasoning with Contradictory Information", NeurIPS 2023. The script
reads the release's test.json files as data (json.load only); run it with python3 -I.

Per example two inputs: the crisp one, convert(theory, goal), and the one with confidences,
convert(theory, goal, fact_conf="0.9", rule_conf="0.8"). The functions slug, tuple_lit, lit_gkp, parse_theory and
convert are the converter of the paper's literature examples, unchanged. A rule's rank is 1, and one more than the
highest rank of any rule that it is preferred over.

Writes OUT/<set>/crisp/e<index>.gkp, OUT/<set>/conf/e<index>.gkp, OUT/meta.json (per example: set, index, label,
goal, question, ranks, conversion status and reason, the first knowledge test and the unmatched literals) and
OUT/counts.json, and prints the counts. Python 3.9 or later, no other package."""
import collections
import json
import os
import re
import sys
import zipfile

SETS = [("d1", "BoardgameQA-Main-depth1"), ("d2", "BoardgameQA-Main-depth2"), ("d3", "BoardgameQA-Main-depth3")]


def slug(s):
  s = s.strip().lower()
  s = re.sub(r"[^a-z0-9]+", "_", s).strip("_")
  if not s: s = "x"
  if s[0].isdigit(): s = "n" + s
  return s

def tuple_lit(t):
  """'~(X, take, snake)' -> (neg, pred, [args]); variables X, Y stay variables"""
  neg = t.startswith("~"); t = t.lstrip("~").strip()
  assert t.startswith("(") and t.endswith(")"), t
  parts = [p.strip() for p in t[1:-1].split(", ", 2)]
  assert len(parts) == 3, t
  subj, rel, obj = parts
  args = [a if a in ("X", "Y") else slug(a) for a in (subj, obj)]
  return neg, slug(rel), args

def lit_gkp(neg, pred, args): return ("-" if neg else "") + f"{pred}({', '.join(args)})"

def parse_theory(theory):
  facts, rules, prefs, sec = [], [], [], None
  for line in theory.splitlines():
    s = line.strip()
    if s.startswith("Facts"): sec = "f"; continue
    if s.startswith("Rules"): sec = "r"; continue
    if s.startswith("Preferences"): sec = "p"; continue
    if not s: continue
    {"f": facts, "r": rules, "p": prefs}[sec].append(s)
  return facts, rules, prefs

def convert(theory, goal, fact_conf=None, rule_conf=None):
  facts, rules, prefs = parse_theory(theory)
  rank = {}
  names = [r.split(":", 1)[0].strip() for r in rules]
  for n in names: rank[n] = 1
  better = {}
  for p in prefs:
    a, b = [x.strip() for x in p.split(">")]
    better.setdefault(a, set()).add(b)
  for _ in range(len(names) + 1):
    for a, bs in better.items():
      for b in bs:
        if rank[a] <= rank[b]: rank[a] = rank[b] + 1
  gk, pr = [], []
  fc = f"{fact_conf}::" if fact_conf else ""; fcp = f"{fact_conf} :: " if fact_conf else ""
  rc = f"{rule_conf}::" if rule_conf else ""; rcp = f"{rule_conf} :: " if rule_conf else ""
  for f in facts:
    neg, pred, args = tuple_lit(f)
    gk.append(f"{fc}{lit_gkp(neg, pred, args)}."); pr.append(f"{fcp}{lit_gkp(neg, pred, args)}.")
  for r in rules:
    name, body_head = r.split(":", 1)
    name = name.strip(); body, head = [x.strip() for x in body_head.split("=>", 1)]
    body = re.sub(r"^exists [XY] ", "", body)
    blits = [tuple_lit(t) for t in re.findall(r"~?\([^()]*\)", body)]
    hneg, hpred, hargs = tuple_lit(head)
    h = lit_gkp(hneg, hpred, hargs); comp = lit_gkp(not hneg, hpred, hargs)
    bl = ", ".join(lit_gkp(*b) for b in blits)
    gk.append(f"{rc}{h} :- {bl}, unless({comp}, {rank[name]}).")
    pr.append(f"{rcp}{h} <- {bl} [unless {comp}, rank {rank[name]}].")
  gneg, gpred, gargs = tuple_lit(goal)
  q = lit_gkp(gneg, gpred, gargs)
  return "\n".join(gk) + f"\nquery({q}).", " ".join(pr), q, rank

def reason_of(e):
  """a short reason for a failed conversion"""
  t = type(e).__name__
  msg = str(e)
  if t == "AssertionError":
    if msg.startswith("(") or msg.startswith("~"):
      return "AssertionError: a literal that is not of the form (subject, relation, object): " + msg[:80]
    return "AssertionError: a literal without parentheses: " + msg[:80]
  if t == "KeyError":
    return "KeyError: a preference names a rule that the theory does not have: " + msg[:40]
  return "%s: %s" % (t, msg[:80])

def literals_of_rule(r):
  """(name, [body literals], head literal) of a rule line, the way convert() reads it"""
  name, body_head = r.split(":", 1)
  body, head = [x.strip() for x in body_head.split("=>", 1)]
  body = re.sub(r"^exists [XY] ", "", body)
  blits = [tuple_lit(t) for t in re.findall(r"~?\([^()]*\)", body)]
  return name.strip(), blits, tuple_lit(head)

def matches(a, b):
  if a[0] != b[0] or a[1] != b[1] or len(a[2]) != len(b[2]):
    return False
  for x, y in zip(a[2], b[2]):
    if x in ("X", "Y") or y in ("X", "Y"):
      continue
    if x != y:
      return False
  return True

def knowledge(theory, proof):
  """(needs knowledge, [unmatched body literals of the rules that the proof cites]) or (None, why)"""
  facts, rules, _ = parse_theory(theory)
  fl = [tuple_lit(f) for f in facts]
  parsed = {}
  for r in rules:
    n, b, h = literals_of_rule(r)
    parsed[n] = (b, h)
  heads = [h for b, h in parsed.values()]
  # the rules that the proof applies: "according to Rule<n>"; a rule named only as a conflicting rule ("we cannot
  # prove the antecedent", "higher preference than the conflicting rules (Rule<n>)") is not applied
  cited = sorted(set(re.findall(r"according to (Rule\d+)\b", proof or "")), key=lambda s: int(s[4:]))
  miss = []
  for n in cited:
    if n not in parsed:
      continue
    for lit in parsed[n][0]:
      if not any(matches(lit, x) for x in fl + heads):
        miss.append("%s: %s%s(%s)" % (n, "-" if lit[0] else "", lit[1], ", ".join(lit[2])))
  return bool(miss), miss, cited

def main():
  if len(sys.argv) != 3:
    print(__doc__)
    sys.exit(2)
  zpath, out_dir = sys.argv[1], sys.argv[2]
  sets_data = {}
  with zipfile.ZipFile(zpath) as z:
    for _, name in SETS:
      sets_data[name] = json.loads(z.read("BoardgameQA/%s/test.json" % name).decode("utf-8"))
  meta = []
  counts = collections.OrderedDict()
  for tag, name in SETS:
    exs = sets_data[name][:1000]
    c = collections.Counter()
    for kind in ("crisp", "conf"):
      os.makedirs(os.path.join(out_dir, tag, kind), exist_ok=True)
    for i, e in enumerate(exs):
      m = {"set": tag, "release_set": name, "index": i, "label": e["label"], "goal": e["goal"]}
      c["examples"] += 1
      c["label " + e["label"]] += 1
      try:
        g1, _p1, q, rank = convert(e["theory"], e["goal"])
        g2, _p2, _q2, _r2 = convert(e["theory"], e["goal"], fact_conf="0.9", rule_conf="0.8")
      except Exception as ex:
        m["converted"] = False
        m["reason"] = reason_of(ex)
        c["not converted"] += 1
        meta.append(m)
        continue
      m["converted"] = True
      m["question"] = q
      m["ranks"] = rank
      m["statements"] = g1.count("\n")
      for kind, text in (("crisp", g1), ("conf", g2)):
        with open(os.path.join(out_dir, tag, kind, "e%d.gkp" % i), "w") as f:
          f.write(text + "\n")
      if re.search(r":- ,", g1):
        m["empty_body"] = True
        c["converted with an empty rule body"] += 1
      try:
        need, miss, cited = knowledge(e["theory"], e.get("proof"))
        m["needs_knowledge"] = need
        m["unmatched"] = miss
        m["cited_rules"] = cited
        c["needs knowledge"] += 1 if need else 0
        c["needs knowledge, label " + e["label"]] += 1 if need else 0
      except Exception as ex:
        m["needs_knowledge"] = None
        m["knowledge_error"] = "%s: %s" % (type(ex).__name__, str(ex)[:80])
        c["knowledge check failed"] += 1
      c["converted"] += 1
      meta.append(m)
    counts[tag] = c
  json.dump(meta, open(os.path.join(out_dir, "meta.json"), "w"), indent=0)
  json.dump({t: dict(c) for t, c in counts.items()}, open(os.path.join(out_dir, "counts.json"), "w"), indent=1)
  for t, c in counts.items():
    print("== %s (%s)" % (t, dict(SETS)[t]))
    for k in sorted(c):
      print("  %-70s %5d" % (k, c[k]))


if __name__ == "__main__":
  main()
