# O1: the worked example (Tweety)

This part reproduces the Tweety table and the values of Section 2 of the paper, and
the reference tool's estimates quoted in Section 5. The question in every
stage is whether Tweety flies, `flies(tweety)`.

| stage | paper | what the stage adds |
|---|---|---|
| 1 | Section 2.1 | an uncertain exception: a ranked penguin default against the flying default |
| 2 | Section 2.2 | the .7 penguin rule replaced by `gull(X) ; penguin(X) :- seabird(X)` and `0.7::-gull(tweety)` |
| 3a | Section 2.3 | stage 2 plus `0.9::gull(X) :- seabird(X), yellow_bill(X)` and `0.6::yellow_bill(tweety)` |
| 3b | Section 2.3 | as 3a, with the certain rule `gull(X) :- seabird(X), yellow_bill(X)` |
| 4 | Section 2.4 | stages 2, 3a and 3b with `bird(tweety)` replaced by a register entry and two lineage rules |

## Files

Each stage has a folder. The file name says which system reads the file.

```text
O1_tweety/
  results.tsv          every result of this part, one row each
  stage1/  gk.gkp  problog.pl  plingo.plp  pasta.lp
  stage2/  gk.gkp  plingo.plp  pasta.lp  smproblog.pl
  stage3a/ gk.gkp  pasta.lp
  stage3b/ gk.gkp  plingo.plp  pasta.lp  smproblog.pl
  stage4/  gk_stage2.gkp  gk_stage3a.gkp  gk_stage3b.gkp
           mcref_ground_stage2.gkp  mcref_ground_stage3a.gkp  mcref_ground_stage3b.gkp
           problog_analogue.pl  plingo_analogue.plp  clingo_skeleton.lp
           pasta_stage2.lp  pasta_stage3b.lp  smproblog_stage2.pl  smproblog_stage3b.pl
           one_rule/  gk_parent_rule.gkp  mcref_ground_parent_rule.gkp  problog_parent_rule.pl
                      gk_child_rule.gkp   mcref_ground_child_rule.gkp   problog_child_rule.pl
                      pasta_child_rule.lp
  runs.tsv             every run of gk, of mcref, and of the external systems run again
```

The `gk.gkp` files are the gk inputs. mcref reads the same files. It
declines function terms, so for stage 4 it reads the ground abstractions
`mcref_ground_*.gkp`. These name the three ancestors `p1`, `gp` and `ggp`
and write out the lineage rules for them. The one-rule inputs have their
own ground abstractions in `stage4/one_rule/`.

## Rerun gk and the reference tool

From the repository root:

```sh
./bin/gk paper2026/O1_tweety/stage1/gk.gkp
python3 mcref/mcref.py paper2026/O1_tweety/stage1/gk.gkp --samples 20000 --seed 1
```

gk prints the line `{"recursive": ...}` first. Its field `value` holds the
four shares (for, against, conflict, ignorance). mcref prints one JSON
object; the field `answers[0].value` holds its four estimates. With seed 1
mcref prints exactly the values below.

To rerun every gk and mcref row of this part and compare it with
`results.tsv`:

```sh
python3 paper2026/check_gk.py --part O1 --mcref
```

This reruns 11 gk runs and 10 mcref runs and takes about 1.5 minutes. The
five lineage runs at the default deadline take about 7 s each, because
lineage searches run until gk's budget stops them: four on each stage-4
input, two on the parent-rule input and one on the child-rule input. The
run with `-seconds 30` takes about 20 s.

## Rerun the other systems

[`../SYSTEMS.md`](../SYSTEMS.md) says how to install each system. The
commands, from the folder `paper2026/O1_tweety`:

```sh
problog stage1/problog.pl
plingo --frontend=problog stage1/plingo.plp 0
pastasolver stage1/pasta.lp --query="flies(tweety)"
pastasolver stage3b/pasta.lp --query="flies(tweety)" --normalize
pypy3 ../tools/run_smproblog.py -k ddnnf stage2/smproblog.pl
python3 ../tools/enumerate_answer_sets.py stage3b/pasta.lp "flies(tweety)" "nflies(tweety)"
```

The last command computes the values of the published semantics of PASTA
and smProbLog by enumeration with clingo. It gives the smProbLog values
of the Tweety table, because the tested smProbLog executable failed on these inputs
(see "Failures of the external executables" below).

In the answer set encodings the atom `nflies(tweety)` stands for the
explicit negation `-flies(tweety)`.

## Results

Times are wall-clock times of single runs on one machine. The kinds of
result:

- *run*: the system printed the value on the named file;
- *enumerated*: `tools/enumerate_answer_sets.py` computed the value of
  the system's published semantics; no run of the system printed it;
- *estimate*: mcref sampled 20,000 worlds with seed 1. Each share then
  lies within .0113 of the exact value with 95 % confidence.

The relation of an external encoding to the gk input:

- *exact translation*: the encoding states the same knowledge, for this
  input only;
- *non-equivalent analogue*: the encoding states a nearby program in the
  system's own language; its value is a different quantity;
- *grounding test*: the encoding replaces `0.7::-gull(tweety)` by the
  positive switch `0.3::gull(tweety)`; it tests whether the system answers
  with both lineage rules, and its number is no matched comparison.

### Stage 1: an uncertain exception

| system | file | relation | result |
|---|---|---|---|
| gk | `stage1/gk.gkp` | | (.396, .56, 0, .044), .3 s |
| ProbLog | `stage1/problog.pl` | exact translation | .396 |
| plingo | `stage1/plingo.plp` | exact translation | .39600 |
| PASTA | `stage1/pasta.lp` | exact translation | [.396, .396] |
| smProbLog | | not run | |
| mcref | `stage1/gk.gkp` | | (.3994, .55575, 0, .04485) |

The PASTA run of stage 1 of 2026-11-08 left no output file. It was run
again on 2026-11-10 through the run store with PASTA 1.0.1, once for
`flies(tweety)` and once for `nflies(tweety)`; it printed equal lower and
upper probabilities, .396 and .56.

The ProbLog encoding replaces the ranked defaults by `\+ penguin(X)` in the
flying rule. This is exact here because nothing opposes `penguin`, so the
rank-3 penguin default wins wherever `penguin` holds.

### Stage 2: a disjunction

| system | file | relation | result |
|---|---|---|---|
| gk | `stage2/gk.gkp` | | (.396, .56, 0, .044), .4 s |
| ProbLog | | no faithful encoding claimed | |
| plingo | `stage2/plingo.plp` | non-equivalent analogue | .31936 |
| PASTA | `stage2/pasta.lp` | non-equivalent analogue | [.18, .396] |
| smProbLog | `stage2/smproblog.pl` | non-equivalent analogue | (.288, .712, 0), enumerated |
| mcref | `stage2/gk.gkp` | | (.40115, .5567, 0, .04215) |

In the analogues the report against gull is the probabilistic atom
`ngull_ev`, and a constraint removes the answer sets where `gull` holds
with it. The share .24 of the choices has two answer sets, one with a gull
and one with a penguin. plingo weights every answer set and normalizes:
.31936 = .396/1.24. smProbLog divides the mass of a choice equally among its
answer sets: .288 = .18 + .216/2. PASTA leaves the allocation open.

### Stage 3a: the gull rule at .9

| system | file | relation | result |
|---|---|---|---|
| gk | `stage3a/gk.gkp` | | (.6984, .224, 0, .0776), .4 s |
| ProbLog | | no faithful encoding claimed | |
| plingo | | not run | |
| PASTA | `stage3a/pasta.lp` | non-equivalent analogue | with `--normalize`: [.425229, .567661] |
| smProbLog | | not run | |
| mcref | `stage3a/gk.gkp` | | (.6963, .22515, 0, .07855) |

The PASTA analogue switches the gull rule on by an independent fact
`0.9::sw_gull_yb(tweety)`. The mass .8 × .7 × .6 × .9 = .3024 then has no
answer set. Without `--normalize` PASTA stops with
`Error: Found 2 worlds without answer sets.`

### Stage 3b: the certain gull rule

| system | file | relation | result |
|---|---|---|---|
| gk | `stage3b/gk.gkp` | | (.6984, .224, 0, .0776), two cycle-cut notes, .5 s |
| ProbLog | | no faithful encoding claimed | |
| plingo | `stage3b/plingo.plp` | non-equivalent analogue | .52105 |
| PASTA | `stage3b/pasta.lp` | non-equivalent analogue | with `--normalize`: [.466265, .596386] |
| smProbLog | `stage3b/smproblog.pl` | non-equivalent analogue | (.3528, .3112, .336), enumerated |
| mcref | `stage3b/gk.gkp` | | (.6963, .22515, 0, .07855) |

The mass .8 × .7 × .6 = .336 has no answer set. plingo normalizes over the
rest: .52105 = .396/.76. smProbLog keeps .336 as inconsistent mass. gk
prints the two approximation notes in the field `readings` of its line; Section 6.5
of the paper explains the cycle cut.

### Stage 4: the lineage

| system | file | relation | result |
|---|---|---|---|
| gk | `stage4/gk_stage2.gkp` | | (.396, .56, 0, .044), 6.8 s, four searches stopped |
| gk | `stage4/gk_stage3a.gkp` | | (.6984, .224, 0, .0776), 6.8 s, four searches stopped |
| gk | `stage4/gk_stage3b.gkp` | | (.6984, .224, 0, .0776), 6.8 s, four searches stopped, two cycle-cut notes |
| gk | `stage4/gk_stage2.gkp`, `-seconds 30` | | (.396, .56, 0, .044), 20.4 s, the same four searches stopped |
| gk | `stage4/gk_stage3b.gkp`, `-seconds 1` | | (.6984, .224, 0, .0776), 691 ms of the budget used, four searches stopped, one cycle-cut note |
| ProbLog | `stage4/problog_analogue.pl` | grounding test | no answer at 60 s |
| plingo | `stage4/plingo_analogue.plp` | grounding test | grounding stopped at 10 s, no model |
| clingo | `stage4/clingo_skeleton.lp` | grounding test | grounding not finished at 10 s, peak memory 1.0 GB |
| PASTA | `stage4/pasta_stage2.lp`, `stage4/pasta_stage3b.lp` | non-equivalent analogue | no answer at 60 s |
| smProbLog | `stage4/smproblog_stage2.pl`, `stage4/smproblog_stage3b.pl` | outside the stated language | the bundled gringo failed with `std::bad_alloc` after 54 s under an 8 GB limit |
| mcref | `stage4/gk_stage2.gkp` | | declines function terms |
| mcref | `stage4/mcref_ground_stage2.gkp` | ground abstraction | (.4008, .5559, 0, .0433) |
| mcref | `stage4/mcref_ground_stage3a.gkp` | ground abstraction | (.6990, .2229, 0, .0781) |
| mcref | `stage4/mcref_ground_stage3b.gkp` | ground abstraction | (.6990, .2229, 0, .0781) |

The four stopped searches are three searches for evidence against
`bird(tweety)`, `bird(parent(tweety))` and `bird(parent(parent(tweety)))`,
and one search for further proofs of the register entry. Section 2.4 of
the paper explains why they cannot change the value. With a deadline of
30 s gk cuts the same four searches and returns the same value; with a
deadline of 1 s it returns the same value with one cycle-cut note in
place of two.

The ProbLog and clingo rows of stage 4 come from runs of 2026-11-10. The
runs of 2026-11-04 on the same files left empty output files and only a
note of the outcome, so the files were run again through the run store,
with ProbLog 2.3.0 and clingo 5.8.3 and the same limits: ProbLog printed
nothing in 60 s, and clingo printed its banner and nothing more in 10 s.
The clingo command is `clingo stage4/clingo_skeleton.lp 0`; the command of
2026-11-04 was not recorded.

Each lineage rule alone leaves one grounding order finite:

| input | system | result |
|---|---|---|
| `stage4/one_rule/gk_parent_rule.gkp`, only `bird(parent(X)) :- bird(X)` | gk | (.396, .56, 0, .044), two searches stopped |
| `stage4/one_rule/mcref_ground_parent_rule.gkp`, its ground abstraction | mcref | (.39835, .5584, 0, .04325) |
| `stage4/one_rule/problog_parent_rule.pl`, its ProbLog grounding test | ProbLog | .396 |
| `stage4/one_rule/gk_child_rule.gkp`, only `bird(X) :- bird(parent(X))` | gk | (.396, .56, 0, .044), one search stopped |
| `stage4/one_rule/mcref_ground_child_rule.gkp`, its ground abstraction | mcref | (.39745, .55975, 0, .0428) |
| `stage4/one_rule/problog_child_rule.pl`, its ProbLog grounding test | ProbLog | no answer at 60 s (run of 2026-11-10) |
| `stage4/one_rule/pasta_child_rule.lp`, its PASTA analogue | PASTA | [.18, .396] |

## Failures of the external executables

- smProbLog 2.1.0.42 does not install under Python 3.12 or later, because
  it imports the removed module `imp`. It ran under PyPy 3.11 with
  `tools/run_smproblog.py`, which restores three removed names and leaves
  smProbLog's code unchanged.
- On `stage2/smproblog.pl` smProbLog's bundled compiler
  `dsharp_with_unfounded` ended with signal 11, and smProbLog reported
  `DSharpError`.
- On `stage3b/smproblog.pl` smProbLog printed (.5313, .1327, .336). It
  divides the true mass by the consistent mass and prints false as the
  remainder. The published semantics gives (.3528, .3112, .336), the value
  in the table.
- PASTA stops with `Error: Found 2 worlds without answer sets.` on stages
  3a and 3b unless it runs with `--normalize`.

## The snapshots of the snapshot table

The snapshot table of the paper (Section 6.2) shows the values of three snapshots of
stage 3a. Part O11 reproduces them from gk's checkpoint dumps of
`stage3a/gk.gkp` (row `t4.stage3a.checkpoints`).

## The printed proof of stage 3a

The printed proof of the paper is gk's default output on
`stage3a/gk.gkp` (run `s3a.gk`) in text form. gk prints its line
`{"recursive": ...}` as JSON; the field `proof` holds the proofs for and
against (`Doc/recursive_output.md`, Section 3.1 "The proofs"). The text
form is that of the web page `commonsense.html`, printed by `gkproofs.js`
of the logictools repository (github.com/tammet/logictools); gkreasoner
does not include it. The lines below are wrapped at 78 columns.

```sh
cd paper2026/O1_tweety/stage3a
../../../bin/gk gk.gkp                 # run s3a.gk
../../../bin/gk gk.gkp -fullproof      # run s3a.gk.fullproof
```

```text
answer flies(tweety), signed confidence 0.4744
  value: for 0.6984, against 0.224, conflict 0, ignorance 0.0776
  for #1, proof of flies(tweety), confidence 0.9:
    1. in(frm_2) 0.9:       flies(X) :- bird(X), unless(-flies(X), 2)
    2. goal(frm_9) 1:       -flies(tweety)
    3. mp(1.2, 2) 0.9:      -bird(tweety) :- unless(-flies(tweety), 2)
    4. in(frm_1) 1:         bird(tweety)
    5. mp(3, 4) 0.9:        :- unless(-flies(tweety), 2)
  against #1, proof of -flies(tweety), confidence 0.56:
    1. in(frm_3) 1:         -flies(X) :- penguin(X), unless(flies(X), 3)
    2. goal(task) 1:        flies(tweety)
    3. mp(1.2, 2) 1:        -penguin(tweety) :- unless(flies(tweety), 3)
    4. in(frm_4) 1:         gull(X) ; penguin(X) :- seabird(X)
    5. mp(3, 4.2) 1:        gull(tweety) :- seabird(tweety),
                            unless(flies(tweety), 3)
    6. in(frm_5) 0.8:       seabird(tweety)
    7. mp(5, 6) 0.8:        gull(tweety) :- unless(flies(tweety), 3)
    8. in(frm_6) 0.7:       -gull(tweety)
    9. mp(7.1, 8) 0.56:     :- unless(flies(tweety), 3)
```

The proof against has the confidence .56, and the share against is .224.
The default output holds no proof of `gull(tweety)`, under no name: it has
no list `guards`, and its proofs have no subproofs. With `-fullproof` the
proof against gets the subproofs of its nested searches. The proof of
`gull(tweety)`, confidence .432, which opposes the premise
`-gull(tweety)`, stands under step 1 of the proof against, inside the
subproof of `penguin(tweety)`, under that proof's step 1 (lines left out
are marked `...`):

```text
against #1, proof of -flies(tweety), confidence 0.56:
  1. in(frm_3) 1:         -flies(X) :- penguin(X), unless(flies(X), 3)
    proof of penguin(tweety), confidence 0.56 (no input instance beyond the
        proof above):
      1. in(frm_4) 1:         gull(X) ; penguin(X) :- seabird(X)
        ...  (the proof of seabird(tweety), 0.8)
        proof of gull(tweety), confidence 0.432:
          1. in(frm_7) 0.9:       gull(X) :- yellow_bill(X), seabird(X)
            proof of -gull(tweety), confidence 0.7:
              ...  (3 steps)
            proof of yellow_bill(tweety), confidence 0.6 (no input instance
                beyond the proof above):
              ...  (3 steps)
          2. goal(task) 1:        -gull(tweety)
          3. mp(1.2, 2) 0.9:      -seabird(tweety) :- yellow_bill(tweety)
          4. in(frm_5) 0.8:       seabird(tweety)
          5. mp(3, 4) 0.72:       -yellow_bill(tweety)
          6. in(frm_8) 0.6:       yellow_bill(tweety)
          7. mp(5, 6) 0.432:      false
      ...  (steps 2 to 7 of the proof of penguin(tweety))
  ...  (steps 2 to 7)
  8. in(frm_6) 0.7:       -gull(tweety)
  9. mp(7.1, 8) 0.56:     :- unless(flies(tweety), 3)
```

## Versions

Every gk and mcref value and time of this part comes from a run of
gk 1.2.5 and mcref 1.1.2 on 2026-11-10. The earlier runs of the paper's
drafts used gk 1.2.3 and mcref 1.1.0 and gave the same values; the times
of stage 3b (.4 s), of the run with `-seconds 30` (20.3 s) and of the run
with `-seconds 1` (677 ms of the budget) were slightly lower. The external
systems ran on 2026-11-04 and 2026-11-08 with the versions in
`results.tsv`, apart from the three reruns of stage 4 named above. The
comment lines of the gk, ProbLog, plingo and clingo files were rewritten
for this folder; their clauses are the ones that were run.
