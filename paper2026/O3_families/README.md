# O3: benchmark families (the families tables)

This part reproduces the families tables of the paper (Section 7.2), the text around it,
and the detail of part O3 of the online appendix. Each family of the families tables has a section
below. Each section names the inputs, the target of
every instance and how it was obtained, gk's value, the limiting factor and
the commands. `results.tsv` has one row per value, `runs.tsv` one row per
run of gk and of the reference tool.

## Conventions

- gk prints four shares: for, against, conflict, ignorance. A single number
  in a table below is the share for; the shares against and conflict are
  then 0. `results.tsv` always gives the four shares.
- gk's value (0, 0, 0, 1) with 0 applications means that gk found no proof.
- gk runs at its default deadline of 10 s with its automatic strategy,
  unless a row names a deadline (`-seconds`) or a strategy file
  (`-strategy`). "Automatic" in the tables means gk's automatic strategy.
- The reference tool (mcref) uses 20,000 samples and seed 1. Each share then
  lies within .0113 of the exact value with 95 % confidence. In the delivery
  and equipment families it uses 100,000 samples (half-width .005).
- A target is one of five kinds: an exact value by enumeration or by an
  exact calculation, a hand value, the value of an external solver
  (ProbLog, pgmpy), an estimate of the reference tool, or a verdict by
  construction. The column `note` of each row of kind `target` says which.
- Each row of a gk or tool value in `results.tsv` repeats the target of its
  instance in the column `target`, where the instance has one;
  `tools/collect.py` compares the stored value with it.
- Counts in the text are per family.
- Times are wall-clock times of single runs on one machine that also ran
  other processes. During the runs of 2026-11-04 orphaned compiler
  processes of ProbLog ran on the same machine. Every run whose value or
  quoted time depends on the deadline or the load has `alone=yes` in
  `runs.tsv`.

The relation of an external encoding to the gk input:

- *exact translation*: the encoding states the same knowledge in the
  system's language, for this input only. The ProbLog files of this part
  hold certain rules, uncertain facts and uncertain rules, and write an
  exception `unless(e)` as `\+e` where nothing opposes `e`.
- *same construction*: a SPINdle or DEFT theory built by the same generator
  step as the gk input, in the system's own syntax. These systems give a
  verdict and no number, so the comparison is qualitative.

## Files

| folder | content |
|---|---|
| `bn/` | 13 gk inputs converted from five bnlearn networks; the BIF files are not in this folder (see "The bnlearn networks") |
| `university/` | 12 gk inputs and 12 ProbLog files of the university base; `univ_bench_rules.pl`, the 87 rules taken from the Univ-Bench ontology; `hyper.json` |
| `delivery/` | 21 gk inputs and 7 ProbLog files; `query_focus_equality.json` |
| `equipment/` | 18 gk inputs: 13 of the family, 2 controls of the reading of equality, 2 inputs with a derived identity and the question of the chain diagnosis; `probes/` (11 probes of equality heads); `strategies/` (8 strategy files); `query_focus_equality.json` |
| `smokers/` | 11 gk inputs and 8 ProbLog files: plain Smokers, the stratified variant, the variant with ranks; `hyper.json` |
| `grids/` | 10 gk inputs and 10 ProbLog files; `hyper.json` |
| `chains_trees/` | 7 gk inputs, 15 SPINdle theories (`.dfl`), 8 DEFT theories (`.dlgp`); `query_focus.json`; `strategies/` (13 strategy files of the sweep) |
| `cascades/` | 10 gk inputs, 6 SPINdle theories, 6 DEFT theories |
| `cyclic/` | 31 gk inputs (programs, rings, argumentation frameworks); 12 files in ProbLog syntax and 12 plingo files of the programs and rings |
| `tools/` | `generate.py` and `generators/`: the generators of the inputs; `targets.py`: the exact targets; `bn_marginals.py`: the pgmpy marginals; `extract_univ_bench_rules.py`: the rule extraction; `DeftRun.java`, `DelpRun.java`, `delp_pom.xml`: the drivers of DEFT and DeLP |

The file name says which system reads the file: `gk_*.gkp` gk and the
reference tool, `problog_*.pl` ProbLog, `plingo_*.plp` plingo,
`spindle_*.dfl` SPINdle, `deft_*.dlgp` DEFT.

## Rerun gk and the reference tool

From the repository root:

```sh
./bin/gk paper2026/O3_families/bn/gk_asia_xray.gkp
./bin/gk paper2026/O3_families/grids/gk_corner16.gkp -strategy paper2026/O3_families/grids/hyper.json
./bin/gk paper2026/O3_families/bn/gk_win95pts_pc2prt.gkp -seconds 60
python3 mcref/mcref.py paper2026/O3_families/bn/gk_asia_xray.gkp --samples 20000 --seed 1
```

gk prints the line `{"recursive": ...}` first; its field `value` holds the
four shares, rounded to 6 decimals. Its fields `applications`, `tasks_cut`,
`tasks_queued` and `stop` give the counts that the sections below quote.
The reference tool prints one JSON object; `answers[0].value` holds its four
estimates.

The column `options` of `results.tsv` gives each run's options with paths
relative to this part folder. The column `options` of `runs.tsv` gives them
relative to the input's folder, where the run store starts each run. To
rerun every gk and mcref row of this part and compare it with `results.tsv`:

```sh
python3 paper2026/check_gk.py --part O3 --mcref
```

This takes about an hour: 394 gk runs and 70 runs of the tool. Rows with
`alone=yes` in `runs.tsv` can give other values or counts on a loaded
machine or with another deadline.

The strategy files:

| file | text | used by |
|---|---|---|
| `hyper.json` | `{"strategy": ["hyper"]}` | university, Smokers, grids |
| `query_focus_equality.json` | `{"strategy": ["query_focus"], "query_preference": 1, "equality": 1}` | delivery, equipment ("`query_focus` with equality") |
| `chains_trees/query_focus.json` | `{"strategy": ["query_focus"], "query_preference": 1}` | chains and trees |
| `chains_trees/strategies/*.json` | the 13 fixed settings of the trial's sweep | the chain of 1,000 defaults, the tree of 2,047 nodes |
| `equipment/strategies/*_equality.json` | a strategy name with `"equality": 1` | the derived identity |
| `equipment/strategies/allowance_*.json` | `{"recursive_L0": 400}`, `{"recursive_L0": 2000}`, `{"recursive_r": 1}` | the equality-chain diagnosis |

The trial passed the strategies as text (`-strategytext`). The files hold
the same text. The texts of the derived-identity and allowance runs were not
saved; their files follow the trial's notes (see "Failures and provenance limits").

## Families reached: Bayesian networks of the bnlearn repository

*The paper (the families tables, families reached): Bayesian networks of the bnlearn repository: 7 marginals of Asia, Earthquake and Cancer; 2 shallow queries of Win95pts and Andes (76 and 223 nodes). target: exact enumeration on the small networks; pgmpy; gk 1.2.5, automatic: 9 of 9; fixed strategies: both: 9 of 9.*

**Inputs.** Asia (8 nodes, 19 clauses), Earthquake and Cancer (5 nodes, 12
clauses each), Win95pts (76 nodes, 1,326 clauses) and Andes (223 nodes,
2,676 clauses) are binary networks of the bnlearn repository. The
conversion (`tools/generators/networks.py`) reads the first state of a node
in the BIF file as true. True is positive usability and false is ignorance.
Each CPT row with a positive probability becomes a rule
`p::node :- ones, unless(g)`, where `g` holds when a parent that the row
sets to false holds. Each question is an unconditional marginal. The trial
asked for the deepest node, a middle node and the node with the most
parents of each network.

**Targets.** `tools/targets.py` computes the seven marginals of the small
networks exactly, as fractions, by enumeration of every state from the
decimals of the BIF file, without pgmpy, gk or the tool. pgmpy 1.1.2
computed the marginals of Win95pts and Andes by variable elimination
(`tools/bn_marginals.py`); the trial kept them rounded to 4 decimals.

| network, query | depth | target | gk, 10 s | gk, 60 s | tool |
|---|---|---|---|---|---|
| asia, xray | 3 | .11029004 | .1103 |  | .112 |
| asia, bronc | 1 | .45 | .45 |  | .445 |
| asia, either | 2 | .064828 | .0648 |  | .0663 |
| earthquake, johncalls | 2 | .06369707 | .0637 |  | .063 |
| earthquake, alarm | 1 | .0161142 | .0161 |  | .0164 |
| cancer, xray | 2 | .208141 | .2081 |  | .209 |
| cancer, cancer | 1 | .01163 | .0116 |  | .0109 |
| win95pts, prtstatpaper | 1 | .979 | .979 | .979 | .979 |
| andes, rapp3 | 2 | .8248 | .825 | .825 | not run |

**Result.** gk gives the seven exact marginals to below 6·10^-17. gk 1.2.5
rounds the shares of its first output line to 6 decimals; the field
`value_c.value` of the dump that follows the line holds the full value.
On all 33 runs of rows 1 and 2 that value equals, bit for bit, the value
that gk 1.2.3 printed in the trial of 2026-11-04, on which the paper's
bounds rest. The two shallow queries agree with pgmpy to the printed
digits, at 10 s and at 60 s. gk used at most 1.0 s on the small networks
and 6.7 s on `rapp3`. The family has no conditioning on evidence and no
multi-valued network. The tool's estimates confirm the conversion on
Win95pts.

## Families not reached: deep queries of Win95pts and Andes

*The paper (the families tables, families not reached): deep queries of Win95pts and Andes. target: pgmpy: .5726, .7766; .7955, .8971; gk 1.2.5, automatic: .695, .005; .630, .572; better fixed strategy: neither; `hyper`: .720, .345; .450, .283; longer deadline: 60 s: the same.*

| network, query | depth | pgmpy | gk, 10 s | gk, 60 s | tool |
|---|---|---|---|---|---|
| win95pts, problem1 | 8 | .5726 | .695 | .695 | .573 |
| win95pts, pc2prt | 6 | .7766 | .005 | .005 | .774 |
| andes, snode_151 | 40 | .7955 | .630 | .630 | not run |
| andes, snode_74 | 14 | .8971 | .572 | .572 | not run |

**Failure analysis.** gk misses all four targets at both deadlines, under
the automatic strategy. Each run of the trial ended with most nested tasks
still queued: 421 of 472 on `pc2prt`, 4,140 of 4,490 on `problem1` (60 s)
and 580 of 636 on `snode_74`. A cap on the number of answers stopped the
root search. The 60-s runs on `pc2prt` and `snode_74` repeated the same two
rounds, so a longer deadline does not help under the current allocation of
the budget. The errors go both ways: .695 lies above its target and .005
below. A partial calculation with exceptions therefore gives no lower
bound. The notes of the rows in `results.tsv` give the queued tasks of each
run of the trial.

## Families reached: the university base in the pattern of LUBM

*The paper (the families tables, families reached): university base generated in the pattern of LUBM: 42 rules, 306 to 3,782 uncertain facts, 12 queries. target: ProbLog 2.3.0; an exact calculation; gk 1.2.5, automatic: 12 of 12; fixed strategies: both: 12 of 12.*

**Inputs.** The official LUBM generator did not run in the trial. A custom
generator (`tools/generators/university.py`) builds universities over the
Univ-Bench vocabulary with LUBM's population pattern. The family is
therefore no official LUBM run, and it does not use LUBM's fourteen
queries. `tools/extract_univ_bench_rules.py` derived 87 Datalog rules from
the ontology (`univ_bench_rules.pl`); 42 are usable on the generated
predicates. Each fact has a random probability in (0, 1], and the rules are
certain. The gk input and the ProbLog file of an instance are the same text.

**Targets.** ProbLog's value, and an exact value: each answer is a
disjunction of independent facts, so its probability is 1 minus the product
of their complements (`tools/targets.py`).

| instance | facts | query | ProbLog | exact | gk, 10 s | `hyper`, 10 s | gk, 60 s |
|---|---|---|---|---|---|---|---|
| 1 department, scale .25 | 306 | `person` | .983935 | .983935 | .9839 | .9839 |  |
| 1 department, scale .25 | 306 | `employee` | .99764394 | .99764394 | .9976 | .9976 |  |
| 1 department, scale .25 | 306 | `organization` | 1 | 1 | 1 | 1 |  |
| 1 department, scale .25 | 306 | `memberOf` | .49 | .49 | .49 | .49 |  |
| 1 department, scale 1 | 1,261 | `person` | .96320384 | .96320384 | .9632 | .9632 |  |
| 1 department, scale 1 | 1,261 | `employee` | .9994135 | .9994135 | .9994 | .9994 |  |
| 1 department, scale 1 | 1,261 | `organization` | 1 | 1 | 1 | 1 |  |
| 1 department, scale 1 | 1,261 | `memberOf` | .49 | .49 | .49 | .49 |  |
| 3 departments, scale 1 | 3,782 | `person` | .96642184 | .96642184 | .9664 | .9664 | .9664 |
| 3 departments, scale 1 | 3,782 | `employee` | .99978095 | .99978095 | .9998 | .9998 | .9998 |
| 3 departments, scale 1 | 3,782 | `organization` | 1 | 1 | 1 | 1 | 1 |
| 3 departments, scale 1 | 3,782 | `memberOf` | .36 | .36 | .36 | .36 | .36 |

**Result.** gk returned ProbLog's value on 12 of 12 queries at 10 s, under
the automatic strategy and under `hyper`. The 60-s runs on the largest
instance gave the same values. gk 1.2.3 printed values within 5·10^-9 of
ProbLog's and within 7·10^-10 of the exact values. gk 1.2.5 gives the same
full values in the field `value_c.value` of its dump; its first output
line rounds them to 6 decimals.

**Limits.** The derivations are short: an answer depends on one to seven
facts, and an `organization` answer on 57 or 226. The `organization` values
round to 1, which is weak evidence that gk collected every alternative;
some of those runs ended with unfinished tasks. ProbLog answered each query
in under half a second; gk used .2 to 1.6 s, and 6.7 s on `organization`.
The reference tool declines the smallest instance at its grounding limit
(`univ.dept1_scale0.25_person.mcref`). The family supports no claim about
large databases.

## Families reached: cold-chain delivery

*The paper (the families tables, families reached): cold-chain delivery: a persistence default over situation terms, plans to 32 legs, 21 inputs. target: hand values; ProbLog on 7 function-free inputs; gk 1.2.5, automatic: 21 of 21; fixed strategies: `query_focus`: 21 of 21; `hyper`: 15 of 21.*

**Inputs.** One persistence default keeps a parcel cold over a plan of legs:
`cold(P, do(A, S)) :- cold(P, S), plan_step(P, A, S), unless(warmed(P, A, S)).`
A plan input has N legs (N = 2, 4, 8, 16, 32), each with a warming event of
.1, and a handover of .95. The control has `0.9::cold(p1, s0)`; the opposed
version adds `0.2::-cold(p1, s0)`. An exception-chain input derives the
warming event of its one leg through K certain rules (K = 1, 5, 20, 50). A
background input adds B unrelated parcels (B = 10, 50, 200). Four flattened
inputs replace the `do` terms by constants and a relation `succ`. The 21
inputs have 9 to 1,008 clauses. The ProbLog files of the controls write
`unless(warmed(P, A, S))` as `\+warmed(P, A, S)`; ProbLog grounds the
situation terms of these finite plans.

**Targets.** A hand value for each input: .9 × .9^N × .95 for a control,
.7 × .9^N × .95 for an opposed version, and .4655 = .7 × .7 × .95 for the
exception-chain and background inputs. The usable initial coldness of an
opposed input is .7: the two reports are on the one atom `cold(p1, s0)` and
share one draw. ProbLog ran on the 7 controls, the tool on the 4 flattened
inputs.

| input | target | automatic, 2 s | 10 s | 30 s | `query_focus`, 2 s | 10 s | 30 s | ProbLog | tool |
|---|---|---|---|---|---|---|---|---|---|
| 2 legs, control | .6926 | .6926 | .6926 | .6926 | .6926 | .6926 | .6926 | .69255 |  |
| 2 legs, control, flattened | .6926 |  | .6926 |  |  | .6926 |  | .69255 | .6923 |
| 2 legs, opposed | .5387 | .5387 | .5387 | .5387 | .5387 | .5387 | .5387 |  |  |
| 2 legs, opposed, flattened | .5387 |  | .5387 |  |  | .5387 |  |  | .5373 |
| 4 legs, control | .561 | .561 | .561 | .561 | .561 | .561 | .561 | .5609655 |  |
| 4 legs, control, flattened | .561 |  | .561 |  |  | .561 |  | .5609655 | .5622 |
| 4 legs, opposed | .4363 | .4363 | .4363 | .4363 | .4363 | .4363 | .4363 |  |  |
| 4 legs, opposed, flattened | .4363 |  | .4363 |  |  | .4363 |  |  | .4376 |
| 8 legs, control | .368 | .368 | .368 | .368 | .368 | .368 | .368 | .36804946 |  |
| 8 legs, opposed | .2863 | .2863 | .2863 | .2863 | .2863 | .2863 | .2863 |  |  |
| 16 legs, control | .1584 | .1760 | .1584 | .1584 | .1584 | .1584 | .1584 | .15843323 |  |
| 16 legs, opposed | .1232 | .1232 | .1232 | .1232 | .1232 | .1232 | .1232 |  |  |
| 32 legs, control | .0294 | .1760 | .0294 | .0294 | .1283 | .0294 | .0294 | .029358 |  |
| 32 legs, opposed | .0228 | .1956 | .0228 | .0228 | .1426 | .0228 | .0228 |  |  |
| exception chain of 1 rule | .4655 | .4655 | .4655 | .4655 | .4655 | .4655 | .4655 |  |  |
| exception chain of 5 rules | .4655 | .4655 | .4655 | .4655 | .4655 | .4655 | .4655 |  |  |
| exception chain of 20 rules | .4655 | .4655 | .4655 | .4655 | .4655 | .4655 | .4655 |  |  |
| exception chain of 50 rules | .4655 | .4655 | .4655 | .4655 | .4655 | .4655 | .4655 |  |  |
| 10 further parcels | .4655 | .4655 | .4655 | .4655 | .4655 | .4655 | .4655 |  |  |
| 50 further parcels | .4655 | .4655 | .4655 | .4655 | .4655 | .4655 | .4655 |  |  |
| 200 further parcels | .4655 | .4655 | .4655 | .4655 | .4655 | .4655 | .4655 |  |  |

`query_focus` in this table is the strategy file `query_focus_equality.json`.
The flattened inputs ran at 10 s only.

**Result.** At 10 s gk equals the hand value to four digits on 21 of 21
inputs, under both strategies. ProbLog agrees on every control, and the
tool agrees within its half-width. At 2 s three inputs miss the target:
the controls of 16 and 32 legs (automatic .1760 for .1584 and .0294;
`query_focus` .1283 for .0294) and the opposed plan of 32 legs (.1956 and
.1426 for .0228).

**Failure analysis.** At 2 s gk spent the budget before it ran the
exception search of each leg. A missed warming event leaves the persistence
of that leg unopposed, so the value lies above the target.

**The 2-s runs of 2026-11-10.** The values above come from the trial of
2026-11-04 and are the values that the paper and `results.tsv` print. The
2-s runs depend on the deadline and on the load, and the stored runs of
2026-11-10 (gk 1.2.5, each run alone) give other values: with the
automatic strategy the controls of 16 and 32 legs give .1760 and .2173,
the opposed plans of 16 and 32 legs .1760 and .2173; with `query_focus`
the control of 32 legs gives .1584 and the opposed plan .1426. With the
automatic strategy four plans now miss the target, the opposed plan of 16
legs among them. Part O6 stores two repeats of the 2-s run of the control
of 32 legs: .1956 and .1956. Every 2-s value that misses the target lies
above it, and every 10-s value equals the target.

## Families reached: equipment under stated equalities

*The paper (the families tables, families reached): equipment under stated equalities, to 2,011 clauses, 13 inputs. target: hand values under one reading of equality (a); gk 1.2.5, automatic: 9 of 13; fixed strategies: `query_focus`: 13 of 13; `hyper`: 0 of 13.*

**Inputs.** A pump and a controller share one supply through
`supply(pump) = b7` and `supply(controller) = b7`. One report states
`0.9::charged(b7)`. A contrary report states `0.2::-charged(maintenance_id)`,
with `maintenance_id = b7`. Each component works by a normal default on
`charged(supply(X))`, against contrary reports of .1 and .15. The question
`cooling_ready` needs both components. The 13 inputs have 11 to 2,011
clauses. In an equality-chain input the contrary report reaches `b7`
through K equalities (K = 1, 3, 6, 10, 20). Other inputs add N further
components (N = 2, 4, 8, 16), a second supply, or B unrelated installations
(B = 10, 50, 200).

**The open question of modelling.** gk reads two names stated equal as two
atoms joined by a certain application. The two reports then have
independent draws: `charged(b7)` is (.72, .02, .18, .08), and the answer is
.72 × .9 × .85 = .5508. Another reading identifies the names before the
world draw. Both reports are then on one atom with one draw: (.7, 0, .2,
.1), and .7 × .9 × .85 = .5355. Two controls support this account: the
flattened input without equality (`gk_flat_reference.gkp`) and the full
input with the contrary report written on `b7`
(`gk_contrary_report_on_b7.gkp`). The targets below use the first reading.
They do not settle the question, which stays open. No sampler and no
external solver checks this family: the tool declines equality, and
ProbLog has none.

| input | target, first reading | second reading | automatic, 2 s | 10 s | 30 s | `query_focus` with equality, 2 s | 10 s | 30 s |
|---|---|---|---|---|---|---|---|---|
| equality chain of 1 | .5508 | .5355 | .5508 | .5508 | .5508 | .5508 | .5508 | .5508 |
| equality chain of 3 | .5508 | .5355 | .6885 | .6885 | .6885 | .5508 | .5508 | .5508 |
| equality chain of 6 | .5508 | .5355 | .6885 | .6885 | .6885 | .5508 | .5508 | .5508 |
| equality chain of 10 | .5508 | .5355 | .6885 | .6885 | .6885 | .5508 | .5508 | .5508 |
| equality chain of 20 | .5508 | .5355 | .6885 | .6885 | .6885 | .5508 | .5508 | .5508 |
| 2 further components | .4461 | .4338 | .4461 | .4461 | .4461 | .4461 | .4461 | .4461 |
| 4 further components | .3614 | .3513 | .3614 | .3614 | .3614 | .3614 | .3614 | .3614 |
| 8 further components | .2371 | .2305 | .2371 | .2371 | .2371 | .2371 | .2371 | .2371 |
| 16 further components | .1021 | .0992 | .2789 | .1021 | .1021 | .4252 | .1021 | .1021 |
| second supply | .3966 | .3749 | .3966 | .3966 | .3966 | .3966 | .3966 | .3966 |
| 10 further installations | .5508 | .5355 | .5508 | .5508 | .5508 | .5508 | .5508 | .5508 |
| 50 further installations | .5508 | .5355 | .5508 | .5508 | .5508 | .5508 | .5508 | .5508 |
| 200 further installations | .5508 | .5355 | .5508 | .5508 | .5508 | .5508 | .5508 | .5508 |

| control | gk | tool |
|---|---|---|
| `gk_flat_reference.gkp`, no equality | .5355 | (.5350, 0, 0, .4650) |
| `gk_contrary_report_on_b7.gkp` | .5355 | |
| `gk_equality_chain1.gkp` | .5508 | declined (equality) |

**Result.** At 10 s gk reaches the first-reading value on 13 of 13 inputs
under `query_focus` with equality and on 9 of 13 under the automatic
strategy. The four misses are the equality chains of 3 to 20 (section "Families not reached: equality chains"). On
16 components at 2 s gk spent the budget before it found each contrary
report (.2789 automatic, .4252 `query_focus`).

The 2-s runs depend on the deadline and on the load. The stored runs of
2026-11-10 (gk 1.2.5, each run alone) give the trial's 2-s values on every
input but one: on 8 components under `query_focus` they give .2634 where
the trial gave .2371.

## Families reached: the common-class cases of the earlier comparison table

*The paper (the families tables, families reached): five common-class cases of our earlier comparison table (part O5): two with shared evidence, two published studies with answer variables, one recursive rule over function terms. target: values recorded from ProbLog 2.2.10; gk 1.2.5, automatic: 5 of 5; fixed strategies: both: 5 of 5.*

This row reuses five inputs of the earlier comparison table, part O5 in
[`../../comparisons/`](../../comparisons/README.md). This part holds no
copy of them:

| case | input | ProbLog 2.2.10 (recorded) | gk 1.2.5 |
|---|---|---|---|
| C1, two independent causes | [`comparisons/inputs/gk/c1.gkp`](../../comparisons/inputs/gk/c1.gkp) | .80 | (.8, 0, 0, .2) |
| C2, a conjunction | [`comparisons/inputs/gk/c2.gkp`](../../comparisons/inputs/gk/c2.gkp) | .30 | (.3, 0, 0, .7) |
| N1, an open question over a join | [`comparisons/inputs/gk/n1_study4.gkp`](../../comparisons/inputs/gk/n1_study4.gkp) | (a,a) .5, (a,b) .3, (b,a) .3, (b,b) .6 | the same, per binding |
| N2, an open question over a recursive rule | [`comparisons/inputs/gk/n2_study10.gkp`](../../comparisons/inputs/gk/n2_study10.gkp) | ann .8, bob .688, carl .1376 | the same, per binding |
| F1, recursion over function terms | [`comparisons/inputs/gk/f1.gkp`](../../comparisons/inputs/gk/f1.gkp) | .576 | (.576, 0, 0, .424) |

The recursive method answers N1 and N2 per binding. The runs ended every
search, with no stopped task, no queued task and no approximation note. The tool agrees on
C1, C2, N1 and N2 and declines F1 (function symbols). The gk values in the
table are those of the stored gk 1.2.5 runs of part O5; gk 1.2.3 gave the
same values in the trial. Part O5
([`../O5_comparisons/`](../O5_comparisons/README.md)) holds the run lists
and the results of gk 1.2.5 and of the tool on these inputs.

## Families not reached: Smokers and the stratified variant

*The paper (the families tables, families not reached): Smokers, 5, 8 and 12 persons. target: ProbLog .4796, .5904, .6475; gk 1.2.5, automatic: .4535 at every size; better fixed strategy: `hyper`: .4535, .5461, .5733; longer deadline: 60 s: the same.*

*The paper (the families tables, families not reached): the same with a stratified exception. target: ProbLog .1919, .0945, .1036; gk 1.2.5, automatic: .1865, .0890, .0937; better fixed strategy: `query_focus`: .1919 at 5 persons; no finished evaluation at 8 and 12; longer deadline: `hyper`, 60 s: .0778, .0922 at 8, 12.*

**Inputs.** The generator (`tools/generators/grids_smokers.py`) builds a
friendship graph by preferential attachment. Each person has stress with .3
and influences each other person with .2. A person smokes from stress, or
from a smoking friend who influences that person. The question is
`smokes(hub)` for the person with the most friends. The gk input and the
ProbLog file are the same text. The target is ProbLog's value, with a limit
of 300 s.

| persons, friendships | ProbLog | tool | gk, 10 s | gk, 60 s | `hyper`, 10 s | `hyper`, 60 s |
|---|---|---|---|---|---|---|
| 5, 7 | .4796 | .479 | .4535 |  |  |  |
| 8, 13 | .5904 | .592 | .4535 |  | .546 | .546 |
| 12, 21 | .6475 | not run | .4535 | .4535 | .573 | .573 |
| 16, 29 | no answer at 300 s | not run | .4535 | .4535 |  |  |
| 20, 37 | no answer at 300 s | not run | .4535 | .4535 |  |  |

**Failure analysis.** gk returned .4535 at each size, while the target rises
with the graph. Each run of the trial finished all nested tasks, with
nothing stopped and nothing queued. The base search found 5 and 8 distinct root
proofs and did not enumerate the proofs through longer chains of friends.
Under `hyper` it found 8 and 9 root proofs at 8 and 12 persons, and the
values moved closer to the target; a longer deadline changed nothing. At 16
and 20 persons no reference exists, and gk's value has the same defect.

**The stratified variant** adds `0.4::asthma(X) :- smokes(X),
unless(treated(X))`, with `0.6::treated` facts for every third person. The
question is `asthma(hub)`. The ProbLog file writes the exception as
`\+treated(X)`.

| persons | ProbLog | tool | gk, 10 s | `hyper`, 10 s | `hyper`, 60 s |
|---|---|---|---|---|---|
| 5 | .1919 | .1902 | .1865 | .1831 |  |
| 8 | .0945 | .0925 | .0890 | .0778 | .0778 |
| 12 | .1036 | .1042 | .0937 | .0922 | .0922 |

gk is short on each instance, for the cause seen on plain Smokers. `hyper`
gave lower values here than the automatic strategy, and the same values at
60 s on 8 and 12 persons.

**A variant with ranks** (`gk_ranked*.gkp`) adds evidence against the
treatment, an asthma default of rank 1 and an opposing default of rank 2
and strength .7 for the hub. The exact answer by hand is (0, .7, 0, .3).

| persons | target | gk, 10 s | tool |
|---|---|---|---|
| 5 | (0, .7, 0, .3) | (0, .7, 0, .3) | (0, .706, 0, .294) |
| 8 | (0, .7, 0, .3) | (0, .7, 0, .3) | (0, .702, 0, .298) |
| 12 | (0, .7, 0, .3) | (0, .7, 0, .3) | (0, .699, 0, .301) |

The answer does not depend on the smoking derivations, so this variant does
not test the many-path part of Smokers.

## Families not reached: ProbLog grids

*The paper (the families tables, families not reached): ProbLog grid, 16 edges, corner to corner. target: .6171 (exactly 40441/65536); gk 1.2.5, automatic: .359; better fixed strategy: `hyper`: .6171; longer deadline: 60 s: .359.*

**Inputs.** A grid has directed edges to the right, down and diagonally,
each a fact `0.5::edge`. Two rules define `path`. The question asks for a
path to the far corner from the node at distance d. The full grid is
16 × 16 with 705 edges. A corner grid keeps the last (d+1) × (d+1) nodes
only: 16, 33 and 56 edges. The gk input and the ProbLog file are the same
text. The target is ProbLog's value; `tools/targets.py` also gives the
16-edge value exactly by enumeration of the 2^16 edge choices.

| instance | target | gk, 10 s | gk, 60 s | `hyper`, 10 s | `hyper`, 60 s | tool |
|---|---|---|---|---|---|---|
| corner grid, 16 edges | .61708069 | .359 | .359 | .6171 |  | .617 |
| corner grid, 33 edges | .56517709 | .490 | .490 | .523 | .5652 | .562 |
| corner grid, 56 edges | .53226978 | .181 | .181 | .234 | .283 | .533 |
| full grid, distance 1 | .71875 | .719 |  |  |  | declined |
| full grid, distance 2 | .61708069 | .359 |  | .6171 | .6171 | declined |
| full grid, distance 3 | .56517709 | .434 |  | .484 | .533 | declined |
| full grid, distance 4 | .53226978 | .195 | .195 | .135 | .135 | not run |
| full grid, distance 5 | .50887161 | .061 | .061 | .071 | .071 | not run |
| full grid, distance 6 | no answer at 300 s | .031 | .031 |  |  | not run |
| full grid, distance 8 | no answer at 300 s | .008 | .008 |  |  | not run |

**Failure analysis.** The 16-edge grid has 13 paths. gk's base search found
3 distinct proofs at 10 s and at 60 s, all through the diagonal first step.
The value .359 is 23/64, the exact value of those three paths. The options
`-maxproofs 100` and `-explore` changed nothing (`grids.corner16.gk.maxproofs100`,
`grids.corner16.gk.explore`). Under `hyper` the search found 9 root proofs
and the exact value. On the larger grids the number of root proofs stopped
growing under `hyper`: 4 at distances 4 and 5 of the full grid, at both
deadlines. The count of root proofs alone does not measure coverage: on the
33-edge grid it stayed at 19 while the value rose from .523 to .5652. The
limit is the discovery of alternative derivations of one ground question.
gk prints no count of root proofs; the counts come from the dumps of the
trial's runs.

**ProbLog's timeouts.** ProbLog answered distances 1 to 5 in .2 to 5.4 s and
gave no answer at 300 s at distances 6 and 8. These timeouts occurred in its
compilation stage: its compiler `dsharp` continued as an orphan process
after each one. gk's values at distances 6 and 8 are incomplete by the
mechanism above, so these rows show no advantage of gk. The tool declines
the full grid at its grounding limit.

## Families not reached: default chains and trees

*The paper (the families tables, families not reached): default chains and trees: 1,000 defaults; 364 and 2,047 nodes. target: conclusion holds by construction; SPINdle, DEFT and the tool give it; gk 1.2.5, automatic: no proof, (0, 0, 0, 1); better fixed strategy: `query_focus`: the 364-node tree only; longer deadline: 60 s: the 364-node tree only.*

**Inputs.** Generated theories in the pattern of the Maher families: chains
of n rules, and trees of 63, 364 and 2,047 nodes. All inputs are ground and
certain. A defeasible rule `a => b` becomes the normal default
`b :- a, unless(-b, r)`; the chains and trees use rank 0, which gk reads as
equal rank. The SPINdle and DEFT theories are the same constructions in
their own syntax (`tools/generators/spindle.py`, `deft.py`).

| input | gk, 10 s | other gk runs | SPINdle | DEFT | tool |
|---|---|---|---|---|---|
| chain of 100 defaults | (1, 0, 0, 0) |  | proved, .016 s | a100(c) DEFEASIBLY_ENTAILED | (1, 0, 0, 0) |
| strict chain of 1,000 rules | (1, 0, 0, 0) |  | proved, .117 s |  | not run |
| chain of 500 defaults | (0, 0, 0, 1) | `query_focus`: (1, 0, 0, 0) |  |  | not run |
| chain of 1,000 defaults | (0, 0, 0, 1) | 60 s: (0, 0, 0, 1); the 13 settings of `strategies/`: no proof | proved, .072 s | a1000(c) DEFEASIBLY_ENTAILED | (1, 0, 0, 0) |
| tree of 63 nodes | (1, 0, 0, 0) |  | proved, .014 s | t1(c) DEFEASIBLY_ENTAILED | (1, 0, 0, 0) |
| tree of 364 nodes | (0, 0, 0, 1) | 60 s: (1, 0, 0, 0); `query_focus`: (1, 0, 0, 0) | proved, .052 s | t1(c) DEFEASIBLY_ENTAILED | (1, 0, 0, 0) |
| tree of 2,047 nodes | (0, 0, 0, 1) | the 13 settings of `strategies/`: no proof | proved, .166 s | t1(c) DEFEASIBLY_ENTAILED | (1, 0, 0, 0) |

**Failure analysis.** gk works from the question by resolution. A proof
along a chain of defaults keeps the blocker literal of each default in the
derived clause, so the clauses grow with the chain. The clauses of a strict
chain stay short. On the failed inputs the base search found no proof, so
no nested search started and the run ended after about 1.8 s. The sweep of
14 settings (the automatic strategy and the 13 files of
`chains_trees/strategies/`) found no proof of the chain of 1,000 defaults or
of the 2,047-node tree. One of the 13, `all_negative_pref`, is no strategy
name of gk; gk warns and runs its default search. `query_focus` proves the
chain of 500 defaults (501 applications) and the 364-node tree (364
applications in about 7 s). SPINdle and the tool do no proof search.
SPINdle handled 100,000 defaults in 1.7 s of reasoning time
(`spindle_chain100000.dfl`, 2.4 MB) and the tool evaluated the 2,047-node
tree in .4 s. These runs do not show that every top-down method fails on
chains. The section "SPINdle and DEFT" lists the other theories of the
trial.

## Families not reached: cascades with priorities and with equal ranks

*The paper (the families tables, families not reached): cascades of defaults, 401 clauses, with priorities and with equal ranks. target: `a0` positive by construction; SPINdle and DEFT agree on the first; gk 1.2.5, automatic: correct in 4 of 6 runs; with priorities **(0, 1, 0, 0)** in one run; better fixed strategy: both: correct with priorities, (0, 0, 0, 1) with equal ranks.*

**Inputs.** A cascade of n levels has the fact `a_n` and two defaults at
each lower level:

```
a_i  :- unless(-a_i, 1).
-a_i :- a_(i+1), unless(a_i, 2).
```

The ranks are 1 and 2, because gk reads rank 0 as equal rank. The question
is `a0`. If `a_(i+1)` is usable, the negative default of higher rank wins;
otherwise the positive default stands alone. The states alternate from
`a_n`, so `a0` is positive for an even n. With equal ranks (both 1) `a0` is
positive at an even distance from `a_n` and in ignorance at an odd one.

| n | clauses | priorities: target | gk | tool | equal ranks: target | gk | tool |
|---|---|---|---|---|---|---|---|
| 4 | 9 | (1, 0, 0, 0) | (1, 0, 0, 0) | (1, 0, 0, 0) | (1, 0, 0, 0) | (1, 0, 0, 0) | (1, 0, 0, 0) |
| 5 | 11 | (0, 1, 0, 0) | (0, 1, 0, 0) | (0, 1, 0, 0) | (0, 0, 0, 1) | (0, 0, 0, 1) | (0, 0, 0, 1) |
| 10 | 21 | (1, 0, 0, 0) | (1, 0, 0, 0) | (1, 0, 0, 0) | (1, 0, 0, 0) | (1, 0, 0, 0) | (1, 0, 0, 0) |
| 50 | 101 | (1, 0, 0, 0) | (1, 0, 0, 0) | (1, 0, 0, 0) | (1, 0, 0, 0) | (1, 0, 0, 0) | (1, 0, 0, 0) |
| 200 | 401 | (1, 0, 0, 0) | (0, 1, 0, 0) | not run | (1, 0, 0, 0) | (0, 0, 0, 1) | not run |

**The failure at 401 clauses.** At n = 200 the exact answer is (1, 0, 0, 0).
SPINdle proves `a0` in .16 s of reasoning time and DEFT entails it (2.8 s
wall time). gk 1.2.3 returned **(0, 1, 0, 0)** after
6.7 s, with 107 applications. The run stopped because the remaining
allowance was below its floor. The collection of applications stopped
before the chain was complete, and the result is a wrong answer. The
sources give no further diagnosis. An earlier memo of the trial reported
this run as correct; the review of 2026-11-04 withdrew that statement. The
tool did not run at this size.

**The equal-rank variant.** gk is correct to 101 clauses. At 401 clauses it
returned ignorance with 115 applications, an incomplete answer.

**The runs of 2026-11-10.** The cascades of 101 and 401 clauses use most
or all of gk's budget, so their verdict depends on the run. The run store
holds three runs of each, each alone (rows `.gk`, `.gk.r2`, `.gk.r3`):

| input | gk 1.2.5, three runs | applications |
|---|---|---|
| 101 clauses, priorities | (1, 0, 0, 0) three times | 101 each |
| 401 clauses, priorities | (1, 0, 0, 0) twice, (0, 1, 0, 0) once | 121, 121; 119 |
| 401 clauses, equal ranks | (1, 0, 0, 0) twice, (0, 0, 0, 1) once | 121, 121; 119 |

A run that imports all 121 applications gives the correct verdict; a run
that stops at 119 gives the wrong or the incomplete one. The first run of
the 101-clause cascade with priorities ran beside two other runs, spent
its budget with 95 applications and gave (0, 1, 0, 0); it is kept in the
run store as an earlier entry, and the row now names the run made alone.
`results.tsv` keeps the values that the paper prints.

**Note.** A first attempt of the trial used ranks 0 and 1, which gk and the
tool read as equal rank. Those runs are not part of this folder.

## Families not reached: equality chains and a derived identity

*The paper (the families tables, families not reached): equality chains of 3 to 20 equalities; a derived identity `U = V :- ...`. target: hand value .5508; the question follows through the identity clause; gk 1.2.5, automatic: .6885 at every size; no proof through the identity; better fixed strategy: `query_focus`: .5508 at every size; no proof through the identity; longer deadline: 2 s and 30 s: .6885.*

The equality-chain inputs are those of the equipment family with K = 3, 6, 10, 20; their
rows in `results.tsv` have the ids `equip.equality_chain*`.

**Failure analysis: equality chains.** Under the automatic strategy the
nested search for `-charged(b7)` ended without a proof on each chain of 3 or
more equalities. gk stopped after .6 s, and .6885 is the answer without the
contrary report. The nested allowance is not the cause: the settings
`recursive_L0` 400 or 2000 ms and `recursive_r` 1 gave the same value
(`equipment/strategies/allowance_*.json`). The base search proves the same
literal when it is the question (`gk_equality_chain3_contrary_question.gkp`,
value (.02, .72, .18, .08); 33 ms in the trial). Under `query_focus` the
nested searches found the chain at each length, with 52 applications at
K = 1 and 1,231 at K = 20 and 30 s.

**Failure analysis: the derived identity.** A second version
(`gk_derived_identity.gkp`) derives the identity by the clause
`U = V :- registered(U), registered(V), serial(U, N), serial(V, N).` The
clause makes the question provable. The recursive method found no proof:
its base search ended after about 45 ms with zero derivations, under the
automatic strategy and under six fixed strategies with equality
(`equipment/strategies/*_equality.json` and `query_focus_equality.json`).
The form with the serial number as a function term
(`gk_derived_identity_function.gkp`) gives no proof either. Probes locate
the limit: the search does not use a clause with a positive equality
between two distinct variables, in each written form tried. It uses a head
equality that is ground or has one variable.

| probe (`equipment/probes/`) | equality head | gk |
|---|---|---|
| `gk_head_ground.gkp` | `a = b :- p.` | (1, 0, 0, 0) |
| `gk_head_two_variables.gkp` | `X = Y :- p(X), p(Y).` | (0, 0, 0, 1) |
| `gk_head_serial_numbers.gkp` | `U = V :- registered(U), registered(V), serial(U, N), serial(V, N).` | (0, 0, 0, 1) |
| `gk_head_serial_numbers_function_term.gkp` | the same, with supply(pump) among the units | (0, 0, 0, 1) |
| `gk_head_one_variable.gkp` | `X = b :- p(X).` | (1, 0, 0, 0) |
| `gk_head_one_variable_under_function.gkp` | `f(X) = m :- p(X).` | (1, 0, 0, 0) |
| `gk_head_two_variables_relation.gkp` | `X = Y :- r(X,Y).` | (0, 0, 0, 1) |
| `gk_head_two_variables_uncertain.gkp` | `0.9::X = Y :- p(X), p(Y).` | (0, 0, 0, 1) |
| `gk_head_two_variables_flat_clause.gkp` | `X = Y | -p(X) | -p(Y).` | (0, 0, 0, 1) |
| `gk_head_two_variables_relation_guard.gkp` | `X = Y :- r(X,Y), p(X).` | (0, 0, 0, 1) |
| `gk_head_two_variables_disequality.gkp` | `X = Y :- p(X), p(Y), X != Y.` | (0, 0, 0, 1) |

## Families not reached: cyclic families

*The paper (the families tables, families not reached): cyclic families: exception rings of 3 to 30 defaults; random programs of 4 to 40 facts; argumentation frameworks of 6 to 40 arguments. target: the tool, within tolerance; gk 1.2.5, automatic: rings 4 of 6; programs 4 of 6; frameworks 9 of 14 questions; better fixed strategy: `query_focus`: frameworks 11 of 14; rings and programs 4 of 6.*

**Inputs.** A ring of k defaults has facts `0.5::f_i` and rules
`a_i :- f_i, unless(a_j)`, where j follows i on the ring. A random program
has n facts with probabilities between .2 and .8, one such rule per fact
with a random j, and some positive rules. The exception literal stands for
negation as failure; this is a policy analogue and no proved translation.
The files `problog_*.pl` and `plingo_*.plp` hold the same programs with
`\+` and `not`; part O4 of this folder gives their values under the other
quantities (appendix part O4.3).

| instance | gk, 10 s | tool |
|---|---|---|
| program of 4 facts | .281 | 0 |
| program of 6 facts | .244 | .237 |
| program of 8 facts | .221 | .219 |
| program of 12 facts | .228 | .227 |
| program of 20 facts | .380 | .380 |
| program of 40 facts | .635; 60 s: .635 | .679 |
| ring of 3 | .375 | .255 |
| ring of 4 | .3125 | .314 |
| ring of 5 | .344 | .314 |
| ring of 8 | .332 | .328 |
| ring of 15 | .3333 | .330 |
| ring of 30 | .3333 | .332 |

**Result.** gk records cycle-cut notes on every ring and every random
program. The cycle cut is gk's approximation for a cycle through
exceptions. gk agrees with the tool within tolerance on the rings of 4, 8,
15 and 30 and on the programs of 6, 8, 12 and 20 facts. It differs on four
instances: the ring of 3, the ring of 5, the program of 40 facts (the same
at 60 s) and the program of 4 facts ((.281, 0, 0, .719) against
(0, 0, 0, 1)).

**Failure analysis.** The exact value on the ring of 3 is .25
(`tools/targets.py`, from its eight choices). The semantics leaves the ring
in ignorance in the choice where all three facts hold; gk's cut lets each
default apply alone. The sources give no diagnosis for the other three
instances beyond the notes. The note also appears on the instances
that agree, so a note alone does not tell whether a value is affected.

**Argumentation frameworks.** Random frameworks have 6, 10, 20, 40 and 80
arguments, with 8 to 200 attacks. An argument `x` is accepted by
`acc(x) :- unless(att_x)`, with `att_x :- acc(y)` for each attacker y (a
single attacker is written directly). The grounded labelling is the target
for the labels in and out, and gk is correct on both at every size. It is
no reference for undecided arguments, because the semantics itself accepts
some of them. There gk agrees with the tool on the attacker atoms at 10
and 20 arguments and differs on the five other undecided questions: at 6
arguments gk gives ignorance and the tool accepts the argument; at 10 and
20 gk accepts the argument and the tool gives ignorance; at 40 gk accepts
the argument and its attacker atom, and the tool gives ignorance for both.
gk agrees with the tool on 9 of the 14 framework questions with a tool
value. At 80 the tool did not run. A first encoding of the
trial with certain rules `-acc(x) :- acc(y)` made each attack mutual,
because gk uses a certain rule in every direction; the trial replaced it,
and this folder holds the second encoding only.

| framework | grounded label | question | gk, 10 s | tool |
|---|---|---|---|---|
| 6 arguments, 8 attacks | in | `acc` | (1, 0, 0, 0) | (1, 0, 0, 0) |
| 6 arguments, 8 attacks | out | `acc` | (0, 0, 0, 1) | (0, 0, 0, 1) |
| 6 arguments, 8 attacks | undecided | `acc` | (0, 0, 0, 1) | (1, 0, 0, 0) |
| 10 arguments, 24 attacks | in | `acc` | (1, 0, 0, 0) | (1, 0, 0, 0) |
| 10 arguments, 24 attacks | out | `acc` | (0, 0, 0, 1) | (0, 0, 0, 1) |
| 10 arguments, 24 attacks | undecided | `acc` | (1, 0, 0, 0) | (0, 0, 0, 1) |
| 10 arguments, 24 attacks | undecided, attacker atom | `att_x` | (0, 0, 0, 1) | (0, 0, 0, 1) |
| 20 arguments, 54 attacks | undecided | `acc` | (1, 0, 0, 0) | (0, 0, 0, 1) |
| 20 arguments, 54 attacks | undecided, attacker atom | `att_x` | (0, 0, 0, 1) | (0, 0, 0, 1) |
| 40 arguments, 93 attacks | in | `acc` | (1, 0, 0, 0) | (1, 0, 0, 0) |
| 40 arguments, 93 attacks | out | `acc` | (0, 0, 0, 1) | (0, 0, 0, 1) |
| 40 arguments, 93 attacks | out, attacker atom | `att_x` | (1, 0, 0, 0) | (1, 0, 0, 0) |
| 40 arguments, 93 attacks | undecided | `acc` | (1, 0, 0, 0) | (0, 0, 0, 1) |
| 40 arguments, 93 attacks | undecided, attacker atom | `att_x` | (1, 0, 0, 0) | (0, 0, 0, 1) |
| 80 arguments, 200 attacks | in | `acc` | (1, 0, 0, 0) | not run |
| 80 arguments, 200 attacks | out | `acc` | (0, 0, 0, 1) | not run |
| 80 arguments, 200 attacks | out, attacker atom | `att_x` | (1, 0, 0, 0) | not run |
| 80 arguments, 200 attacks | undecided | `acc` | (0, 0, 0, 1) | not run |
| 80 arguments, 200 attacks | undecided, attacker atom | `att_x` | (1, 0, 0, 0) | not run |

**Tool version.** The tool's values above are those of mcref 1.1.2, which
computes the cycle rule of 2026-11-10: sweeps only for a sweep group (one sign, no
exception literal inside the group, no normal default, no unresolved
outside atom), the narrowing for every other cycle group. mcref 1.1.1 ran
sweeps on every group without a cycle across signs. Five values of this
part changed, all in this row, with the same seeds and sample counts:

| instance | mcref 1.1.1 | mcref 1.1.2 |
|---|---|---|
| program of 8 facts | (.222, 0, 0, .778) | (.219, 0, 0, .781) |
| program of 40 facts | (.665, 0, 0, .335) | (.679, 0, 0, .321) |
| 6 arguments, undecided, `acc` | (0, 0, 0, 1) | (1, 0, 0, 0) |
| 10 arguments, undecided, `acc` | (1, 0, 0, 0) | (0, 0, 0, 1) |
| 20 arguments, undecided, `acc` | (1, 0, 0, 0) | (0, 0, 0, 1) |

In the framework of 6 arguments, the arguments x3, x4 and x5 attack each
other through exception literals. The sweeps of 1.1.1 settled with x3 and
x4 accepted, so the attack on x1 held and `acc(x1)` was in ignorance. The
narrowing of 1.1.2 leaves x3, x4 and x5 undecided, and an undecided atom
of a group without a cycle across signs is in ignorance. The attacker x3
of x1 is then not established, and `acc(x1)` is positive in every world.
The agreement on the programs is unchanged: gk agrees within tolerance on
the programs of 6, 8, 12 and 20 facts and differs on those of 4 and 40.

**Tool version.** The tool's values above are those of mcref 1.1.2, which
computes the cycle rule of 2026-11-10: sweeps only for a sweep group (one sign, no
exception literal inside the group, no normal default, no unresolved
outside atom), the narrowing for every other cycle group. mcref 1.1.1 ran
sweeps on every group without a cycle across signs. Five values of this
part changed, all in this row, with the same seeds and sample counts:

| instance | mcref 1.1.1 | mcref 1.1.2 |
|---|---|---|
| program of 8 facts | (.222, 0, 0, .778) | (.219, 0, 0, .781) |
| program of 40 facts | (.665, 0, 0, .335) | (.679, 0, 0, .321) |
| 6 arguments, undecided, `acc` | (0, 0, 0, 1) | (1, 0, 0, 0) |
| 10 arguments, undecided, `acc` | (1, 0, 0, 0) | (0, 0, 0, 1) |
| 20 arguments, undecided, `acc` | (1, 0, 0, 0) | (0, 0, 0, 1) |

In the framework of 6 arguments, the arguments x3, x4 and x5 attack each
other through exception literals. The sweeps of 1.1.1 settled with x3 and
x4 accepted, so the attack on x1 held and `acc(x1)` was in ignorance. The
narrowing of 1.1.2 leaves x3, x4 and x5 undecided, and an undecided atom
of a group without a cycle across signs is in ignorance. The attacker x3
of x1 is then not established, and `acc(x1)` is positive in every world.
The agreement on the programs is unchanged: gk agrees within tolerance on
the programs of 6, 8, 12 and 20 facts and differs on those of 4 and 40.

**Tool version.** The tool's values above are those of mcref 1.1.2, which
computes the cycle rule of 2026-11-10: sweeps only for a sweep group (one sign, no
exception literal inside the group, no normal default, no unresolved
outside atom), the narrowing for every other cycle group. mcref 1.1.1 ran
sweeps on every group without a cycle across signs. Five values of this
part changed, all in this row, with the same seeds and sample counts:

| instance | mcref 1.1.1 | mcref 1.1.2 |
|---|---|---|
| program of 8 facts | (.222, 0, 0, .778) | (.219, 0, 0, .781) |
| program of 40 facts | (.665, 0, 0, .335) | (.679, 0, 0, .321) |
| 6 arguments, undecided, `acc` | (0, 0, 0, 1) | (1, 0, 0, 0) |
| 10 arguments, undecided, `acc` | (1, 0, 0, 0) | (0, 0, 0, 1) |
| 20 arguments, undecided, `acc` | (1, 0, 0, 0) | (0, 0, 0, 1) |

In the framework of 6 arguments, the arguments x3, x4 and x5 attack each
other through exception literals. The sweeps of 1.1.1 settled with x3 and
x4 accepted, so the attack on x1 held and `acc(x1)` was in ignorance. The
narrowing of 1.1.2 leaves x3, x4 and x5 undecided, and an undecided atom
of a group without a cycle across signs is in ignorance. The attacker x3
of x1 is then not established, and `acc(x1)` is positive in every world.
The agreement on the programs is unchanged: gk agrees within tolerance on
the programs of 6, 8, 12 and 20 facts and differs on those of 4 and 40.

## Fixed strategies and run times (runs of 2026-11-10)

The families tables of the paper give, beside the automatic strategy, the
better of the two fixed strategies `hyper` and `query_focus`. The trial
had run them on a few families only. On 2026-11-10 gk 1.2.5 ran under
both strategies, at the default deadline of 10 s, on the instances of
every family where the store had no such run: 189 runs of this part
(ids `*.gk.hyper` and `*.gk.query_focus`, strategy files `hyper.json` and
`query_focus.json` in the family folders) and 10 of part O5. A run is
alone when the automatic run of the same instance is. The family sections
above quote the result; `results.tsv` has every value.

The run times of Section 7.5 of the paper come from 39 further runs made
with no other run of the store active (ids `*.timing`, setting
`repeat=timing`): gk 1.2.5 under the automatic strategy and ProbLog 2.3.0
on the 12 university queries, and on the delivery plans of 2 to 32 legs
(gk on the control and the opposed plan, ProbLog on the control plan).
gk took .3 to 1.8 s on nine university queries and 6.8 to 6.9 s on the
three `organization` queries, where the budget stopped searches; ProbLog
took .1 to .5 s. On the delivery plans gk took .6 s at 2 legs, .9 s at 4
legs and 6.4 to 6.9 s from 8 legs on, and ProbLog .1 s. These ProbLog
runs give times only; the values of the families tables are ProbLog's
recorded runs of 2026-11-04.

## SPINdle and DEFT

SPINdle reads the theories directly: facts `>> a`, strict rules `->`,
defeasible rules `=>`, superiority `r > d`. DEFT is Defeasible Datalog±: it
has no classical negation, so a disputed pair of literals uses a negative
constraint `! :- a(X), na(X).`, and a defeasible fact is a rule from a fact
`top(c)`. The reasoning time is SPINdle's own figure, and for DEFT the
saturation and query time of the driver; the wall time includes the start
of the Java machine. The rows marked "not in the paper" are further
theories of the trial.

SPINdle's conclusion tags for the query literal: +Δ and -Δ say that the
literal is or is not definitely provable, +∂ and -∂ that it is or is not
defeasibly provable.

| theory | SPINdle | conclusion tags | paper |
|---|---|---|---|
| `chains_trees/spindle_chain100.dfl`, chain of 100 defaults | proved, .016 s | -Δ +∂ | part O3 |
| `chains_trees/spindle_strict_chain100.dfl`, strict chain of 100 rules | proved, .037 s | +Δ +∂ | part O3 (not in the paper) |
| `chains_trees/spindle_chain1000.dfl`, chain of 1,000 defaults | proved, .072 s | -Δ +∂ | families not reached: chains and trees |
| `chains_trees/spindle_strict_chain1000.dfl`, strict chain of 1,000 rules | proved, .117 s | +Δ +∂ | part O3 |
| `chains_trees/spindle_chain10000.dfl`, chain of 10,000 defaults | proved, .303 s | -Δ +∂ | part O3 (not in the paper) |
| `chains_trees/spindle_strict_chain10000.dfl`, strict chain of 10,000 rules | proved, .734 s | +Δ +∂ | part O3 (not in the paper) |
| `chains_trees/spindle_chain100000.dfl`, chain of 100,000 defaults | proved, 1.694 s | -Δ +∂ | Section 7.2 |
| `chains_trees/spindle_cycle100.dfl`, cycle of 100 defaults | no defeasible conclusion printed, .006 s | -Δ | part O3 (not in the paper) |
| `chains_trees/spindle_cycle10000.dfl`, cycle of 10,000 defaults | no defeasible conclusion printed, .098 s | -Δ | part O3 (not in the paper) |
| `chains_trees/spindle_tree63.dfl`, tree of 63 nodes | proved, .014 s | -Δ +∂ | part O3 |
| `chains_trees/spindle_tree364.dfl`, tree of 364 nodes | proved, .052 s | -Δ +∂ | families not reached: chains and trees |
| `chains_trees/spindle_tree2047.dfl`, tree of 2,047 nodes | proved, .166 s | -Δ +∂ | families not reached: chains and trees |
| `chains_trees/spindle_tree32767.dfl`, tree of 32,767 nodes | proved, 2.297 s | -Δ +∂ | part O3 (not in the paper) |
| `chains_trees/spindle_disputed1000.dfl`, 1,000 disputed pairs | not provable, .096 s | -Δ -∂ | part O3 (not in the paper) |
| `chains_trees/spindle_disputed10000.dfl`, 10,000 disputed pairs | not provable, .625 s | -Δ -∂ | part O3 (not in the paper) |
| `cascades/spindle_cascade5_priorities.dfl`, cascade of 5 levels, priorities | not provable, .01 s | -Δ -∂ | the summary table |
| `cascades/spindle_cascade5_equal.dfl`, cascade of 5 levels, equal ranks | no defeasible conclusion printed, .009 s | -Δ | part O3 (not in the paper) |
| `cascades/spindle_cascade200_priorities.dfl`, cascade of 200 levels, priorities | proved, .161 s | -Δ +∂ | families not reached: cascades |
| `cascades/spindle_cascade200_equal.dfl`, cascade of 200 levels, equal ranks | no defeasible conclusion printed, .292 s | -Δ | part O3 (not in the paper) |
| `cascades/spindle_cascade2000_priorities.dfl`, cascade of 2,000 levels, priorities | proved, 26.106 s | -Δ +∂ | part O3 (not in the paper) |
| `cascades/spindle_cascade2000_equal.dfl`, cascade of 2,000 levels, equal ranks | no defeasible conclusion printed, 52.884 s | -Δ | part O3 (not in the paper) |

| theory | DEFT | paper |
|---|---|---|
| `chains_trees/deft_chain100.dlgp`, chain of 100 defaults | a100(c) DEFEASIBLY_ENTAILED | part O3 |
| `chains_trees/deft_chain1000.dlgp`, chain of 1,000 defaults | a1000(c) DEFEASIBLY_ENTAILED | families not reached: chains and trees |
| `chains_trees/deft_chain5000.dlgp`, chain of 5,000 defaults | failed: java.lang.StackOverflowError | part O3 (not in the paper) |
| `chains_trees/deft_tree63.dlgp`, tree of 63 nodes | t1(c) DEFEASIBLY_ENTAILED | part O3 |
| `chains_trees/deft_tree364.dlgp`, tree of 364 nodes | t1(c) DEFEASIBLY_ENTAILED | families not reached: chains and trees |
| `chains_trees/deft_tree2047.dlgp`, tree of 2,047 nodes | t1(c) DEFEASIBLY_ENTAILED | families not reached: chains and trees |
| `chains_trees/deft_disputed100.dlgp`, 100 disputed pairs | a0(c) NOT_ENTAILED; na0(c) NOT_ENTAILED | part O3 (not in the paper) |
| `chains_trees/deft_disputed1000.dlgp`, 1,000 disputed pairs | a0(c) NOT_ENTAILED; na0(c) NOT_ENTAILED | part O3 (not in the paper) |
| `cascades/deft_cascade5_priorities.dlgp`, cascade of 5 levels, priorities | a0(c) NOT_ENTAILED; na0(c) DEFEASIBLY_ENTAILED | the summary table |
| `cascades/deft_cascade5_equal.dlgp`, cascade of 5 levels, equal ranks | a0(c) DEFEASIBLY_ENTAILED; na0(c) NOT_ENTAILED | part O3 (not in the paper) |
| `cascades/deft_cascade50_priorities.dlgp`, cascade of 50 levels, priorities | a0(c) DEFEASIBLY_ENTAILED; na0(c) NOT_ENTAILED | the summary table |
| `cascades/deft_cascade50_equal.dlgp`, cascade of 50 levels, equal ranks | a0(c) DEFEASIBLY_ENTAILED; na0(c) NOT_ENTAILED | part O3 (not in the paper) |
| `cascades/deft_cascade200_priorities.dlgp`, cascade of 200 levels, priorities | a0(c) DEFEASIBLY_ENTAILED; na0(c) NOT_ENTAILED | families not reached: cascades |
| `cascades/deft_cascade200_equal.dlgp`, cascade of 200 levels, equal ranks | a0(c) DEFEASIBLY_ENTAILED; na0(c) NOT_ENTAILED | part O3 (not in the paper) |

Two semantic differences are not errors. On the equal-rank cascade of odd
length SPINdle (ambiguity blocking) leaves `a0` undecided, the support
semantics gives ignorance, and DEFT (ambiguity propagating with team
defeat) entails `a0`. SPINdle's time on cascades with superiority grew
faster than linearly (.16 s at 200 levels, 26 s at 2,000); its chains and
trees stayed near linear up to 100,000 rules. DEFT failed on the chain of
5,000 defaults with `java.lang.StackOverflowError`. The theory
`spindle_strict_chain100000.dfl` of the trial (SPINdle +Delta in 5.4 s) is
not stored; `tools/generate.py` does not write it either.

Commands, from this part folder, with the jars and the class path of
SYSTEMS.md:

```sh
java -Xmx8g -jar spindle_2.2.4.jar chains_trees/spindle_chain1000.dfl
java -Xmx8g -cp "DEFT-1.0.0.jar:$DEFT_CLASSPATH" tools/DeftRun.java chains_trees/deft_chain1000.dlgp 'a1000(c)'
java -Xmx8g -cp "DEFT-1.0.0.jar:$DEFT_CLASSPATH" tools/DeftRun.java cascades/deft_cascade200_priorities.dlgp 'a0(c)' 'na0(c)'
```

SPINdle prints the conclusions of every literal; the query literal is `a_n`
for a chain, `t1` for a tree and `a0` for a cascade. DeftRun takes the
theory and the query atoms, saturates the knowledge base and prints the
entailment status of each atom and the times. `DelpRun.java` is the
corresponding driver for TweetyProject's DeLP (part O7 uses it); it parses
a DeLP program and prints YES, NO, UNDECIDED or UNKNOWN for each query.

## The bnlearn networks

The five networks come from the bnlearn repository (M. Scutari,
<https://www.bnlearn.com/bnrepository/>). This folder holds no copy of
them until their licence is checked. The gk inputs of `bn/` are our
conversions and are stored. To rebuild them, or to compute the targets,
download the files and check them:

| network | address | SHA-256 of the `.bif` file (after `gunzip`) |
|---|---|---|
| asia | <https://www.bnlearn.com/bnrepository/asia/asia.bif.gz> | `9f770c96940dc4d860b581602120790ac538983b30b28d38631b8184dc7b5f89` |
| earthquake | <https://www.bnlearn.com/bnrepository/earthquake/earthquake.bif.gz> | `74dd131e2c6437a39de17f2963d2d16fadd91e70450d1fc20501df05e8dc4f2e` |
| cancer | <https://www.bnlearn.com/bnrepository/cancer/cancer.bif.gz> | `05d4ea00a758450eed6fe68ea6de4da05ce0e3e919bd3e8ff7f0bc80a1db4b48` |
| win95pts | <https://www.bnlearn.com/bnrepository/win95pts/win95pts.bif.gz> | `14d2195e0c4613e0beb1f06e9199c8cd39a1154171a215c38b47c0fd773d0b36` |
| andes | <https://www.bnlearn.com/bnrepository/andes/andes.bif.gz> | `2330f233405fbbdf2a485651edd4130d3d09f816e81cb7056842ae6021edabe4` |

The trial used these five files; on 2026-11-10 the addresses above gave
files with the same SHA-256. Then:

```sh
python3 tools/generate.py --out NEW_FOLDER --bif BIF_FOLDER  # needs pgmpy and networkx
python3 tools/bn_marginals.py BIF_FOLDER                      # the pgmpy marginals of the 13 queries
python3 tools/targets.py --bif BIF_FOLDER                     # the exact targets, the BN part included
```

## Generators and targets

The inputs of every family except the hand-written equipment controls,
identity inputs and probes are generated. `tools/generate.py` writes them
with the sizes and seeds of the trial; its generation functions in
`tools/generators/` are copied unchanged from the trial's generators.
Its output equals the files of this folder byte for byte (checked when the
folder was built):

```sh
python3 tools/generate.py --out NEW_FOLDER
diff -r NEW_FOLDER/grids grids
```

`tools/targets.py` computes the exact targets: the 16-edge grid by
enumeration of 2^16 edge choices, the university answers by source
propagation, the ring of 3 from its 8 choices, the cascade values by the
recurrence, and with `--bif` the seven marginals of the small networks. It
prints one JSON object. It needs Python 3 only (`fractions`).

## Rerun the other systems

[`../SYSTEMS.md`](../SYSTEMS.md) says how to install each system. From
this part folder:

```sh
problog grids/problog_corner16.pl
problog university/problog_dept1_scale0.25_person.pl
problog delivery/problog_legs16_control.pl
plingo --frontend=problog cyclic/plingo_ring3.plp 0
```

The runner of the trial stopped ProbLog after 300 s (600 s on the university
base, the stratified Smokers and the delivery controls) and killed its
process group. The raw outputs of the external runs are in the full
dataset, not in this folder.

## Failures and provenance limits

- The 401-clause cascade with priorities is a wrong verdict of gk, not a
  slow answer (the cascades).
- The seven exact marginals and the university values: the paper's bounds
  6·10^-17, 5·10^-9 and 7·10^-10 rest on full-precision values. gk 1.2.5
  rounds the shares of its first line to 6 decimals and keeps the full
  value in the field `value_c.value` of its dump; on all 33 runs of rows 1
  and 2 that value equals gk 1.2.3's value bit for bit.
- The appendix says that the tool timed out at 600 s on the smallest
  university instance. The saved output of a later run of the trial, and
  mcref 1.1.2, decline the instance at the grounding limit instead.
- The trial wrote one output file per input and deadline. Where it ran two
  strategies at one deadline (delivery, equipment, university, stratified
  Smokers), the saved output is the later run; the result files of the
  trial keep the values of both.
- The automatic runs at 60 s on the corner grids of 33 and 56 edges have a
  value in the trial's notes and no saved output.
- The strategy texts of the six derived-identity runs and of the three
  allowance runs were not saved. `equipment/strategies/` reconstructs them
  from the trial's notes: a strategy name with `"equality": 1`, and the
  single keys `recursive_L0` and `recursive_r`.
- The tool's runs on the chain of 1,000 defaults (.22 s) and on the tree of
  2,047 nodes (.40 s) have values in the trial's notes and no saved output.
- The pgmpy marginals of Win95pts and Andes were kept rounded to 4 decimals
  in the trial's result file; pgmpy's own output was not saved.
- ProbLog's timeouts at 300 s (grids at distances 6 and 8, Smokers at 16 and
  20 persons) are recorded in the trial runner's log only.
- The appendix gives "2.3 s" for the chain of 500 defaults under
  `query_focus`; that is the time of the direct method's search in the
  sweep. The recursive run took 7.2 s.
- The record of the trial holds 68 further gk inputs that this folder
  leaves out: 10 inputs of the English cases with their DEFT and DeLP
  skeletons (part O7); 24 inputs of two trial families that the paper does
  not report (first-order defaults, published DeLP examples); 11 first
  versions of the delivery and equipment examples; 3 further probes of the
  equality chain; 20 further default theories (short chains, cycles,
  disputed pairs, and the cascades with ranks 0 and 1).

## Versions

The trial of 2026-11-04 ran gk 1.2.3 and mcref 1.1.0. Every gk and mcref
row of this part names a run of gk 1.2.5 or mcref 1.1.2 of 2026-11-10 in
the run store: 611 gk runs (400 of the trial's settings, 189 under fixed
strategies, 22 timing runs), 70 mcref runs and 17 ProbLog timing runs. The
gk and mcref runs give the printed value
on every row, except the rows that depend on the deadline or the load:
the 2-s delivery and equipment runs and the cascades of
401 clauses, described above. The external systems ran on
2026-11-04 with the versions in `results.tsv` and SYSTEMS.md.
