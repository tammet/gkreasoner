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

gk answers `$is_number(5)` with (1, 0, 0, 0). No arithmetic strategy key is
required.
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

gk answers `johnhad(8)` with (.8, 0, 0, .2). Resolution reduces the query to
the condition `X + 2 = 10`; the `arithinst` inference tests bounded
candidates and retains 8. The arithmetic step is not replayed as an
application, so the line reports it among `pending_steps`.

[`boundary_comparison.js`](boundary_comparison.js) asks for a value satisfying
`X > 7`. Mode 1 returns the first candidate that satisfies the condition, 8,
and gk answers `above_seven(8)` with (1, 0, 0, 0):

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

gk answers `product_witness(6,1)` and `product_witness(1,6)`, both
(1, 0, 0, 0). Mode 1 finds no answer for this file: the line reports
`the recursion did not run`.

## Arithmetic combined with other reasoning

[`blocker_apples.js`](blocker_apples.js) sends an instantiated value through a
default rule and confidence calculation: `bird(8)` with .8, a default of
confidence .9, and its exception `penguin(8)` with .7. gk answers
`flies(8)` with (.216, 0, 0, .784), that is .8 × .9 × (1 − .7). The `donor_instantiation*.js` files
cover an additional equation, a comparison guard, selection between cars, and
division into boxes.

## File index

| File | Expected result | Mode |
|---|---|---:|
| `apples_answer.gkp`, `apples_answer.js` | `8`, (.8, 0, 0, .2) | 1 |
| `boundary_comparison.js` | `8` | 1 |
| `blocker_apples.js` | `8` through a default rule, (.216, 0, 0, .784) | 1 |
| `donor_instantiation11_apples.js` | `8` | 1 |
| `donor_instantiation12_apples_comparison.js` | (1, 0, 0, 0) | 1 |
| `donor_instantiation13_cars.js` | `mike` | 1 |
| `donor_instantiation16_boxes.js` | `4` | 2 |
| `product_tuple.js` | `(6, 1)` and `(1, 6)` | 2 |
| `ground_unary.js`, `donor_ground_unary.js` | (1, 0, 0, 0) | none |
| `donor_overflow_safety.js` | (1, 0, 0, 0) | none |

Instantiation modes use fixed candidate, probe, and depth limits. They
are intended for small integer conditions; they do not perform general
algebra or constraint solving. Strategy keys are listed in
[`../../Doc/strategy_reference.md`](../../Doc/strategy_reference.md).
