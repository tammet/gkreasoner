# How GK Works

GK combines a first-order resolution prover with confidence annotations and
defeasible rules. The prover constructs ordinary logical derivations. A
separate assessment stage examines the evidence used by those derivations,
checks exceptions, combines alternative proofs, and compares positive and
negative evidence.

## 1. From input to answers

All supported input notations are converted to GK's internal clausal form.
Rules are therefore available to the same resolution procedure regardless of
whether they were written in GKP, JSON-LD-LOGIC, GKS, or TPTP.

A query with variables is converted to an answer clause. A proof of
`grandfather(john, mark)`, for example, derives `$ans(mark)` and returns `mark`
as the substitution. A ground query returns `true` when the query is proved
and `false` when its negation is proved. If neither polarity is proved, the
result is `no information`.

Resolution is refutational. The prover combines clauses whose complementary
literals unify, applies the resulting substitution, and continues until it
derives an answer or contradiction clause. Simplification, equality reasoning,
rewriting, and arithmetic evaluation are applied when enabled by the problem
and strategy.

The proof printed with an answer records the input clauses and inference steps.
Common step labels are:

| Label | Meaning |
|---|---|
| `in` | input clause |
| `goal` | clause generated from the query |
| `mp` | resolution or multi-premise resolution |
| `simp` | simplification |
| `cumul` | combination of alternative proofs |
| `arithinst` | bounded arithmetic instantiation |

## 2. Confidence annotations

An input confidence is a value between 0 and 1. In the scrutiny
model used by GK, it is interpreted as the probability that the item of
evidence survives a test. It is not a learned statistical parameter and need
not be a calibrated probability that the formula is objectively true.

An unannotated statement has confidence 1. In GKP:

```prolog
0.8::bird(tweety).
flies(X) :- bird(X).
```

The confidence belongs to a ground use of the input clause. Two uses of the
same rule with different substitutions count as different evidence instances.
Repeated use of the same ground instance within one proof counts once.

When one annotated formula is clausified into several clauses, the confidence
is divided by taking an appropriate root. If a formula of confidence `P`
becomes `N` clauses, each clause receives `P^(1/N)`. This preserves confidence
`P` for a proof that requires all `N` clauses. The distinction matters mainly
for non-clausal formulas such as equivalences.

## 3. One proof

The confidence of one proof is the product of the confidences of its distinct
evidence instances. Consider:

```prolog
0.5::p(heads1).
0.6::p(heads2).
r(c) :- p(heads1), p(heads2).
query(r(X)).
```

The only proof uses both uncertain facts and a rule of confidence 1:

```text
0.5 * 0.6 * 1 = 0.3
```

This calculation is performed from reconstructed proof histories. If an
instance cannot be reconstructed, GK retains the conservative product already
stored on the inference steps.

## 4. Several proofs of the same answer

Alternative proofs may be independent, identical, nested, or partly
overlapping. Treating every proof as independent would count shared facts and
rules more than once.

GK records the evidence-instance set for each proof and combines the sets by
inclusion-exclusion:

- identical support sets are idempotent;
- if one set contains another, the stronger proof determines the result;
- disjoint sets combine by noisy-or;
- partial overlap produces a value between those cases.

For two disjoint proofs with confidences `a` and `b`, noisy-or gives:

```text
1 - (1 - a)(1 - b)
```

Thus two independent facts of confidence `0.5` and `0.6` supporting the same
answer combine to `0.8`. The `overlap*.js` examples show why the proof supports
are required; final proof confidences alone are insufficient.

Exact inclusion-exclusion is used for up to 20 reduced proof masks. Above that
limit GK uses a deterministic greedy fold and prints a warning. This bounds the
cost of combining a large number of proofs.

The normal combiner measures overlap directly. In a strategy file,
`independence: 0` disables combination and retains the best proof. Any nonzero
value enables the normal exact combiner. Intermediate percentages affect only
the older heuristic selected with `-oldcumulate`.

## 5. Positive and negative evidence

GK searches separately for proofs of a conclusion and its explicit negation.
Suppose the pooled positive confidence is `a` and the pooled negative confidence is
`b`. The basic four-part division is:

```text
support_for     = max(a - b, 0)
support_against = max(b - a, 0)
conflict        = min(a, b)
ignorance       = 1 - max(a, b)
```

The four values sum to 1. With `0.7::flies(a)` and `0.4::-flies(a)`, they are:

```text
support_for      0.3
support_against  0.0
conflict         0.4
ignorance        0.3
```

This division follows from a shared scrutiny threshold for each ground atom.
Below both evidence confidences, the two sides conflict and neither is usable.
Between the confidences, only the side with higher confidence is usable. Above
both confidences, neither side is usable.

For conclusions reached through rules, assessment proceeds from conditions to
conclusions. A rule contributes evidence only in the worlds in which its body
is usable and its blockers do not fire. Shared contested ancestors are treated
jointly where the bounded evaluator can enumerate them. If structural
assessment is incomplete, GK preserves the proof-derived assessment and marks
the report with fallback flags rather than discarding a proof.

The ordinary `confidence` field is retained for compact output and threshold
compatibility. It is the magnitude of the dominant support margin; ties are
reported as zero. The answer is routed as accepted or rejected according to
the dominant polarity. `-detail` adds the four masses, conflict sources, and
flags.

The optional `-envelope` report varies the resolution of identified conflicts
and returns minimum and maximum support. It is a sensitivity interval, not a
probability interval. `-stake F` compares that interval with a decision
threshold and reports `ACCEPT`, `DEFER`, or `REJECT`.

## 6. Defaults and blockers

A default rule has an exception condition. In GKP:

```prolog
flies(X) :- bird(X), unless(-flies(X), 2).
```

The rule first derives a candidate conclusion containing a blocker. GK then
starts a bounded subsidiary proof search for the blocking condition. The
candidate survives when no blocking argument with sufficient priority is found.
The blocker is retained in the printed proof, so the defeasible assumption is
visible.

Blockers have priorities. A blocking proof may itself depend on defaults, and
priorities prevent a lower-priority default from defeating a higher-priority
one. Priorities may be numbers or taxonomy terms such as `tax(penguin)`. Taxonomy terms require
`-defaults` and the two auxiliary taxonomy files.

Opposed defaults need not have a forced winner. In the Nixon diamond,

```prolog
pacifist(X)  :- quaker(X),     unless(-pacifist(X), 1).
-pacifist(X) :- republican(X), unless(pacifist(X), 1).
```

equal-priority arguments support both polarities. GK reports the contest and a
zero margin rather than choosing one conclusion by rule order.

## 7. Arithmetic

Ground arithmetic is simplified during proof search. For example, `2 + 3` is
evaluated to `5` when all operands are known.

Arithmetic conditions containing variables require bounded instantiation.
With `arith_instantiation: 1`, GK considers selected one-variable conditions;
mode `2` also considers selected conditions with two variables. Candidate and
probe limits keep the procedure finite. It is intended for small integer
problems and is not a general constraint solver.

## 8. Search control

Resolution is complete only when it runs without restrictive strategy limits.
Practical searches use time, clause-size, and selection controls. GK generates
an automatic strategy from the input: a short ladder of candidate strategies
with no-proof give-up times, where the first strategy that proves something
keeps the remaining budget and is reused for the query's later searches (see
[`strategy_reference.md`](strategy_reference.md)). A strategy file can instead
specify:

- clause selection preferences such as `negative_pref` or `query_focus`;
- goal, assumption, and axiom queue treatment;
- limits on time, answers, clause size, depth, length, and weight;
- equality, rewriting, and SINE relevance filtering;
- several runs attempted in sequence.

Unit resolution and other short-argument restrictions can be fast but are
incomplete. A timeout or a restrictive strategy therefore means only that no
proof was found under those limits.

## 9. Relation to other approaches

### Classical first-order provers

GK uses the resolution, equality, and term machinery of a classical prover,
but adds explicit confidence and blocker semantics. Positive and negative
proofs are retained as separate evidence instead of reducing an inconsistent
answer to a single Boolean result.

### Probabilistic logic programming

For one-sided, disjoint evidence, GK's products and noisy-or combinations often
match probabilistic logic-programming calculations. The general semantics are
different: GK measures overlap between proof-instance sets, treats classical
negative literals as evidence, and reports conflict and ignorance separately.
Default blockers are proof searches, not negation as failure.

### Answer set programming

Answer set programs normally obtain defaults through nonmonotonic model
semantics and negation as failure. GK instead derives first-order proofs and
checks explicit blocker conditions. Function terms, equality, and confidence
annotations remain part of the same proof process.

### Bayesian networks and Markov logic

GK does not learn weights or construct a complete joint distribution over the
knowledge base. Its annotations are supplied with individual facts and rules,
and answer assessment is derived from the resulting proofs. The confidence
calculation uses proof provenance.

## 10. Result states

Common result strings are:

| Result | Meaning |
|---|---|
| `answer found` | at least one answer met the confidence threshold |
| `evidence below limit` | a derivation was found but its margin was below `-confidence` |
| `no answers found` | no substitution was found for an open query |
| `no information` | neither polarity of a ground query was proved |
| `time limit, proof not found` | the search time expired before finding a proof |

The command-line options are listed in [`cli_reference.md`](cli_reference.md).
Input examples are in [`input_languages.md`](input_languages.md), and runnable
algorithm examples are indexed by [`../Examples/README.md`](../Examples/README.md).
