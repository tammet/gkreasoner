"""mcref_graph: the passes of mcref over the applications before any world, and the cycle groups. The
dependency closure and the rank-context check; the reachable literals; no self-support (rule1_filter());
the strongly connected components and the cycle groups (build_comps(), build_comps_part()); the clause nodes of
the listed clauses (CLAUSE_OF)."""
from mcref_apps import CLAUSE_LITS, app_text
from mcref_read import atom_text, lit_text
from mcref_tables import NEG, POS


CLAUSE_OF = {}      # PROOFS: per clause node index of the run, its literals as (atom index, POS or NEG)


# ------------------------------------------------------------------ static passes before sampling

def closure(starts, byhead):
  """the atoms the start atoms depend on, through bodies and exceptions"""
  seen, todo = set(), list(starts)
  while todo:
    a = todo.pop()
    if a in seen:
      continue
    seen.add(a)
    if a in CLAUSE_LITS:
      todo += [b for _s, b in CLAUSE_LITS[a] if b not in seen]
    for x in byhead.get(a, []):
      todo += [b for _s, b in x.body + x.exc if b not in seen]
      if x.cls:
        todo += [k for k in x.cls if k not in seen]
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
  """rank contexts are not covered. A default of positive rank k (the largest
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
  exceptions and opposition ignored: a least fixpoint over the
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



# ------------------------------------------------------------------ no self-support
#
# A rule whose body can hold only when its head already holds is ignored. RULE1 False turns the rule off (a test
# setting).
RULE1 = True
RULE1_LAST = []   # the left-out applications of the last call whose body literals are all reachable, as texts


def rule1_filter(apps):
  """an application with head L is left out when one of its body literals cannot be derived without the
  applications that have head L. "Derived" is the test of reachable(): exceptions and opposition are not looked at.
  It works on applications, so the spelling of a statement does not matter (`d :- d.` and `d ; -d.` lose the same
  applications). Made once, before the removal of the applications whose body can never hold."""
  del RULE1_LAST[:]
  if not RULE1:
    return apps
  allr = reachable(apps)
  cache, keep = {}, []
  for x in apps:
    if x.body:
      lit = (x.hsign, x.head)
      if lit not in cache:
        cache[lit] = reachable([y for y in apps if (y.hsign, y.head) != lit])
      if any(b not in cache[lit] for b in x.body):
        if all(b in allr for b in x.body):
          RULE1_LAST.append(app_text(x))
        continue
    keep.append(x)
  return keep

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


def node_deps(i, apps_i):
  """the atoms that atom i reads: the body and exception literals of its
  applications; for a clause node, the atoms of its clause"""
  d = {j for x in apps_i for j, _s in x[2] + x[3]}
  if i in CLAUSE_OF:
    d.update(j for j, _s in CLAUSE_OF[i])
  return d


def deps_of(byatom, n):
  return [sorted(node_deps(h, byatom[h])) for h in range(n)]


def real_exc(x):
  """the exception literals of the tuple x without its clause nodes"""
  if not CLAUSE_OF:
    return x[3]
  return [e for e in x[3] if e[0] not in CLAUSE_OF]


def build_comps(deps, n):
  """the cycle groups in dependency order: (atoms, the outside
  atoms the group depends on, the readers of each atom inside the group,
  whether the group has a cycle). group_kinds() adds the procedure."""
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


def is_cross_sign(nodes, byatom):
  """the group has a cycle across signs when an application with
  its head in the group has a body literal in the group of the other sign,
  or two such applications have heads of opposite signs; exception literals
  and facts do not count"""
  members = set(nodes)
  sg = [False, False]
  for h in nodes:
    for x in byatom[h]:
      hs, body = x[0], x[2]
      inside = [(j, sgn) for j, sgn in body if j in members]
      if inside:
        sg[hs] = True
        if any(sgn != hs for _j, sgn in inside):
          return True
  return sg[0] and sg[1]


def build_comps_part(deps, part):
  """the cycle groups of the atoms `part` alone, in dependency order, as
  build_comps() gives them for the graph restricted to these atoms: the
  dependencies on atoms outside `part` are left out of the graph and
  become outside atoms of the groups. deps holds the dependencies of every
  atom."""
  loc = {i: k for k, i in enumerate(part)}
  ldeps = [sorted({loc[j] for j in deps[i] if j in loc}) for i in part]
  comps = []
  for lnodes in components(ldeps, len(part)):
    nodes = sorted(part[k] for k in lnodes)
    members = set(nodes)
    outside = sorted({j for i in nodes for j in deps[i] if j not in members})
    inner = {i: [] for i in nodes}
    for h in nodes:
      for j in deps[h]:
        if j in members:
          inner[j].append(h)
    comps.append((nodes, outside, inner, len(nodes) > 1 or nodes[0] in deps[nodes[0]]))
  return comps


def reachable_tuples(byatom):
  """reachable() on the applications of byatom (tuples): the literals (atom index, POS or NEG) that some chain of
  applications derives from the applications without a body, exceptions and opposition ignored"""
  possible, waiting, need, todo = set(), {}, {}, []
  for h, xs in enumerate(byatom):
    for k, x in enumerate(xs):
      need[(h, k)] = len(x[2])
      for lit in x[2]:
        waiting.setdefault(lit, []).append((h, k))
      if not x[2]:
        todo.append((h, k))
  while todo:
    h, k = todo.pop()
    lit = (h, POS if byatom[h][k][0] == 0 else NEG)
    if lit in possible:
      continue
    possible.add(lit)
    for hk in waiting.get(lit, []):
      need[hk] -= 1
      if need[hk] == 0:
        todo.append(hk)
  return possible
