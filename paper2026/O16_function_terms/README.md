# O16: function terms: the delivery plans

This part holds the delivery plans with function terms on gk and on the other systems, the delivery inputs
written without function terms against the tool, and the count of complete answers of the exact method on
inputs with function terms. The plans are the delivery family of part O3.

## Where the inputs come from

The plans were written for the paper: `../O3_families/inputs/delivery/`. The inputs without function terms are
in `inputs/flat_delivery/`. The ProbLog programs of the plans are in `../O3_families/inputs/delivery/`.

## Rerun

To rerun every gk and tool run of this part and compare each value with `results.csv`:

```sh
python3 check_gk.py --part O16_function_terms --gk PATH/TO/gk --mcref PATH/TO/mcref.py
```

Its last line names the values compared and how many differ. Every value is expected to be equal, except that
a value can change from run to run when the recorded run did not end by itself or the rerun reports cut or
queued searches; the check reports such a difference apart. The runs and values that it compares:

<!-- table check -->
| gk runs | tool runs | runs with a recorded value | values compared | of these, on runs that did not end by themselves |
|---|---|---|---|---|
| 8 | 4 | 12 | 12 | 2 |
<!-- end table -->

`$GK` stands for the gk binary and `$MCREF` for the tool's `mcref.py`. Every command of `runs.tsv` runs
in the folder that its column `cwd` names, relative to this folder's parent (`paper2026/`).

## Results

The plans on gk and the other systems:

<!-- table delivery -->
| plan | calculated value | gk 1.3.2, the default | ProbLog | smProbLog | plingo | PASTA |
|---|---|---|---|---|---|---|
| gk_legs2_control.gkp | (.69255, 0, 0, .30745) | (.69255, 0, 0, .30745), by the general method, 0.52 s | same value 0.69255 | no answer | no encoding | no encoding |
| gk_legs8_control.gkp | (.368049, 0, 0, .631951) | (.368049, 0, 0, .631951), by the general method, 6.31 s | same value 0.36804946 | no answer | no encoding | no encoding |
| gk_legs32_control.gkp | (.029358, 0, 0, .970642) | (.029358, 0, 0, .970642), by the general method, limit | same value 0.029357997 | no answer | no encoding | no encoding |
| gk_legs8_opposed.gkp | (.286261, 0, 0, .713739) | (.286261, 0, 0, .713739), by the general method, limit | no encoding | no encoding | no encoding | no encoding |
<!-- end table -->

The inputs without function terms, against the tool:

<!-- table flat -->
| input | calculated value | the exact method | the tool |
|---|---|---|---|
| deliv_ctl_long_flat | (.69255, 0, 0, .30745) | (.69255, 0, 0, .30745), complete, 0.05 s | (.69255, 0, 0, .30745), exact value of the tool |
| deliv_ctl_short_flat | (.5985, 0, 0, .4015) | (.5985, 0, 0, .4015), complete, 0.06 s | (.5985, 0, 0, .4015), exact value of the tool |
| deliv_opp_long_flat | (.53865, 0, 0, .46135) | (.53865, 0, 0, .46135), complete, 0.05 s | (.53865, 0, 0, .46135), exact value of the tool |
| deliv_opp_short_flat | (.4655, 0, 0, .5345) | (.4655, 0, 0, .5345), complete, 0.06 s | (.4655, 0, 0, .5345), exact value of the tool |
<!-- end table -->

The complete answers of the exact method on inputs with a function term (`complete_with_function_terms.csv`,
from the runs of parts O3 and O13). The default sends every input with a function term to the general method,
so these answers come from runs with `-exact`.

<!-- table complete -->
| kind of input, group of runs | complete answers on inputs with a function term |
|---|---|
| exact method, a1_fam_exact | 26 |
| exact method, a3_exact | 14 |
| all | 40 |
<!-- end table -->

## Where the paper's numbers are

- The function terms (the text does not cite this part): the table of the plans, and `complete_with_function_terms.csv` for
  the count of complete answers.
- "the tool confirms the delivery inputs without function terms": the rows of `flat_delivery.csv` and of the
  inputs `deliv_*` in `results.csv`.

`results.csv` has one row per run and answer. The columns are described on the first page of the
folder ([`../README.md`](../README.md), section "The tables of a part").
