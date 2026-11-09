# GK Reasoner

GK is a first-order reasoner for uncertain facts, opposing evidence,
defaults, exceptions and contradictions. For a question it reports four
shares: support for the statement, support against it, conflict and
ignorance. GK works on clauses with variables, function terms, equality,
classical disjunction and explicit negation. The current version is 1.2.4.

This repository holds the GK binaries, the user documentation, the
examples, the taxonomy data and the reference tool `mcref`. The source code
is in a separate repository.

GK extends the resolution prover [GKC](https://github.com/tammet/gkc) with:

- confidences on facts and rules;
- evidence for and evidence against a statement, kept apart;
- default rules with exceptions and ranks;
- the recursive method: starting from a proof, recursive searches for
  support, opposition and exceptions, with smaller time allowances at
  greater depth;
- one calculation of the four shares over all the evidence found, with
  shared evidence counted once;
- shared-memory reuse of a fixed axiom set across queries (native builds);
- concurrent execution of automatically selected search strategies (Unix).

A web version of GK, with examples and documentation, runs in the browser
at [https://logictools.org/commonsense.html](https://logictools.org/commonsense.html);
no installation is needed.

## Running GK

Prebuilt binaries for Linux x86-64, macOS on Apple silicon, Windows x64 and
WebAssembly are in `bin/`. On Linux:

```sh
chmod +x bin/gk
./bin/gk Examples/exceptions/penguin.gkp
```

Run `./bin/gk -help` for the option summary. The native binaries use the
same command-line interface. [`bin/README.md`](bin/README.md) covers the
other platforms, the browser build and its limits.

## Example

[`Examples/semantics/default_vs_fact.gkp`](Examples/semantics/default_vs_fact.gkp)
has a default and an uncertain fact against it:

```prolog
bird(t).
0.3::-flies(t).
0.9::flies(X) :- bird(X), unless(-flies(X), 2).
query(flies(t)).
```

```sh
./bin/gk Examples/semantics/default_vs_fact.gkp
```

GK prints one line that starts with `{"recursive":`, then a dump of the
evidence. Shortened, the line is:

```text
{"recursive":{"method":"recursive","question":"flies(t)",
 "value":[0.63,0.3,0,0.07],"value_from":"checkpoint 2",...}}
```

The value is (for, against, conflict, ignorance) = (.63, .3, 0, .07). The
default "birds fly" yields to the contrary evidence: where `-flies(t)` holds
(.3 of the cases) the answer is against. In the other .7 the default gives
support .9, so .7 × .9 = .63 is for, and the remaining .07 is ignorance.
With an ordinary rule `0.9::flies(X) :- bird(X)` in place of the default,
the two sides fight instead, and the value is (.6, 0, .3, .1).

## How GK answers

1. GK searches for a proof of the question with resolution and
   paramodulation.
2. It turns the proof into **applications**: one use of one input clause,
   with its conditions, exceptions and confidence.
3. It starts searches for opposition to each conclusion, for further
   support and opposition at each condition, and for each exception. Each
   proof found adds applications and searches of its own. Searches deeper
   in the proof get smaller time allowances.
4. At intervals, one calculation over all the applications found gives the
   four shares. Shared evidence counts once.
5. GK returns the latest completed calculation, with notes on what it does
   not include: searches cut by the time budget, and the approximations
   that the calculation applied.

[`Doc/how_gk_works.md`](Doc/how_gk_works.md) describes the method on
examples. `./bin/gk INPUT -direct` runs the older direct method of
gk 1.1.2 ([`Doc/direct_method.md`](Doc/direct_method.md)).

## What the four shares mean

The meaning of the four shares is defined by the **support semantics**
([`Doc/support_semantics.md`](Doc/support_semantics.md)), on examples and
then as precise rules. GK's recursive method approximates this semantics
and says where its value can differ. The reference tool
[`mcref`](mcref/README.md) computes the semantics by sampling worlds. It
shares no code with GK's proof search:

```sh
python3 mcref/mcref.py Examples/semantics/default_vs_fact.gkp --samples 20000
```

It reports (.627, .302, 0, .071), each share within ±.0113 at 20,000
samples. [`Doc/mcref.md`](Doc/mcref.md) describes the tool and its
comparison with GK.

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
[`Doc/json_ld_logic.md`](Doc/json_ld_logic.md) specifies the native format.

## English-language reasoning

The
[llmpipe commonsense-reasoning system](https://github.com/tammet/nlpsolver/tree/main/llmpipe)
translates English into GK logic and uses GK as its reasoning engine. The
resulting logic and runnable examples are described in
[`Examples/language/`](Examples/language/README.md). The
[nlformtasks collection](https://github.com/tammet/nlformtasks) provides a
larger set of language-translation examples runnable by GK.

## Documentation

| Document | Contents |
|---|---|
| [`Examples/README.md`](Examples/README.md) | Tutorial based on runnable examples |
| [`Doc/support_semantics.md`](Doc/support_semantics.md) | What the four shares mean: the support semantics, on examples, and its rules stated precisely |
| [`Doc/how_gk_works.md`](Doc/how_gk_works.md) | How GK reaches an answer with the recursive method |
| [`Doc/recursive_output.md`](Doc/recursive_output.md) | The output: the `{"recursive": ...}` line, the readings and the status facts |
| [`Doc/mcref.md`](Doc/mcref.md) | The reference tool `mcref` and its comparison with GK |
| [`Doc/input_languages.md`](Doc/input_languages.md) | Facts, rules, questions, defaults and confidences in each notation |
| [`Doc/json_ld_logic.md`](Doc/json_ld_logic.md) | The JSON-LD-LOGIC format |
| [`Doc/cli_reference.md`](Doc/cli_reference.md) | Command-line options |
| [`Doc/strategy_reference.md`](Doc/strategy_reference.md) | Automatic search and strategy files |
| [`Doc/comparison_with_other_systems.md`](Doc/comparison_with_other_systems.md) | Comparisons with other reasoners |
| [`Doc/direct_method.md`](Doc/direct_method.md) | The direct method of gk 1.1.2 (`-direct`) |
| [`Examples/semantics/README.md`](Examples/semantics/README.md) | The inputs of the support semantics page, with their answers |
| [`Examples/language/README.md`](Examples/language/README.md) | Logic generated from English-language inputs |
| [`comparisons/README.md`](comparisons/README.md) | Inputs, classifications and captured outputs of the comparison table |
| [`montecarlo/README.md`](montecarlo/README.md) | The two sampling checks of the direct method |

## Repository layout

```text
bin/          GK executables for each platform
data/         taxonomy data for -taxonomy, with its builder
Doc/          user documentation
Examples/     example problems grouped by feature
mcref/        the reference tool of the support semantics
montecarlo/   the sampling checks of the direct method
comparisons/  comparison table inputs, classifications and outputs
```

## Papers

The support semantics and the recursive method of gk 1.2 are described in:

- T. Tammet. *Reasoning with Uncertain Evidence, Opposition and
  Exceptions: Support Semantics in Three Layers and a First-Order
  Inference Method.* In preparation, 2026.
  [`Doc/support_semantics.md`](Doc/support_semantics.md) states its
  semantics.

Older versions of GK are described in:

- [Structure-Preserving Uncertainty Propagation in First-Order Proof Search](https://arxiv.org/abs/2608.09190)
  (2026). It describes GK as of July 2026, whose calculation became the
  direct method, which gk 1.2 runs with `-direct`. It does not describe
  the recursive method, the default since gk 1.2.0, or the support
  semantics.
- [GK: Implementing Full First Order Default Logic for Commonsense Reasoning (System Description)](https://doi.org/10.1007/978-3-031-10769-6_18)
  (2022).
- [Confidences for Commonsense Reasoning](https://doi.org/10.1007/978-3-030-79876-5_29)
  (2021).

The underlying resolution prover is described in:

- [GKC: A Reasoning System for Large Knowledge Bases](https://doi.org/10.1007/978-3-030-29436-6_32)

## Development

GK is developed by Tanel Tammet, with database technology contributions by
Priit Järv and conceptual ideas by Tanel Tammet, Priit Järv, and Dirk Draheim.
