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
- four-part reports of support, opposition, conflict, and ignorance;
- shared-memory reuse of a fixed axiom set across queries;
- concurrent execution of automatically selected search strategies.

## Running GK

The distribution contains ready-to-run binaries in `bin/`:

| File | Platform |
|---|---|
| `bin/gk` | Linux x86-64, statically linked |
| `bin/gk-macos-arm64` | macOS on Apple silicon |
| `bin/gk-windows-x64.exe` | 64-bit Windows |
| `bin/gkjs.wasm` + `bin/gkjs.js` | WebAssembly, for a browser page or Node.js |

```sh
chmod +x bin/gk
./bin/gk Examples/exceptions/penguin.gkp
```

The command returns the ordinary bird `b` as flying and rejects the penguin
`p`. Run `./bin/gk -help` for the option summary and `-version` for build
information. The macOS and Windows binaries take the same arguments. The
WebAssembly build is loaded through the `gkjs.js` glue; the hosting page or
script supplies the input and reads the output.

## Example

`Examples/exceptions/penguin.gkp` contains:

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

The priority-3 bird default derives `flies(b)`. The lower-priority object
default does not defeat it. The strict penguin rule derives `-flies(p)`, so
`p` is rejected as an answer to `flies(X)`.

```text
answer: b
confidence: 1

rejected answer: p
confidence against: 1
```

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
```

The example categories are classical reasoning, confidence calculation,
defaults and exceptions, arithmetic, proof-search strategy, and
natural-language reasoning.

## Development

GK is developed by Tanel Tammet, with database technology contributions by
Priit Järv and conceptual ideas by Tanel Tammet, Priit Järv, and Dirk Draheim.
