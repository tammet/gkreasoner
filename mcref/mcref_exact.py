#!/usr/bin/env python3
"""mcref_exact: exact evaluation of the five numbers of the support semantics by cells.

mcref.py calls run() for --mode auto and --mode exact; the file also runs
alone. It imports the mcref of its own folder (MCREF_DIR in the environment
selects another folder) and uses its functions unchanged: the reading of the
input (mcref_read.read_input), the applications (orient), no self-support, the
closure, the rank-context check, the reachable literals, the cycle groups
(build_comps, group_kinds) and the evaluation of one world (world). Only
the sampling of mcref.run() is replaced. For every atom whose numbers
matter (mcref's needu and needv), the cut points are the supports of every
subset of the atom's applications of each sign (for applications with rule
identities, mcref.support() of every subset). The states of a world are
constant inside each cell of the cut points, so world() runs once at the
midpoint of each cell, and the cell's volume is added to the state of each
question. The result is exact up to the rounding of doubles. prepare() and
run() also accept the ground clauses and the directed statements of one
world of the sampling check (tests/sampling_check.py).

Usage: mcref_exact.py INPUT [--max-cells N] [--refine K] [--all-atoms]
                            [--max-ground N] [--cases] [--proofs] [--layers] [--ranks]
Run alone it computes the rules of mcref.py --rules 1.1; --proofs --layers
give the definition. --refine K splits every cell into K equal parts on
every axis (a test of the cells).
Output: one JSON line {"exact": {...}}, with the answers in mcref's form:
"value" (for, against, conflict, ignorance; swapped for a negated question)
and "unstable" (the unresolved share). "too_many_cells" when the cells
exceed --max-cells; "unsupported" as mcref gives it."""
import argparse
import itertools
import json
import os
import sys

MCREF_DIR = os.environ.get("MCREF_DIR", os.path.dirname(os.path.abspath(__file__)))   # this folder
sys.path.insert(0, MCREF_DIR)
import mcref  # noqa: E402
from mcref import (POS, NEG, IGN, closure, rank_contexts, reachable, orient, build_comps,  # noqa: E402
                   group_kinds, world, app_text, SweepError)
from mcref_read import Unsupported, atom_text, lit_text, read_input, untyped  # noqa: E402

VERSION = mcref.VERSION


def prepare(path, max_ground=200000, all_atoms=False, files=None, inp=None, ground=None, directed=None):
  """mcref.run() up to the loop over the worlds: the same steps in the same
  order. Returns a dict with the state of the run, or {"unsupported": ...}.
  inp, ground, directed: an input already read, other ground clauses for it
  and the statements whose certain rules keep their direction (a world of
  the sampling check)."""
  files = files if files is not None else []
  if inp is None:
    inp = read_input(path, max_ground, files)
  qs, qp, qargs = inp.question
  gr = inp.ground if ground is None else ground
  apps, dropped = orient(gr) if directed is None else orient(gr, None, directed)
  byhead = {}
  for x in apps:
    byhead.setdefault(x.head, []).append(x)
  insts = []
  if inp.qvars:
    for tup in itertools.product(inp.constants, repeat=len(inp.qvars)):
      sub = dict(zip(inp.qvars, tup))
      key = (qp, tuple(sub.get(a, a) for a in qargs))
      if key in byhead:
        insts.append((lit_text(qs, *key), key, [untyped(t) for t in tup]))
  else:
    insts.append((lit_text(qs, qp, qargs), (qp, qargs), []))
  atoms = {x.head for x in apps} | {b for x in apps for _s, b in x.body + x.exc} | {k for _t, k, _b in insts}
  if getattr(mcref, "PROOFS", False):
    atoms |= {k for x in apps if x.cls for k in x.cls}
    atoms |= {a for k in mcref.CLAUSE_LITS for _s, a in mcref.CLAUSE_LITS[k]}
  qatoms = closure([k for _t, k, _b in insts], byhead)
  rc = rank_contexts(atoms, byhead)
  why = [rc[k] for _t, k, _b in insts if k in rc]
  if why:
    return {"unsupported": why[0]}
  rel = atoms if all_atoms else qatoms
  readings = []
  for si, x, lit in dropped:
    if x.head in rel:
      readings.append(["self exception", "statement %d: %s (exception %s)" % (si + 1, app_text(x),
                                                                           lit_text(lit[0], *lit[1]))])
  if hasattr(mcref, "rule1_filter"):
    apps = mcref.rule1_filter(apps)   # no self-support (mcref.py), before the applications whose body can never hold
  possible = reachable(apps)
  order = sorted(rel, key=lambda k: (atom_text(*k), k[1] is None))
  idx = {k: i for i, k in enumerate(order)}
  n = len(order)
  if hasattr(mcref, "setup_clause_nodes"):
    mcref.setup_clause_nodes(idx)
  byatom = [[] for _ in range(n)]
  tuple_of = getattr(mcref, "tuple_of", None)
  part4 = tuple_of is not None and any(getattr(x, "ids", None) for x in apps)
  for x in apps:
    if x.head in idx:
      h = idx[x.head]
      if tuple_of is not None:
        byatom[h].append(tuple_of(x, idx, part4))
        continue
      body = [(idx[a], POS if s == 0 else NEG) for s, a in x.body]
      exc = [(idx[a], POS if s == 0 else NEG) for s, a in x.exc]
      byatom[h].append((x.hsign, 1.0 - x.conf, body, exc, x.normal, x.rank))
  live = {(POS if sg == 0 else NEG, idx[a]) for sg, a in possible if a in idx}
  byatom = [[x for x in byatom[h] if all((sg, j) in live for j, sg in x[2])] for h in range(n)]
  if hasattr(mcref, "setup_concluded"):
    mcref.setup_concluded(byatom)
  if hasattr(mcref, "deps_of"):
    deps = mcref.deps_of(byatom, n)
  else:
    deps = [sorted({j for x in byatom[h] for j, _s in x[2] + x[3]}) for h in range(n)]
  comps = group_kinds(build_comps(deps, n), byatom)
  both = [len({x[0] for x in byatom[i]}) == 2 for i in range(n)]
  needu = [i for i in range(n) if both[i] or any(x[1] > 0 for x in byatom[i])]
  needv = [i for i in range(n) if both[i] and any(x[4] for x in byatom[i])]
  if getattr(mcref, "PROOFS", False) and mcref.LAST_PROOFS is not None:
    ps = mcref.LAST_PROOFS
    readings.append(["proofs", "%d applications of proofs of several statements (%d proofs, %d absorbed)%s"
                     % (len(ps["applications"]), ps.get("proofs", 0), ps.get("absorbed", 0),
                        "; LIMIT: %s, evaluated with the single applications only" % ps["limit"] if ps["limit"] else "")])
  return {"inp": inp, "apps": apps, "dropped": dropped, "insts": insts, "order": order, "idx": idx, "n": n,
          "byatom": byatom, "comps": comps, "needu": needu, "needv": needv, "readings": readings, "rc": rc,
          "qs": qs, "qatoms": qatoms}


def cut_points(apps_of_atom, refine=1):
  """the bounds of the cells of one atom's number: 0, 1 and the support of
  every subset of the atom's applications of each sign; with refine K each
  interval is split into K equal parts"""
  pts = {0.0, 1.0}
  for sign in (0, 1):
    side = [x for x in apps_of_atom if x[0] == sign]
    qs = [x[1] for x in side]
    if len(qs) > 16:
      raise OverflowError("an atom with %d applications of one sign" % len(qs))
    if any(len(x) > 6 for x in side):   # rule identities: the support of every subset, by mcref
      for k in range(len(side) + 1):
        for sub in itertools.combinations(side, k):
          a = mcref.support(list(sub))
          if 0.0 < a < 1.0:
            pts.add(a)
      continue
    for k in range(len(qs) + 1):
      for sub in itertools.combinations(qs, k):
        r = 1.0
        for q in sub:
          r *= q
        a = 1.0 - r
        if 0.0 < a < 1.0:
          pts.add(a)
  b = sorted(pts)
  if refine > 1:
    out = []
    for lo, hi in zip(b, b[1:]):
      for j in range(refine):
        out.append(lo + (hi - lo) * j / refine)
    out.append(1.0)
    b = sorted(set(out))
  return b


def run(path, max_cells=2000000, refine=1, all_atoms=False, max_ground=200000, inp=None, ground=None, directed=None):
  res = {"version": VERSION, "input": path, "answers": [], "unsupported": None, "cells": None,
         "too_many_cells": None, "evaluated_atoms": None, "groups": None}
  try:
    pr = prepare(path, max_ground, all_atoms, None, inp, ground, directed)
  except Unsupported as e:
    res["unsupported"] = str(e)
    return res
  if "unsupported" in pr:
    res["unsupported"] = pr["unsupported"]
    return res
  n, byatom, comps = pr["n"], pr["byatom"], pr["comps"]
  res["evaluated_atoms"] = n
  res["readings"] = pr["readings"]
  kinds = {0: "one", 1: "sweep", 2: "narrow_ign", 3: "narrow_unres"}
  res["groups"] = [{"atoms": [atom_text(*pr["order"][i]) for i in nodes], "kind": kinds[kind]}
                   for nodes, _o, _i, kind in comps if kind != 0]
  axes = []   # (atom, 'u' or 'v', bounds)
  try:
    for i in pr["needu"]:
      axes.append((i, 0, cut_points(byatom[i], refine)))
    for i in pr["needv"]:
      axes.append((i, 1, cut_points(byatom[i], refine)))
  except OverflowError as e:
    res["too_many_cells"] = str(e)
    return res
  total = 1
  for _i, _k, b in axes:
    total *= len(b) - 1
  res["cells"] = total
  if total > max_cells:
    res["too_many_cells"] = "%d cells, more than %d" % (total, max_cells)
    return res
  qidx = [pr["idx"][key] for _t, key, _b in pr["insts"]]
  acc = [[0.0] * 5 for _ in qidx]
  aacc = [[0.0] * 5 for _ in range(n)] if all_atoms else None
  state, u, v = [IGN] * n, [0.0] * n, [0.0] * n
  stats = [0]
  ranges = [list(zip(b, b[1:])) for _i, _k, b in axes]
  circle = getattr(mcref, "CIRCLE_LAST", None)
  circle_share, circle_q, circle_groups = 0.0, [0.0] * len(qidx), set()
  if circle is not None:
    mcref.CIRCLE_STATS["groups"] = set()
  for cell in itertools.product(*ranges):
    w = 1.0
    for (i, k, _b), (lo, hi) in zip(axes, cell):
      mid = (lo + hi) / 2
      if k == 0:
        u[i] = mid
      else:
        v[i] = mid
      w *= hi - lo
    world(byatom, comps, u, v, state, stats)
    if circle:
      circle_share += w
      for j, qi in enumerate(qidx):
        if qi in circle:
          circle_q[j] += w
    for j, qi in enumerate(qidx):
      acc[j][state[qi]] += w
    if all_atoms:
      for i in range(n):
        aacc[i][state[i]] += w
  qs = pr["qs"]
  clause_of = getattr(mcref, "CLAUSE_OF", {})
  if circle is not None and clause_of:
    res["clause_rule_in_circle"] = {"world_share": circle_share, "question_share": circle_q,
                                    "groups": [[atom_text(*pr["order"][i]) for i in g if i not in clause_of]
                                               for g in sorted(mcref.CIRCLE_STATS["groups"])]}
  if getattr(mcref, "PROOFS", False) and mcref.LAST_PROOFS is not None:
    res["proofs"] = {k: mcref.LAST_PROOFS[k] for k in ("limit", "proofs", "absorbed", "triples", "resolvents",
                                                       "normal_ranks_differ", "normal_uncertain_left_out",
                                                       "free_with_exceptions")
                     if k in mcref.LAST_PROOFS}
    res["proofs"]["applications"] = len(mcref.LAST_PROOFS["applications"])
  for j, (text, key, binding) in enumerate(pr["insts"]):
    c = list(acc[j])
    if qs == 1:
      c[0], c[1] = c[1], c[0]
    a = {"instance": text, "value": c[:4], "unstable": c[4]}
    if pr["inp"].qvars:
      a["binding"] = binding
    res["answers"].append(a)
  if all_atoms:
    rc = pr["rc"]   # as mcref: an atom where rank contexts can matter has no value
    res["atom_values"] = [{"atom": atom_text(*pr["order"][i]), "unsupported": rc[pr["order"][i]]}
                          if pr["order"][i] in rc else
                          {"atom": atom_text(*pr["order"][i]), "value": aacc[i][:4], "unstable": aacc[i][4]}
                          for i in range(n) if i not in clause_of]
  return res


def main():
  ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
  ap.add_argument("input")
  ap.add_argument("--max-cells", type=int, default=2000000)
  ap.add_argument("--refine", type=int, default=1)
  ap.add_argument("--all-atoms", action="store_true")
  ap.add_argument("--max-ground", type=int, default=200000)
  ap.add_argument("--cases", action="store_true")
  ap.add_argument("--proofs", action="store_true")
  ap.add_argument("--layers", action="store_true")
  ap.add_argument("--ranks", action="store_true")
  a = ap.parse_args()
  mcref.CASES = a.cases
  if hasattr(mcref, "PROOFS"):
    mcref.PROOFS, mcref.LAYERS, mcref.RANKS = a.proofs, a.layers, a.ranks
  try:
    res = run(a.input, a.max_cells, a.refine, a.all_atoms, a.max_ground)
  except SweepError as e:
    sys.stderr.write("SweepError: %s\n" % (e.args[0],))
    sys.exit(3)
  print(json.dumps({"exact": res}))


if __name__ == "__main__":
  main()
