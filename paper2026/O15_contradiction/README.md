# O15: an unrelated contradiction in the university base

This part adds a contradiction to the university base of part O3 and asks whether the values of the queries
change. Variant (a) adds two certain facts that contradict each other about a new individual, `c4new`, which
occurs nowhere else: `fullProfessor(c4new).` and `-fullProfessor(c4new).`. Variant (b) adds the negation of the
base's first `researchInterest` fact; the predicate `researchInterest` occurs in no rule, so no query depends on
it. The smallest and the largest base of the twelve university queries are used, each with its four queries.

gk 1.3.2 answers every query under the default, the general method and the exact method. The other systems get
inputs generated from the ProbLog program of the base, with the contradiction encoded as row X1 of the 16-case
table encodes it for that system. ProbLog has no encoding of row X1.

## Where the inputs come from

The bases are those of part O3. The variants and the encodings for the other systems are generated; they are
packed in `inputs/generated.tar.xz` (listing `inputs/generated.files.tsv`). Unpack with
`tar -xJf inputs/generated.tar.xz -C inputs`. The PASTA files come in two forms:

- `generated/pasta_first/`: the first generated files. PASTA's parser rejects a probabilistic fact whose argument
  has an upper-case letter, and the university constants have such letters. These cells have the outcome
  "generated encoding rejected".
- `generated/pasta/`: the corrected files, in the switch form of the record's PASTA encodings: each uncertain fact
  `p::f` is written as `p::swN.` and `f :- swN.`.

## Rerun

To rerun every gk and tool run of this part and compare each value with `results.csv`:

```sh
python3 check_gk.py --part O15_contradiction --gk PATH/TO/gk --mcref PATH/TO/mcref.py
```

Its last line names the values compared and how many differ. Every value is expected to be equal, except that
a value can change from run to run when the recorded run did not end by itself or the rerun reports cut or
queued searches; the check reports such a difference apart. The runs and values that it compares:

<!-- table check -->
| gk runs | tool runs | runs with a recorded value | values compared | of these, on runs that did not end by themselves |
|---|---|---|---|---|
| 72 | 0 | 72 | 72 | 16 |
<!-- end table -->

`$GK` stands for the gk binary and `$MCREF` for the tool's `mcref.py`. Every command of `runs.tsv` runs
in the folder that its column `cwd` names, relative to this folder's parent (`paper2026/`).

## Results

gk by method. "Value kept" means equal to the value on the base within 1e-6.

<!-- table gk -->
| method | variant | queries | value kept | value changed | complete | answered by | ended by itself |
|---|---|---|---|---|---|---|---|
| default | (a) | 8 | 8 | 0 | 0 | exact 0, general 8 | 6 |
| default | (b) | 8 | 8 | 0 | 8 | exact 8, general 0 | 8 |
| general | (a) | 8 | 8 | 0 | no mark | exact 0, general 8 | 6 |
| general | (b) | 8 | 8 | 0 | no mark | exact 0, general 8 | 6 |
| exact | (a) | 8 | 5 | 3 | 0 | exact 8, general 0 | 0 |
| exact | (b) | 8 | 8 | 0 | 8 | exact 8, general 0 | 8 |
<!-- end table -->

The changed values:

<!-- table changed -->
| base | question | method | on the base | on variant (a) | first limit |
|---|---|---|---|---|---|
| dept3_scale1 | person(grad39_d0) | exact | (.966422, 0, 0, .033578), complete, 0.43 s | (.957496, 0, 0, .042504), not complete, limit | tasks: the time budget of the collection |
| dept3_scale1 | employee(full1_d0) | exact | (.999781, 0, 0, .000219), complete, 0.48 s | (.84, 0, 0, .16), not complete, limit | tasks: the time budget of the collection |
| dept3_scale1 | organization(dept0) | exact | (1, 0, 0, 0), complete, 0.45 s | (.784, 0, 0, .216), not complete, limit | task limit: more ground statements than the limit of the key mode (GK_KEY_GROUND), in the ground search of a task |
<!-- end table -->

The other systems:

<!-- table others -->
| system | version | outcome | queries | detail of the first |
|---|---|---|---|---|
| ProbLog 2.3.0 | base | same value | 8 | a probability of the query atom; equal to the exact method's complete answer within 1e-6 |
| ProbLog 2.3.0 | a | no encoding | 8 | row X1 has no ProbLog encoding (no classical negation) |
| ProbLog 2.3.0 | b | no encoding | 8 | row X1 has no ProbLog encoding (no classical negation) |
| smProbLog 2.1.0.42 | base | no answer | 8 | generated from the ProbLog program; exit 1: DSharpError: DSharp has encountered an error. (the bundled compile |
| smProbLog 2.1.0.42 | a | another quantity | 8 | generated from the ProbLog program; the printed (true, false, inconsistent) does not follow smProbLog's publis |
| smProbLog 2.1.0.42 | b | no answer | 8 | generated from the ProbLog program; exit 1: DSharpError: DSharp has encountered an error. (the bundled compile |
| PASTA 1.0.1, first generated file | base | generated encoding rejected | 8 | the first generated file: PASTA's parser rejects a probabilistic fact whose argument has an upper-case letter; |
| PASTA 1.0.1, first generated file | a | generated encoding rejected | 8 | the first generated file: PASTA's parser rejects a probabilistic fact whose argument has an upper-case letter; |
| PASTA 1.0.1, first generated file | b | generated encoding rejected | 8 | the first generated file: PASTA's parser rejects a probabilistic fact whose argument has an upper-case letter; |
| plingo 1.1.0 | base | did not end | 8 | generated from the ProbLog program; the limit of 60 s; 8543679 models enumerated, interrupted; the printed num |
| plingo 1.1.0 | a | no answer | 8 | generated from the ProbLog program; exit 20: UNSATISFIABLE, 0 models (no stable model of the whole program) |
| plingo 1.1.0 | b | did not end | 8 | generated from the ProbLog program; the limit of 60 s; 8863069 models enumerated, interrupted; the printed num |
| PASTA 1.0.1, corrected file | base | did not end | 8 | the corrected file, in the record's switch form (304 switches); the limit of 60 s |
| PASTA 1.0.1, corrected file | a | another quantity | 8 | the corrected file, in the record's switch form (304 switches); [0.0, 0.0] after the warning: This program is  |
| PASTA 1.0.1, corrected file | b | did not end | 8 | the corrected file, in the record's switch form (304 switches); the limit of 60 s |
<!-- end table -->

## Where the paper's numbers are

- The unrelated contradiction (Section 7.2): the table "gk by method", from the rows with `system`
  gk 1.3.2, columns `class`, `complete`, `answered_by` and `ended_by_itself`; the other systems from the rows
  of each system, column `outcome`.

`results.csv` has one row per run and answer. The columns are described on the first page of the
folder ([`../README.md`](../README.md), section "The tables of a part").
