"""mcref_proofs: the proofs of several statements for mcref (the option
--proofs, on in the default command).

A proof of a literal Q is a pair (L, G): L a set of statements, G a set of
single literals (the premises). L with G implies Q classically, L with G is
consistent, no statement can be left out of L and no literal out of G, and
every uncertain rule and every rule with an exception in L has Q as its head.

The general form, as in "Confidences for Commonsense Reasoning" (2021):
resolution on triples (clause, dependency list), the dependency list being
the set of statements used, with c-subsumption: (C1, L1) removes (C2, L2)
when C1 is a subset of C2 and L1 a subset of L2. A kept triple (C, L) with
Q in C is the proof (L, G) of Q with G the complements of the other
literals of C. c-subsumption removes the triples that are not minimal and
those whose statements and premises are inconsistent (a triple (C', L')
with Q not in C' and C' a subset of C). Resolution is complete for
consequence finding, so every minimal proof is a kept triple.

The statements that take part (proof_applications() in mcref.py fills
free and directed):
- free: a certain clause of several literals without an exception literal
  (a certain written-head rule without an exception is such a clause: every
  direction), and a clause of several literals without a written head,
  certain or uncertain, with or without exception literals; an uncertain
  clause enters with the negation of its source event atom, so a proof that
  uses it has the event among its premises (one event, shared by all uses);
  a proof that uses a clause with exception literals keeps them;
- directed, for its head literal only: an uncertain rule with a written head
  and a certain rule with a written head and exception literals, of several
  literals, normal defaults included (an uncertain normal default with its
  rule identity). In the saturation for its head h it is never resolved on
  h's atom, so every derived clause keeps h.
Facts do not take part; they enter as premises.

The free clauses are saturated per connected part (atoms joined by a free
clause); the directed rules of a head h are saturated on top of the parts
that their atoms touch. Only literals with at least two statements that
contain them (free clauses with the literal, directed rules with that head)
can get a proof that a single statement does not already give with fewer
requirements (an "absorbed" proof, below), so only their parts are
saturated. find_proofs() also searches the literals in `extra`: a literal
that one statement holds, whose single application does not absorb the
proofs (MCREF_B3 in mcref.py).

From a proof (L, G) of Q the application: its body is every single literal
that G and the non-goal clauses (the clauses of L without Q) imply
(requirement 1); its listed clauses are the non-goal clauses (each of
several literals; requirement 2); its exception literals those of the
rules of L (requirement 3); its identities those of the uncertain rules of
L (each counted once in a side's support). An application is absorbed, and
left out, when another application of the same literal has a body, listed
clauses, exception literals and identities that are subsets of its own:
the other is present whenever it is, with no more rules, so the support
of the side does not change.

Limits: PROOF_RESOLVENTS resolvents and PROOF_TRIPLES kept triples per
input, PROOF_APPS applications per input. When a limit is reached no
application of several statements is added, and the input is evaluated
with the single applications only; the statistics name the limit and mcref
prints it as a reading."""
import itertools

PROOF_RESOLVENTS = 3000000   # the most resolvents formed for one input
PROOF_TRIPLES = 300000       # the most triples kept at one time for one input
PROOF_APPS = 20000           # the most proofs of several statements read for one input


class ProofLimit(Exception):
  """a limit of the proof search was reached"""


def popcount(x):
  return bin(x).count("1")


class Store:
  """the kept triples (clause, deps) of one saturation, with an index by
  literal; clause a frozenset of literal numbers, deps an int bitmask"""

  def __init__(self, budget):
    self.trip = []      # (clause, deps) or None when removed
    self.bylit = {}     # literal -> list of triple numbers holding it
    self.bymin = {}     # smallest literal -> triple numbers (forward subsumption)
    self.empty = []     # triple numbers of empty clauses
    self.alive = 0
    self.budget = budget

  def subsumed(self, c, d):
    """some kept triple c-subsumes (c, d)"""
    for t in self.empty:
      e = self.trip[t]
      if e is not None and e[1] & ~d == 0:
        return True
    for l in c:
      for t in self.bymin.get(l, ()):
        e = self.trip[t]
        if e is not None and e[1] & ~d == 0 and e[0] <= c:
          return True
    return False

  def remove_subsumed(self, c, d):
    """remove the kept triples that (c, d) c-subsumes"""
    if not c:
      cands = range(len(self.trip))
    else:
      best = min(c, key=lambda l: len(self.bylit.get(l, ())))
      cands = list(self.bylit.get(best, ()))
    for t in cands:
      e = self.trip[t]
      if e is not None and d & ~e[1] == 0 and c <= e[0]:
        self.trip[t] = None
        self.alive -= 1

  def add(self, c, d):
    t = len(self.trip)
    self.trip.append((c, d))
    self.alive += 1
    if self.alive > PROOF_TRIPLES:
      raise ProofLimit("more than %d kept triples of the proof search" % PROOF_TRIPLES)
    if not c:
      self.empty.append(t)
    else:
      self.bymin.setdefault(min(c), []).append(t)
      for l in c:
        self.bylit.setdefault(l, []).append(t)
    return t

  def items(self):
    return [e for e in self.trip if e is not None]


def saturate(store, passive, frozen_atom=None, dmask=0):
  """given-clause saturation. passive: list of (clause, deps) to add.
  frozen_atom: with dmask, a triple whose deps meet dmask is never resolved
  on a literal of that atom (literal number // 2)."""
  import heapq
  heap = []
  cnt = 0
  for c, d in passive:
    heapq.heappush(heap, (popcount(d), len(c), cnt, c, d))
    cnt += 1
  budget = store.budget
  while heap:
    _p, _l, _k, c, d = heapq.heappop(heap)
    if store.subsumed(c, d):
      continue
    store.remove_subsumed(c, d)
    t = store.add(c, d)
    if not c:
      continue
    dirc = dmask and (d & dmask)
    for l in c:
      if dirc and (l >> 1) == frozen_atom:
        continue
      for t2 in list(store.bylit.get(l ^ 1, ())):
        e = store.trip[t2]
        if e is None or t2 == t:
          continue
        c2, d2 = e
        if dmask and (d2 & dmask) and (l >> 1) == frozen_atom:
          continue
        budget[0] -= 1
        if budget[0] < 0:
          raise ProofLimit("more than %d resolvents of the proof search" % PROOF_RESOLVENTS)
        r = (c - {l}) | (c2 - {l ^ 1})
        if any((x ^ 1) in r for x in r):
          continue
        d3 = d | d2
        heapq.heappush(heap, (popcount(d3), len(r), cnt, frozenset(r), d3))
        cnt += 1
  return store


def find_proofs(free, directed, nlits_atoms, noq=(), extra=()):
  """free: list of (statement index, frozenset of literal numbers);
  directed: list of (statement index, head literal number, frozenset of
  literal numbers); literal number 2*atom + sign (sign 1 negative).
  Returns (proofs, stats): proofs a list of (Q, clause, deps) with deps a
  frozenset of statement indices, every minimal proof of several
  statements of each literal Q that has at least two statements holding
  it, and of each literal in extra (a literal whose one statement does not
  absorb its proofs); and a lookup of the free triples for the
  implied literals."""
  budget = [PROOF_RESOLVENTS]
  stats = {"free_clauses": len(free), "directed_rules": len(directed), "parts": 0, "parts_saturated": 0,
           "directed_heads": 0, "triples": 0, "resolvents": 0, "limit": None}
  # statement bit numbers
  sid = {}
  for s, _c in free:
    sid.setdefault(s, len(sid))
  for s, _h, _c in directed:
    sid.setdefault(s, len(sid))
  sof = {b: s for s, b in sid.items()}
  # connected parts of the free clauses (union-find over atoms)
  par = {}

  def find(a):
    while par.get(a, a) != a:
      par[a] = par.get(par[a], par[a])
      a = par[a]
    return a

  def union(a, b):
    ra, rb = find(a), find(b)
    if ra != rb:
      par[ra] = rb

  for _s, c in free:
    ats = sorted({l >> 1 for l in c})
    for a in ats[1:]:
      union(ats[0], a)
  holders = {}
  for _s, c in free:
    for l in c:
      holders[l] = holders.get(l, 0) + 1
  dby = {}
  for s, h, c in directed:
    dby.setdefault(h, []).append((s, c))
    holders[h] = holders.get(h, 0) + 1
  cand = sorted(l for l, k in holders.items() if (k >= 2 or l in extra) and l not in noq)
  partof = {}
  for s, c in free:
    partof.setdefault(find(next(iter(c)) >> 1), []).append((s, c))
  stats["parts"] = len(partof)
  stores = {}

  def part_store(root):
    st = stores.get(root)
    if st is None:
      st = Store(budget)
      saturate(st, [(c, 1 << sid[s]) for s, c in partof.get(root, [])])
      stores[root] = st
      stats["parts_saturated"] += 1
    return st

  proofs = []
  try:
    for q in cand:
      a = q >> 1
      roots = {find(a)}
      if q not in dby:
        if find(a) not in partof:
          continue
        st = part_store(find(a))
        for c, d in st.items():
          if q in c and popcount(d) > 1:
            proofs.append((q, c, d))
        if len(proofs) > PROOF_APPS:
          raise ProofLimit("more than %d proofs of several statements" % PROOF_APPS)
        continue
      stats["directed_heads"] += 1
      for _s, c in dby[q]:
        for l in c:
          roots.add(find(l >> 1))
      st = Store(budget)
      for r in sorted(roots):
        if r in partof:
          for c, d in part_store(r).items():
            st.add(c, d)
      dmask = 0
      pas = []
      for s, c in dby[q]:
        b = 1 << sid[s]
        dmask |= b
        pas.append((c, b))
      saturate(st, pas, a, dmask)
      for c, d in st.items():
        if q in c and popcount(d) > 1:
          proofs.append((q, c, d))
      if len(proofs) > PROOF_APPS:
        raise ProofLimit("more than %d proofs of several statements" % PROOF_APPS)
  except ProofLimit as e:
    stats["limit"] = str(e)
    proofs = []
  stats["resolvents"] = PROOF_RESOLVENTS - budget[0]
  stats["triples"] = sum(s.alive for s in stores.values())

  def free_triples(atoms):
    """the kept free triples of the parts of the atoms"""
    out = []
    for r in sorted({find(x) for x in atoms}):
      if r in stores:
        out += stores[r].items()
      elif r in partof:
        out += part_store(r).items()
    return out

  out = [(q, c, frozenset(sof[b] for b in range(len(sof)) if (d >> b) & 1), d) for q, c, d in proofs]
  return out, stats, free_triples, sid
