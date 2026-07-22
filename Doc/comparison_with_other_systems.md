# Reasoner comparison

This document records executable comparisons with ProbLog, PASTA,
TweetyProject, clingo, DLV, I-DLV, and s(CASP). Each system uses its native
semantics. Current measurements are kept separate from historical results.

## ProbLog

### Positive-only results

A ProbLog probabilistic fact is an independent Boolean choice. Standard
inference reports the probability that a query succeeds across those choices.
For a finite program with only positive support, gk's current proof-instance
calculation often gives the same number:

- two independent facts with confidences 0.5 and 0.6 supporting one answer give
  `1 - (1 - 0.5)(1 - 0.6) = 0.8`;
- one proof using facts with confidences 0.5 and 0.6 gives
  `0.5 * 0.6 = 0.3`;
- when proofs share a premise, gk records the ground evidence instances and
  uses that premise once when combining the proofs.

The first two are the usual ProbLog distribution-semantics values as well as
gk's results. The shared-premise cases in
[`../montecarlo/`](../montecarlo/README.md) are compared with independent
possible-world sampling: `overlap1.js` estimates 0.8450 with gk at 0.846, and
`overlap3.js` estimates 0.9596 with gk at 0.959. Both gk values lie inside the
reported 95% sampling intervals. The intervals and commands are in
[`../montecarlo/comparison.md`](../montecarlo/comparison.md).

The sampler supports constants only. GK uses exact inclusion-exclusion for up
to 20 reduced proof masks and a deterministic approximation above that limit.

### Opposing evidence

gk treats a negative literal such as `-flies(a)` as explicit evidence with its
own confidence. If the aggregated positive support is 0.7 and the aggregated
negative support is 0.4, gk's detailed result is:

```text
support_for      0.3
support_against  0.0
conflict         0.4
ignorance        0.3
```

This four-component assessment is not a ProbLog success probability. ProbLog
does not report gk's conflict and ignorance values.

Defaults also differ. A gk blocker starts another proof search to determine
whether an exception defeats a candidate proof, and priorities restrict which
defaults may participate in that check. ProbLog's Prolog-style negation and
probabilistic choices do not implement those blocker and priority rules.

### Other ProbLog operations

ProbLog provides evidence conditioning, MPE and MAP queries, probability
learning, annotated disjunctions, and continuous distributions. GK does not
provide these operations. See the
[ProbLog documentation](https://problog.readthedocs.io/en/latest/cli.html).

## PASTA

PASTA extends ASP with probabilistic facts. Under its credal semantics, each
selection of probabilistic facts can have one or more stable models. The lower
query probability counts selections where the query holds in every stable
model; the upper probability counts selections where it holds in at least one.

Recorded results:

- independent facts with probabilities `0.5` and `0.6`, each sufficient for
  the query, give lower = upper = `0.8`;
- independent facts with probabilities `0.5` and `0.6`, both required by one
  proof, give lower = upper = `0.3`;
- the two opposed Nixon defaults give two stable models, so both `pacifist`
  and `nonpacifist` have lower probability `0` and upper probability `1`.

The first two numbers agree with gk's `cumulate.js` and `coin1.js` results.
That is the same limited agreement already described for ProbLog: positive
independent evidence uses the same arithmetic. The Nixon interval
has no direct gk numeric counterpart. It measures variation across stable
models, whereas gk assesses opposing proofs and default blockers.

Inputs, exact commands, implementation provenance, and captured output are in
[`../Examples/system_comparison/`](../Examples/system_comparison/README.md).

## TweetyProject

TweetyProject is a Java library collection rather than one reasoning
formalism. The comparison uses two modules related to gk's default examples:

- Reiter default logic computes extensions. In the bird theory there is one
  extension: the normal bird default derives `Flies(tweety)`, while the strict
  fact `!Flies(opus)` prevents the default conclusion for Opus.
- DeLP builds arguments from strict and defeasible rules and compares
  conflicting arguments. With generalized specificity, the penguin argument
  for `~Flies(opus)` defeats the less-specific bird argument. With equally
  supported Nixon defaults, both `pacifist(nixon)` and its negation are
  `UNDECIDED`.

The semantics differ from gk's. A Reiter justification is tested against a
candidate extension; DeLP uses dialectical argument evaluation; gk launches a
blocker proof search and can use explicit priorities and numeric evidence. The
repository harness runs both TweetyProject modules and records skeptical,
credulous, and DeLP answers in
[`../Examples/system_comparison/`](../Examples/system_comparison/README.md).

## Answer Set Programming

### Basic defaults

The bird/penguin rule can be written in ASP as:

```prolog
flies(X) :- bird(X), not -flies(X).
```

On the finite basic example, gk, clingo, DLV, and s(CASP) all obtain the
expected query answer. The route to that answer is different: ASP uses stable
models and negation as failure, whereas gk constructs a first-order proof and
checks an explicit blocker.

### clingo and DLV

clingo and DLV ground non-ground rules before stable-model search. Function
terms are valid syntax, but positive recursion such as
`bird(f(X)) :- bird(X)` needs infinitely many ground terms. The historical
grounders in this repository's birds example did not finish that input. GK
does not enumerate stable models or provide ASP optimization constructs.

### I-DLV

I-DLV has two relevant roles. It can evaluate a disjunction-free program that
is stratified under negation and answer a query using Magic Sets, or it can
ground a general ASP program for a separate stable-model solver.

Both roles were exercised on defeasible examples. Its direct query mode
derives the ordinary bird's flight while respecting an explicit penguin
exception. For the non-stratified Nixon defaults, I-DLV grounds the program
and [clasp](https://potassco.org/clasp/) returns two stable models, one
containing `pacifist(nixon)` and the other its opposing atom.

I-DLV was also added to the normalized birds workload. Query rewriting does
not evaluate the ancestor closure, which is not needed for `flies(b1)`. Single
runs returned `flies(b1)` in less than 0.01 seconds at 1,000 and 2,000
constants and 0.24 seconds at 100,000 constants.
The exact inputs, memory figures, command, and executable hash are in
[`../Examples/asp_comparison/`](../Examples/asp_comparison/README.md).

### s(CASP)

s(CASP) is not a grounding solver. It evaluates a query top-down and can return
a partial stable model and a justification. clingo and DLV instead ground the
complete finite program before stable-model search.

On the normalized input, s(CASP) 1.1.4 follows the left-recursive transitivity
rule although the query does not use it. The runs reached either the time limit
or the Prolog stack limit.

### Birds benchmark

The `flies(b1)` query does not use the recursive ancestor relation. clingo and
DLV materialize that relation, I-DLV restricts evaluation with Magic Sets,
s(CASP) enters deep recursive search, and gk proves the query directly.
Commands and measurements are in
[`../Examples/asp_comparison/README.md`](../Examples/asp_comparison/README.md).

## First-order clause problems

These three classical clause sets test non-Horn first-order reasoning with
equality, disequality, and function terms.

| Problem | Required features | gk result | Median wall time |
|---|---|---:|---:|
| NLP inconsistency | non-Horn clauses, equality and disequality, Skolem functions, cardinality axioms | theorem; 33 proof clauses | 0.01 s |
| Dreadbury | non-Horn clauses, equality and disequality, nested Skolem functions | theorem; 35 proof clauses | 0.01 s |
| set identity | non-Horn set axioms and four unrestricted witness functions | theorem; 74 proof clauses | 0.08 s |

Commands and gk measurements are in
[`../Examples/fol_comparison/`](../Examples/fol_comparison/README.md).

NLP and Dreadbury require equality reasoning in non-Horn clauses and were not
translated to the tested ASP languages. The set problem has an equality-free
translation, but its recursive term closure has an infinite Herbrand universe.

Results for the set translation:

| System | Result |
|---|---|
| ProbLog | accepted the surface file but returned probability 0; its ground form reduces the query to `fail` because classical disjunctive clauses are not ProbLog rule heads |
| PASTA | reached the run bound after using about 950 MiB while grounding; no interval was produced |
| TweetyProject | the set input parses, but its simple FOL reasoner rejects signatures containing functors; its TPTP parser rejects the other two inputs at equality literals containing functions |
| clingo | reached the grounding memory bound; no model was produced |
| DLV | rejected the recursive term rule because termination is not guaranteed |
| I-DLV | reached the grounding memory bound; no ground program was produced |
| s(CASP) | returned no answer within the run bound |

No tested run returned a proof. Commands, versions, resource bounds, and
parser or grounding results are in
[`../Examples/fol_comparison/other_systems/`](../Examples/fol_comparison/other_systems/README.md).

## English-language examples

[`Examples/language/`](../Examples/language/README.md) contains compiled output
from the [llmpipe commonsense-reasoning system](https://github.com/tammet/nlpsolver/tree/main/llmpipe).
llmpipe translates English into gk logic and uses gk for proof search.

The compiled examples combine several features: first-order variables and
function terms, existential witnesses, explicit negation, disjunction,
contexts, question-answer bridges, defaults, confidence annotations, and a
shared background theory for taxonomy, part-whole relations, degrees, events,
and space. The compared systems do not accept these JSON-LD-LOGIC conventions,
so no cross-system results are listed for this group.

## Capabilities

| Question | gk | ProbLog | PASTA | TweetyProject modules compared here | clingo / DLV | I-DLV | s(CASP) |
|---|---|---|---|---|---|---|---|
| Primary result | first-order query proof and assessment | query probability | lower and upper query probability | default extensions or DeLP query status | stable models | stratified query answers or a ground ASP program | query-directed partial stable model |
| Numeric uncertainty | proof support and four-component assessment | distribution-semantics probability | credal probability interval | none in the two compared modules | none in the base systems | none | none in the base system |
| Exceptions and conflict | blockers, priorities, opposing evidence | encoding-dependent | stable-model variation | Reiter justifications or dialectical arguments | negation as failure | stratified negation or stable models with a solver | negation as failure |
| Query focus | yes | finite proof/formula construction | finite grounding and model analysis | library algorithm depends on the formalism | complete grounding | Magic Sets for stratified queries | top-down evaluation |
| Multiple alternatives | proof alternatives combine into an assessment | summed possible worlds | lower/upper bounds over stable models | extensions or competing arguments | stable-model enumeration | solver-dependent outside stratified mode | query-relevant partial models |
| Evidence conditioning or learning | no | yes | conditioning and additional inference modes | separate TweetyProject modules, not these two | no | no | no |
| Explanation object | gk proof | explanation modes | stable models and probability bounds | extensions or dialectical arguments | models; further tooling is needed for proof-style explanations | query answers or ground rules | justification tree |

GK's algorithms are described in [`how_gk_works.md`](how_gk_works.md).
