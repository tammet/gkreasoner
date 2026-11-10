# O2: gk against the reference tool on the collection

This part reproduces Section 7.1 of the paper: gk against the reference
tool mcref on every input of the project's collection that the tool
accepts. It holds the 360 accepted inputs, a table of the 662 declined
inputs, one gk run and one mcref run per input, and the answer rows that
the paper counts.

## Files

| file | content |
|---|---|
| `inputs/<set>/...` | the 360 accepted inputs, by set; `inputs/demo/gk_similarity.txt` is read by `kingqueen.js` under `-similarities`, and `inputs/examples/gks/gks15_included.gks` is included by `gks15_include.gks` |
| `inputs.tsv` | each input with its set, its source and its SHA-256 |
| `lit_sources.tsv` | the source of each input of the set `lit` |
| `declined.tsv` | the 662 declined inputs: name, sets and the reason the tool gives; the files are not included |
| `runs.tsv` | 720 runs: gk without options (`-similarities` for `kingqueen.js`), and mcref with 20,000 worlds and seed 1 |
| `rows.tsv` | 438 answer rows: input, set, answer, class, gk's four shares, the tool's four estimates, the unresolved share, the tolerance, the largest difference, the flags, gk's approximation notes (the output field `readings`), the searches stopped by the budget, gk's stop message and exit status, the two run ids, the pending steps |
| `make_rows.py` | builds `rows.tsv` from the stored outputs; `tools/collect.py` calls it |
| `count_rows.py` | recomputes every count of Section 7.1 from `rows.tsv`, `inputs.tsv` and `declined.tsv`, and compares each with the paper |
| `row_statistics.py` | the statistics of the agreement on the resolved rows: the separation of the differences, approximation notes and stopped searches against agreement, agreement by kind of note, the differing rows with a cycle cut (`--cycles`), the run times (`--store` or `--raw`), and agreement by set |

## Rerun

From the repository root:

```sh
./bin/gk paper2026/O2_record/inputs/lit/plp/plp4_viral.gkp
python3 mcref/mcref.py paper2026/O2_record/inputs/lit/plp/plp4_viral.gkp --samples 20000 --seed 1
python3 paper2026/O2_record/count_rows.py
python3 paper2026/O2_record/row_statistics.py --cycles
python3 paper2026/check_gk.py --part O2 --mcref
```

gk runs in the folder of each input. The last command reruns all 720 runs
and compares their shares with `rows.tsv`; it takes about 15 minutes with
three runs at a time, most of it for the estimates of the generated
families. The full dataset holds the raw output of every run;
`python3 paper2026/tools/collect.py --raw paper2026/raw O2` rebuilds
`rows.tsv` from it.

## The collection

The project keeps a collection of 1,022 distinct inputs in eleven sets. It
is a development and example collection: most inputs were written while
the method was built, and many probe known cases. It is no held-out
benchmark. One input, `chain_12_pos.js`, belongs to two sets
(`families` and `boundary`), so the sets hold 1,023 set records. The tool
declines 662 inputs, among them 522 for equality, 86 for function symbols,
and every input of the two sets translated from English by a language
model (`nlpipe` and `mle`). gk ran on the 360 accepted inputs only.

The paper's phrase "86 for function symbols and both translated sets"
names two groups: the 86 inputs declined for function symbols, and the
445 inputs of the two translated sets, which the tool declines for
equality. `declined.tsv` gives the reason of every declined input; the
reasons other than equality and function symbols cover 54 inputs.

## Units and the agreement criterion

- **Answer row.** One ground answer. A question with variables gives one
  row for each instance that gk or the tool lists.
- **Comparable row.** A row on which gk and the tool both give a value for
  the same instance.
- **Settled row.** A comparable row on which the tool's unresolved share is
  0. The unresolved share is the share of sampled worlds in which the tool
  reaches no verdict on the answer.
- **Agreement.** A resolved row agrees when each of its four shares (for,
  against, conflict, ignorance) differs from the tool's estimate by at most
  e = sqrt(ln(8/.05)/(2n)) = .011264, with n = 20,000 worlds. e is the
  Hoeffding half-width with a union bound over the eight one-sided tails
  of the four shares.

On an agreeing row each share of gk lies within .0113 of a sampled
estimate. The criterion does not prove equality: a difference below the
tolerance stays undetected. The bound holds with 95 % for one answer and
gives no simultaneous guarantee for the collection. The runs used gk's
default deadline of 10 s; the record does not show what a longer deadline
gives.

## The counts of Section 7.1

`count_rows.py` prints:

```text
count                                                        rows  paper
inputs in the collection                                     1022   1022 ok
sets                                                           11     11 ok
inputs the tool declines                                      662    662 ok
declined for equality                                         522    522 ok
declined for function symbols                                  86     86 ok
declined inputs of the two translated sets                    445    445 ok
inputs the tool accepts                                       360    360 ok
gk processes that ended with exit status 0                    360    360 ok
answer rows                                                   438    438 ok
rows with a value on both sides                               395    395 ok
resolved rows                                                 394    394 ok
resolved rows that agree                                      375    375 ok
resolved rows that differ                                      19     19 ok
rows with an unresolved share (the Yale row)                    1      1 ok
rows without a comparable value                                43     43 ok
instances only the tool lists                                  35     35 ok
instances only gk lists                                         4      4 ok
inputs where neither side answers                               4      4 ok
instances only the tool lists, with a for share above e         4      4 ok
differing rows with an approximation note                      14     14 ok
  of these first: cycle cut                                    12     12 ok
  first: residual variable                                      1      1 ok
  first: step not represented                                   1      1 ok
differing rows without an approximation note                    5      5 ok
  of these with a search stopped by the budget                  3      3 ok
  of these with no search stopped                               2      2 ok

the Yale row: inputs/lit/nm/nm3_yale_shooting.gkp, gk [0,1,0,0], tool [0.0,0.0,0.0,0.0], unresolved share 1, gk's approximation notes: cycle cut x4
the two differing rows where every search ended:
  inputs/examples/confidences/rules2.js r(c): gk [0.3276,0.1776,0.3024,0.1924], tool [0.0,0.0,0.0,1.0]
  inputs/lit/plp/plp4_viral.gkp buys(c): gk [0.35,0,0,0.65], tool [0.4325,0.0,0.0,0.5675]

set        inputs   rows resolved  agree differ no value
ab            109    109      109    108      1        0
examples       97    136      115    101     14       21
families       54     54       54     54      0        0
lit            39     39       38     37      1        0
studies        21     47       33     32      1       14
demo           18     26       18     16      2        8
table          16     21       21     21      0        0
paper           4      4        4      4      0        0
boundary        2      2        2      2      0        0
total         360    438      394    375     19       43

0 counts differ from the paper
```

## The statistics of Section 7.1 and the notes table

`row_statistics.py --cycles` prints the separation of the agreeing and
the differing rows, the notes table of the paper (item 2, first three
lines; unfinished work is a search stopped by the budget or a pending
step), agreement by kind of note and the kind of cycle of the 12
differing rows with a cycle cut. With `--store STORE` or `--raw RAW` it
also prints the run times of the 360 gk runs (median .24 s, largest
6.8 s, 216 s in total, three runs at a time).

```text
1. Separation over the 394 resolved rows (375 agree, 19 differ)
   largest difference among the agreeing rows: 0.0106 (3.1 standard errors), inputs/examples/confidences/net_direct.gkp flies(a), share 3, gk [0.3,0,0.4,0.3], tool [0.29905,0.0,0.41065,0.2903]
   smallest difference among the differing rows: 0.0239 (8.3 standard errors), inputs/examples/confidences/conf3.js r(a), share 3, gk [0.15188,0.0012,0.79132,0.0556], tool [0.1404,0.0013,0.8152,0.0431]
   the 19 differences in ascending order: 0.0239, 0.0302, 0.0701, 0.0786, 0.0786, 0.0825, 0.0839, 0.0900, 0.0905, 0.0905, 0.1146, 0.1510, 0.1534, 0.2478, 0.2478, 0.5000, 0.7621, 0.8076, 0.9000
   agreeing rows with difference exactly 0: 112
   agreeing rows: median difference 0.0012, 90th percentile 0.0062, largest 0.0106

2. Approximation notes against agreement (the notes table: unfinished work)
                                                         agree differ
   no approximation note, no unfinished work               280      2
   no approximation note, unfinished work listed             5      3
   an approximation note                                    90     14
     the same with a stopped search alone:
   no approximation note, every search ended               281      2
   no approximation note, a search stopped by the budget      4      3

3. Agreement by kind of approximation note (a row with several kinds counts under each)
   kind                                            agree differ
   cycle cut                                          64     12
   residual variable                                   7      3
   step not represented or proof application           5      3
   self exception                                     24      2
   built-in                                            1      0
   rank zero as equal rank                             1      0
   rows whose notes are only self exception or rank zero as equal rank: 18 agree, 0 differ

4. The 12 differing rows with a cycle cut
   inputs/ab/A_cycle_through_exception__q0.js, q: gk [0.5,0,0,0.5], tool [0.0,0.0,0.0,1.0]; cycle: through exception literals only; of the kind of row C5b
   inputs/examples/confidences/alarm_v2.js, burglary(c): gk [0.442947,9.8e-05,0.30013,0.256825], tool [0.43705,0.0001,0.3702,0.19265]; cycle: across signs
   inputs/examples/confidences/conf2.js, r(a): gk [0.432,0.012,0,0.556], tool [0.4363,0.0119,0.1104,0.4414]; cycle: across signs
   inputs/examples/confidences/conf2.js, r(b): gk [0.36,0.01,0,0.63], tool [0.3632,0.00955,0.0877,0.53955]; cycle: across signs
   inputs/examples/confidences/conf3.js, r(a): gk [0.15188,0.0012,0.79132,0.0556], tool [0.1404,0.0013,0.8152,0.0431]; cycle: across signs
   inputs/examples/confidences/conf3.js, r(b): gk [0.36,0.01,0,0.63], tool [0.3632,0.00955,0.0877,0.53955]; cycle: across signs
   inputs/examples/confidences/n2.js, r(a): gk [0.1852,0.0024,0.7012,0.1112], tool [0.17265,0.00225,0.7314,0.0937]; cycle: across signs
   inputs/examples/confidences/n2c.js, r(a): gk [0.2724,0.0644,0.6356,0.0276], tool [0.11905,0.0,0.789,0.09195]; cycle: across signs
   inputs/examples/confidences/n2plus.js, r(a): gk [0.11232,0.8154,0,0.07228], tool [0.05425,0.05335,0.4835,0.4089]; cycle: across signs
   inputs/examples/exceptions/bird_penguin.js, -flies(p): gk [0.72,0,0,0.28], tool [0.72205,0.07655,0.0,0.2014]; cycle: across signs
   inputs/examples/exceptions/bird_penguin.p, -flies(p): gk [0.72,0,0,0.28], tool [0.72205,0.07655,0.0,0.2014]; cycle: across signs
   inputs/studies/study23_penguinsneg.js, flies(messy): gk [0,0.09,0,0.91], tool [0.0,0.0,0.0,1.0]; cycle: across signs

6. By set
   set         agree differ
   ab            108      1
   examples      101     14
   families       54      0
   lit            37      1
   studies        32      1
   demo           16      2
   table          21      0
   paper           4      0
   boundary        2      0
   total         375     19
```

## Results by set

| set | contents | accepted (rerun) | declined | answer rows | comparable | resolved | agree | differ | unresolved | no comparable value |
|---|---|---|---|---|---|---|---|---|---|---|
| ab | design probes of the recursive method, with exact hand values | 109 | 9 | 109 | 109 | 109 | 108 | 1 | 0 | 0 |
| examples | the example inputs of the gk distribution (folder `Examples/`) | 97 | 139 | 136 | 115 | 115 | 101 | 14 | 0 | 21 |
| families | generated directed families, with exact hand values | 54 | 54 | 54 | 54 | 54 | 54 | 0 | 0 | 0 |
| lit | examples with confidences and defaults from the literature (`lit_sources.tsv`) | 39 | 7 | 39 | 39 | 38 | 37 | 1 | 1 | 0 |
| studies | the published studies of gk's earlier ProbLog comparison | 21 | 2 | 47 | 33 | 33 | 32 | 1 | 0 | 14 |
| demo | the demonstration inputs of the gk distribution | 18 | 4 | 26 | 18 | 18 | 16 | 2 | 0 | 8 |
| table | the inputs of the extended comparison table | 16 | 2 | 21 | 21 | 21 | 21 | 0 | 0 | 0 |
| paper | worked examples of the method's design | 4 | 0 | 4 | 4 | 4 | 4 | 0 | 0 | 0 |
| boundary | boundary cases of the recursive method | 2 | 1 | 2 | 2 | 2 | 2 | 0 | 0 | 0 |
| nlpipe | English-pipeline cases, translated by a language model (not included) | 0 | 303 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| mle | Multi-LogiEval items, translated by a language model (not included) | 0 | 142 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| total | | 360 | 663 | 438 | 395 | 394 | 375 | 19 | 1 | 43 |

## The 19 differing rows

The flags are the approximation notes that gk records (cycle cut,
residual variable, step not represented) and one check of the row
builder: "contrapositive use of a certain rule", found in gk's dump. The
rows are in the order of the paper's count: first the cycle cut, then the
residual variable, then a step not represented, then no note with
searches stopped by the budget, then no note and no stopped search.

| # | input | answer | gk 1.2.5 | mcref 1.1.2 | largest difference | flags | searches stopped |
|---|---|---|---|---|---|---|---|
| 1 | `ab/A_cycle_through_exception__q0.js` | q | (.5, 0, 0, .5) | (0, 0, 0, 1) | .5000 | cycle cut | 0 |
| 2 | `examples/confidences/alarm_v2.js` | burglary(c) | (.4429, .0001, .3001, .2568) | (.437, .0001, .3702, .1926) | .0701 | cycle cut | 0 |
| 3 | `examples/confidences/conf2.js` | r(a) | (.432, .012, 0, .556) | (.4363, .0119, .1104, .4414) | .1146 | cycle cut | 0 |
| 4 | `examples/confidences/conf2.js` | r(b) | (.36, .01, 0, .63) | (.3632, .0095, .0877, .5395) | .0905 | cycle cut | 0 |
| 5 | `examples/confidences/conf3.js` | r(a) | (.1519, .0012, .7913, .0556) | (.1404, .0013, .8152, .0431) | .0239 | cycle cut | 0 |
| 6 | `examples/confidences/conf3.js` | r(b) | (.36, .01, 0, .63) | (.3632, .0095, .0877, .5395) | .0905 | cycle cut | 0 |
| 7 | `examples/confidences/n2.js` | r(a) | (.1852, .0024, .7012, .1112) | (.1726, .0022, .7314, .0937) | .0302 | cycle cut | 0 |
| 8 | `examples/confidences/n2c.js` | r(a) | (.2724, .0644, .6356, .0276) | (.1191, 0, .789, .092) | .1534 | cycle cut; step not represented | 0 |
| 9 | `examples/confidences/n2plus.js` | r(a) | (.1123, .8154, 0, .0723) | (.0542, .0534, .4835, .4089) | .7621 | cycle cut; residual variable | 0 |
| 10 | `examples/exceptions/bird_penguin.js` | -flies(p) | (.72, 0, 0, .28) | (.722, .0766, 0, .2014) | .0786 | cycle cut | 0 |
| 11 | `examples/exceptions/bird_penguin.p` | -flies(p) | (.72, 0, 0, .28) | (.722, .0766, 0, .2014) | .0786 | cycle cut | 0 |
| 12 | `studies/study23_penguinsneg.js` | flies(messy) | (0, .09, 0, .91) | (0, 0, 0, 1) | .0900 | cycle cut; residual variable; contrapositive use of a certain rule; step not represented | 0 |
| 13 | `examples/confidences/rules3.js` | p(a) | (.18, .08, .72, .02) | (.0984, 0, .804, .0977) | .0839 | residual variable | 0 |
| 14 | `demo/kingqueen.js` | prop(rich,q1) | (.9, 0, 0, .1) | (0, 0, 0, 1) | .9000 | step not represented | 0 |
| 15 | `demo/near.json` | near(c1,c10) | (.7522, 0, 0, .2478) | (1, 0, 0, 0) | .2478 | none | 46 |
| 16 | `examples/confidences/near.js` | near(c1,c10) | (.7522, 0, 0, .2478) | (1, 0, 0, 0) | .2478 | none | 46 |
| 17 | `examples/confidences/smokes_alchemy.js` | cancer(george) | (.1, 0, 0, .9) | (.251, 0, 0, .749) | .1510 | none | 10 |
| 18 | `examples/confidences/rules2.js` | r(c) | (.3276, .1776, .3024, .1924) | (0, 0, 0, 1) | .8076 | none | 0 |
| 19 | `lit/plp/plp4_viral.gkp` | buys(c) | (.35, 0, 0, .65) | (.4325, 0, 0, .5675) | .0825 | none | 0 |

An approximation note records an approximation that gk applied on the
row. It does not show that the approximation produced the difference:
that needs a controlled run that changes only that approximation and then
obtains the tool's value. No such run exists for any of the 19 rows, so
the notes are associated with the differences, not shown to cause them.

- **The cycle cut.** gk records the cut on 12 rows. On other inputs the cut
  alone changes the value; on these rows no run isolates it.
- **The residual variable.** gk represents an unbound variable of a proof
  by a fresh constant; the tool grounds over the constants of the input.
- **A step not represented.** gk states that the value rests on a proof
  step that its calculation does not represent. On `demo/kingqueen.js` the
  value comes from the base proof (checkpoint 1).
- **The budget.** Three runs spent their budget with searches stopped. No run
  at a longer deadline was made, so the budget is not shown to be the
  cause.

### The two rows without a note and without a stopped search

Both runs ended every search, and neither run recorded an approximation
note, a pending step or a stopped search. The saved applications explain both numbers.

`examples/confidences/rules2.js`, question `r(c)`: at the instance `c` the
input has four uncertain classical clauses:

```text
.9 :: p(c) or r(c)
.8 :: p(c) or not r(c)
.7 :: not p(c) or r(c)
.6 :: not p(c) or not r(c)
```

gk's dump has two applications of origin `composite`, each a proof by
cases on `p(c)` that uses two clauses together: `r(c)` from the source
events of the .9 and .7 clauses, and `not r(c)` from those of the .8 and
.6 clauses. Positive evidence then has probability .9 x .7 = .63 and
negative evidence .8 x .6 = .48, on disjoint sources: for .63 x .52 =
.3276, against .37 x .48 = .1776, conflict .63 x .48 = .3024, ignorance
.37 x .52 = .1924. The semantics builds applications from single clauses.
Each orientation needs a signed premise, and no fact supplies one, so the
semantics and the tool give ignorance. The composite applications put this
run outside Theorem 3 of the paper, although its output records no
approximation note.

`lit/plp/plp4_viral.gkp`, question `buys(c)`:

```prolog
0.7::buys(a).
trusts(b,a). trusts(c,b). trusts(c,a). trusts(a,c).
0.5::buys(X) :- trusts(X,Y), buys(Y).
query(buys(c)).
```

gk's dump has three applications: `buys(a)` (.7), `trusts(c,a)`, and
`buys(c) <- trusts(c,a), buys(a)` (.5). Its value .35 = .7 x .5 is exact
for this snapshot, which has no application for `buys(b)` and none for
`buys(c)` through `b`. For the full input, given `buys(a)`, `buys(b)` holds
in .5 of the worlds, and `buys(c)` then has support .75 with `buys(b)` and
.5 without it: .7 x (.5 x .75 + .5 x .5) = .4375. The tool's .4325 is an
estimate within .0113 of this value. The analysis does not show which
search behaviour omitted the route through `b`.

Both rows show that an ended search and an empty list of approximation
notes certify neither evidence completeness nor all the structural
hypotheses of Theorem 3.

## The unresolved row

The tool reports the unresolved share 1 on `alive(s2)` of
`lit/nm/nm3_yale_shooting.gkp`, the Yale shooting written with a certain shooting rule:
the input has two consistent readings. gk gives (0, 1, 0, 0) there, with the
approximation notes cycle cut x4. Part O8 explains the example.

## Rows without a comparable value

The 43 rows count neither as agreements nor as differences.

- **35 instances that only the tool lists.** 16 of
  them have a share for, against or in conflict, and 19 have
  ignorance only. Most of the first group have the against share 1: gk's
  answer list leaves out answers that are false. Four have support that
  gk did not return:

| input | instance | for share of the tool |
|---|---|---|
| `studies/study15_smokesproblog.js` | smokes(1) | .436 |
| `studies/study16_smokesproblog2.js` | asthma(1) | .175 |
| `studies/study17_semwebproblog.js` | moviebook(sleepyhollow) | .905 |
| `studies/study17_semwebproblog.js` | moviebook(theadventuresofrobinhood) | .975 |

- **4 instances that only gk lists:** `above_seven(8)` in `boundary_comparison.js`, `r($k6_1)` in `n2plus.js`, `flies($k7_1)` in `study20_neginconsistency3.js`, `flies($k13_1)` in `study23_penguinsneg.js`. The first is an
  arithmetic instance that the tool does not generate; the others are
  instances with a fresh constant.
- **4 inputs without an answer from either side:** `demo/quasi_4.js`, `demo/quasi_5.js`, `demo/quasi_6.js`, `demo/quasi_7.js`. gk
  reports that the recursion did not run, because its initial search
  returned no ground answer, and the tool finds no instance.

The four instances with support are missing answers of the recursive
method: for a question with variables it takes each ground answer of its
initial search as a separate root, and an instance that the initial search
does not return gets no report.

## Versions and provenance

The values come from gk 1.2.5 and mcref 1.1.2, run on 2026-11-10 by
`tools/run_store.py`, the gk runs three at a time and the mcref 1.1.2 runs
four at a time. The paper's earlier runs used
gk 1.2.3 and mcref 1.1.0; gk 1.2.5 gives the same value on every row, and
mcref 1.1.2 the same estimate (mcref 1.1.1 too). All 360 gk processes exited with status 0.
A normal exit does not mean that every nested search finished: the column
`stop` of `rows.tsv` gives gk's stop message, and five runs report that
searches were stopped by the budget or not run.

The inputs are copies of the files of the record of 2026-11-09, under
new folder names (`inputs.tsv` gives the SHA-256 of each). Their contents
are unchanged except in one file: the comment lines of
`examples/confidences/net_strong.js` named a document outside this
repository and were replaced by the comment lines of the same example in
`Examples/`; its statements are the ones that were run.
