# Reasoner comparison

This document summarizes executable comparisons of GK with
[ProbLog](https://dtai.cs.kuleuven.be/problog/),
[PASTA](https://github.com/damianoazzolini/pasta),
[TweetyProject](https://tweetyproject.org/),
[clingo](https://potassco.org/clingo/),
[DLV](https://dlv.demacs.unical.it/),
[I-DLV](https://github.com/DeMaCS-UNICAL/I-DLV), and
[s(CASP)](https://gitlab.software.imdea.org/ciao-lang/sCASP). Each system was
run with its native semantics; the exact inputs, versions, commands, and
captured outputs are in the linked directories.

GK's relevant strengths in these comparisons: query-directed non-ground
first-order reasoning, input confidences, explicit opposition, recursively
evaluated prioritized exceptions, retained proofs, and four-component
reports.

The per-cell comparison table of 16 cases, which also covers
[plingo](https://github.com/potassco/plingo) and
[smProbLog](https://github.com/PietroTotis/smProblog), is in
[`../comparisons/`](../comparisons/README.md); its case descriptions are in
[`../comparisons/CASES.md`](../comparisons/CASES.md). This document covers
the comparisons that are not part of that package.

## ProbLog

A ProbLog probabilistic fact is an independent Boolean choice. Standard
inference reports the probability that a query succeeds across those
choices.

On finite programs with only positive support, GK's provenance-aware
retained-proof calculation returns the same numbers for a fixed retained
proof set; agreement with the full ProbLog result additionally requires that
the retained set covers all relevant minimal explanations. Otherwise the
retained-proof value is a lower bound on the ProbLog success probability.
Recorded cases:

- two independent facts with confidences 0.5 and 0.6 supporting one answer:
  `1 - (1 - 0.5)(1 - 0.6) = 0.8` in both systems;
- one proof using facts with confidences 0.5 and 0.6:
  `0.5 * 0.6 = 0.3` in both systems;
- proofs sharing a premise: GK records the ground activation events and uses
  the shared premise once. `overlap1.js` and `overlap3.js` return 0.846 and
  0.959; independent possible-world sampling estimates 0.8450 and 0.9596,
  and both GK values lie inside the reported 95% sampling intervals
  ([`../montecarlo/comparison.md`](../montecarlo/comparison.md)).

GK uses exact inclusion-exclusion for up to 20 reduced activation-event
sets and a deterministic approximation above that limit.

With opposing evidence the outputs differ in kind. For aggregated positive
support 0.7 and negative support 0.4, GK reports:

```text
support_for      0.3
support_against  0.0
conflict         0.4
ignorance        0.3
```

This four-component report is not a success probability; ProbLog has no
counterpart of the conflict and ignorance components. GK's default rules
run a blocker proof search with priorities; ProbLog's negation and
probabilistic choices do not implement those rules.

ProbLog additionally provides evidence conditioning, MPE and MAP queries,
probability learning, annotated disjunctions, and continuous distributions;
GK does not provide these operations
([ProbLog documentation](https://problog.readthedocs.io/en/latest/cli.html)).

## PASTA

PASTA extends ASP with probabilistic facts. Under its credal semantics, the
lower query probability counts the selections of probabilistic facts whose
every stable model satisfies the query; the upper probability counts the
selections with at least one such model. Recorded results:

- independent facts 0.5 and 0.6, each sufficient: lower = upper = 0.8;
- independent facts 0.5 and 0.6, both required: lower = upper = 0.3;
- the two opposed Nixon defaults: `pacifist` and `nonpacifist` both get the
  interval [0, 1], from the two stable models.

The first two values equal GK's `cumulate.js` and `coin1.js` results; the
agreement covers positive independent evidence. The Nixon interval measures
variation across stable models; GK reports the same conflict as signed
confidence 0 with pure ignorance. Inputs and captured outputs:
[`../Examples/system_comparison/`](../Examples/system_comparison/README.md).

## TweetyProject

Two modules were run on the default examples
([`../Examples/system_comparison/`](../Examples/system_comparison/README.md)):

- Reiter default logic: one extension for the bird theory; the default
  derives `Flies(tweety)`, and the strict fact `!Flies(opus)` prevents the
  default conclusion for Opus.
- DeLP with generalized specificity: the more specific penguin argument
  defeats the bird argument, so Opus does not fly; with the equally
  supported Nixon defaults, `pacifist(nixon)` and its negation are both
  `UNDECIDED`.

A Reiter justification is tested against a candidate extension; DeLP
compares conflicting arguments dialectically; GK runs a blocker proof
search with explicit priorities and numeric evidence.

## clingo and DLV

The bird/penguin default can be written in ASP as
`flies(X) :- bird(X), not -flies(X)`. On the finite basic example, GK,
clingo, DLV, and s(CASP) all reach the expected answer; ASP reaches it by
stable models and negation as failure, GK by a first-order proof and a
blocker check. clingo and DLV ground non-ground rules before stable-model
search; positive recursion through a function term needs infinitely many
ground terms and does not ground (row F1 of
[`../comparisons/`](../comparisons/README.md)). GK does not enumerate
stable models and has no ASP optimization constructs.

## I-DLV

The tested I-DLV roles are:

- direct query answering on disjunction-free programs that are stratified
  under negation, using Magic Sets: on the birds workload it answers
  `flies(b1)` without evaluating the unused ancestor closure;
- grounding a non-stratified program for a separate solver: on the Nixon
  defaults [clasp](https://potassco.org/clasp/) returns the two stable
  models from I-DLV's ground program.

## s(CASP)

s(CASP) evaluates a query top-down and can return a partial stable model
and a justification. On the normalized birds input its execution follows
the left-recursive transitivity rule although the query does not use it,
and the runs reached the time or stack limit
([`../Examples/asp_comparison/`](../Examples/asp_comparison/README.md)).

## Birds workload

The normalized workload asks `flies(b1)` next to a recursive ancestor
relation that the query does not use. GK and I-DLV answer without
evaluating the closure; clingo and DLV materialize it before answering;
s(CASP) enters deep recursive search. Generated inputs, commands, and
measurements: [`../Examples/asp_comparison/`](../Examples/asp_comparison/README.md).

## First-order clause problems

Three classical clause sets test non-Horn first-order reasoning with
equality, disequality, and function terms:

| Problem | Required features | GK result | Median wall time |
|---|---|---:|---:|
| NLP inconsistency | non-Horn clauses, equality and disequality, Skolem functions, cardinality axioms | theorem; 33 proof clauses | 0.01 s |
| Dreadbury | non-Horn clauses, equality and disequality, nested Skolem functions | theorem; 35 proof clauses | 0.01 s |
| set identity | non-Horn set axioms and four unrestricted witness functions | theorem; 74 proof clauses | 0.08 s |

NLP and Dreadbury need equality reasoning in non-Horn clauses and were not
translated to the tested ASP languages. The set problem has an
equality-free translation with an infinite set of ground terms; no tested
external run returned a proof. The commands, translations, resource bounds,
and per-system outcomes are in
[`../Examples/fol_comparison/`](../Examples/fol_comparison/README.md) and
[`../Examples/fol_comparison/other_systems/`](../Examples/fol_comparison/other_systems/README.md).

GK's algorithms are described in [`how_gk_works.md`](how_gk_works.md).
