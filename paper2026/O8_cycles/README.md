# O8_cycles: further examples of cycles

This part holds the further examples of cycles of the paper's appendix. Each input has a question and the value of the semantics that the paper or this part
states (column `target`). gk 1.3.2 answers each input under the default, and the tool computes it.

The table compares both with the stated value. A stated value of four numbers is compared share by share, and a
single number with the for share. A number with decimals allows half a unit of its last decimal; an integer is
exact.

## Rerun

From the folder `paper2026/`, for one input:

```sh
cd O8_cycles/inputs && $GK 01_chain_q.gkp
```

To rerun every gk and tool run of this part and compare each value with `results.csv`:

```sh
python3 check_gk.py --part O8_cycles --gk PATH/TO/gk --mcref PATH/TO/mcref.py
```

Its last line names the values compared and how many differ. Every value is expected to be equal, except that
a value can change from run to run when the recorded run did not end by itself or the rerun reports cut or
queued searches; the check reports such a difference apart. The runs and values that it compares:

<!-- table check -->
| gk runs | tool runs | runs with a recorded value | values compared | of these, on runs that did not end by themselves |
|---|---|---|---|---|
| 33 | 33 | 66 | 66 | 0 |
<!-- end table -->

`$GK` stands for the gk binary and `$MCREF` for the tool's `mcref.py`. Every command of `runs.tsv` runs
in the folder that its column `cwd` names, relative to this folder's parent (`paper2026/`).

## Results

<!-- table targets -->
| case | question | the stated value | gk 1.3.2, the default | against the stated value | the tool | against the stated value |
|---|---|---|---|---|---|---|
| 01_chain_q | q | (.64, .04, .16, .16) | (.64, .04, .16, .16), complete, by the exact method, 0.07 s | equal | (.64, .04, .16, .16) | equal |
| 01_chain_p | p | (.64, .04, .16, .16) | (.64, .04, .16, .16), complete, by the exact method, 0.05 s | equal | (.64, .04, .16, .16) | equal |
| 01_chain_r | r | (.64, .04, .16, .16) | (.64, .04, .16, .16), complete, by the exact method, 0.06 s | equal | (.64, .04, .16, .16) | equal |
| 02_uncertain_bird_bird | bird(t) | (0, .2, .8, 0) | (0, .2, .8, 0), complete, by the exact method, 0.05 s | equal | (0, .2, .8, 0) | equal |
| 02_uncertain_bird_flies | flies(t) | (0, .2, .8, 0) | (0, .2, .8, 0), complete, by the exact method, 0.06 s | equal | (0, .2, .8, 0) | equal |
| 02_uncertain_bird_sings | sings(t) | (1, 0, 0, 0) | (1, 0, 0, 0), complete, by the exact method, 0.06 s | equal | (1, 0, 0, 0) | equal |
| 03_chain_stop_q | q | (.2, .3, .2, .3) | (.2, .3, .2, .3), complete, by the exact method, 0.07 s | equal | (.2, .3, .2, .3) | equal |
| 03_chain_stop_p | p | (.2, .15, .6, .05) | (.2, .15, .6, .05), complete, by the exact method, 0.06 s | equal | (.2, .15, .6, .05) | equal |
| 03_chain_stop_certain_q | q | (0, 1, 0, 0) | (0, 1, 0, 0), complete, by the exact method, 0.06 s | equal | (0, 1, 0, 0) | equal |
| 04_two_routes_q | q | (.7416, 0, 0, .2584) | (.7416, 0, 0, .2584), complete, by the exact method, 0.06 s | equal | (.7416, 0, 0, .2584) | equal |
| 04_two_routes_swapped_q | q | (.7416, 0, 0, .2584) | (.7416, 0, 0, .2584), complete, by the exact method, 0.05 s | equal | (.7416, 0, 0, .2584) | equal |
| 05_own_consequence_p | p | (.1, 0, .9, 0) | (.1, 0, .9, 0), complete, by the exact method, 0.05 s | equal | (.1, 0, .9, 0) | equal |
| 05_own_consequence_q | q | (.1, 0, 0, .9) | (.1, 0, 0, .9), complete, by the exact method, 0.06 s | equal | (.1, 0, 0, .9) | equal |
| 05_fact_against_fact_p | p | (.1, 0, .9, 0) | (.1, 0, .9, 0), complete, by the exact method, 0.06 s | equal | (.1, 0, .9, 0) | equal |
| 05_own_consequence_default_p | p | (1, 0, 0, 0) | (1, 0, 0, 0), complete, by the exact method, 0.06 s | equal | (1, 0, 0, 0) | equal |
| 06_three_facts_p | p | (0, 0, 1, 0) | (0, 0, 1, 0), complete, by the exact method, 0.06 s | equal | (0, 0, 1, 0) | equal |
| 06_three_facts_q | q | (0, 0, 1, 0) | (0, 0, 1, 0), complete, by the exact method, 0.06 s | equal | (0, 0, 1, 0) | equal |
| 06_three_facts_r | r | (0, 0, 1, 0) | (0, 0, 1, 0), complete, by the exact method, 0.06 s | equal | (0, 0, 1, 0) | equal |
| 07_disjunction_cycle_b | b | (.56, .06, .24, .14) | (.56, .06, .24, .14), complete, by the exact method, 0.06 s | equal | (.56, .06, .24, .14) | equal |
| 07_directed_rule_b | b | (.5, 0, .3, .2) | (.5, 0, .3, .2), complete, by the exact method, 0.06 s | equal | (.5, 0, .3, .2) | equal |
| 08_one_clause_q | q | (.84, 0, 0, .16) | (.84, 0, 0, .16), complete, by the exact method, 0.07 s | equal | (.84, 0, 0, .16) | equal |
| 09_default_certain_rule_flies | flies(p) | (.18, .8, 0, .02) | (.18, .8, 0, .02), complete, by the exact method, 0.06 s | equal | (.18, .8, 0, .02) | equal |
| 10_fact_default_rule_r | r | (.5, .45, 0, .05) | (.5, .45, 0, .05), complete, by the exact method, 0.06 s | equal | (.5, .45, 0, .05) | equal |
| 10_fact_default_rule_p | p | (.45, .5, 0, .05) | (.45, .5, 0, .05), complete, by the exact method, 0.06 s | equal | (.45, .5, 0, .05) | equal |
| 11_ordinary_first_p | p | (.8, 0, 0, .2) | (.8, 0, 0, .2), complete, by the exact method, 0.07 s | equal | (.8, 0, 0, .2) | equal |
| 12_mutual_pair_p | p(a) | (0, 0, 0, 1) | (0, 0, 0, 1), complete, by the exact method, 0.06 s | equal | (0, 0, 0, 1) | equal |
| 12_mutual_pair_b | b(a) | (0, 0, 0, 1) | (0, 0, 0, 1), complete, by the exact method, 0.05 s | equal | (0, 0, 0, 1) | equal |
| 12_mutual_pair_half_p | p(a) | (.25, 0, 0, .75) | (.25, 0, 0, .75), complete, by the exact method, 0.08 s | equal | (.25, 0, 0, .75) | equal |
| 13_yale_alive | alive(s2) | (0, 0, 0, 0) | (0, 0, 0, 0), complete, by the exact method, 0.06 s | equal | (0, 0, 0, 0) | equal |
| 13_yale_099_alive | alive(s2) | (.01, .99, 0, 0) | (.01, .99, 0, 0), complete, by the exact method, 0.07 s | equal | (.01, .99, 0, 0) | equal |
| 13_yale_q | q | (1, 0, 0, 0) | (1, 0, 0, 0), complete, by the exact method, 0.06 s | equal | (1, 0, 0, 0) | equal |
| 13_yale_walks | walks(s2) | (0, 0, 0, 0) | (0, 0, 0, 0), complete, by the exact method, 0.06 s | equal | (0, 0, 0, 0) | equal |
| 13_yale_buried | buried(s2) | (0, 0, 0, 0) | (0, 0, 0, 0), complete, by the exact method, 0.06 s | equal | (0, 0, 0, 0) | equal |
<!-- end table -->

`results.csv` has one row per run and answer. The columns are described on the first page of the
folder ([`../README.md`](../README.md), section "The tables of a part").
