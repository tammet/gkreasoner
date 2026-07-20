# Core reasoning examples

These problems exercise resolution, variable substitution, equality, function
terms, and explicit negation. Run commands from the repository root.

## Resolution and function terms

[`logic_chain.js`](logic_chain.js) encodes implication with function terms and
proves `p(i(a,i(b,a)))`. It contains no confidence annotations or defaults, so
the result is a classical proof with confidence 1.

[`algebra.js`](algebra.js) contains inverse, identity, and associativity axioms
and proves `m(e,c) = c` by equality reasoning.

## Explicit negative evidence

[`negation.js`](negation.js) supplies several positive and negative sources for
one predicate. [`negation_conflict.js`](negation_conflict.js) places conflicting
evidence on `bird(a)` and propagates it through rules for `flies(a)`.

```sh
./bin/gk Examples/core/negation_conflict.js -detail
```

The returned confidence is `0.252`. The detailed report names the contested
`bird(a)` premise as a conflict source.

## Selected files

| File | Main feature |
|---|---|
| `algebra.js` | equational reasoning |
| `logic_chain.js` | propositional resolution |
| `negation.js` | positive and negative sources |
| `negation_conflict.js` | a contested premise propagated into a conclusion |

See [`../../Doc/how_gk_works.md`](../../Doc/how_gk_works.md) for the proof and
confidence algorithms.
