"""Generation functions of the stratified Smokers variant and the variant with ranks
(family E), copied unchanged from the trial's generator of 2026-11-04."""
import random


def graph(N, seed):
  rnd = random.Random(seed)
  persons = [f'p{i}' for i in range(1, N + 1)]
  edges = set(); degree = {p: 0 for p in persons}
  for k in range(1, N):
    targets = persons[:k]; chosen = set()
    while len(chosen) < min(2, k):
      chosen.add(rnd.choices(targets, weights=[degree[t] + 1 for t in targets])[0])
    for t in chosen:
      edges.add((persons[k], t)); edges.add((t, persons[k])); degree[t] += 1; degree[persons[k]] += 1
  hub = max(persons, key=lambda p: degree[p])
  return persons, sorted(edges), hub


BASE = ['0.3::stress(X) :- person(X).',
        '0.2::influences(X,Y) :- person(X), person(Y).',
        'smokes(X) :- stress(X).',
        'smokes(X) :- friend(X,Y), influences(Y,X), smokes(Y).']


def variant1(N, seed):
  persons, edges, hub = graph(N, seed)
  facts = [f'person({p}).' for p in persons] + [f'friend({a},{b}).' for a, b in edges]
  treated = [p for i, p in enumerate(persons) if i % 3 == 0]
  tf = [f'0.6::treated({p}).' for p in treated]
  gk = facts + BASE + tf + ['0.4::asthma(X) :- smokes(X), unless(treated(X)).']
  pl = facts + BASE + tf + ['0.4::asthma(X) :- smokes(X), \\+treated(X).']
  return gk, pl, f'asthma({hub})', hub, treated


def variant2(N, seed):
  persons, edges, hub = graph(N, seed)
  facts = [f'person({p}).' for p in persons] + [f'friend({a},{b}).' for a, b in edges]
  treated = [p for i, p in enumerate(persons) if i % 3 == 0]
  tf = [f'0.6::treated({p}).' for p in treated] + [f'0.3::-treated({p}).' for p in treated]
  gk = facts + BASE + tf + [f'athlete({hub}).',
                            'untreated(X) :- person(X), unless(treated(X)).',
                            '0.4::asthma(X) :- smokes(X), untreated(X), unless(-asthma(X), 1).',
                            '0.7::-asthma(X) :- athlete(X), unless(asthma(X), 2).']
  return gk, None, f'asthma({hub})', hub, treated


