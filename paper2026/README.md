# Inputs and results of the paper

This folder lets a reader rerun the examples and experiments of the paper

> Tanel Tammet, Dirk Draheim and Priit Järv. Reasoning with Uncertain Evidence, Opposition and Exceptions: Support
> Semantics in Three Layers and a First-Order Inference Method. Submitted, 2026.

gk is the reasoner of the paper: a program that answers a question from an input with uncertain rules, opposition
and exceptions. Its answer, a value, is four shares (for, against, conflict, ignorance). gk has three ways to
answer: the exact method (`gk FILE -exact`), the general method (`gk FILE -general`), and the default (`gk FILE`),
which runs the exact method first and then the general method with the time left. The tool, mcref, is an
independent Python program that computes the same semantics on a ground input; it is the reference of the
comparisons. [`../Doc/input_languages.md`](../Doc/input_languages.md) describes gk's input language and
[`../Doc/support_semantics.md`](../Doc/support_semantics.md) the semantics.

The folder holds the inputs of every run, the encodings for the other systems, the commands, and the results with
one row per run and answer. Every gk value comes from gk 1.3.2 and every value of the tool from mcref 1.3.1:

| program | version | file | SHA-256 |
|---|---|---|---|
| gk | 1.3.2 (Linux x86-64) | `bin/gk` of the repository | `f73e9f2e9aac47bb8aaa20fa37db6e79042c0ffff441ed1ed4f5e0b05a1fb642` |
| the tool (mcref) | 1.3.1 | `mcref/mcref.py` of the repository, with its modules | `e7489ee3ef14ebcc506099236ec4dd6962ff8880faa7ab7f09a2a6653179ec13` |

The address of this folder is <https://github.com/tammet/gkreasoner/tree/master/paper2026>. The full dataset is
archived at Zenodo: <https://doi.org/10.5281/zenodo.XXXXXXX>.

The online appendix, which the paper cites by part (O1 to O20), is the file
[`ONLINE_APPENDIX.md`](ONLINE_APPENDIX.md) of this folder.

## Quick start

From this folder of a copy of the gkreasoner repository, on Linux x86-64 (the repository has `bin/gk` and
`mcref/` beside this folder):

```sh
export GK=$(realpath ../bin/gk)
export MCREF=$(realpath ../mcref/mcref.py)
cd O1_tweety/inputs/stage3a && $GK gk.gkp && cd ../../..
python3 check_gk.py --part O18_lifschitz --gk $GK --mcref $MCREF
python3 tools/summarize.py --check
```

With the two variables set, every command of a part's README and of a `runs.tsv` can be pasted as it is, in the
folder that its column `cwd` names (relative to this folder).

The third command answers stage 3a of the Tweety example. gk prints its answer as one long JSON line. Three of its
fields matter to a reader: `value`, the four shares, here `[0.6984,0.224,0,0.0776]`; `complete` in
`complete_mode`, the mark complete, here `true`; and `answer_from` in `policy`, the method that answered, here
`"the exhaustive search"`. The word `recursive` at the start of the line and the phrase "the exhaustive search"
are gk's names; the paper says "the exact method". `python3 -m json.tool` prints the whole line indented; the
three fields alone:

```sh
cd O1_tweety/inputs/stage3a && $GK gk.gkp | python3 -c 'import json, sys; r = json.load(sys.stdin)["recursive"]; print(r["value"], r["complete_mode"]["complete"], r["policy"]["answer_from"])' && cd ../../..
```

It prints `[0.6984, 0.224, 0, 0.0776] True the exhaustive search`.
[`../Doc/recursive_output.md`](../Doc/recursive_output.md) describes the other fields.

The fourth command reruns every gk and tool run of Lifschitz's problems in less than a minute and compares each
value with the recorded one. Its last line reports every compared value as equal; it compares these runs and
values:

<!-- table check -->
| gk runs | tool runs | runs with a recorded value | values compared | of these, on runs that did not end by themselves |
|---|---|---|---|---|
| 21 | 7 | 22 | 22 | 0 |
<!-- end table -->

The fifth command computes every table of every README again from the results files and compares them; it
reports every table as equal.

The repository's `bin/` also has gk 1.3.2 for macOS (`gk-macos-arm64`) and for Windows (`gk-windows-x64.exe`);
set `GK` to that file there. The recorded runs are from Linux (`bin/gk`).

### One input by hand

Take a row of a part's `runs.tsv` and go to the folder that its column `cwd` names, relative to this folder.
Run its column `command`, with `GK` and `MCREF` set as above; the value is in the first output line. The
recorded value is in the rows of the part's `results.csv` with the same `run_id`.

## The test material

One row per part. Each part folder has a README with what the part shows, where its inputs come from, one command
to rerun it, and for each number of the paper the file and the column that hold it. The last two columns give
the gk and tool runs that `check_gk.py --part` reruns and the time that it takes with one process, from the
recorded times of the runs; a run that did not end by itself counts with its time limit.

<!-- table material -->
| part | material | size | where it comes from | where the paper uses it | gk and tool runs that `check_gk.py` reruns | time with one process |
|---|---|---|---|---|---|---|
| [O1_tweety](O1_tweety/README.md) | the Tweety stages, with the encodings of the other systems, and s(CASP) on stage 4 | 7 inputs; 21 runs of s(CASP) | written for this paper | Sections 2 and 4; Section 7.2, the Tweety table and s(CASP); Section 7.6 | 31 | 5 min |
| [O2_record](O2_record/README.md) | our collection: inputs written while the method was built | 1,022 inputs; the tool accepts 360 | ours: design probes, documentation examples, published studies, cases restated from the literature, inputs translated from English by a language model | Section 7, the table of the test material | 1,440 | 1.9 h |
| [O3_families](O3_families/README.md) | the benchmark families, and the table of limits | 108 inputs | published: the bnlearn networks, a LUBM-style university base, Smokers, grids; ours: delivery plans, equipment, cyclic inputs, chains and trees | Sections 7.1, 7.3, 7.4, 7.5 and 7.6; Appendix C | 418 | 28 min |
| [O4_quantities](O4_quantities/README.md) | small inputs under the quantities of the compared systems | 10 inputs | constructed for this paper | Appendix D, the five-inputs table | 20 | 1 s |
| [O5_comparisons](O5_comparisons/README.md) | the 16 small cases on 9 systems, one encoding per system | 18 gk inputs | constructed for this paper | Section 7.2, row D3; Appendix D, the 16-case table; Appendix C | 72 | 18 s |
| [O6_budget](O6_budget/README.md) | the time budget of the general method, and the runs at 600 s | 13 runs of the time budget; 92 runs at 600 s | inputs of parts O3, O7, O14, O15, O19 and O20 | Section 7.6, the effect of a longer time limit | 107 | 11.1 h |
| [O7_english](O7_english/README.md) | cases translated from English, and the pipeline's tasks | 303 tasks | ours: translated by a language model | Section 7.6 | 305 | 24 min |
| [O8_cycles](O8_cycles/README.md) | further examples of cycles | 33 inputs | written for this paper | Section 7.6, the table of the three methods | 66 | 6 s |
| [O11_text_examples](O11_text_examples/README.md) | the small examples of the text | 19 inputs | written for this paper | Section 4; Appendix A | 40 | 3 s |
| [O13_conformance](O13_conformance/README.md) | generated conformance inputs, against the tool, and further questions on new inputs | 50,134 questions; 4,340 inputs of the evaluator check; 225,102 further questions on new inputs; 5,000 pairs with function terms | generated by our scripts for comparison with the tool | Sections 7.4 and 7.6 | 331,519 | 28.5 h |
| [O14_routes](O14_routes/README.md) | route queries in four families | 5 to 200 links | constructed for this paper | Sections 7.1, 7.2, 7.3, 7.5 and 7.6 | 132 | 11 min |
| [O15_contradiction](O15_contradiction/README.md) | the university base with an unrelated contradiction | 8 queries on 2 bases, each with two variants | the university base of part O3, with generated variants | Sections 7.2 and 7.6 | 72 | 3 min |
| [O16_function_terms](O16_function_terms/README.md) | delivery plans with function terms | 4 plans | written for this paper | not cited in the text | 12 | 31 s |
| [O17_boardgameqa](O17_boardgameqa/README.md) | BoardgameQA, converted by a script from its formal form | 3,000 test examples | a public benchmark: Kazemi et al., NeurIPS 2023, <https://storage.googleapis.com/gresearch/BoardgameQA/BoardgameQA.zip> | Section 7.1 | 6,301 | 6 min |
| [O18_lifschitz](O18_lifschitz/README.md) | Lifschitz's benchmark problems | 7 published conclusions | the literature: Lifschitz, 1989 | Sections 7.1 and 7.5 | 28 | 33 s |
| [O19_defeasible_logic](O19_defeasible_logic/README.md) | theories of defeasible logic: chains, trees, cascades | 33 theories in three forms | the literature (2001); generated for this paper | Sections 7.1, 7.5 and 7.6 | 99 | 3 min |
| [O20_outside_classes](O20_outside_classes/README.md) | the exact method outside both classes | 24 inputs | constructed for this paper | Section 7.6, the table of the three methods | 104 | 12 min |
<!-- end table -->

`check_gk.py --all` reruns 340,766 runs; with one process that takes about 43.0 h. The largest
recorded peak memory of a run is 8.9 GB (part O6_budget), and 2 runs of part O6 at
600 s ended at their memory limit of 12 GB, with no recorded peak. `runs.tsv` gives the memory limit of each run
(column `memory_cap`).

The parts O9, O10 and O12 of the online appendix are texts in
[`ONLINE_APPENDIX.md`](ONLINE_APPENDIX.md): the method in detail
([`../Doc/how_gk_works.md`](../Doc/how_gk_works.md)), the tool in detail ([`../Doc/mcref.md`](../Doc/mcref.md)),
and the schedule, the proof listing and the list of notes. Part O11 has both: a folder with the small examples of
the text, and a text in the online appendix, the complete definition with all its examples.

## This folder and the full dataset

This folder holds the inputs, the commands and the results in brief: one row per run and answer, with the value,
the mark complete, the method that answered, the first limit, the time and whether the run ended by itself. The
full dataset adds the raw output of every run (standard output, standard error, the exit status, the time and the
peak memory), the gk binary and the tool. The column `raw` of every `runs.tsv` names the raw output of the run in
the full dataset: `raw/GROUP.tar.xz:GROUP/RUN.out`.

## The tables of a part

`runs.tsv` has one row per run:

| column | content |
|---|---|
| `run_id` | the run's name: the group of runs and the run within it |
| `system` | gk 1.3.2, mcref 1.3.1, or another system with its version |
| `method` | for gk: default (`gk FILE`), general (`gk FILE -general`), exact (`gk FILE -exact`), or exact, ground first (`gk FILE -exact -ground-first`); a fixed strategy of the general method is named |
| `input` | the run's input, relative to this folder |
| `cwd`, `command` | the folder in which the run starts, relative to this folder, and the command; `$GK` is the gk binary, `$MCREF` the tool's `mcref.py` |
| `limit_s` | gk's time limit in seconds (the option `-seconds`, by default 10) |
| `timed_alone` | `yes` for a run that ran with no other gk, tool or solver process on the machine |
| `memory_cap`, `time_cap_s` | the memory limit (without swap) and the time limit of the process |
| `exit`, `peak_mb` | the exit status and the peak memory of the run |
| `raw` | the raw output of the run in the full dataset |

`results.csv` has one row per run and answer:

| column | content |
|---|---|
| `run_id` | the run (in `runs.tsv`) |
| `system`, `method`, `input` | as in `runs.tsv` |
| `question` | the answer's literal; the value is the value of this literal |
| `value`, `unresolved` | gk's four shares (for, against, conflict, ignorance) and the share with no value; for another system, what it printed |
| `complete` | the mark of the exact method: `yes` or `no`; empty for the general method, which gives no such mark |
| `answered_by` | the method that answered: `exact` or `general`; under the default either one |
| `first_limit` | for an answer that is not complete, the first limit that the exact method names, or `not covered` with the reason; for the general method, the searches that its time limit stopped |
| `ended_by_itself` | `yes` when the run ended by itself: the exact method's answer is complete, or the general method stopped no search and finished its evaluation |
| `time_s` | the time of the run in seconds, only for a run that ended by itself |
| `target`, `target_kind` | the value against which the answer is judged, and its kind: calculated, the exact value of the tool, a sampled value of the tool with its bound, a value of the tool with a stated limit of its proof search (which is not an exact value), or the answer of another system with its version |
| `class` | the answer against its target |
| `outcome` | for another system: same value, another quantity, no answer, did not end, no encoding, not run, or generated encoding rejected; for s(CASP): a model, no model, or did not end |
| `note` | the meaning of another system's quantity, a message, or the source of the row |

A part adds its own columns after these. A large table is compressed (`results.csv.gz`, `runs.tsv.gz`); the
scripts read both forms. Inputs that are many or large are packed in `inputs/*.tar.xz`, each with a listing
`inputs/*.files.tsv` (compressed, `*.files.tsv.gz`, above 20,000 members); unpack them with
`tar -xJf inputs/NAME.tar.xz -C inputs` in the part folder.

## Versions and runs

- One run per input and method, on gk 1.3.2 and the tool 1.3.1. The other systems keep their recorded runs where
  a part says so; `SYSTEMS.md` gives every version.
- A time is given only for a run that ended by itself. A run that used its time limit has no time; its value can
  change from run to run. `check_gk.py` reports a difference apart, and not as a failure, when the recorded run
  used its time limit or when the rerun reports cut or queued searches.
- A run with `timed_alone` = yes ran with no other gk, tool or solver process on the machine. The other runs ran
  beside other processes, so a run alone can take less time. Every process ran under a memory limit without swap
  and a time limit.
- The machine: an AMD Ryzen 5 3600 processor (six cores, 12 threads) with 64 GB of memory, Ubuntu 26.04.1 LTS with
  Linux 7.0, Python 3.14.4 and PyPy 3.11.

## The scripts

| script | what it does |
|---|---|
| `check_gk.py` | reruns the gk and tool runs of one or more parts and compares every value with `results.csv` |
| `tools/summarize.py` | computes the tables of the READMEs from the results files; `--check` compares them with the READMEs |
| `tools/gkline.py` | reads gk's first output line and the tool's output object |
| `tools/make_questions.py` | writes the question files of part O13 from its inputs |
| `tools/enumerate_answer_sets.py` | the quantities of PASTA's and smProbLog's published semantics, by enumeration with clingo |
| `tools/run_smproblog.py` | starts smProbLog 2.1.0.42 under PyPy 3.11 |
| `O14_routes/make_routes.py` | writes the route inputs |
| `O17_boardgameqa/convert_boardgameqa.py` | converts the BoardgameQA release into gk input |
| `O13_conformance/tools/evaluator_check.py` | the driver of the evaluator check |

The scripts need Python 3.9 or later and no other package.

## Licence

The inputs, results, documentation and scripts of this folder are licensed under CC BY 4.0;
[`LICENSE`](LICENSE) names the exceptions and the third-party material.
