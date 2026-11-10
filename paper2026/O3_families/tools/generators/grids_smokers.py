"""Generation functions of the ProbLog grids and the Smokers graphs, copied unchanged
from the trial's generator of 2026-11-04 (family A)."""
import random


def grid(N, d, prob=0.5, full=True):
  """N x N grid, directed edges right, down, diagonal, each with probability prob;
  query path(n_i_i, n_N_N) with i = N - d. With full=False only the (d+1)^2 corner."""
  i0 = N - d
  lo = 1 if full else i0
  facts = []
  for i in range(lo, N + 1):
    for j in range(lo, N + 1):
      for (di, dj) in ((0, 1), (1, 0), (1, 1)):
        a, b = i + di, j + dj
        if a <= N and b <= N:
          facts.append(f'{prob}::edge(n_{i}_{j}, n_{a}_{b}).')
  rules = ['path(X,Y) :- edge(X,Y).', 'path(X,Y) :- edge(X,Z), path(Z,Y).']
  q = f'path(n_{i0}_{i0}, n_{N}_{N})'
  return facts, rules, q


def smokers(N, seed):
  """power-law (preferential attachment, m=2) friendship graph on N persons."""
  rnd = random.Random(seed)
  persons = [f'p{i}' for i in range(1, N + 1)]
  edges = set()
  degree = {p: 0 for p in persons}
  for k in range(1, N):
    targets = persons[:k]
    m = min(2, k)
    chosen = set()
    while len(chosen) < m:
      weights = [degree[t] + 1 for t in targets]
      t = rnd.choices(targets, weights=weights)[0]
      chosen.add(t)
    for t in chosen:
      edges.add((persons[k], t)); edges.add((t, persons[k]))
      degree[t] += 1; degree[persons[k]] += 1
  facts = [f'person({p}).' for p in persons] + [f'friend({a},{b}).' for a, b in sorted(edges)]
  rules = ['0.3::stress(X) :- person(X).',
           '0.2::influences(X,Y) :- person(X), person(Y).',
           'smokes(X) :- stress(X).',
           'smokes(X) :- friend(X,Y), influences(Y,X), smokes(Y).',
           '0.4::asthma(X) :- smokes(X).']
  hub = max(persons, key=lambda p: degree[p])
  return facts, rules, f'smokes({hub})', len(edges) // 2


