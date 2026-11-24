# O18: Lifschitz's benchmark problems

This part holds the problems A1 to A6 of Lifschitz's benchmark problems for formal nonmonotonic reasoning
(V. Lifschitz, "Benchmark problems for formal nonmonotonic reasoning", 1989), stated in gk's input language.
gk 1.3.2 answers each published conclusion under the exact method, the general method and the default, and the
tool computes the inputs that it accepts. A published conclusion holds under a method when gk's value is
(1, 0, 0, 0).

## Where the inputs come from

`inputs/*.js`: the problems as gk input. The encoding of A4 adds a stronger premise than the source: A is
excluded from the default and stated not to be on the table. A5 asks for a universal conclusion through a formula
abbreviation. The second conclusion of A6 needs a choice of a smallest set of exceptions, which the support
semantics does not make.

## Rerun

From the folder `paper2026/`:

```sh
python3 check_gk.py --part O18_lifschitz --gk PATH/TO/gk --mcref PATH/TO/mcref.py
```

It takes less than a minute. Every compared value is expected to be equal. The runs and values that it
compares:

<!-- table check -->
| gk runs | tool runs | runs with a recorded value | values compared | of these, on runs that did not end by themselves |
|---|---|---|---|---|
| 21 | 7 | 22 | 22 | 0 |
<!-- end table -->

`$GK` stands for the gk binary and `$MCREF` for the tool's `mcref.py`. Every command of `runs.tsv` runs
in the folder that its column `cwd` names, relative to this folder's parent (`paper2026/`).

## Results

<!-- table problems -->
| problem | published conclusion | the exact method | the general method | the default | the tool |
|---|---|---|---|---|---|
| A1 | B is on the table | (1, 0, 0, 0), complete, 0.05 s; the published conclusion holds | (1, 0, 0, 0), 0.16 s; the published conclusion holds | (1, 0, 0, 0), complete, by the exact method, 0.05 s; the published conclusion holds | (1, 0, 0, 0); the published conclusion holds |
| A2 | B is on the table | (1, 0, 0, 0), complete, 0.05 s; the published conclusion holds | (1, 0, 0, 0), 0.18 s; the published conclusion holds | (1, 0, 0, 0), complete, by the exact method, 0.06 s; the published conclusion holds | (1, 0, 0, 0); the published conclusion holds |
| A3 | B is on the table and A is red | not covered: a compound question; no value | (1, 0, 0, 0), 0.33 s; the published conclusion holds | (1, 0, 0, 0), by the general method, 0.33 s; the published conclusion holds | declines: compound question |
| A4 | B is on the table | not covered: an equality between terms; no value | (1, 0, 0, 0), 0.20 s; the published conclusion holds | (1, 0, 0, 0), by the general method, 0.17 s; the published conclusion holds | declines: equality |
| A5 | all heavy blocks other than A are on the table | not covered: an equality between terms; no value | (0, 0, 0, 1), 0.26 s; does not hold | (0, 0, 0, 1), by the general method, 0.23 s; does not hold | declines: equality |
| A6a | C is on the table | (1, 0, 0, 0), complete, 0.06 s; the published conclusion holds | (1, 0, 0, 0), 0.18 s; the published conclusion holds | (1, 0, 0, 0), complete, by the exact method, 0.05 s; the published conclusion holds | (1, 0, 0, 0); the published conclusion holds |
| A6b | exactly one of A and B is not on the table | (0, 0, 1, 0), complete, 0.06 s; does not hold | (0, 0, 1, 0), 0.55 s; does not hold | (0, 0, 1, 0), complete, by the exact method, 0.05 s; does not hold | (0, 0, 1, 0); does not hold |
<!-- end table -->

<!-- table count -->
| published conclusions | that hold under the default | that hold under the exact method |
|---|---|---|
| 7 | 5 | 3 |
<!-- end table -->

## Where the paper's numbers are

- Lifschitz's problems (Sections 7.1 and 7.5): the rows of `results.csv`, columns `value` and `class`, by `problem`
  and `method`.

`results.csv` has one row per run and answer. The columns are described on the first page of the
folder ([`../README.md`](../README.md), section "The tables of a part").
