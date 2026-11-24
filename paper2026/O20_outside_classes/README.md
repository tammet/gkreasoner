# O20: the exact method outside both classes

This part holds inputs outside both classes on which the exact method matches rule bodies against facts. Each
input has K links of .9, the reach rules, the disjunction `safe(X) ; guarded(X) :- reach(n0,X)`, two rules for
`ok`, and D facts `site(mj)` with constants that the question does not need. The calculated value of `ok(nK)` is
.9^K. gk 1.3.2 answers each input under the exact method, the exact method with a full grounding first, the
general method and the default; the tool computes the inputs with D = 0 and D = 10.

## Where the inputs come from

`inputs/cases_K_D.gkp`, generated for this paper. The column `peak_mb_run` is the peak memory of the run.

## Rerun

To rerun every gk and tool run of this part and compare each value with `results.csv`:

```sh
python3 check_gk.py --part O20_outside_classes --gk PATH/TO/gk --mcref PATH/TO/mcref.py
```

Its last line names the values compared and how many differ. Every value is expected to be equal, except that
a value can change from run to run when the recorded run did not end by itself or the rerun reports cut or
queued searches; the check reports such a difference apart. The runs and values that it compares:

<!-- table check -->
| gk runs | tool runs | runs with a recorded value | values compared | of these, on runs that did not end by themselves |
|---|---|---|---|---|
| 96 | 8 | 96 | 96 | 40 |
<!-- end table -->

`$GK` stands for the gk binary and `$MCREF` for the tool's `mcref.py`. Every command of `runs.tsv` runs
in the folder that its column `cwd` names, relative to this folder's parent (`paper2026/`).

## Results

<!-- table cases -->
| K links | D constants not needed | calculated value | the exact method | the exact method, ground first | the general method | the default | the tool |
|---|---|---|---|---|---|---|---|
| 2 | 0 | (.81, 0, 0, .19) | (.81, 0, 0, .19), complete, 0.15 s; 99 MB | (.81, 0, 0, .19), complete, 0.06 s; 98 MB | (.81, 0, 0, .19), 0.40 s; 128 MB | (.81, 0, 0, .19), complete, by the exact method, 0.15 s; 99 MB | (.81, 0, 0, .19); exact value of the tool |
| 2 | 10 | (.81, 0, 0, .19) | (0, 0, 0, 1), not complete, limit; 1100 MB | (0, 0, 0, 1), not complete, limit; 1100 MB | (.81, 0, 0, .19), 0.39 s; 104 MB | (.81, 0, 0, .19), by the general method, 3.13 s; 1099 MB | (0, 0, 0, 1); limit: more than 3000000 resolvents of the proof search |
| 2 | 20 | (.81, 0, 0, .19) | (0, 0, 0, 1), not complete, limit; 1103 MB | (0, 0, 0, 1), not complete, limit; 1103 MB | (.81, 0, 0, .19), 0.40 s; 104 MB | (.81, 0, 0, .19), by the general method, 1.84 s; 1102 MB | - |
| 2 | 50 | (.81, 0, 0, .19) | (0, 0, 0, 1), not complete, limit; 1106 MB | (0, 0, 0, 1), not complete, limit; 1105 MB | (.81, 0, 0, .19), 0.40 s; 128 MB | (.81, 0, 0, .19), by the general method, 1.12 s; 1100 MB | - |
| 2 | 100 | (.81, 0, 0, .19) | (0, 0, 0, 1), not complete, limit; 661 MB | not covered: more ground statements than the limit of the key mode (GK_KEY_GROUND); 642 MB | (.81, 0, 0, .19), 0.84 s; 154 MB | (.81, 0, 0, .19), by the general method, 2.32 s; 643 MB | - |
| 2 | 200 | (.81, 0, 0, .19) | (0, 0, 0, 1), not complete, limit; 685 MB | not covered: more ground statements than the limit of the key mode (GK_KEY_GROUND); 659 MB | (.81, 0, 0, .19), 0.84 s; 201 MB | (.81, 0, 0, .19), by the general method, 2.38 s; 665 MB | - |
| 3 | 0 | (.729, 0, 0, .271) | (.729, 0, 0, .271), complete, 0.38 s; 100 MB | (.729, 0, 0, .271), complete, 0.22 s; 100 MB | (.729, 0, 0, .271), 0.54 s; 129 MB | (.729, 0, 0, .271), complete, by the exact method, 0.37 s; 100 MB | (.729, 0, 0, .271); exact value of the tool |
| 3 | 10 | (.729, 0, 0, .271) | (0, 0, 0, 1), not complete, limit; 1099 MB | (0, 0, 0, 1), not complete, limit; 1099 MB | (.729, 0, 0, .271), 0.55 s; 105 MB | (.729, 0, 0, .271), by the general method, 2.64 s; 1103 MB | (0, 0, 0, 1); limit: more than 3000000 resolvents of the proof search |
| 3 | 20 | (.729, 0, 0, .271) | (0, 0, 0, 1), not complete, limit; 1106 MB | (0, 0, 0, 1), not complete, limit; 1106 MB | (.729, 0, 0, .271), 0.55 s; 105 MB | (.729, 0, 0, .271), by the general method, 1.93 s; 1105 MB | - |
| 3 | 50 | (.729, 0, 0, .271) | (0, 0, 0, 1), not complete, limit; 1111 MB | (0, 0, 0, 1), not complete, limit; 1111 MB | (.729, 0, 0, .271), 0.54 s; 130 MB | (.729, 0, 0, .271), by the general method, 1.28 s; 1103 MB | - |
| 3 | 100 | (.729, 0, 0, .271) | (0, 0, 0, 1), not complete, limit; 660 MB | not covered: more ground statements than the limit of the key mode (GK_KEY_GROUND); 643 MB | (.729, 0, 0, .271), 1.11 s; 199 MB | (.729, 0, 0, .271), by the general method, 2.61 s; 643 MB | - |
| 3 | 200 | (.729, 0, 0, .271) | (0, 0, 0, 1), not complete, limit; 682 MB | not covered: more ground statements than the limit of the key mode (GK_KEY_GROUND); 662 MB | (.729, 0, 0, .271), 1.12 s; 170 MB | (.729, 0, 0, .271), by the general method, 2.69 s; 662 MB | - |
| 4 | 0 | (.6561, 0, 0, .3439) | (.6561, 0, 0, .3439), not complete, limit; 148 MB | (.6561, 0, 0, .3439), not complete, limit; 149 MB | (.6561, 0, 0, .3439), 2.69 s; 165 MB | (.6561, 0, 0, .3439), by the general method, 5.04 s; 179 MB | (0, 0, 0, 1); limit: more than 20000 proofs of several statements |
| 4 | 10 | (.6561, 0, 0, .3439) | (0, 0, 0, 1), not complete, limit; 1100 MB | (0, 0, 0, 1), not complete, limit; 1100 MB | (.6561, 0, 0, .3439), 2.70 s; 166 MB | (.6561, 0, 0, .3439), by the general method, 4.15 s; 1152 MB | (0, 0, 0, 1); limit: more than 3000000 resolvents of the proof search |
| 4 | 20 | (.6561, 0, 0, .3439) | (0, 0, 0, 1), not complete, limit; 1107 MB | (0, 0, 0, 1), not complete, limit; 1107 MB | (.6561, 0, 0, .3439), 2.70 s; 166 MB | (.6561, 0, 0, .3439), by the general method, 3.71 s; 1128 MB | - |
| 4 | 50 | (.6561, 0, 0, .3439) | (0, 0, 0, 1), not complete, limit; 1111 MB | (0, 0, 0, 1), not complete, limit; 1104 MB | (.6561, 0, 0, .3439), 2.70 s; 165 MB | (.6561, 0, 0, .3439), by the general method, 3.21 s; 1105 MB | - |
| 4 | 100 | (.6561, 0, 0, .3439) | (0, 0, 0, 1), not complete, limit; 661 MB | not covered: more ground statements than the limit of the key mode (GK_KEY_GROUND); 642 MB | (.6561, 0, 0, .3439), limit; 227 MB | (.6561, 0, 0, .3439), by the general method, limit; 643 MB | - |
| 4 | 200 | (.6561, 0, 0, .3439) | (0, 0, 0, 1), not complete, limit; 684 MB | not covered: more ground statements than the limit of the key mode (GK_KEY_GROUND); 659 MB | (.6561, 0, 0, .3439), limit; 230 MB | (.6561, 0, 0, .3439), by the general method, limit; 663 MB | - |
| 5 | 0 | (.59049, 0, 0, .40951) | (.59049, 0, 0, .40951), not complete, limit; 176 MB | (.59049, 0, 0, .40951), not complete, limit; 180 MB | (.59049, 0, 0, .40951), 4.27 s; 201 MB | (.59049, 0, 0, .40951), by the general method, 5.83 s; 219 MB | (0, 0, 0, 1); limit: more than 3000000 resolvents of the proof search |
| 5 | 10 | (.59049, 0, 0, .40951) | (0, 0, 0, 1), not complete, limit; 1100 MB | (0, 0, 0, 1), not complete, limit; 1100 MB | (.59049, 0, 0, .40951), 4.27 s; 202 MB | (.59049, 0, 0, .40951), by the general method, 5.49 s; 1194 MB | (0, 0, 0, 1); limit: more than 3000000 resolvents of the proof search |
| 5 | 20 | (.59049, 0, 0, .40951) | (0, 0, 0, 1), not complete, limit; 1104 MB | (0, 0, 0, 1), not complete, limit; 1104 MB | (.59049, 0, 0, .40951), 4.27 s; 203 MB | (.59049, 0, 0, .40951), by the general method, 5.29 s; 1141 MB | - |
| 5 | 50 | (.59049, 0, 0, .40951) | (0, 0, 0, 1), not complete, limit; 1109 MB | (0, 0, 0, 1), not complete, limit; 1109 MB | (.59049, 0, 0, .40951), 4.27 s; 200 MB | (.59049, 0, 0, .40951), by the general method, 4.75 s; 1102 MB | - |
| 5 | 100 | (.59049, 0, 0, .40951) | (0, 0, 0, 1), not complete, limit; 660 MB | not covered: more ground statements than the limit of the key mode (GK_KEY_GROUND); 642 MB | (.59049, 0, 0, .40951), 3.27 s; 175 MB | (.59049, 0, 0, .40951), by the general method, 4.45 s; 643 MB | - |
| 5 | 200 | (.59049, 0, 0, .40951) | (0, 0, 0, 1), not complete, limit; 682 MB | not covered: more ground statements than the limit of the key mode (GK_KEY_GROUND); 660 MB | (.59049, 0, 0, .40951), 3.31 s; 176 MB | (.59049, 0, 0, .40951), by the general method, 4.52 s; 662 MB | - |
<!-- end table -->

<!-- table summary -->
| method | inputs | complete | equal to the calculated value | ignorance (0, 0, 0, 1) |
|---|---|---|---|---|
| exact | 24 | 2 | 4 | 20 |
| exact, ground first | 24 | 2 | 4 | 12 |
| general | 24 | 0 | 24 | 0 |
| default | 24 | 2 | 24 | 0 |
<!-- end table -->

The tool reports a limit of its own proof search on some inputs; its value there comes from the single
applications only and is not an exact value.

## Where the paper's numbers are

- The exact method outside both classes (one row of the table of limits): the rows of `results.csv`, columns
  `value`, `complete`, `class` and `first_limit`.

`results.csv` has one row per run and answer. The columns are described on the first page of the
folder ([`../README.md`](../README.md), section "The tables of a part").
