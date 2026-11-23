#!/usr/bin/env python3
"""mcref: the reference tool of the support semantics of gk.

The default command computes the support semantics that
Doc/support_semantics.md describes (the reference definitions in its Section
11). It reads a gk input and grounds it over the input's constants
(mcref_read.py), builds the single applications of the ground statements and
the applications of the proofs of several statements (orient() here,
mcref_apps.py, mcref_proofs.py), leaves out the applications that only
support themselves (no self-support) and those whose body can never hold,
forms the groups (mcref_graph.py) and the layers, and evaluates worlds: each
group by the tables (mcref_tables.py), by sweeps, by the narrowing or by the
clause rule in a cycle, inside the exception pass (layers, removal,
restore). The report comes from exact evaluation (mcref_exact.py: one world
per cell of the world space) or from sampling (run(): N drawn worlds). The
tool calls no prover and shares no code with gk; gk runs only as `gk FILE
-writejson -recursive` to read inputs that are not JSON.

Options keep other rules of the tool for tests and comparisons: --rules 1.1
(no proofs of several statements and no layers; --cases, --proofs and
--layers then turn single parts on), --backbone fix (with --rules 1.1) and
--ranks (a candidate rule for ranks across atoms, not part of the
definition). Constants are typed: 1, 1.0 and "1" are three terms. The rows
of the tables (rows()) follow the definition, not gk's C code. README.md
describes the tool.

Usage: mcref.py INPUT [--mode auto|exact|sampling] [--max-cells N] [--samples N]
                [--seed N] [--max-ground N] [--all-atoms] [--rules 8|1.1]
                [--backbone judge|fix] [--cases] [--proofs] [--layers] [--ranks]
Output: one JSON line {"mcref": {...}}. Exit status 3 and a message on
stderr: a sweep group that did not settle, an internal error (SweepError)."""
import argparse
import itertools
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcref_read import Unsupported, atom_text, lit_text, read_input, sha256_file, untyped  # noqa: E402
import mcref_proofs  # noqa: E402
from mcref_apps import (admissible, App, app_text, application, B3, case_applications, CASE_CONTEXTS, CASE_DEPTH,
  CASE_EXC_IN_CONTEXT, CASE_EXCEPTIONS, case_proofs, CASE_SOURCES, CASE_UNCERTAIN, CASE_UNIONS, CaseLimit, CASES,
  CHECK_SUPPORT, CLAUSE_KEYS, CLAUSE_LITS, consistent, LAST_CASES, LIFT_UND, minimal_sets, neg_lit, PCACHE,
  PCACHE_LIMIT, proof_applications, RULE_TEXT, RULE_W, unions, uniq)  # noqa: E402,F401
from mcref_tables import (CON, dnf_brute, dnf_prob, IGN, NEG, outcome, outcome_sets_plain, pool, POS, row_side_holds,
  rows, side_regimes, side_regimes_p4, support, SUPPORT_CHECKS, tuple_of, UNRES, wf_side_usable)  # noqa: E402,F401
from mcref_graph import (build_comps, build_comps_part, by_components, CLAUSE_OF, closure, components, deps_of,
  is_cross_sign, lower, node_deps, rank_contexts, reachable, reachable_tuples, real_exc, RULE1, rule1_filter,
  RULE1_LAST)  # noqa: E402,F401
from mcref_texts import (BACKBONE_TEXT, CASES_TEXT, INTERPRETATION, LAYERS_TEXT, PROOFS_TEXT)  # noqa: E402,F401

VERSION = "1.3.1"   # the tool's version, printed in every output
MASK = (1 << 64) - 1
GOLDEN = 0x9E3779B97F4A7C15   # splitmix64's increment
TWO53 = 2.0 ** -53
BACKBONE = "judge"   # the variant of the backbone step when run() is not given one: "judge" or "fix"
HERE = os.path.dirname(os.path.abspath(__file__))
TOOL = {f: sha256_file(os.path.join(HERE, f)) for f in ("mcref.py", "mcref_read.py", "mcref_proofs.py", "mcref_apps.py",
                                                       "mcref_tables.py", "mcref_graph.py", "mcref_texts.py")}

# ------------------------------------------------------------------ the parts of the definition
#
# False here; main() turns PROOFS and LAYERS on for the default command (--rules 8). With all three False the
# tool computes the rules of --rules 1.1.
# PROOFS (--proofs): the proofs (L, G) of several statements (mcref_proofs.py) in place of the case proofs,
#   each with requirement 1 (its body: every single literal that G and the non-goal clauses imply) and
#   requirement 2 (its listed clauses: no one contradicted), the latter in every evaluation path through
#   clause nodes (below), with the clause rule in a cycle and the check that cannot be decided; a clause
#   without a written head takes part in the proofs also when it has exception literals, and the proofs keep
#   them.
# LAYERS (--layers): the exception pass, exceptions judged in layers on signed literals.
# RANKS (--ranks): a candidate rule for ranks across atoms, not part of the definition.
PROOFS = False
LAYERS = False
RANKS = False
LAST_PROOFS = None  # PROOFS: the statistics of the last orient()
CIRCLE_LAST = set()  # PROOFS: the clause nodes of a group whose clause rule in a cycle had no result, and the
                     # atoms that the rule left without a value, in the last evaluation pass
CIRCLE_CACHE = {}    # PROOFS: per cycle group with clause nodes, its atoms without clause nodes and their cycle groups


# ------------------------------------------------------------------ the applications of the ground statements


def orient(gclauses, cases=None, directed=None):
  """the applications of the ground clauses; source events get atoms
  ('$src_i', ()). A certain clause with a written head and no exception
  literal is the same statement as the disjunction of its literals and gives
  one application per literal. The self-exception rule: an application whose
  exception literal is one of its body literals never applies; it is not
  created, and it is returned in `dropped` as (statement index, application,
  literal). The test is made on the ground application, after the expansion
  of the exception-only variables, so an exception that matches a body
  literal by binding only its exception-only variables counts. With
  conclusions by cases on (cases, else the module's CASES), the guarded
  applications of case_applications() are added, and LAST_CASES holds their
  statistics. With PROOFS the applications of proof_applications() are added
  instead, and LAST_PROOFS holds their statistics. directed (a test setting
  of the sampling check): statement indices whose certain written-head rules
  keep their written direction."""
  global LAST_CASES
  cases = CASES if cases is None else cases
  global LAST_PROOFS
  RULE_W.clear()
  RULE_TEXT.clear()
  PCACHE.clear()
  CLAUSE_KEYS.clear()
  CLAUSE_LITS.clear()
  LAST_PROOFS = None
  if PROOFS:
    cases = False   # the proofs of several statements replace the case proofs
  src_of, rid_of = {}, {}   # PROOFS: the source event of an uncertain flat clause, the identity of an uncertain rule
  apps, nsrc, dropped = [], 0, []
  classical, units = [], set()   # for the case proofs: the classical clauses and the certain facts
  excrules = []   # for the case proofs: the certain written-head applications with exception literals
  uncrules = []   # for the case proofs: the uncertain written-head applications, with their identities
  def keep(x, si):
    same = [e for e in x.exc if e in x.body]
    if same:
      dropped.append((si, x, same[0]))
      return False
    apps.append(x)
    return True
  for gi, (si, conf, lits, blocks, head) in enumerate(gclauses):
    excs = uniq([(l[0], (l[1], l[2])) for _st, l in blocks])
    strength = {}
    for st, l in blocks:
      k = (l[0], (l[1], l[2]))
      strength[k] = max(strength.get(k, 0), st)
    crank = max(strength.values()) if strength else 0
    if len(lits) == 1:
      head = 0
    if head is not None and len(lits) > 1 and conf >= 1 and not blocks and not (directed and si in directed):
      head = None   # a certain written-head rule without exceptions: every direction
    if head is not None:   # a fact, or an uncertain rule or a default with a written head: its head only
      h = lits[head]
      if len(lits) == 1 and conf >= 1 and not blocks:
        units.add((h[0], (h[1], h[2])))
      body = uniq([(1 - l[0], (l[1], l[2])) for i, l in enumerate(lits) if i != head])
      x = application(h, body, excs, strength, conf, crank, False)
      if PROOFS and conf < 1 and (not x.normal or LIFT_UND) and len(lits) > 1:   # with LIFT_UND also a normal default
        x.rid = len(RULE_W)
        RULE_W[x.rid] = conf
        RULE_TEXT[x.rid] = "%s (%.6g)" % (app_text(x), conf)
        rid_of[gi] = x.rid
      if keep(x, si) and not x.normal and cases:
        if conf >= 1 and (x.exc or (directed and si in directed)) and CASE_EXCEPTIONS:
          excrules.append(x)   # with the test setting `directed`, a held rule is a leaf at its head too
        elif conf < 1 and CASE_UNCERTAIN:
          x.rid = len(RULE_W)
          RULE_W[x.rid] = conf
          RULE_TEXT[x.rid] = "%s (%.6g)" % (app_text(x), conf)
          uncrules.append(x)
      continue
    extra, c2, src = [], conf, None   # a flat clause: one application per literal
    if conf < 1:
      nsrc += 1
      src = ("$src_%d" % nsrc, ())
      src_of[gi] = src
      apps.append(App(src, 0, [], [], conf, False, 0, "source event", 0))
      extra, c2 = [(0, src)], 1.0
    for i, h in enumerate(lits):
      body = uniq([(1 - l[0], (l[1], l[2])) for j, l in enumerate(lits) if j != i] + extra)
      keep(application(h, body, excs, strength, c2, crank, True), si)
    if not blocks:
      classical.append((lits, src))
  LAST_CASES = None
  if cases:
    new, LAST_CASES = case_applications(classical, units, apps, excrules, uncrules)
    apps.extend(new)
  if PROOFS:
    new, LAST_PROOFS = proof_applications(gclauses, apps, src_of, rid_of, directed)
    apps.extend(new)
  return apps, dropped


# ------------------------------------------------------------------ the clause nodes and the check of a listed clause


def setup_clause_nodes(idx):
  """PROOFS: the clause nodes of a run, for the atom indices idx: CLAUSE_OF
  maps the index of each clause node to its literals (atom index, POS or
  NEG)"""
  CLAUSE_OF.clear()
  CIRCLE_CACHE.clear()
  CONCLUDED.clear()
  for k, lits in CLAUSE_LITS.items():
    if k in idx:
      CLAUSE_OF[idx[k]] = [(idx[a], POS if sg == 0 else NEG) for sg, a in lits]


CONCLUDED = set()


def setup_concluded(byatom):
  """PROOFS: the literals (atom index, POS or NEG) that some application of
  the run concludes, after the applications whose body cannot hold are
  removed (reachable()). clause_state() reads it"""
  CONCLUDED.clear()
  for h, xs in enumerate(byatom):
    for x in xs:
      CONCLUDED.add((h, POS if x[0] == 0 else NEG))


def clause_state(c, state):
  """the state of the clause node c: POS when its clause is contradicted
  (each literal has evidence for its opposite: the atom of the opposite
  sign or in conflict), UNRES when it is not decided because of an
  unresolved atom, IGN otherwise. An unresolved atom leaves the check open
  only if some application concludes the
  opposite of the clause's literal on that atom (CONCLUDED); if none does,
  that literal has no evidence against it and the clause is not
  contradicted. Example: in `t. p :- t, unless(-p,1).
  w :- t, unless(-w,1). -p :- w. d :- p. a. -a. a ; d. q :- a. q :- d.`
  the atom d is unresolved, no application concludes -d, the clause
  `a ; d` is not contradicted, q is (1, 0, 0, 0)"""
  unres = False
  for j, sg in CLAUSE_OF[c]:
    st = state[j]
    if st == CON or st == (NEG if sg == POS else POS):
      continue
    if st == UNRES:
      if (j, NEG if sg == POS else POS) not in CONCLUDED:
        return IGN
      unres = True
      continue
    return IGN
  return UNRES if unres else POS


# ------------------------------------------------------------------ the state of one atom from sets of literals


def outcome_sets(apps, u, v, bset, eset):
  """the state of one atom when its applications count as present with
  their body literals in bset and no exception literal in eset (the
  conflict step of the narrowing, and an atom with neither literal
  possible); RANKS: inside a stage of the rank rule, the staged form"""
  if RANKS:
    return staged_outcome_sets(apps, u, v, bset, eset)
  return outcome_sets_plain(apps, u, v, bset, eset)


# ------------------------------------------------------------------ the rank rule across atoms (--ranks, a candidate)
#
# A candidate rule, not part of the definition. In a narrow group with normal defaults the stages run by descending rank: the
# ordinary stage (thr None), then each positive rank r, then all ("ALL"). A side of an atom (all its present
# applications for one sign) enters a stage as a whole once it has an ordinary application or a normal default
# of rank >= r; a side whose regime is a normal default of rank 0 opposes at every positive stage and establishes
# only at "ALL". An atom settled in a stage keeps its state. Equal ranks keep no value, as without the rule.
CUR_THR = "ALL"

def qual_own(x, thr):
  if thr == "ALL": return True
  if thr is None: return not x[4]
  return (not x[4]) or x[5] >= thr

def qual_opp(x, thr):
  if thr == "ALL": return True
  if thr is None: return not x[4]
  return (not x[4]) or x[5] == 0 or x[5] >= thr

def staged_side_regimes(apps_side, bmin, emax, bmax, emin, require_nonempty_min=False, is_opp=False):
  thr = CUR_THR
  qfn = qual_opp if is_opp else qual_own
  s_min, s_max = [], []
  for x in apps_side:
    in_max = all(l in bmax for l in x[2]) and not any(e in emin for e in x[3])
    if not in_max: continue
    s_max.append(x)
    if bmin is not None and all(l in bmin for l in x[2]) and not any(e in emax for e in x[3]):
      s_min.append(x)
  has_qual_min = any(qfn(x, thr) for x in s_min)
  has_qual_max = any(qfn(x, thr) for x in s_max)
  if require_nonempty_min and not has_qual_max:
    return []
  full_regs = side_regimes(apps_side, bmin, emax, bmax, emin, False)
  regs = []
  if not has_qual_min and not require_nonempty_min:
    regs.append((False, False, 0, 0.0, 0.0))
  for present, norm, rk, lo, hi in full_regs:
    if not present: continue
    if thr == "ALL":
      regs.append((present, norm, rk, lo, hi))
    elif thr is None:
      if not norm: regs.append((present, norm, rk, lo, hi))
    elif is_opp:
      if not norm or rk == 0 or rk >= thr: regs.append((present, norm, rk, lo, hi))
    else:
      if not norm or rk >= thr: regs.append((present, norm, rk, lo, hi))
  return regs

def staged_env_surely(sign, apps, u_val, v_val, X, L, U):
  thr = CUR_THR
  if thr == "ALL" and not any(x[4] for x in apps):
    return wf_side_usable(sign, apps, u_val, v_val, X, U, U, L)
  own_apps = [x for x in apps if x[0] == sign]
  if not any(qual_own(x, thr) and all(l in X for l in x[2]) and not any(e in U for e in x[3]) for x in own_apps):
    return False
  opp_apps = [x for x in apps if x[0] != sign]
  own_regs = staged_side_regimes(own_apps, X, U, U, L, False, is_opp=False)
  opp_regs = staged_side_regimes(opp_apps, L, U, U, L, False, is_opp=True)
  for po, no, ro, cmin_o, _cmax_o in own_regs:
    for pp, np_, rp_, _cmin_p, cmax_p in opp_regs:
      if not row_side_holds(sign, (po, no, ro), cmin_o, (pp, np_, rp_), cmax_p, u_val, v_val):
        return False
  return True

def staged_env_possibly(sign, apps, u_val, v_val, X, L, U):
  thr = CUR_THR
  if thr == "ALL" and not any(x[4] for x in apps):
    return wf_side_usable(sign, apps, u_val, v_val, X, L, L, U)
  own_apps = [x for x in apps if x[0] == sign]
  own_regs = staged_side_regimes(own_apps, L, U, X, L, True, is_opp=False)
  if not own_regs: return False
  opp_apps = [x for x in apps if x[0] != sign]
  opp_regs = staged_side_regimes(opp_apps, L, U, U, L, False, is_opp=True)
  for po, no, ro, _cmin_o, cmax_o in own_regs:
    for pp, np_, rp_, cmin_p, _cmax_p in opp_regs:
      if row_side_holds(sign, (po, no, ro), cmax_o, (pp, np_, rp_), cmin_p, u_val, v_val):
        return True
  return False

def staged_outcome_sets(apps, u, v, bset, eset):
  thr = CUR_THR
  if thr == "ALL": return outcome_sets_plain(apps, u, v, bset, eset)
  present_pos = [x for x in apps if x[0] == 0 and all((j, s) in bset for j, s in x[2]) and not any((j, s) in eset for j, s in x[3])]
  present_neg = [x for x in apps if x[0] == 1 and all((j, s) in bset for j, s in x[2]) and not any((j, s) in eset for j, s in x[3])]
  keep_pos = any(qual_own(x, thr) for x in present_pos)
  keep_neg = any(qual_own(x, thr) for x in present_neg)
  filtered = [x for x in apps if (x[0] == 0 and keep_pos) or (x[0] == 1 and keep_neg)]
  return outcome_sets_plain(filtered, u, v, bset, eset)

def side_rank_narrow_group(nodes, outside, byatom, u, v, state, unres_reading, stats):
  """the side-level rank rule:
  At stage thr (None for ordinary, then descending positive ranks r > 0):
  a side (i, sign) is eligible in own_regs iff it has a present ordinary rule (at thr=None)
  or a present ordinary rule / normal default of rank >= thr (at thr > 0).
  Once eligible, the side's regime pools ALL present applications on that side.
  Rank-0 normal defaults are included in opp_regs at all normal-default stages thr > 0
  and in own_regs at the final stage thr == 'ALL'."""
  global CUR_THR
  ext_base, unres_lits = set(), set()
  for j in outside:
    if state[j] == POS: ext_base.add((j, POS))
    elif state[j] == NEG: ext_base.add((j, NEG))
    elif state[j] == UNRES:
      unres_lits.add((j, POS)); unres_lits.add((j, NEG))
  locked = {}
  stage1_ign = set()
  ranks = sorted({x[5] for i in nodes for x in byatom[i] if x[4] and x[5] > 0}, reverse=True)
  has_norm = any(x[4] for i in nodes for x in byatom[i])
  has_rank0 = any(x[4] and x[5] == 0 for i in nodes for x in byatom[i])
  sw = 0
  if ranks:
    stages = [None] + (ranks if has_rank0 else ranks[:-1])
  elif has_norm:
    stages = [None]
  else:
    stages = []
  for thr in stages:
    CUR_THR = thr
    L1, U1, s1 = run_narrow_stage(nodes, ext_base, unres_lits, locked, byatom, u, v)
    sw += s1
    for i in nodes:
      if i not in locked:
        if (i, POS) in L1: locked[i] = POS
        elif (i, NEG) in L1: locked[i] = NEG
        elif ((i, POS) not in U1) and ((i, NEG) not in U1):
          st0 = staged_outcome_sets(byatom[i], u[i], v[i], L1, U1)
          if st0 == CON:
            locked[i] = CON
          elif thr is None and st0 == IGN:
            stage1_ign.add(i)
  CUR_THR = "ALL"
  L, U, s2 = run_narrow_stage(nodes, ext_base, unres_lits, locked, byatom, u, v)
  if sw + s2 > stats[0]: stats[0] = sw + s2
  for i in nodes:
    if i in locked: state[i] = locked[i]
    elif (i, POS) in L: state[i] = POS
    elif (i, NEG) in L: state[i] = NEG
    elif ((i, POS) not in U) and ((i, NEG) not in U):
      state[i] = outcome_sets_plain(byatom[i], u[i], v[i], L, U)
    else:
      state[i] = unres_reading


# ------------------------------------------------------------------ the narrowing
#
# The new sure set and the new possible set of a group; the selections of a side are in mcref_tables.py.


def env_surely_usable(sign, apps, u_val, v_val, X, L, U):
  """the new sure set of the narrowing: the tables give the sign for every
  selection, with
  the applications for the literal reading bodies from X (the sure set
  being built) and exceptions from U (the old possible set), and the
  applications against it reading bodies from U and exceptions from L (the
  old sure set)"""
  if RANKS:   # the rank rule uses the staged form in every stage, "ALL" too
    return staged_env_surely(sign, apps, u_val, v_val, X, L, U)
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
  """the new possible set of the narrowing: the tables give the sign for
  some selection, with the
  applications for the literal reading bodies from X (the possible set
  being built) and exceptions from L (the new sure set), and the
  applications against it reading bodies from L and exceptions from U (the
  old possible set)"""
  if RANKS:   # in "ALL" too: the rank rule reads the possible set with bmin L and emax U
    return staged_env_possibly(sign, apps, u_val, v_val, X, L, U)
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
  """the new sure set, built from the base literals upward"""
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
  """the new possible set, built from the base literals upward; ext holds
  the base literals and the literals of the unresolved
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


def run_narrow_stage(nodes, ext_base, unres_lits, locked, byatom_stage, u, v):
  """the narrowing on one set of applications (byatom_stage):
  steps 1 to 5, repeated with the atoms fixed in conflict left out. ext_base
  holds the base literals of the outside atoms; unres_lits both literals of
  every unresolved outside atom (possible, never sure); locked the
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
  """the procedure for one group: the two stages when the group has normal
  defaults, one otherwise; then the state of every
  atom. An atom left possible but not sure gets unres_reading: UNRES for a
  cycle across signs or a group that depends on an unresolved atom, IGN for
  any other group that is not a sweep group (Doc/support_semantics.md, Section 11.7).
  RANKS: the side-level rank rule (side_rank_narrow_group())."""
  if RANKS:
    return side_rank_narrow_group(nodes, outside, byatom, u, v, state, unres_reading, stats)
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


ONE, SWEEP, NARROW_IGN, NARROW_UNRES = 0, 1, 2, 3   # the procedure of a cycle group


class SweepError(Exception):
  """a sweep group whose sweeps changed a state in sweep |G|+2. The sweep
  lemma (Doc/support_semantics.md, Section 12) says the states are final after at
  most |G|+1 sweeps, so this is an internal error of the tool."""

  def __init__(self, nodes, sweeps):
    Exception.__init__(self, "a sweep group did not settle")
    self.nodes, self.sweeps = nodes, sweeps


def group_kinds(comps, byatom):
  """the procedure of each cycle group (Doc/support_semantics.md, Section 11.7), decided
  once: ONE for an atom that does not depend on
  itself; SWEEP for a sweep group, which has no cycle across signs, no
  application of the group with an exception literal in the group, and no
  normal default among the applications of the group; NARROW_IGN for any
  other group without a cycle across signs; NARROW_UNRES for a cycle across
  signs. The fourth condition of a sweep group, no unresolved outside atom,
  depends on the world and is tested in world(). The complement of its own
  head on a normal default is not among an application's exceptions
  (application()), so it does not count in the second condition."""
  out = Groups()
  for nodes, outside, inner, cyclic in comps:
    if not cyclic:
      kind = ONE
    elif is_cross_sign(nodes, byatom):
      kind = NARROW_UNRES
    else:
      members = set(nodes)
      apps = [x for i in nodes for x in byatom[i]]
      exc_inside = any(j in members for x in apps for j, _s in x[3])
      normal = any(x[4] for x in apps)
      kind = NARROW_IGN if exc_inside or normal else SWEEP
    out.append((nodes, outside, inner, kind))
  return out


def sweep_group(nodes, inner, byatom, u, v, state, stats):
  """the sweeps of a sweep group: every atom starts in ignorance, and each
  sweep recomputes the atoms from the states of the previous sweep, until a
  sweep changes nothing. The sweep lemma bounds the count by |G|+2, the
  last sweep changing nothing; a change in sweep |G|+2 raises SweepError."""
  for i in nodes:
    state[i] = IGN
  dirty, sw, limit = nodes, 0, len(nodes) + 2
  while True:
    sw += 1
    changed = []
    for i in dirty:
      s = outcome(byatom[i], state, u[i], v[i])
      if s != state[i]:
        changed.append((i, s))
    if not changed:
      break
    if sw >= limit:
      raise SweepError(nodes, sw)
    nd = set()
    for i, s in changed:
      state[i] = s
      nd.update(inner[i])
    dirty = sorted(nd)
  if sw > stats[0]:
    stats[0] = sw


def eval_group(byatom, group, u, v, state, stats):
  """one cycle group from the final states of the atoms outside it
  (Doc/support_semantics.md, Section 11.7). A group that depends on an unresolved
  atom runs the narrowing whatever its shape, an undecided atom then
  unresolved."""
  nodes, outside, inner, kind = group
  if CLAUSE_OF:
    if kind == ONE and nodes[0] in CLAUSE_OF:
      state[nodes[0]] = clause_state(nodes[0], state)
      return
    cn = [i for i in nodes if i in CLAUSE_OF]
    if cn:
      circle_group(byatom, group, cn, u, v, state, stats)
      return
  if any(state[j] == UNRES for j in outside):
    narrow_group(nodes, outside, byatom, u, v, state, UNRES, stats)
  elif kind == ONE:
    i = nodes[0]
    state[i] = outcome(byatom[i], state, u[i], v[i])
  elif kind == SWEEP:
    sweep_group(nodes, inner, byatom, u, v, state, stats)
  else:
    narrow_group(nodes, outside, byatom, u, v, state, IGN if kind == NARROW_IGN else UNRES, stats)


CIRCLE_STATS = {"worlds": 0, "groups": set(), "unresolved_clause": 0}


def circle_listed_present(byatom, nodes, c, state):
  """some application of the group with the clause node c among its
  exception entries has its body usable and no other exception established
  in the states state"""
  for h in nodes:
    for x in byatom[h]:
      if (c, POS) not in x[3]:
        continue
      if any(state[j] != s for j, s in x[2]):
        continue
      members = set(nodes)
      if any(state[j] == s for j, s in x[3] if j != c and not (j in CLAUSE_OF and j in members)):
        continue
      return True
  return False


# The clause rule without a result keeps the atoms whose state is the same in every evaluation. CIRCLE_KEEP False
# (the environment CIRCLE_KEEP=0, a test setting) gives every atom of the group no value then; the default is on.
CIRCLE_KEEP = os.environ.get("CIRCLE_KEEP", "1") != "0"


def circle_group(byatom, group, cn, u, v, state, stats):
  """PROOFS: a cycle group that holds clause nodes cn: requirement 2 in a
  cycle, the clause rule. The other atoms of the group are evaluated in the cycle
  groups they form without the clause nodes, the clause nodes fixed:
  1. first with no clause node contradicted (IGN: every proof applies);
  2. the evaluation gives each clause node its state (clause_state()); a
     clause node whose listing applications are all absent in this
     evaluation for another reason (circle_listed_present(): a body
     literal not usable, or a real exception established) keeps its fixed
     state, since it does not matter there; when these states equal the
     fixed states, the result is
     taken: none contradicted, or the collected ones still contradicted
     and no new one;
  3. otherwise every newly contradicted clause node is collected, all at
     once, and fixed contradicted (POS: the proofs that list it are left
     out), and the group is evaluated again from 2;
  4. when a clause node collected earlier is no longer contradicted, or a
     clause node is unresolved (a check that cannot be decided: an atom of
     its clause unresolved and its opposite literal concluded by some
     application, clause_state()), the rule has no result in this world: a
     listed clause is contradicted only while its own proof applies. With
     CIRCLE_KEEP an atom of the group with the same state in every
     evaluation the rule made keeps it; every other atom of the group gets
     no value (UNRES). When the rule stops at a check that cannot be
     decided, one more evaluation with every such clause counted as
     contradicted comes first.
  5. after the rule, with a result or without one, every clause node of
     the group gets the check on the final states (clause_state()), so
     that an application outside the group that lists the clause reads
     that check (requirement 2), not the setting of the last round.
  Each round collects at least one clause node, so the loop ends after at
  most len(cn) + 1 evaluations. Example: in
  `p ; r. q :- p. q :- r. 0.9::-p :- q. -r.` the clause `p ; r` is
  contradicted with every proof applying, and stays contradicted when the
  proof of q that lists it is left out: -p keeps its proof
  ({`q :- p.`, `0.9::-p :- q.`}, {}), whose two clauses both contain -p,
  so it lists no clause; q is in ignorance in the worlds with the .9 rule."""
  nodes = group[0]
  key = (tuple(nodes), id(byatom))
  ent = CIRCLE_CACHE.get(key)
  if ent is None or ent[0] is not byatom:
    rest = [i for i in nodes if i not in CLAUSE_OF]
    deps = {i: sorted(node_deps(i, byatom[i])) for i in nodes}
    sub = group_kinds(build_comps_part(deps, rest), byatom) if rest else []
    ent = (byatom, rest, sub)
    if len(CIRCLE_CACHE) < CACHE_LIMIT:
      CIRCLE_CACHE[key] = ent
  _b, rest, sub = ent
  alpha = [IGN] * len(cn)
  ok = False
  hist = []   # the states of the group's atoms in every evaluation the rule makes
  for _round in range(len(cn) + 1):
    for c, b in zip(cn, alpha):
      state[c] = b
    for g in sub:
      eval_group(byatom, g, u, v, state, stats)
    hist.append([state[i] for i in rest])
    beta = [clause_state(c, state) for c in cn]
    beta = [a if not circle_listed_present(byatom, nodes, c, state) else b for c, a, b in zip(cn, alpha, beta)]
    if beta == alpha:
      ok = True
      # the rounds' settings hold only inside the rule; a reader outside the group gets the check on the
      # final states
      for c in cn:
        state[c] = clause_state(c, state)
      break
    if UNRES in beta:
      CIRCLE_STATS["unresolved_clause"] += 1
      if CIRCLE_KEEP:
        # one more evaluation, every listed clause whose check is open or contradicted counted as
        # contradicted, the others as not contradicted, so that both readings exist
        for c, b in zip(cn, beta):
          state[c] = POS if b in (POS, UNRES) else IGN
        for g in sub:
          eval_group(byatom, g, u, v, state, stats)
        hist.append([state[i] for i in rest])
      break
    if any(a == POS and b != POS for a, b in zip(alpha, beta)):
      break
    alpha = [POS if b == POS else a for a, b in zip(alpha, beta)]
  if not ok:
    CIRCLE_STATS["groups"].add(tuple(nodes))
    if CIRCLE_KEEP:
      # an atom with the same state in every evaluation keeps it; every other atom of the group has no value;
      # every clause node gets the check on these final states
      for k, i in enumerate(rest):
        seen = {h[k] for h in hist}
        if len(seen) == 1:
          state[i] = hist[0][k]
          CIRCLE_STATS["kept"] = CIRCLE_STATS.get("kept", 0) + 1
        else:
          state[i] = UNRES
          CIRCLE_LAST.add(i)
      for c in cn:
        state[c] = clause_state(c, state)
        CIRCLE_LAST.add(c)
    else:
      for i in nodes:
        state[i] = UNRES
      CIRCLE_LAST.update(nodes)


def world_groups(byatom, comps, u, v, state, stats):
  """the cycle groups in dependency order, each by eval_group(): one
  evaluation of all groups, no application held out or removed. comps holds
  the procedures of
  group_kinds(). stats = [the longest sweep or round count]."""
  CIRCLE_LAST.clear()
  for group in comps:
    eval_group(byatom, group, u, v, state, stats)


# ------------------------------------------------------------------ the backbone step and the exception pass

CACHE_LIMIT = 50000   # the most entries of a cache of split groups (Backbone, Judge); above it they are formed in each world


class Groups(list):
  """the cycle groups that group_kinds() returns, in dependency order; the
  attribute plan holds the backbone step of world() for them once world()
  has built it"""
  plan = None


class Backbone:
  """the backbone step of the variant "fix" (--backbone fix, only with
  --rules 1.1) for the applications byatom and their cycle groups comps,
  built once per run:
  strict    per atom, its applications without an exception literal that
            are not normal defaults (the backbone)
  scomps    the cycle groups of the backbone, formed from its own
            dependencies, with their procedures
  deps      the dependencies of every atom over all applications
  pure      per group of comps: every application of the group is in the
            backbone. Such a group is also a group of the backbone, with the
            same applications and procedure, so its backbone states stand
            when its outside atoms keep their backbone states.
  affected  per atom: its dependency closure holds an application outside
            the backbone, so that a kept state can differ from the state
            without the step
  cache     the groups of step 3 per (group of comps, its kept atoms)"""
  mode = "fix"

  def __init__(self, byatom, comps):
    n = len(byatom)
    self.strict = [[x for x in byatom[h] if not x[3] and not x[4]] for h in range(n)]
    sdeps = [sorted({j for x in self.strict[h] for j, _s in x[2]}) for h in range(n)]
    self.scomps = group_kinds(build_comps(sdeps, n), self.strict)
    self.deps = [sorted({j for x in byatom[h] for j, _s in x[2] + x[3]}) for h in range(n)]
    self.pure = [all(len(self.strict[i]) == len(byatom[i]) for i in nodes) for nodes, _o, _i, _k in comps]
    self.affected = [False] * n
    for gi, (nodes, outside, _inner, _kind) in enumerate(comps):
      a = not self.pure[gi] or any(self.affected[j] for j in outside)
      for i in nodes:
        self.affected[i] = a
    self.cache = {}
    self.cache_full = False
    self.st1 = [IGN] * n
    self.diff = [False] * n
    self.fixed_cycle = self.fixed_cycle_affected = False


def world_fix(bb, byatom, comps, u, v, state, stats):
  """one world with the backbone step of the variant "fix":
  1. the backbone, the applications without an exception literal that are
     not normal defaults, in its own cycle groups, by world_groups();
  2. an atom positive, negative or in conflict there keeps that state;
  3. the other atoms from all applications, by eval_group(), a kept atom
     read as a fact of its state: a group of comps without kept atoms as it
     is, a group with kept atoms split into the groups of its other atoms
     (build_comps_part(): the dependencies of the kept atoms left out).
  A group whose applications are all in the backbone and whose outside
  atoms keep their backbone states takes its backbone states without a
  second evaluation (Backbone.pure). comps holds the procedures of
  group_kinds(); stats = [the longest sweep or round count]."""
  st1, diff, aff = bb.st1, bb.diff, bb.affected
  world_groups(bb.strict, bb.scomps, u, v, st1, stats)
  bb.fixed_cycle = bb.fixed_cycle_affected = False
  for gi, group in enumerate(comps):
    nodes = group[0]
    fixed = [i for i in nodes if st1[i] < IGN]   # POS, NEG or CON
    if not fixed:
      if bb.pure[gi] and not any(diff[j] for j in group[1]):
        for i in nodes:
          state[i] = st1[i]
          diff[i] = False
      else:
        eval_group(byatom, group, u, v, state, stats)
        for i in nodes:
          diff[i] = state[i] != st1[i]
      continue
    if group[3] != ONE:
      bb.fixed_cycle = True
      if any(aff[i] for i in fixed):
        bb.fixed_cycle_affected = True
    for i in fixed:
      state[i] = st1[i]
      diff[i] = False
    if len(fixed) == len(nodes):
      continue
    key = (gi, tuple(fixed))
    sub = bb.cache.get(key)
    if sub is None:
      sub = group_kinds(build_comps_part(bb.deps, [i for i in nodes if st1[i] >= IGN]), byatom)
      if len(bb.cache) < CACHE_LIMIT:
        bb.cache[key] = sub
      else:
        bb.cache_full = True
    for h in sub:
      eval_group(byatom, h, u, v, state, stats)
      for i in h[0]:
        diff[i] = state[i] != st1[i]

RESTORE = True   # variant judge: the restore step repeated; False: without it (a test setting)


class Judge:
  """the backbone step of the variant "judge" (the backbone judges
  exceptions only, with the restore step repeated) for the applications
  byatom and their cycle groups comps, built once per run:
  strict    per atom, its applications without an exception literal that
            are not normal defaults (the backbone)
  scomps    the cycle groups of the backbone that pass 1 evaluates: those of
            the atoms that some exception literal depends on through the
            backbone, with their procedures, in dependency order
  excapps   the applications with an exception literal, as (head, index in
            byatom[head], exception literals), in the order of the heads
  gidx      per atom, the index of its group in comps
  cache     the groups of pass 2 per (group of comps, the applications
            removed from it), with their applications
  st1       the states of pass 1 in the last world
  removed0  the applications that pass 1 removed in the last world, as
            (head, index)
  removed   those still removed at its end (after the restore step)
  rounds    the restore rounds of the last world"""
  mode = "judge"

  def __init__(self, byatom, comps):
    n = len(byatom)
    self.strict = [[x for x in byatom[h] if not real_exc(x) and not x[4]] for h in range(n)]
    sdeps = deps_of(self.strict, n)
    self.excapps = [(h, k, real_exc(x)) for h in range(n) for k, x in enumerate(byatom[h]) if real_exc(x)]
    need, todo = set(), [e for _h, _k, exc in self.excapps for e, _s in exc]
    while todo:
      a = todo.pop()
      if a not in need:
        need.add(a)
        todo += sdeps[a]
    # an atom of a group of the backbone is in `need` exactly when every atom of the group is
    self.scomps = [g for g in group_kinds(build_comps(sdeps, n), self.strict) if g[0][0] in need]
    self.gidx = [0] * n
    for gi, (nodes, _o, _i, _k) in enumerate(comps):
      for i in nodes:
        self.gidx[i] = gi
    self.cache = {}
    self.cache_full = False
    self.st1 = [IGN] * n
    self.removed0 = self.removed = []
    self.rounds = 0

  def split(self, byatom, group, rm):
    """the groups of pass 2 for a group of comps without the applications
    rm: the applications of its atoms that remain, and the cycle groups that
    they form, in dependency order (build_comps_part()). The dependencies of
    a removed application are left out of the graph."""
    nodes = group[0]
    drop = set(rm)
    by2 = {i: [x for k, x in enumerate(byatom[i]) if (i, k) not in drop] for i in nodes}
    deps2 = {i: sorted(node_deps(i, by2[i])) for i in nodes}
    return by2, group_kinds(build_comps_part(deps2, nodes), by2)


# ------------------------------------------------------------------ the blocked-rule repair
#
# In every evaluation of the exception pass, the applications held out or removed count as absent in the whole
# preparation: on the available applications no self-support and the rule for a body that can never hold are applied
# again, the literals some remaining application concludes are noted again (CONCLUDED, the undecided clause
# check), and the groups are formed again from the remaining applications. The layers stay as computed once from
# all applications. One entry of a cache per set of absent applications. BLOCKED_REPAIR False (the environment
# BLOCKED_REPAIR=0, a test setting) turns this off; the default is on.
BLOCKED_REPAIR = os.environ.get("BLOCKED_REPAIR", "1") != "0"
REPAIR_LOG = {}       # per set of absent applications (a tuple of (head index, index)): the applications that the
                      # repair leaves out beyond them, as (head index, index); filled while REPAIR_LOGGING is on
REPAIR_LOGGING = False
REPAIR_STATS = {"preparations": 0, "evaluations": 0}


def prepare_available(byatom, absent):
  """the preparation for one evaluation of the exception pass: the applications not in absent, no self-support and the rule
  for a body that can never hold applied again on them, the concluded literals, the groups. Returns (the remaining
  applications per atom, their groups, the concluded literals, the left-out applications beyond absent as (h, k))"""
  n = len(byatom)
  drop = set(absent)
  keep = [[k for k in range(len(byatom[h])) if (h, k) not in drop] for h in range(n)]
  if RULE1:
    cache, k2 = {}, []
    for h in range(n):
      row = []
      for k in keep[h]:
        x = byatom[h][k]
        if x[2]:
          lit = (h, POS if x[0] == 0 else NEG)
          if lit not in cache:
            cache[lit] = reachable_tuples([[byatom[g][j] for j in keep[g] if not (g == h and (byatom[g][j][0] == 0) == (lit[1] == POS))]
                                           for g in range(n)])
          if any(b not in cache[lit] for b in x[2]):
            continue
        row.append(k)
      k2.append(row)
    keep = k2
  poss = reachable_tuples([[byatom[h][k] for k in keep[h]] for h in range(n)])
  keep = [[k for k in keep[h] if all(b in poss for b in byatom[h][k][2])] for h in range(n)]
  avail = [[byatom[h][k] for k in keep[h]] for h in range(n)]
  left = sorted((h, k) for h in range(n) for k in range(len(byatom[h])) if (h, k) not in drop and k not in keep[h])
  concl = {(h, POS if x[0] == 0 else NEG) for h, xs in enumerate(avail) for x in xs}
  comps = group_kinds(build_comps(deps_of(avail, n), n), avail)
  return avail, comps, concl, left


def judge_pass(bb, byatom, comps, removed, u, v, state, stats):
  """all atoms from the applications that are not in removed, by
  eval_group(). With BLOCKED_REPAIR (the default) the applications in
  removed (held out or removed) are absent from the whole preparation
  (prepare_available()). Without it a group of comps without removed
  applications is evaluated as it is, and a group with removed applications
  is split into the groups that its remaining applications form
  (Judge.split())."""
  global CONCLUDED
  CIRCLE_LAST.clear()
  if BLOCKED_REPAIR and removed:
    key = tuple(removed)
    rc = getattr(bb, "rcache", None)
    if rc is None:
      rc = bb.rcache = {}
    ent = rc.get(key)
    if ent is None:
      ent = prepare_available(byatom, removed)
      REPAIR_STATS["preparations"] += 1
      if len(rc) < CACHE_LIMIT:
        rc[key] = ent
    REPAIR_STATS["evaluations"] += 1
    avail, comps2, concl, left = ent
    if REPAIR_LOGGING and left:
      REPAIR_LOG[key] = left
    saved = CONCLUDED
    CONCLUDED = concl
    try:
      for group in comps2:
        eval_group(avail, group, u, v, state, stats)
    finally:
      CONCLUDED = saved
    return
  bygroup = {}
  for h, k in removed:
    bygroup.setdefault(bb.gidx[h], []).append((h, k))
  for gi, group in enumerate(comps):
    rm = bygroup.get(gi)
    if rm is None:
      eval_group(byatom, group, u, v, state, stats)
      continue
    key = (gi, tuple(rm))
    sub = bb.cache.get(key)
    if sub is None:
      sub = bb.split(byatom, group, rm)
      if len(bb.cache) < CACHE_LIMIT:
        bb.cache[key] = sub
      else:
        bb.cache_full = True
    by2, groups2 = sub
    for g in groups2:
      eval_group(by2, g, u, v, state, stats)


def world_judge(bb, byatom, comps, u, v, state, stats):
  """one world with the backbone step of the variant "judge" (the restore
  step repeated), without layers:
  1. pass 1: the backbone, the applications without an exception literal
     that are not normal defaults, alone, by world_groups() (the groups
     that no exception literal depends on are left out: they decide
     nothing here);
  2. every application with an exception literal that pass 1 establishes
     (the atom positive for a positive literal, negative for a negative
     one) is removed in this world, once;
  3. all atoms from the applications that are not removed, by judge_pass();
  4. the restore step: every removed application none of whose exception
     literals established in pass 1 is usable in that result is restored,
     and step 3 is repeated, until no application is restored. A restored
     application is never removed again, so the rounds are at most as many
     as the removed applications. No state of pass 1 is kept.
  With no application removed, the world is one evaluation by
  world_groups(). RESTORE False leaves out step 4 (a test setting)."""
  removed = []
  if bb.excapps:
    st1 = bb.st1
    world_groups(bb.strict, bb.scomps, u, v, st1, stats)
    removed = [(h, k) for h, k, exc in bb.excapps if any(st1[e] == s for e, s in exc)]
  bb.removed0 = removed
  bb.rounds = 0
  if not removed:
    bb.removed = removed
    world_groups(byatom, comps, u, v, state, stats)
    return
  st1 = bb.st1
  while True:
    judge_pass(bb, byatom, comps, removed, u, v, state, stats)
    if not RESTORE:
      break
    keep = [(h, k) for h, k in removed if any(st1[e] == s and state[e] == s for e, s in real_exc(byatom[h][k]))]
    if len(keep) == len(removed):
      break
    removed = keep
    bb.rounds += 1
  bb.removed = removed


def compute_layers(byatom):
  """LAYERS: the layer of every application: an application without
  an exception literal has layer 0 (the own complement of a normal default
  is no exception literal here, and neither is a clause node); one with
  exception literals has 1 + the highest layer of its exception literals.
  The layer of a literal, an atom with a sign, is the highest layer of the
  applications that conclude it, raised to the layer of every body literal
  of those applications and (PROOFS) of the opposite of every literal of
  their listed clauses, whose evidence decides requirement 2. Every
  direction of a certain clause is an application, so the written
  direction is not used. Exceptions in a cycle get the top layer 2n + 1."""
  n = len(byatom)
  top = 2 * n + 1
  sig = [[0 if not real_exc(x) else 1 for x in byatom[h]] for h in range(n)]
  reads = []   # per application, the literals that raise its head literal's layer
  for h in range(n):
    row = []
    for x in byatom[h]:
      r = list(x[2])
      for e, _es in x[3]:
        if e in CLAUSE_OF:
          r += [(j, NEG if sg == POS else POS) for j, sg in CLAUSE_OF[e]]
      row.append(r)
    reads.append(row)
  for _round in range(top + 1):
    lit = {}
    for h in range(n):
      for k, x in enumerate(byatom[h]):
        key = (h, POS if x[0] == 0 else NEG)
        lit[key] = max(lit.get(key, 0), sig[h][k])
    for _inner in range(2 * n + 1):
      changed = False
      for h in range(n):
        for k, x in enumerate(byatom[h]):
          key = (h, POS if x[0] == 0 else NEG)
          for b in reads[h][k]:
            if lit.get(b, 0) > lit.get(key, 0):
              lit[key] = lit[b]
              changed = True
      if not changed:
        break
    changed = False
    for h in range(n):
      for k, x in enumerate(byatom[h]):
        ex = real_exc(x)
        if ex:
          req = min(top, 1 + max(lit.get(e, 0) for e in ex))
          if req != sig[h][k]:
            sig[h][k] = req
            changed = True
    if not changed:
      break
  return sig


def world_layers(bb, byatom, comps, u, v, state, stats):
  """LAYERS: one world of the exception pass, exceptions judged in layers:
  1. for s = 1, 2, ...: evaluate with the applications of layer s and above
     held out (and those removed before), by judge_pass(); remove every
     application of layer s with an exception literal established there;
  2. evaluate all applications that are not removed;
  3. restore every removed application none of whose exception literals
     established at its removal is established in the result; repeat 2
     until nothing is restored.
  With one layer of exceptions this is world_judge() except that the
  normal defaults (layer 0) take part in step 1."""
  sig, top = bb.sigma, bb.max_s
  removed, why = [], {}
  if top > 0:
    st_cur = bb.st1
    for lev in range(1, top + 1):
      hold = removed + bb.by_level_ge[lev]
      for i in range(len(st_cur)):
        st_cur[i] = IGN
      judge_pass(bb, byatom, comps, sorted(set(hold)), u, v, st_cur, stats)
      for h, k in bb.by_level[lev]:
        est = [(e, sg) for e, sg in real_exc(byatom[h][k]) if st_cur[e] == sg]
        if est:
          removed.append((h, k))
          why[(h, k)] = est
  bb.removed0 = list(removed)
  bb.rounds = 0
  if not removed:
    bb.removed = removed
    world_groups(byatom, comps, u, v, state, stats)
    return
  removed = sorted(removed)
  while True:
    judge_pass(bb, byatom, comps, removed, u, v, state, stats)
    keep = [(h, k) for h, k in removed if any(state[e] == sg for e, sg in why[(h, k)])]
    if len(keep) == len(removed):
      break
    removed = keep
    bb.rounds += 1
  bb.removed = removed


def make_plan(byatom, comps, mode):
  """the backbone step of the variant mode ("judge" or "fix") for byatom
  and comps, stored on comps (a Groups list) for world()"""
  bb = Judge(byatom, comps) if mode == "judge" else Backbone(byatom, comps)
  bb.layers = LAYERS and mode == "judge"
  if bb.layers:
    bb.sigma = compute_layers(byatom)
    bb.max_s = max((x for row in bb.sigma for x in row), default=0)
    bb.by_level = {lev: [] for lev in range(bb.max_s + 2)}
    for h, row in enumerate(bb.sigma):
      for k, lev in enumerate(row):
        if lev > 0:
          bb.by_level[lev].append((h, k))
    bb.by_level_ge = {lev: sorted(hk for l2 in range(lev, bb.max_s + 1) for hk in bb.by_level[l2])
                      for lev in range(1, bb.max_s + 2)}
  if isinstance(comps, Groups):
    comps.plan = bb
  return bb


def world(byatom, comps, u, v, state, stats):
  """one world with the backbone step: the variant of the plan stored on
  comps (make_plan(), called by run()), else the variant BACKBONE.
  comps holds the procedures of group_kinds(); stats = [the longest sweep
  or round count]."""
  bb = getattr(comps, "plan", None)
  if bb is None:
    bb = make_plan(byatom, comps, BACKBONE)
  if bb.mode == "judge":
    if bb.layers:
      world_layers(bb, byatom, comps, u, v, state, stats)
    else:
      world_judge(bb, byatom, comps, u, v, state, stats)
  else:
    world_fix(bb, byatom, comps, u, v, state, stats)


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

def run(path, samples, seed, max_ground, all_atoms, backbone=None, cases=None):
  mode = BACKBONE if backbone is None else backbone
  if mode not in BACKBONE_TEXT:
    raise ValueError("backbone variant %r: expected judge or fix" % mode)
  cases = CASES if cases is None else cases
  interp = dict(INTERPRETATION)
  interp["exception pass"] = LAYERS_TEXT if LAYERS else BACKBONE_TEXT[mode]
  if cases and not PROOFS:
    interp["conclusions by cases"] = CASES_TEXT
    interp["not represented"] = ("a classical consequence that needs several input statements at once, except "
                                 "the conclusions by cases")
  if PROOFS:
    interp["proofs of several statements"] = PROOFS_TEXT
    interp["not represented"] = ("nothing within the limits of the proof search; a limit is printed as a "
                                 "reading")
  res = {"version": VERSION, "input": path, "converted_by": None, "interpretation": interp, "question": None, "variables": [],
         "constants": None, "ground_clauses": None, "atoms": None, "applications": None, "evaluated_atoms": None,
         "components": None, "samples": samples, "seed": seed, "readings": [], "answers": [], "backbone": None,
         "cases": None, "unsupported": None,
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
  if (PROOFS or LAYERS or RANKS) and mode != "judge":
    raise ValueError("--proofs, --layers and --ranks need --backbone judge")
  apps, dropped = orient(inp.ground, cases)
  cstats = LAST_CASES if cases and not PROOFS else None
  pstats = LAST_PROOFS if PROOFS else None
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
  if PROOFS:
    atoms |= {k for x in apps if x.cls for k in x.cls}
    atoms |= {a for k in CLAUSE_LITS for _s, a in CLAUSE_LITS[k]}
  res["atoms"] = len(atoms)
  qatoms = closure([k for _t, k, _b in insts], byhead)
  rc = rank_contexts(atoms, byhead)
  why = [rc[k] for _t, k, _b in insts if k in rc]
  if why:
    res["unsupported"] = why[0]
    return res
  rel = atoms if all_atoms else qatoms   # the atoms evaluated; printed with --all-atoms
  if pstats is not None:
    mine = [app_text(x) for x in apps if x.kind == "proof" and x.head in qatoms]
    res["proofs"] = {"applications": mine, "applications_of_input": len(pstats["applications"]),
                     "proofs": pstats.get("proofs", 0), "absorbed": pstats.get("absorbed", 0),
                     "free_clauses": pstats["free_clauses"], "directed_rules": pstats["directed_rules"],
                     "parts_saturated": pstats["parts_saturated"], "triples": pstats["triples"],
                     "resolvents": pstats["resolvents"], "limit": pstats["limit"],
                     "normal_ranks_differ": pstats.get("normal_ranks_differ", 0),
                     "normal_uncertain_left_out": pstats.get("normal_uncertain_left_out", 0),
                     "free_with_exceptions": pstats.get("free_with_exceptions", 0)}
    if pstats["limit"]:
      res["readings"].append(["proofs", "LIMIT: the proofs of several statements are incomplete (%s); the input was "
                              "evaluated with the single applications only" % pstats["limit"]])
      res["proofs_incomplete"] = pstats["limit"]
    elif mine:
      res["readings"].append(["proofs", "proofs of several statements gave the applications %s" % "; ".join(mine)])
    if pstats.get("normal_ranks_differ"):
      res["readings"].append(["proofs", "%d proofs with normal defaults of different ranks count as normal defaults "
                              "of the smallest of their ranks" % pstats["normal_ranks_differ"]])
    if pstats.get("normal_uncertain_left_out"):
      res["readings"].append(["proofs", "%d uncertain normal defaults take no part in proofs of several statements (no "
                              "identity to count them once); their single applications only" % pstats["normal_uncertain_left_out"]])
  if cases and cstats is not None:
    mine = [app_text(x) for x in apps if x.kind == "case proof" and x.head in qatoms]
    res["cases"] = {"applications": mine, "applications_of_input": len(cstats["applications"]),
                    "literals_with_splits": cstats["literals_with_splits"], "contexts": cstats["contexts"],
                    "unions": cstats["unions"], "limit": cstats["limit"],
                    "exception_leaves": cstats["exception_leaves"],
                    "applications_with_exceptions_of_input": cstats["applications_with_exceptions"],
                    "rule_leaves": cstats["rule_leaves"],
                    "applications_with_rules_of_input": cstats["applications_with_rules"]}
    if cstats["limit"]:
      res["readings"].append(["cases", "the input was evaluated without conclusions by cases: %s" % cstats["limit"]])
    elif mine:
      res["readings"].append(["cases", "proofs by cases from the classical clauses gave the applications %s"
                              % "; ".join(mine)])
  for si, x, lit in dropped:
    if x.head in rel:
      res["readings"].append(["self exception", "statement %d: %s (exception %s)" % (si + 1, app_text(x),
                                                                                     lit_text(lit[0], *lit[1]))])
  apps = rule1_filter(apps)   # no self-support
  if RULE1_LAST:
    res["left_out_by_no_self_support"] = list(RULE1_LAST)
  possible = reachable(apps)
  order = sorted(rel, key=lambda k: (atom_text(*k), k[1] is None))
  idx = {k: i for i, k in enumerate(order)}
  n = len(order)
  res["evaluated_atoms"] = n
  setup_clause_nodes(idx)
  byatom = [[] for _ in range(n)]
  appof = [[] for _ in range(n)]   # beside byatom: the application of each entry, for the readings
  part4 = any(x.ids for x in apps)
  for x in apps:
    if x.head in idx:
      h = idx[x.head]
      byatom[h].append(tuple_of(x, idx, part4))
      appof[h].append(x)
  qidx = [idx[key] for _t, key, _b in insts]
  # An application with a body literal outside the reachable literals is
  # present in no world; it is removed before the cycle groups are formed,
  # so that it decides no dependence.
  live = {(POS if sg == 0 else NEG, idx[a]) for sg, a in possible if a in idx}
  appof = [[a for a, x in zip(appof[h], byatom[h]) if all((sg, j) in live for j, sg in x[2])] for h in range(n)]
  byatom = [[x for x in byatom[h] if all((sg, j) in live for j, sg in x[2])] for h in range(n)]
  setup_concluded(byatom)
  deps = deps_of(byatom, n)
  comps = group_kinds(build_comps(deps, n), byatom)
  res["components"] = len(comps)
  counts = [[0, 0, 0, 0, 0] for _ in insts]
  acounts = [[0, 0, 0, 0, 0] for _ in range(n)] if all_atoms else None
  state, u, v = [IGN] * n, [0.0] * n, [0.0] * n
  stats = [0]
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
  # the backbone step (world()). Variant "fix": how often it keeps the
  # state of an atom whose dependency closure holds an application outside
  # the backbone (watched, the question's closure only), and how often it
  # keeps an atom of a cycle group of the whole program. Variant "judge":
  # how often it removes an application with its head in the question's
  # closure, how often the head is in a cycle group of the whole program,
  # and how often pass 2 leaves the atom of a removing exception literal in
  # another state than the literal's (the application stays removed).
  bb = make_plan(byatom, comps, mode)
  qset = set(qatoms)
  watched = [i for i in range(n) if order[i] in qset and (mode == "judge" or bb.affected[i])]
  wset = set(watched)
  wcount = [0] * n
  w_fixing = w_cycle = w_cycle_aff = 0
  rcount, reopen, w_reopen = {}, {}, 0
  restc, w_restoring, w_round, w_multi, max_rounds, w_rest_usable = {}, 0, 0, 0, 0, 0
  cyc = [False] * n
  for nodes, _o, _i, kind in comps:
    for i in nodes:
      cyc[i] = kind != ONE
  circle_worlds, circle_q = 0, [0] * len(qidx)
  CIRCLE_STATS["groups"] = set()
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
    try:
      world(byatom, comps, u, v, state, stats)
      if CIRCLE_LAST:
        circle_worlds += 1
        for j, qi in enumerate(qidx):
          if qi in CIRCLE_LAST:
            circle_q[j] += 1
    except SweepError as e:
      e.args = ("mcref %s: internal error: the sweep group {%s} of %s changed a state in sweep %d; the sweep "
                "lemma of Doc/support_semantics.md, Section 12, says that sweep %d changes nothing"
                % (VERSION, ", ".join(atom_text(*order[i]) for i in e.nodes), path, e.sweeps, len(e.nodes) + 2),)
      raise
    for j, qi in enumerate(qidx):
      counts[j][state[qi]] += 1
    if all_atoms:
      for i in range(n):
        acounts[i][state[i]] += 1
    if mode == "judge":
      if bb.removed0:
        if bb.rounds:
          w_round += 1
          w_multi += bb.rounds > 1
          if bb.rounds > max_rounds:
            max_rounds = bb.rounds
        fin = set(bb.removed)
        st1 = bb.st1
        hit = hcyc = hre = hrest = hru = False
        for h, k in bb.removed0:
          if h not in wset:
            continue
          exc = real_exc(byatom[h][k])
          if (h, k) in fin:
            rcount[(h, k)] = rcount.get((h, k), 0) + 1
            hit = True
            hcyc = hcyc or cyc[h]
            for e, sg in exc:
              if st1[e] == sg and state[e] != sg:
                reopen[e] = reopen.get(e, 0) + 1
                hre = True
          else:
            restc[(h, k)] = restc.get((h, k), 0) + 1
            hrest = True
            hru = hru or any(st1[e] == sg and state[e] == sg for e, sg in exc)
        w_fixing += hit
        w_cycle += hcyc
        w_reopen += hre
        w_restoring += hrest
        w_rest_usable += hru
      continue
    st1, hit = bb.st1, False
    for i in watched:
      if st1[i] < IGN:
        wcount[i] += 1
        hit = True
    w_fixing += hit
    w_cycle += bb.fixed_cycle
    w_cycle_aff += bb.fixed_cycle_affected
  res["longest_sweeps"] = stats[0]
  if CLAUSE_OF:
    res["clause_rule_in_circle"] = {"worlds": circle_worlds, "question_worlds": circle_q,
                                    "groups": [[atom_text(*order[i]) for i in g] for g in sorted(CIRCLE_STATS["groups"])]}
    if circle_worlds:
      res["readings"].append(["clause rule in a circle", "in %d of %d worlds the clause rule in a cycle had no "
                              "result: a listed clause of the group is contradicted only while its own proof "
                              "applies, or a check cannot be decided; there the atoms of the group that change "
                              "between its evaluations have no value: %s"
                              % (circle_worlds, samples, "; ".join("{%s}" % ", ".join(atom_text(*order[i]) for i in g
                                                                                        if i not in CLAUSE_OF)
                                                                   for g in sorted(CIRCLE_STATS["groups"])))])
  if mode == "judge":
    rem = [(app_text(appof[h][k]), rcount[(h, k)]) for h, k in sorted(rcount)]
    rst = [(app_text(appof[h][k]), restc[(h, k)]) for h, k in sorted(restc)]
    reo = [(atom_text(*order[e]), reopen[e]) for e in sorted(reopen)]
    res["backbone"] = {"variant": "judge", "restore": RESTORE,
                       "removed": [{"application": t, "worlds": k} for t, k in rem],
                       "worlds_removing": w_fixing, "worlds_cycle_group": w_cycle,
                       "restored": [{"application": t, "worlds": k} for t, k in rst], "worlds_restoring": w_restoring,
                       "restored_exception_usable_at_end": w_rest_usable,
                       "restore_rounds_max": max_rounds, "worlds_with_restore_rounds": w_round,
                       "worlds_with_more_than_one_round": w_multi,
                       "reopened": [{"atom": t, "worlds": k} for t, k in reo], "worlds_reopened": w_reopen,
                       "pass2_group_sets": len(bb.cache), "pass2_cache_full": bb.cache_full}
    if rem:
      res["readings"].append(["backbone", "an exception literal of the application was usable, and the "
                              "exception pass removed it: %s"
                              % ", ".join("%s (in %d of %d worlds)" % (t, k, samples) for t, k in rem)])
    if rst:
      res["readings"].append(["backbone", "a removed application was restored, its exception not usable "
                              "in the result without it: %s"
                              % ", ".join("%s (in %d of %d worlds)" % (t, k, samples) for t, k in rst)])
    if reo:
      res["readings"].append(["backbone", "the evaluation after the removal left the atom of a removing "
                              "exception literal in another state: %s; the application stays removed"
                              % ", ".join("%s (in %d of %d worlds)" % (t, k, samples) for t, k in reo)])
  else:
    kept = [(atom_text(*order[i]), wcount[i]) for i in watched if wcount[i]]
    res["backbone"] = {"variant": "fix", "kept": [{"atom": t, "worlds": k} for t, k in kept], "worlds_keeping": w_fixing,
                       "worlds_cycle_group": w_cycle, "worlds_cycle_group_affected": w_cycle_aff,
                       "step3_group_sets": len(bb.cache), "step3_cache_full": bb.cache_full}
    if kept:
      res["readings"].append(["backbone", "the applications without an exception literal kept the state of %s"
                              % ", ".join("%s (in %d of %d worlds)" % (t, k, samples) for t, k in kept)])
  for j, (text, key, binding) in enumerate(insts):
    a = {"instance": text, "key": ["-" if qs else "+", key[0], None if key[1] is None else [untyped(t) for t in key[1]]]}
    if inp.qvars:
      a["binding"] = binding
    a.update(summary(counts[j], samples, qs == 1))
    res["answers"].append(a)
  if all_atoms:
    res["atom_values"] = [{"atom": atom_text(*order[i]), "unsupported": rc[order[i]]} if order[i] in rc else
                          dict({"atom": atom_text(*order[i])}, **summary(acounts[i], samples, False)) for i in range(n)
                          if i not in CLAUSE_OF]
  return res


def main():
  """the command. With --rules 8 (the default) it computes the definition: proofs of several statements, layers,
  the backbone variant judge. --mode auto (the default) uses exact evaluation when the cells are at most
  --max-cells (mcref_exact.py), sampling above it; --mode exact and --mode sampling force one method. The output
  names the method ("mode"), the cells or the worlds, and the error bound. --rules 1.1 leaves out the proofs of
  several statements and the layers; --cases, --proofs and --layers then turn single parts on."""
  ap = argparse.ArgumentParser(description="mcref: the reference tool of the support semantics "
                                           "(Doc/support_semantics.md), by exact evaluation or by sampling")
  ap.add_argument("input")
  ap.add_argument("--mode", choices=["auto", "exact", "sampling"], default="auto",
                  help="auto (the default): exact evaluation when the cells are at most --max-cells, sampling "
                       "above it; exact: exact evaluation only; sampling: sampling only")
  ap.add_argument("--max-cells", type=int, default=300000, help="the cell limit of exact evaluation (300000)")
  ap.add_argument("--samples", type=int, default=100000, help="the number of sampled worlds (100000)")
  ap.add_argument("--seed", type=int, default=1, help="the seed of the random numbers (1)")
  ap.add_argument("--max-ground", type=int, default=200000, help="the limit of the grounding work (200000)")
  ap.add_argument("--all-atoms", action="store_true", help="also report every ground atom")
  ap.add_argument("--backbone", choices=sorted(BACKBONE_TEXT), default=BACKBONE,
                  help="the variant of the exception pass with --rules 1.1: judge (the default: the applications "
                       "without exception literals decide which exceptions apply, and a removed application comes "
                       "back when its exceptions are no longer usable) or fix (those applications also keep the "
                       "states they establish)")
  ap.add_argument("--rules", choices=["8", "1.1"], default="8",
                  help="8 (the default): the support semantics of Doc/support_semantics.md; 1.1: the rules of mcref "
                       "1.1, without proofs of several statements and layers, where --cases, --proofs and --layers "
                       "turn single parts on")
  ap.add_argument("--cases", action="store_true", default=CASES,
                  help="with --rules 1.1: conclusions by cases from the classical clauses")
  ap.add_argument("--proofs", action="store_true", help="with --rules 1.1: proofs of several statements; on with --rules 8")
  ap.add_argument("--layers", action="store_true", help="with --rules 1.1: the exception pass in layers; on with --rules 8")
  ap.add_argument("--ranks", action="store_true", help="a candidate rule for ranks across atoms, not part of the definition")
  a = ap.parse_args()
  global PROOFS, LAYERS, RANKS
  if a.rules == "8":
    PROOFS, LAYERS = True, True
  else:
    PROOFS, LAYERS = a.proofs, a.layers
  RANKS = a.ranks
  if a.samples < 1:
    ap.error("--samples must be at least 1")
  res, why = None, None
  if a.mode in ("auto", "exact"):
    import mcref_exact as E
    M = E.mcref   # the module that mcref_exact imported (this file run as __main__ is another copy)
    M.PROOFS, M.LAYERS, M.RANKS, M.CASES, M.BACKBONE = PROOFS, LAYERS, RANKS, a.cases, a.backbone
    try:
      ex = E.run(a.input, max_cells=a.max_cells, all_atoms=a.all_atoms, max_ground=a.max_ground)
    except SweepError as e:
      sys.stderr.write(e.args[0] + "\n")
      sys.exit(3)
    if ex.get("too_many_cells") and a.mode == "auto":
      why = ex["too_many_cells"]
    else:
      res = ex
      res["mode"] = "exact"
      res["rules"] = a.rules
      res["error_bound"] = 0.0
      res["error_bound_text"] = "exact up to the rounding of floating-point numbers"
  if res is None:
    try:
      res = run(a.input, a.samples, a.seed, a.max_ground, a.all_atoms, a.backbone, a.cases)
    except SweepError as e:
      sys.stderr.write(e.args[0] + "\n")
      sys.exit(3)
    res["mode"] = "sampling"
    res["rules"] = a.rules
    res["worlds"] = a.samples
    res["error_bound"] = hoeffding(a.samples)
    res["error_bound_text"] = ("Hoeffding's inequality with a union bound: 95 per cent for the four shares of one "
                               "answer together")
    if why:
      res["exact_not_used"] = why
  print(json.dumps({"mcref": res}))


if __name__ == "__main__":
  main()
