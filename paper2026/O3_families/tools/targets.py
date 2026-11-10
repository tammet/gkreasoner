#!/usr/bin/env python3
"""The exact targets of part O3, by small independent calculations.

No solver runs. The calculations come from the review of the trial's records
of 2026-11-04, changed to read the files of this folder:

- the 16-edge corner grid: enumeration of the 2^16 edge choices;
- the university answers: each answer is a disjunction of independent facts,
  so its probability is 1 minus the product of their complements; the script
  computes the sets of source facts to a least fixed point;
- the cascades: the value by the recurrence from the fact a_n;
- the ring of 3: its 8 choices, with the ring left in ignorance when all
  three facts hold;
- the hand values of the delivery and equipment families;
- with --bif FOLDER: the seven marginals of Asia, Earthquake and Cancer by
  rational enumeration of every state, from the decimals of the BIF files.

Usage, from this part folder or elsewhere:

  python3 tools/targets.py [--bif BIF_FOLDER]

Prints one JSON object. Python 3.8 or later, standard library only.
"""
import argparse, glob, itertools, json, os, re, sys
from fractions import Fraction as F

PART = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PART, "tools", "generators"))
import first_order  # noqa: E402


def corner16():
  text = open(os.path.join(PART, "grids", "gk_corner16.gkp")).read()
  edges = re.findall(r"0\.5::edge\((\w+),\s*(\w+)\)", text)
  source, target = re.search(r"query\(path\((\w+),\s*(\w+)\)\)", text).groups()
  assert len(edges) == 16
  successes = 0
  for bits in itertools.product((False, True), repeat=len(edges)):
    reachable = {source}
    while True:
      enlarged = reachable | {b for (a, b), present in zip(edges, bits) if present and a in reachable}
      if enlarged == reachable:
        break
      reachable = enlarged
    successes += target in reachable
  exact = F(successes, 2 ** len(edges))
  return {"fraction": str(exact), "value": float(exact), "three_proofs_found_by_gk": str(F(23, 64))}


def networks(bif):
  out = {}
  queries = {"asia": ["xray", "bronc", "either"], "earthquake": ["JohnCalls", "Alarm"], "cancer": ["Xray", "Cancer"]}
  for network, nodes in queries.items():
    text = open(os.path.join(bif, network + ".bif")).read()
    states = dict((n, [s.strip() for s in ss.split(",")]) for n, ss in
                  re.findall(r"variable\s+(\w+)\s*\{\s*type discrete\s*\[\s*2\s*\]\s*\{([^}]+)\}", text))
    cpts = {}
    for header, body in re.findall(r"probability\s*\(([^)]+)\)\s*\{([^}]+)\}", text):
      head, *parentpart = header.split("|")
      head = head.strip()
      parents = [s.strip() for s in parentpart[0].split(",")] if parentpart else []
      if not parents:
        table = {(): [F(s.strip()) for s in re.search(r"table\s+([^;]+);", body)[1].split(",")]}
      else:
        table = {tuple(s.strip() for s in key.split(",")): [F(x.strip()) for x in values.split(",")]
                 for key, values in re.findall(r"\(([^)]+)\)\s*([^;]+);", body)}
      assert all(sum(x) == 1 for x in table.values())
      cpts[head] = (parents, table)
    assert set(states) == set(cpts)
    totals = {n: F(0) for n in states}
    mass = F(0)
    for chosen in itertools.product(*states.values()):
      world = dict(zip(states, chosen))
      weight = F(1)
      for n, (parents, table) in cpts.items():
        weight *= table[tuple(world[p] for p in parents)][states[n].index(world[n])]
      mass += weight
      for n in states:
        if world[n] == states[n][0]:
          totals[n] += weight
    assert mass == 1
    for n in nodes:
      out[f"{network}_{n.lower()}"] = {"fraction": str(totals[n]), "value": float(totals[n])}
  return out


def atom(s):
  name, args = re.fullmatch(r"(\w+)\(([^()]*)\)", s.strip()).groups()
  return name, tuple(a.strip() for a in args.split(","))


def university():
  # On these generated inputs the only rule with two body atoms is the
  # transitive subOrganizationOf rule, and its base edges cannot compose.
  # Every other rule has one body atom, so every answer is an OR of
  # independent input facts.
  out = {}
  for path in sorted(glob.glob(os.path.join(PART, "university", "gk_*.gkp"))):
    lines = open(path).read().splitlines()
    facts, rules, transitive_seen, query = [], [], False, None
    for line in lines:
      line = line.strip()
      if not line:
        continue
      if line.startswith("query("):
        query = line[len("query("):-2]
        continue
      if "::" in line:
        probability, literal = line[:-1].split("::")
        facts.append((F(probability), atom(literal)))
      elif line == "subOrganizationOf(X,Z) :- subOrganizationOf(X,Y), subOrganizationOf(Y,Z).":
        transitive_seen = True
      else:
        head, body = line[:-1].split(" :- ")
        rules.append((atom(head), atom(body)))
    assert transitive_seen
    links = [args for _, (pred, args) in facts if pred == "subOrganizationOf"]
    assert not ({a for a, b in links} & {b for a, b in links})
    assert not any(h[0] == "subOrganizationOf" for h, b in rules)
    lineage = {}
    for i, (_, a) in enumerate(facts):
      lineage.setdefault(a, set()).add(i)
    changed = True
    while changed:
      changed = False
      for (pred, args), sources in list(lineage.items()):
        for (hp, ha), (bp, ba) in rules:
          if bp != pred or len(ba) != len(args):
            continue
          subst = {}
          for var, term in zip(ba, args):
            if var in subst:
              assert subst[var] == term
            subst[var] = term
          head = hp, tuple(subst[x] for x in ha)
          old = lineage.setdefault(head, set())
          new = sources - old
          if new:
            old.update(new)
            changed = True
    sources = lineage.get(atom(query), set())
    complement = F(1)
    for i in sorted(sources):
      complement *= 1 - facts[i][0]
    out[os.path.basename(path)] = {"independent_sources": len(sources), "value": float(1 - complement),
                                   "exactly_one": complement == 0}
  return out


def cascades():
  out = {}
  for n in (4, 5, 10, 50, 200):
    for kind, rank in (("priorities", 2), ("equal", 1)):
      lines = [l.strip() for l in open(os.path.join(PART, "cascades", f"gk_cascade{n}_{kind}.gkp")) if l.strip()]
      expected = [f"a{n}."]
      for i in range(n - 1, -1, -1):
        expected += [f"a{i} :- unless(-a{i}, 1).", f"-a{i} :- a{i+1}, unless(a{i}, {rank})."]
      assert lines == expected + ["query(a0)."], (n, kind)
      # priorities: a_i is negative when a_(i+1) is positive, else positive
      # equal ranks: a_i is ignorance when a_(i+1) is positive, else positive
      state = "positive"
      for _ in range(n):
        if kind == "priorities":
          state = "negative" if state == "positive" else "positive"
        else:
          state = "ignorance" if state == "positive" else "positive"
      out[f"gk_cascade{n}_{kind}.gkp"] = {"positive": [1, 0, 0, 0], "negative": [0, 1, 0, 0],
                                          "ignorance": [0, 0, 0, 1]}[state]
  return out


def ring3():
  worlds, positive = [], 0
  for facts in itertools.product((False, True), repeat=3):
    state, seen = (False,) * 3, set()
    while state not in seen:
      seen.add(state)
      nxt = tuple(facts[i] and not state[(i + 1) % 3] for i in range(3))
      if nxt == state:
        break
      state = nxt
    else:
      assert all(facts)
      state = (False,) * 3   # ignorance after narrowing in this case
    positive += state[0]
    worlds.append({"switches": list(map(int, facts)), "usable": list(map(int, state))})
  return {"value": str(F(positive, 8)), "worlds": worlds}


def hand_values():
  out = {"delivery": {}, "equipment": {}}
  for n in (2, 4, 8, 16, 32):
    out["delivery"][f"legs{n}_control"] = first_order.deliv_target(n)
    out["delivery"][f"legs{n}_opposed"] = first_order.deliv_target(n, opposed=True)
  out["delivery"]["exception_chain and background"] = first_order.deliv_target(1, .3, True)
  for label, kw in (("equality_chain and background", {}), ("components2", {"extra_components": 2}),
                    ("components4", {"extra_components": 4}), ("components8", {"extra_components": 8}),
                    ("components16", {"extra_components": 16}), ("second_supply", {"distinct": True})):
    one, two = first_order.equip_targets(**kw)
    out["equipment"][label] = {"first reading (two atoms)": two, "second reading (one atom)": one}
  return out


def main():
  ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
  ap.add_argument("--bif", help="the folder with asia.bif, earthquake.bif and cancer.bif")
  a = ap.parse_args()
  out = {"corner16": corner16(), "university": university(), "cascades": cascades(), "ring3": ring3(),
         "hand_values": hand_values()}
  if a.bif:
    out["small_networks"] = networks(a.bif)
  print(json.dumps(out, indent=1))


if __name__ == "__main__":
  main()
