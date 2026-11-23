"""mcref_apps: the applications of mcref. App and the single applications of a ground statement
(application(), app_text()); the conclusions by cases (--cases, case_applications()); the applications of the
proofs of several statements (proof_applications(), with the search of mcref_proofs.py). mcref.py's orient()
calls them. The rule identities (RULE_W, RULE_TEXT) and the listed clauses (CLAUSE_KEYS, CLAUSE_LITS) of the
last orient() are here."""
import os

import mcref_proofs
from mcref_read import lit_text


# Rules of the definition with a switch in the environment; each is on, and 0 turns it off (a test setting):
# LIFT_UND: an uncertain rule with a written head and a body literal has a rule identity also when it is a
#   normal default, and an uncertain normal default takes part in the proofs of its own head with that
#   identity, counted once;
# MCREF_B3: the proofs of a literal are also searched when its one statement is a clause without a written
#   head whose single application towards it is a normal default (that single application does not absorb the
#   ordinary proof);
# MCREF_B2 (two choices of constants give two ground statements) is in mcref_read.py.
LIFT_UND = os.environ.get("LIFT_UND", "1") != "0"
B3 = os.environ.get("MCREF_B3", "1") != "0"
CLAUSE_KEYS = {}    # PROOFS: per listed clause (a frozenset of literals), its clause node atom ("$clause_k", ())
CLAUSE_LITS = {}    # PROOFS: per clause node atom, the literals of its clause



# ------------------------------------------------------------------ applications

class App:
  """one application. rid: the identity of an uncertain rule with a
  written head (a rule of the proofs of several statements, or a leaf of a
  proof by cases); ids: for the application of a proof, the identities of
  the uncertain rules it uses"""
  __slots__ = ("head", "hsign", "body", "exc", "conf", "normal", "rank", "kind", "crank", "rid", "ids", "cls")

  def __init__(self, head, hsign, body, exc, conf, normal, rank, kind, crank):
    self.head, self.hsign, self.body, self.exc = head, hsign, body, exc
    self.conf, self.normal, self.rank, self.kind, self.crank = conf, normal, rank, kind, crank
    self.rid = None
    self.ids = None
    self.cls = None   # PROOFS: the clause node atoms of the listed clauses (requirement 2)


def uniq(xs):
  out = []
  for x in xs:
    if x not in out:
      out.append(x)
  return out


def application(h, body, excs, strength, conf, crank, flat):
  """one application with head literal h. The complement of the head among
  the exceptions marks a normal default: it is not tested for presence, and
  its strength is the rank. The other exceptions decide presence."""
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
  if x.ids:
    t += " [rules: %s]" % "; ".join(RULE_TEXT.get(r, "#%d" % r) for r in sorted(x.ids))
  if x.cls:
    t += " [clauses: %s]" % "; ".join(" ; ".join(lit_text(s, *a) for s, a in sorted(CLAUSE_LITS[k], key=repr))
                                       for k in x.cls)
  return t


# ------------------------------------------------------------------ conclusions by cases (--cases)

CASES = False                # conclusions by cases when orient() is not told; --cases sets it
CASE_CONTEXTS = 200000       # the most contexts of the case proofs of one input
CASE_UNIONS = 2000000        # the most unions of branch requirement sets of one input
CASE_DEPTH = 200             # the most hypotheses of one context
CASE_SOURCES = True          # uncertain disjunctions take part with their source events (False: a test setting)
CASE_EXCEPTIONS = True       # certain rules with exception literals as leaves (False: a test setting)
CASE_EXC_IN_CONTEXT = True   # such a leaf also in a context that holds its exception literal (False: a test setting)
CASE_UNCERTAIN = True        # uncertain written-head rules as leaves (False: a test setting)
RULE_W = {}                  # the confidence of each rule identity of the last orient()
RULE_TEXT = {}               # the text of each rule identity
PCACHE = {}                  # the probabilities of support formulas, for the identities of RULE_W
PCACHE_LIMIT = 200000
CHECK_SUPPORT = False        # a test setting: compare every support formula with a sum over all assignments
LAST_CASES = None            # the statistics of the last orient() with case proofs


class CaseLimit(Exception):
  """the case proofs of an input passed CASE_CONTEXTS, CASE_UNIONS or
  CASE_DEPTH; the input is then evaluated without them"""


def neg_lit(l):
  return (1 - l[0], l[1])


def consistent(g):
  return not any((1 - s, a) in g for s, a in g)


# In a requirement set of the case proofs, a kept exception literal (s, a)
# is the element (s + 2, a), and the identity r of an uncertain rule used
# is the element (4, r), beside the requirement literals (s, a)
# with s 0 or 1; so minimal_sets() and unions() handle all alike (a set is
# smaller when every part is), and consistent() reads the requirement
# literals only.

def admissible(g):
  """a requirement set that can give an application: its requirement
  literals are consistent, and no kept exception literal is one of them (an
  application whose exception literal is its own body literal never
  applies: the self-exception rule)"""
  return consistent(g) and not any(s in (2, 3) and (s - 2, a) in g for s, a in g)


def minimal_sets(sets):
  """the inclusion-minimal sets among sets, smallest first"""
  out = []
  for g in sorted(set(sets), key=lambda x: (len(x), sorted(map(repr, x)))):
    if not any(x <= g for x in out):
      out.append(g)
  return out


def unions(options, e, budget):
  """the minimal consistent unions of one requirement set from each of
  options (the branches of a split), with the source event literal e of
  the split clause added when it has one"""
  acc = [frozenset([e]) if e else frozenset()]
  for opt in options:
    if not opt:
      return []
    budget[1] -= len(acc) * len(opt)
    if budget[1] < 0:
      raise CaseLimit("more than %d unions of case requirements" % CASE_UNIONS)
    acc = minimal_sets(g for g in (a | b for a in acc for b in opt) if admissible(g))
  return acc


def case_proofs(L, leaves, csplits, asplits, cls, budget):
  """the minimal requirement sets of the case proofs of the literal L with
  no hypothesis left: f(H) below, for H empty. A context H is a consistent
  set of hypothetical case literals. In H:
  - L itself as a hypothesis needs nothing;
  - a clause of L (leaves: its body literals, its source event and its
    exception literals) needs its body literals that are not hypotheses,
    its source event, and keeps its exception literals;
  - a split (a clause of csplits with no literal decided in H, or an atom
    of asplits not in H) needs the union of one requirement set of each
    branch H + {l}, and the source event of the split clause.
  A set that holds L, both signs of an atom, or a requirement literal that
  is also a kept exception literal is dropped (admissible())."""
  memo = {}

  def f(h):
    r = memo.get(h)
    if r is not None:
      return r
    budget[0] -= 1
    if budget[0] < 0:
      raise CaseLimit("more than %d contexts of case proofs" % CASE_CONTEXTS)
    if len(h) > CASE_DEPTH:
      raise CaseLimit("a context of more than %d case hypotheses" % CASE_DEPTH)
    if L in h:
      r = [frozenset()]
    else:
      cands = []
      for body, e, x in leaves:
        if x and not CASE_EXC_IN_CONTEXT and any((s - 2, a) in h for s, a in x):
          continue
        g = frozenset(b for b in body if b not in h) | x
        cands.append(g | {e} if e else g)
      for k in csplits:
        c, e = cls[k]
        if any(l in h or neg_lit(l) in h for l in c):
          continue
        cands += unions([f(h | {l}) for l in sorted(c, key=repr)], e, budget)
      for a in asplits:
        if (0, a) in h or (1, a) in h:
          continue
        cands += unions([f(h | {(0, a)}), f(h | {(1, a)})], None, budget)
      r = minimal_sets(g for g in cands if L not in g and admissible(g))
    memo[h] = r
    return r

  return f(frozenset())


def case_applications(classical, units, apps, excrules=(), uncrules=()):
  """the guarded applications of the conclusions by cases (guarded case
  proofs), for orient(). classical holds the ground clauses
  without exception literals of at least two literals, certain ones with
  source None and uncertain flat ones with their source event atom; units
  the literals of the certain facts without exception literals; excrules
  the certain written-head applications with exception literals that are not
  normal defaults; uncrules the uncertain written-head applications that are
  not normal defaults, with their identities.

  A proof of a literal L under case hypotheses H keeps the requirements G:
  the literals it uses as premises that are not hypotheses of its branch,
  and the source event of every uncertain clause it uses. A finished proof
  (H empty) gives the certain application L <- G. Only the inclusion-
  minimal sets are kept; a set that holds L or both signs of an atom is
  dropped; a set that is the body of an existing certain application of L
  with the same exception literals adds nothing.

  An application of excrules is a leaf of the proofs
  of its head literal only, with its body literals and its exception
  literals; it is no clause to split on. The proof keeps the exception
  literals of every such leaf it uses, and a finished proof gives L <- G
  with those exception literals. Example: `q :- p, unless(e). q :- -p.`
  For q, B = {p, -p}; the split on p has the branches p (the first rule,
  keeping e) and -p (the second); q gets `q <- [unless e]`.

  An application of uncrules is a leaf of the proofs of its head literal
  only, like those of excrules, and the proof keeps its identity. A finished proof gives L <- G
  with the kept exception literals and the set of identities used (ids); its
  confidence is the product of their confidences, for the output only: the
  support of a side is computed by pool(), which counts each identity once.
  Example: `0.8::q :- p. 0.8::q :- -p.` gives `q <-` with the identities of
  both rules, and q is (.64, 0, 0, .36).

  The method (computed per literal): a premise that
  is not a hypothesis always enters G, so the leaves of a minimal proof of
  L use one clause containing L each, and a hypothesis matters only where
  it is a body literal of such a clause (the set B of L). A split whose
  branch literal lies outside B and L is replaced, without a larger G, by
  the proof of that branch alone. So the splits of L are the clauses whose
  literals all lie in B or are L, and the atoms that B holds with both
  signs. A literal without such a split gets nothing new, and neither does
  a certain fact. Example: `p ; r. q :- p. q :- r.` For q, B = {p, r}; the
  clause `p ; r` splits into the branches p and r; in each, a clause of q
  has its body literal as a hypothesis; G is empty, and q gets `q <-`.

  Returns the new applications and the statistics; above CASE_CONTEXTS,
  CASE_UNIONS or CASE_DEPTH no application is returned and the statistics
  name the limit."""
  cls, seen = [], set()
  for lits, src in classical:
    if src is not None and not CASE_SOURCES:
      continue
    c = frozenset((l[0], (l[1], l[2])) for l in lits)
    e = None if src is None else (0, src)
    if not consistent(c) or (c, e) in seen:
      continue
    seen.add((c, e))
    cls.append((c, e))
  byl = {}
  for k, (c, _e) in enumerate(cls):
    for l in c:
      byl.setdefault(l, []).append(k)
  known = {(x.hsign, x.head, frozenset(x.body), frozenset(x.exc), frozenset() if x.rid is None else frozenset([x.rid]))
           for x in apps if (x.conf == 1 or x.rid is not None) and not x.normal}
  exl = {}   # per head literal, the leaves of its rules with exception literals
  for x in excrules:
    exl.setdefault((x.hsign, x.head), []).append(
      (frozenset(x.body), None, frozenset((s + 2, a) for s, a in x.exc)))
  for x in uncrules:   # the leaves of the uncertain written-head rules, with their identities
    exl.setdefault((x.hsign, x.head), []).append(
      (frozenset(x.body), None, frozenset((s + 2, a) for s, a in x.exc) | {(4, x.rid)}))
  budget = [CASE_CONTEXTS, CASE_UNIONS]
  stats = {"literals_with_splits": 0, "contexts": 0, "unions": 0, "applications": [], "limit": None,
           "exception_leaves": len(excrules), "applications_with_exceptions": 0,
           "rule_leaves": len(uncrules), "applications_with_rules": 0}
  new = []
  try:
    for L in sorted(set(byl) | set(exl), key=repr):
      if L in units:
        continue
      own = byl.get(L, [])
      B = set()
      for k in own:
        B.update(neg_lit(l) for l in cls[k][0] if l != L)
      for body, _e, _x in exl.get(L, ()):
        B.update(body)
      allowed = B | {L}
      cand = set()
      for x in allowed:
        cand.update(byl.get(x, ()))
      csplits = sorted(k for k in cand if cls[k][0] <= allowed)
      asplits = sorted({a for s, a in B if (1 - s, a) in B}, key=repr)
      if not csplits and not asplits:
        continue
      stats["literals_with_splits"] += 1
      leaves = [(frozenset(neg_lit(l) for l in cls[k][0] if l != L), cls[k][1], frozenset()) for k in own]
      leaves += exl.get(L, [])
      for g in case_proofs(L, leaves, csplits, asplits, cls, budget):
        body = frozenset(b for b in g if b[0] < 2)
        exc = frozenset((s - 2, a) for s, a in g if s in (2, 3))
        ids = frozenset(a for s, a in g if s == 4)
        key = (L[0], L[1], body, exc, ids)
        if key in known:
          continue
        known.add(key)
        conf = 1.0
        for r in sorted(ids):
          conf *= RULE_W[r]
        x = App(L[1], L[0], sorted(body, key=repr), sorted(exc, key=repr), conf, False, 0, "case proof", 0)
        if ids:
          x.ids = ids
          stats["applications_with_rules"] += 1
        new.append(x)
        if exc:
          stats["applications_with_exceptions"] += 1
  except CaseLimit as e:
    stats["limit"] = str(e)
    new = []
  stats["contexts"] = CASE_CONTEXTS - budget[0]
  stats["unions"] = CASE_UNIONS - budget[1]
  stats["applications"] = [app_text(x) for x in new]
  stats["rules"] = {str(r): RULE_TEXT[r] for r in sorted(RULE_W)}
  return new, stats


# ------------------------------------------------------------------ proofs of several statements, pairs (L, G) (--proofs)

def proof_applications(gclauses, apps, src_of, rid_of, directed=None):
  """the applications of the proofs of several statements (mcref_proofs.py),
  for orient() with PROOFS. A proof (L, G) of Q gives the application Q <- B
  with B every single literal that G and the non-goal clauses of L imply
  (requirement 1), the non-goal clauses of L as its listed clauses (cls,
  requirement 2), the exception literals of the rules of L (requirement 3)
  and the identities of the uncertain rules of L (ids). An application that
  another application of Q absorbs (body, listed clauses, exception literals
  and identities all subsets) is left out. Returns the new applications and
  the statistics. A clause without a written head takes part in the proofs
  also when it has exception
  literals, as a free clause (with its source event when it is uncertain);
  a proof that uses it, as a goal clause or as a non-goal clause, gets its
  exception literals (requirement 3). They stay ordinary exception literals,
  also one that is the complement of the proof's goal: such a clause has no
  head, so it is no normal default."""
  num, lits_of = {}, []

  def ln(l):
    a = l[1]
    k = num.get(a)
    if k is None:
      k = num[a] = len(lits_of)
      lits_of.append(a)
    return 2 * k + l[0]

  def lt(n):
    return (n & 1, lits_of[n >> 1])

  free, drs, meta, stclause = [], [], {}, {}
  free_exc = {}   # per free clause without a written head, its exception literals
  normal_out, ranks_differ = [0], 0
  for si, (_stmt, conf, lits, blocks, head) in enumerate(gclauses):   # si: the ground clause's position
    if len(lits) < 2:
      continue
    c = frozenset((l[0], (l[1], l[2])) for l in lits)
    if not consistent(c):
      continue
    excs = uniq([(l[0], (l[1], l[2])) for _st, l in blocks])
    stclause[si] = c
    if not blocks and conf >= 1 and (head is None or not (directed and si in directed)):
      free.append((si, frozenset(ln(l) for l in c)))
      continue
    if head is None:
      # without a written head: a free clause, with or without exception literals; uncertain: with its source event
      free.append((si, frozenset(ln(l) for l in c) | ({ln((1, src_of[si]))} if conf < 1 else frozenset())))
      if blocks:
        free_exc[si] = excs
      continue
    h = lits[head]
    hl = (h[0], (h[1], h[2]))
    comp = (1 - hl[0], hl[1])
    if comp in excs:
      # a normal default takes part in the proofs of its own head, as a rule with an exception; the proof
      # counts as a normal default of its rank (the marker's). An uncertain one takes part with its rule
      # identity, counted once (LIFT_UND); with LIFT_UND off it keeps its single application only, and the
      # count is printed. A proof with normal defaults of different ranks counts as a normal default of the
      # smallest of their ranks; such proofs are counted
      if conf < 1 and not LIFT_UND:
        normal_out[0] += 1
        continue
      nrank = max(st for st, l in blocks if (l[0], (l[1], l[2])) == comp)
      rest = [e for e in excs if e != comp]
      if any(e in [(1 - l[0], (l[1], l[2])) for i, l in enumerate(lits) if i != head] for e in rest):
        continue   # the self-exception rule: never applies
      drs.append((si, ln(hl), frozenset(ln(l) for l in c)))
      meta[si] = (rest, rid_of.get(si) if conf < 1 else None, conf, nrank)   # with LIFT_UND: its identity, counted once
      continue
    if any(e in [(1 - l[0], (l[1], l[2])) for i, l in enumerate(lits) if i != head] for e in excs):
      continue   # the self-exception rule: never applies
    drs.append((si, ln(hl), frozenset(ln(l) for l in c)))
    meta[si] = (excs, rid_of.get(si), conf, None)
  noq = {ln((sg, a)) for a in list(num) if str(a[0]).startswith("$src") for sg in (0, 1)}   # a source event is no goal
  # MCREF_B3: a literal L of a clause without a written head whose exception
  # literals hold the opposite of L. The single application towards L is a normal default and absorbs no ordinary
  # proof, so the proofs of L are searched also when this clause is the only statement that holds L.
  extra = set()
  if B3:
    for si, excs in free_exc.items():
      for l in stclause[si]:
        if (1 - l[0], l[1]) in excs:
          extra.add(ln(l))
  proofs, stats, free_triples, _sid = mcref_proofs.find_proofs(free, drs, len(lits_of), noq, extra)
  stats["proofs"] = len(proofs)
  stats["applications"] = []
  stats["absorbed"] = 0
  stats["normal_uncertain_left_out"] = normal_out[0]
  stats["normal_ranks_differ"] = 0
  stats["free_with_exceptions"] = len(free_exc)
  if stats["limit"] or not proofs:
    return [], stats
  freec = dict((si, c) for si, c in free)
  # the absorbers: the single applications of the input that carry their uncertainty in a body
  # literal or an identity; a normal default with its rank (it absorbs only a proof that counts as a
  # normal default of the same rank)
  have = {}
  for x in apps:
    if x.conf < 1 and x.rid is None:
      continue
    have.setdefault((x.hsign, x.head), []).append(
      (frozenset(x.body), frozenset(x.exc), frozenset(), frozenset() if x.rid is None else frozenset([x.rid]),
       (True, x.rank) if x.normal else (False, 0)))
  cands = {}
  for q, c, deps, dmask in proofs:
    Q = lt(q)
    others = c - {q}
    G = frozenset(lt(l ^ 1) for l in others)
    goal = [si for si in deps if (si in freec and q in freec[si]) or si in meta]
    non = [si for si in deps if si not in goal]
    body = set(G)
    if non:
      nmask = 0
      bit = _sid
      for si in non:
        nmask |= 1 << bit[si]
      atoms = {l >> 1 for si in non for l in freec[si]}
      bad = False
      for c2, d2 in free_triples(atoms):
        if d2 & ~nmask:
          continue
        rest = c2 - others
        if len(rest) == 1:
          m = next(iter(rest))
          if m == q or m == q ^ 1:
            bad = True
            break
          body.add(lt(m))
        elif not rest:
          bad = True
          break
      if bad:
        continue
    exc, ids, conf = set(), set(), 1.0
    nranks = set()
    for si in deps:
      if si in free_exc:
        exc.update(free_exc[si])   # the exceptions of every clause without a written head it uses
    for si in goal:
      if si in meta:
        excs, rid, cf, nrank = meta[si]
        exc.update(excs)
        if nrank is not None:
          nranks.add(nrank)
        if rid is not None:
          ids.add(rid)
          conf *= cf
    if len(nranks) > 1:
      ranks_differ += 1   # built, with the smallest rank
    nk = (True, min(nranks)) if nranks else (False, 0)
    if any(e in body for e in exc):
      continue   # the self-exception rule: an exception literal that is its own requirement never applies
    cls = frozenset(frozenset(l for l in stclause[si]) for si in non)
    key = (frozenset(body), frozenset(exc), cls, frozenset(ids), nk)
    cands.setdefault((Q[0], Q[1]), {})[key] = (conf, sorted(deps))
  stats["normal_ranks_differ"] = ranks_differ
  new = []
  for (hs, hd), keys in sorted(cands.items(), key=repr):
    old = have.get((hs, hd), [])
    order = sorted(keys, key=lambda k: (len(k[0]) + len(k[1]) + len(k[2]) + len(k[3]), repr(k)))
    kept = []
    for k in order:
      b, e, cl, ids, nk = k
      # a proof without a normal default absorbs any proof; one that counts as a normal default only a
      # proof of its own rank
      if any(b2 <= b and e2 <= e and c2 <= cl and i2 <= ids and (not nk2[0] or nk2 == nk)
             for b2, e2, c2, i2, nk2 in old + kept):
        stats["absorbed"] += 1
        continue
      kept.append(k)
      conf, _deps = keys[k]
      x = App(hd, hs, sorted(b, key=repr), sorted(e, key=repr), conf, nk[0], nk[1], "proof", 0)
      if ids:
        x.ids = frozenset(ids)
      if cl:
        ks = []
        for c3 in sorted(cl, key=lambda z: sorted(map(repr, z))):
          key3 = CLAUSE_KEYS.get(c3)
          if key3 is None:
            key3 = CLAUSE_KEYS[c3] = ("$clause_%d" % (len(CLAUSE_KEYS) + 1), ())
            CLAUSE_LITS[key3] = sorted(c3, key=repr)
          ks.append(key3)
        x.cls = ks
      new.append(x)
  stats["applications"] = [app_text(x) for x in new]
  return new, stats
