#!/usr/bin/env python3
"""mcref: an independent Monte Carlo reference for the support semantics of
gk's recursive method (step 16 of the gk 1.2 work, 2026-10-29; step 19,
2026-11-03: the tool computes the semantics memo of 2026-11-03).

The definition it computes is the support semantics of 2026-11-03, stated in
Doc/support_semantics.md (Section 14). The section numbers cited below as
"memo" are those of the unpublished memo of 2026-11-03 that the page follows.
It reads a gk input and grounds it over the input's
constants (mcref_read.py), turns every ground clause into applications (memo
4.1), draws one pair of uniform numbers (U, V) per ground atom, evaluates
every cycle group in that world by the tables of memo 4 and the procedures of
memo 5, and counts the state of the question. It calls no prover and shares
no code with gk; gk runs only as `gk FILE -writejson -recursive` to read
inputs that are not JSON.

Interpretation, printed in every output: a certain rule with a written head
and no exception literal is used in every direction (memo 4.1); below
confidence 1, or with an exception literal, a rule derives its written head
only; a flat clause gives one application per literal, an uncertain one with
a source event; a classical consequence that needs several clauses at once
is not represented; the domain is the constants of the input; the kind of a
side is decided in each world from the present applications (memo 4.5); a
cycle across signs is evaluated by the narrowing of memo 5.5; an application
whose exception is its own body literal never applies (decision 68).
Constants are typed: 1, 1.0 and "1" are three terms.

The rows of the tables (function `outcome`) are those of memo 4.2 and 4.4,
not gk's C code. README.md describes the tool.

Usage: mcref.py INPUT [--samples N] [--seed N] [--max-ground N] [--all-atoms]
Output: one JSON line {"mcref": {...}}."""
import argparse
import itertools
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcref_read import Unsupported, atom_text, lit_text, read_input, sha256_file, untyped  # noqa: E402

VERSION = "1.1.1"   # the tool's version, printed in every output
POS, NEG, CON, IGN, UNRES = 0, 1, 2, 3, 4
MASK = (1 << 64) - 1
GOLDEN = 0x9E3779B97F4A7C15   # splitmix64's increment
TWO53 = 2.0 ** -53
INTERPRETATION = {
  "semantics": "Doc/support_semantics.md, the support semantics of 2026-11-03",
  "written-head rules": "a certain rule without exception literals is used in every direction (memo 4.1); "
                        "below confidence 1 or with an exception literal, at its written head only",
  "flat clauses": "one application per literal; one source event per uncertain ground clause",
  "not represented": "a classical consequence that needs several input clauses at once",
  "domain": "the constants of the input",
  "kind of a side": "decided in each world from the applications present in it (memo 4.4, 4.5)",
  "cycles": "a cycle across signs by the narrowing of memo 5.5, ordinary applications first when the group has "
            "normal defaults; a one-sign or exception-only group by sweeps, the narrowing only when the sweeps "
            "repeat a state, an undecided atom then read as ignorance (memo 5.1, 5.4)",
  "unresolved": "an atom of a cycle across signs left possible but not sure (memo 5.4, 5.5); a group that depends "
                "on an unresolved atom runs the narrowing with that atom's two literals possible and neither sure "
                "(memo 5), and an atom of it left possible but not sure is unresolved too",
  "rank contexts (decision 13)": "not covered; an input where they can matter is unsupported",
  "self exception (decision 68)": "an application whose exception is its own body literal never applies",
}
HERE = os.path.dirname(os.path.abspath(__file__))
TOOL = {f: sha256_file(os.path.join(HERE, f)) for f in ("mcref.py", "mcref_read.py")}


# ------------------------------------------------------------------ applications

class App:
  __slots__ = ("head", "hsign", "body", "exc", "conf", "normal", "rank", "kind", "crank")

  def __init__(self, head, hsign, body, exc, conf, normal, rank, kind, crank):
    self.head, self.hsign, self.body, self.exc = head, hsign, body, exc
    self.conf, self.normal, self.rank, self.kind, self.crank = conf, normal, rank, kind, crank


def uniq(xs):
  out = []
  for x in xs:
    if x not in out:
      out.append(x)
  return out


def application(h, body, excs, strength, conf, crank, flat):
  """one application with head literal h. The complement of the head among
  the exceptions marks a normal default (memo 4.4): it is not tested for
  presence, and its strength is the rank. The other exceptions decide
  presence (memo 4.3)."""
  head, sign = (h[1], h[2]), h[0]
  comp = (1 - sign, head)
  if comp in excs:
    return App(head, sign, body, [e for e in excs if e != comp], conf, True, strength[comp], "normal default", crank)
  if excs:
    return App(head, sign, body, list(excs), conf, False, 0, "default", crank)
  return App(head, sign, body, [], conf, False, 0, "fact" if not body else ("classical" if flat else "directed"), 0)


def app_text(x):
  t = lit_text(x.hsign, *x.head)
  if x.body:
    t += " <- " + ", ".join(lit_text(s, *a) for s, a in x.body)
  if x.exc:
    t += " [unless " + ", ".join(lit_text(s, *a) for s, a in x.exc) + "]"
  return t


def orient(gclauses):
  """the applications of the ground clauses (memo 4.1); source events get
  atoms ('$src_i', ()). A certain clause with a written head and no
  exception literal is the same statement as the disjunction of its
  literals and gives one application per literal (memo 4.1, second bullet;
  decision 69). Decision 68: an application whose exception literal is one
  of its body literals never applies; it is not created, and it is returned
  in `dropped` as (statement index, application, literal). The test is made
  on the ground application, after the existential expansion of decision 67,
  so an exception that matches a body literal by binding only its
  exception-only variables counts (case 1)."""
  apps, nsrc, dropped = [], 0, []
  def keep(x, si):
    same = [e for e in x.exc if e in x.body]
    if same:
      dropped.append((si, x, same[0]))
    else:
      apps.append(x)
  for si, conf, lits, blocks, head in gclauses:
    excs = uniq([(l[0], (l[1], l[2])) for _st, l in blocks])
    strength = {}
    for st, l in blocks:
      k = (l[0], (l[1], l[2]))
      strength[k] = max(strength.get(k, 0), st)
    crank = max(strength.values()) if strength else 0
    if len(lits) == 1:
      head = 0
    if head is not None and len(lits) > 1 and conf >= 1 and not blocks:
      head = None   # a certain written-head rule without exceptions: every direction (memo 4.1)
    if head is not None:   # a fact, or an uncertain rule or a default with a written head: its head only
      h = lits[head]
      body = uniq([(1 - l[0], (l[1], l[2])) for i, l in enumerate(lits) if i != head])
      keep(application(h, body, excs, strength, conf, crank, False), si)
      continue
    extra, c2 = [], conf   # a flat clause: one application per literal
    if conf < 1:
      nsrc += 1
      src = ("$src_%d" % nsrc, ())
      apps.append(App(src, 0, [], [], conf, False, 0, "source event", 0))
      extra, c2 = [(0, src)], 1.0
    for i, h in enumerate(lits):
      body = uniq([(1 - l[0], (l[1], l[2])) for j, l in enumerate(lits) if j != i] + extra)
      keep(application(h, body, excs, strength, c2, crank, True), si)
  return apps, dropped


# ------------------------------------------------------------------ static passes before sampling

def closure(starts, byhead):
  """the atoms the start atoms depend on, through bodies and exceptions"""
  seen, todo = set(), list(starts)
  while todo:
    a = todo.pop()
    if a in seen:
      continue
    seen.add(a)
    for x in byhead.get(a, []):
      todo += [b for _s, b in x.body + x.exc if b not in seen]
  return seen


def by_components(atoms, byhead, own, combine):
  """a value per atom over its dependency closure: own(a) combined with the
  values of the atoms a depends on (bodies and exceptions), computed over
  the strongly connected components, dependencies first"""
  order = sorted(atoms, key=lambda k: (atom_text(*k), k[1] is None))
  idx = {k: i for i, k in enumerate(order)}
  deps = [sorted({idx[b] for x in byhead.get(a, []) for _s, b in x.body + x.exc}) for a in order]
  val = [None] * len(order)
  for nodes in components(deps, len(order)):
    v = None
    for i in nodes:
      v = combine(v, own(order[i]))
      for j in deps[i]:
        if j not in nodes:
          v = combine(v, val[j])
    for i in nodes:
      val[i] = v
  return {order[i]: val[i] for i in range(len(order))}


def lower(a, b):
  return b if a is None or (b is not None and b[0] < a[0]) else a


def rank_contexts(atoms, byhead):
  """decision 13 is not covered. A default of positive rank k (the largest
  strength of its $block literals) is affected when the dependency closure
  of one of its external exceptions (bodies and exceptions, through
  rank-zero defaults) holds a default of a positive rank below k; the
  normal marker is no exception here. Returns, for every atom whose own
  closure holds an affected default, the description of one such case."""
  def own_min(a):
    r = [(x.crank, lit_text(x.hsign, *x.head)) for x in byhead.get(a, []) if x.crank > 0]
    return min(r) if r else None
  low = by_components(atoms, byhead, own_min, lower)
  bad = {}
  for a in atoms:
    for x in byhead.get(a, []):
      if x.crank > 0 and x.exc:
        for _s, e in x.exc:
          m = low.get(e)
          if m is not None and m[0] < x.crank:
            bad.setdefault(a, "rank contexts: a rank-%d default for %s inside a rank-%d exception check" % (
              m[0], m[1], x.crank))
  return {a: v for a, v in by_components(atoms, byhead, lambda a: bad.get(a),
                                         lambda u, w: u if u is not None else w).items() if v is not None}


def reachable(apps):
  """the literals that some chain of applications derives from the facts,
  exceptions and opposition ignored (memo 4.6): a least fixpoint over the
  applications. An application with a body literal outside it is present in
  no world; it is removed before the cycle groups are formed."""
  possible, waiting, need = set(), {}, {}
  todo = []
  for i, x in enumerate(apps):
    need[i] = len(x.body)
    for lit in x.body:
      waiting.setdefault(lit, []).append(i)
    if not x.body:
      todo.append(i)
  while todo:
    x = apps[todo.pop()]
    lit = (x.hsign, x.head)
    if lit in possible:
      continue
    possible.add(lit)
    for j in waiting.get(lit, []):
      need[j] -= 1
      if need[j] == 0:
        todo.append(j)
  return possible


def components(deps, n):
  """the strongly connected components of h -> deps[h], dependencies first
  (Tarjan's algorithm, iterative)"""
  index, low, onst, st, out, c = [None] * n, [0] * n, [False] * n, [], [], 0
  for root in range(n):
    if index[root] is not None:
      continue
    work = [(root, 0)]
    while work:
      h, i = work.pop()
      if i == 0:
        index[h] = low[h] = c
        c += 1
        st.append(h)
        onst[h] = True
      if i < len(deps[h]):
        work.append((h, i + 1))
        j = deps[h][i]
        if index[j] is None:
          work.append((j, 0))
        elif onst[j]:
          low[h] = min(low[h], index[j])
        continue
      if low[h] == index[h]:
        comp = []
        while True:
          j = st.pop()
          onst[j] = False
          comp.append(j)
          if j == h:
            break
        out.append(sorted(comp))
      if work:
        low[work[-1][0]] = min(low[work[-1][0]], low[h])
  return out


def build_comps(deps, n):
  """the cycle groups (memo 5) in dependency order: (atoms, the outside
  atoms the group depends on, the readers of each atom inside the group,
  whether the group has a cycle)"""
  comps = []
  for nodes in components(deps, n):
    members = set(nodes)
    outside = sorted({j for i in nodes for j in deps[i] if j not in members})
    inner = {i: [] for i in nodes}
    for h in nodes:
      for j in deps[h]:
        if j in members:
          inner[j].append(h)
    comps.append((nodes, outside, inner, len(nodes) > 1 or nodes[0] in deps[nodes[0]]))
  return comps


# ------------------------------------------------------------------ the tables (memo 4.2, 4.4)

def rows(np, nn, ordp, ordn, rp, rn, a, b, u, v):
  """the state of an atom from its two sides: np, nn applications present
  for and against it, ordp, ordn of them ordinary, rp, rn the largest ranks
  of the normal defaults, a, b the supports (memo 4.2 steps 1 to 4, the
  table of 4.2 and the table of 4.4). The kind of a side is decided here,
  from the present applications (memo 4.5)."""
  if not np and not nn:
    return IGN
  if not nn:
    return POS if u < a else IGN
  if not np:
    return NEG if u < b else IGN
  normp = ordp == 0
  normn = ordn == 0
  if not normp and not normn:
    if b <= u < a:
      return POS
    if a <= u < b:
      return NEG
    return CON if u < min(a, b) else IGN
  if normp and not normn:
    return NEG if u < b else (POS if v < a else IGN)
  if normn and not normp:
    return POS if u < a else (NEG if v < b else IGN)
  if rp == rn or rp == 0 or rn == 0:
    p, q = u < a, v < b
    return POS if p and not q else (NEG if q and not p else IGN)
  if rp > rn:
    return POS if u < a else (NEG if u < b else IGN)
  return NEG if u < b else (POS if u < a else IGN)


def outcome(apps, state, u, v):
  """the state of one atom from the final states of the atoms it reads: an
  application is present when its body literals are usable and none of its
  exceptions is (memo 4.2). apps holds (sign, 1 - confidence, body,
  exceptions, normal, rank) with body and exception entries (atom, state)."""
  ra = rb = 1.0
  np = nn = 0
  ordp = ordn = 0
  rp = rn = 0
  for x in apps:
    ok = True
    for a, s in x[2]:
      if state[a] != s:
        ok = False
        break
    if ok:
      for a, s in x[3]:
        if state[a] == s:
          ok = False
          break
    if not ok:
      continue
    if x[0] == 0:
      np += 1
      ra *= x[1]
      if x[4]:
        rp = max(rp, x[5])
      else:
        ordp += 1
    else:
      nn += 1
      rb *= x[1]
      if x[4]:
        rn = max(rn, x[5])
      else:
        ordn += 1
  return rows(np, nn, ordp, ordn, rp, rn, 1.0 - ra, 1.0 - rb, u, v)


def outcome_sets(apps, u, v, bset, eset):
  """the state of one atom when its applications count as present with
  their body literals in bset and no exception literal in eset (memo 5.5,
  step 5 and the procedure's step 2)"""
  ra = rb = 1.0
  np = nn = 0
  ordp = ordn = 0
  rp = rn = 0
  for hs, q, body, exc, normal, rank in apps:
    ok = True
    for j, s in body:
      if (j, s) not in bset:
        ok = False
        break
    if ok:
      for j, s in exc:
        if (j, s) in eset:
          ok = False
          break
    if not ok:
      continue
    if hs == 0:
      np += 1
      ra *= q
      if normal:
        rp = max(rp, rank)
      else:
        ordp += 1
    else:
      nn += 1
      rb *= q
      if normal:
        rn = max(rn, rank)
      else:
        ordn += 1
  return rows(np, nn, ordp, ordn, rp, rn, 1.0 - ra, 1.0 - rb, u, v)


# ------------------------------------------------------------------ the narrowing (memo 5.5)
#
# Ported from an unpublished prototype of 2026-11-02 (its options
# `--wf mutual --per-world-kind`): the
# functions wf_side_usable, side_regimes, row_side_holds, env_surely_usable,
# env_possibly_usable, wf_lfp_sure, wf_lfp_poss, is_cross_sign and
# run_narrow_stage keep their names. Literals are (atom index, POS or NEG).
# The sets: X is the set being built, L the old sure set, U the old possible
# set. An application's side reads bodies from one set and exceptions from
# another, as memo 5.5 steps 2 and 3 say.

def wf_side_usable(sign, apps, u_val, v_val, body_own, exc_own, body_opp, exc_opp):
  """whether the tables give the atom the sign, for sides without normal
  defaults: the rows reduce to b <= u < a and a <= u < b, which are monotone
  in the own side's applications and antitone in the opposing side's, so
  one selection decides."""
  ra = rb = 1.0
  np = nn = 0
  for hs, q, body, exc, _normal, _rank in apps:
    if hs == sign:
      bset, eset = body_own, exc_own
    else:
      bset, eset = body_opp, exc_opp
    ok = True
    for j, s in body:
      if (j, s) not in bset:
        ok = False
        break
    if ok:
      for j, s in exc:
        if (j, s) in eset:
          ok = False
          break
    if not ok:
      continue
    if hs == 0:
      np += 1
      ra *= q
    else:
      nn += 1
      rb *= q
  if sign == 0:
    if not np:
      return False
    a = 1.0 - ra
    return (u_val < a) if not nn else ((1.0 - rb) <= u_val < a)
  if not nn:
    return False
  b = 1.0 - rb
  return (u_val < b) if not np else ((1.0 - ra) <= u_val < b)


def side_regimes(apps_side, bmin, emax, bmax, emin, require_nonempty_min=False):
  """the regimes (present, normal, rank, least support, largest support)
  that a side can take over the selections between its certainly present
  applications (bodies in bmin, no exception in emax) and its possibly
  present ones (bodies in bmax, no exception in emin), memo 5.5 "When a
  side holds normal defaults". A selection changes the side's support, its
  kind and its rank; one regime per reachable (kind, rank) with the range
  of supports it can have."""
  s_min, s_max = [], []
  for x in apps_side:
    in_max = all(l in bmax for l in x[2]) and not any(e in emin for e in x[3])
    if not in_max:
      continue
    s_max.append(x)
    if bmin is not None and all(l in bmin for l in x[2]) and not any(e in emax for e in x[3]):
      s_min.append(x)
  regs = []
  if not s_min and not require_nonempty_min:
    regs.append((False, False, 0, 0.0, 0.0))
  if not s_max:
    return regs
  r_smin = 1.0
  min_has_ord = False
  for x in s_min:
    r_smin *= x[1]
    if not x[4]:
      min_has_ord = True
  max_ords = [x for x in s_max if not x[4]]
  if max_ords:
    r_smax = 1.0
    for x in s_max:
      r_smax *= x[1]
    if min_has_ord:
      r_ord_max = r_smin
    else:
      s_min_ids = {id(x) for x in s_min}
      r_ord_max = r_smin * max(x[1] for x in max_ords if id(x) not in s_min_ids)
    regs.append((True, False, 0, 1.0 - r_ord_max, 1.0 - r_smax))
  if not min_has_ord:
    n_max = [x for x in s_max if x[4]]
    if n_max:
      r_base = max((x[5] for x in s_min), default=None)
      ranks = sorted({x[5] for x in n_max if r_base is None or x[5] >= r_base})
      s_min_ids = {id(x) for x in s_min}
      for rk in ranks:
        r_rk_min = 1.0
        for x in n_max:
          if x[5] <= rk:
            r_rk_min *= x[1]
        if r_base is not None and rk == r_base:
          r_rk_max = r_smin
        else:
          r_rk_max = r_smin * max(x[1] for x in n_max if x[5] == rk and id(x) not in s_min_ids)
        regs.append((True, True, rk, 1.0 - r_rk_max, 1.0 - r_rk_min))
  return regs


def row_side_holds(sign, own_reg, a_own, opp_reg, b_opp, u_val, v_val):
  """whether the row selected by the two regimes gives the atom the sign,
  with the own side's support a_own and the opposing side's b_opp (the
  tables of memo 4.2 and 4.4, read for one sign)"""
  p_own, norm_own, r_own = own_reg
  p_opp, norm_opp, r_opp = opp_reg
  if not p_own:
    return False
  if not p_opp:
    return u_val < a_own
  if sign == 0:
    a, b, normp, normn, rp, rn = a_own, b_opp, norm_own, norm_opp, r_own, r_opp
    if not normp and not normn:
      return b <= u_val < a
    if normp and not normn:
      return (u_val >= b) and (v_val < a)
    if normn and not normp:
      return u_val < a
    if rp == rn or rp == 0 or rn == 0:
      return (u_val < a) and (v_val >= b)
    if rp > rn:
      return u_val < a
    return b <= u_val < a
  a, b, normp, normn, rp, rn = b_opp, a_own, norm_opp, norm_own, r_opp, r_own
  if not normp and not normn:
    return a <= u_val < b
  if normp and not normn:
    return u_val < b
  if normn and not normp:
    return (u_val >= a) and (v_val < b)
  if rp == rn or rp == 0 or rn == 0:
    return (v_val < b) and (u_val >= a)
  if rp > rn:
    return a <= u_val < b
  return u_val < b


def env_surely_usable(sign, apps, u_val, v_val, X, L, U):
  """memo 5.5 step 2: the tables give the sign for every selection, with
  the applications for the literal reading bodies from X (the sure set
  being built) and exceptions from U (the old possible set), and the
  applications against it reading bodies from U and exceptions from L (the
  old sure set)"""
  if not any(x[4] for x in apps):
    return wf_side_usable(sign, apps, u_val, v_val, X, U, U, L)
  own_apps = [x for x in apps if x[0] == sign]
  if not any(all(l in X for l in x[2]) and not any(e in U for e in x[3]) for x in own_apps):
    return False
  opp_apps = [x for x in apps if x[0] != sign]
  own_regs = side_regimes(own_apps, X, U, U, L, False)
  opp_regs = side_regimes(opp_apps, L, U, U, L, False)
  for po, no, ro, cmin_o, _cmax_o in own_regs:
    for pp, np_, rp_, _cmin_p, cmax_p in opp_regs:
      if not row_side_holds(sign, (po, no, ro), cmin_o, (pp, np_, rp_), cmax_p, u_val, v_val):
        return False
  return True


def env_possibly_usable(sign, apps, u_val, v_val, X, L, U):
  """memo 5.5 step 3: the tables give the sign for some selection, with the
  applications for the literal reading bodies from X (the possible set
  being built) and exceptions from L (the new sure set), and the
  applications against it reading bodies from L and exceptions from U (the
  old possible set)"""
  if not any(x[4] for x in apps):
    return wf_side_usable(sign, apps, u_val, v_val, X, L, L, U)
  own_apps = [x for x in apps if x[0] == sign]
  own_regs = side_regimes(own_apps, None, None, X, L, True)
  if not own_regs:
    return False
  opp_apps = [x for x in apps if x[0] != sign]
  opp_regs = side_regimes(opp_apps, L, U, U, L, False)
  for po, no, ro, _cmin_o, cmax_o in own_regs:
    for pp, np_, rp_, cmin_p, _cmax_p in opp_regs:
      if row_side_holds(sign, (po, no, ro), cmax_o, (pp, np_, rp_), cmin_p, u_val, v_val):
        return True
  return False


def wf_lfp_sure(active_nodes, ext, byatom, u, v, L, U):
  """the new sure set, built from the base literals upward (memo 5.5 step 2)"""
  X = set(ext)
  while True:
    added = False
    for i in active_nodes:
      if (i, POS) not in X and env_surely_usable(0, byatom[i], u[i], v[i], X, L, U):
        X.add((i, POS))
        added = True
      if (i, NEG) not in X and env_surely_usable(1, byatom[i], u[i], v[i], X, L, U):
        X.add((i, NEG))
        added = True
    if not added:
      return X


def wf_lfp_poss(active_nodes, ext, byatom, u, v, L, U):
  """the new possible set, built from the base literals upward (memo 5.5
  step 3); ext holds the base literals and the literals of the unresolved
  outside atoms, which stay possible"""
  X = set(ext)
  while True:
    added = False
    for i in active_nodes:
      if (i, POS) not in X and env_possibly_usable(0, byatom[i], u[i], v[i], X, L, U):
        X.add((i, POS))
        added = True
      if (i, NEG) not in X and env_possibly_usable(1, byatom[i], u[i], v[i], X, L, U):
        X.add((i, NEG))
        added = True
    if not added:
      return X


def is_cross_sign(nodes, byatom):
  """memo 5.2: the group has a cycle across signs when an application with
  its head in the group has a body literal in the group of the other sign,
  or two such applications have heads of opposite signs; exception literals
  and facts do not count"""
  members = set(nodes)
  sg = [False, False]
  for h in nodes:
    for hs, _q, body, _exc, _normal, _rank in byatom[h]:
      inside = [(j, sgn) for j, sgn in body if j in members]
      if inside:
        sg[hs] = True
        if any(sgn != hs for _j, sgn in inside):
          return True
  return sg[0] and sg[1]


def run_narrow_stage(nodes, ext_base, unres_lits, locked, byatom_stage, u, v):
  """the narrowing of memo 5.5 on one set of applications (byatom_stage):
  steps 1 to 5, repeated with the atoms fixed in conflict left out. ext_base
  holds the base literals of the outside atoms; unres_lits both literals of
  every unresolved outside atom (memo 5: possible, never sure); locked the
  fixed atoms with their states. Returns the sure set, the possible set and
  the number of rounds."""
  sweeps = 0
  while True:
    ext = set(ext_base)
    for k_i, k_st in locked.items():
      if k_st == POS:
        ext.add((k_i, POS))
      elif k_st == NEG:
        ext.add((k_i, NEG))
    active = [i for i in nodes if i not in locked]
    ext_poss = ext | unres_lits
    L = set(ext)
    U = set(ext_poss) | {(i, POS) for i in active} | {(i, NEG) for i in active}
    while True:
      sweeps += 1
      nL = wf_lfp_sure(active, ext, byatom_stage, u, v, L, U)
      nU = wf_lfp_poss(active, ext_poss, byatom_stage, u, v, nL, U)
      if nL == L and nU == U:
        break
      L, U = nL, nU
    new_conf = [i for i in active
                if (i, POS) not in L and (i, NEG) not in L
                and outcome_sets(byatom_stage[i], u[i], v[i], U, L) == CON]
    if not new_conf:
      return L, U, sweeps
    for i in new_conf:
      locked[i] = CON


def narrow_group(nodes, outside, byatom, u, v, state, unres_reading, stats):
  """the procedure of memo 5.5 for one group: the two stages when the group
  has normal defaults (memo 5.3), one otherwise; then the state of every
  atom. An atom left possible but not sure gets unres_reading: UNRES for a
  cycle across signs or a group that depends on an unresolved atom, IGN for
  a one-sign or exception-only group whose sweeps did not settle (memo 5.4)."""
  ext_base, unres_lits = set(), set()
  for j in outside:
    if state[j] == POS:
      ext_base.add((j, POS))
    elif state[j] == NEG:
      ext_base.add((j, NEG))
    elif state[j] == UNRES:
      unres_lits.add((j, POS))
      unres_lits.add((j, NEG))
  locked = {}
  has_norm = any(x[4] for i in nodes for x in byatom[i])
  if has_norm:
    byatom_ord = {i: [x for x in byatom[i] if not x[4]] for i in nodes}
    L1, U1, sw1 = run_narrow_stage(nodes, ext_base, unres_lits, locked, byatom_ord, u, v)
    for i in nodes:
      if i not in locked:
        if (i, POS) in L1:
          locked[i] = POS
        elif (i, NEG) in L1:
          locked[i] = NEG
        elif ((i, POS) not in U1) and ((i, NEG) not in U1):
          if outcome_sets(byatom_ord[i], u[i], v[i], L1, U1) == CON:
            locked[i] = CON
  else:
    sw1 = 0
  L, U, sw2 = run_narrow_stage(nodes, ext_base, unres_lits, locked, byatom, u, v)
  if sw1 + sw2 > stats[0]:
    stats[0] = sw1 + sw2
  for i in nodes:
    if i in locked:
      state[i] = locked[i]
    elif (i, POS) in L:
      state[i] = POS
    elif (i, NEG) in L:
      state[i] = NEG
    elif ((i, POS) not in U) and ((i, NEG) not in U):
      state[i] = outcome_sets(byatom[i], u[i], v[i], L, U)
    else:
      state[i] = unres_reading


SWEEP_CAP = 100000   # a safety stop for the sweeps, never reached on the record; counted in sweep_cap_hits


def world(byatom, comps, u, v, state, stats):
  """one world: the cycle groups in dependency order, each from the final
  states of the atoms outside it (memo 5, the table). A group that depends
  on an unresolved atom runs the narrowing whatever its shape (memo 5, the
  paragraph after the table). stats = [the longest sweep or round count,
  the safety stops of the sweeps]."""
  for nodes, outside, inner, cyclic in comps:
    if any(state[j] == UNRES for j in outside):
      narrow_group(nodes, outside, byatom, u, v, state, UNRES, stats)
      continue
    if not cyclic:
      i = nodes[0]
      state[i] = outcome(byatom[i], state, u[i], v[i])
      continue
    cross = is_cross_sign(nodes, byatom)
    if not cross:
      # a one-sign or exception-only group: sweeps (memo 5.1); the narrowing
      # only when a sweep repeats a state, an undecided atom then ignorance
      for i in nodes:
        state[i] = IGN
      dirty, settled, sw = nodes, False, 0
      seen = {tuple(state[i] for i in nodes)}
      while True:
        sw += 1
        changed = []
        for i in dirty:
          s = outcome(byatom[i], state, u[i], v[i])
          if s != state[i]:
            changed.append((i, s))
        if not changed:
          settled = True
          break
        nd = set()
        for i, s in changed:
          state[i] = s
          nd.update(inner[i])
        dirty = sorted(nd)
        key = tuple(state[i] for i in nodes)
        if key in seen:
          break
        if sw >= SWEEP_CAP:
          stats[1] += 1
          break
        seen.add(key)
      if sw > stats[0]:
        stats[0] = sw
      if settled:
        continue
      narrow_group(nodes, outside, byatom, u, v, state, IGN, stats)
      continue
    narrow_group(nodes, outside, byatom, u, v, state, UNRES, stats)


def hoeffding(n):
  return math.sqrt(math.log(8 / 0.05) / (2 * n)) if n else 1.0


def summary(counts, n, swap):
  c = list(counts)
  if swap:
    c[0], c[1] = c[1], c[0]
  e = hoeffding(n)
  val = [x / n for x in c[:4]]
  return {"counts": c, "value": val, "unstable": c[4] / n,
          "interval_95": [[max(0.0, p - e), min(1.0, p + e)] for p in val]}


# ------------------------------------------------------------------ the run

def run(path, samples, seed, max_ground, all_atoms):
  res = {"version": VERSION, "input": path, "converted_by": None, "interpretation": INTERPRETATION, "question": None, "variables": [],
         "constants": None, "ground_clauses": None, "atoms": None, "applications": None, "evaluated_atoms": None,
         "components": None, "samples": samples, "seed": seed, "readings": [], "answers": [], "unsupported": None,
         "provenance": {"tool": TOOL, "files": []}}
  files = res["provenance"]["files"]
  try:
    inp = read_input(path, max_ground, files)
  except Unsupported as e:
    res["unsupported"] = str(e)
    res["converted_by"] = "gk -writejson -recursive" if any(f[0] == "gk" for f in files) else None
    return res
  res["converted_by"] = inp.converted_by
  qs, qp, qargs = inp.question
  res["question"] = lit_text(qs, qp, qargs)
  res["variables"] = [a[2:] for a in inp.qvars]
  res["constants"] = len(inp.constants)
  res["ground_clauses"] = len(inp.ground)
  apps, dropped = orient(inp.ground)
  res["applications"] = len(apps)
  res["self_exception_applications"] = len(dropped)
  byhead = {}
  for x in apps:
    byhead.setdefault(x.head, []).append(x)
  insts = []   # the question's ground instances: (text, atom, binding)
  if inp.qvars:
    for tup in itertools.product(inp.constants, repeat=len(inp.qvars)):
      sub = dict(zip(inp.qvars, tup))
      key = (qp, tuple(sub.get(a, a) for a in qargs))
      if key in byhead:
        insts.append((lit_text(qs, *key), key, [untyped(t) for t in tup]))
  else:
    insts.append((lit_text(qs, qp, qargs), (qp, qargs), []))
  atoms = {x.head for x in apps} | {b for x in apps for _s, b in x.body + x.exc} | {k for _t, k, _b in insts}
  res["atoms"] = len(atoms)
  qatoms = closure([k for _t, k, _b in insts], byhead)
  rc = rank_contexts(atoms, byhead)
  why = [rc[k] for _t, k, _b in insts if k in rc]
  if why:
    res["unsupported"] = why[0]
    return res
  rel = atoms if all_atoms else qatoms   # the atoms evaluated; printed with --all-atoms
  for si, x, lit in dropped:
    if x.head in rel:
      res["readings"].append(["self exception", "statement %d: %s (exception %s)" % (si + 1, app_text(x),
                                                                                     lit_text(lit[0], *lit[1]))])
  possible = reachable(apps)
  order = sorted(rel, key=lambda k: (atom_text(*k), k[1] is None))
  idx = {k: i for i, k in enumerate(order)}
  n = len(order)
  res["evaluated_atoms"] = n
  byatom = [[] for _ in range(n)]
  for x in apps:
    if x.head in idx:
      h = idx[x.head]
      body = [(idx[a], POS if s == 0 else NEG) for s, a in x.body]
      exc = [(idx[a], POS if s == 0 else NEG) for s, a in x.exc]
      byatom[h].append((x.hsign, 1.0 - x.conf, body, exc, x.normal, x.rank))
  qidx = [idx[key] for _t, key, _b in insts]
  # An application with a body literal outside the reachable literals is
  # present in no world; it is removed before the cycle groups are formed,
  # so that it decides no dependence (memo 4.6).
  live = {(POS if sg == 0 else NEG, idx[a]) for sg, a in possible if a in idx}
  byatom = [[x for x in byatom[h] if all((sg, j) in live for j, sg in x[2])] for h in range(n)]
  deps = [sorted({j for x in byatom[h] for j, _s in x[2] + x[3]}) for h in range(n)]
  comps = build_comps(deps, n)
  res["components"] = len(comps)
  counts = [[0, 0, 0, 0, 0] for _ in insts]
  acounts = [[0, 0, 0, 0, 0] for _ in range(n)] if all_atoms else None
  state, u, v = [IGN] * n, [0.0] * n, [0.0] * n
  stats = [0, 0]
  # splitmix64 in the order of the atom texts: atom i's U and V are the
  # draws 2i+1 and 2i+2 of a world. The state advances by GOLDEN per draw,
  # so a draw is computed only where it can change a state: U for an atom
  # with an uncertain application or applications of both signs, V where a
  # normal default meets the other sign. The other draws are skipped by
  # their offset; every computed value is the one the full stream gives.
  both = [len({x[0] for x in byatom[i]}) == 2 for i in range(n)]
  needu = [(i, ((2 * i + 1) * GOLDEN) & MASK) for i in range(n) if both[i] or any(x[1] > 0 for x in byatom[i])]
  needv = [(i, ((2 * i + 2) * GOLDEN) & MASK) for i in range(n) if both[i] and any(x[4] for x in byatom[i])]
  step = (2 * n * GOLDEN) & MASK
  s = seed & MASK
  for _t in range(samples):
    for i, off in needu:
      t = (s + off) & MASK
      z = ((t ^ (t >> 30)) * 0xBF58476D1CE4E5B9) & MASK
      z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & MASK
      u[i] = ((z ^ (z >> 31)) >> 11) * TWO53
    for i, off in needv:
      t = (s + off) & MASK
      z = ((t ^ (t >> 30)) * 0xBF58476D1CE4E5B9) & MASK
      z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & MASK
      v[i] = ((z ^ (z >> 31)) >> 11) * TWO53
    s = (s + step) & MASK
    world(byatom, comps, u, v, state, stats)
    for j, qi in enumerate(qidx):
      counts[j][state[qi]] += 1
    if all_atoms:
      for i in range(n):
        acounts[i][state[i]] += 1
  res["longest_sweeps"], res["sweep_cap_hits"] = stats
  for j, (text, key, binding) in enumerate(insts):
    a = {"instance": text, "key": ["-" if qs else "+", key[0], None if key[1] is None else [untyped(t) for t in key[1]]]}
    if inp.qvars:
      a["binding"] = binding
    a.update(summary(counts[j], samples, qs == 1))
    res["answers"].append(a)
  if all_atoms:
    res["atom_values"] = [{"atom": atom_text(*order[i]), "unsupported": rc[order[i]]} if order[i] in rc else
                          dict({"atom": atom_text(*order[i])}, **summary(acounts[i], samples, False)) for i in range(n)]
  return res


def main():
  ap = argparse.ArgumentParser(description="mcref: a Monte Carlo reference for gk's recursive method")
  ap.add_argument("input")
  ap.add_argument("--samples", type=int, default=100000)
  ap.add_argument("--seed", type=int, default=1)
  ap.add_argument("--max-ground", type=int, default=200000)
  ap.add_argument("--all-atoms", action="store_true")
  a = ap.parse_args()
  if a.samples < 1:
    ap.error("--samples must be at least 1")
  print(json.dumps({"mcref": run(a.input, a.samples, a.seed, a.max_ground, a.all_atoms)}))


if __name__ == "__main__":
  main()
