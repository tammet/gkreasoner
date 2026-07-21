# The uncertainty page examples: gk versus the two samplers

A side-by-side of gk's reported confidences and the two Monte-Carlo
readings on all 23 examples of the logictools.org *Reasoning under
uncertainty* page (`commonsense.html` in the
[logictools repository](https://github.com/tammet/logictools)), with the
refusal reason wherever a sampler does not apply.

The three columns answer different questions:

- **gk** weighs arguments: the best derivation for an answer against the
  best derivation against it, contested premises netted before use.
  Column: the native gk 1.0.4 run with each example's own page settings;
  answers as `value at confidence`, with the four masses
  (for/against/conflict/ignorance) where they add information.
- **Inclusion sampling** (`montecarlo/gkmc.py`, one coin per ground
  clause): the fraction of sampled worlds in which the answer is provable
  minus the fraction in which its explicit negation is. 2000 worlds,
  seed 1 (95% half-width about 0.02); example 12 at 200 worlds (its
  grounding is about 20000 clauses).
- **Threshold sampling** (`--semantics threshold`, one shared bar per
  atom plus the mutual-gate treatment of defaults): the four masses.
  20000 draws, seed 1 (half-width about 0.007).

| # | Example | gk 1.0.4 | Inclusion (net) | Threshold (masses) |
|---|---|---|---|---|
| 1 | facts and rules | polly at 1.0 | 1.000 | 1.0/0/0/0 |
| 2 | confidences | 0.56 | 0.560 | 0.556/0/0/0.444 |
| 3 | several sources | 0.8 | 0.815 | 0.797/0/0/0.203 |
| 4 | for and against | 0.3 (0.3/0/0.4/0.3) | 0.295 | 0.298/0/0.401/0.301 |
| 5 | rule chains | 0.3764 | 0.387 | 0.377/0/0/0.623 |
| 6 | shared evidence | 0.846 | 0.855 | 0.845/0/0/0.155 |
| 7 | contested premises | 0.27 | **0.464 — differs** | 0.270/0/0/0.730 |
| 8 | defaults | tweety 1.0, robin 1.0 | both 1.000 | both 1.0/0/0/0 |
| 9 | an exception | tweety rejected at 0.8 (0.1/0.9/0/0) | −0.804 | 0.102/0.899/0/0 |
| 10 | penguins | tweety 1.0; pingu rejected at 1 (0/1/0/0) | tweety 1.000; pingu never provable | tweety 1/0/0/0; pingu 0/1/0/0 |
| 11 | Nixon diamond | rejected at 0, ignorance 1 | 0.000 | ignorance 1.0 |
| 12 | where is John | kitchen 1.0; hallway rejected, ignorance 1 | kitchen 1.000; hallway never provable | kitchen 1.0/0/0/0 |
| 13 | arithmetic | 7 at 0.8 | *refused: function terms (`$product`)* | *same refusal* |
| 14 | equality | true at 1.0 | *refused: function term `capital(estonia)`* | *same refusal* |
| 15 | conflict detail | tweety at 0.252 | 0.260 | 0.254/0/0/0.746 |
| 16 | JSON notation | 0.56 | 0.560 | 0.556/0/0/0.444 |
| 17 | GKS notation | 0.56 | 0.560 | 0.556/0/0/0.444 |
| 18 | TPTP notation | p at 0.64 (0.72/0.08/0/0.2) | 0.646 | 0.724/0.077/0/0.199 |
| 19 | defaults in JSON | true at 1.0 | 1.000 | *refused: compact `=>` connective (the model reads the original statements)* |
| 20 | planning | plan at 1.0 | *refused: function terms (`on(a,table)`, `do(...)`)* | *same refusal* |
| 21 | English: penguins | false at 1.0 | *refused: background knowledge base with `$ctxt` structured terms* | *same refusal* |
| 22 | English: which one | `$some_fox` at 1.0 | *same as 21* | *same as 21* |
| 23 | taxonomy classification | b1 at 0.5552, h1 at 0.44 | *refused: taxonomy-valued priorities and auxiliary data files* | *same refusal* |

## Reading the table

**The threshold column tracks gk to sampling precision on every example it
accepts** — including all the default, exception, priority and standoff
cases (8–12, 18). This is by construction: on its accepted fragment the
threshold model is a sampling semantics for gk's own arithmetic, with the
mutual-gate treatment of defaults (each gated default survives only off
the mass of what fires its exception; equal-rank pairs gate each other
symmetrically; unequal ranks take the priority award).

**The inclusion column agrees everywhere except example 7.** The one
remaining disagreement is the contested-premise case: `bird(tweety)`
carries 0.5 for and 0.2 against, and birds fly at 0.9. gk nets the premise
before using it — (0.5 − 0.2) × 0.9 = 0.27 — while the coin count cannot:
"Tweety is not a bird" never makes "Tweety does not fly" derivable, so the
doubt changes nothing and the count gives 0.5 × 0.9 ≈ 0.46. This is a
deliberate difference between the two readings, not an error in either;
the threshold model sides with gk. Small offsets elsewhere (3, 5, 6, 15)
are inside the stated sampling intervals.

**The refusals fall into four families.** Function terms, arithmetic and
equality (13, 14, 20) are outside the samplers' finite ground model.
Compact connectives (19) are a threshold-only limit: that model reads the
original statements, where `=>` has not yet been flattened, while
inclusion sampling works from gk's own clausifier and accepts the example.
The English-generated examples (21, 22) need the shared background
knowledge base, whose `$ctxt` context terms are structured terms. The
taxonomy example (23) uses taxonomy-valued priorities resolved from
auxiliary data files, which neither sampling model represents.

**Notable individual rows.** Example 9: the balance points 0.8 against
Tweety flying, and all three columns say so — gk as a rejected answer,
inclusion as a net of −0.8, threshold as 0.1/0.9. Example 18 is the same
family from the refuting side: the penguin does not fly at about 0.64 in
all three columns. Example 11 is the Nixon standoff — equal-priority
defaults cancel into pure ignorance, and both samplers concur (nothing is
provable, no mass on any side). Example 12's persistence answer is
unanimous: the kitchen with certainty, the hallway claim withdrawn into
ignorance because John's own later movement fires the inertia rule's
exception in every world.

## Versions and reproduction

gk column: native gk **1.0.4** (the build with the settlement fixes),
each example run with its page preset arguments plus
`-detail -outformat json -seconds 5` (example 20 with
`-seconds 30 -maxanswers 1`; 21/22 with the shared knowledge base,
`-confidence 0.1` and the page's strategy; 23 with `-defaults` and the
taxonomy data files). Binaries built before 1.0.4 — including, at the
time of writing, the page's WebAssembly build and the shipped release
binaries — report different values on examples 9, 11, 12 and 18 (most
visibly: example 9's tweety as a positive answer at 0.1 and example 18's
penguin as rejected at 0.08).

Samplers: GKP/GKS/TPTP examples are first converted with
`gk <file> -writejson`; then

```sh
montecarlo/gkmc.py -n 2000 --seed 1 --jobs 4 EX.js
montecarlo/gkmc.py --semantics threshold -n 20000 --seed 1 EX.js
```

Open queries are handled by both samplers per closed answer instance.

## Related documents in this repository

- [`README.md`](README.md) — the two sampling modes, the difference
  families worked through, and the settlement cells.
- [`comparison.md`](comparison.md) — the recorded comparison on the
  repository's own example corpus (recorded against the shipped binary).
- [`settlement_checks/`](settlement_checks/) — ten adjudicated cells with
  the fixed native gk's four masses as expectations; the threshold
  sampler passes all ten.

The page inputs themselves live in the
[logictools repository](https://github.com/tammet/logictools)
(`commonsense.html`); numbers and names above refer to its example menus.
