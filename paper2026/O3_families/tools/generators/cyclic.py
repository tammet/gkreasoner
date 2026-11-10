"""Generation functions of the random non-stratified programs, the exception rings
(family C) and the argumentation frameworks (family D), copied unchanged from the
trial's generators of 2026-11-04."""
import random


def random_program(n, seed, pos_rules=1):
  rnd = random.Random(seed)
  pl, gk = [], []
  for i in range(n):
    p = round(rnd.uniform(0.2, 0.8), 2)
    pl.append(f'{p}::f{i}.'); gk.append(f'{p}::f{i}.')
    j = rnd.choice([k for k in range(n) if k != i])
    pl.append(f'a{i} :- f{i}, \\+a{j}.'); gk.append(f'a{i} :- f{i}, unless(a{j}).')
  for _ in range(pos_rules):
    i, k = rnd.sample(range(n), 2)
    pl.append(f'a{i} :- a{k}.'); gk.append(f'a{i} :- a{k}.')
  return pl, gk, 'a0'


def ring(k, p=0.5):
  pl, gk = [], []
  for i in range(k):
    pl.append(f'{p}::f{i}.'); gk.append(f'{p}::f{i}.')
    j = (i + 1) % k
    pl.append(f'a{i} :- f{i}, \\+a{j}.'); gk.append(f'a{i} :- f{i}, unless(a{j}).')
  return pl, gk, 'a0'


def grounded(n, attacks):
  att = {i: set() for i in range(n)}
  for a, b in attacks:
    att[b].add(a)
  lab = {i: 'undec' for i in range(n)}
  changed = True
  while changed:
    changed = False
    for x in range(n):
      if lab[x] != 'undec':
        continue
      if all(lab[y] == 'out' for y in att[x]):
        lab[x] = 'in'; changed = True
      elif any(lab[y] == 'in' for y in att[x]):
        lab[x] = 'out'; changed = True
  return lab, att


def af(n, p, seed):
  rnd = random.Random(seed)
  attacks = [(a, b) for a in range(n) for b in range(n) if a != b and rnd.random() < p]
  lab, att = grounded(n, attacks)
  cl = []
  af.att = att
  for x in range(n):
    if att[x]:
      # gk allows one unless per rule: an OR gate over the attackers
      if len(att[x]) == 1:
        y = next(iter(att[x]))
        cl.append(f'acc(x{x}) :- unless(acc(x{y})).')
      else:
        for y in sorted(att[x]):
          cl.append(f'att_x{x} :- acc(x{y}).')
        cl.append(f'acc(x{x}) :- unless(att_x{x}).')
      # no negative rules: a certain `-acc(x) :- acc(y)` would be used in every
      # direction (an attack in both directions); out is read off att_x instead
    else:
      cl.append(f'acc(x{x}).')
  return cl, lab, attacks


