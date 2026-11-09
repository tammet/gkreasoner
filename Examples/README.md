# Tutorial

Commands in this document are run from the repository root. On Linux, `gk`
below is `./bin/gk`.

Most introductory problems are supplied in GKP (`.gkp`) and native
JSON-LD-LOGIC (`.js`) forms. The logic is the same; only the surface notation
differs.

gk 1.2.4 answers with the recursive method by default. It prints one line
that starts with `{"recursive":`, then a dump of the evidence. The line's
`value` holds the four shares in the order (for, against, conflict,
ignorance). A question with a variable gets an `answers` list, one entry per
instance. [`../Doc/recursive_output.md`](../Doc/recursive_output.md)
describes the output, and
[`../Doc/support_semantics.md`](../Doc/support_semantics.md) the meaning of
the four shares. The values below are gk 1.2.4's, shortened.

## 1. Defaults and answer substitutions

[`exceptions/penguin.gkp`](exceptions/penguin.gkp) asks which objects fly:

```prolog
bird(b).
penguin(p).
bird(X)   :- penguin(X).
object(X) :- bird(X).
-flies(X) :- penguin(X).
flies(X)  :- bird(X),   unless(-flies(X), 3).
-flies(X) :- object(X), unless(flies(X), 2).
query(flies(X)).
```

```sh
./bin/gk Examples/exceptions/penguin.gkp
```

The ordinary bird default has rank 3 and the opposing object default has
rank 2. The certain penguin rule supplies the exception:

```text
"answers":[{"answer":"flies(b)","value":[1,0,0,0]},
           {"answer":"flies(p)","value":[0,1,0,0]}]
```

[`core/logic_chain.js`](core/logic_chain.js) shows a longer implication chain.
[`core/algebra.js`](core/algebra.js) introduces equality reasoning. The
recursive method finds no proof for either of them; see
[`core/README.md`](core/README.md).

## 2. Several proofs for one answer

[`confidences/cumulate.gkp`](confidences/cumulate.gkp) states the same fact
from two distinct uncertain sources:

```prolog
0.5::bird(a).
0.6::bird(a).
query(bird(a)).
```

```text
"value":[0.8,0,0,0.2]
```

The two statements are two independent sources, so they combine by
noisy-or: `1 - (1 - 0.5)(1 - 0.6) = 0.8`. When proofs share a source, gk
counts the shared source once. The overlap cases are in
[`confidences/overlap1.js`](confidences/overlap1.js) and
[`confidences/overlap3.js`](confidences/overlap3.js).

## 3. Evidence on both sides

[`confidences/net_direct.gkp`](confidences/net_direct.gkp) contains direct
evidence for and against one atom:

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

Both sides are tested against one shared number of the atom. Where the
number lies below .4, both sides pass: conflict .4. Between .4 and .7, only
the stronger side passes: for .3. Above .7, neither side passes: ignorance
.3. The weaker side never wins alone. The signed confidence, for minus
against, is .3.

[`confidences/net_premise.js`](confidences/net_premise.js) shows how a
contested premise affects a downstream conclusion.

## 4. Defaults and exceptions

[`exceptions/bird_default.gkp`](exceptions/bird_default.gkp) defines a rule
that applies unless its exception can be established:

```prolog
bird(a).
bird(b).
flies(X) :- bird(X), unless(-flies(X), 2).
query(flies(X)).
```

With no evidence for either exception, `flies(a)` and `flies(b)` are both
(1, 0, 0, 0). [`exceptions/bird_exception.gkp`](exceptions/bird_exception.gkp)
adds `0.9::-flies(a).`: the default yields to the contrary fact, so
`flies(a)` is (.1, .9, 0, 0), while `flies(b)` stays (1, 0, 0, 0).

[`exceptions/nixon.gkp`](exceptions/nixon.gkp) is the Nixon diamond. The
equal-rank defaults block each other, so neither side is usable and the
downstream question `dislikeswar(n)` is (0, 0, 0, 1): ignorance, not
conflict. [`exceptions/penguin.gkp`](exceptions/penguin.gkp) adds ranks and a
certain exception. [`exceptions/classify.gkp`](exceptions/classify.gkp) uses
taxonomy priorities:

```sh
./bin/gk Examples/exceptions/classify.gkp \
  -taxonomy -datafolder data
```

It answers `isa(b1,organism)` (.5731, .0179, .3821, .0269) and
`isa(a1,organism)` (0, .4, .6, 0), with two `cycle cut` readings.

## 5. Search strategies

gk constructs a strategy automatically when none is supplied. An explicit
strategy is useful for reproducing a search or changing clause selection:

```sh
./bin/gk Examples/exceptions/penguin.gkp \
  -strategy Examples/strategy/query_focus.json
```

A strategy may also contain a sequence of runs. gk tries the runs in order
until one produces an answer or the total time limit is reached:

```sh
./bin/gk Examples/exceptions/penguin.gkp \
  -strategy Examples/strategy/runs.json
```

Both give the answers of Section 1. See
[`../Doc/strategy_reference.md`](../Doc/strategy_reference.md) for the
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

The answer is `johnhad(8)` with (.8, 0, 0, .2). The arithmetic step is not
replayed as an application, so the line reports it among `pending_steps`.
Mode `1` instantiates one arithmetic unknown from a bounded candidate range;
mode `2` also considers selected two-variable cases. The mode is bounded
enumeration; it does not solve general equations.

## 7. Checking a value with the reference tool

The reference tool [`mcref`](../mcref/README.md) computes the support
semantics by sampling worlds. It shares no code with gk's proof search.
[`semantics/default_vs_fact.gkp`](semantics/default_vs_fact.gkp) has a
default and a weaker fact against it:

```prolog
bird(t).
0.3::-flies(t).
0.9::flies(X) :- bird(X), unless(-flies(X), 2).
query(flies(t)).
```

gk answers (.63, .3, 0, .07). The tool, with 20,000 samples:

```sh
python3 mcref/mcref.py Examples/semantics/default_vs_fact.gkp --samples 20000
```

```text
"value": [0.62695, 0.30225, 0.0, 0.0708]
```

Its sampling error is at most ±.0113 per share at 20,000 samples, so the
two agree. [`semantics/`](semantics/README.md) holds all the inputs of the
semantics page with their values.

## Categories

| Directory | Contents |
|---|---|
| [`core/`](core/README.md) | Resolution, substitutions, equality, and negation |
| [`confidences/`](confidences/README.md) | Uncertain facts and rules, several proofs, shared sources, evidence against, conflict, and ignorance |
| [`exceptions/`](exceptions/README.md) | Defaults, exceptions, ranks, taxonomies, and persistence |
| [`semantics/`](semantics/README.md) | The inputs of the support semantics page, one per example, with their values |
| [`strategy/`](strategy/README.md) | Strategy files used with `-strategy` |
| [`arithmetic/`](arithmetic/README.md) | Ground evaluation and bounded numeric instantiation |
| [`language/`](language/README.md) | GK encodings of English reasoning problems, run against a shared knowledge base |
| [`asp_comparison/`](asp_comparison/README.md) | Bird-default inputs for gk, [clingo](https://potassco.org/clingo/), [DLV](https://dlv.demacs.unical.it/), [I-DLV](https://github.com/DeMaCS-UNICAL/I-DLV), and [s(CASP)](https://gitlab.software.imdea.org/ciao-lang/sCASP), with a scaling workload |
| [`fol_comparison/`](fol_comparison/README.md) | Non-Horn first-order clause problems with equality and function terms, with runs of other reasoners on the same inputs |
| [`system_comparison/`](system_comparison/README.md) | Executable semantic comparisons with [TweetyProject](https://tweetyproject.org/), [PASTA](https://github.com/damianoazzolini/pasta), and I-DLV |

The comparison cases, with captured outputs from the external systems, are
in [`../comparisons/`](../comparisons/README.md); their per-case
descriptions are in [`../comparisons/CASES.md`](../comparisons/CASES.md).

Input notation is covered in [`../Doc/input_languages.md`](../Doc/input_languages.md)
and [`../Doc/json_ld_logic.md`](../Doc/json_ld_logic.md).
How gk reaches an answer is described in
[`../Doc/how_gk_works.md`](../Doc/how_gk_works.md).
