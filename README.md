# GK Reasoner

GK is a first-order reasoner for knowledge bases containing uncertain facts,
default rules, exceptions, and contradictions. It returns logical proofs and a
confidence assessment for each answer.

GK extends the resolution prover [GKC](https://github.com/tammet/gkc) with:

- confidence annotations on facts and rules;
- combination of several proofs without double-counting shared evidence;
- separate treatment of evidence for and against a conclusion;
- default rules whose exceptions are checked by subsidiary proof searches;
- numeric priorities and taxonomy-based priorities for competing defaults;
- four-part reports of support, opposition, conflict, and ignorance.

The bundled executable is beta software. The source code of GK is not part of
this repository.

## Running GK

The current distribution contains a statically linked Linux x86-64 binary:

```sh
chmod +x bin/gk
./bin/gk Examples/core/grandfather.gkp
```

The command returns the substitution `mark`, a confidence of `0.684`, and the
resolution proof. Run `./bin/gk -help` for the built-in option
summary and `-version` for build information.

The executable requires a 64-bit x86 Linux system. Binaries for other
platforms are not included in this revision.

## Example

`Examples/core/grandfather.gkp` contains:

```prolog
0.9::father(john, pete).
0.8::father(pete, mark).
0.95::grandfather(X, Z) :- father(X, Y), father(Y, Z).
query(grandfather(john, X)).
```

The proof uses both facts and the rule. Their confidences multiply:

```text
0.9 * 0.8 * 0.95 = 0.684
```

The same problem is available as `Examples/core/grandfather.gks` in the
premise-to-consequence notation and as `Examples/core/grandfather.js` in GK's
native JSON-LD-LOGIC representation.

## Input formats

GK accepts four input notations:

| Notation | Typical suffix | Purpose |
|---|---|---|
| GKP | `.gkp`, `.pl`, `.pro`, `.prolog` | Prolog-style notation for hand-written problems |
| JSON-LD-LOGIC | `.js` | Native representation |
| GKS | `.gks` | Premise-to-consequence notation using `=>` |
| TPTP CNF | `.p`, `.ax`, `.tptp`, `.cnf` | Clause-normal-form problems and interchange |

The formats and their correspondence are described by examples in
[`Doc/input_languages.md`](Doc/input_languages.md).

## English-language reasoning

The
[llmpipe commonsense-reasoning system](https://github.com/tammet/nlpsolver/tree/main/llmpipe)
automatically translates English into gk logic and uses gk as its reasoning
engine. The resulting logic and runnable examples are described in
[`Examples/language/`](Examples/language/README.md). The
[nlformtasks collection](https://github.com/tammet/nlformtasks) provides a
larger set of language-translation examples runnable by gk.

## Documentation

| Document | Contents |
|---|---|
| [`Examples/README.md`](Examples/README.md) | Tutorial based on runnable examples |
| [`Doc/input_languages.md`](Doc/input_languages.md) | Facts, rules, queries, defaults, and confidence annotations in each input notation |
| [`Doc/how_gk_works.md`](Doc/how_gk_works.md) | Resolution, proof confidence, evidence combination, contradictions, and defaults |
| [`Doc/cli_reference.md`](Doc/cli_reference.md) | Command-line options |
| [`Doc/strategy_reference.md`](Doc/strategy_reference.md) | Automatic search and strategy files |
| [`Doc/comparison_with_other_systems.md`](Doc/comparison_with_other_systems.md) | Scoped comparison with [ProbLog](https://dtai.cs.kuleuven.be/problog/editor.html), [PASTA](https://github.com/damianoazzolini/pasta), [TweetyProject](https://tweetyproject.org/), [clingo](https://potassco.org/clingo/), [DLV](https://www.dlvsystem.it/dlvsite/dlv/), [I-DLV](https://github.com/DeMaCS-UNICAL/I-DLV), and [s(CASP)](https://swish.swi-prolog.org/example/scasp.swinb) |
| [`montecarlo/README.md`](montecarlo/README.md) | Estimating the confidence numbers by Monte-Carlo sampling, as an independent check |

## Repository layout

```text
bin/         GK executables
Doc/         user documentation
Examples/    example problems grouped by feature
montecarlo/  Monte-Carlo checks of the confidence numbers
LICENSE      distribution and use terms
```

The example categories are classical reasoning, confidence calculation,
defaults and exceptions, arithmetic, proof-search strategy, and
natural-language reasoning.

## Licence

GK may be used, copied, and redistributed for experimentation, evaluation,
research, and education, subject to the conditions in [`LICENSE`](LICENSE).
Other uses require prior written permission from Tanel Tammet. The software is
distributed without warranty.

GK is developed by Tanel Tammet, with contributions by Priit Järv.
