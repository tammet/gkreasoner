# O11_text_examples: the small examples of the text

This part holds the small examples of Sections 1 and 4 to 6 of the paper and the inputs of the stated limits of the definition. Each input has a question and the value of the semantics that the paper or this part
states (column `target`). gk 1.3.2 answers each input under the default, and the tool computes it. Two inputs equal generated inputs of part O13 byte for byte; their gk rows take the runs of those inputs and say so in `note`.

The table compares both with the stated value. A stated value of four numbers is compared share by share, and a
single number with the for share. A number with decimals allows half a unit of its last decimal; an integer is
exact.

## Rerun

From the folder `paper2026/`, for one input:

```sh
cd O11_text_examples/inputs && $GK s4_1_penguin.gkp
```

To rerun every gk and tool run of this part and compare each value with `results.csv`:

```sh
python3 check_gk.py --part O11_text_examples --gk PATH/TO/gk --mcref PATH/TO/mcref.py
```

Its last line names the values compared and how many differ. Every value is expected to be equal, except that
a value can change from run to run when the recorded run did not end by itself or the rerun reports cut or
queued searches; the check reports such a difference apart. The runs and values that it compares:

<!-- table check -->
| gk runs | tool runs | runs with a recorded value | values compared | of these, on runs that did not end by themselves |
|---|---|---|---|---|
| 21 | 19 | 40 | 40 | 0 |
<!-- end table -->

`$GK` stands for the gk binary and `$MCREF` for the tool's `mcref.py`. Every command of `runs.tsv` runs
in the folder that its column `cwd` names, relative to this folder's parent (`paper2026/`).

## Results

<!-- table targets -->
| case | question | the stated value | gk 1.3.2, the default | against the stated value | the tool | against the stated value |
|---|---|---|---|---|---|---|
| s1_bird_conflict | flies(a) | (0, 0, 0, 1) | (0, 0, 0, 1), complete, by the exact method, 0.06 s | equal | (0, 0, 0, 1) | equal |
| s4_1_penguin | penguin(tweety) | .56 | (.56, 0, 0, .44), complete, by the exact method, 0.07 s | equal | (.56, 0, 0, .44) | equal |
| s4_2_certain_rule_bird | bird(t) | (0, 1, 0, 0) | (0, 1, 0, 0), complete, by the exact method, 0.06 s | equal | (0, 1, 0, 0) | equal |
| s4_2_rule_099_bird | bird(t) | (0, 0, 0, 1) | (0, 0, 0, 1), complete, by the exact method, 0.06 s | equal | (0, 0, 0, 1) | equal |
| s4_2_rule_08_bird | bird(t) | (0, 0, 0, 1) | (0, 0, 0, 1), complete, by the exact method, 0.07 s | equal | (0, 0, 0, 1) | equal |
| s5_case_split_q | q | (1, 0, 0, 0) | (1, 0, 0, 0), complete, by the exact method, 0.06 s | equal | (1, 0, 0, 0) | equal |
| s6_1_combined_b | b | .42 | (.42, 0, 0, .58), complete, by the exact method, 0.07 s | equal | (.42, 0, 0, .58) | equal |
| s6_4_shared_premise_q | q | (.5, 0, 0, .5) | (.5, 0, 0, .5), complete, by the exact method, 0.06 s | equal | (.5, 0, 0, .5) | equal |
| a2_1_one_sign_a | a | (.5, 0, 0, .5) | (.5, 0, 0, .5), complete, by the exact method, 0.06 s | equal | (.5, 0, 0, .5) | equal |
| a2_1_one_sign_b | b | (.5, 0, 0, .5) | (.5, 0, 0, .5), complete, by the exact method, 0.06 s | equal | (.5, 0, 0, .5) | equal |
| a2_1_exception_cycle_p | p | (0, 0, 0, 1) | (0, 0, 0, 1), complete, by the exact method, 0.05 s | equal | (0, 0, 0, 1) | equal |
| a2_1_exception_cycle_q | q | (0, 0, 0, 1) | (0, 0, 0, 1), complete, by the exact method, 0.06 s | equal | (0, 0, 0, 1) | equal |
| a2_1_exception_cycle_r | r | (0, 0, 0, 1) | (0, 0, 0, 1), complete, by the exact method, 0.07 s | equal | (0, 0, 0, 1) | equal |
| a2_5_selection_p | p | (.64, .04, .16, .16) | (.64, .04, .16, .16), complete, by the exact method, 0.06 s | equal | (.64, .04, .16, .16) | equal |
| a2_5_selection_r | r | (.64, .04, .16, .16) | (.64, .04, .16, .16), complete, by the exact method, 0.05 s | equal | (.64, .04, .16, .16) | equal |
| s4_3_default_vs_fact | flies(t) | (.63, .3, 0, .07) | (.63, .3, 0, .07), complete, by the exact method, 0.06 s | equal | (.63, .3, 0, .07) | equal |
| s4_3_rule_vs_fact | flies(t) | (.6, 0, .3, .1) | (.6, 0, .3, .1), complete, by the exact method, 0.05 s | equal | (.6, 0, .3, .1) | equal |
| s4_3_nixon | pacifist(n) | (0, 0, 0, 1) | (0, 0, 0, 1), complete, by the exact method, 0.06 s | equal | (0, 0, 0, 1) | equal |
| s4_3_nixon_uncertain | pacifist(n) | (.32, .12, 0, .56) | (.32, .12, 0, .56), complete, by the exact method, 0.06 s | equal | (.32, .12, 0, .56) | equal |
<!-- end table -->

`results.csv` has one row per run and answer. The columns are described on the first page of the
folder ([`../README.md`](../README.md), section "The tables of a part").
