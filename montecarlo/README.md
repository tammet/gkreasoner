# Monte Carlo checks for GK confidences

## Purpose and scope

This directory contains two sampling calculations for small GK examples.
Each estimates a defined reference model, so GK results can be compared
with model-level numbers computed without GK's support arithmetic. The two
models measure different quantities; they need not agree with each other
or with every GK report, and their disagreements identify the modelling
decision an example turns on.

The calculations are diagnostic tools rather than theorem provers. Both
are limited to finite inputs with named constants and no function terms. Run
the commands below from the repository root; the scripts require
[Python 3](https://www.python.org/) (standard library only) and the
shipped `bin/gk`.

## The two reference models

### Clause-activation sampling

Clause-activation sampling implements the ground-instance activation
semantics: each ground instance of an uncertain input clause is an
independent activation event whose probability is the input confidence.
For each trial:

1. gk clausifies the input.
2. The script grounds the clauses over the constants in the file.
3. Each uncertain ground clause is active with probability `c` and absent
   otherwise. Certain clauses are always active.
4. The active clauses, without their confidence annotations, form one
   Boolean program.
5. gk checks whether the query and its explicit negation are provable in
   that program.

For an answer `A`, the reported estimate is

```text
P(A is provable) - P(-A is provable),
```

the signed derivability measure of the activation-world sampler, measured
in the same sampled worlds. A world in which both polarities are provable
contributes zero to the difference; contradictory worlds are permitted,
without conditioning on consistency. The measure agrees with GK's signed
confidence on the stated common fragment; premise-level opposition,
defaults, retained-proof coverage, and calculation fallbacks can separate
the two values ([`comparison.md`](comparison.md)).

By default, separate ground instances of an uncertain rule receive
separate draws; this is the ground-instance activation setting. `--draws
shared` instead activates all instances originating from one input
statement together. That is a statement-level sensitivity calculation, and
it is not GK's event identity: GK distinguishes ground instances and
counts repeated use of the same ground instance once. State the draw
setting with any result.

An uncertain input statement that clausifies into more than one clause is
rejected: its activation events are not defined by this sampler.

### Shared-threshold sampling

Shared-threshold sampling, run by the threshold-world sampler, estimates
the shared-threshold reference construction on a restricted fragment. It
does not call gk, and it estimates the reference model, not every GK
report: a GK report whose `calculation` field is `flat`, `blocked_flat`,
or `proof_fallback` is a proof-pool decomposition, not a completed
shared-threshold atom partition.

Suppose the pooled positive support for one ground atom is `a` and the
pooled negative support is `b`. The sampler draws two independent uniforms
from 0 to 1 for each ground atom. Ordinary opposition uses the first draw
`U` as one shared uniform threshold for both polarities:

| Condition | Outcome |
|---|---|
| `b < U <= a` | positive support |
| `a < U <= b` | negative support |
| `U <= min(a,b)` | conflict |
| `U > max(a,b)` | ignorance |

Same-polarity confidences are pooled by noisy-or. A ground rule instance
holds in a draw when its body atoms are usable in the required polarity
and no exception condition fires. Each ground atom has one fixed pair of
draws per trial, so downstream derivations that depend on the same atom
remain correlated.

Opposition involving defaults uses both draws, following the local
combination rules: with equal explicit ranks, each polarity fires on its
own threshold and survives only if the other misses (mutual blocking);
with unequal ranks, the higher-ranked default takes the overlap region of
the shared threshold (the strict-priority override); a default opposed by
ordinary evidence takes the exclusive split, with no conflict component.

Atoms are evaluated in dependency order. A cycle containing only
single-polarity positive dependencies is evaluated by a least fixpoint in
each trial. A blocker cycle through the queried atom is resolved
credulously for the query, matching GK's blocker check. Any other cycle
through an exception condition or a contested atom, and a rank-restricted
exception check, is reported as `not scored`.

## Commands

Clause-activation sampling:

```sh
montecarlo/gkmc.py -n 10000 --seed 1 Examples/confidences/cumulate.js
```

Shared-threshold sampling:

```sh
montecarlo/gkmc.py --semantics threshold -n 10000 --seed 1 \
  Examples/confidences/net_direct.js
```

Batch reference check (no input file needed):

```sh
montecarlo/gkmc.py --semantics threshold -n 100000 --seed 1 \
  --check montecarlo/reference_checks
```

Other modes: `--semantics provable` reports only `P(A is provable)`;
`--semantics gkdefault` samples the same Boolean worlds but runs gk's
default acceptance on each closed answer; `--classify` (ground
single-literal query) prints the A-only / not-A-only / both / neither
world frequencies.

Options:

```text
montecarlo/gkmc.py [-n TRIALS] [--seed SEED]
                   [--draws per-instance|shared]
                   [--semantics subtract|provable|gkdefault|threshold]
                   [--classify] [--jobs N] [--gk PATH]
                   [--gk-args "..."] [--gk-timeout SECONDS]
                   [--max-ground N] [--keep-worlds DIR]
                   [--json FILE] [--check DIR] [input.js]
```

- `--seed` makes the sampled worlds repeatable; integer and string seeds
  are both stable across processes.
- `--jobs` controls concurrent gk calls in clause-activation mode.
- `--gk` defaults to the repository's `bin/gk`; `--gk-timeout` applies to
  each Boolean world.
- `--max-ground` stops grounding at the configured limit in both modes.
- `--keep-worlds` retains generated Boolean inputs; `--json` writes the
  clause-activation result in machine-readable form.

## Output fields

Clause-activation output is a table per answer: `MC pos`, `MC neg`, their
paired difference `MC pos-neg` with a 95% sampling interval, and
`GK result` — the signed confidence from one ordinary `gk -detail` run on
the original file, negative for a rejected answer. Below the table, one
line per answer reports GK's `calculation`, `coverage_status`,
`polarity_status`, and flags; these say what kind of GK result the number
is (see the report-status tables in
[`../Doc/how_gk_works.md`](../Doc/how_gk_works.md)). A numeric agreement
is meaningful only together with those fields.

Shared-threshold output is the four components `support_for`,
`support_against`, `conflict`, and `ignorance` per query instance, or
`not scored` with a reason for an unsupported case.

## Exactness and support limits

At 10,000 trials the largest approximate 95% half-width for one sampled
proportion is about 0.01; smaller differences require more trials.
Clause-activation mode is slow because subtraction normally needs at least
two gk runs per world; shared-threshold mode runs its trials in one Python
process.

On the GK side, a retained-proof value is the exact union probability of
the retained proof set only when the activation-event identifiers are
ground, replay succeeds, and the proof-union calculation stays within its
bounds; retained proofs need not cover every possible proof. A completed
shared-threshold report is marked `calculation: canonical_atom`. The
comparison tables therefore record GK's calculation and status next to
each number.

Input limits of the samplers:

- the input must be a JSON-LD-LOGIC `.js` file;
- both modes require a finite constant domain and reject function terms;
- clause-activation mode rejects an uncertain statement that clausifies
  into several clauses;
- shared-threshold mode needs a single predicate query (ground, or open
  and then evaluated per closed instance over the named constants) and
  directional clauses: the head is the last ordinary literal, or the
  consequent of the implication form `[antecedent, "=>", consequent]`; a
  clause with more than one positive literal is rejected as ambiguous;
- shared-threshold mode reports function terms, arithmetic and other
  built-ins, equality, formula connectives, non-integer blocker
  priorities, and the cycle and rank-restriction cases above as
  unsupported;
- neither mode performs probabilistic conditioning on evidence or
  learning.

## Results and checks

Result tables, the worked difference cases, and the coverage status of the
example directories are in [`comparison.md`](comparison.md).

[`reference_checks/`](reference_checks/) holds ten ground-query reference
inputs for the defaults family — uncertain and certain exception
conditions, equal-rank mutual blocking, the strict-priority override with
uncertain strengths, strict-priority ordering in both rank directions, a
default opposed by ordinary evidence, and a negated query.
`expected.tsv` records the four
components derived analytically from the local combination rules; the
batch check above reproduces all ten. gk `-detail` returns the same
values for these cases; that parity is an observation recorded in
`expected.tsv`, and gk output is not the source of the expected numbers.

[`test_threshold_rank0.py`](test_threshold_rank0.py) checks the
priority-zero cases and the contextual rank-restriction cases of the
threshold sampler against hand-derived closed forms, without gk:

```sh
python3 montecarlo/test_threshold_rank0.py
```
