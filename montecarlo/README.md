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
draws one threshold `U` uniformly from 0 to 1 for that atom. The same threshold
is used for both sides:

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
atom has one threshold, so two downstream proofs that depend on the same atom
remain correlated.

Atoms are evaluated in dependency order. A cycle containing only one-sided,
positive dependencies is evaluated by a least fixpoint in each trial. A cycle
through a blocker or a contested atom is reported as `not scored`, because the
small model does not define a reliable outcome for it.

Run a threshold calculation as follows:

```sh
montecarlo/gkmc.py --semantics threshold -n 10000 --seed 1 \
  Examples/confidences/net_direct.js
```

`net_direct.js` has evidence 0.7 for `flies(a)` and 0.4 against it. With 10,000
draws the sampler returned 0.2977 support for, 0 support against, 0.4041
conflict, and 0.2982 ignorance. gk reports 0.3, 0, 0.4, and 0.3.

Threshold mode does not call gk. It accepts a smaller input fragment than
inclusion mode: one ground predicate query and directional clauses whose final
ordinary literal is the conclusion. It rejects function terms, arithmetic and
other built-ins, equality, compact formula connectives, ambiguous clauses with
several positive literals, and taxonomy-valued blocker priorities.

## Differences

Agreement is expected when both calculations use the same independence and
dependency structure. It supports the stated interpretation for that example.

There are three sources of differences:

- A recursive rule may have many possible ground proof trees. Inclusion and
  threshold sampling accept a world when any sampled tree succeeds. gk may
  report the evidence product of a selected proof. `near.js` demonstrates this
  difference.
- If a premise has both positive and negative support, gk can net the premise's
  support before using it in a rule. Inclusion sampling instead counts the
  worlds in which the positive premise is provable, including worlds where its
  negation is also provable. `net_premise.js` demonstrates this difference.
- Defaults and priorities determine evidence usability after clause inclusion.
  The samplers implement only the documented restricted cases and decline or
  disagree on other priority encodings.

The detailed results and the coverage status of every example directory are in
[`comparison.md`](comparison.md).

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
