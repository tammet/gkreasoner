# O4: different quantities on the same input

This part reproduces the five-inputs table of Section 7.3 of the paper and the matrix of
ten small inputs from which the five-inputs table takes five rows. Outside the common
class the compared systems return different quantities for one input:

- the support share of the support semantics, which gk computes;
- ProbLog's probability;
- the credal interval of PASTA: a lower and an upper probability over the
  stable models of each choice;
- the equal allocation of smProbLog: the mass of a choice split equally
  among its stable models, with a separate inconsistent mass;
- plingo's normalization: the weight of the stable models with the answer,
  divided by the weight of all stable models;
- the well-founded shares (true, false, undefined).

A difference between two of these quantities is a contrast of meanings. It
is no win for either side. One comparison here is a correctness check: gk
against the support target and the reference tool.

## Files

Each case has a folder. The file name says which system reads the file.

```text
O4_quantities/
  results.tsv  runs.tsv  enumerate.py
  c1_shared/               gk.gkp  problog.pl  plingo.plp
  c1b_positive_cycle/      gk.gkp  problog.pl  plingo.plp
  c2_exception/            gk.gkp  problog.pl  plingo.plp
  c2b_opposed_exception/   gk.gkp  problog_raw.pl  problog_usable.pl  plingo_raw.plp  plingo_usable.plp
  c3_contested/            gk.gkp  problog_raw.pl  problog_guarded.pl  problog_matched.pl
                           plingo_raw.plp  plingo_guarded.plp  plingo_matched.plp
  c4_equal_rank/           gk.gkp  problog.pl  plingo.plp  plingo_dummy.plp
  c4b_priority/            gk.gkp  problog.pl  plingo.plp
  c5_mutual_half/          gk.gkp  problog.pl  plingo.plp
  c5b_common_consequence/  gk.gkp  problog.pl  plingo.plp  plingo_dummy.plp
  c6_locality/             gk.gkp  constrained.lp  problog_unconstrained.pl  plingo.plp  plingo_unconstrained.plp
```

- `gk.gkp` is the gk input. The reference tool reads the same file. The five
  gk inputs of the five-inputs table are the files printed in Section 7.3 of the paper.
- `problog*.pl` and `constrained.lp` are the logic-program counterparts.
  ProbLog reads them, and `enumerate.py` computes the credal, equal
  allocation and well-founded columns from them. Each probabilistic fact
  of gk becomes a switch `p::sw_x.`, and an exception becomes negation as
  failure `\+`.
- `plingo*.plp` are the plingo renderings of the counterparts: `p::a.`
  becomes `a :- &problog("p").`, `\+` becomes `not`, and `query(q).`
  becomes `&query(q).` plingo stopped with a syntax error on each
  unrendered `.pl` file.
- `_dummy` files add the unused fact `dummy :- &problog("0.5").` plingo's
  ProbLog front end stops on an input without a probabilistic fact
  ("No soft weights in program"). The added fact makes the run possible.

The files are the files that were run, without changes.

## Rerun gk and the reference tool

From the repository root:

```sh
./bin/gk paper2026/O4_quantities/c5b_common_consequence/gk.gkp
python3 mcref/mcref.py paper2026/O4_quantities/c5b_common_consequence/gk.gkp --samples 200000 --seed 1 --all-atoms
```

The reference tool ran with 200,000 samples, seed 1 and `--all-atoms` on
this part, as in the runs of 2026-11-04. With `--all-atoms` the tool also
evaluates the atoms that the question does not depend on (field
`atom_values`). The tool gives the random draws of a world to the atoms
by their position in the sorted list of evaluated atoms, so the option
changes which draws an atom gets: without it the estimate of C6 is
(.59982, 0, 0, .40018) in place of (.6008, 0, 0, .3992). Both lie within
.0036 of the exact value (.6, 0, 0, .4). Each share lies within .0036 of the exact value
with 95 % confidence.
`python3 paper2026/check_gk.py --part O4 --mcref` reruns every gk and mcref
row of this part. Each gk run takes less than .5 s.

## Rerun the other systems and the enumeration

[`../SYSTEMS.md`](../SYSTEMS.md) says how to install ProbLog and plingo. The
commands, from the folder `paper2026/O4_quantities`:

```sh
problog c2b_opposed_exception/problog_usable.pl
plingo --frontend=problog c2b_opposed_exception/plingo_usable.plp
python3 enumerate.py */problog*.pl c6_locality/constrained.lp
```

`enumerate.py` needs Python 3 and no other package. It enumerates the
choices of the probabilistic facts. For each choice it finds the stable
models by brute force against the Gelfond-Lifschitz reduct and computes the
well-founded model by the alternating fixpoint. It prints the credal
bounds, the equal allocation, the inconsistent mass and the well-founded
shares of each query. Its output on these files equals the recorded output
of 2026-11-04 line by line. PASTA and smProbLog could not be installed for
the runs of 2026-11-04, so their columns come from this script and are
marked *enumerated*. The script computes the well-founded model without the
constraints of an input, so it gives no well-founded value for
`c6_locality/constrained.lp`.

## Results

The kinds of result in `results.tsv`:

- *target*: the four shares of the support semantics, a hand calculation;
- *run*: the system printed the value on the named file;
- *estimate*: mcref sampled 200,000 worlds with seed 1;
- *enumerated*: `enumerate.py` computed the value of the system's published
  semantics; no run of that system printed it;
- *declined*, *no answer*, *failed*, *not run*: the system gave no value.

The relation of a counterpart to its gk input:

- *exact translation*: the counterpart states the same knowledge, for this
  input only. This holds for C1, C1b and C2, which are positive or have a
  stratified exception;
- *non-equivalent analogue*: the counterpart states a nearby program in the
  system's own constructs. Its value is a different quantity.

### The five-inputs table

The paper's codes are the case names. "Same" means that gk returns the
support target exactly. The marks follow the paper: *E* enumerated, *A*
non-equivalent analogue, *P* see the note on C6.

| case | support target; gk | ProbLog 2.3.0 | credal (PASTA), E | equal allocation (smProbLog), E | plingo 1.1.0 | well-founded (t, f, u), E |
|---|---|---|---|---|---|---|
| C1, `q` | (.44, 0, 0, .56); same | .44 | [.44, .44] | .44 | .44 | (.44, .56, 0) |
| C2b, `flies(t)` | (.54, 0, 0, .46); same | .459 A | [.459, .459] A | .459 A | .459 A | (.459, .541, 0) A |
| C4b, `p` | (.1, .8, 0, .1); same | .18 A | [.18, .18] A | .18 A | .18 A | (.18, .82, 0) A |
| C5b, `q` | (0, 0, 0, 1); gk **(1, 0, 0, 0)**, cycle cut | rejected: negative cycle | [1, 1] A | 1 A | 1 A | (0, 0, 1) A |
| C6, `r` | (.6, 0, 0, .4); same | .6 P | no value A | all mass inconsistent A | no model, no value A | nc |

The file of each cell:

| case | gk and mcref | ProbLog and enumerate.py | plingo |
|---|---|---|---|
| C1 | `c1_shared/gk.gkp` | `c1_shared/problog.pl` | `c1_shared/plingo.plp` |
| C2b | `c2b_opposed_exception/gk.gkp` | `c2b_opposed_exception/problog_usable.pl` | `c2b_opposed_exception/plingo_usable.plp` |
| C4b | `c4b_priority/gk.gkp` | `c4b_priority/problog.pl` | `c4b_priority/plingo.plp` |
| C5b | `c5b_common_consequence/gk.gkp` | `c5b_common_consequence/problog.pl` | `c5b_common_consequence/plingo_dummy.plp` |
| C6 | `c6_locality/gk.gkp` | `c6_locality/constrained.lp` | `c6_locality/plingo.plp` |

The reference tool agrees with the support target within .0036 on all five
rows: (.4378, 0, 0, .5622), (.5400, 0, 0, .4600), (.1008, .7996, 0, .0996),
(0, 0, 0, 1) and (.6008, 0, 0, .3992).

### The matrix of ten inputs

The first table compares gk with the support target and the reference
tool. The tool's unresolved share is 0 on every row.

| case | input and question | support target | tool's estimate | gk 1.2.5 |
|---|---|---|---|---|
| C1 | shared evidence on two routes, `q` | (.44, 0, 0, .56) | (.4378, 0, 0, .5622) | same |
| C1b | a positive cycle, `q` | (.5, 0, 0, .5) | (.4992, 0, 0, .5008) | same |
| C2 | an uncertain exception, `flies(t)` | (.27, 0, 0, .73) | (.2718, 0, 0, .7282) | same |
| C2b | an exception with evidence of both signs, `flies(t)` | (.54, 0, 0, .46) | (.5400, 0, 0, .4600) | same |
| C3 | a contested premise, `flies(a)` | (0, 0, 0, 1) | (0, 0, 0, 1) | same |
| C4 | two certain defaults of equal rank, `pacifist(n)` | (0, 0, 0, 1) | (0, 0, 0, 1) | same |
| C4b | a priority between two defaults, `p` | (.1, .8, 0, .1) | (.1008, .7996, 0, .0996) | same |
| C5 | a mutual pair of exceptions at .5, `p(a)` | (.25, 0, 0, .75) | (.2502, 0, 0, .7498) | same, two cycle-cut notes |
| C5b | the common consequence `q` of a certain mutual pair | (0, 0, 0, 1) | (0, 0, 0, 1) | **(1, 0, 0, 0)**, two cycle-cut notes |
| C6 | an unrelated question `r` beside a certain contradiction | (.6, 0, 0, .4) | (.6008, 0, 0, .3992) | same |

The second table gives the other quantities. C2b and C3 have several
counterparts. *Raw* keeps the positive rule or fact alone. *Usable* and
*guarded* add a guard by negation as failure: the premise counts only
without evidence against it. *Matched* is a control for C3 only, with one
switch for both reports. Each of these counterparts has one stable model
per choice, so the three enumerated quantities have one value.

| case | ProbLog 2.3.0 | plingo 1.1.0 | credal, E | equal allocation, E | well-founded, E |
|---|---|---|---|---|---|
| C1 | .44 | .44 | [.44, .44] | .44 | (.44, .56, 0) |
| C1b | .5 | .5 | [.5, .5] | .5 | (.5, .5, 0) |
| C2 | .27 | .27 | [.27, .27] | .27 | (.27, .73, 0) |
| C2b, A | raw .27; usable .459 | raw .27; usable .459 | raw [.27, .27]; usable [.459, .459] | usable .459 | usable (.459, .541, 0) |
| C3, A | raw .45; guarded .225; matched 0 | .45; .225; 0 | [.45, .45]; [.225, .225]; [0, 0] | guarded .225 | guarded (.225, .775, 0) |
| C4, A | rejected: `NegativeCycle` | no probability; .5 with the unused fact | [0, 1] | .5 | (0, 0, 1) |
| C4b, A | .18 | .18 | [.18, .18] | .18 | (.18, .82, 0) |
| C5, A | rejected: `NegativeCycle` | .40 | [.25, .5] | .375 | (.25, .5, .25) |
| C5b, A | rejected: `NegativeCycle` | no probability; 1.0 with the unused fact | [1, 1] | 1 | (0, 0, 1) |
| C6, A | .6, no result for the constrained input | unsatisfiable, 0 models, no value | no value | all mass (1.0) inconsistent | not computed |

### Notes on the matrix

- **C5b is the one departure of gk from its semantics.** Two certain
  defaults block each other, and `q` follows from either. The semantics
  leaves both premises unusable, so `q` is in ignorance. gk prints two
  cycle-cut notes, one for each exception clause. After the cut both
  defaults apply, and gk returns (1, 0, 0, 0). Every stable model of the
  counterpart contains `q`, so gk's value equals the credal value.
- **C5.** gk prints the same two approximation notes and returns the target. The cut
  lets each default apply alone, which gives .25 here.
- **plingo .40 against the equal allocation .375 on C5.** plingo gives each
  stable model the weight of its choice and divides by the total. C5 has 5
  stable models with a total weight of 1.25. The choice with both switches
  on has two models, so `p(a)` gets (.25 + .25) / 1.25 = .40. The equal
  allocation splits the mass of that choice between its two models and
  gives .375. Neither value equals the credal interval [.25, .5].
- **C6.** With the constraint `:- p_pos, p_neg.` no choice has a stable
  model. plingo reports UNSATISFIABLE with 0 models. The credal
  construction has no value, and smProbLog's definition puts all mass into
  its inconsistent state. ProbLog 2.3.0 accepted `constrained.lp` and
  answered `r` .6, but its parser did not apply the constraint (the paper's
  mark *P*). ProbLog and plingo both give .6 on
  `problog_unconstrained.pl` and `plingo_unconstrained.plp`, the input
  without the constraint. The support semantics answers `r` unchanged and
  reports `p` as (0, 0, 1, 0).
- **Parsing.** ProbLog 2.3.0 parsed every `.pl` file unchanged. plingo
  stopped with a syntax error on each of the 14 unrendered counterparts,
  so it ran on the renderings.

The appendix's further tables of this topic are not part of this folder
part: ProbLog and plingo on the examples of the semantics sections, the
generated families under the five quantities (their inputs are in part
O3), and rows D1 to D7 of the earlier comparison table (part O5,
[`../../comparisons/`](../../comparisons/README.md)).

## Versions

ProbLog 2.3.0 and plingo 1.1.0 (with clingo 5.8.3) ran on 2026-11-04. The
paper's gk and mcref values came from gk 1.2.3 and mcref 1.1.0 on the same
day. Every gk and mcref row of this part names a run of gk 1.2.5 or mcref
1.1.2 of 2026-11-10 in the run store; each gives the value of the record,
the mcref runs with `--all-atoms` the record's counts.
