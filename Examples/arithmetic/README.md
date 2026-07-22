# Arithmetic examples

GK has two arithmetic mechanisms:

- ground evaluation simplifies expressions whose operands are known;
- bounded instantiation proposes small integer values for variables in selected
  arithmetic conditions.

The automatic strategy does not enable useful instantiation for these open
arithmetic queries. The commands below set the mode explicitly.

## Ground evaluation

[`ground_unary.js`](ground_unary.js) derives a term containing `2 + 3` and asks
whether the result is `5`:

```sh
./bin/gk Examples/arithmetic/ground_unary.js
```

Expected result: `true`, confidence 1. No arithmetic strategy key is required.
[`donor_ground_unary.js`](donor_ground_unary.js) is a second ground case, and
[`donor_overflow_safety.js`](donor_overflow_safety.js) checks a large product.

## One-variable instantiation

[`apples_answer.gkp`](apples_answer.gkp) and [`apples_answer.js`](apples_answer.js)
contain:

```prolog
0.8::johnhad(X) :- X + 2 = 10.
query(johnhad(X)).
```

```sh
./bin/gk Examples/arithmetic/apples_answer.gkp -seconds 5 \
  -strategytext '{"strategy":["unit"],"query_preference":0,"arith_instantiation":1}'
```

Expected answer: `8`, confidence `0.8`. Resolution reduces the query to the
condition `X + 2 = 10`; the `arithinst` inference tests bounded candidates and
retains 8.

[`boundary_comparison.js`](boundary_comparison.js) asks for a value satisfying
`X > 7`. Mode 1 returns the first retained candidate, 8:

```sh
./bin/gk Examples/arithmetic/boundary_comparison.js -seconds 5 \
  -strategytext '{"strategy":["unit"],"query_preference":0,"arith_instantiation":1}'
```

The mode is bounded enumeration. It does not characterize all integers above
7 and must not be read as a complete answer set.

## Two-variable instantiation

[`product_tuple.js`](product_tuple.js) asks for `X * Y = 6`. Use mode 2 because
two variables occur in the condition:

```sh
./bin/gk Examples/arithmetic/product_tuple.js -seconds 5 \
  -strategytext '{"strategy":["unit"],"query_preference":0,"arith_instantiation":2}'
```

Expected retained answer: `(6, 1)`, confidence 1. Mode 1 finds no answer for
this file.

## Arithmetic combined with other reasoning

[`blocker_apples.js`](blocker_apples.js) sends an instantiated value through a
default rule and confidence calculation. The `donor_instantiation*.js` files
cover an additional equation, a comparison guard, selection between cars, and
division into boxes.

## File index

| File | Expected result | Mode |
|---|---|---:|
| `apples_answer.gkp`, `apples_answer.js` | `8`, confidence `0.8` | 1 |
| `boundary_comparison.js` | `8` | 1 |
| `blocker_apples.js` | `8` through a default rule | 1 |
| `donor_instantiation11_apples.js` | `8` | 1 |
| `donor_instantiation12_apples_comparison.js` | `true` | 1 |
| `donor_instantiation13_cars.js` | `mike` | 1 |
| `donor_instantiation16_boxes.js` | `4` | 2 |
| `product_tuple.js` | `(6, 1)` | 2 |
| `ground_unary.js`, `donor_ground_unary.js` | `true` | none |
| `donor_overflow_safety.js` | `true` | none |

Instantiation modes set conservative candidate, probe, and depth limits. They
are intended for small integer conditions, not general algebra or constraint
solving. Strategy keys are listed in
[`../../Doc/strategy_reference.md`](../../Doc/strategy_reference.md).
