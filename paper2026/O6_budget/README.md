# O6: the time budget

This part holds the runs that show how a value of the general method depends on the time limit: the delivery
plan of 32 legs at 2, 10 and 60 s, the grid of 56 edges at 10 and 60 s, the library member and "Does John eat
berries?" at 10 and 60 s. It also holds the runs at 600 s: every run of the archive that was
wrong, without a value or not complete at 10 s, again with `-seconds 600`.

## Where the inputs come from

The inputs are those of parts O3 (`../O3_families/inputs/delivery/gk_legs32_control.gkp`,
`../O3_families/inputs/grids/gk_corner56.gkp`) and O7 (`../O7_english/inputs/n2v2/gk_deepseek.js`,
`../O7_english/inputs/n4/gk.js`); `runs.tsv` names them.

## Rerun

From the folder `paper2026/`:

```sh
cd O7_english/inputs/n4 && $GK ../pipeline/axioms_std.js -strategy ../pipeline/strategy.json -seconds 60 gk.js -defaults -confidence 0.1 -keepconfidence 0.1 -datafolder ../../../../data
```

The general method uses its whole budget on this input, so the run takes most of its time limit, and its value
can differ from run to run.

To rerun every gk and tool run of this part and compare each value with `results.csv`:

```sh
python3 check_gk.py --part O6_budget --gk PATH/TO/gk --mcref PATH/TO/mcref.py
```

Its last line names the values compared and how many differ. Every value is expected to be equal, except that
a value can change from run to run when the recorded run did not end by itself or the rerun reports cut or
queued searches; the check reports such a difference apart. The runs and values that it compares:

<!-- table check -->
| gk runs | tool runs | runs with a recorded value | values compared | of these, on runs that did not end by themselves |
|---|---|---|---|---|
| 195 | 0 | 87 | 87 | 57 |
<!-- end table -->

`$GK` stands for the gk binary and `$MCREF` for the tool's `mcref.py`. Every command of `runs.tsv` runs
in the folder that its column `cwd` names, relative to this folder's parent (`paper2026/`).

## Results

<!-- table budget -->
| input | limit | method | value | answered by | ended by itself | first limit |
|---|---|---|---|---|---|---|
| the delivery plan of 32 legs | 2 s | default | (.21733, 0, 0, .78267) | general | no | searches stopped: 2 cut, 153 queued |
| the delivery plan of 32 legs | 10 s | default | (.029358, 0, 0, .970642) | general | no | searches stopped: 31 cut, 1 queued |
| the delivery plan of 32 legs | 60 s | default | (.029358, 0, 0, .970642) | general | no | searches stopped: 10 cut, 0 queued |
| the grid of 56 edges | 10 s | default | (.53227, 0, 0, .46773) | exact | yes | - |
| the grid of 56 edges | 60 s | default | (.53227, 0, 0, .46773) | exact | yes | - |
| the library member (English case N2) | 10 s | default | (.010993, .949195, 0, .039812) | general | no | searches stopped: 31 cut, 45 queued |
| the library member (English case N2) | 10 s | general | (.010993, .949195, 0, .039812) | general | no | searches stopped: 32 cut, 44 queued |
| the library member (English case N2) | 60 s | default | (.010993, .949195, 0, .039812) | general | no | searches stopped: 86 cut, 0 queued |
| the library member (English case N2) | 60 s | general | (.010993, .949195, 0, .039812) | general | no | searches stopped: 86 cut, 0 queued |
| does John eat berries (English case N4) | 10 s | default | (.98, 0, 0, .02) | general | no | searches stopped: 19 cut, 2 queued |
| does John eat berries (English case N4) | 10 s | general | (.98, 0, 0, .02) | general | no | searches stopped: 19 cut, 2 queued |
| does John eat berries (English case N4) | 60 s | default | (0, .98, 0, .02) | general | no | searches stopped: 30 cut, 0 queued |
| does John eat berries (English case N4) | 60 s | general | (0, .98, 0, .02) | general | no | searches stopped: 30 cut, 0 queued |
<!-- end table -->

### The effect of a longer time limit

Every run of the archive that was wrong, without a value or not complete at 10 s ran again with `-seconds 600`,
under a cap of 12 GB and 660 s. The runs `n2/` of `runs.tsv` are 92 runs at 600 s, one per input and
method, and two runs at 10 s, `english/library@10s.exact` and `english/berries@10s.exact`, which give the values
at 10 s of the two English cases under the exact method. Their inputs are those of parts O3, O7, O14,
O15, O19 and O20; `runs.tsv` names them. "Right" compares the value with the target: an
exact target to 1e-6, a printed target to half a unit of its last decimal, a sampled value of the tool within its
bound. The run at 10 s is the run of the part that holds the input (column `run_10s` of `longer_limit.csv`); for
the two English cases under the exact method it is a run of the same group at 10 s. `longer_limit.csv` has one
row per input and method, with both values, the marks complete, the judgements and the end of the run at 600 s.

<!-- table longer -->
| group | method | runs | wrong or without a value at 10 s | of these right at 600 s | right but not complete at 10 s | of these complete at 600 s | without a target | the same value at 10 s and 600 s | ended by itself at 600 s |
|---|---|---|---|---|---|---|---|---|---|
| benchmark families | exact | 22 | 12 | 0 | 8 | 0 | 2 | 22 | 0 |
| benchmark families | general | 26 | 14 | 0 | 0 | 0 | 2 | 24 | 9 |
| routes | exact | 3 | 1 | 0 | 2 | 0 | 0 | 3 | 0 |
| routes | general | 5 | 3 | 0 | 0 | 0 | 0 | 4 | 3 |
| university base with a contradiction | exact | 8 | 2 | 0 | 6 | 0 | 0 | 8 | 0 |
| university base with a contradiction | general | 8 | 0 | 0 | 0 | 0 | 0 | 8 | 6 |
| outside the classes | exact | 6 | 4 | 0 | 1 | 0 | 0 | 6 | 1 |
| outside the classes | general | 6 | 0 | 0 | 0 | 0 | 0 | 6 | 6 |
| defeasible logic | exact | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 1 |
| defeasible logic | general | 3 | 3 | 0 | 0 | 0 | 0 | 2 | 2 |
| English cases | exact | 2 | 0 | 0 | 0 | 0 | 2 | 2 | 0 |
| English cases | general | 2 | 0 | 0 | 0 | 0 | 2 | 0 | 0 |
| all |  | 92 | 40 | 1 | 17 | 0 | 8 | 85 | 28 |
<!-- end table -->

The runs whose value at 600 s differs from the value at 10 s:

<!-- table changed -->
| input | method | target | value at 10 s | right | value at 600 s | right | complete at 600 s |
|---|---|---|---|---|---|---|---|
| bn/gk_andes_snode_151.gkp | general | (.7955, 0, 0, .2045) | (.630096, 0, 0, .369904) | no | no value | - | - |
| bn/gk_andes_snode_74.gkp | general | (.8971, 0, 0, .1029) | (.572286, 0, 0, .427714) | no | no value | - | - |
| inputs/route_opp_20.gkp | general | (0.129986, 0, 0, 0.870014, 0) | (0, 0, 0, 1) | no | (.267589, 0, 0, .732411) | no | - |
| gk/tree_b2_d14.gkp | exact | (1, 0, 0, 0, 0) | no value | - | (1, 0, 0, 0) | yes | yes |
| gk/tree_b2_d14.gkp | general | (1, 0, 0, 0, 0) | no value | - | (0, 0, 0, 1) | no | - |
| n2v2/gk_deepseek.js | general | - | (.010993, .949195, 0, .039812) | - | (.002478, .949195, 0, .048327) | - | - |
| n4/gk.js | general | - | (.98, 0, 0, .02) | - | (0, .98, 0, .02) | - | - |
<!-- end table -->

## Where the paper's numbers are

- The paragraph on the time budget, and row C of the table of limits (part O3): the rows of `results.csv`,
  columns `value`, `limit_s` and `first_limit`.
- The effect of a longer time limit (Section 7.6, "1 of 40"): the row "all" of the first table above, from
  `longer_limit.csv`, columns `target`, `right_10s`, `right_600s`, `complete_10s` and `complete_600s`; "Does
  John eat berries?": the rows of the input `O7_english/inputs/n4/gk.js`, here and in the table of the time
  budget above.

`results.csv` has one row per run and answer. The columns are described on the first page of the
folder ([`../README.md`](../README.md), section "The tables of a part").
