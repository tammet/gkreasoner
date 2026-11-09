# Confidence and support examples

The examples in this directory show how input confidences produce the four
shares of an answer: for, against, conflict, and ignorance. Each ground
instance of an uncertain input clause is an independent source: it is
present with the probability of its confidence.
[`../../Doc/support_semantics.md`](../../Doc/support_semantics.md) states
the meaning of the four shares on examples.

gk's default method, the recursive method, starts from the proofs it finds,
searches recursively for further support, opposition and exceptions, and
evaluates all the evidence in one calculation. Run commands from the
repository root. The values below are gk 1.2.4's, shortened.

## Product along a proof

[`coin1.gkp`](coin1.gkp) and [`coin1.js`](coin1.js) contain:

```prolog
0.5::p(heads1).
0.6::p(heads2).
r(c) :- p(heads1), p(heads2).
query(r(X)).
```

The proof of `r(c)` uses both uncertain facts, so `r(c)` holds where both
are present: `0.5 * 0.6 = 0.3`. gk answers `r(c)` with (.3, 0, 0, .7).

[`rulemult.js`](rulemult.js) gives the same calculation to a conjunctive
rule. [`rules4.js`](rules4.js) and [`rules5.js`](rules5.js) use a rule with
confidence `0.8` three times after a fact with confidence `0.9`, producing
`0.9 * 0.8^3 = 0.4608` for `p(f(f(f(a))))`. `rules5.js` asks an open
question and also gets the longer chains, for example `p(f(f(f(f(a)))))`
with .3686. gk uses its whole time budget on these two inputs, about 7
seconds.

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

```text
"value":[0.8,0,0,0.2]
```

The sources are independent, so noisy-or gives
`1 - (1 - 0.5)(1 - 0.6) = 0.8`.

[`overlap1.js`](overlap1.js) and [`overlap3.js`](overlap3.js) contain proofs
with shared premises. gk counts each shared source once. It answers .846
and .959 for, respectively.

gk combines the proofs it finds. A proof that it does not find adds
nothing. In an input without evidence against, a search cut by the budget
can therefore only lower the share for.

## Positive and negative support

[`net_direct.gkp`](net_direct.gkp) and [`net_direct.js`](net_direct.js) contain:

```prolog
0.7::flies(a).
0.4::-flies(a).
query(flies(a)).
```

```sh
./bin/gk Examples/confidences/net_direct.gkp
```

```text
"value":[0.3,0,0.4,0.3]
```

Both sides are tested against one shared number of the atom. Below .4 both
pass (conflict .4), between .4 and .7 only the support for it passes (.3),
and above .7 neither passes (ignorance .3).

The `net_*.js` files vary which side is stronger:

| File | Evidence | gk 1.2.4 |
|---|---|---|
| `net_lone.js` | .5 for, nothing against | (.5, 0, 0, .5) |
| `net_fought.js` | .9 for, .4 against | (.5, 0, .4, .1) |
| `net_against.js` | .3 for, .8 against | (0, .5, .3, .2) |
| `net_strong.js` | .9 for, .3 against | (.6, 0, .3, .1) |
| `net_premise.js` | a contested premise, then a rule | (.27, 0, 0, .73) |

In `net_premise.js`, `bird(a)` has .5 for it and .2 against it. Only where
`bird(a)` holds without conflict, a share of .3, does the rule of
confidence .9 derive `flies(a)`: .3 × .9 = .27.

## Chains and networks

[`near.js`](near.js) and [`near2.js`](near2.js) apply a transitivity rule
with confidence `0.9`. One proof of the chain applies the rule eight times:
`0.9^8 = 0.4305`. The chain has many proofs, one for each way to group its
links, and each proof uses other ground instances of the rule.

- `near.js` uses ten constants. gk finds several of these proofs within its
  budget and answers (.7522, 0, 0, .2478), with 46 searches cut by their
  allowances. The reference tool, which samples the semantics, gives
  (1, 0, 0, 0): with so many routes, almost every world contains one.
- `near2.js` builds the chain with a function symbol. gk answers
  (.4305, 0, 0, .5695), the value of one proof, with 34 searches cut. The
  reference tool does not accept function symbols.

[`smokes.gkp`](smokes.gkp) and [`smokes.js`](smokes.js) contain several
proofs of `smokes(sam)`. gk answers (.3804, 0, 0, .6196); the reference tool
gives .3716 for it, within its sampling error of ±.0113. The `alarm*.js` and
`socialsmoking*.js` files provide larger networks and keep comparison
material in their comments.

## Small values

The recursive method reports the four shares of every answer it finds, also
small ones. [`n3.js`](n3.js) gives (.08, 0, 0, .92), and
[`rules3.js`](rules3.js) and [`equality3.js`](equality3.js) give
(.18, .08, .72, .02).

## File index

| Files | Calculation or feature |
|---|---|
| `cumulate.gkp`, `cumulate.js` | two independent sources, noisy-or, for .8 |
| `coin1.gkp`, `coin1.js` | product of two facts, for .3 |
| `coin2.js` | two-coin disjunction, for .8 |
| `coin3.js`, `coin4.js` | four sources with confidence `0.6`, for .9744 |
| `coin4_err.js` | four sources plus an inequality constraint |
| `coin4_err1.js`, `coin4_err2.js` | smaller constrained variants |
| `overlap1.js`, `overlap3.js` | proofs that share sources |
| `near.js`, `near2.js` | repeated rule confidence along a transitive chain |
| `rulemult.js` | confidence product for a conjunctive rule |
| `rules1.js`, `rules2.js` | positive and negative rule evidence, open and ground query forms |
| `rules3.js` | disjunctive evidence with a small share for |
| `rules4.js`, `rules5.js` | repeated rule instances, open and ground query forms |
| `net_direct.gkp`, `net_direct.js` | direct support and opposition |
| `net_lone.js` | single-side baseline |
| `net_fought.js`, `net_against.js`, `net_strong.js` | cases where one side is stronger |
| `net_premise.js` | contested premise propagated through a rule |
| `n1.js`, `n2.js`, `n2a.js`, `n2c.js`, `n2plus.js`, `n3.js` | progressively larger combinations of evidence for and against |
| `conf1.js` through `conf4.js` | compact combination and opposition cases |
| `alarm.js`, `alarm_v1.js`, `alarm_v2.js` | alarm network variants |
| `smokes.gkp`, `smokes.js`, `smokes2.js` | smoking-network variants |
| `socialsmoking.js`, `socialsmoking2.js` | larger social-influence networks |
| `smokes_alchemy.js` | a smokes/cancer rule set adapted from an MLN example |
| `equality1.js`, `equality2.js`, `equality3.js` | support propagated and opposed through equality |

How gk reaches an answer is described in
[`../../Doc/how_gk_works.md`](../../Doc/how_gk_works.md).
