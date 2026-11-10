#!/usr/bin/env python3
"""Independent enumeration of the small probabilistic normal programs of
part O4: the files problog*.pl and constrained.lp of the case folders.
Usage, from the part folder: python3 enumerate.py */problog*.pl c6_locality/constrained.lp

For each program: enumerate the switch choices (probabilistic facts), and for
each choice compute
  - the stable models of the resulting ground normal program (brute force over
    interpretations, checked against the Gelfond-Lifschitz reduct),
  - the well-founded model (alternating fixpoint).
From these, report for the query:
  credal lower/upper   sum over choices with >= 1 stable model of P(w)*[q in all / some models]
  equal allocation     each choice's mass split equally among its stable models (smProbLog style)
  inconsistent mass    total P(w) of choices with no stable model
  well-founded shares  P(true), P(false), P(undefined)
  problog (stratified) when every choice has exactly one stable model, P(q) = sum P(w)[q in it]

Syntax accepted: `p::atom.` probabilistic facts; `head :- b1, \\+b2, ...` rules;
`atom.` facts; `:- b1, b2.` constraints; `query(atom).`; `%` comments.
Atoms are strings like `flies(t)`; no variables.
"""
import itertools, re, sys, os


def parse(path):
  facts, rules, cons, queries = {}, [], [], []
  text = open(path).read()
  for raw in text.splitlines():
    line = raw.split('%')[0].strip()
    if not line:
      continue
    assert line.endswith('.'), line
    line = line[:-1].strip()
    m = re.match(r'^([0-9.]+)::(.+)$', line)
    if m:
      facts[m.group(2).strip()] = float(m.group(1))
      continue
    m = re.match(r'^query\((.+)\)$', line)
    if m:
      queries.append(m.group(1).strip())
      continue
    if line.startswith(':-'):
      body = [b.strip() for b in split_body(line[2:])]
      cons.append(body)
      continue
    if ':-' in line:
      head, body = line.split(':-', 1)
      rules.append((head.strip(), [b.strip() for b in split_body(body)]))
    else:
      rules.append((line.strip(), []))
  return facts, rules, cons, queries


def split_body(s):
  out, depth, cur = [], 0, ''
  for ch in s:
    if ch == '(':
      depth += 1
    elif ch == ')':
      depth -= 1
    if ch == ',' and depth == 0:
      out.append(cur); cur = ''
    else:
      cur += ch
  if cur.strip():
    out.append(cur)
  return out


def lit(b):
  b = b.strip()
  if b.startswith('\\+'):
    return (False, b[2:].strip())
  if b.startswith('not '):
    return (False, b[4:].strip())
  return (True, b)


def atoms_of(rules, cons, facts):
  s = set(facts)
  for h, body in rules:
    s.add(h)
    for b in body:
      s.add(lit(b)[1])
  for body in cons:
    for b in body:
      s.add(lit(b)[1])
  return sorted(s)


def stable_models(rules, cons, true_facts, atoms):
  """brute force: an interpretation M is stable iff M = least model of the
  reduct P^M (rules with a false negative literal removed, negative literals
  dropped) and M satisfies the constraints."""
  prog = [(h, [lit(b) for b in body]) for h, body in rules] + [(f, []) for f in true_facts]
  out = []
  for bits in itertools.product([False, True], repeat=len(atoms)):
    M = {a for a, b in zip(atoms, bits) if b}
    # constraints
    ok = True
    for body in cons:
      if all((a in M) == pos for pos, a in (lit(b) for b in body)):
        ok = False; break
    if not ok:
      continue
    # reduct and least model
    red = []
    for h, body in prog:
      if any((not pos) and (a in M) for pos, a in body):
        continue
      red.append((h, [a for pos, a in body if pos]))
    L = set()
    changed = True
    while changed:
      changed = False
      for h, pb in red:
        if h not in L and all(a in L for a in pb):
          L.add(h); changed = True
    if L == M:
      out.append(M)
  return out


def well_founded(rules, true_facts, atoms):
  """alternating fixpoint: T = lfp of reduct wrt U (upper), U = lfp of reduct wrt T."""
  prog = [(h, [lit(b) for b in body]) for h, body in rules] + [(f, []) for f in true_facts]

  def lfp_given(neg_true_set):
    # reduct: a negative literal \+a is true iff a not in neg_true_set
    L = set(); changed = True
    while changed:
      changed = False
      for h, body in prog:
        if h in L:
          continue
        if all(((a in L) if pos else (a not in neg_true_set)) for pos, a in body):
          L.add(h); changed = True
    return L
  T = set(); U = set(atoms)
  while True:
    T2 = lfp_given(U)
    U2 = lfp_given(T2)
    if T2 == T and U2 == U:
      break
    T, U = T2, U2
  return T, U   # true = T, undefined = U - T, false = atoms - U


def analyse(path):
  facts, rules, cons, queries = parse(path)
  atoms = atoms_of(rules, cons, facts)
  swl = sorted(facts)
  res = {}
  for q in queries:
    lower = upper = equal = incons = wt = wf = wu = plog = 0.0
    unique = True
    for bits in itertools.product([False, True], repeat=len(swl)):
      pw = 1.0
      tf = []
      for s, b in zip(swl, bits):
        pw *= facts[s] if b else (1 - facts[s])
        if b:
          tf.append(s)
      if pw == 0:
        continue
      sms = stable_models(rules, cons, tf, atoms)
      if not sms:
        incons += pw
      else:
        if len(sms) != 1:
          unique = False
        if all(q in M for M in sms):
          lower += pw
        if any(q in M for M in sms):
          upper += pw
        equal += pw * sum(q in M for M in sms) / len(sms)
      T, U = well_founded(rules, tf, atoms)
      if q in T:
        wt += pw
      elif q in U:
        wu += pw
      else:
        wf += pw
    res[q] = dict(credal=(round(lower, 6), round(upper, 6)), equal_allocation=round(equal, 6),
                  inconsistent_mass=round(incons, 6), well_founded=(round(wt, 6), round(wf, 6), round(wu, 6)),
                  every_choice_unique_model=unique and incons == 0)
  return res


if __name__ == '__main__':
  for path in sys.argv[1:]:
    r = analyse(path)
    for q, v in r.items():
      print(f"{path:44s} {q:14s} credal={v['credal']} equal={v['equal_allocation']} "
            f"incons={v['inconsistent_mass']} wf(t,f,u)={v['well_founded']} unique={v['every_choice_unique_model']}")
