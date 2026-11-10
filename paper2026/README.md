# Inputs and results of the paper

This folder lets a reader rerun the examples and experiments of the paper

> Tanel Tammet. Reasoning with Uncertain Evidence, Opposition and
> Exceptions: Support Semantics in Three Layers and a First-Order Inference
> Method. Submitted to the Journal of Artificial Intelligence Research, 2026.

It holds the input of every run, the encodings for the other systems, the
commands, the list of runs, and the results in brief: one row per result,
with the value that the paper prints and the value of the stored run. It
holds no code of the external systems. [`SYSTEMS.md`](SYSTEMS.md) says
where to get each system and how to install it.

The **full dataset** adds the raw output of every run (standard output,
standard error, exit status, time and memory), the saved outputs of the
external systems, the gk binary and the reference tool. It is archived at
Zenodo: <https://doi.org/10.5281/zenodo.XXXXXXX>. This folder is the full
dataset without the raw outputs, the binary and the tool.

## Quick start

From the root of this repository, on Linux x86-64:

```sh
./bin/gk paper2026/O1_tweety/stage3a/gk.gkp
python3 mcref/mcref.py paper2026/O1_tweety/stage3a/gk.gkp --samples 20000 --seed 1
python3 paper2026/check_gk.py --part O1 --mcref
```

The first command answers stage 3a of the Tweety example: the field
`value` of the first output line is `[0.6984,0.224,0,0.0776]`, the four
shares (for, against, conflict, ignorance) of the Tweety table. The second command
estimates the same shares with the reference tool. The third command
reruns every gk and mcref run of part O1 and compares each with the
recorded value. Without `--part` it reruns every part; that takes about
one hour.

The binaries for macOS, Windows and the browser are in
[`../bin/`](../bin/README.md). The browser version at
<https://logictools.org/commonsense.html> runs gk without installation.
The results here come from the native Linux binary; the other builds were
not checked on them.

## Where each result of the paper is

| paper | part | folder |
|---|---|---|
| Section 2, the Tweety table: the Tweety stages; the tool's estimates of Section 5; the printed proof | O1 | [`O1_tweety/`](O1_tweety/README.md) |
| Section 7.1: gk against the reference tool, 375 of 394 rows | O2 | [`O2_record/`](O2_record/README.md) |
| Section 7.2, the families tables: benchmark families | O3 | [`O3_families/`](O3_families/README.md) |
| Section 7.3, the five-inputs table: five inputs under the quantities of the systems | O4 | [`O4_quantities/`](O4_quantities/README.md) |
| Section 7.4: what each system can state; the families tables, the five cases of the earlier table | O5 | [`O5_comparisons/`](O5_comparisons/README.md), the run lists for the earlier comparison table [`../comparisons/`](../comparisons/README.md) |
| Section 7.4: the time budget | O6 | [`O6_budget/`](O6_budget/README.md) |
| Section 7.2: the English case | O7 | [`O7_english/`](O7_english/README.md) |
| Appendix A: further examples of cycles | O8 | [`O8_cycles/`](O8_cycles/README.md) |
| the recursive method in detail | O9 | [`../Doc/how_gk_works.md`](../Doc/how_gk_works.md), [`../Doc/recursive_output.md`](../Doc/recursive_output.md) |
| the reference tool in detail | O10 | [`../Doc/mcref.md`](../Doc/mcref.md) |
| Sections 1 and 4 to 6, Appendix A: the small examples; the snapshot table | O11 | [`O11_text_examples/`](O11_text_examples/README.md) |
| Section 7.1, the notes table | O2 | [`O2_record/`](O2_record/README.md) |
| Section 7.5, the summary table; the run times | O3 | collects the parts above; the run times in [`O3_families/`](O3_families/README.md) |


## The paper's tables and figures

The parts name the paper's tables and figures by the names of the first
column. The second column gives their numbers in version 5 of the paper
(draft of 2026-11-10); a renumbering of the paper changes this table only.

| name in this folder | in the paper | section |
|---|---|---|
| the Tweety table | Table 1 | Section 2 |
| the snapshot table | Table 5 | Section 6.2 |
| the printed proof | Figure 4 | Section 6.5 |
| the systems table | Table 6 | Section 7 |
| the notes table | Table 7 | Section 7.1 |
| the families tables: families reached | Table 8a | Section 7.2 |
| the families tables: families not reached | Table 8b | Section 7.2 |
| the five-inputs table | Table 9 | Section 7.3 |
| the summary table | Table 10 | Section 7.5 |

A row of the families tables is named by its family, for example
"families reached: delivery". The words follow version 5: a search
stopped by the budget is *stopped*, gk's notes are *approximation notes*
(the output field `readings`), and a row on which the tool's unresolved
share is 0 is a *resolved* row.

## How a part is organized

Each part folder has a `README.md` that reproduces the paper's table or
values with the file of each cell, the commands, and notes on the
encodings. Each part also has two tab-separated tables.

`runs.tsv` lists the runs of gk, of the reference tool, and of the
external systems that were run again for this folder:

| column | content |
|---|---|
| `run_id` | the run's name within the part |
| `tool` | `gk`, `mcref`, or an external system |
| `input` | the input file, relative to the part folder |
| `options` | the options; `{input}` marks the place of the input file, `{outdir}` a folder of the run's own |
| `settings` | for mcref the number of worlds and the seed; for an external system its version |
| `alone` | `yes` for a run whose value or quoted time can depend on gk's deadline or on the machine load; such a run ran with no other run active |
| `timeout_s` | the runner's limit in seconds |

Each command runs in the folder of its input file. gk runs without
options unless the row names some: its default is the recursive method,
a deadline of 10 s and the automatic choice of search strategy.

`results.tsv` has one row per result:

| column | content |
|---|---|
| `id` | the row's name within the part |
| `paper` | where the paper prints the result |
| `system` | the system and its version |
| `input`, `options` | the input file and the options of the run |
| `kind` | `run` (a system printed the value), `enumerated` (computed from the system's published semantics by `tools/enumerate_answer_sets.py`), `estimate` (mcref), `target` (a value from an exact calculation, an external solver or a hand calculation), `no answer`, `failed`, `declined`, `not run`, `no encoding` |
| `relation` | for an external encoding: `exact translation`, `non-equivalent analogue`, `grounding test` and others, as the part README defines |
| `result` | the value as the paper prints it |
| `note` | remarks: the reason for a failure, the source of a value |
| `run` | the `run_id` of the run that produced the value |
| `stored` | the value that the stored run printed, at the precision of the system |
| `measured` | the stored run's wall time and, for gk, the searches stopped by the budget, the applications, the approximation notes (the output field `readings`) and the checkpoint of the value |

Parts O8 and O11 add the columns `question`, `target` (the value of the
semantics as the paper or the part README states it) and `target_check`.
Part O2 has a third table, `rows.tsv`, with one row per answer.

gk prints four shares (for, against, conflict, ignorance), written
(.396, .56, 0, .044). Other systems print other quantities: a probability
(ProbLog, plingo), a lower and an upper probability (PASTA), or true,
false and inconsistent mass (smProbLog). Section 2 of the paper explains
why these numbers are not approximations of one another.

## Versions and runs

Every gk and mcref value, time and note of this folder comes from a run of
gk 1.2.5 and mcref 1.1.2 on 2026-11-10, the versions in this repository.
The earlier runs of the paper's drafts used gk 1.2.3 and mcref 1.1.0; the
part READMEs name every value that changed. mcref 1.1.2 computes the
cycle rule of 2026-11-10 and changed five values of part O3. The external systems keep
their recorded runs of 2026-11-04 and 2026-11-08, with the versions in
`SYSTEMS.md` and in each `results.tsv`. The runs whose outputs had not
been saved were run again on 2026-11-10 with the same versions and
limits; the part READMEs name them.

The runs were made by `tools/run_store.py`, which keeps every run in a run
store under a key: the SHA-256 of the tool, the input, every file the
input reads, the options and the settings. A stored run is never
repeated, and a changed or added row runs alone. `tools/collect.py` fills
the columns `stored` and `measured` from the stored runs. With the raw
outputs of the full dataset it rebuilds them without running a tool:

```sh
python3 paper2026/tools/collect.py --raw paper2026/raw
```

## Helper scripts

| script | what it does |
|---|---|
| `check_gk.py` | reruns the gk runs (and with `--mcref` the mcref runs) and compares them with `results.tsv` and `O2_record/rows.tsv` |
| `tools/run_store.py` | runs every run of the run lists that its store does not hold yet |
| `tools/collect.py` | fills the columns `stored` and `measured` from a run store or from the raw outputs |
| `tools/gkout.py` | reads the outputs of gk and of the reference tool |
| `tools/enumerate_answer_sets.py` | the values of PASTA's and smProbLog's published semantics, by enumeration with clingo |
| `tools/run_smproblog.py` | starts smProbLog 2.1.0.42 under PyPy 3.11 |
| `O2_record/count_rows.py` | recomputes the counts of Section 7.1 from `O2_record/rows.tsv` |

The scripts need Python 3.9 or later and no other package.

## Licence

The inputs, results, documentation and scripts of this folder are
licensed under CC BY 4.0; [`LICENSE`](LICENSE) names the exceptions and
the third-party material.
