# Monte Carlo interpretation of gk confidences

This directory contains two sampling calculations for small gk examples. They
give each confidence result a concrete meaning. Their estimates can be compared
with gk's results without reusing gk's confidence arithmetic.

The calculations are diagnostic tools, not alternative theorem provers. The
inclusion calculation repeatedly calls gk as a Boolean proof oracle. The
threshold calculation evaluates a restricted, directional clause model in
[Python 3](https://www.python.org/). Both are limited to finite inputs without
function terms.

Run the commands below from the repository root. The scripts require Python 3
and the shipped `bin/gk`; they use only the Python standard library.

## Sampling modes

The two modes test different readings. They agree on many simple examples but
need not agree on recursive rules, contested premises, or defaults.

### Inclusion sampling: random Boolean programs

In this mode a confidence `c` is treated as an inclusion probability.
For each trial:

1. gk clausifies the input.
2. The script grounds the clauses over the constants in the file.
3. Each uncertain ground clause is retained with probability `c` and otherwise
   removed. Certain clauses are always retained.
4. The retained clauses, without confidence annotations, form one Boolean
   program.
5. gk checks whether the query and its explicit negation are provable in that
   program.

For an answer `A`, the reported estimate is

```text
P(A is provable) - P(-A is provable).
```

The two probabilities are measured in the same sampled worlds. A world in
which both sides are provable contributes zero to the difference. This permits
contradictory worlds; it is not conditioning on consistent worlds.

This construction is close to the usual independent-fact reading used by
[ProbLog](https://dtai.cs.kuleuven.be/problog/editor.html) when
the program contains independent facts and definite rules. A shared uncertain
premise is drawn once per world, so proofs that use it are correlated. Explicit
negative evidence and defaults add behavior that is not a standard ProbLog
query probability.

Run an inclusion calculation as follows:

```sh
montecarlo/gkmc.py -n 10000 --seed 1 Examples/confidences/cumulate.js
```

`cumulate.js` contains two independent sources, 0.5 and 0.6, for `bird(a)`.
The exact inclusion probability is

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

### Threshold sampling: four outcome masses

Threshold mode estimates gk's four-part report:

```text
support_for, support_against, conflict, ignorance.
```

Suppose the pooled confidence of the positive evidence for one ground atom is
`a`, and the pooled confidence of the negative evidence is `b`. The script
draws two independent uniforms from 0 to 1 for each ground atom (revised
2026-07-21 together with the gk 1.0.4 settlement; earlier versions drew one).
For plain opposed evidence only the first draw `U` is used, as one shared
acceptance bar for both sides:

| Condition | Outcome |
|---|---|
| `b < U <= a` | support for |
| `a < U <= b` | support against |
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

Multiple testimonies on one side are combined by noisy-or. Rules become
available only when their body atoms are available in the required polarity.
A blocker disables a rule when the blocking atom is available. Each ground
atom has one fixed pair of draws per trial, so two downstream proofs that
depend on the same atom remain correlated.

Contests involving defaults use both draws, following gk's settled arithmetic
(the settlement section below): with equal explicit ranks on both sides, each
side fires on its own bar and survives only if the other missed (the symmetric
gate); with unequal ranks, the higher-ranked side takes the overlap region of
the shared bar (the priority award); when only one side is a gated default,
the two outcome regions are exclusive and no conflict mass arises. The second,
independent bar is what makes a product such as `a * (1 - b)` expressible; a
single shared bar cannot produce it.

Atoms are evaluated in dependency order. A cycle containing only one-sided,
positive dependencies is evaluated by a least fixpoint in each trial. A
blocker cycle that runs through the queried atom is resolved credulously for
the query, matching gk's blocker check (the query is evaluated first with the
in-cycle blockers against it voided, then the rest reach a fixpoint). Any
other cycle through a blocker or a contested atom is reported as
`not scored`, because the small model does not define a reliable outcome for
it.

Run a threshold calculation as follows:

```sh
montecarlo/gkmc.py --semantics threshold -n 10000 --seed 1 \
  Examples/confidences/net_direct.js
```

`net_direct.js` has evidence 0.7 for `flies(a)` and 0.4 against it. With 10,000
draws the sampler returned 0.3018 support for, 0 support against, 0.3984
conflict, and 0.2998 ignorance. gk reports 0.3, 0, 0.4, and 0.3.

Threshold mode does not call gk. It accepts a smaller input fragment than
inclusion mode: a single predicate query — ground, or open, in which case each
closed instance over the named constants is evaluated separately (added
2026-07-21) — and directional clauses whose final ordinary literal is the
conclusion. It rejects function terms, arithmetic and
other built-ins, equality, compact formula connectives, ambiguous clauses with
several positive literals, and taxonomy-valued blocker priorities.

## Differences

Agreement is expected when both calculations use the same independence and
dependency structure. It supports the stated interpretation for that example.
When the numbers differ, neither is a mistake: the calculations answer
different questions, and the shape of a disagreement identifies which
modelling decision the example turns on. This section works through the
known sources of difference on concrete examples. One former difference
family — the default with an uncertain exception — became an agreement with
the gk 1.0.4 fix of 2026-07-21; it is kept first because the reconciliation
shows the scenario split all three calculations share.

The one-sentence summary of each reading:

- **gk weighs arguments.** It builds the best derivation for an answer and
  the best derivation against it, and reports what remains of the support
  once the opposition is subtracted, netting contested premises before they
  are used.
- **Inclusion sampling counts scenarios with one coin per ground clause.**
  Each uncertain ground clause is independently present or absent (with
  `--draws shared`, per input statement instead); a world is counted for an
  answer when the answer is provable in it, and against when its explicit
  negation is provable.
- **Threshold sampling counts scenarios with per-atom acceptance bars.**
  Evidence counts when its pooled strength clears a bar. Plain opposed
  evidence about one atom faces one shared bar (gk's netting); a default and
  its counter-evidence gate each other through the atom's two independent
  bars (gk's settled defaults arithmetic).

The third reading is, on its documented fragment, a sampling semantics for
gk's own arithmetic: gk's four-mass formulas are exactly the probabilities
of the corresponding bar events, chaining corresponds to
independent draws for distinct atoms, and the shared bar reproduces both
the netting of contested atoms and the refusal to double-count shared
support. That is why the threshold table in [`comparison.md`](comparison.md)
tracks gk to sampling precision while inclusion sampling deviates exactly
where a coin-per-statement reading and gk's netting part ways.

### A default with an uncertain exception (agreement since gk 1.0.4)

[`bird_exception.js`](../Examples/exceptions/bird_exception.js): two birds,
birds fly by default, and evidence at 0.9 that `a` does not fly.

```text
gk 1.0.4 (query flies(X)):  b accepted at 1.0; a rejected at 0.8
                            detail for a: support_for 0.1,
                            support_against 0.9
inclusion sampling:         provable 0.10, negation provable 0.90,
                            net -0.80
```

All columns rest on the same split: in nine worlds of ten the contrary
evidence exists and makes `-flies(a)` itself provable; in one world of ten
the flying default stands. gk's signed result for `a` is -0.8, matching the
sampled net, and its 0.1 support-for equals the sampled positive column.

Before gk 1.0.4 this family was a difference: gk printed `a` at 0.1 with the
0.9 filed under `conflict`. That report came from a defect — the negated
query was counted as evidence inside the blocker assessment, which erased
the support-against mass — and was fixed on 2026-07-21. The `bin/gk`
binary currently shipped in this repository predates the fix and still
prints the old report until the next binary refresh.

### A contested premise

[`net_premise.js`](../Examples/confidences/net_premise.js): `bird(a)` at
0.5, `-bird(a)` at 0.2, and birds fly at 0.9.

```text
gk:                  0.27   (nets the premise: (0.5 - 0.2) * 0.9)
inclusion sampling:  0.45   (0.5 * 0.9; the negative evidence is invisible)
threshold sampling:  0.27   (bird usable iff 0.2 < U <= 0.5, i.e. 0.3)
```

Here the coin and bar readings split. Under one coin per statement,
`-bird(a)` never makes `-flies(a)` derivable, so it changes nothing: the
positive premise is provable in half of the worlds — including worlds where
its negation is provable alongside it — and the rule fires in 0.9 of those.
Under one shared bar, the two bird statements compete for the same
threshold: only the margin `0.2 < U <= 0.5` leaves the premise usable, and
gk's netting is the closed form of exactly that. gk is the more cautious
reading: doubt about a premise reduces every conclusion built on it, whether
or not the doubt can be propagated to the conclusion's negation.

### A recursive rule

[`near.js`](../Examples/confidences/near.js): a chain of nine certain
`near` links and a transitivity rule at 0.9.

```text
gk:                  0.4305   (0.9^8: eight applications of the rule)
threshold sampling:  1.0000   (recorded; a draw counts if any
                               decomposition works, and inclusion
                               sampling behaves alike)
```

The difference is a third dependence convention, and gk's side of it is
exact and stable (the same 0.4305 under different time limits and search
strategies). Within one derivation gk multiplies a rule's confidence once
per application — eight uses of the one transitivity statement give
0.9^8 — and across derivations it combines with inclusion–exclusion at
the level of input statements, so the many alternative decompositions of
the chain, all standing on the same statement, add nothing. The samplers
instead draw each ground instance of the rule once (one coin per ground
clause), under which almost every sampled world assembles the chain some
way. Neither convention is derivable from the other; a threshold-style
evaluator extended with statement-level bookkeeping would reproduce gk's
number, while a plain world count cannot express per-use multiplication.

### Defaults and priorities

Evidence usability after clause inclusion is decided by gk's default and
priority machinery. Since the settlement of 2026-07-21 the threshold sampler
implements the settled defaults family — the exception gates, the equal-rank
symmetric contest, the priority award, and blocker cycles through the queried
atom. On the remaining priority encodings, such as taxonomy-valued priorities
and multi-level default structures, the samplers decline (`not scored`) or
annotate rather than guess; those refusals mark the constructs for which a
clean world-counting story of gk's behavior has not been settled.

### Why gk does not simply adopt the inclusion numbers

Three reasons, in increasing order of weight. First, cost: the inclusion
answer is a count over all combinations of the uncertain statements, and
the number of combinations doubles with every statement — that is why this
directory samples instead of counting, needs thousands of proof searches
per estimate, and still returns numbers with sampling noise, while gk's
arithmetic is deterministic and costs almost nothing per proof. Second,
coverage: gk answers on inputs the samplers refuse (function terms,
equality, arithmetic, taxonomy priorities). Third, and decisively, the
inclusion reading is not uniformly better: on `net_premise.js` it ignores
counter-evidence entirely, which is rarely what a knowledge author wants.
The threshold model shows that gk's numbers already have a scenario
semantics of their own on a well-defined fragment; the two samplers are
kept as independent checks precisely because their disagreements carry
information.

The detailed results and the coverage status of every example directory are in
[`comparison.md`](comparison.md). A three-way table over the 23 examples of
the public logictools.org uncertainty page — gk against both samplers, with
refusal reasons — is in
[`uncertainty_page_comparison.md`](uncertainty_page_comparison.md).

## The settlement cells (2026-07-21)

`settlement_checks/` holds ground-query probes for the defaults family
settled by the gk 1.0.4 fixes -- the uncertain and certain exception, the
equal-rank symmetric contest, the priority award, a default against plain
evidence, the rank-restricted check in both directions, and the negated
query -- with `expected.tsv` recording the four masses of the fixed native
gk. The threshold sampler reproduces all ten:

```sh
montecarlo/gkmc.py --semantics threshold -n 100000 --seed 1 \
  --check montecarlo/settlement_checks montecarlo/settlement_checks/sc_exc09.js
```

The threshold core mirrors the adjudicated arithmetic (each atom draws two
independent uniforms; plain contests keep the shared-bar netting, gated
defaults take the exclusive one-sided, symmetric equal-rank, or
priority-award treatment), open queries are evaluated per closed instance,
and a blocker cycle through the query atom resolves credulously for the
query, as gk's blocker check does. Loop cases need an adequate `-seconds`
budget on the gk side: with the default budget the check-of-check may not
complete, and gk then reports ignorance for the loop.

## Other modes

`--semantics provable` reports only `P(A is provable)`.

`--semantics gkdefault` samples the same Boolean worlds but runs gk's default
acceptance calculation on each closed answer. It estimates how often gk would
accept that answer in a sampled world; it is not the four-mass threshold model.

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
- `--jobs` controls concurrent gk calls in inclusion mode.
- `--gk` defaults to the repository's `bin/gk`.
- `--gk-timeout` applies to each Boolean world, not to the complete run.
- `--max-ground` stops grounding when it reaches the configured limit.
- `--keep-worlds` retains generated Boolean inputs for inspection.
- `--json` writes the inclusion result in machine-readable form.

At 10,000 trials, the largest approximate 95% half-width for one sampled
proportion is about 0.01. Smaller differences require more trials. Inclusion
mode can be slow because subtraction normally requires at least two gk runs per
world. Threshold mode performs its trials in one Python process and is much
faster.

## Input limits

- The command-line input must be a JSON-LD-LOGIC `.js` file. Equivalent `.gkp`,
  `.gks`, TPTP, ASP, and Prolog files are outside these scripts.
- Both modes require a finite constant domain and reject nested function terms.
- Inclusion mode obtains clauses from gk and refuses to continue when it cannot
  map the clauses back to input confidence annotations safely.
- Threshold mode has the narrower clause and query restrictions described
  above. It reports unresolved cyclic or priority cases instead of guessing.
- Neither mode performs probabilistic conditioning on evidence or learning.
