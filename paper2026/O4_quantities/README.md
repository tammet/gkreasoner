# O4: different quantities on the same input

This part holds the ten small inputs of the matrix from which the five-inputs table of Appendix D of the paper
takes five rows. Outside the common class the compared systems return different quantities for one input: the
support share of gk, ProbLog's probability, PASTA's credal interval, smProbLog's equal allocation, plingo's
normalization and the well-founded shares. A difference between two of these quantities is a contrast of
meanings.

gk 1.3.2 and the tool ran on all ten inputs of the matrix. The cells of the other systems come from the recorded
runs of the earlier comparison. Where a system
did not run, `enumerate.py` computed the quantity of its published semantics; such a cell has the outcome "not
run" and the computed quantity in `value`.

## Where the inputs come from

The inputs were written for the paper. Each case has a folder under `inputs/`; the file name says which system
reads it (`gk.gkp`, `problog*.pl`, `plingo*.plp`, `constrained.lp`).

## Rerun

From the folder `paper2026/`:

```sh
cd O4_quantities/inputs/c1_shared && $GK gk.gkp
```

The first line holds `"value":[0.44,0,0,0.56]`, answered by the exact method and complete.

To rerun every gk and tool run of this part and compare each value with `results.csv`:

```sh
python3 check_gk.py --part O4_quantities --gk PATH/TO/gk --mcref PATH/TO/mcref.py
```

Its last line names the values compared and how many differ. Every value is expected to be equal, except that
a value can change from run to run when the recorded run did not end by itself or the rerun reports cut or
queued searches; the check reports such a difference apart. The runs and values that it compares:

<!-- table check -->
| gk runs | tool runs | runs with a recorded value | values compared | of these, on runs that did not end by themselves |
|---|---|---|---|---|
| 10 | 10 | 20 | 20 | 0 |
<!-- end table -->

`$GK` stands for the gk binary and `$MCREF` for the tool's `mcref.py`. Every command of `runs.tsv` runs
in the folder that its column `cwd` names, relative to this folder's parent (`paper2026/`).

## Results

<!-- table cases -->
| case | question | calculated value | gk 1.3.2, the default | the tool |
|---|---|---|---|---|
| c1_shared | q | (.44, 0, 0, .56) | (.44, 0, 0, .56), complete, by the exact method, 0.06 s | (.44, 0, 0, .56), exact value of the tool; equal |
| c1b_positive_cycle | q | (.5, 0, 0, .5) | (.5, 0, 0, .5), complete, by the exact method, 0.06 s | (.5, 0, 0, .5), exact value of the tool; equal |
| c2_exception | flies(t) | (.27, 0, 0, .73) | (.27, 0, 0, .73), complete, by the exact method, 0.06 s | (.27, 0, 0, .73), exact value of the tool; equal |
| c2b_opposed_exception | flies(t) | (.54, 0, 0, .46) | (.54, 0, 0, .46), complete, by the exact method, 0.05 s | (.54, 0, 0, .46), exact value of the tool; equal |
| c3_contested | flies(a) | (0, 0, 0, 1) | (0, 0, 0, 1), complete, by the exact method, 0.07 s | (0, 0, 0, 1), exact value of the tool; equal |
| c4_equal_rank | pacifist(n) | (0, 0, 0, 1) | (0, 0, 0, 1), complete, by the exact method, 0.05 s | (0, 0, 0, 1), exact value of the tool; equal |
| c4b_priority | p | (.1, .8, 0, .1) | (.1, .8, 0, .1), complete, by the exact method, 0.05 s | (.1, .8, 0, .1), exact value of the tool; equal |
| c5_mutual_half | p(a) | (.25, 0, 0, .75) | (.25, 0, 0, .75), complete, by the exact method, 0.06 s | (.25, 0, 0, .75), exact value of the tool; equal |
| c5b_common_consequence | q | (0, 0, 0, 1) | (0, 0, 0, 1), complete, by the exact method, 0.05 s | (0, 0, 0, 1), exact value of the tool; equal |
| c6_locality | r | (.6, 0, 0, .4) | (.6, 0, 0, .4), complete, by the exact method, 0.05 s | (.6, 0, 0, .4), exact value of the tool; equal |
<!-- end table -->

The other systems and semantics:

<!-- table others -->
| case | system or semantics | outcome | value | relation of the encoding |
|---|---|---|---|---|
| c1_shared | ProbLog 2.3.0 | another quantity | .44 | exact translation |
| c1_shared | plingo 1.1.0 | another quantity | .44 | exact translation |
| c1_shared | credal semantics (PASTA) | not run | [.44, .44] | exact translation |
| c1_shared | equal allocation (smProbLog) | not run | .44 | exact translation |
| c1_shared | well-founded semantics | not run | (.44, .56, 0) | exact translation |
| c1b_positive_cycle | ProbLog 2.3.0 | another quantity | .5 | exact translation |
| c1b_positive_cycle | plingo 1.1.0 | another quantity | .5 | exact translation |
| c1b_positive_cycle | credal semantics (PASTA) | not run | [.5, .5] | exact translation |
| c1b_positive_cycle | equal allocation (smProbLog) | not run | .5 | exact translation |
| c1b_positive_cycle | well-founded semantics | not run | (.5, .5, 0) | exact translation |
| c2_exception | ProbLog 2.3.0 | another quantity | .27 | exact translation |
| c2_exception | plingo 1.1.0 | another quantity | .27 | exact translation |
| c2_exception | credal semantics (PASTA) | not run | [.27, .27] | exact translation |
| c2_exception | equal allocation (smProbLog) | not run | .27 | exact translation |
| c2_exception | well-founded semantics | not run | (.27, .73, 0) | exact translation |
| c2b_opposed_exception | ProbLog 2.3.0 | another quantity | .27 | non-equivalent analogue |
| c2b_opposed_exception | ProbLog 2.3.0 | another quantity | .459 | non-equivalent analogue |
| c2b_opposed_exception | plingo 1.1.0 | another quantity | .27 | non-equivalent analogue |
| c2b_opposed_exception | plingo 1.1.0 | another quantity | .459 | non-equivalent analogue |
| c2b_opposed_exception | credal semantics (PASTA) | not run | [.27, .27] | non-equivalent analogue |
| c2b_opposed_exception | credal semantics (PASTA) | not run | [.459, .459] | non-equivalent analogue |
| c2b_opposed_exception | equal allocation (smProbLog) | not run | .459 | non-equivalent analogue |
| c2b_opposed_exception | well-founded semantics | not run | (.459, .541, 0) | non-equivalent analogue |
| c3_contested | ProbLog 2.3.0 | another quantity | .45 | non-equivalent analogue |
| c3_contested | ProbLog 2.3.0 | another quantity | .225 | non-equivalent analogue |
| c3_contested | ProbLog 2.3.0 | another quantity | 0 | non-equivalent analogue |
| c3_contested | plingo 1.1.0 | another quantity | .45 | non-equivalent analogue |
| c3_contested | plingo 1.1.0 | another quantity | .225 | non-equivalent analogue |
| c3_contested | plingo 1.1.0 | another quantity | 0 | non-equivalent analogue |
| c3_contested | credal semantics (PASTA) | not run | [.45, .45] | non-equivalent analogue |
| c3_contested | credal semantics (PASTA) | not run | [.225, .225] | non-equivalent analogue |
| c3_contested | credal semantics (PASTA) | not run | [0, 0] | non-equivalent analogue |
| c3_contested | equal allocation (smProbLog) | not run | .225 | non-equivalent analogue |
| c3_contested | well-founded semantics | not run | (.225, .775, 0) | non-equivalent analogue |
| c4_equal_rank | ProbLog 2.3.0 | no answer | - | non-equivalent analogue |
| c4_equal_rank | plingo 1.1.0 | no answer | - | non-equivalent analogue |
| c4_equal_rank | plingo 1.1.0 | another quantity | .5 | non-equivalent analogue |
| c4_equal_rank | credal semantics (PASTA) | not run | [0, 1] | non-equivalent analogue |
| c4_equal_rank | equal allocation (smProbLog) | not run | .5 | non-equivalent analogue |
| c4_equal_rank | well-founded semantics | not run | (0, 0, 1) | non-equivalent analogue |
| c4b_priority | ProbLog 2.3.0 | another quantity | .18 | non-equivalent analogue |
| c4b_priority | plingo 1.1.0 | another quantity | .18 | non-equivalent analogue |
| c4b_priority | credal semantics (PASTA) | not run | [.18, .18] | non-equivalent analogue |
| c4b_priority | equal allocation (smProbLog) | not run | .18 | non-equivalent analogue |
| c4b_priority | well-founded semantics | not run | (.18, .82, 0) | non-equivalent analogue |
| c5_mutual_half | ProbLog 2.3.0 | no answer | - | non-equivalent analogue |
| c5_mutual_half | plingo 1.1.0 | another quantity | .40 | non-equivalent analogue |
| c5_mutual_half | credal semantics (PASTA) | not run | [.25, .5] | non-equivalent analogue |
| c5_mutual_half | equal allocation (smProbLog) | not run | .375 | non-equivalent analogue |
| c5_mutual_half | well-founded semantics | not run | (.25, .5, .25) | non-equivalent analogue |
| c5b_common_consequence | ProbLog 2.3.0 | no answer | - | non-equivalent analogue |
| c5b_common_consequence | plingo 1.1.0 | no answer | - | non-equivalent analogue |
| c5b_common_consequence | plingo 1.1.0 | another quantity | 1 | non-equivalent analogue |
| c5b_common_consequence | credal semantics (PASTA) | not run | [1, 1] | non-equivalent analogue |
| c5b_common_consequence | equal allocation (smProbLog) | not run | 1 | non-equivalent analogue |
| c5b_common_consequence | well-founded semantics | not run | (0, 0, 1) | non-equivalent analogue |
| c6_locality | ProbLog 2.3.0 | another quantity | .6 | non-equivalent analogue |
| c6_locality | ProbLog 2.3.0 | another quantity | .6 | non-equivalent analogue |
| c6_locality | plingo 1.1.0 | no answer | - | non-equivalent analogue |
| c6_locality | plingo 1.1.0 | another quantity | .6 | non-equivalent analogue |
| c6_locality | credal semantics (PASTA) | not run | no value | non-equivalent analogue |
| c6_locality | equal allocation (smProbLog) | not run | all mass inconsistent | non-equivalent analogue |
| c6_locality | well-founded semantics | not run | - | non-equivalent analogue |
| c1_shared | plingo 1.1.0 | no answer | - | - |
<!-- end table -->

## Where the paper's numbers are

- The five-inputs table of Appendix D: the rows with `system` gk 1.3.2 (column `value`) and the rows of the
  other systems (columns `outcome` and `value`).

`results.csv` has one row per run and answer. The columns are described on the first page of the
folder ([`../README.md`](../README.md), section "The tables of a part").
