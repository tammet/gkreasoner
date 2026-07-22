# The uncertainty page examples: gk versus the two samplers

A side-by-side of gk's reported confidences and the two Monte Carlo
readings on all 23 examples of the logictools.org *Reasoning under
uncertainty* page (`commonsense.html` in the
[logictools repository](https://github.com/tammet/logictools)), with the
reason wherever a sampler does not apply.

The three columns answer different questions:

- **gk** evaluates argument support: the best derivation for an answer and the
  best derivation for its negation, with opposition on contested premises
  resolved before use.
  Column: native gk run with each example's own page settings;
  answers as `value at confidence`, with the four components
  (positive/negative/conflict/ignorance) where they add information.
- **Clause-activation sampling** (`montecarlo/gkmc.py`, independent activation
  per ground clause): the fraction of sampled worlds in which the answer is provable
  minus the fraction in which its explicit negation is. 2000 worlds,
  seed 1 (95% half-width about 0.02); example 12 at 200 worlds (its
  grounding is about 20000 clauses).
- **Shared-threshold sampling** (`--semantics threshold`, one shared threshold
  per atom plus the mutual-blocking treatment of defaults): the four components.
  20000 draws, seed 1 (half-width about 0.007).

| # | Example | gk | Clause-activation (difference) | Shared-threshold (components) |
|---|---|---|---|---|
| 1 | facts and rules | polly at 1.0 | 1.000 | 1.0/0/0/0 |
| 2 | input weights | 0.56 | 0.560 | 0.556/0/0/0.444 |
| 3 | several sources | 0.8 | 0.815 | 0.797/0/0/0.203 |
| 4 | positive and negative support | 0.3 (0.3/0/0.4/0.3) | 0.295 | 0.298/0/0.401/0.301 |
| 5 | rule chains | 0.3764 | 0.387 | 0.377/0/0/0.623 |
| 6 | shared evidence | 0.846 | 0.855 | 0.845/0/0/0.155 |
| 7 | contested premises | 0.27 | **0.464 — differs** | 0.270/0/0/0.730 |
| 8 | defaults | tweety 1.0, robin 1.0 | both 1.000 | both 1.0/0/0/0 |
| 9 | an exception | tweety rejected at 0.8 (0.1/0.9/0/0) | −0.804 | 0.102/0.899/0/0 |
| 10 | penguins | tweety 1.0; pingu rejected at 1 (0/1/0/0) | tweety 1.000; pingu never provable | tweety 1/0/0/0; pingu 0/1/0/0 |
| 11 | Nixon diamond | rejected at 0, ignorance 1 | 0.000 | ignorance 1.0 |
| 12 | where is John | kitchen 1.0; hallway rejected, ignorance 1 | kitchen 1.000; hallway never provable | kitchen 1.0/0/0/0 |
| 13 | arithmetic | 7 at 0.8 | *unsupported: function terms (`$product`)* | *same limitation* |
| 14 | equality | true at 1.0 | *unsupported: function term `capital(estonia)`* | *same limitation* |
| 15 | conflict detail | tweety at 0.252 | 0.260 | 0.254/0/0/0.746 |
| 16 | JSON notation | 0.56 | 0.560 | 0.556/0/0/0.444 |
| 17 | GKS notation | 0.56 | 0.560 | 0.556/0/0/0.444 |
| 18 | TPTP notation | p at 0.64 (0.72/0.08/0/0.2) | 0.646 | 0.724/0.077/0/0.199 |
| 19 | defaults in JSON | true at 1.0 | 1.000 | *unsupported: compact `=>` connective (the model reads the original statements)* |
| 20 | planning | plan at 1.0 | *unsupported: function terms (`on(a,table)`, `do(...)`)* | *same limitation* |
| 21 | English: penguins | false at 1.0 | *unsupported: background knowledge base with `$ctxt` structured terms* | *same limitation* |
| 22 | English: which one | `$some_fox` at 1.0 | *same as 21* | *same as 21* |
| 23 | taxonomy classification | b1 at 0.5552, h1 at 0.44 | *unsupported: taxonomy-valued priorities and auxiliary data files* | *same limitation* |

## Reading the table

**The shared-threshold column tracks gk to sampling precision on every example it
supports** — including all the default, exception, priority, and mutual-blocking
cases (8–12, 18). This is by construction: on its supported fragment the
shared-threshold model is a sampling semantics for gk's own arithmetic, with the
mutual-blocking treatment of defaults (each default with an exception
condition survives only off the mass of what fires that condition;
equal-rank pairs block each other symmetrically; unequal ranks take the
strict-priority override).

**The clause-activation column agrees everywhere except example 7.** The one
remaining disagreement is the contested-premise case: `bird(tweety)`
carries 0.5 positive and 0.2 negative evidence, and birds fly at 0.9. gk
resolves the opposition on the premise before using it —
(0.5 − 0.2) × 0.9 = 0.27 — while the clause-activation count cannot:
"Tweety is not a bird" never makes "Tweety does not fly" derivable, so the
doubt changes nothing and the count gives 0.5 × 0.9 ≈ 0.46. This is a
documented semantic difference between the two readings;
the shared-threshold model reproduces gk's result. Small offsets elsewhere
(3, 5, 6, 15) are inside the stated sampling intervals.

**The unsupported cases fall into four families.** Function terms, arithmetic
and equality (13, 14, 20) are outside the samplers' finite ground model.
Compact connectives (19) are a shared-threshold-only limit: that model reads the
original statements, where `=>` has not yet been flattened, while
clause-activation sampling works from gk's own clausifier and supports the
example. The English-generated examples (21, 22) need the shared background
knowledge base, whose `$ctxt` context terms are structured terms. The
taxonomy example (23) uses taxonomy-valued priorities resolved from
auxiliary data files, which neither sampling model represents.

**Notable individual rows.** Example 9: negative support exceeds positive
support by 0.8, and all three columns say so — gk as a rejected answer,
clause-activation as a difference of −0.8, shared-threshold as 0.1/0.9. Example 18 is
the same family for a negative query: the penguin does not fly at about
0.64 in all three columns. Example 11 is the Nixon mutual-blocking case — equal-priority
defaults cancel into pure ignorance, and both samplers concur (nothing is
provable, and all four components except ignorance are zero). Example 12's persistence answer is
unanimous: the kitchen with certainty, the hallway claim withdrawn into
ignorance because John's own later movement fires the inertia rule's
exception in every world.

## Reproduction

The gk column uses native gk, with each example run with its page preset
arguments plus
`-detail -outformat json -seconds 5` (example 20 with
`-seconds 30 -maxanswers 1`; 21/22 with the shared knowledge base,
`-confidence 0.1` and the page's strategy; 23 with `-defaults` and the
taxonomy data files).

Samplers: GKP/GKS/TPTP examples are first converted with
`gk <file> -writejson`; then

```sh
montecarlo/gkmc.py -n 2000 --seed 1 --jobs 4 EX.js
montecarlo/gkmc.py --semantics threshold -n 20000 --seed 1 EX.js
```

Open queries are handled by both samplers per closed answer instance.

## Related documents in this repository

- [`README.md`](README.md) — the two sampling modes, the difference
  families worked through, and the reference checks.
- [`comparison.md`](comparison.md) — the comparison on the repository's own
  suite of examples, produced with the current repository binary.
- [`settlement_checks/`](settlement_checks/) — ten hand-derived reference
  outputs with native GK's four components as expectations; the threshold-world
  sampler passes all ten.

The page inputs themselves live in the
[logictools repository](https://github.com/tammet/logictools)
(`commonsense.html`); numbers and names above refer to its example menus.
