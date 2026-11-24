# O1: the worked example (Tweety)

This part holds the Tweety stages of Section 2 of the paper. Each stage asks whether Tweety flies,
`flies(tweety)`. gk 1.3.2 answers every stage under the default, the exact method and the general method. The
tool computes stages 1 to 3b exactly. The cells of the other systems come from the recorded runs of the earlier
comparison; this part names their outcomes.

| stage | what the stage adds |
|---|---|
| 1 | an uncertain exception: a ranked penguin default against the flying default |
| 2 | the .7 penguin rule replaced by `gull(X) ; penguin(X) :- seabird(X)` and `0.7::-gull(tweety)` |
| 3a | stage 2 plus `0.9::gull(X) :- seabird(X), yellow_bill(X)` and `0.6::yellow_bill(tweety)` |
| 3b | as 3a, with the certain rule `gull(X) :- seabird(X), yellow_bill(X)` |
| 4 | stages 2, 3a and 3b with `bird(tweety)` replaced by a register entry and two lineage rules |

## Where the inputs come from

The inputs were written for the paper. The file name says which system reads the file:

```text
inputs/stage1/  gk.gkp  problog.pl  plingo.plp  pasta.lp
inputs/stage2/  gk.gkp  plingo.plp  pasta.lp  smproblog.pl
inputs/stage3a/ gk.gkp  pasta.lp
inputs/stage3b/ gk.gkp  plingo.plp  pasta.lp  smproblog.pl
inputs/stage4/  gk_stage2.gkp  gk_stage3a.gkp  gk_stage3b.gkp
                mcref_ground_stage2.gkp  mcref_ground_stage3a.gkp  mcref_ground_stage3b.gkp
                problog_analogue.pl  plingo_analogue.plp  clingo_skeleton.lp
                pasta_stage2.lp  pasta_stage3b.lp  smproblog_stage2.pl  smproblog_stage3b.pl
inputs/stage4/one_rule/  inputs with one lineage rule only, for gk, the tool, ProbLog and PASTA
inputs/stage4/scasp/     l_both.pl  l_down.pl  l_up.pl  stage4_s2.pl  stage4_s3b.pl, for s(CASP)
inputs/stage4/scasp/controls/  the control inputs for s(CASP)
scasp_outputs/           the standard output (.out) and the standard error (.err) of every run of s(CASP)
```

The stage-4 inputs have function terms. The tool declines function terms; the files `mcref_ground_*.gkp` are
ground abstractions for it, which gk 1.3.2 and the tool did not run.

## Rerun

From the folder `paper2026/`:

```sh
cd O1_tweety/inputs/stage3a && $GK gk.gkp
```

The first output line holds the field `"value":[0.6984,0.224,0,0.0776]`: the four shares (for, against,
conflict, ignorance) of stage 3a. The line names the exact method as the one that answered
(`"answer_from":"the exhaustive search"`) and marks the answer complete. To rerun every gk and tool run of this
part and compare each value with `results.csv`:

```sh
python3 check_gk.py --part O1_tweety --gk PATH/TO/gk --mcref PATH/TO/mcref.py
```

It takes about three minutes. The lineage runs of the default and the general method use their whole time
limit. Their value can change from run to run; the check reports such a difference apart. The table below gives
the runs and the values that the check compares:

<!-- table check -->
| gk runs | tool runs | runs with a recorded value | values compared | of these, on runs that did not end by themselves |
|---|---|---|---|---|
| 27 | 4 | 31 | 31 | 15 |
<!-- end table -->

`$GK` stands for the gk binary and `$MCREF` for the tool's `mcref.py`. Every command of `runs.tsv` runs
in the folder that its column `cwd` names, relative to this folder's parent (`paper2026/`).

## Results

The stages under the three methods of gk and the tool, at the time limit of 10 s. "Limit" in place of a time
means that the run did not end by itself; it then has no time.

<!-- table stages -->
| stage | calculated value | the default | the exact method | the general method | the tool |
|---|---|---|---|---|---|
| 1 | (.396, .56, 0, .044) | (.396, .56, 0, .044), complete, by the exact method, 0.06 s | (.396, .56, 0, .044), complete, 0.05 s | (.396, .56, 0, .044), 0.28 s | (.396, .56, 0, .044), exact value of the tool; equal |
| 2 | (.396, .56, 0, .044) | (.396, .56, 0, .044), complete, by the exact method, 0.05 s | (.396, .56, 0, .044), complete, 0.05 s | (.396, .56, 0, .044), 0.33 s | (.396, .56, 0, .044), exact value of the tool; equal |
| 3a | (.6984, .224, 0, .0776) | (.6984, .224, 0, .0776), complete, by the exact method, 0.05 s | (.6984, .224, 0, .0776), complete, 0.06 s | (.6984, .224, 0, .0776), 0.43 s | (.6984, .224, 0, .0776), exact value of the tool; equal |
| 3b | (.6984, .224, 0, .0776) | (.6984, .224, 0, .0776), complete, by the exact method, 0.05 s | (.6984, .224, 0, .0776), complete, 0.05 s | (.6984, .224, 0, .0776), 0.51 s | (.6984, .224, 0, .0776), exact value of the tool; equal |
| 4, from stage 2 | (.396, .56, 0, .044) | (.396, .56, 0, .044), by the general method, limit | (.396, .56, 0, .044), not complete, limit | (.396, .56, 0, .044), limit | not run |
| 4, from stage 3a | (.6984, .224, 0, .0776) | (.6984, .224, 0, .0776), by the general method, limit | (.6984, .224, 0, .0776), not complete, limit | (.6984, .224, 0, .0776), limit | not run |
| 4, from stage 3b | (.6984, .224, 0, .0776) | (.6984, .224, 0, .0776), by the general method, limit | (.6984, .224, 0, .0776), not complete, limit | (.6984, .224, 0, .0776), limit | not run |
<!-- end table -->

The lineage stages under the default at three time limits:

<!-- table lineage -->
| input | limit | value of the default | against the calculated value | ended by itself | first limit |
|---|---|---|---|---|---|
| gk_stage2.gkp | 2 s | (.396, .56, 0, .044) | equal | no | searches stopped: 5 cut, 0 queued |
| gk_stage2.gkp | 10 s | (.396, .56, 0, .044) | equal | no | searches stopped: 4 cut, 0 queued |
| gk_stage2.gkp | 60 s | (.396, .56, 0, .044) | equal | no | searches stopped: 4 cut, 0 queued |
| gk_stage3a.gkp | 2 s | (.6984, .224, 0, .0776) | equal | no | searches stopped: 5 cut, 1 queued |
| gk_stage3a.gkp | 10 s | (.6984, .224, 0, .0776) | equal | no | searches stopped: 4 cut, 0 queued |
| gk_stage3a.gkp | 60 s | (.6984, .224, 0, .0776) | equal | no | searches stopped: 4 cut, 0 queued |
| gk_stage3b.gkp | 2 s | (.6984, .224, 0, .0776) | equal | no | searches stopped: 5 cut, 3 queued |
| gk_stage3b.gkp | 10 s | (.6984, .224, 0, .0776) | equal | no | searches stopped: 4 cut, 0 queued |
| gk_stage3b.gkp | 60 s | (.6984, .224, 0, .0776) | equal | no | searches stopped: 4 cut, 0 queued |
<!-- end table -->

The other systems, from the recorded runs. The outcomes are those of the comparison: same value, another
quantity, no answer, did not end, no encoding, not run.

<!-- table others -->
| stage | system | outcome | what the system printed | relation of the encoding |
|---|---|---|---|---|
| stage1 | ProbLog 2.3.0 | same value | .396 | exact translation |
| stage1 | plingo 1.1.0 | same value | .39600 | exact translation |
| stage1 | PASTA 1.0.1 | same value | [.396, .396] | exact translation |
| stage1 | smProbLog 2.1.0.42 | not run | - | - |
| stage2 | ProbLog 2.3.0 | no encoding | - | no faithful encoding claimed |
| stage2 | plingo 1.1.0 | another quantity | .31936 | non-equivalent analogue |
| stage2 | PASTA 1.0.1 | another quantity | [.18, .396] | non-equivalent analogue |
| stage2 | smProbLog 2.1.0.42 | no answer | - | non-equivalent analogue |
| stage3a | ProbLog 2.3.0 | no encoding | - | no faithful encoding claimed |
| stage3a | plingo 1.1.0 | not run | - | - |
| stage3a | PASTA 1.0.1 | another quantity | [.425229, .567661] | non-equivalent analogue |
| stage3a | smProbLog 2.1.0.42 | not run | - | - |
| stage3b | ProbLog 2.3.0 | no encoding | - | no faithful encoding claimed |
| stage3b | plingo 1.1.0 | another quantity | .52105 | non-equivalent analogue |
| stage3b | PASTA 1.0.1 | another quantity | [.466265, .596386] | non-equivalent analogue |
| stage3b | smProbLog 2.1.0.42 | another quantity | (.5313, .1327, .336) | non-equivalent analogue |
| stage4 | ProbLog 2.3.0 | did not end | - | grounding test |
| stage4 | plingo 1.1.0 | did not end | - | grounding test |
| stage4 | clingo 5.8.3 | did not end | - | grounding test |
| stage4 | PASTA 1.0.1 | did not end | - | non-equivalent analogue |
| stage4 | PASTA 1.0.1 | did not end | - | non-equivalent analogue |
| stage4 | smProbLog 2.1.0.42 | no answer | - | outside the stated language |
| stage4 | smProbLog 2.1.0.42 | no answer | - | outside the stated language |
| stage4 | ProbLog 2.3.0 | same value | .396 | grounding test |
| stage4 | PASTA 1.0.1 | another quantity | [.18, .396] | non-equivalent analogue |
| stage4 | ProbLog 2.3.0 | did not end | - | grounding test |
<!-- end table -->

### s(CASP) on stage 4

s(CASP) 1.1.4 searches from the question and returns a verdict with a model, no number. It ran on crisp
counterparts of stage 4 (`inputs/stage4/scasp/`): every confidence is dropped, and the disjunction is written as
two rules with negation as failure. `l_both.pl`, `l_down.pl` and `l_up.pl` hold the register fact and the lineage
rules alone. `stage4_s2.pl` is the counterpart of the disjunction stage, `stage4_s3b.pl` the one with the certain
gull rule. The controls (`controls/`) change one thing each: the order of the register fact and the lineage rules,
or `bird(tweety)` as a fact in place of the lineage. After a model, s(CASP) waits at its answer prompt while its
input stays open; three controls ran again with input from /dev/null. The run of `not flies(tweety)` on
`stage4_s2.pl` printed every model (`-n 0`). Column `raw` of `runs.tsv` names each run's output in
`scasp_outputs/`.

<!-- table scasp -->
| run | input | question | encoding | limits | outcome | time |
|---|---|---|---|---|---|---|
| short | l_both.pl | bird(tweety) | the register fact and both lineage rules | 120 s, 2 GB | a model | 0.07 s |
| short | l_down.pl | bird(tweety) | the register fact and the rule towards the child | 120 s, 2 GB | a model | 0.08 s |
| short | l_up.pl | bird(tweety) | the register fact and the rule towards the parent | 120 s, 2 GB | no model | 0.08 s |
| short | stage4_s2.pl | not flies(tweety) | the crisp counterpart of the disjunction stage | 120 s, 2 GB | a model | not recorded |
| short | stage4_s2.pl | flies(tweety) | the crisp counterpart of the disjunction stage | 120 s, 2 GB | did not end | limit |
| short | stage4_s3b.pl | flies(tweety) | the crisp counterpart with the certain gull rule | 120 s, 2 GB | did not end | limit |
| short | stage4_s3b.pl | not flies(tweety) | the crisp counterpart with the certain gull rule | 120 s, 2 GB | did not end | limit |
| one hour | stage4_s2.pl | flies(tweety) | the crisp counterpart of the disjunction stage | 3600 s, 16 GB | did not end | limit |
| one hour | stage4_s3b.pl | flies(tweety) | the crisp counterpart with the certain gull rule | 3600 s, 16 GB | did not end | limit |
| one hour | stage4_s3b.pl | not flies(tweety) | the crisp counterpart with the certain gull rule | 3600 s, 16 GB | did not end | limit |
| control | controls/clingo_skeleton_scasp.pl | flies(tweety) | the content of the clingo skeleton, the register fact after the lineage rules | 60 s, 2 GB | did not end | limit |
| control | controls/clingo_skeleton_scasp.pl | flies(tweety) | the content of the clingo skeleton, the register fact after the lineage rules; input from /dev/null | 60 s, 2 GB | did not end | limit |
| control | controls/clingo_skeleton_scasp_factfirst.pl | flies(tweety) | the content of the clingo skeleton, the register fact first | 60 s, 2 GB | a model, then the answer prompt until the time limit | limit |
| control | controls/clingo_skeleton_scasp_factfirst.pl | flies(tweety) | the content of the clingo skeleton, the register fact first; input from /dev/null | 60 s, 2 GB | a model | 0.08 s |
| control | controls/clingo_skeleton_scasp_nolineage.pl | flies(tweety) | the content of the clingo skeleton, bird(tweety) as a fact in place of the lineage | 60 s, 2 GB | a model | 0.05 s |
| control | controls/l_both_factlast.pl | bird(tweety) | l_both.pl with the register fact after the lineage rules | 60 s, 2 GB | did not end | limit |
| control | controls/l_both_factlast.pl | bird(tweety) | l_both.pl with the register fact after the lineage rules; input from /dev/null | 60 s, 2 GB | did not end | limit |
| control | controls/s2_nolineage.pl | flies(tweety) | stage4_s2.pl with bird(tweety) as a fact in place of the lineage | 60 s, 2 GB | no model | 0.06 s |
| control | controls/s2_nolineage.pl | not flies(tweety) | stage4_s2.pl with bird(tweety) as a fact in place of the lineage | 60 s, 2 GB | a model | 0.05 s |
| control | controls/s3b_nolineage.pl | flies(tweety) | stage4_s3b.pl with bird(tweety) as a fact in place of the lineage | 60 s, 2 GB | no model | 0.06 s |
| control | controls/s3b_nolineage.pl | not flies(tweety) | stage4_s3b.pl with bird(tweety) as a fact in place of the lineage | 60 s, 2 GB | no model | 0.06 s |
<!-- end table -->

## Where the paper's numbers are

- The Tweety tables of Sections 2 and 7.2: `results.csv`, the rows of the stage with `system` gk 1.3.2, `method` default
  and `limit_s` 10, column `value`; the method that answered is in `answered_by`.
- "about .1 s, each marked complete": the same rows, columns `complete` and `time_s`.
- "the lineage stages go to the general method": the rows of `stage4_2`, `stage4_3a` and `stage4_3b`. These
  runs did not end by themselves (searches stopped at the time limit), so `time_s` is empty.
- The cells of the other systems: the rows whose `system` is another system, columns `outcome`, `value` and
  `note`.
- s(CASP) on stage 4 (Sections 2.4 and 7.2): the rows whose `system` is s(CASP) 1.1.4, columns `outcome`,
  `time_s` and `note`; the dependence on the order of the clauses: the controls with the register fact first and
  after the lineage rules.

`results.csv` has one row per run and answer. The columns are described on the first page of the
folder ([`../README.md`](../README.md), section "The tables of a part").
