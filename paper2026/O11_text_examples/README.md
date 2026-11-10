# O11: the small examples of the text

This part holds the small examples that the paper states as clauses in
Sections 1 and 4 to 6 and in Appendix A. The paper prints them as text
only. Here each question has its own input file in `inputs/`, with the
clauses of the paper only, and gk 1.2.5 and the reference tool mcref
1.1.2 ran on every file. The Tweety stages of Section 2 and the five
inputs of Section 7.3 are in parts O1 and O4.

The column "value in the paper" holds the value of the semantics as the
paper states it. Where the paper states a value in words ("no support and
complete ignorance", "derives -bird(t)") the column gives the four shares
that the words mean. Where the paper states gk's own value, which differs
from the semantics, the column gives both.

## Rerun

From the repository root:

```sh
./bin/gk paper2026/O11_text_examples/inputs/a2_5_selection_p.gkp
python3 mcref/mcref.py paper2026/O11_text_examples/inputs/a2_5_selection_p.gkp --samples 100000 --seed 1
python3 paper2026/check_gk.py --part O11 --mcref
```

The column "check" says whether gk prints the paper's value at its printed
precision and whether each estimate of mcref lies within .0050 of it, the
half-width for 100,000 worlds (Section 5 of the paper).

## Results

mcref's estimate lies within .0050 of the value in the paper on 18 of 18
questions. gk prints that value on 16 of 19 questions; on the other 3 gk
records the approximation note `cycle cut` on 3, and its value differs. The cycle cut
is the approximation of Section 6.5 of the paper; the paper prints no gk
value for these questions.

| input | question | value in the paper | gk 1.2.5 | gk's approximation notes | mcref 1.1.2, 100,000 worlds | check |
|---|---|---|---|---|---|---|
| `inputs/s1_bird_conflict.gkp` | `flies(a)` | (0, 0, 0, 1) (the paper: no support and complete ignorance) | (0, 0, 0, 1) | none | (0, 0, 0, 1) | gk equals it; mcref within .0050 |
| `inputs/s4_1_penguin.gkp` | `penguin(tweety)` | .56 (the paper prints the share .56 of the worlds) | (.56, 0, 0, .44) | none | (.55832, 0, 0, .44168) | gk equals it; mcref within .0050 |
| `inputs/s4_2_certain_rule_bird.gkp` | `bird(t)` | (0, 1, 0, 0) (the paper: derives -bird(t)) | (0, 1, 0, 0) | none | (0, 1, 0, 0) | gk equals it; mcref within .0050 |
| `inputs/s4_2_rule_099_bird.gkp` | `bird(t)` | (0, 0, 0, 1) (the paper: does not derive -bird(t)) | (0, 0, 0, 1) | none | (0, 0, 0, 1) | gk equals it; mcref within .0050 |
| `inputs/s4_2_rule_08_bird.gkp` | `bird(t)` | (0, 0, 0, 1) (the paper: nothing follows about its being a bird) | (0, 0, 0, 1) | none | (0, 0, 0, 1) | gk equals it; mcref within .0050 |
| `inputs/s5_case_split_q.gkp` | `q` | (0, 0, 0, 1); gk: (1, 0, 0, 0) (the paper: q is in ignorance in the semantics, and gk's prover derives q) | (1, 0, 0, 0) | none | (0, 0, 0, 1) | gk equals it; mcref within .0050 |
| `inputs/s6_1_combined_b.gkp` | `b` | not printed; gk: .42 (the paper: resolution derives b with support .6 x .7 = .42; the semantics has no such application) | (.42, 0, 0, .58) | none | (0, 0, 0, 1) | gk equals it |
| `inputs/s6_4_shared_premise_q.gkp` | `q` | (.5, 0, 0, .5) (support .5, not .5 x .5) | (.5, 0, 0, .5) | none | (.4995, 0, 0, .5005) | gk equals it; mcref within .0050 |
| `inputs/a2_1_one_sign_a.gkp` | `a` | (.5, 0, 0, .5) (the paper: a and b positive in .5 of the worlds) | (.5, 0, 0, .5) | none | (.49856, 0, 0, .50144) | gk equals it; mcref within .0050 |
| `inputs/a2_1_one_sign_b.gkp` | `b` | (.5, 0, 0, .5) | (.5, 0, 0, .5) | none | (.49856, 0, 0, .50144) | gk equals it; mcref within .0050 |
| `inputs/a2_1_exception_cycle_p.gkp` | `p` | (0, 0, 0, 1) | (1, 0, 0, 0) | cycle cut x3 | (0, 0, 0, 1) | gk differs from the target; mcref within .0050 |
| `inputs/a2_1_exception_cycle_q.gkp` | `q` | (0, 0, 0, 1) | (1, 0, 0, 0) | cycle cut x3 | (0, 0, 0, 1) | gk differs from the target; mcref within .0050 |
| `inputs/a2_1_exception_cycle_r.gkp` | `r` | (0, 0, 0, 1) | (1, 0, 0, 0) | cycle cut x3 | (0, 0, 0, 1) | gk differs from the target; mcref within .0050 |
| `inputs/a2_5_selection_p.gkp` | `p` | (.64, .04, .16, .16) | (.64, .04, .16, .16) | cycle cut | (.63884, .04061, .15991, .16064) | gk equals it; mcref within .0050 |
| `inputs/a2_5_selection_r.gkp` | `r` | (.64, .04, .16, .16) | (.64, .04, .16, .16) | cycle cut | (.63884, .04061, .15991, .16064) | gk equals it; mcref within .0050 |
| `inputs/s4_3_default_vs_fact.gkp` | `flies(t)` | (.63, .3, 0, .07) (the input of Examples/semantics/default_vs_fact.gkp) | (.63, .3, 0, .07) | none | (.63, .3, 0, .07) | gk equals it; mcref within .0050 |
| `inputs/s4_3_rule_vs_fact.gkp` | `flies(t)` | (.6, 0, .3, .1) (the input of Examples/semantics/rule_vs_fact.gkp) | (.6, 0, .3, .1) | none | (.6, 0, .3, .1) | gk equals it; mcref within .0050 |
| `inputs/s4_3_nixon.gkp` | `pacifist(n)` | (0, 0, 0, 1) (the input of Examples/semantics/nixon.gkp) | (0, 0, 0, 1) | none | (0, 0, 0, 1) | gk equals it; mcref within .0050 |
| `inputs/s4_3_nixon_uncertain.gkp` | `pacifist(n)` | (.32, .12, 0, .56) (the input of Examples/semantics/nixon_uncertain.gkp) | (.32, .12, 0, .56) | none | (.32, .12, 0, .56) | gk equals it; mcref within .0050 |

## The snapshot table of the paper: the snapshots of stage 3a

The snapshot table (Section 6.2) shows three snapshots of the evaluation of Tweety
stage 3a. gk writes a dump of its evidence at every checkpoint when it
runs with `-checkpoints DIR`:

```sh
mkdir cp
./bin/gk paper2026/O1_tweety/stage3a/gk.gkp -checkpoints cp
```

The field `value_c.value` of the dumps `cp/checkpoint_001_*.json` to
`cp/checkpoint_003_*.json` holds the three values of the snapshot table. The later
checkpoints repeat the third value.

| snapshot | value in the snapshot table | gk 1.2.5 |
|---|---|---|
| the bird proof and the flying default | (.9, 0, 0, .1) | (.9, 0, 0, .1) |
| with the penguin proof | (.396, .56, 0, .044) | (.396, .56, 0, .044) |
| with the yellow-bill proof | (.6984, .224, 0, .0776) | (.6984, .224, 0, .0776) |

In the folder's results the row is `t4.stage3a.checkpoints`; the run
writes the dumps into a folder of its own in the run store.

## Notes on the examples

- **Section 1** (`s1_bird_conflict.gkp`): the evidence about the premise
  `bird(a)` is in conflict; the conclusion gets no support and complete
  ignorance. The paper contrasts this with two other readings: .45 when
  the second clause is ignored, and .225 when the negated head blocks the
  atom.
- **Section 4.3** (`s4_3_*.gkp`, copies of four inputs of
  `Examples/semantics`): the design choices; ordinary evidence wins over a
  normal default, (.63, .3, 0, .07), and with an ordinary rule in place of
  the default (.6, 0, .3, .1); defaults of equal rank cancel, (0, 0, 0, 1),
  and (.32, .12, 0, .56) with confidences .8 and .6.
- **Section 4.3** (`s4_3_*.gkp`, copies of four inputs of
  `Examples/semantics`): the design choices; ordinary evidence wins over a
  normal default, (.63, .3, 0, .07), and with an ordinary rule in place of
  the default (.6, 0, .3, .1); defaults of equal rank cancel, (0, 0, 0, 1),
  and (.32, .12, 0, .56) with confidences .8 and .6.
- **Section 4.3** (`s4_3_*.gkp`, copies of four inputs of
  `Examples/semantics`): the design choices; ordinary evidence wins over a
  normal default, (.63, .3, 0, .07), and with an ordinary rule in place of
  the default (.6, 0, .3, .1); defaults of equal rank cancel, (0, 0, 0, 1),
  and (.32, .12, 0, .56) with confidences .8 and .6.
- **Section 4.3** (`s4_3_*.gkp`, copies of four inputs of
  `Examples/semantics`): the design choices; ordinary evidence wins over a
  normal default, (.63, .3, 0, .07), and with an ordinary rule in place of
  the default (.6, 0, .3, .1); defaults of equal rank cancel, (0, 0, 0, 1),
  and (.32, .12, 0, .56) with confidences .8 and .6.
- **Section 4.1** (`s4_1_penguin.gkp`): the conclusion is established in
  .8 x .7 = .56 of the worlds. The paper prints the share .56 only.
- **Section 4.2** (`s4_2_*.gkp`): a certain rule is read backwards and
  derives `-bird(t)` from `-flies(t)`; an uncertain rule (.99 or .8) is
  not read backwards, so nothing follows about `bird(t)`.
- **Section 5** (`s5_case_split_q.gkp`): the applications of the
  semantics each use one clause and establish neither `a` nor `b`, so `q`
  is in ignorance. gk's prover derives `q` by resolution; the paper uses
  this input to show where gk's value can differ from the semantics.
- **Section 6.1** (`s6_1_combined_b.gkp`): resolution derives `b` from
  both clauses, a combined application with support .6 x .7 = .42. The
  semantics has no such application; the paper prints no value of the
  semantics for `b`.
- **Section 6.4** (`s6_4_shared_premise_q.gkp`): both conditions of the
  rule for `q` come from the one premise `a`, so the support is .5, not
  .5 x .5.
- **Appendix A.2.1** (`a2_1_*.gkp`): the cycle of one sign is a sweep
  group, and its sweeps settle with `a` and `b` positive in .5 of the
  worlds; the cycle through exceptions is no sweep group, the narrowing
  makes no literal sure, and every atom is in ignorance.
- **Appendix A.2.5** (`a2_5_selection_*.gkp`): the four cases are `r`
  alone (.64, `p` positive), `-p` alone (.04, `r` negative), neither
  (.16, both in ignorance), and both (.16, `r` and `p` in conflict).
