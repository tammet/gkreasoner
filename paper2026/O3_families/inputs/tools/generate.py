#!/usr/bin/env python3
"""Write the generated inputs of part O3 into a folder.

The generation functions in generators/ are copied unchanged from the
generators of the trial of 2026-11-04. This script calls them with the
sizes and seeds of the trial and writes each input under its name in this
part. The files it writes are byte for byte the files of the part folder,
so a reader can check them with diff:

  python3 tools/generate.py --out /some/new/folder
  diff -r /some/new/folder/grids grids

The Bayesian networks need pgmpy, networkx and the five BIF files of the
bnlearn repository (see README.md, "The bnlearn networks"):

  python3 tools/generate.py --out FOLDER --bif FOLDER_WITH_BIF_FILES

Without --bif the networks are skipped. The hand-written inputs of
equipment/ (the controls, the derived identity and the probes) are not
generated. Python 3.8 or later.
"""
import argparse, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PART = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(HERE, "generators"))
import cyclic, defaults, deft, first_order, grids_smokers, smokers_variants, spindle, university  # noqa: E402

FILES = {}


def put(path, text):
  FILES[path] = text


def lines(cl, q):
  return "\n".join(cl) + f"\nquery({q}).\n"


def grids_and_smokers():
  # the full 16 x 16 grid at distance d, and the corner grid of the last
  # (d+1) x (d+1) nodes; the ProbLog file and the gk file are the same text
  for d in (1, 2, 3, 4, 5, 6, 8):
    facts, rules, q = grids_smokers.grid(16, d, full=True)
    body = "\n".join(facts + rules) + f"\nquery({q}).\n"
    put(f"grids/gk_full_d{d}.gkp", body)
    put(f"grids/problog_full_d{d}.pl", body)
  for d, edges in ((2, 16), (3, 33), (4, 56)):
    facts, rules, q = grids_smokers.grid(16, d, full=False)
    assert len(facts) == edges
    body = "\n".join(facts + rules) + f"\nquery({q}).\n"
    put(f"grids/gk_corner{edges}.gkp", body)
    put(f"grids/problog_corner{edges}.pl", body)
  for n in (5, 8, 12, 16, 20):
    facts, rules, q, _ = grids_smokers.smokers(n, seed=n)
    body = "\n".join(facts + rules) + f"\nquery({q}).\n"
    put(f"smokers/gk_smokers{n}.gkp", body)
    put(f"smokers/problog_smokers{n}.pl", body)
  for n in (5, 8, 12):
    gk, pl, q, _, _ = smokers_variants.variant1(n, seed=n)
    put(f"smokers/gk_stratified{n}.gkp", lines(gk, q))
    put(f"smokers/problog_stratified{n}.pl", lines(pl, q))
    gk, _, q, _, _ = smokers_variants.variant2(n, seed=n)
    put(f"smokers/gk_ranked{n}.gkp", lines(gk, q))


def cyclic_families():
  def write(name, pl, gk, q):
    put(f"cyclic/problog_{name}.pl", lines(pl, q))
    put(f"cyclic/gk_{name}.gkp", lines(gk, q))
    out = []
    for line in pl:
      if "::" in line and ":-" not in line:
        p, a = line[:-1].split("::")
        out.append(f'{a} :- &problog("{p}").')
      else:
        out.append(line.replace("\\+", "not "))
    put(f"cyclic/plingo_{name}.plp", "\n".join(out) + f"\n&query({q}).\n")
  for n in (4, 6, 8, 12, 20, 40):
    pl, gk, q = cyclic.random_program(n, seed=100 + n, pos_rules=max(1, n // 4))
    write(f"program{n}", pl, gk, q)
  for k in (3, 4, 5, 8, 15, 30):
    pl, gk, q = cyclic.ring(k)
    write(f"ring{k}", pl, gk, q)
  for n, p in ((6, 0.3), (10, 0.25), (20, 0.12), (40, 0.06), (80, 0.03)):
    cl, lab, attacks = cyclic.af(n, p, seed=n)
    att = cyclic.af.att
    for want in ("in", "out", "undec"):
      xs = [x for x in range(n) if lab[x] == want]
      if not xs:
        continue
      x = xs[0]
      name = f"af{n}_{want}_x{x}"
      put(f"cyclic/gk_{name}.gkp", lines(cl, f"acc(x{x})"))
      if want != "in" and len(att[x]) > 1:
        put(f"cyclic/gk_{name}_att.gkp", lines(cl, f"att_x{x}"))


def default_families():
  for n, strict, name in ((100, False, "chain100"), (500, False, "chain500"), (1000, False, "chain1000"),
                          (1000, True, "strict_chain1000")):
    cl, q, _ = defaults.chain(n, strict)
    put(f"chains_trees/gk_{name}.gkp", lines(cl, q))
  for b, d in ((2, 5), (3, 5), (2, 10)):
    cl, q, _, count = defaults.tree(b, d)
    put(f"chains_trees/gk_tree{count}.gkp", lines(cl, q))
  for n in (4, 5, 10, 50, 200):
    for pr in (True, False):
      cl, q, _ = defaults.cascade(n, pr)
      put(f"cascades/gk_cascade{n}_{'priorities' if pr else 'equal'}.gkp", lines(cl, q))


def defeasible_theories():
  # SPINdle 2.2.4 (DFL) and DEFT 1.0.0 (DLGP); the file text is the clause list
  # with a final newline, as the trial's runners wrote it
  def dfl(folder, name, cl):
    put(f"{folder}/spindle_{name}.dfl", "\n".join(cl) + "\n")
  for n in (100, 1000, 10000, 100000):
    cl, _ = spindle.chain(n, False)
    dfl("chains_trees", f"chain{n}", cl)
    if n != 100000:
      # the strict chain of 100,000 rules ran, but its theory is not stored
      cl, _ = spindle.chain(n, True)
      dfl("chains_trees", f"strict_chain{n}", cl)
  for n in (100, 10000):
    cl, _ = spindle.cycle(n)
    dfl("chains_trees", f"cycle{n}", cl)
  for n in (5, 200, 2000):
    for pr in (True, False):
      cl, _ = spindle.cascade(n, pr)
      dfl("cascades", f"cascade{n}_{'priorities' if pr else 'equal'}", cl)
  for b, d in ((2, 5), (3, 5), (2, 10), (2, 14)):
    cl, _, count = spindle.tree(b, d)
    dfl("chains_trees", f"tree{count}", cl)
  for m in (1000, 10000):
    cl, _ = spindle.disputed(m)
    dfl("chains_trees", f"disputed{m}", cl)

  def dlgp(folder, name, cl):
    put(f"{folder}/deft_{name}.dlgp", "\n".join(cl) + "\n")
  for n in (100, 1000, 5000):
    cl, _ = deft.chain(n)
    dlgp("chains_trees", f"chain{n}", cl)
  for b, d in ((2, 5), (3, 5), (2, 10)):
    cl, _, count = deft.tree(b, d)
    dlgp("chains_trees", f"tree{count}", cl)
  for n in (5, 50, 200):
    for pr in (True, False):
      cl, _ = deft.cascade(n, pr)
      dlgp("cascades", f"cascade{n}_{'priorities' if pr else 'equal'}", cl)
  for m in (100, 1000):
    cl, _ = deft.disputed(m)
    dlgp("chains_trees", f"disputed{m}", cl)


def university_base():
  import random
  university.RULES[:] = [l.strip() for l in open(os.path.join(PART, "university", "univ_bench_rules.pl")) if l.strip()]
  for ndept, scale, tag in ((1, 0.25, "dept1_scale0.25"), (1, 1.0, "dept1_scale1"), (3, 1.0, "dept3_scale1")):
    facts, people = university.university(ndept, seed=ndept, scale=scale)
    prof, grad = people[0]
    for q in (f"person({grad})", f"employee({prof})", "organization(dept0)", f"memberOf({prof},dept0)"):
      rnd = random.Random(ndept + 7)
      rules = university.usable_rules(facts)
      body = "\n".join([f"{rnd.uniform(0.05, 1.0):.2f}::{f}." for f in facts] + rules) + f"\nquery({q}).\n"
      name = f"{tag}_{q.split('(')[0]}"
      put(f"university/gk_{name}.gkp", body)
      put(f"university/problog_{name}.pl", body)


def first_order_families():
  def record(path, ls, problog=True):
    put(path + ".gkp", "\n".join(ls) + "\n")
    pl = first_order.to_problog(ls) if problog else None
    if pl and not any("=" in l and "::" not in l and ":-" not in l for l in ls):
      folder, name = os.path.split(path)
      put(os.path.join(folder, name.replace("gk_", "problog_", 1)) + ".pl", "\n".join(pl) + "\n")
  for k in (1, 3, 6, 10, 20):
    record(f"equipment/gk_equality_chain{k}", first_order.equip_lines(ident_chain=k))
  for n in (2, 4, 8, 16):
    record(f"equipment/gk_components{n}", first_order.equip_lines(extra_components=n))
  record("equipment/gk_second_supply", first_order.equip_lines(distinct=True))
  for b in (10, 50, 200):
    record(f"equipment/gk_background{b}", first_order.equip_lines(background=b))
  for n in (2, 4, 8, 16, 32):
    for opp in (False, True):
      kind = "opposed" if opp else "control"
      record(f"delivery/gk_legs{n}_{kind}", first_order.deliv_lines(n_legs=n, opposed=opp))
      if n <= 4:
        record(f"delivery/gk_legs{n}_{kind}_flat", first_order.deliv_lines(n_legs=n, opposed=opp, flat=True))
  for k in (1, 5, 20, 50):
    record(f"delivery/gk_exception_chain{k}", first_order.deliv_lines(n_legs=1, h=.3, opposed=True, exc_chain=k))
  for b in (10, 50, 200):
    record(f"delivery/gk_background{b}", first_order.deliv_lines(n_legs=1, h=.3, opposed=True, background=b))


def networks(bif):
  import networks as N
  for net in ("asia", "earthquake", "cancer", "win95pts", "andes"):
    nodes, _ = N.read_bif(os.path.join(bif, net + ".bif"))
    cl = N.to_gkp(nodes)
    depth = N.depth_order(nodes)
    names = [n["name"] for n in nodes]
    # the trial's queries: the deepest node, a middle one, the node with the most parents
    deepest = max(names, key=lambda x: depth[x])
    mid = sorted(names, key=lambda x: depth[x])[len(names) // 2]
    fat = max(nodes, key=lambda n: len(n["parents"]))["name"]
    qs = []
    for q in (deepest, mid, fat):
      if q not in qs:
        qs.append(q)
    for q in qs:
      put(f"bn/gk_{net}_{N.atom(q)}.gkp", "\n".join(cl) + f"\nquery({N.atom(q)}).\n")


def main():
  ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
  ap.add_argument("--out", required=True, help="the folder to write into")
  ap.add_argument("--bif", help="the folder with asia.bif, earthquake.bif, cancer.bif, win95pts.bif, andes.bif")
  a = ap.parse_args()
  grids_and_smokers()
  cyclic_families()
  default_families()
  defeasible_theories()
  university_base()
  first_order_families()
  if a.bif:
    networks(a.bif)
  for path, text in sorted(FILES.items()):
    p = os.path.join(a.out, path)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w") as f:
      f.write(text)
  print(len(FILES), "files written into", a.out)


if __name__ == "__main__":
  main()
