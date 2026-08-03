# Monte Carlo comparison results

This file compares GK's reported results with estimates from the sampling
calculations described in [`README.md`](README.md). Each result can be
repeated with the command and fixed settings below. The examples start
with individual facts and simple chains of rules; later examples add
conflicting facts, recursive rules, and defaults.

The appendix explains why some other repository examples have no numerical
rows here.

## Reproduction protocol

The GK columns come from gk 1.0.10 (`bin/gk`, one `-detail` run per file).
Sampling uses the Python standard-library random generator, 10,000 trials,
and seed 1. Clause-activation sampling uses per-ground-instance draws; the
shared-threshold sampler uses two independent uniforms per atom and the
local combination rules described in [`README.md`](README.md).

Clause-activation command (add `--json FILE` for a machine-readable
capture of the run):

```sh
montecarlo/gkmc.py -n 10000 --seed 1 FILE
```

All clause-activation rows below had 10,000 valid trials and zero
timeouts. Shared-threshold command:

```sh
montecarlo/gkmc.py --semantics threshold -n 10000 --seed 1 FILE
```

For one sampled proportion, 10,000 trials give a worst-case approximate
95% half-width of 0.01. Clause-activation rows show the paired interval
calculated by the script. Small differences of a few thousandths in the
shared-threshold table are sampling variation. The sampler outputs are
regenerated from the fixed seed rather than committed.

The GK calculation column shows the `-detail` `calculation` value, as
defined in [`../Doc/how_gk_works.md`](../Doc/how_gk_works.md):
`canonical_atom` is a completed shared-threshold report; `flat` is a
direct retained-proof calculation. Every row below had `coverage_status:
complete`; `polarity_status` was `guaranteed` for the `canonical_atom`
rows and `not_guaranteed` for the `flat` rows.

## Clause-activation sampling

`MC pos-neg` is the fraction of worlds proving the answer minus the
fraction proving its explicit negation. `GK result` is the signed GK
result: a rejected answer is negative even when gk's output prints its
magnitude separately from the rejection label.

| File and answer | Mechanism | MC pos-neg | 95% CI | GK result | GK calculation |
|---|---|---:|---:|---:|---|
| `cumulate.js`, `true` | noisy-or of 0.5 and 0.6 | 0.8013 | [0.7935, 0.8091] | 0.8000 | flat |
| `coin1.js`, `c` | one proof using 0.5 and 0.6 | 0.2979 | [0.2889, 0.3069] | 0.3000 | flat |
| `overlap1.js`, `true` | two proofs sharing one premise | 0.8450 | [0.8379, 0.8521] | 0.8460 | flat |
| `overlap3.js`, `true` | three overlapping proof paths | 0.9596 | [0.9557, 0.9635] | 0.9590 | flat |
| `net_direct.js`, `true` | opposing facts about the queried atom | 0.3107 | [0.2976, 0.3238] | 0.3000 | canonical_atom |
| `negation_conflict.js`, `a` | contested premise propagated through rules | 0.2487 | [0.2373, 0.2601] | 0.2520 | canonical_atom |
| `bird_exception.js`, `b` | unopposed default | 1.0000 | [1.0000, 1.0000] | 1.0000 | canonical_atom |
| `bird_exception.js`, `a` | default with exception evidence at confidence 0.9 | -0.7968 | [-0.8086, -0.7850] | -0.8000 | canonical_atom |
| `bird_penguin.js`, `p` | opposing bird and penguin conclusions | 0.6409 | [0.6287, 0.6531] | 0.6400 | canonical_atom |
| `net_premise.js`, `true` | contested premise followed by a 0.9 rule | 0.4543 | [0.4445, 0.4641] | 0.2700 | canonical_atom |

All rows except `net_premise.js` agree within their intervals. The
agreeing rows cover the cases most closely related to independent
probabilistic facts, definite rules, and the default interactions
described below.

`bird_exception.js`, `a` is the uncertain-exception case. GK rejects the
answer at 0.8 with 0.1 positive support and 0.9 negative support —
signed -0.80, in agreement with the sampled difference.

`bird_penguin.js`, `p` (query: who does not fly) is the same family for a
negative query. Sampling finds `-flies(p)` provable in the 0.72 of worlds
where the penguin fact and the no-fly rule are both present, and
`flies(p)` provable only in the 0.08 where the penguin is a bird but the
no-fly rule is absent, a difference of +0.64. GK reports 0.72 positive
support, 0.08 negative support, and the accepted answer at 0.64.

`net_premise.js` is a counterexample to a general equivalence between the
two measures; the worked explanation is under Differences below.

## Shared-threshold sampling

Each cell has the order:

```text
positive support / negative support / conflict / ignorance
```

| File | Shared-threshold MC | gk `-detail` | GK calculation | Assessment |
|---|---:|---:|---|---|
| `trivial.js` | 1.0000 / 0 / 0 / 0 | 1.0000 / 0 / 0 / 0 | canonical_atom | deterministic agreement |
| `cumulate.js` | 0.7984 / 0 / 0 / 0.2016 | 0.8000 / 0 / 0 / 0.2000 | flat | agreement |
| `net_lone.js` | 0.4972 / 0 / 0 / 0.5028 | 0.5000 / 0 / 0 / 0.5000 | flat | agreement |
| `net_direct.js` | 0.3018 / 0 / 0.3984 / 0.2998 | 0.3000 / 0 / 0.4000 / 0.3000 | canonical_atom | agreement |
| `net_fought.js` | 0.4965 / 0 / 0.3984 / 0.1051 | 0.5000 / 0 / 0.4000 / 0.1000 | canonical_atom | agreement |
| `net_against.js` | 0 / 0.5028 / 0.2956 / 0.2016 | 0 / 0.5000 / 0.3000 / 0.2000 | canonical_atom | agreement |
| `net_strong.js` | 0.5993 / 0 / 0.2956 / 0.1051 | 0.6000 / 0 / 0.3000 / 0.1000 | canonical_atom | agreement |
| `coin3.js` | 0.9759 / 0 / 0 / 0.0241 | 0.9744 / 0 / 0 / 0.0256 | flat | agreement |
| `coin4.js` | 0.9724 / 0 / 0 / 0.0276 | 0.9744 / 0 / 0 / 0.0256 | flat | agreement |
| `n2c.js` | 0.1157 / 0 / 0.7909 / 0.0934 | 0.1180 / 0 / 0.7900 / 0.0920 | canonical_atom | agreement |
| `near.js` | 1.0000 / 0 / 0 / 0 | 0.4305 / 0 / 0 / 0.5695 | flat | different recursive-proof treatment |
| `nixon_taxonomy.js` | 0 / 0 / 0 / 1.0000 | 0 / 0 / 0 / 1.0000 | canonical_atom | agreement |

A `canonical_atom` row is a completed shared-threshold report, and the
sampler estimates the same construction, so agreement checks the two
implementations against each other. The calculation value alone does not
establish that a case lies inside the paper's correspondence fragment;
`nixon_taxonomy.js`, for example, exercises the separately defined local
rule for equally ranked opposed defaults (mutual blocking) rather than
the acyclic opposition fragment. The `flat` rows are direct
retained-proof calculations; agreement there holds because the retained
proof set covers the relevant derivations of these small examples.
`near.js` is the case where retained-proof coverage and the exhaustively
grounded model differ; see Differences.

## Differences

The one-sentence summary of each reading:

- GK pools the retained derivations of an answer and its negation; when a
  relevant atom is contested, the dependency-aware calculation resolves
  the opposition at that atom before usable support is propagated.
- Clause-activation sampling counts ground-instance activation worlds:
  each uncertain ground clause is independently active or absent, and a
  world counts for an answer when the answer is provable in it.
- Shared-threshold sampling counts worlds with per-atom thresholds:
  evidence counts when its pooled strength clears the atom's threshold,
  and ordinary opposition about one atom faces one shared threshold.

### A default with an uncertain exception condition

[`bird_exception.js`](../Examples/exceptions/bird_exception.js): two
birds, birds fly by default, and evidence at 0.9 that `a` does not fly.

```text
GK (query flies(X)):        b accepted at 1.0; a rejected at 0.8
                            detail for a: support_for 0.1,
                            support_against 0.9
clause-activation sampling: provable 0.10, negation provable 0.90,
                            difference -0.80
```

All columns rest on the same world split: in nine worlds of ten, support
for the exception condition is active and makes `-flies(a)` provable; in
one world of ten the flying default stands. GK's signed result for `a` is
-0.8, matching the sampled difference, and its 0.1 positive support
equals the sampled positive column.

### A contested premise

[`net_premise.js`](../Examples/confidences/net_premise.js): `bird(a)` at
0.5, `-bird(a)` at 0.2, and birds fly at 0.9.

```text
GK:                          0.27   (resolves the opposition on the
                                     premise: (0.5 - 0.2) * 0.9)
clause-activation sampling:  0.45   (0.5 * 0.9; support for the explicit
                                     negation does not reach the query)
shared-threshold sampling:   0.27   (bird usable iff 0.2 < U <= 0.5)
```

Here the two sampled readings split. Under independent activation,
`-bird(a)` never makes `-flies(a)` derivable, so it changes nothing: the
positive premise is provable in half of the worlds, including worlds
where its negation is provable alongside it, and the rule fires in 0.9 of
those. Under one shared threshold, the two bird statements are evaluated
against the same draw: only the margin `0.2 < U <= 0.5` leaves the
premise usable, and GK's subtraction is the closed form of exactly that.
In GK's dependency-aware calculation, doubt about a premise reduces every
conclusion built on it, whether or not the doubt can be propagated to the
conclusion's negation.

### A recursive rule

[`near.js`](../Examples/confidences/near.js): a chain of nine certain
`near` links and a transitivity rule at 0.9.

```text
GK:                        0.4305   (0.9^8: eight rule applications;
                                     calculation flat)
shared-threshold sampling: 1.0000   (alternative derivations made the
                                     query usable in all sampled worlds)
```

GK's retained answer proof is one chain using eight distinct ground
instances of the transitivity rule, hence `0.9^8`; the value is exact for
that ground retained proof's activation-event set. The threshold sampler
instead grounds the finite graph before sampling and considers every
reachable ground rule instance, each active with probability 0.9 per
draw; there are enough alternative derivations of the query that at least
one was available in all 10,000 sampled worlds. Clause-activation
sampling behaves like the threshold sampler here. The difference is
retained-proof coverage against exhaustive grounded evaluation; it is not
caused by statement-level sharing.

### Defaults and priorities

The threshold-world sampler implements the defined local combination
rules for defaults and opposing evidence: exception conditions,
equal-rank mutual blocking, the strict-priority override, and blocker
cycles through the queried atom. These are covered by
[`reference_checks/`](reference_checks/). Cycles through an exception
condition away from the query, cycles through a contested atom,
rank-restricted checks, taxonomy-valued priorities, and multi-level
default structures are reported as unsupported (`not scored`) rather than
scored.

The two models measure different quantities; GK's calculations are
bounded report-time evaluations rather than world enumeration, and the
samplers are kept as independent checks of the two reference models on
their stated fragments.

## Coverage limits

The result tables use examples for which the sampled model has a clear
reading. Other repository examples were excluded for the reasons below.

### Other input syntaxes

`gkmc.py` reads JSON-LD-LOGIC `.js` files. Equivalent `.gkp`, `.gks`,
TPTP, ASP, and Prolog inputs are not sampled.

### Function terms, equality, and arithmetic

The samplers require a finite domain of named constants. They do not
cover function-term examples (`near2.js`, `rules4.js`, `rules5.js`,
`penguin4.js`, `gbirds_funsymbs.js`), equality examples (`algebra*.js`,
`equality*.js`, the fluent equalities in `people_room.js`), or the
arithmetic examples under `Examples/arithmetic/`. The translated language
examples use context terms, Skolem terms, quantifier encodings, and
built-in answer predicates; they run with `axioms_std.js` and are outside
these finite standalone samplers.

### Queries and clauses outside the shared-threshold model

Shared-threshold mode requires a single predicate query and directional
clauses with an unambiguous head. It does not score conjunctive queries
(parts of the `n1`, `n2`, `conf`, and `n3` families) or clauses with
several positive literals (`rules1.js` through `rules3.js`). Open queries
are evaluated per closed instance over the named constants. Some of these
files run under clause-activation mode, but the tables already contain
simpler examples of the same pooling mechanisms.

### Defaults and priorities outside the model

The sampled models cover the default cases in the result tables and in
[`reference_checks/`](reference_checks/). Taxonomy priorities, multi-level
competing defaults, and persistence defaults need GK-specific usability
checks; this excludes `classify`, the larger `penguin` variants,
`taxonomy.js`, `people_room.js`, and the full Nixon variants from a
sampled numerical comparison.

### Deterministic and auxiliary files

Sampling adds no information when every statement has confidence 1. Apart
from the small `trivial.js` baseline retained in the table, this covers
the basic `gbirds`, `bird_default`, and the ASP timing inputs; the ASP
encodings are compared in
[`../Examples/asp_comparison/`](../Examples/asp_comparison/README.md).
Strategy JSON files, taxonomy data files, `axioms_std.js`, and input
generators are configuration or support material rather than standalone
knowledge-base queries.
