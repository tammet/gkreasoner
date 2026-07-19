# Confidence examples

The examples in this directory isolate the main confidence calculations:

1. multiply the distinct evidence instances used by one proof;
2. combine alternative proofs from their evidence-instance sets;
3. calculate positive and negative support separately;
4. report the remaining mass as conflict or ignorance.

Run commands from the repository root. `-detail` adds the four-part report;
`-confidence 0` retains results below the default acceptance threshold.

## Product along a proof

[`coin1.gkp`](coin1.gkp) and [`coin1.js`](coin1.js) contain:

```prolog
0.5::p(heads1).
0.6::p(heads2).
r(c) :- p(heads1), p(heads2).
query(r(X)).
```

The proof of `r(c)` uses both uncertain facts. Its confidence is
`0.5 * 0.6 = 0.3`.

[`rulemult.js`](rulemult.js) gives the same calculation to a conjunctive rule.
[`rules4.js`](rules4.js) and [`rules5.js`](rules5.js) use a rule of confidence
`0.8` three times after a fact of confidence `0.9`, producing
`0.9 * 0.8^3 = 0.4608`.

## Alternative proofs

[`cumulate.gkp`](cumulate.gkp) and [`cumulate.js`](cumulate.js) give one atom
two distinct sources:

```prolog
0.5::bird(a).
0.6::bird(a).
query(bird(a)).
```

```sh
./bin/gk Examples/confidences/cumulate.gkp
```

The sources are disjoint, so noisy-or gives
`1 - (1 - 0.5)(1 - 0.6) = 0.8`.

[`overlap1.js`](overlap1.js) and [`overlap3.js`](overlap3.js) contain proofs
with shared premises. GK reconstructs each proof's ground evidence instances
and uses the shared instances only once. The resulting confidences are `0.846`
and `0.959`, respectively.

## Positive and negative support

[`net_direct.gkp`](net_direct.gkp) and [`net_direct.js`](net_direct.js) contain:

```prolog
0.7::flies(a).
0.4::-flies(a).
query(flies(a)).
```

```sh
./bin/gk Examples/confidences/net_direct.gkp -detail
```

Expected assessment:

```text
confidence: 0.3
support: 0.3 for, 0 against
conflict: 0.4   ignorance: 0.3
```

The `net_*.js` files vary which side dominates. `net_premise.js` places the
conflict on a premise and then derives a conclusion from it.

## Chains and networks

[`near.js`](near.js) and [`near2.js`](near2.js) apply a transitivity rule of
confidence `0.9` eight times, producing `0.9^8 = 0.4305`.

[`smokes.gkp`](smokes.gkp) and [`smokes.js`](smokes.js) contain several proofs
of `smokes(sam)`. GK multiplies within each proof and combines the proof
supports, returning `0.3764`. The `alarm*.js` and `socialsmoking*.js` files
provide larger networks and retain comparison material in their comments.

## Acceptance threshold

The default `-confidence` threshold is `0.1`. A derivation at or below the
effective limit may be printed with `result: evidence below limit`. This occurs
in `n3.js`, `rules3.js`, and `equality3.js`. Lowering the threshold changes the
acceptance label, not the derivation:

```sh
./bin/gk Examples/confidences/n3.js -confidence 0
```

## File index

| Files | Calculation or feature |
|---|---|
| `cumulate.gkp`, `cumulate.js` | two disjoint sources, noisy-or, result `0.8` |
| `coin1.gkp`, `coin1.js` | product of two facts, result `0.3` |
| `coin2.js` | two-coin disjunction, result `0.8` |
| `coin3.js`, `coin4.js` | four sources with confidence `0.6`, result `0.9744` |
| `coin4_err.js` | four sources plus an inequality constraint |
| `coin4_err1.js`, `coin4_err2.js` | smaller constrained variants |
| `overlap1.js`, `overlap3.js` | measured overlap between proof supports |
| `near.js`, `near2.js` | repeated confidence along a transitive chain |
| `rulemult.js` | confidence product for a conjunctive rule |
| `rules1.js`, `rules2.js` | positive and negative rule evidence, open and ground query forms |
| `rules3.js` | disjunctive evidence at the acceptance boundary |
| `rules4.js`, `rules5.js` | repeated rule instances, open and ground query forms |
| `net_direct.gkp`, `net_direct.js` | direct support and opposition |
| `net_lone.js` | one-sided baseline |
| `net_fought.js`, `net_against.js`, `net_strong.js` | positive- and negative-dominant cases |
| `net_premise.js` | contested premise propagated through a rule |
| `n1.js`, `n2.js`, `n2a.js`, `n2c.js`, `n2plus.js`, `n3.js` | progressively larger combinations of pro and con evidence |
| `conf1.js` through `conf4.js` | compact pooling and netting cases |
| `alarm.js`, `alarm_v1.js`, `alarm_v2.js` | alarm network variants |
| `smokes.gkp`, `smokes.js`, `smokes2.js` | smoking-network variants |
| `socialsmoking.js`, `socialsmoking2.js` | larger social-influence networks |
| `smokes_alchemy.js` | a smokes/cancer rule set adapted from an MLN example |
| `equality1.js`, `equality2.js`, `equality3.js` | confidence propagated and opposed through equality |

The algorithms are described in
[`../../Doc/how_gk_works.md`](../../Doc/how_gk_works.md).
