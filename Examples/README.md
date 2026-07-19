# Tutorial

Commands in this document are run from the repository root. On Linux, `gk`
below is `./bin/gk`.

Most introductory problems are supplied in GKP (`.gkp`) and native
JSON-LD-LOGIC (`.js`) forms. The logic is the same; only the surface notation
and output format differ.

## 1. Resolution and answer substitutions

[`core/grandfather.gkp`](core/grandfather.gkp) contains two facts, one rule,
and a query with a variable:

```prolog
0.9::father(john, pete).
0.8::father(pete, mark).
0.95::grandfather(X, Z) :- father(X, Y), father(Y, Z).
query(grandfather(john, X)).
```

```sh
./bin/gk Examples/core/grandfather.gkp
```

The expected answer is:

```text
answer: mark
confidence: 0.684
```

Resolution first combines the rule with `father(pete, mark)`, then with
`father(john, pete)`. The query variable is bound to `mark`. The proof
confidence is `0.95 * 0.8 * 0.9 = 0.684`.

[`core/logic_chain.js`](core/logic_chain.js) shows a longer implication chain.
[`core/algebra.js`](core/algebra.js) and
[`core/grandfather_equality.js`](core/grandfather_equality.js) introduce
equality reasoning.

## 2. Several proofs for one answer

[`confidences/cumulate.gkp`](confidences/cumulate.gkp) gives the same fact two
independent sources:

```prolog
0.5::bird(a).
0.6::bird(a).
query(bird(a)).
```

```text
confidence: 0.8
```

For disjoint evidence the combination is noisy-or:
`1 - (1 - 0.5)(1 - 0.6) = 0.8`. When proofs share input instances, GK uses
the recorded proof supports to avoid counting the shared evidence twice.
The overlap cases are in [`confidences/overlap1.js`](confidences/overlap1.js)
and [`confidences/overlap3.js`](confidences/overlap3.js).

## 3. Evidence on both sides

[`confidences/net_direct.gkp`](confidences/net_direct.gkp) contains direct
evidence for and against one atom:

```prolog
0.7::flies(a).
0.4::-flies(a).
query(flies(a)).
```

```sh
./bin/gk Examples/confidences/net_direct.gkp -detail
```

The result has confidence `0.3`. The detailed report separates the unit mass
as follows:

```text
support: 0.3 for, 0 against
conflict: 0.4   ignorance: 0.3
```

Conflict records the part supported on both sides. Ignorance records the part
supported on neither side. [`confidences/net_premise.js`](confidences/net_premise.js)
shows how a contested premise affects a downstream conclusion.

## 4. Defaults and exceptions

[`exceptions/bird_default.gkp`](exceptions/bird_default.gkp) defines a rule
that applies unless its exception can be established:

```prolog
bird(a).
bird(b).
flies(X) :- bird(X), unless(-flies(X), 2).
query(flies(X)).
```

With no evidence for either exception, both answers have confidence 1 and
record their blocker. [`exceptions/bird_exception.gkp`](exceptions/bird_exception.gkp)
adds `0.9::-flies(a).`; the confidence for `flies(a)` becomes `0.1`, while
`flies(b)` remains at 1.

[`exceptions/nixon.gkp`](exceptions/nixon.gkp) is the Nixon diamond. Equal
defaults support `pacifist(n)` and its negation; its downstream candidate has
a zero margin and is marked contested.
[`exceptions/penguin.gkp`](exceptions/penguin.gkp) adds priorities and a strict
exception. [`exceptions/classify.gkp`](exceptions/classify.gkp) uses taxonomy
priorities:

```sh
./bin/gk Examples/exceptions/classify.gkp \
  -defaults -datafolder Examples/exceptions
```

## 5. Search strategies

GK constructs a strategy automatically when none is supplied. An explicit
strategy is useful for reproducing a search or changing clause selection:

```sh
./bin/gk Examples/core/grandfather.gkp \
  -strategy Examples/strategy/query_focus.json
```

A strategy may also contain a sequence of runs. GK tries the runs in order
until one produces an answer or the total time limit is reached:

```sh
./bin/gk Examples/core/grandfather.gkp \
  -strategy Examples/strategy/runs.json
```

See [`../Doc/strategy_reference.md`](../Doc/strategy_reference.md) for the
selection methods and limits.

## 6. Arithmetic instantiation

Ground arithmetic is evaluated during proof search. Finding a value for a
variable inside an arithmetic condition requires bounded instantiation.
[`arithmetic/apples_answer.gkp`](arithmetic/apples_answer.gkp) asks for `X` in
`X + 2 = 10`:

```sh
./bin/gk Examples/arithmetic/apples_answer.gkp -seconds 5 \
  -strategytext '{"strategy":["unit"],"query_preference":0,"arith_instantiation":1}'
```

The answer is `8` with confidence `0.8`. Mode `1` handles one arithmetic
unknown conservatively; mode `2` also considers selected two-variable cases.
This is bounded enumeration, not general equation solving.

## Categories

| Directory | Contents |
|---|---|
| [`core/`](core/README.md) | Resolution, substitutions, equality, and negation |
| [`confidences/`](confidences/README.md) | Proof products, pooling, overlap, negative evidence, conflict, and ignorance |
| [`exceptions/`](exceptions/README.md) | Defaults, blockers, priorities, taxonomies, and persistence |
| [`strategy/`](strategy/README.md) | Strategy files used with `-strategy` |
| [`arithmetic/`](arithmetic/README.md) | Ground evaluation and bounded numeric instantiation |
| [`language/`](language/README.md) | gk encodings of English reasoning problems, run against a shared knowledge base |
| [`asp_comparison/`](asp_comparison/README.md) | Current and historical bird-default inputs for gk, [clingo](https://potassco.org/clingo/), [DLV](https://www.dlvsystem.it/dlvsite/dlv/), [I-DLV](https://github.com/DeMaCS-UNICAL/I-DLV), and [s(CASP)](https://swish.swi-prolog.org/example/scasp.swinb) |
| [`system_comparison/`](system_comparison/README.md) | Executable semantic comparisons with [TweetyProject](https://tweetyproject.org/), [PASTA](https://github.com/damianoazzolini/pasta), and I-DLV |

Input notation is covered in [`../Doc/input_languages.md`](../Doc/input_languages.md).
The algorithms behind the examples are described in
[`../Doc/how_gk_works.md`](../Doc/how_gk_works.md).
