# Monte Carlo interpretations of GK weights and results

This directory contains two sampling calculations for small GK examples. They
give each reported confidence value a concrete meaning. Their estimates can be
compared with GK's results without reusing GK's support arithmetic.

The calculations are diagnostic tools, not alternative theorem provers. The
clause-activation calculation repeatedly calls gk as an unweighted prover. The
shared-threshold calculation evaluates a restricted, directional clause model
in [Python 3](https://www.python.org/). Both are limited to finite inputs without
function terms.

Run the commands below from the repository root. The scripts require Python 3
and the shipped `bin/gk`; they use only the Python standard library.

## Sampling modes

The two modes test different readings. They agree on many simple examples but
need not agree on recursive rules, contested premises, or defaults.

### Clause-activation sampling: random Boolean programs

The clause-activation sampler independently activates uncertain ground clause
instances and invokes the unweighted prover in each sampled world. In this mode
an input weight `c` is treated as an activation probability. For each trial:

1. gk clausifies the input.
2. The script grounds the clauses over the constants in the file.
3. Each uncertain ground clause is retained with probability `c` and otherwise
   removed. Certain clauses are always retained.
4. The retained clauses, without their input weights, form one Boolean program.
5. gk checks whether the query and its explicit negation are provable in that
   program.

For an answer `A`, the reported estimate is

```text
P(A is provable) - P(-A is provable).
```

The two probabilities are measured in the same sampled worlds. A world in
which both polarities are provable contributes zero to the difference. This permits
contradictory worlds; it is not conditioning on consistent worlds.

This construction is close to the usual independent-fact reading used by
[ProbLog](https://dtai.cs.kuleuven.be/problog/editor.html) when
the program contains independent facts and definite rules. A shared uncertain
premise is drawn once per world, so proofs that use it are correlated. Explicit
support for explicit negation and defaults add behavior that is not a standard
ProbLog query probability.

Run a clause-activation calculation as follows:

```sh
montecarlo/gkmc.py -n 10000 --seed 1 Examples/confidences/cumulate.js
```

`cumulate.js` contains two independent sources, 0.5 and 0.6, for `bird(a)`.
The exact probability is

```text
1 - (1 - 0.5)(1 - 0.6) = 0.8.
```

A representative run gives:

```text
| answer | MC pos | MC neg | MC pos-neg | 95% CI | gk exact |
| yes    | 0.8013 | 0.0000 | 0.8013     | [0.7935, 0.8091] | 0.8 |
```

The columns mean:

- `MC pos`: fraction of valid trials in which the answer is provable;
- `MC neg`: fraction in which its explicit negation is provable;
- `MC pos-neg`: their paired difference;
- `95% CI`: sampling interval for that difference;
- `gk exact`: the number from one ordinary gk run on the original file.

Open queries are supported. The script first discovers answer bindings and
then checks each closed answer and its closed negation in the same worlds. This
extra pass avoids losing a binding when an open query is simplified in a
contradictory world.

By default, separate ground instances of an uncertain rule receive separate
draws. `--draws shared` instead gives all instances originating from one input
statement the same draw. The choice matters for rules with variables and
should be stated with any result.

### Shared-threshold sampling: the four-component report

Shared-threshold mode, run by the threshold-world sampler, estimates GK's
four-component report:

```text
support_for, support_against, conflict, ignorance.
```

Suppose the aggregated positive support for one ground atom is `a`, and the
aggregated negative support is `b`. The script draws two independent uniforms
from 0 to 1 for each ground atom.
For ordinary opposition only the first draw `U` is used, as one shared uniform
threshold for both polarities:

| Condition | Outcome |
|---|---|
| `b < U <= a` | positive support |
| `a < U <= b` | negative support |
| `U <= min(a,b)` | conflict |
| `U > max(a,b)` | ignorance |

When the input contains only positive and negative facts for the queried atom,
this gives the four values exactly in the limit:

```text
support_for     = max(a - b, 0)
support_against = max(b - a, 0)
conflict        = min(a, b)
ignorance       = 1 - max(a, b)
```

Same-polarity evidence strengths are combined by noisy-or. Rules become
available only when their body atoms are available in the required polarity.
A blocker check disables a rule when its exception condition is supported.
Each ground atom has one fixed pair of draws per trial, so two downstream proofs that
depend on the same atom remain correlated.

Opposition involving defaults uses both draws, following GK's defined local
combination rules: with equal explicit ranks, each polarity fires on its own
threshold and survives only if the other misses (mutual blocking); with unequal
ranks, the higher-ranked default takes the overlap region of the shared
threshold (the strict-priority override); when only one polarity is supported
by a default with an exception condition, the two outcome regions are exclusive
and no conflict component arises. The second, independent threshold is what
makes a product such as `a * (1 - b)` expressible; a single shared threshold
cannot produce it.

Atoms are evaluated in dependency order. A cycle containing only
single-polarity positive dependencies is evaluated by a least fixpoint in each
trial. A blocker cycle that runs through the queried atom is resolved credulously for
the query, matching gk's blocker check (the query is evaluated first with the
in-cycle blockers against it voided, then the rest reach a fixpoint). Any
other cycle through a blocker or a contested atom is reported as
`not scored`, because the small model does not define a reliable outcome for
it.

Run a shared-threshold calculation as follows:

```sh
montecarlo/gkmc.py --semantics threshold -n 10000 --seed 1 \
  Examples/confidences/net_direct.js
```

`net_direct.js` has positive evidence strength 0.7 for `flies(a)` and negative
evidence strength 0.4 for its negation. With 10,000 draws the sampler returned
0.3018 positive support, 0 negative support, 0.3984 conflict, and 0.2998
ignorance. GK reports 0.3, 0, 0.4, and 0.3.

Shared-threshold mode does not call GK. It supports a smaller input fragment
than clause-activation mode: a single predicate query — ground, or open, in which
case each closed instance over the named constants is evaluated separately —
and directional clauses whose final ordinary literal is
the conclusion. It reports function terms, arithmetic and other built-ins,
equality, compact formula connectives, ambiguous clauses with several positive
literals, and taxonomy-valued blocker priorities as unsupported.

## Differences

Agreement is expected when both calculations use the same independence and
dependency structure. It supports the stated interpretation for that example.
When the numbers differ persistently, that indicates an implementation or
semantic discrepancy. The cases below are known semantic differences, and the
shape of each difference identifies which modelling decision the example turns
on. The uncertain-exception case is included because it clearly shows the
world split shared by all three calculations.

The one-sentence summary of each reading:

- **GK evaluates argument support.** It builds the best derivation for an
  answer and the best derivation for its negation, then reports the support
  that remains after opposition resolution. Opposing support on contested
  premises is resolved before the premises are used.
- **Clause-activation sampling counts ground-instance activation worlds.**
  Each uncertain ground clause is independently present or absent
  (with `--draws shared`, per input statement instead); a world is counted for
  an answer when the answer is provable in it, and for the negation when its
  explicit negation is provable.
- **Shared-threshold sampling counts worlds with per-atom thresholds.**
  Evidence counts when its pooled strength clears a threshold. Ordinary
  opposition about one atom faces one shared threshold (gk's opposition
  resolution); when the negated conclusion is also a default's exception
  condition, the default and support for that condition interact through the
  atom's two independent thresholds (GK's local default-combination rules).

The third reading is, on its documented fragment, a sampling semantics for
gk's own arithmetic: gk's four-component formulas are exactly the probabilities
of the corresponding threshold events, chaining corresponds to
independent draws for distinct atoms, and the shared threshold reproduces both
the opposition resolution on contested atoms and the decision not to
double-count shared support. That is why the shared-threshold table in
[`comparison.md`](comparison.md) tracks gk to sampling precision while
clause-activation sampling deviates exactly where independent statement activation
and gk's opposition resolution part ways.

### A default with an uncertain exception condition

[`bird_exception.js`](../Examples/exceptions/bird_exception.js): two birds,
birds fly by default, and evidence at 0.9 that `a` does not fly.

```text
gk (query flies(X)):        b accepted at 1.0; a rejected at 0.8
                            detail for a: support_for 0.1,
                            support_against 0.9
clause-activation sampling: provable 0.10, negation provable 0.90,
                            difference -0.80
```

All columns rest on the same split: in nine worlds of ten, support for the
exception condition is active and makes `-flies(a)` itself provable; in one
world of ten the flying default stands. GK's signed result for `a` is -0.8, matching the
sampled difference, and its 0.1 positive support equals the sampled positive
column.

### A contested premise

[`net_premise.js`](../Examples/confidences/net_premise.js): `bird(a)` at
0.5, `-bird(a)` at 0.2, and birds fly at 0.9.

```text
gk:                          0.27   (resolves the opposition on the premise:
                                     (0.5 - 0.2) * 0.9)
clause-activation sampling:  0.45   (0.5 * 0.9; support for the explicit
                                     negation does not reach the query)
shared-threshold sampling:   0.27   (bird usable iff 0.2 < U <= 0.5, i.e. 0.3)
```

Here the clause-activation and shared-threshold readings split. Under one
independent activation decision per statement,
`-bird(a)` never makes `-flies(a)` derivable, so it changes nothing: the
positive premise is provable in half of the worlds — including worlds where
its negation is provable alongside it — and the rule fires in 0.9 of those.
Under one shared threshold, the two bird statements are evaluated against the
same draw: only the margin `0.2 < U <= 0.5` leaves the premise usable, and
GK's subtraction is the closed form of exactly that. In GK's dependency-aware
evaluation, doubt about a premise reduces every conclusion built on it,
whether or not the doubt can be propagated to the conclusion's negation.

### A recursive rule

[`near.js`](../Examples/confidences/near.js): a chain of nine certain
`near` links and a transitivity rule at 0.9.

```text
gk:                  0.4305   (0.9^8: eight applications of the rule)
shared-threshold sampling: 1.0000 (recorded; a draw counts if any
                               decomposition works, and clause-activation
                               sampling behaves alike)
```

The difference is a third dependence convention, and GK's calculation is
exact and stable (the same 0.4305 under different time limits and search
strategies). Within one derivation GK multiplies a rule's strength once
per application — eight uses of the one transitivity statement give
0.9^8 — and across derivations it combines with inclusion–exclusion at
the level of input statements, so the many alternative decompositions of
the chain, all standing on the same statement, add nothing. The samplers
instead activate each ground instance of the rule independently, under which
almost every sampled world assembles the chain some
way. Neither convention is derivable from the other; a provenance-aware
evaluator extended with statement-level bookkeeping would reproduce GK's
number, while a plain clause-activation count cannot express per-use multiplication.

### Defaults and priorities

Evidence usability after clause activation is decided by GK's default and
priority machinery. The threshold-world sampler implements the defined local
combination rules for defaults and
opposing evidence — exception conditions, equal-rank mutual blocking, the
strict-priority override, and blocker cycles through the queried atom. On the
remaining priority encodings, such as taxonomy-valued priorities
and multi-level default structures, the samplers report the case as unsupported
(`not scored`) or annotate rather than guess; those unsupported cases mark the
constructs for which a defined world-counting account of GK's behavior is not
available.

### Why GK does not simply adopt the clause-activation numbers

Three reasons, in increasing order of weight. First, cost: the
clause-activation answer is a count over all combinations of the uncertain
statements, and the number of combinations doubles with every statement —
that is why this directory samples instead of counting, needs thousands of
proof searches per estimate, and still returns numbers with sampling noise,
while GK's arithmetic is deterministic and costs almost nothing per proof.
Second, coverage: GK answers on inputs the samplers do not support (function
terms, equality, arithmetic, taxonomy priorities). Third, and decisively, the
clause-activation reading is not uniformly better: on `net_premise.js` it does
not propagate negative support on the premise to the conclusion. The
shared-threshold model shows that GK's numbers already have a world-based
semantics of their own on a well-defined fragment; the two samplers are
kept as independent checks precisely because their disagreements carry
information.

The detailed results and the coverage status of every example directory are in
[`comparison.md`](comparison.md). A three-way table over the 23 examples of
the public logictools.org uncertainty page — gk against both samplers, with a
reason for every unsupported case — is in
[`uncertainty_page_comparison.md`](uncertainty_page_comparison.md).

## Reference checks

`settlement_checks/` holds ground-query probes for the defaults family — the
uncertain and certain exception, the
equal-rank mutual blocking, the strict-priority override, a default opposed by
ordinary evidence, the rank-restricted check in both directions, and the
negated query — with `expected.tsv` recording the four components of native
GK. The threshold-world sampler reproduces all ten:

```sh
montecarlo/gkmc.py --semantics threshold -n 100000 --seed 1 \
  --check montecarlo/settlement_checks montecarlo/settlement_checks/sc_exc09.js
```

The shared-threshold core mirrors the hand-derived reference arithmetic (each atom
draws two independent uniforms; ordinary opposition keeps the shared-threshold
subtraction, defaults with exception conditions take the exclusive treatment
for a default opposed by ordinary support, the symmetric equal-rank treatment,
or the strict-priority treatment), open queries are evaluated per closed
instance, and a blocker cycle through the query atom resolves
credulously for the query, as gk's blocker check does. Loop cases need an
adequate `-seconds` budget on the gk side: with the default budget the
check-of-check may not complete, and gk then reports ignorance for the loop.

## Other modes

`--semantics provable` reports only `P(A is provable)`.

`--semantics gkdefault` samples the same Boolean worlds but runs GK's default
acceptance calculation on each closed answer. It estimates how often gk would
accept that answer in a sampled world; it is not the four-component threshold
model.

For a ground, single-literal query, `--classify` prints four world frequencies:

```text
A only, -A only, both, neither.
```

This is useful for seeing the information hidden by the signed difference.

## Options and reproducibility

```text
montecarlo/gkmc.py [-n TRIALS] [--seed SEED]
                   [--draws per-instance|shared]
                   [--semantics subtract|provable|gkdefault|threshold]
                   [--classify] [--jobs N] [--gk PATH]
                   [--gk-args "..."] [--gk-timeout SECONDS]
                   [--max-ground N] [--keep-worlds DIR]
                   [--json FILE] input.js
```

- The default is 10,000 trials. State the count and seed with every result.
- `--seed` makes the sampled worlds repeatable.
- `--jobs` controls concurrent gk calls in clause-activation mode.
- `--gk` defaults to the repository's `bin/gk`.
- `--gk-timeout` applies to each Boolean world, not to the complete run.
- `--max-ground` stops grounding when it reaches the configured limit.
- `--keep-worlds` retains generated Boolean inputs for inspection.
- `--json` writes the clause-activation result in machine-readable form.

At 10,000 trials, the largest approximate 95% half-width for one sampled
proportion is about 0.01. Smaller differences require more trials.
Clause-activation mode can be slow because subtraction normally requires at
least two GK runs per world. Shared-threshold mode performs its trials in one
Python process and is much faster.

## Input limits

- The command-line input must be a JSON-LD-LOGIC `.js` file. Equivalent `.gkp`,
  `.gks`, TPTP, ASP, and Prolog files are outside these scripts.
- Both modes require a finite constant domain and reject nested function terms.
- Clause-activation mode obtains clauses from GK and does not continue when it
  cannot map the clauses back to input weights safely.
- Shared-threshold mode has the narrower clause and query restrictions described
  above. It reports unresolved cyclic or priority cases instead of guessing.
- Neither mode performs probabilistic conditioning on evidence or learning.
