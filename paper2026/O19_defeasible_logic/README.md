# O19: theories of defeasible logic

This part holds scalable theories of defeasible logic in six families: a chain of defeasible rules, a chain of
strict rules, trees, a cascade with equal ranks, a cascade with priorities, and a disputed family. Each theory is
written in three forms: for gk, for SPINdle 2.2.4 and for DEFT 1.0.0. Every system gets the same signed question.

## Where the inputs come from

The families follow the scalable test theories of the defeasible-logic literature (2001). The theories were
generated for this paper by the scripts of the earlier comparison; `inputs/theories.tar.xz` holds the three forms (`gk/`, `dfl/` for SPINdle, `dlgp/` for DEFT), with
the listing `inputs/theories.files.tsv`. Unpack with `tar -xJf inputs/theories.tar.xz -C inputs`.
`tools/DeftRun.java` is the driver that loads one DEFT theory and prints the status of each query.

**Reading the cells.** gk: "holds" is (1, 0, 0, 0), "the opposite holds" is (0, 1, 0, 0), "neither" is
(0, 0, 0, 1). SPINdle: the tags of the question; its time includes all conclusions of the theory, which SPINdle
computes and prints. DEFT: the status of the question; its time includes the saturation of the whole theory.

## Rerun

To rerun every gk and tool run of this part and compare each value with `results.csv`:

```sh
python3 check_gk.py --part O19_defeasible_logic --gk PATH/TO/gk --mcref PATH/TO/mcref.py
```

Its last line names the values compared and how many differ. Every value is expected to be equal, except that
a value can change from run to run when the recorded run did not end by itself or the rerun reports cut or
queued searches; the check reports such a difference apart. The runs and values that it compares:

<!-- table check -->
| gk runs | tool runs | runs with a recorded value | values compared | of these, on runs that did not end by themselves |
|---|---|---|---|---|
| 99 | 0 | 95 | 95 | 10 |
<!-- end table -->

`$GK` stands for the gk binary and `$MCREF` for the tool's `mcref.py`. Every command of `runs.tsv` runs
in the folder that its column `cwd` names, relative to this folder's parent (`paper2026/`).

## Results

<!-- table theories -->
| family | size | the exact method | the general method | the default | SPINdle 2.2.4 | DEFT 1.0.0 |
|---|---|---|---|---|---|---|
| chain of defeasible rules | 5 | holds, complete, 0.06 s | holds, 0.38 s | holds, complete, by the exact method, 0.05 s | -D +d, 0.17 s | another quantity: a5(c) DEFEASIBLY_ENTAILED, 0.64 s |
| chain of defeasible rules | 10 | holds, complete, 0.06 s | holds, 1.52 s | holds, complete, by the exact method, 0.06 s | -D +d, 0.14 s | another quantity: a10(c) DEFEASIBLY_ENTAILED, 0.63 s |
| chain of defeasible rules | 100 | holds, complete, 0.06 s | holds, limit | holds, complete, by the exact method, 0.06 s | -D +d, 0.20 s | another quantity: a100(c) DEFEASIBLY_ENTAILED, 0.69 s |
| chain of defeasible rules | 200 | holds, complete, 0.07 s | holds, limit | holds, complete, by the exact method, 0.07 s | -D +d, 0.20 s | another quantity: a200(c) DEFEASIBLY_ENTAILED, 0.72 s |
| chain of defeasible rules | 300 | holds, complete, 0.07 s | neither, 1.84 s | holds, complete, by the exact method, 0.07 s | -D +d, 0.20 s | another quantity: a300(c) DEFEASIBLY_ENTAILED, 0.73 s |
| chain of defeasible rules | 500 | holds, complete, 0.07 s | neither, 1.87 s | holds, complete, by the exact method, 0.07 s | -D +d, 0.23 s | another quantity: a500(c) DEFEASIBLY_ENTAILED, 0.83 s |
| chain of defeasible rules | 1000 | holds, complete, 0.10 s | neither, 1.86 s | holds, complete, by the exact method, 0.10 s | -D +d, 0.27 s | another quantity: a1000(c) DEFEASIBLY_ENTAILED, 1.14 s |
| chain of defeasible rules | 5000 | holds, complete, 0.62 s | neither, 2.02 s | holds, complete, by the exact method, 0.61 s | -D +d, 0.49 s | no answer: Exception in thread "main" java.lang.StackOverflowError (exit 1), 8.08 s |
| chain of defeasible rules | 10000 | holds, complete, 2.14 s | neither, 2.23 s | holds, complete, by the exact method, 2.14 s | -D +d, 0.73 s | no answer: Exception in thread "main" java.lang.StackOverflowError (exit 1), 28.40 s |
| chain of strict rules | 10 | holds, complete, 0.05 s | holds, 0.61 s | holds, complete, by the exact method, 0.05 s | +D +d, 0.18 s | no encoding |
| chain of strict rules | 100 | holds, complete, 0.05 s | holds, limit | holds, complete, by the exact method, 0.06 s | +D +d, 0.19 s | no encoding |
| chain of strict rules | 1000 | holds, complete, 0.09 s | holds, limit | holds, complete, by the exact method, 0.09 s | +D +d, 0.39 s | no encoding |
| chain of strict rules | 10000 | holds, complete, 2.07 s | no value: gk's error: db memory allocation error: the database of 5000 MB is full (the option -mbsize sets its size in MB): cannot extend datarec area with a new subarea of size: 8192 | holds, complete, by the exact method, 2.08 s | +D +d, 1.37 s | no encoding |
| tree | 2 branches, depth 5 | holds, complete, 0.06 s | holds, limit | holds, complete, by the exact method, 0.06 s | -D +d, 0.18 s | another quantity: t1(c) DEFEASIBLY_ENTAILED, 0.68 s |
| tree | 3 branches, depth 5 | holds, complete, 0.06 s | neither, 1.83 s | holds, complete, by the exact method, 0.07 s | -D +d, 0.23 s | another quantity: t1(c) DEFEASIBLY_ENTAILED, 0.73 s |
| tree | 2 branches, depth 10 | holds, complete, 0.12 s | neither, 1.89 s | holds, complete, by the exact method, 0.13 s | -D +d, 0.46 s | another quantity: t1(c) DEFEASIBLY_ENTAILED, 1.32 s |
| tree | 2 branches, depth 14 | no value: time limit, proof not found | no value: time limit, proof not found | no value: time limit, proof not found | -D +d, 3.57 s | did not end: did not end (60 s), limit |
| cascade with equal ranks | 4 | holds, complete, 0.05 s | holds, 0.42 s | holds, complete, by the exact method, 0.06 s | -D, 0.16 s | another quantity: a0(c) DEFEASIBLY_ENTAILED; na0(c) NOT_ENTAILED, 0.68 s |
| cascade with priorities | 4 | holds, complete, 0.06 s | holds, 0.42 s | holds, complete, by the exact method, 0.05 s | -D +d, 0.16 s | another quantity: a0(c) DEFEASIBLY_ENTAILED; na0(c) NOT_ENTAILED, 0.71 s |
| cascade with equal ranks | 5 | neither, complete, 0.06 s | neither, 0.51 s | neither, complete, by the exact method, 0.06 s | -D, 0.15 s | another quantity: a0(c) DEFEASIBLY_ENTAILED; na0(c) NOT_ENTAILED, 0.67 s |
| cascade with priorities | 5 | the opposite holds, complete, 0.05 s | the opposite holds, 0.58 s | the opposite holds, complete, by the exact method, 0.05 s | -D -d, 0.17 s | another quantity: a0(c) NOT_ENTAILED; na0(c) DEFEASIBLY_ENTAILED, 0.69 s |
| cascade with equal ranks | 10 | holds, complete, 0.06 s | holds, 1.16 s | holds, complete, by the exact method, 0.06 s | -D, 0.16 s | another quantity: a0(c) DEFEASIBLY_ENTAILED; na0(c) NOT_ENTAILED, 0.66 s |
| cascade with priorities | 10 | holds, complete, 0.06 s | holds, 1.06 s | holds, complete, by the exact method, 0.06 s | -D +d, 0.16 s | another quantity: a0(c) DEFEASIBLY_ENTAILED; na0(c) NOT_ENTAILED, 0.69 s |
| cascade with equal ranks | 50 | holds, complete, 0.06 s | holds, 6.60 s | holds, complete, by the exact method, 0.06 s | -D, 0.23 s | another quantity: a0(c) DEFEASIBLY_ENTAILED; na0(c) NOT_ENTAILED, 0.71 s |
| cascade with priorities | 50 | holds, complete, 0.06 s | holds, limit | holds, complete, by the exact method, 0.06 s | -D +d, 0.19 s | another quantity: a0(c) DEFEASIBLY_ENTAILED; na0(c) NOT_ENTAILED, 0.93 s |
| cascade with equal ranks | 200 | holds, complete, 0.07 s | neither, limit | holds, complete, by the exact method, 0.07 s | -D, 0.50 s | another quantity: a0(c) DEFEASIBLY_ENTAILED; na0(c) NOT_ENTAILED, 0.88 s |
| cascade with priorities | 200 | holds, complete, 0.07 s | holds, limit | holds, complete, by the exact method, 0.06 s | -D +d, 0.35 s | another quantity: a0(c) DEFEASIBLY_ENTAILED; na0(c) NOT_ENTAILED, 2.57 s |
| cascade with equal ranks | 2000 | holds, complete, 0.49 s | neither, limit | holds, complete, by the exact method, 0.48 s | -D, 54.54 s | another quantity: a0(c) DEFEASIBLY_ENTAILED; na0(c) NOT_ENTAILED, 5.55 s |
| cascade with priorities | 2000 | holds, complete, 0.48 s | the opposite holds, limit | holds, complete, by the exact method, 0.47 s | -D +d, 26.15 s | did not end: did not end (60 s), limit |
| disputed family | 10 | neither, complete, 0.05 s | neither, 0.12 s | neither, complete, by the exact method, 0.06 s | -D -d, 0.15 s | another quantity: a0(c) NOT_ENTAILED; na0(c) NOT_ENTAILED, 0.69 s |
| disputed family | 100 | neither, complete, 0.06 s | neither, 0.20 s | neither, complete, by the exact method, 0.06 s | -D -d, 0.18 s | another quantity: a0(c) NOT_ENTAILED; na0(c) NOT_ENTAILED, 0.83 s |
| disputed family | 1000 | neither, complete, 0.09 s | neither, 0.24 s | neither, complete, by the exact method, 0.09 s | -D -d, 0.34 s | another quantity: a0(c) NOT_ENTAILED; na0(c) NOT_ENTAILED, 1.95 s |
| disputed family | 10000 | neither, complete, 2.42 s | neither, 2.68 s | neither, complete, by the exact method, 2.41 s | -D -d, 1.14 s | did not end: did not end (60 s), limit |
<!-- end table -->

<!-- table summary -->
| system | theories | outcome | times of the runs that ended by themselves |
|---|---|---|---|
| the exact method | 33 | 32 complete | .05 to 2.42 s |
| SPINdle 2.2.4 | 33 | 33 answered | .14 to 54.54 s |
| DEFT 1.0.0 | 29 | 24 answered, 2 no answer, 3 did not end | .63 to 5.55 s |
<!-- end table -->

## Where the paper's numbers are

- The theories of defeasible logic (Sections 7.1, 7.5 and 7.6): the table above, from the rows of each system, columns
  `verdict`, `value`, `outcome` and `time_s`.

`results.csv` has one row per run and answer. The columns are described on the first page of the
folder ([`../README.md`](../README.md), section "The tables of a part").
