# Monte Carlo comparison results

This file compares gk's reported confidences with estimates from the independent
sampling calculations described in [`README.md`](README.md). Each result can be
repeated using the command and fixed settings below. The examples start with
individual facts and simple chains of rules. Later examples introduce
conflicting facts, recursive rules, and defaults.

The appendix explains why some other repository examples do not have numerical
rows here.

## Reproduction protocol

Results were recorded with:

- gk 1.0.0;
- `bin/gk` SHA-256
  `a639b29a8a9578bb8b01cd6b96614f1e93ada7b98fa7f26eec6f058393a716d1`;
- [Python 3](https://www.python.org/) standard-library random generator;
- 10,000 trials and seed 1;
- per-ground-instance rule draws for inclusion sampling.

The gk columns were rechecked on 2026-07-20 with the current shipped binary,
SHA-256
`7a976fd38fdffcade87a67de9f30339ec3ebf4cca12d5b45045be418f6a7c5e2`;
the values were unchanged. The hash above remains the provenance for the
recorded sampling runs.

Inclusion command:

```sh
montecarlo/gkmc.py -n 10000 --seed 1 FILE
```

All inclusion rows below had 10,000 valid trials and zero timeouts. Threshold
command:

```sh
montecarlo/gkmc.py --semantics threshold -n 10000 --seed 1 FILE
```

For one sampled proportion, 10,000 trials give a worst-case approximate 95%
half-width of 0.01. Inclusion rows show the paired interval calculated by the
script. The threshold table shows four proportions compactly; small differences
of a few thousandths are sampling variation.

## Inclusion sampling

`MC pos-neg` is the fraction of worlds proving the answer minus the fraction
proving its explicit negation. `gk` is the signed gk result: a rejected answer
is shown as negative even when gk's output prints its magnitude separately from
the rejection label.

The first four rows cover independent facts, a product along one proof, and
alternative proofs with shared premises.

| File and answer | Mechanism | MC pos-neg | 95% CI | gk |
|---|---|---:|---:|---:|
| `cumulate.js`, `true` | noisy-or of 0.5 and 0.6 | 0.8013 | [0.7935, 0.8091] | 0.8000 |
| `coin1.js`, `c` | one proof using 0.5 and 0.6 | 0.2979 | [0.2889, 0.3069] | 0.3000 |
| `overlap1.js`, `true` | two proofs sharing one premise | 0.8450 | [0.8379, 0.8521] | 0.8460 |
| `overlap3.js`, `true` | three overlapping proof paths | 0.9596 | [0.9557, 0.9635] | 0.9590 |
| `net_direct.js`, `true` | opposing facts about the queried atom | 0.3107 | [0.2976, 0.3238] | 0.3000 |
| `negation_conflict.js`, `a` | contested premise propagated through rules | 0.2487 | [0.2373, 0.2601] | 0.2520 |
| `bird_exception.js`, `b` | unopposed default | 1.0000 | [1.0000, 1.0000] | 1.0000 |
| `bird_exception.js`, `a` | default with 0.9 contrary evidence | 0.1016 | [0.0957, 0.1075] | 0.1000 |
| `bird_penguin.js`, `p` | opposing bird and penguin conclusions | -0.0793 | [-0.0846, -0.0740] | -0.0800 |
| `net_premise.js`, `true` | contested premise followed by a 0.9 rule | 0.4543 | [0.4445, 0.4641] | 0.2700 |

The first ten answer rows agree within their intervals. They cover the cases
most closely related to independent probabilistic facts and definite rules.

`net_premise.js` is a counterexample to a general equivalence. Its premise has
0.5 positive and 0.2 negative evidence, followed by a rule with confidence 0.9.
gk first nets the premise to 0.3 and obtains `0.3 * 0.9 = 0.27`. In inclusion
sampling, the positive premise is provable in about half the worlds, including
worlds where its negation is also provable. The positive query frequency is
therefore about `0.5 * 0.9 = 0.45`; no rule derives the negative query, so
subtraction does not remove those contested-premise worlds.

This distinction also explains why inclusion sampling alone is insufficient
for general default programs. It classifies provability of the final literal;
gk can propagate conflict and priority information from intermediate atoms.

## Threshold sampling

Each cell has the order:

```text
support for / support against / conflict / ignorance
```

| File | Threshold MC | gk `-detail` | Assessment |
|---|---:|---:|---|
| `trivial.js` | 1.0000 / 0 / 0 / 0 | 1.0000 / 0 / 0 / 0 | deterministic agreement |
| `cumulate.js` | 0.7980 / 0 / 0 / 0.2020 | 0.8000 / 0 / 0 / 0.2000 | agreement |
| `net_lone.js` | 0.5023 / 0 / 0 / 0.4977 | 0.5000 / 0 / 0 / 0.5000 | agreement |
| `net_direct.js` | 0.2977 / 0 / 0.4041 / 0.2982 | 0.3000 / 0 / 0.4000 / 0.3000 | agreement |
| `net_fought.js` | 0.4926 / 0 / 0.4041 / 0.1033 | 0.5000 / 0 / 0.4000 / 0.1000 | agreement |
| `net_against.js` | 0 / 0.4965 / 0.3015 / 0.2020 | 0 / 0.5000 / 0.3000 / 0.2000 | agreement |
| `net_strong.js` | 0.5952 / 0 / 0.3015 / 0.1033 | 0.6000 / 0 / 0.3000 / 0.1000 | agreement |
| `coin3.js` | 0.9734 / 0 / 0 / 0.0266 | 0.9744 / 0 / 0 / 0.0256 | agreement |
| `coin4.js` | 0.9720 / 0 / 0 / 0.0280 | 0.9744 / 0 / 0 / 0.0256 | agreement |
| `n2c.js` | 0.1205 / 0 / 0.7894 / 0.0901 | 0.1180 / 0 / 0.7900 / 0.0920 | agreement |
| `near.js` | 1.0000 / 0 / 0 / 0 | 0.4305 / 0 / 0 / 0.5695 | different recursive-proof treatment |
| `nixon_taxonomy.js` | 0 / 0 / 1.0000 / 0 | 0 / 1.0000 / 0 / 0 | priority/default case outside the model |

The cases with positive and negative facts about the queried atom reproduce the
four masses because one shared threshold partitions the unit interval into the
same four regions as gk's netting calculation for those facts.

`near.js` contains nine certain links and a transitivity rule with confidence
0.9. gk reports the product of eight uses in one chain, `0.9^8 = 0.4305`. The
threshold model grounds the recursive rule and allows many alternative
decompositions of the same path. Every one of the 10,000 sampled evaluations
found at least one proof. This is a semantic difference, not evidence that one
of the two displayed numbers is an inaccurate Monte Carlo estimate.

`nixon_taxonomy.js` has two opposed equal defaults. The restricted threshold
model leaves their overlap as conflict. Current gk assigns the mass to support
against for this direct query. Taxonomy/default priority behavior is therefore
not claimed by the threshold model.

## Coverage limits

The result tables use examples for which the independent calculation has a
clear interpretation. Other repository examples were excluded for the reasons
below. This appendix explains omissions; it is not another result table.

### Other input syntaxes

`gkmc.py` reads JSON-LD-LOGIC `.js` files. Equivalent `.gkp`, `.gks`, TPTP,
ASP, [DLV](https://www.dlvsystem.it/dlvsite/dlv/), and Prolog inputs are not
sampled. Examples include the GKP versions of the confidence and default
examples, `bird_penguin.p`, and the
files under `Examples/asp_comparison/other_systems/`.

### Function terms, equality, and arithmetic

The samplers require a finite domain of named constants. They do not cover:

- function-term examples such as `near2.js`, `rules4.js`, `rules5.js`,
  `penguin4.js`, and `gbirds_funsymbs.js`;
- equality examples such as `algebra*.js`, `equality*.js`, and the fluent
  equalities in `people_room.js`;
- arithmetic evaluation and bounded instantiation under `Examples/arithmetic/`.

The translated language examples also use context terms, Skolem terms,
quantifier encodings, and built-in answer predicates. They must be run with
`axioms_std.js` and are outside these finite standalone samplers.

### Queries and clauses outside the threshold model

Threshold mode requires one ground predicate query and directional clauses
with an unambiguous conclusion. It therefore does not score open or conjunctive
queries such as the `n1`, `n2`, `conf`, and `n3` families, or legacy clauses
with several possible positive heads such as `rules1.js` through `rules3.js`.
Some of these files can be used with inclusion mode, but they were not added as
further numerical rows because the tables already contain simpler examples of
the same pooling mechanisms.

### Defaults and priorities outside the model

The independent models cover only the default cases shown in the result
tables. Taxonomy priorities, multi-level competing defaults, and persistence
defaults require gk-specific usability checks. This excludes `classify`, the
larger `penguin` variants, `taxonomy.js`, `people_room.js`, and the full Nixon
variants from a claimed independent numerical comparison.

### Deterministic and auxiliary files

Sampling adds no information when every statement has confidence 1. Apart from
the small `trivial.js` baseline retained in the table, this includes the basic
`gbirds`, `bird_default`, and large ASP timing inputs. The ASP encodings are
compared in
[`../Examples/asp_comparison/`](../Examples/asp_comparison/README.md).

Strategy JSON files, taxonomy data files, `axioms_std.js`, and input generators
are configuration or support material rather than standalone knowledge-base
queries.
