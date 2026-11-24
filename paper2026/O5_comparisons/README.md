# O5: the 16 small cases on 9 systems

This part holds the comparison table of 16 small cases, each stated in gk and in the languages of nine other
systems: ProbLog, PASTA, plingo, smProbLog, TweetyProject, clingo, DLV and I-DLV, and s(CASP). gk 1.3.2 answers
the 18 gk inputs under the default, the general method and the exact method; the tool computes the inputs that it
accepts. The cells of the other systems come from the recorded runs of the table, with the versions of
`../SYSTEMS.md`; each cell has one outcome: same value, another quantity, no answer, did not end, no encoding.

## Where the inputs come from

The cases were constructed for the paper. `inputs/<system>/` holds each system's encoding. The gk runs read the
copies of the gk inputs in part O2 (`../O2_record/inputs/table/`), which are the same files.

## Rerun

From the folder `paper2026/`:

```sh
cd O2_record/inputs/table && $GK d3.gkp
```

The first line holds `"value":[0,0,0,1]` for the contested premise (row D3): ignorance.

To rerun every gk and tool run of this part and compare each value with `results.csv`:

```sh
python3 check_gk.py --part O5_comparisons --gk PATH/TO/gk --mcref PATH/TO/mcref.py
```

Its last line names the values compared and how many differ. Every value is expected to be equal, except that
a value can change from run to run when the recorded run did not end by itself or the rerun reports cut or
queued searches; the check reports such a difference apart. The runs and values that it compares:

<!-- table check -->
| gk runs | tool runs | runs with a recorded value | values compared | of these, on runs that did not end by themselves |
|---|---|---|---|---|
| 54 | 18 | 69 | 89 | 0 |
<!-- end table -->

`$GK` stands for the gk binary and `$MCREF` for the tool's `mcref.py`. Every command of `runs.tsv` runs
in the folder that its column `cwd` names, relative to this folder's parent (`paper2026/`).

## Results

<!-- table table -->
| row | input | the default | answered by | complete | the exact method | the tool | ProbLog | PASTA | plingo | smProbLog | TweetyProject | clingo | DLV | s(CASP) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C1 | c1.gkp | (.8, 0, 0, .2) | exact | yes | (.8, 0, 0, .2) | (.8, 0, 0, .2) | same value | same value | same value | same value | no encoding | no encoding | no encoding | no encoding |
| C2 | c2.gkp | (.3, 0, 0, .7) | exact | yes | (.3, 0, 0, .7) | (.3, 0, 0, .7) | same value | same value | same value | same value | no encoding | no encoding | no encoding | no encoding |
| D1 | d1.gkp | (.1, .9, 0, 0) | exact | yes | (.1, .9, 0, 0) | (.1, .9, 0, 0) | another quantity | another quantity | another quantity | another quantity | no encoding | another quantity | another quantity | another quantity |
| D2 | d2.gkp | (.54, 0, 0, .46) | exact | yes | (.54, 0, 0, .46) | (.54, 0, 0, .46) | another quantity | another quantity | another quantity | another quantity | no encoding | another quantity | another quantity | another quantity |
| D3 | d3.gkp | (0, 0, 0, 1) | exact | yes | (0, 0, 0, 1) | (0, 0, 0, 1) | another quantity | another quantity | another quantity | another quantity | no encoding | another quantity | another quantity | another quantity |
| D4 | d4.gkp | (0, 0, 0, 1) | exact | yes | (0, 0, 0, 1) | (0, 0, 0, 1) | no answer | another quantity | another quantity | another quantity | another quantity | another quantity | another quantity | another quantity |
| D4-P | d4sm_pos.gkp | (.32, .12, 0, .56) | exact | yes | (.32, .12, 0, .56) | (.32, .12, 0, .56) | no encoding | another quantity | another quantity | another quantity | no encoding | no encoding | no encoding | no encoding |
| D4-P | d4sm_neg.gkp | (.12, .32, 0, .56) | exact | yes | (.12, .32, 0, .56) | (.12, .32, 0, .56) | no encoding | another quantity | another quantity | another quantity | no encoding | no encoding | no encoding | no encoding |
| D5 | d5.gkp | (.6, .3, 0, .1) | exact | yes | (.6, .3, 0, .1) | (.6, .3, 0, .1) | another quantity | another quantity | another quantity | another quantity | another quantity | another quantity | another quantity | another quantity |
| D6 | d6_undercut.gkp | (1, 0, 0, 0) | exact | yes | (1, 0, 0, 0) | (1, 0, 0, 0) | another quantity | another quantity | another quantity | another quantity | no encoding | another quantity | another quantity | another quantity |
| D6 | d6_rebut.gkp | (1, 0, 0, 0) | exact | yes | (1, 0, 0, 0) | (1, 0, 0, 0) | another quantity | another quantity | another quantity | another quantity | no encoding | another quantity | another quantity | another quantity |
| D7 | d7.gkp | (.36, .48, 0, .16) | exact | yes | (.36, .48, 0, .16) | (.36, .48, 0, .16) | another quantity | another quantity | another quantity | another quantity | no encoding | no encoding | no encoding | no encoding |
| N1 | n1_study4.gkp | (.5, 0, 0, .5); (.3, 0, 0, .7); (.3, 0, 0, .7); (.6, 0, 0, .4) | exact | yes | (.5, 0, 0, .5); (.3, 0, 0, .7); (.3, 0, 0, .7); (.6, 0, 0, .4) | (.5, 0, 0, .5); (.3, 0, 0, .7); (.3, 0, 0, .7); (.6, 0, 0, .4) | same value | same value | same value | same value | no encoding | another quantity | another quantity | another quantity |
| N2 | n2_study10.gkp | (.8, 0, 0, .2); (.688, 0, 0, .312); (.1376, 0, 0, .8624) | exact | yes | (.8, 0, 0, .2); (.688, 0, 0, .312); (.1376, 0, 0, .8624) | (.8, 0, 0, .2); (.688, 0, 0, .312); (.1376, 0, 0, .8624) | same value | same value | same value | same value | no encoding | another quantity | another quantity | another quantity |
| EQ1 | e1.gkp | (.396, .056, .504, .044) | general | - | not covered: an equality between terms | declines: equality | another quantity | no answer | another quantity | another quantity | no encoding | no answer | no answer | no answer |
| X1 | x1.gkp | (1, 0, 0, 0) | exact | yes | (1, 0, 0, 0) | (1, 0, 0, 0) | no encoding | no answer | another quantity | another quantity | no encoding | no answer | no answer | no answer |
| F1 | f1.gkp | (.576, 0, 0, .424) | general | - | (.576, 0, 0, .424) | declines: function symbols | same value | did not end | did not end | did not end | no encoding | did not end | did not end | another quantity |
| DJ1 | dj1.gkp | (.72, 0, 0, .28) | exact | yes | (.72, 0, 0, .28) | (.72, 0, 0, .28) | no encoding | another quantity | no answer | another quantity | no encoding | another quantity | another quantity | another quantity |
<!-- end table -->

`results.csv` gives each cell with its detail in `note`: the meaning of the quantity, the message of a system
that gave no answer, or the limit of a run that did not end.

## Where the paper's numbers are

- The contested premise (row D3) in Section 7.2, and the whole table in Appendix D: the rows of the
  row, columns `value`, `outcome` and `note`.

`results.csv` has one row per run and answer. The columns are described on the first page of the
folder ([`../README.md`](../README.md), section "The tables of a part").
