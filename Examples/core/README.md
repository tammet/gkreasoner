# Core reasoning examples

These problems exercise resolution, variable substitution, equality, function
terms, and explicit negation. Run commands from the repository root.

## Resolution and function terms

[`logic_chain.js`](logic_chain.js) encodes implication with function terms and
asks for `p(i(a,i(b,a)))`. [`algebra.js`](algebra.js) contains inverse,
identity, and associativity axioms and asks for `m(e,c) = c`. Both inputs
are classical: they have no confidences and no defaults.

gk's default method, the recursive method, finds no proof for either of
them. It reports (0, 0, 0, 1), also with `-seconds 30`. The direct method
finds both classical proofs and answers `true` with confidence 1:

```sh
./bin/gk Examples/core/algebra.js -direct
./bin/gk Examples/core/logic_chain.js -direct
```

The second command needs about 8 seconds. In gk 1.2.5 the recursive
method does not find these proofs: they are measured limits of its search.

## Support for explicit negation

[`negation.js`](negation.js) gives `r(a)` two sources for it (.8 and .5) and
two against it (.7 and .3). The sources on one side combine by noisy-or:
.9 for and .79 against. gk answers `r(a)` with (.11, 0, .79, .1). Both
sides are tested against one shared number of the atom: below .79 both
pass (conflict .79), between .79 and .9 only the support for it passes
(.11), and above .9 neither passes (.1).

[`negation_conflict.js`](negation_conflict.js) places conflicting support
on `bird(a)` and propagates it through rules for `flies(a)`:

```sh
./bin/gk Examples/core/negation_conflict.js
```

```text
"answers":[{"answer":["flies","a"],"value":[0.252,0,0,0.748],...}]
```

`bird(a)` has the sources .9 and .8 for it (.98 together) and .7 against
it. Only where `bird(a)` holds without conflict, a share of .28, does the
rule of confidence .9 support `flies(a)`: .28 × .9 = .252. The route
against `flies(a)` goes through `-bird(a)`, which never holds alone, so the
share against is 0. The line has one `cycle cut` reading: the two rules
connect `bird(a)` and `flies(a)` in both signs, and gk cuts that cycle.
The reference tool gives the same value within its sampling error.

## Selected files

| File | Main feature |
|---|---|
| `algebra.js` | equational reasoning; proved by `-direct` only |
| `logic_chain.js` | Hilbert-style implication axioms with function terms; proved by `-direct` only |
| `negation.js` | positive and negative sources |
| `negation_conflict.js` | a contested premise propagated into a conclusion |

See [`../../Doc/how_gk_works.md`](../../Doc/how_gk_works.md) for how gk
reaches an answer, and
[`../../Doc/support_semantics.md`](../../Doc/support_semantics.md) for the
meaning of the four shares.
