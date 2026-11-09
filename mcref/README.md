# mcref: the reference tool of the support semantics

`mcref` estimates the four shares of an answer by sampling worlds. It
computes the support semantics of [`Doc/support_semantics.md`](../Doc/support_semantics.md),
the semantics that gk's recursive method approximates. It is a standalone
Python 3 program without third-party packages. It calls no prover and shares
no code with gk. For gk's clause notations it runs gk's parser only:
`gk INPUT -writejson -recursive`.

- What the tool computes, what it declines, its output and its comparison
  with gk: [`Doc/mcref.md`](../Doc/mcref.md).
- Version 1.1.1 (2026-11-09). It gives the same counts as version 1.1.0 of
  2026-11-03.

## Files

| file | content |
|---|---|
| `mcref_read.py` | reading the input, conversion with gk's parser, clauses, grounding |
| `mcref.py` | applications, the static passes, one world, the narrowing, the state rows, sampling, the output |

## Running the tool

From the repository root:

```sh
python3 mcref/mcref.py Examples/semantics/default_vs_fact.gkp --samples 20000
```

The answer is `flies(t)` with the shares (.627, .302, 0, .071), each within
±.0113. gk gives (.63, .3, 0, .07) for the same input.

```
python3 mcref/mcref.py INPUT [--samples N] [--seed N] [--max-ground N] [--all-atoms]
```

| option | meaning | default |
|---|---|---|
| `INPUT` | a gk input: JSON-LD-LOGIC (`.js`, `.json`), or GKP, GKS or TPTP, converted by `gk INPUT -writejson -recursive` | |
| `--samples N` | the number of sampled worlds | 100000 |
| `--seed N` | the seed of the random numbers (splitmix64) | 1 |
| `--max-ground N` | the limit of the grounding work; above it the input is `unsupported: grounding limit` | 200000 |
| `--all-atoms` | also report every ground atom, in `atom_values` | off |

The tool runs `bin/gk` of this repository as the parser. On macOS or
Windows, or for another binary, name it with the environment variable
`MCREF_GK`:

```sh
MCREF_GK=bin/gk-macos-arm64 python3 mcref/mcref.py Examples/semantics/penguin.gkp
```

A JSON input needs no parser. The same input, seed and sample count give
the same counts.

## Output

The tool prints one JSON line, `{"mcref": {...}}`. Its main fields:

| field | meaning |
|---|---|
| `answers` | one entry per ground instance of the question: `instance`, `key`, `binding`, `counts` (positive, negative, conflict, ignorance, unresolved), `value`, `unstable`, `interval_95` |
| `value` | the four shares (for, against, conflict, ignorance) |
| `unstable` | the unresolved share; the four shares sum to one minus it |
| `interval_95` | per share `p ± e`, with e = √(ln(8 / .05) / (2N)): 95 % for the four shares of one answer together; .0113 at 20,000 samples and .0050 at 100,000 |
| `unsupported` | `null`, or the reason the input is declined, with no value |
| `readings` | the applications dropped by the self-exception rule |
| `interpretation` | the reading of the semantics that the run used |
| `provenance` | the sha256 of the tool and of every file read |

[`Doc/mcref.md`](../Doc/mcref.md) Section 11.4 lists every field, and
Section 6 lists the reasons for declining an input.

## What the tool declines

The tool grounds over the constants of the input. It declines, among
others, inputs with function symbols, equality, taxonomy priorities, rank
contexts or a built-in over an open domain, and inputs whose grounding
exceeds `--max-ground`. The `unsupported` field names the reason.

The tool is the reference for gk's default, the recursive method. The two
older sampling programs in [`../montecarlo/`](../montecarlo/README.md)
check the direct method (`gk -direct`).
