# Comparison with probabilistic and defeasible reasoning systems

gk and the systems below accept superficially similar rules, but they do not
assign the same meaning to every program. The comparison begins with the
result each system computes:

- gk searches for first-order proofs of a query, checks default blockers, and
  assesses the supporting and opposing proofs;
- [ProbLog](https://dtai.cs.kuleuven.be/problog/editor.html) computes
  probabilities induced by probabilistic choices in a logic program;
- [PASTA](https://github.com/damianoazzolini/pasta) computes lower and upper
  probabilities for probabilistic answer-set programs under credal semantics;
- [TweetyProject](https://tweetyproject.org/) implements many knowledge
  representation formalisms; the comparisons here use Reiter default logic
  and Defeasible Logic Programming (DeLP);
- [clingo](https://potassco.org/clingo/),
  [DLV](https://www.dlvsystem.it/dlvsite/dlv/), and
  [I-DLV](https://github.com/DeMaCS-UNICAL/I-DLV) evaluate ASP or Datalog
  programs, using stable-model or stratified-query semantics as appropriate;
- [s(CASP)](https://swish.swi-prolog.org/example/scasp.swinb) searches from a
  query and returns a partial stable model with a justification, without
  grounding the complete program first.

Consequently, agreement on one example does not imply equivalent semantics.
The sections below state the cases narrowly and distinguish historical results
from current gk behavior.

The papers *Confidences for Commonsense Reasoning* and *GK: Implementing Full
First Order Default Logic for Commonsense Reasoning* describe earlier CONFER/gk
versions. Their ProbLog and
[Alchemy](https://doi.org/10.1145/1557019.1557025) confidence tables use the
older confidence calculation, which differs from current gk.
This document does not reuse those numbers as current results. Historical ASP
measurements are kept separate from results produced from the current
repository.

## ProbLog

### Comparable one-sided cases

A ProbLog probabilistic fact is an independent Boolean choice. Standard
inference reports the probability that a query succeeds across those choices.
For a finite program with only positive support, gk's current proof-instance
calculation often gives the same number:

- two independent facts with confidences 0.5 and 0.6 supporting one answer give
  `1 - (1 - 0.5)(1 - 0.6) = 0.8`;
- one proof using facts with confidences 0.5 and 0.6 gives `0.5 * 0.6 = 0.3`;
- when proofs share a premise, gk records the ground evidence instances and
  uses that premise once when combining the proofs.

The first two are the usual ProbLog distribution-semantics values as well as
gk's results. The shared-premise cases in
[`../montecarlo/`](../montecarlo/README.md) are compared with independent
possible-world sampling: `overlap1.js` estimates 0.8450 with gk at 0.846, and
`overlap3.js` estimates 0.9596 with gk at 0.959. Both gk values lie inside the
reported 95% sampling intervals. The intervals and commands are in
[`../montecarlo/comparison.md`](../montecarlo/comparison.md).

The agreement is limited to these examples. The sampler supports constants
only, the search must find the relevant proofs, and gk uses exact
inclusion-exclusion only up to 20 reduced proof masks. Above that limit it uses
a deterministic approximation and reports a warning.

### Different treatment of opposing evidence

gk treats a negative literal such as `-flies(a)` as explicit evidence with its
own confidence. If the positive confidence is 0.7 and the negative confidence
is 0.4, gk's detailed result is:

```text
support_for      0.3
support_against  0.0
conflict         0.4
ignorance        0.3
```

This four-part assessment is not a ProbLog success probability. A ProbLog model
can introduce separate positive and negative atoms and rules for reconciling
them, but the result then depends on that encoding. ProbLog does not give gk's
conflict/ignorance report as part of its standard semantics.

Defaults also differ. A gk blocker starts another proof search to determine
whether an exception defeats a candidate proof, and priorities restrict which
defaults may participate in that check. ProbLog's Prolog-style negation and
probabilistic choices do not implement those blocker and priority rules.

### Operations provided by ProbLog

ProbLog's standard tools provide operations that gk does not:

- conditioning a query on positive or negative observations with `evidence`;
- exact inference by knowledge compilation for supported finite problems, and
  sampling-based estimates as an alternative;
- most-probable-explanation and MAP queries;
- learning probabilities from examples;
- annotated disjunctions and decision-theoretic extensions;
- sampling from continuous distributions.

See the official [ProbLog model documentation](https://problog.readthedocs.io/en/latest/modeling_basic.html)
and [command-line modes](https://problog.readthedocs.io/en/latest/cli.html).
gk assigns supplied confidences to proof evidence; it is not a general
probabilistic conditioning or learning system.

## PASTA

PASTA extends ASP with probabilistic facts. Under its credal semantics, each
selection of probabilistic facts can have one or more stable models. The lower
query probability counts selections where the query holds in every stable
model; the upper probability counts selections where it holds in at least one.

Three current repository examples isolate the consequences:

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

### Grounded ASP: clingo and DLV

clingo and DLV ground and solve finite ASP programs. Their languages
provide stable-model enumeration, integrity constraints, choice or disjunctive
rules, aggregates, and optimization facilities. These operations support
scheduling, configuration, and graph problems. gk does not enumerate
stable models and has no corresponding ASP optimization language.

Both systems ground non-ground rules before stable-model search. Function terms
are valid syntax, but positive recursion such as `bird(f(X)) :- bird(X)` needs
infinitely many ground terms. The historical grounders in this repository's
birds example did not finish that input. Large finite transitive closures can
also make grounding expensive.

The official [Potassco guide](https://potassco.org/guide/) documents clingo.
The DLV system page describes DLV's disjunctive logic-programming and
optimization use cases.

### I-DLV: stratified query answering and ASP grounding

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
These timings measure query focus for this stratified program; they do not rank
general ASP performance. The exact inputs, memory figures, command, and
executable hash are in
[`../Examples/asp_comparison/`](../Examples/asp_comparison/README.md).

### Query-directed ASP: s(CASP)

s(CASP) is not a grounding solver. It evaluates a query top-down and can return
a partial stable model and a justification. clingo and DLV instead ground the
complete finite program before stable-model search.

Query-directed execution does not guarantee termination. On the normalized
large input, s(CASP) 1.1.4 follows the left-recursive transitivity rule even
though the query does not depend on it. The bounded runs either reached their
time limit or the Prolog stack limit. These results apply to that encoding and
version. Smaller historical inputs are retained in
[`../Examples/asp_comparison/other_systems/`](../Examples/asp_comparison/other_systems/).

### What the birds benchmark establishes

The current normalized benchmark uses the same facts and rules in each
system's syntax. The systems handle the ancestor closure differently:

- clingo and DLV materialize the ancestor closure before answering
  `flies(b1)`, whose derivation does not use `anc`;
- I-DLV uses Magic Sets to restrict its stratified evaluation to the query;
- s(CASP) encounters deep recursive search while evaluating that closure;
- gk answers `flies(b1)` without materializing the closure.

The measurements characterize this workload, not general performance. The
`flies(b1)` query does not depend on the ancestor closure. Commands, resource
limits, current results, and the separate historical table are documented in
[`../Examples/asp_comparison/README.md`](../Examples/asp_comparison/README.md).

## English-language examples

The repository's [`Examples/language/`](../Examples/language/README.md) are
compiled outputs of the
[llmpipe commonsense-reasoning system](https://github.com/tammet/nlpsolver/tree/main/llmpipe).
llmpipe automatically translates English into gk logic and uses gk as its
reasoning engine. The
[nlformtasks collection](https://github.com/tammet/nlformtasks) provides a
larger set of language-translation examples runnable by gk.

The compiled examples combine several features: first-order variables and
function terms, existential witnesses, explicit negation, disjunction,
contexts, question-answer bridges, defaults, confidence annotations, and a
shared background theory for taxonomy, part-whole relations, degrees, events,
and space. None of the systems compared above accepts this JSON-LD-LOGIC input
and its conventions directly. Individual fragments could be rewritten for
ProbLog, PASTA, TweetyProject, or an ASP system, but such a rewrite would need
to select corresponding semantics for the unsupported features. Its result
would test the hand-written translation as well as the reasoner.

For that reason, this document does not report cross-system runs of these
compiled files. The narrower examples elsewhere in this document compare
features that can be represented without removing material parts of the
input.

## Systems considered but not run

[Fusemate](https://peba62.github.io/systems/) combines possible-model
reasoning, default negation, and a probabilistic extension with query-guided
grounding. Baumgartner's system page and the
[probabilistic Fusemate paper](https://arxiv.org/abs/2308.15862) point to
source distributions on CSIRO's Bitbucket. Those locations now lead to an
authenticated sign-in, direct repository access also requires credentials,
and no public mirror or source archive was found. Without a retrievable
implementation, a current result would not be reproducible, so no Fusemate
numbers are reported.

[XSB](https://xsb.sourceforge.net/about.html) provides tabled logic programming
with well-founded semantics. That includes nonmonotonic negation, but the core
system does not provide probabilistic inference or a dedicated defeasible-rule
formalism with conflict resolution or priorities. Its overlap with this
comparison would therefore be ordinary logic-program negation already covered
by the ASP systems, so XSB was not added.

## Capability summary

| Question | gk | ProbLog | PASTA | TweetyProject modules compared here | clingo / DLV | I-DLV | s(CASP) |
|---|---|---|---|---|---|---|---|
| Primary result | first-order query proof and assessment | query probability | lower and upper query probability | default extensions or DeLP query status | stable models | stratified query answers or a ground ASP program | query-directed partial stable model |
| Numeric uncertainty | proof confidences and four-part assessment | distribution-semantics probability | credal probability interval | none in the two compared modules | none in the base systems | none | none in the base system |
| Exceptions and conflict | blockers, priorities, opposing evidence | encoding-dependent | stable-model variation | Reiter justifications or dialectical arguments | negation as failure | stratified negation or stable models with a solver | negation as failure |
| Query focus | yes | finite proof/formula construction | finite grounding and model analysis | library algorithm depends on the formalism | complete grounding | Magic Sets for stratified queries | top-down evaluation |
| Multiple alternatives | proof alternatives combine into an assessment | summed possible worlds | lower/upper bounds over stable models | extensions or competing arguments | stable-model enumeration | solver-dependent outside stratified mode | query-relevant partial models |
| Evidence conditioning or learning | no | yes | conditioning and additional inference modes | separate TweetyProject modules, not these two | no | no | no |
| Explanation object | gk proof | explanation modes | stable models and probability bounds | extensions or dialectical arguments | models; further tooling is needed for proof-style explanations | query answers or ground rules | justification tree |

The table describes the named systems or modules. Capability entries are
qualified when they depend on termination or an encoding choice. For gk's own
algorithms, see
[`how_gk_works.md`](how_gk_works.md).
