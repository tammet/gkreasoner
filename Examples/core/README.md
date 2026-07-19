# Core reasoning examples

These problems exercise resolution, variable substitution, equality, function
terms, and explicit negation. Run commands from the repository root.

## Rules and substitutions

[`grandfather.gkp`](grandfather.gkp), [`grandfather.gks`](grandfather.gks), and
[`grandfather.js`](grandfather.js) encode the same problem in GKP, GKS, and
JSON-LD-LOGIC:

```prolog
0.9::father(john, pete).
0.8::father(pete, mark).
0.95::grandfather(X, Z) :- father(X, Y), father(Y, Z).
query(grandfather(john, X)).
```

```sh
./bin/gk Examples/core/grandfather.gkp
```

Expected answer: `mark`, confidence `0.684`. Resolution binds the intermediate
variable to `pete` and the query variable to `mark`. The confidence is the
product of the three annotated inputs.

## Equality and function terms

[`grandfather_equality.js`](grandfather_equality.js) represents parents as
functions and supplies equalities such as `father(john) = pete`. Equality
reasoning returns two answers:

```text
john  confidence 0.9
mike  confidence 0.9
```

[`algebra.js`](algebra.js) contains inverse, identity, and associativity axioms
and proves `m(e,c) = c`. [`algebra_confidence.js`](algebra_confidence.js) gives
the identity axiom confidence `0.9`. The proof uses three ground instances of
that axiom and returns `0.9^3 = 0.729`.

## Propositional clauses

[`logic_chain.js`](logic_chain.js) encodes implication with function terms and
proves `p(i(a,i(b,a)))`. It contains no confidence annotations or defaults, so
the result is a classical proof with confidence 1.

## Explicit negative evidence

[`negation.js`](negation.js) supplies several positive and negative sources for
one predicate. [`negation_conflict.js`](negation_conflict.js) places conflicting
evidence on `bird(a)` and propagates it through rules for `flies(a)`.

```sh
./bin/gk Examples/core/negation_conflict.js -detail
```

The returned confidence is `0.252`. The detailed report names the contested
`bird(a)` premise as a conflict source.

## File index

| File | Main feature |
|---|---|
| `grandfather.gkp`, `grandfather.gks`, `grandfather.js` | one problem in three input notations; rules, substitutions, and a proof product |
| `grandfather_equality.js` | equality, function terms, multiple answers |
| `algebra.js` | equational reasoning |
| `algebra_confidence.js` | distinct ground uses of an uncertain axiom |
| `logic_chain.js` | propositional resolution |
| `negation.js` | positive and negative sources |
| `negation_conflict.js` | a contested premise propagated into a conclusion |

See [`../../Doc/how_gk_works.md`](../../Doc/how_gk_works.md) for the proof and
confidence algorithms.
