# mcref: the reference tool of the support semantics

`mcref` computes the support report of a question as the support semantics
of [`Doc/support_semantics.md`](../Doc/support_semantics.md) defines it. It
has two methods: exact evaluation, which gives the report itself, and
sampling, which gives an estimate with an error bound. It is a standalone
Python 3 program without third-party packages. It calls no prover and
shares no code with gk. For gk's clause notations it runs gk's parser only:
`gk INPUT -writejson -recursive`.

- What the tool computes, its two methods, what it declines, its output and
  its comparison with gk: [`Doc/mcref.md`](../Doc/mcref.md).
- This is version 1.3.1. Versions 1.1.0 to 1.1.2 computed an earlier form
  of the definition, without the proofs of several statements and without
  the exception pass in layers; records made with them keep their values.
  Version 1.3.0 let a proof outside a cycle group read, for a listed clause
  of the group, the setting of the last round of the clause rule, or
  "cannot be decided" when the rule had no result; version 1.3.1 gives that
  proof the check of the clause on the final states.

## Files

| file | content |
|---|---|
| `mcref.py` | the command; the applications of the ground statements, the narrowing, the procedures of the groups, the clause rule in a cycle, the exception pass, sampling, the output |
| `mcref_apps.py` | the single applications, the applications of the proofs of several statements, the conclusions by cases of `--cases` |
| `mcref_proofs.py` | the search for the proofs of several statements: resolution with dependency lists |
| `mcref_graph.py` | the passes before any world: the reachable literals, no self-support, the rank-context check, the cycle groups |
| `mcref_tables.py` | the state of one atom: the support of a side, the table of the states, the selections of a side |
| `mcref_texts.py` | the texts of the output field `interpretation` |
| `mcref_read.py` | reading the input, conversion with gk's parser, statements, grounding |
| `mcref_exact.py` | exact evaluation: one world per cell |

## Running the tool

From the repository root:

```sh
python3 mcref/mcref.py Examples/semantics/default_vs_fact.gkp
```

The tool evaluates the input exactly. The answer is `flies(t)` with the
shares (.63, .3, 0, .07), the value that gk gives for the same input.

```
python3 mcref/mcref.py INPUT [--mode auto|exact|sampling] [--max-cells N]
                             [--samples N] [--seed N] [--max-ground N] [--all-atoms]
```

| option | meaning | default |
|---|---|---|
| `INPUT` | a gk input: JSON-LD-LOGIC (`.js`, `.json`), or GKP, GKS or TPTP, converted by `gk INPUT -writejson -recursive` | |
| `--mode auto` | exact evaluation when the cells are at most `--max-cells`, sampling above it | the default |
| `--mode exact` | exact evaluation only; above the cell limit the output names the cells and gives no value | |
| `--mode sampling` | sampling only | |
| `--max-cells N` | the cell limit of exact evaluation | 300000 |
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

A JSON input needs no parser. With sampling, the same input, seed and
sample count give the same counts.

## Output

The tool prints one JSON line, `{"mcref": {...}}`. The main fields of both
methods:

| field | meaning |
|---|---|
| `mode` | `exact` or `sampling`: the method that computed the answers |
| `answers` | one entry per ground instance of the question: `instance`, `value`, `unstable`, and `binding` for a question with variables |
| `value` | the four shares (positive, negative, conflict, ignorance) |
| `unstable` | the share of worlds where the atom has no value; the four shares sum to one minus it |
| `error_bound` | 0 for exact evaluation; for sampling, the half-width of the 95 % interval of each share |
| `cells` | exact evaluation: the number of cells; `too_many_cells` names the cells when they pass the limit |
| `worlds` | sampling: the number of sampled worlds; `exact_not_used` says why exact evaluation was not used |
| `unsupported` | `null`, or the reason the input is declined, with no value |
| `readings` | the notes of the run: the applications of proofs of several statements, a proof limit, the self-exception rule, the clause rule in a cycle without a result |
| `proofs` | the counts of the search for proofs of several statements |

Sampling adds the fields `counts`, `interval_95` and `key` to each answer,
and `interpretation`, `provenance` and the counts of the input
(`ground_clauses`, `applications`, ...) to the output.
[`Doc/mcref.md`](../Doc/mcref.md) Section 7 lists every field; Section 6
lists the reasons for declining an input.

Exit status: 0 with the JSON line; 2 for a usage error; 3 for an internal
error, a sweep group whose sweeps did not settle within the bound of the
sweep lemma, with a message on stderr that names the input and the group.

## What the tool declines

The tool grounds over the constants of the input. It declines, among
others, inputs with function symbols, equality, taxonomy strengths, rank
contexts or a built-in over an open domain, and inputs whose grounding
passes `--max-ground`. The `unsupported` field names the reason.

The tool is the reference for gk's exact method and general method. The two
older sampling programs in [`../montecarlo/`](../montecarlo/README.md)
check the direct method (`gk -direct`).

## Options for tests and comparisons

| option | meaning |
|---|---|
| `--rules 1.1` | without the proofs of several statements and without the layers of the exception pass; `--proofs` and `--layers` then turn each part on |
| `--cases` | with `--rules 1.1`: proofs by cases from the classical clauses, an earlier way to represent conclusions of several statements |
| `--backbone fix` | with `--rules 1.1`: a variant of the backbone step that keeps the states it establishes |
| `--ranks` | a candidate rule for ranks across atoms; not part of the definition |

Environment switches, each on by default and off with the value 0, turn
single rules of the definition off for tests: `LIFT_UND` (an uncertain
normal default takes part in proofs with its rule identity), `MCREF_B2`
(two choices of constants give two ground statements), `MCREF_B3` (a
proof is searched for a literal that one statement holds when its single
application does not absorb the proof), `BLOCKED_REPAIR` (absent
applications are absent from the whole preparation), `CIRCLE_KEEP` (the
clause rule without a result keeps the atoms that do not change) and
`READHEAD` (the head read from a default, for JSON input).

`python3 mcref/mcref_exact.py INPUT --proofs --layers [--all-atoms] [--max-cells N]`
runs exact evaluation alone and prints `{"exact": {...}}`; without
`--proofs --layers` it computes the rules of `--rules 1.1`.

The acceptance cases of the tool (151 cases in seven sets, each with an
expected value from a hand calculation) and its comparison script are in
gk's source repository.
