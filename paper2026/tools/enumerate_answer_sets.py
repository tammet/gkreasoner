#!/usr/bin/env python3
"""Values of the published semantics of PASTA and smProbLog, by enumeration.

The input is an answer set program whose probabilistic facts are written
p::atom. on lines of their own, as in the PASTA files of this folder. For
every choice of the probabilistic facts the script asks clingo for all answer
sets of the rest of the program. Then for each query atom q:

- PASTA (credal semantics): lower = mass of the choices where every answer
  set holds q; upper = mass of the choices where some answer set holds q.
  "normalized" divides both by the mass of the choices with an answer set,
  as PASTA's option --normalize does.
- smProbLog: the mass of each choice is divided equally among its answer
  sets; true = mass with q, false = mass of answer sets without q,
  inconsistent = mass of the choices without an answer set.

Usage: python3 tools/enumerate_answer_sets.py FILE.lp QUERY [QUERY ...]
Example: python3 tools/enumerate_answer_sets.py O1_tweety/stage3b/pasta.lp "flies(tweety)"
Needs the clingo Python module (pip install clingo).
"""
import itertools, re, sys
import clingo


def split(path):
  rules, facts = [], []
  for line in open(path):
    m = re.match(r"([0-9.]+)::(.*)\.\s*$", line.strip())
    if m:
      facts.append((float(m.group(1)), m.group(2)))
    elif line.strip():
      rules.append(line.strip())
  return rules, facts


def answer_sets(rules, true_facts):
  ctl = clingo.Control(["0", "--warn=none"])
  ctl.add("base", [], "\n".join(rules + [f + "." for f in true_facts]))
  ctl.ground([("base", [])])
  out = []
  ctl.solve(on_model=lambda m: out.append(set(str(s) for s in m.symbols(atoms=True))))
  return out


def main():
  if len(sys.argv) < 3:
    sys.exit(__doc__)
  rules, facts = split(sys.argv[1])
  queries = sys.argv[2:]
  res = {q: [0.0, 0.0, 0.0, 0.0] for q in queries}   # lower, upper, true, false
  inconsistent = 0.0
  for bits in itertools.product((True, False), repeat=len(facts)):
    p = 1.0
    true = []
    for (pr, a), b in zip(facts, bits):
      p *= pr if b else 1 - pr
      if b:
        true.append(a)
    ms = answer_sets(rules, true)
    if not ms:
      inconsistent += p
      continue
    for q in queries:
      k = sum(1 for m in ms if q in m)
      r = res[q]
      if k == len(ms):
        r[0] += p
      if k > 0:
        r[1] += p
      r[2] += p * k / len(ms)
      r[3] += p * (len(ms) - k) / len(ms)
  cons = 1 - inconsistent
  print("%d choices, mass without an answer set %.6g" % (2 ** len(facts), inconsistent))
  for q in queries:
    lo, up, t, f = res[q]
    norm = "[%.6g, %.6g]" % (lo / cons, up / cons) if cons > 0 else "none"
    print("%s: PASTA [%.6g, %.6g], normalized %s; smProbLog (%.6g, %.6g, %.6g)" % (
      q, lo, up, norm, t, f, inconsistent))


if __name__ == "__main__":
  main()
