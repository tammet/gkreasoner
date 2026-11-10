#!/usr/bin/env python3
"""Recompute the counts of Section 7.1 of the paper from rows.tsv,
inputs.tsv and declined.tsv, and compare each with the printed count.

Usage, from this folder or any other:

  python3 count_rows.py            the counts, the comparison, the table by set
  python3 count_rows.py --rows     also the 19 differing rows and the Yale row

Python 3.8 or later, standard library only. Exit status 0 means that every
count equals the printed one.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DIFFER = ("differ, gk records a reading", "differ, gk used a contrapositive", "differ, gk used a step not represented",
          "differ, no flag")
SETS = ("ab", "examples", "families", "lit", "studies", "demo", "table", "paper", "boundary")


def read(name):
  lines = open(os.path.join(HERE, name), encoding="utf-8").read().rstrip("\n").split("\n")
  cols = lines[0].split("\t")
  return [dict(zip(cols, l.split("\t"))) for l in lines[1:]]


def shares(text):
  return [float(x) for x in text.strip("[]").split(",")] if text else None


def main():
  rows, inputs, declined = read("rows.tsv"), read("inputs.tsv"), read("declined.tsv")
  agree = [r for r in rows if r["class"] == "agree with recursive"]
  differ = [r for r in rows if r["class"] in DIFFER]
  unresolved = [r for r in rows if r["class"].startswith("incomplete")]
  only_tool = [r for r in rows if r["class"].startswith("binding only in mcref")]
  only_gk = [r for r in rows if r["class"] == "binding only in the record"]
  neither = [r for r in rows if r["class"] == "no answer in either"]
  with_support = [r for r in only_tool if shares(r["mcref"])[0] > float(r["tolerance"])]
  settled = agree + differ
  comparable = settled + [r for r in unresolved if r["gk"]]
  reading = [r for r in differ if r["flags"] and set(r["flags"].split("; ")) - {"contrapositive use of a certain rule"}]
  def first(r):
    f = r["flags"].split("; ")
    for name in ("cycle cut", "residual variable represented by a fresh constant", "step not represented"):
      if name in f:
        return name
    return None
  by_first = {}
  for r in reading:
    by_first[first(r)] = by_first.get(first(r), 0) + 1
  no_reading = [r for r in differ if r not in reading]
  cut = [r for r in no_reading if int(r["searches_cut"] or 0) > 0]
  exits = {}
  for r in rows:
    exits[r["input"]] = r["gk_exit"]
  sets_all = {s for d in declined for s in d["sets"].split()} | {x["set"] for x in inputs}
  reasons = {}
  for d in declined:
    reasons[d["reason"]] = reasons.get(d["reason"], 0) + 1
  translated = [d for d in declined if set(d["sets"].split()) & {"nlpipe", "mle"}]
  counts = [
    ("inputs in the collection", len(inputs) + len(declined), 1022, "a collection of 1,022 inputs"),
    ("sets", len(sets_all), 11, "in eleven sets"),
    ("inputs the tool declines", len(declined), 662, "The tool declines 662 of the inputs"),
    ("declined for equality", reasons.get("equality", 0), 522, "522 of them for equality"),
    ("declined for function symbols", reasons.get("function symbols", 0), 86, "86 for function symbols"),
    ("declined inputs of the two translated sets", len(translated), 445, "All 445 inputs of the two translated sets"),
    ("inputs the tool accepts", len(inputs), 360, "and accepts 360"),
    ("gk processes that ended with exit status 0", sum(1 for v in exits.values() if v == "0"), 360,
     "All 360 processes ended normally"),
    ("answer rows", len(rows), 438, "The 360 inputs give 438 rows"),
    ("rows with a value on both sides", len(comparable), 395, "On 395 rows both sides give a value"),
    ("resolved rows", len(settled), 394, "we call these 394 rows resolved"),
    ("resolved rows that agree", len(agree), 375, "375 of the 394 rows agree"),
    ("resolved rows that differ", len(differ), 19, "and 19 differ"),
    ("rows with an unresolved share (the Yale row)", len(unresolved), 1, "The remaining row is the Yale shooting problem"),
    ("rows without a comparable value", len(rows) - len(comparable), 43, "The 43 rows without a comparable value"),
    ("instances only the tool lists", len(only_tool), 35, "35 instances that only the tool lists"),
    ("instances only gk lists", len(only_gk), 4, "4 that only GK lists"),
    ("inputs where neither side answers", len(neither), 4, "4 inputs on which neither side gives an answer"),
    ("instances only the tool lists, with a for share above e", len(with_support), 4, "Four of the 35 have support"),
    ("differing rows with an approximation note", len(reading), 14, "Of the 104 rows with a note, 14 differ"),
    ("  of these first: cycle cut", by_first.get("cycle cut", 0), 12, "12 have the cycle cut"),
    ("  first: residual variable", by_first.get("residual variable represented by a fresh constant", 0), 1,
     "one a residual variable"),
    ("  first: step not represented", by_first.get("step not represented", 0), 1, "one a step not represented"),
    ("differing rows without an approximation note", len(no_reading), 5, "Five differing rows have no note"),
    ("  of these with a search stopped by the budget", len(cut), 3, "On three of them the budget stopped searches"),
    ("  of these with no search stopped", len(no_reading) - len(cut), 2, "On the other two every search ended"),
  ]
  bad = 0
  print("%-58s %6s %6s" % ("count", "rows", "paper"))
  for name, n, printed, phrase in counts:
    mark = "" if printed is None else ("ok" if n == printed else "DIFF")
    bad += mark == "DIFF"
    print("%-58s %6d %6s %s" % (name, n, "" if printed is None else printed, mark))
  yale = unresolved[0] if unresolved else None
  if yale:
    print("\nthe Yale row: %s, gk %s, tool %s, unresolved share %s, gk's approximation notes: %s" % (
      yale["input"], yale["gk"], yale["mcref"], yale["unresolved"], yale["readings"]))
  print("the two differing rows where every search ended:")
  for r in no_reading:
    if r not in cut:
      print("  %s %s: gk %s, tool %s" % (r["input"], r["answer"], r["gk"], r["mcref"]))
  print("\n%-10s %6s %6s %8s %6s %6s %8s" % ("set", "inputs", "rows", "resolved", "agree", "differ", "no value"))
  for s in SETS + ("total",):
    rs = rows if s == "total" else [r for r in rows if r["set"] == s]
    ins = inputs if s == "total" else [x for x in inputs if x["set"] == s]
    st = [r for r in rs if r["class"] == "agree with recursive" or r["class"] in DIFFER]
    comp = st + [r for r in rs if r["class"].startswith("incomplete") and r["gk"]]
    print("%-10s %6d %6d %8d %6d %6d %8d" % (s, len(ins), len(rs), len(st),
                                            sum(1 for r in st if r["class"] == "agree with recursive"),
                                            sum(1 for r in st if r["class"] in DIFFER), len(rs) - len(comp)))
  if "--rows" in sys.argv:
    print("\nthe 19 differing rows:")
    for r in differ:
      print("  %s %s\n    gk %s, tool %s; flags: %s; searches stopped %s" % (
        r["input"], r["answer"], r["gk"], r["mcref"], r["flags"] or "none", r["searches_cut"]))
  print("\n%d counts differ from the paper" % bad)
  sys.exit(1 if bad else 0)


if __name__ == "__main__":
  main()
