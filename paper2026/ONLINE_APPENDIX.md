# Online appendix

The online appendix of the paper "Reasoning with Uncertain Evidence, Opposition and Exceptions: Support Semantics
in Three Layers and a First-Order Inference Method" (T. Tammet, D. Draheim and P. Järv). The paper cites it by
part, O1 to O20.

## How to read this appendix

- Every result comes from **gk 1.3.2** and from the reference tool **mcref 1.3.1**. gk answers by the exact method
  (`gk -exact FILE`), by the general method (`gk -general FILE`), or by the default (`gk FILE`), which runs the
  exact method within half of the time limit and then the general method with the time left. The tool computes
  the semantics on the grounding of an input, by exact evaluation or, above its cell limit, by sampling.
- A value is four shares in the order **for, against, conflict, ignorance**. Where some worlds give an atom no
  value, the share of these worlds is written after a semicolon: (.52, 0, 0, 0; .48). gk's output names that
  share `unresolved`.
- This file is part of the archive folder <https://github.com/tammet/gkreasoner/tree/master/paper2026>. The parts
  with data are the folders O1 to O8 and O13 to O20 beside it. Each folder has a README with what the part shows,
  where its inputs come from, the command that reruns it, and one row per run and answer. Its tables are computed
  from the part's results by the folder's scripts. The full dataset, with the raw output of every run and the
  binaries, is archived at Zenodo.
- The parts O9 to O12 are texts. O9 and O10 point to the documents of the repository that describe gk and the
  tool. O11 prints the complete definition of the semantics. O12 gives the details of gk's output and limits that
  Section 6 of the paper refers to.
- Every timing is one run on a machine that also ran other jobs. A timing gives an order of magnitude and no
  ranking.

## Parts

| part | contents | where |
|---|---|---|
| O1 | the Tweety stages of Section 2, with the encodings of the other systems and the runs of s(CASP) on the lineage | archive folder [`O1_tweety`](O1_tweety/README.md) |
| O2 | our collection: 1,022 inputs written while the method was built; the tool accepts 360 | archive folder [`O2_record`](O2_record/README.md) |
| O3 | the benchmark families, and the inputs on which a specialized system is stronger | archive folder [`O3_families`](O3_families/README.md) |
| O4 | ten small inputs under the quantities of the compared systems | archive folder [`O4_quantities`](O4_quantities/README.md) |
| O5 | the 16 small cases on 9 systems, one encoding per system | archive folder [`O5_comparisons`](O5_comparisons/README.md) |
| O6 | the time budget of the general method, and the runs at 600 s | archive folder [`O6_budget`](O6_budget/README.md) |
| O7 | inputs translated from English, and the 303 tasks of the translation pipeline | archive folder [`O7_english`](O7_english/README.md) |
| O8 | further examples of cycles | archive folder [`O8_cycles`](O8_cycles/README.md); the examples below |
| O9 | gk's methods in detail | the documents of the repository, below |
| O10 | the reference tool in detail | the documents of the repository, below |
| O11 | the complete definition of the semantics with all 42 examples, and the inputs of the stated limits | below; the small examples of the text in archive folder [`O11_text_examples`](O11_text_examples/README.md) |
| O12 | the schedule and the checkpoints of the general method, one proof in full, the limits of the exact method and of the evaluation, and gk's notes | below |
| O13 | the comparison of gk with the tool on generated inputs, the collection and the families; the check on 225,102 further questions and 5,000 pairs with function terms | archive folder [`O13_conformance`](O13_conformance/README.md) |
| O14 | route queries in four families, and the counts of ground statements | archive folder [`O14_routes`](O14_routes/README.md) |
| O15 | the university base with a contradiction that no query mentions | archive folder [`O15_contradiction`](O15_contradiction/README.md) |
| O16 | delivery plans with function terms | archive folder [`O16_function_terms`](O16_function_terms/README.md) |
| O17 | BoardgameQA, converted by a script from its formal form | archive folder [`O17_boardgameqa`](O17_boardgameqa/README.md) |
| O18 | Lifschitz's benchmark problems | archive folder [`O18_lifschitz`](O18_lifschitz/README.md) |
| O19 | theories of defeasible logic | archive folder [`O19_defeasible_logic`](O19_defeasible_logic/README.md) |
| O20 | the exact method on inputs outside both of its classes | archive folder [`O20_outside_classes`](O20_outside_classes/README.md) |

## The parts with data

Each part below is a folder beside this file. Its README holds the tables of the part, computed from its results,
and the command that reruns its gk and tool runs and compares each value with the recorded one:

```sh
python3 check_gk.py --part FOLDER --gk PATH/TO/gk --mcref PATH/TO/mcref.py
```

### O1 The worked example (Tweety)

Folder: [`O1_tweety`](O1_tweety/README.md).

The five Tweety stages of Section 2: an uncertain exception, a disjunction, evidence against a premise with an
uncertain or a certain gull rule, and the lineage with function terms. The folder holds the gk input of each
stage, the encodings of the stages for ProbLog, plingo, PASTA and smProbLog where the system can state them, the
ground abstractions of the lineage stages for the tool, the inputs with one lineage rule only, and the runs of s(CASP) on the lineage (the
section "s(CASP) on stage 4"): the crisp counterparts of stage 4, the commands, and the outputs of 7 short
runs, 3 runs of one hour and 11 controls. gk
answers every stage under the default,
the exact method and the general method; the tool computes stages 1 to 3b exactly and the ground abstractions of
stage 4. Section 2 and the Tweety table of Section 7.2 use this part, and Sections 2.4 and 7.2 use the s(CASP)
runs, also for the dependence of its result on the order of the clauses; the value (.6984, .224, 0, .0776) of the
certain gull rule in Section 4.6 is the row of stage 3b.

### O2 Our collection

Folder: [`O2_record`](O2_record/README.md).

The 1,022 inputs that were written while the method was built, in 11 sets: design probes, examples of the
documentation, published studies, cases restated from the literature, and two sets translated from English by a
language model. The tool accepts 360 of them. gk answers each accepted input under the default, the general
method and the exact method, and the tool computes it, exactly or by sampling. The inputs that the tool declines
are listed with the reason and with the answer of the default. The table of test material in Section 7 uses
this part; the questions of this collection are also among those of part O13.

### O3 The benchmark families

Folder: [`O3_families`](O3_families/README.md).

Bayesian networks of the bnlearn repository, a university knowledge base in the pattern of LUBM, delivery plans,
equipment with equality, Smokers, ProbLog grids, chains and trees of defaults, cascades with priorities, cyclic
inputs, and five cases of the comparison table: 108 inputs. Each input has a target from outside our tools,
whose kind the results name. gk answers each input under the default, the general method and the exact method at
the time limit of 10 s. Sections 7.1, 7.3, 7.5 and 7.6 use this part, and Appendix C uses its saved runs of the
compared systems.

### O4 Different quantities on the same input

Folder: [`O4_quantities`](O4_quantities/README.md).

Ten small inputs, each with the quantity that each compared system returns: the support share of gk, ProbLog's
probability, PASTA's credal interval, the equal allocation of smProbLog, plingo's normalization and the
well-founded shares. Five of them are the construct-isolating inputs of the table of numerical quantities in
Appendix D; there the case name S-C*n* denotes case C*n* of this part.

### O5 The 16 small cases on 9 systems

Folder: [`O5_comparisons`](O5_comparisons/README.md).

The cases of the table of the 16 small cases in Appendix D ("Sixteen small comparison cases"): 18 gk inputs,
each stated in gk and in the languages of ProbLog, PASTA, plingo, smProbLog, TweetyProject, clingo, DLV, I-DLV
and s(CASP). gk answers the 18 inputs under
the default, the general method and the exact method, and the tool computes the inputs that it accepts. The cells
of the other systems come from their recorded runs, with the versions of [`SYSTEMS.md`](SYSTEMS.md). The folder
holds the encodings and the number behind every cell. Section 7.2 (the contested premise, row D3) and Appendix C
use this part.

### O6 The time limit

Folder: [`O6_budget`](O6_budget/README.md).

The part holds two kinds of runs. The table of the time budget has single runs that show how a value of the general method
depends on the time limit: the delivery plan of 32 legs at 2, 10 and 60 s, the grid of 56 edges at 10 and 60 s,
and the library member and "Does John eat berries?" (case N4 of part O7) at 10 and 60 s. The answer to "Does
John eat berries?" is (.98, 0, 0, .02) at 10 s and (0, .98, 0, .02) at 60 s.

The section "The effect of a longer time limit" holds the runs at 600 s: every run of the archive that was
wrong, without a value or not complete at 10 s ran again with `-seconds 600`, 92 runs in all. Of the 40 runs
that were wrong or without a value at 10 s, 1 is right at 600 s: the defeasible tree of two branches and depth 14
under the exact method, complete. Of the 17 runs that were right but not complete at 10 s, none is complete at
600 s. The section's second table lists the 7 runs whose value changes, among them "Does John eat berries?"
under the general method. Section 7.6 uses this part for the effect of a longer time limit.

### O7 Inputs translated from English

Folder: [`O7_english`](O7_english/README.md).

Four English cases that a language-model pipeline translated into gk input, the certain skeletons of two of them
for DEFT and TweetyProject DeLP, and the 303 tasks of the pipeline's regression set, run with gk's option for
taxonomy priorities. Section 7.6 uses the 303 tasks. The runs of case N4, "Does John eat berries?", at 10, 60
and 600 s are in part O6.

### O8 Further examples of cycles

Folder: [`O8_cycles`](O8_cycles/README.md).

The examples of cycles below, 33 questions in all. The folder holds one input per question, the value of the
semantics stated here, and the answers of gk under the default and of the tool. The table of the three methods
in Section 7.6 uses the cyclic inputs of this part.

The entries below give the input, the question, the four shares and the rule of the semantics that produces
them. The rules are the narrowing of Section 4.6 of the paper and the definitions of Appendix A and part O11.
gk 1.3.2 under the default (the exact method, complete) and the tool give every stated value; one further value,
marked below, is a hand calculation that no version of the tool computes. The entries name six rules.

- **Chain conflict.** A chain is a sequence of certain applications, each reading the head of the previous one.
  Suppose the evidence establishes the start of a chain and the complement of its end. Step 5 of the narrowing
  then fixes every atom of the chain in conflict.
- **Chain stop.** A fact, or an application with a body established outside the group, counts in both the sure
  and the possible set. An atom with such opposing evidence of its own is in conflict, and the chain ends there.
- **Nothing from conflict.** An atom in conflict supplies no usable literal of either sign.
- **Ordinary first.** In a cycle across signs with normal defaults, the ordinary applications are evaluated
  alone first. Their settled atoms keep their states.
- **Undecided in the narrowing.** A group with an exception literal or a normal default inside is evaluated by
  the narrowing. When it has no cycle across signs, an atom that the narrowing leaves undecided is in ignorance.
- **No value.** In a cycle across signs, an atom with a literal that is possible but not sure has no value. The
  share of these worlds is a fifth number, and nothing is rescaled.

#### Cycles across signs without normal defaults

**1. A longer chain.** Input: `0.8::r. 0.2::-q. p :- r. q :- p.` Question: `q`. Result: (.64, .04, .16, .16), and the same for `p` and `r`. In the .16 share where both facts pass, all three atoms are in conflict. A chain of any length gives the same numbers. Rule: chain conflict.

**2. The uncertain bird.** Input: `0.8::bird(t). flies(X) :- bird(X). -flies(t).` Questions: `bird(t)` and `flies(t)`. Result: (0, .2, .8, 0) for both. In .8 of the worlds the chain from `bird(t)` to `flies(t)` starts at an established atom. It ends at an atom with a fact against it. In the other .2, `-flies(t)` gives `-bird(t)` by the rule read backwards. An added fact `sings(t)` stays (1, 0, 0, 0), because it lies in another group. Rule: chain conflict.

**3. A chain that stops at an atom with its own opposing evidence.** Input: `0.8::r. 0.5::-p. 0.5::-q. p :- r. q :- p.` Question: `q`. Result: `q` (.2, .3, .2, .3) and `p` (.2, .15, .6, .05). Rule: chain stop.

- Where `r`, `-p` and `-q` all pass (.2), the chain from `r` reaches `p`. The fact `-p` is in force, so `p` is in conflict and the chain ends. `q` keeps only its fact `-q` and is negative.
- Where `r` and `-q` pass and `-p` fails (.2), the chain from `r` through `p` to `q` runs to its end. All three atoms are in conflict.
- The all-certain version `r. -p. -q. p :- r. q :- p.` gives `q` (0, 1, 0, 0). `r` and `p` are in conflict, and `q` is negative from its fact.

The trace of the first case: the group is {r, p, q}. The sure set stays empty in the first round, because every literal has possible opposition. The possible set is {r, ¬p, ¬q}. The literal p, tested with the application from r against the passing fact ¬p, gets conflict. So does ¬r against the passing fact r. The literal q needs p, which is not possible. Step 5 fixes r and p in conflict. It does not fix q, which has only its fact against it. The procedure repeats without r and p. The only application for q reads p, which is fixed and supplies no literal. The fact ¬q decides: ¬q is sure, and q is negative.

**4. Two routes from both sides of a conflict.** Input: `0.8::r. 0.2::-p. p :- r. 0.9::q :- p. 0.9::q :- -r.` Question: `q`. Result: (.7416, 0, 0, .2584), in either order of the two rules for `q`. In .64 of the worlds `p` is positive and `q` has support .9. In .04, `r` is negative and `q` has support .9. In .16 both `r` and `p` are in conflict. The clause `p :- r` is then contradicted, and neither route nor the proof by cases is usable. In the last .16 neither fact holds. There the proof of several statements by cases on `r` (`p :- r`, `0.9::q :- p` and `0.9::q :- -r`) gives `q` the support .9 × .9 = .81. The sum is .576 + .036 + .1296 = .7416. Rules: nothing from conflict; proofs of several statements.

**5. A fact opposed by its own consequence.** Input: `p. q :- p. 0.9::-p :- q.` Question: `p`. Result: `p` (.1, 0, .9, 0) and `q` (.1, 0, 0, .9). The input `p. 0.9::-p.` alone gives the same value for `p`. In .9 of the worlds the fact, the certain rule and the uncertain rule are all in force, and `p` is in conflict. `q` has `p` as its only route. It is positive where `p` is positive and in ignorance where `p` is in conflict. Written as a normal default, `0.9::-p :- q, unless(p, 1)`, the rule yields to the fact, and `p` is (1, 0, 0, 0). Rules: step 5 of the narrowing fixes `p` in conflict; nothing from conflict.

**6. Three facts that cannot all hold.** Input: `p. q. r. -p ; -q. -q ; -r. -r ; -p.` Questions: `p`, `q` and `r`. Result: (0, 0, 1, 0) for each. Each atom is established, and a certain clause derives its complement from another atom. Rule: chain conflict.

**7. An uncertain disjunction in a cycle.** Input: `a. 0.3::-b. 0.8::-a ; b.` Question: `b`. Result: (.56, .06, .24, .14). The disjunction has one source event with confidence .8.

- Where the source event passes (.8), `b` has support 1 from `a`. `b` is in conflict where `-b` also passes (.8 × .3 = .24) and positive elsewhere (.8 × .7 = .56).
- Where the source event fails (.2), `b` is negative where `-b` passes (.2 × .3 = .06) and in ignorance elsewhere (.2 × .7 = .14).

The directed rule `0.8::b :- a` in place of the disjunction gives (.5, 0, .3, .2). The directed rule has no source event, and .8 and .3 meet on the one number of `b`. Rule: the source event of Appendix A, then the narrowing in each of the two cases.

**8. A proof by cases.** Input: `0.8::r. 0.2::-p. p :- r. q :- p. q :- -r.` Question: `q`. Result: (.84, 0, 0, .16). Classical logic proves `q` outright by cases on `r`. The semantics has this proof as a proof of several statements, with listed clause `p :- r`. In .64 of the worlds `p` is positive, and in .04 `r` is negative; `q` is positive in both. In .16 neither fact holds, and the proof by cases makes `q` positive. In the last .16 both `r` and `p` are in conflict. The listed clause `p :- r` is then contradicted, the proof by cases does not apply, and `q` is in ignorance. Rules: proofs of several statements; nothing from conflict.

#### Normal defaults in a cycle across signs

**9. A normal default meets a certain rule.** Input:

```prolog
bird(p).
0.8::penguin(p).
0.9::flies(X) :- bird(X), unless(-flies(X), 2).
-flies(X) :- penguin(X).
```

Question: `flies(p)`. Result: (.18, .8, 0, .02). In .8 of the worlds `penguin(p)` is positive, and `-flies(p)` follows by the certain rule. That evidence is ordinary, so the normal default yields. In the other .2 the normal default holds with .9. Rule: ordinary first.

Without that rule the normal default, where it passes, would give `-penguin(p)` by the certain rule read backwards. `penguin(p)` would be in conflict in .8 × .9 = .72 of the worlds, and the result would be (.9, .08, 0, .02). This second value is a hand calculation. No version of the reference tool computes it.

**10. A fact, a normal default and a certain rule.** Input: `0.5::r. 0.9::p :- unless(-p, 1). -r :- p.` Questions: `r` and `p`. Result: `r` (.5, .45, 0, .05) and `p` (.45, .5, 0, .05). The certain rule also gives `-p` from `r`. Where `r` passes, `-p` follows and the normal default yields. Where `r` fails, the normal default holds in .9 and gives `-r`. Rule: ordinary first.

**11. The ordinary evidence is fixed before the defaults.** Input: `0.8::p. 0.9::q :- p, unless(-q, 1). 0.8::-p :- q.` Question: `p`. Result: (.8, 0, 0, .2). The fact fixes `p` positive before the normal default for `q` is considered. The rule `0.8::-p :- q` is present only where that default holds, and it cannot change the fixed state. Rule: ordinary first.

#### Symmetric situations

**12. A mutual pair of defaults.** Input: `p(a) :- unless(b(a)). b(a) :- unless(p(a)).` Questions: `p(a)` and `b(a)`. Result: (0, 0, 0, 1) for both. Each rule applies when the head of the other rule is not usable. The group has exception literals, so the narrowing evaluates it, and it finds neither atom sure. The group has no cycle across signs, so both atoms are in ignorance. With confidence .5 on both rules, `p(a)` is (.25, 0, 0, .75): it is positive where its rule passes and the other rule fails. Rule: undecided in the narrowing.

**13. The Yale shooting.** Input:

```prolog
alive(s0).  loaded(s0).  result(s0,s1).  result(s1,s2).  happens(shoot,s1).
alive(S2) :- alive(S1), result(S1,S2), unless(-alive(S2), 1).
loaded(S2) :- loaded(S1), result(S1,S2), unless(-loaded(S2), 1).
-alive(S2) :- happens(shoot,S1), loaded(S1), result(S1,S2).
```

Question: `alive(s2)`. Result: no value in every world, (0, 0, 0, 0; 1). The last rule is certain, so it also gives `-loaded(s1)` from `alive(s2)`. The atoms `alive(s2)` and `loaded(s1)` form one group with a cycle across signs. The input has two consistent accounts. In one the gun stays loaded and the shot kills. In the other the person stays alive and the gun was unloaded. The two inertia defaults have the same rank. Each faces a possible ordinary application against it, so neither atom becomes sure, and both literals of both atoms stay possible. Rule: no value.

With the last rule at confidence .99 the rule is directed, and `alive(s2)` is (.01, .99, 0, 0).

Three additions show how other atoms depend on `alive(s2)`.

| added clauses | question | result | reason |
|---|---|---|---|
| `q. 0.9::q :- alive(s2).` | `q` | (1, 0, 0, 0) | the fact makes `q` sure, whatever `alive(s2)` is |
| `walks(s2) :- alive(s2).` | `walks(s2)` | no value in every world | its only route needs the atom without a value |
| `buried(s2) :- unless(alive(s2)).` | `buried(s2)` | no value in every world | the exception may or may not block |

### O13 Agreement with the tool

Folder: [`O13_conformance`](O13_conformance/README.md).

gk's exact method and default against the tool, which computes the semantics directly by its definition. The
questions come from two generated sets of small inputs, the collection of part O2 and the benchmark families of
part O3. The folder also holds two further checks: gk's two evaluators on the tool's own lists of applications,
and the atoms on which the general method misses evidence that the tool finds. Two sections of their own hold
the check on new inputs that Section 7.4 reports. "Further questions on new inputs" has 225,102 questions on
inputs generated with new seeds, at the stored settings and larger, with the seeds and the list of inputs left
out as repeats. "Pairs with function terms" has 5,000 pairs of an input with function terms and an equivalent
input without them. The script [`tools/make_questions.py`](tools/make_questions.py) writes the question files from the inputs. The
section "The general method by time limit" has the general method's answers at 1 s and 10 s on the questions
of the missed-evidence check. Sections 7.4 and 7.6 use this
part.

### O14 Routes

Folder: [`O14_routes`](O14_routes/README.md).

Four families of route queries, 5 to 200 links, and the counts that show how much of a full grounding the exact
method forms: the number of ground statements of gk, the full grounding and the instances that clingo's grounder
writes. gk answers each route under the exact method, the exact method with a full grounding first
(`-exact -ground-first`) and the general method; ProbLog computes the same routes. The folder also counts the
ground statements on the university base and the grids of part O3. Sections 7.1, 7.2, 7.3, 7.5 and 7.6 use this
part.

### O15 A contradiction in a large base

Folder: [`O15_contradiction`](O15_contradiction/README.md).

The smallest and the largest university base of part O3, each with its four queries, in two variants. Variant
(a) adds two certain facts that contradict each other about a new individual that no query mentions. Variant (b)
adds the negation of a fact whose predicate occurs in no rule. Section 7.2 and the table of the three methods in
Section 7.6 use this part.

### O16 Function terms

Folder: [`O16_function_terms`](O16_function_terms/README.md).

The delivery plans with function terms on gk and on the other systems, the delivery inputs written without
function terms against the tool, and the count of complete answers of the exact method on inputs with function
terms.

### O17 BoardgameQA

Folder: [`O17_boardgameqa`](O17_boardgameqa/README.md).

The BoardgameQA benchmark (Kazemi et al., NeurIPS 2023): the 3,000 test examples of the three main sets,
converted by a script from the release's own formal form, without a language model. gk answers every example
under the default; the label of the release is the target. A second input per example adds confidences; the tool
computes the first examples of each set. Section 7.1 uses this part.

### O18 Lifschitz's problems

Folder: [`O18_lifschitz`](O18_lifschitz/README.md).

The problems A1 to A6 of Lifschitz's benchmark problems for formal nonmonotonic reasoning (1989), with their 7
published conclusions. gk answers each conclusion under the exact method, the general method and the default,
and the tool computes the inputs that it accepts. Sections 7.1 and 7.5 use this part.

### O19 Defeasible logic

Folder: [`O19_defeasible_logic`](O19_defeasible_logic/README.md).

33 theories of defeasible logic in six families: a chain of defeasible rules, a chain of strict rules, trees, a
cascade with equal ranks, a cascade with priorities, and a disputed family. Each theory is written for gk, for
SPINdle and for DEFT, and every system gets the same signed question. Sections 7.1, 7.5 and 7.6 use this part.

### O20 Outside both classes

Folder: [`O20_outside_classes`](O20_outside_classes/README.md).

Inputs outside both classes of the exact method on which it matches rule bodies against facts: K links of .9,
reach rules, a disjunction and D facts with constants that the question does not need. The calculated value is
.9^K. gk answers each input under the exact method, the exact method with a full grounding first, the general
method and the default; the tool computes the inputs with D = 0 and D = 10. The table of the three methods in
Section 7.6 uses this part.

## O9 gk's methods in detail

The repository <https://github.com/tammet/gkreasoner>, which holds this folder, publishes gk's methods in detail.
Its documents follow each version of gk:

- [`../Doc/how_gk_works.md`](../Doc/how_gk_works.md): the exact method, the general method and the default; applications and proofs of several
  statements; the procedure of the exact method; the recursive checks, the contexts, the exclusions and the
  budget of the general method; the evaluation of the collected evidence; the guarantees and limits of an answer;
  function terms, equality, ranks and arithmetic.
- [`../Doc/recursive_output.md`](../Doc/recursive_output.md): the answer line of each method, the proofs, the status facts and the dump.
- [`../Doc/cli_reference.md`](../Doc/cli_reference.md): the options.

The version of gk that these documents describe is in [`../bin/README.md`](../bin/README.md).

## O10 The reference tool in detail

The tool is in `mcref/` of the same repository, with its command reference
[`../mcref/README.md`](../mcref/README.md). [`../Doc/mcref.md`](../Doc/mcref.md) describes what the tool computes, its exact evaluation and its sampling,
what it declines (Section 6, "What the tool declines, and its limits", with the complete list of reasons), its
output and its comparison with gk.

## O11 The complete definition

This part prints the complete definition of the support semantics. Appendix A of the paper is generated from the
same text: it keeps the examples that the text refers to and leaves out Section O11.11, the stated limits, which
Section 4.7 of the paper summarizes. This part keeps all 42 examples and the inputs of the stated limits. The
sections O11.1 to O11.10 are Sections A.1 to A.10 of the paper; Section O11.0 is Section 4.1 of the paper.

Every example has the form "statements, then `Values:`". A value is four numbers: the share of worlds in which the
atom is positive, negative, in conflict, in ignorance. Where some worlds give the atom no value, their share is
written after a semicolon: (.52, 0, 0, 0; .48). The values are those of the tool's exact evaluation; mcref 1.3.1 gives every stated value of this part (90 values in 53 inputs), and gk 1.3.2 gives the same values
under the default and under the exact method, each answer complete.

The small examples of Sections 1 and 4 to 6 of the paper, each with its stated value, gk's answer and the tool's
value, are in archive folder [`O11_text_examples`](O11_text_examples/README.md).

### O11.0 The principles

These principles are the basis of the definition.

1. Simple cases give intuitive results; the plain penguin and its variants are
   critical.
2. The classical truth dominates. Proofs without exceptions are accepted first, and
   everything with an exception must accept them. A blocked rule cannot undo the
   evidence that blocked it. A rule is restored where its exception ends in conflict.
3. Only a proof that contains the question clause is acceptable. A contradiction
   somewhere in the input proves nothing about other atoms.
4. A premise that a proof establishes and uses must be usable.
5. A rule with an exception that is not blocked is evidence like any other, also
   against a certain fact.
6. One number per atom; each uncertain statement counts once.
7. Classical agreement: on a consistent input of certain clauses without exceptions,
   an atom that follows gets (1, 0, 0, 0), an atom whose negation follows gets
   (0, 1, 0, 0), any other atom (0, 0, 0, 1).
8. Nested classes: a small class of inputs has the values of ProbLog and similar
   systems; a wider class is a Bayesian network; outside them the values are decided
   by thinking through examples.
9. Evidence against a clause in a proof discards the proof. Evidence against the
   goal itself is opposition.
10. Uncertain rules and rules with exceptions work only in their written direction. A
    certain rule without an exception works in every direction; its spelling does not
    change its meaning. A default written without a head has the literal that its
    exception opposes as its head.
11. An exception is judged before the rule it guards, also when the exception is
    itself a default conclusion.

Principle 2 is read together with principle 5. The exception pass (Section O11.9) uses
the evidence of the lower layers to decide which rules to remove. It does not fix the
state of every atom of those layers: a rule that is not removed can still oppose it.

Three consequences that the examples below show:

- *Direction is necessary.* `bird(a). 0.9::flies(X) :- bird(X). -flies(a).` must keep
  `bird(a)` certain. If the uncertain rule worked backwards, the fact `-flies(a)`
  would become evidence against `bird(a)` (Example 3).
- *Classical proofs come first.* `p ; r. q :- p. q :- r.` gives `q` although no single
  statement concludes it (Example 6).
- *An exception that cannot hold is dropped.* In `p ; -f :- unless(x). p ; f.` no
  statement can conclude `x`, so the exception never blocks. `p` has the value of the
  same input without the exception (Example 5). This holds for every input without a
  cycle. In a cycle an exception that never holds can change a value through the
  order of the exception pass (Section O11.11).

### O11.1 Terms

- An **atom** is a predicate applied to arguments, such as `flies(t)`. It is **ground**
  when it has no variables. A **literal** is an atom or its negation. The **opposite**
  of a literal is the same atom with the other sign.
- A **statement** is one input fact, rule or disjunction, with its **confidence** (the
  number written on it; 1 when none is written), its **written head** if it has one,
  and its **exception literals** if it has any. A statement is **certain** when its
  confidence is 1 and **uncertain** otherwise. A confidence is written on an input
  statement. A **strength** belongs to an application or to a side and is computed.
- `p :- f.` and `f => p` have the written head `p`. `p ; -f.` has no written head.
- **The head of a default whose consequent is a disjunction**. The **consequent** of a statement is what stands left of `:-` or right of
  `=>`; a statement written as a plain list of literals is all consequent. Take a
  statement with an exception literal whose consequent has several literals. If one
  literal L of the consequent is the opposite of the exception literal, L is its head,
  and from here on the statement counts as a statement with the written head L.
  `flies(X) ; -bird(X) :- unless(-flies(X)).` is read as
  `flies(X) :- bird(X), unless(-flies(X)).` The test is made on the statement as
  written, before grounding. If no literal of the consequent passes it, the statement
  remains without a written head: `p ; -f :- unless(x).` (A statement with several
  exception literals of which more than one has such a literal also stays without a
  written head.)
- An exception literal is written `unless(E)`, `unless(E, k)` or `$block(k, E)`, with a
  **rank** k, an integer of 0 or more. `unless(E)` has rank 0.
- The **clause** of a statement is the disjunction of its literals without its
  exception literals: the clause of `p :- f, unless(x).` is `p ; -f`.

### O11.2 Grounding

Let D be the set of constants of the input, the question's constants included. Every
variable of a statement's ordinary literals is replaced by a constant of D, in every
combination. A repeated variable gets the same constant in each place.

- A variable that occurs only in exception literals is not instantiated per statement.
  All its instances are exceptions of the one ground statement.
- A built-in condition such as `X < 10` is computed after instantiation. A true
  condition is dropped. A false one drops the ground statement.
- A statement with confidence 0 is excluded. It gives no support and no application,
  so it takes no part in deciding the kind or the rank of a side (Example 5a).
- Two statements with the same text are two statements: the position in the input
  identifies a statement. One statement instantiated twice with the same constants is
  one ground statement. Two different choices of constants for the ordinary variables
  of one statement are two ground statements, also when they give the same clause
  (Example 5e).
- **The order of the steps.** First the written head of a statement, if it has one, is
  read on the statement as written (Section O11.1). Then the statement is instantiated.
  In each ground statement a literal that occurs several times in the clause counts
  once; a body literal that is the opposite of the head is the head literal again.
  Only then is the ground statement classified (Section O11.3). When one literal is
  left, the ground statement is a fact of that literal with the statement's
  confidence, also when the statement was written with several literals or as a rule:
  it has no event and no rule identity. A rule has a body literal only when a literal
  other than its head is left. The ground statement keeps its exception literals. With
  the one constant `a`, `0.5::p(a) ; p(X).` is the fact `0.5::p(a).`, and so is
  `0.5::p(a) :- -p(X).`; with `0.5::-p(a).` either gives `p(a)` (0, 0, .5, .5), where an
  event of its own would give (.25, .25, .25, .25).
- Constants are typed: the integer `1`, the real `1.0` and the string `"1"` differ.
- A ground statement whose clause contains a literal and its opposite takes no part in
  a proof of several statements (Section O11.4). Its single applications remain.

From here on, "statement" means a ground statement.

### O11.3 The kinds of statement and their single uses

| kind | example | how it is used |
|---|---|---|
| certain clause | `p ; r.`, `q :- p.`, `p.` | in every direction |
| uncertain fact | `0.8::p.` | evidence at its atom |
| uncertain clause with several literals and no written head | `0.8::p ; r.` | in every direction; it holds or fails as one **event**, shared by all its uses |
| uncertain rule (written head) | `0.9::flies(a) :- bird(a).` | only towards its head; its confidence counts at its head |
| rule with an exception (written head) | `flies(a) :- bird(a), unless(penguin(a)).` | only towards its head; the exception is kept |
| clause with an exception and no written head | `p ; -f :- unless(x).` | in every direction; the exception is kept |

Only a written head gives a direction, and only on a statement that is uncertain or
has an exception. A certain rule without an exception is a certain clause. A head
read from a default (Section O11.1) is a written head.

A subclass:
an input **has heads on its exceptions** when every statement with an exception has a
head: its consequent is a single literal, or its consequent is a disjunction and the
head is read as in Section O11.1. The definition also covers statements outside this subclass. Results that require heads
on exceptions state that assumption explicitly. The last row of the table is for
statements outside the subclass.

An **application** is a standing possibility to conclude one literal. It has a
**head**, the literal it concludes; **body literals**, which must be usable; exception
literals, which must not be usable; **listed clauses**, which must not be contradicted
(only proofs of several statements have them, Section O11.4); a **strength** in [0, 1];
and, when it uses uncertain rules, their identities.

**The identity of an uncertain rule.** An uncertain rule with a written head and at
least one body literal (counted as Section O11.2 says, "The order of the steps") has an identity, also when it is a normal default. Its single
application has that identity, and so has every proof that uses the rule
(Section O11.4). A rule that is used in several applications is one rule: it holds or
fails once (Section O11.6, the strength of a side). A fact, and a rule without a body
literal such as `0.5::a :- unless(-a).`, have no identity: their uncertainty is a
strength only.

The **single applications** of a statement:

| statement | applications |
|---|---|
| a fact L | head L, empty body, the fact's confidence |
| a rule with a written head H that is uncertain or has an exception | head H, body the opposites of its other literals, the rule's confidence (**directed**) |
| a certain clause | one application per literal L: head L, body the opposites of the other literals, strength 1 |
| an uncertain clause with several literals and no written head, confidence c | an event s: a new atom for this ground statement alone, with one fact of confidence c; one application per literal as in the row above, with s added to its body, strength 1. Every use of the statement refers to that one atom |
| a clause with an exception and no written head | as the two rows above, certain or uncertain; each application has the exception literals |

Every application of a statement has the statement's exception literals. An exception
literal that is written several times counts once, with the largest of its ranks. For
each application:

- If the opposite of the head is among the exception literals, the application is a
  **normal default**, and the rank of that literal is the application's **rank**. That
  literal is not used in the test whether the application applies; the table of
  Section O11.6 handles the opposite evidence.
- Every other exception literal is **external**. An application that is not a normal
  default is **ordinary**.

The test is made per application. One direction of a clause without a written head can
be a normal default while another direction is not.

An application with an external exception literal that is also one of its body
literals never applies and is excluded.

**A rule that blocks itself is excluded.** After grounding, and after the instances of
a variable that occurs only in exception literals are collected, a rule with a written
head is excluded when the same signed literal is one of its body literals and one of
its external exception literals. This is done once, before the single applications are
formed and before proofs of several statements are built, so the rule takes part in
none (Example 9c). It is a different test from the one for a clause with a literal and
its opposite (Section O11.2), which keeps its single applications. A statement without a written head is
not excluded: one of its directions can still apply (Example 9d).

**Example 1.** A certain rule and an uncertain rule.

```
0.8::bird(t).
0.9::flies(X) :- bird(X).
```
Values: `flies(t)` (.72, 0, 0, .28), `bird(t)` (.8, 0, 0, .2).

**Example 2.** A certain rule works in every direction.

```
flies(X) :- bird(X).
-flies(a).
```
Values: `bird(a)` (0, 1, 0, 0).

**Example 3.** An uncertain rule works only towards its head.

```
bird(a).
0.9::flies(X) :- bird(X).
-flies(a).
```
Values: `bird(a)` (1, 0, 0, 0), `flies(a)` (0, .1, .9, 0).

**Example 3a.** The head is read from a default. Nothing says that `os` is a bird. Both
defaults are written without a head; each has an exception that is the opposite of one
of its literals, so `flies(X)` is the head of the first and `-flies(X)` of the second.
Without the reading both would work in every direction, and a proof by cases on
`flies(os)` would give `bird(os)` (0, 1, 0, 0).

```
ostrich(os).
-bird(X) ; object(X).
flies(X) ; -bird(X) :- unless(-flies(X)).
-flies(X) ; -object(X) :- unless(flies(X)).
```
Values: `bird(os)` (0, 0, 0, 1), `flies(os)` (0, 0, 0, 1).

**Example 4.** An uncertain clause without a written head holds or fails as one event.

```
0.8::p ; r.
-r.
```
Values: `p` (.8, 0, 0, .2), `r` (0, 1, 0, 0).

**Example 5a.** A statement with confidence 0 is excluded. If it stayed, the side for
`p` would be ordinary, and the value would be (.2, 0, .6, .2).

```
0.0::p.
0.8::p :- unless(-p, 1).
0.6::-p.
```
Values: `p` (.32, .6, 0, .08).

### O11.4 Proofs of several statements

A consequence that needs several statements at once, such as a proof by cases, is
evidence too.

**A proof of a literal Q** is a pair (L, G). L is a set of statements. G is a set of
single literals, the **premises**. Neither Q nor its opposite is in G. The conditions:

1. the clauses of L together with G imply Q classically;
2. the clauses of L together with G are consistent;
3. no statement can be excluded of L and no literal out of G: no smaller L with the
   same G, and no smaller G with the same L, still implies Q;
4. every statement in L with a written head that is uncertain or has an exception has
   the signed literal Q as its head.

A fact `Q.` is the proof ({`Q.`}, {}). A single application is the proof with one
statement; it keeps the strength and the kind that Section O11.3 gives it. The
construction below adds the applications of the proofs that use several statements,
each with two or more literals. A fact enters such a proof as a premise: its literal is
in G, and its confidence counts at its own atom (Example 5b). The order of derivation
steps does not matter: two derivations with the same pair are the same proof.

The premises are not proved inside the proof. Each premise is evidence-tested at its
own atom. In `p. 0.8::q :- p. s :- q.` the proof of `s` is ({`s :- q.`}, {`q`}). The
uncertain rule is not in it, by condition 4, so its confidence counts once, at `q`.
For the certain chain `p. q :- p. s :- q.`, the two-rule proof with premise `p`
produces body {`p`, `q`} and lists the non-goal clause `q :- p`; the single
application of `s :- q` requires only `q`, has no listed clause or exceptions,
and is certain and ordinary, so it absorbs the combined application (compare
Example 9d for a case in which the single application does not absorb the proof).

A clause without a written head may take part in any proof, whether or not it has a
confidence or an exception. An uncertain one, with clause C and event s, is read in the
proof as the clause "not s, or C", so the proof has s as a premise. The event is never
the goal of a proof. Where the proof lists the clause (below), it lists C itself.

The **non-goal clauses** of a proof are the clauses of L that do not contain Q.

**The application of a proof (L, G) of Q** has:

- head Q;
- body: every single literal that G and the non-goal clauses imply (the literals of G
  among them);
- exception literals: those of every statement in L. The opposite of Q on a normal
  default of Q is the mark of a normal default, not an external exception of the proof;
- listed clauses: the non-goal clauses with several literals;
- the identities of the uncertain rules of L, and as strength the product of their
  confidences;
- kind: when L holds normal defaults of Q, the application is a normal default, and its
  rank is the smallest of their ranks. An uncertain normal default takes part like a
  certain one, with its identity (Examples 9a and 9b). Otherwise the application is
  ordinary. An exception of
  a clause without a written head remains an external exception of the proof, also when
  it is the opposite of Q; it never makes the proof a normal default. The kind of the
  proof is decided by its rules with a written head alone: with a normal default of Q
  among them the proof is a normal default of their smallest rank, and it still has
  that external exception; without one it is ordinary. The single application of such
  a clause towards Q is a normal default (Section O11.3). It does not absorb an
  ordinary proof that uses the clause (Example 9d).

An application with an exception literal that is also one of its body literals never
applies and is excluded.

**A redundant proof is dropped.** The application of a proof of Q is excluded when
another application of Q requires no more: the body literals, the exception literals,
the listed clauses and the uncertain rules of the other are all among those of the
first. The other application must be certain, or have its uncertainty in a body literal
(an event) or in the identities of its uncertain rules. An application whose
uncertainty is a strength only absorbs nothing: an uncertain fact, and an uncertain
rule without a body literal (Example 5c). An application that is a normal default absorbs only a normal default of
the same rank. Of several applications with equal requirements, kind and rank, one is
kept.

**A rule whose body can never hold is ignored.** After the proofs are built: start
with the heads of the applications without a body; add the head of an application when
all its body literals have been added; exception literals, listed clauses and opposing
evidence are ignored. An application that needs a literal outside this set is
excluded. The dependencies of Section O11.7 are formed from the applications that
remain. "Can conclude" in Section O11.8 means: some remaining application has that
head.

*Lemma.* In a proof of Q no clause of L contains the opposite of Q, and every single
literal other than Q that some part of L and G implies is implied by G and the
non-goal clauses.

**A rule whose body can hold only when its head already holds is ignored**. An application with head L is excluded when one of its body literals
cannot be derived, in the sense of the paragraph above, without the applications that
have head L. The test is made once, on all applications, before the applications whose
body can never hold are excluded. A second round would exclude nothing more: an
application that is excluded never adds a literal to a derivation, because L is
derived by another application before its body can be. The rule works on applications,
so the clause notation does not matter: `d :- d.` and `d ; -d.` lose the same applications.
An abbreviation `q :- A. -q :- -A.` of an atom A keeps its two applications for `q`
and loses the two for A, when `q` has no other source.

**Example 5e.** Two choices of constants are two ground statements (Section O11.2). The
constants are `a` and `b`. With X = a the rule has the body literal `-p(a)`, the
opposite of its own head, which is the head literal again; with X = b the body literal
`-p(b)` is written twice. Both instances have the clause `p(a) ; p(b)`. They are two
ground statements with one identity each: 1 − (1 − .5)(1 − .5) = .75.

```
0.5::p(a) :- -p(b), -p(X).
-p(b).
```
Values: `p(a)` (.75, 0, 0, .25).

**Example 5d.** The last two rules say nothing new about `a`. They are a cycle: `a`
from `b`, and `b` only from `a`. The application `a` from `b` is excluded, and `a` has
the value of the first two statements alone.

```
0.5::a :- unless(-a).
0.2::-a.
0.5::a :- b.
b :- a.
```
Values: `a` (.4, .2, 0, .4), `b` (.4, 0, 0, .6).

**Example 5b.** A fact in a proof is a premise; its confidence counts once, at its atom.

```
0.4::p.
q :- p.
```
Values: `q` (.4, 0, 0, .6).

**Example 5c.** An uncertain fact does not absorb a proof by cases:
1 − (1 − .4)(1 − .8 × .6) = .688.

```
0.4::q.
0.8::q :- p.
0.6::q :- -p.
```
Values: `q` (.688, 0, 0, .312).

**Example 5.** A clause with an exception and no written head takes part in a proof.
The exception is kept.

```
p ; -f :- unless(x).
p ; f.
```
Values: `p` (1, 0, 0, 0), `f` (0, 0, 0, 1).

With `x.` added:

```
x.
p ; -f :- unless(x).
p ; f.
```
Values: `p` (0, 0, 0, 1).

**Example 6.** A proof by cases.

```
p ; r.
q :- p.
q :- r.
```
Values: `q` (1, 0, 0, 0), `p` (0, 0, 0, 1).

**Example 7.** Each uncertain rule counts once (condition 4 and the identities).

```
0.5::p.
0.8::q :- p.
0.8::q :- -p.
```
Values: `q` (.72, 0, 0, .28).

**Example 8.** An uncertain clause without a written head in a proof shares its event.

```
0.8::p ; -f.
p ; f.
0.9::q :- p.
```
Values: `p` (.8, 0, 0, .2), `q` (.72, 0, 0, .28).

**Example 9.** A normal default in a proof by cases, and ordinary evidence against it.

```
q :- a, unless(-q, 1).
q :- -a.
```
Values: `q` (1, 0, 0, 0).

```
q :- a, unless(-q, 1).
q :- -a.
0.3::-q.
```
Values: `q` (.7, .3, 0, 0).

**Example 9a.** Two uncertain normal defaults cover both cases. Nothing is known about
`bird`, so neither default applies by its own premise. The proof by cases needs both
rules: .8 × .8 = .64.

```
0.8::flies :- bird, unless(-flies).
0.8::flies :- -bird, unless(-flies).
```
Values: `flies` (.64, 0, 0, .36).

**Example 9b.** An uncertain normal default counts once. The third statement supports
`a` from the fact `d`. It also takes part in a proof by cases on `d` with the second
statement. Both applications have the identity of the one rule, so the support is .8.
Counted as two sources it would be .96.

```
d.
a :- -d, unless(f).
0.8::a :- d, unless(-a, 2).
```
Values: `a` (.8, 0, 0, .2).

**Example 9c.** A rule that blocks itself is excluded (Section O11.3). The first rule
needs `e` as a premise and has `e` as an exception. If it stayed, the two rules would
combine by cases on `e` into "`r`, no premise, unless `e`", with strength .36. It is
excluded; the second rule has no usable premise.

```
0.6::r :- e, unless(e).
0.6::r :- -e.
```
Values: `r` (0, 0, 0, 1).

**Example 9d.** A proof with one statement that holds the proved literal, which its
single application does not absorb. The first statement has no written head: neither
`p` nor `r` is the opposite of its exception `b`. Its clause is `p ; r ; -b`. Towards
`-b` its single application needs `-p` and `-r` and is a normal default, because `b`
is the opposite of that head. The first two statements with the premise `-r` are a
proof of `-b`: the second gives `-p`, and then the first gives `-b`. In the proof the
exception `b` is an ordinary exception, so the proof is ordinary. The normal default
for `b` of the last statement yields to it.

```
p ; r :- b, unless(b).
-p :- -r.
-r.
b :- unless(-b).
```
Values: `b` (0, 1, 0, 0).

### O11.5 Worlds

For every ground atom A, the events of uncertain clauses included, take two numbers U_A
and V_A. Each is uniform on [0, 1). They are independent of each other and of the
numbers of every other atom. Nothing else is random, and no number is drawn again when
an atom is used a second time. A share of worlds is a probability under these numbers. One assignment of all these numbers is a **world**.
Sections O11.6 to O11.9 give every atom a state in each world: positive, negative,
conflict or ignorance; or no state, when the atom has **no value** in that world.

### O11.6 Applicability of an application and the state of one atom

A literal is **usable** when its atom is in the state of its sign: A positive, or ¬A
negative. Conflict and ignorance make neither literal usable. A literal **has
evidence** when its atom has its sign or is in conflict.

**The check of a listed clause** has three results. The clause is **contradicted**
when the opposite of each of its literals has evidence. It is **not contradicted**
when the opposite of one of its literals certainly has no evidence: the atom of that
literal has a state without such evidence, or it has no value and no application can
conclude the opposite of the literal. Otherwise the check **cannot be decided**: no
literal certainly lacks evidence against it, and some atom of the clause has no value.

An application **applies** in a world when it has not been removed by the exception
pass (Section O11.9) and:

- **Requirement 1, usable premises.** Every body literal is usable.
- **Requirement 2, no contradicted clause.** Every listed clause is not contradicted.
  An application with a check that cannot be decided neither applies nor is absent:
  the atom of its head is evaluated by the procedure of Section O11.7, where the check
  counts as a dependency without a value (Example 16a).
- **Requirement 3, exceptions.** No external exception literal is usable.

The check of a listed clause is not an exception literal. It has no part in the layers
of Section O11.9.

Evidence against the head is not a reason to discard an application. It is opposition.

**The strength of a side.** The applications with head A that apply form the side for
A; those with head ¬A form the side against A. The strength of a side is the
probability that at least one of its applications succeeds, where a single application
succeeds with its strength, a proof succeeds when all its uncertain rules succeed, each
uncertain rule succeeds with its confidence independently of the others, and a rule
used in several proofs is one rule. For applications that share no rule this is
1 − ∏ (1 − c). In general it is 1 − ∏ (1 − c_i) × (1 − p), with the product over the
applications without identities and p the probability that at least one of the others
has all its rules. This probability is a calculation of the strength. It adds no random
number to the world.

A side that is not empty is **normal** when every application in it is a normal
default, and **ordinary** when at least one is not. The kind is decided in each world. The rank of
a normal side is the largest rank among its applications.

With a the strength of the side for A, b that of the side against A, and U, V the two
numbers of A:

| sides that apply | state |
|---|---|
| none | ignorance |
| for only | positive if U < a; else ignorance |
| against only | negative if U < b; else ignorance |
| both ordinary | positive if b ≤ U < a; negative if a ≤ U < b; conflict if U < min(a, b); else ignorance |
| for normal, against ordinary | negative if U < b; else positive if V < a; else ignorance |
| for ordinary, against normal | positive if U < a; else negative if V < b; else ignorance |
| both normal, equal ranks or a rank 0 | P = (U < a), N = (V < b): positive if P and not N; negative if N and not P; else ignorance |
| both normal, higher rank for | positive if U < a; else negative if U < b; else ignorance |
| both normal, higher rank against | negative if U < b; else positive if U < a; else ignorance |

**Example 10.** Two ordinary sides share the number U.

```
0.8::p.
0.3::-p.
```
Values: `p` (.5, 0, .3, .2).

**Example 11.** A normal default yields to ordinary evidence.

```
bird(t).
0.3::-flies(t).
0.9::flies(X) :- bird(X), unless(-flies(X), 2).
```
Values: `flies(t)` (.63, .3, 0, .07).

**Example 12.** Two normal defaults of equal rank block each other; a higher rank wins.

```
quaker(n).
republican(n).
0.8::pacifist(X) :- quaker(X), unless(-pacifist(X), 1).
0.6::-pacifist(X) :- republican(X), unless(pacifist(X), 1).
```
Values: `pacifist(n)` (.32, .12, 0, .56).

```
quaker(n).
republican(n).
pacifist(X) :- quaker(X), unless(-pacifist(X), 2).
-pacifist(X) :- republican(X), unless(pacifist(X), 1).
```
Values: `pacifist(n)` (1, 0, 0, 0).

**Example 13.** Requirement 1: a premise in conflict is not usable.

```
p ; r.
p ; -r.
-p.
q :- p.
```
Values: `p` (0, 0, 1, 0), `q` (0, 0, 0, 1).

**Example 14.** Requirement 2: a contradicted clause discards the proof.

```
p ; r.
-p.
-r.
q :- p.
q :- r.
```
Values: `q` (0, 0, 0, 1).

**Example 15.** Requirement 2 in a part of the worlds.

```
0.8::r.
0.2::-p.
p :- r.
0.9::q :- p.
0.9::q :- -r.
```
Values: `q` (.7416, 0, 0, .2584).

**Example 16.** A proof without a non-goal clause applies also on a contradiction.

```
p.
-p.
q :- p.
q :- -p.
```
Values: `q` (1, 0, 0, 0), `p` (0, 0, 1, 0).

**Example 16a.** A check that cannot be decided outside a cycle. `p` and `w` have no
value; `-p` can be concluded; `c` is in conflict. So the check of `p ; c` cannot be
decided, and `q` has no value.

```
p :- unless(-p).
w :- unless(-w).
-p :- w.
c.
-c.
p ; c.
q :- p.
q :- c.
```
Values: `q` (0, 0, 0, 0; 1), `c` (0, 0, 1, 0).

### O11.7 Evaluation order and groups of atoms

**Dependency.** Atom A depends on every atom in the body literals, the external
exception literals and the listed clauses of the applications with head A or ¬A that
remain after Section O11.4. The
**groups** are the strongly connected components of this relation; an atom that is in
no dependency cycle forms a group of its own. In each world the groups are evaluated in the
order of the dependency, each after every group it depends on.

A group has a **cycle across signs** when an application whose head is a literal of
the group has a body literal in the group of the other sign, or when two applications
with body literals in the group have heads of opposite signs in the group. Exception
literals and facts do not count.

**Sweep groups.** A group G is a sweep group when

1. G has no cycle across signs;
2. no application of G has an exception literal whose atom is in G; the opposite of
   its own head on a normal default does not count;
3. no application of G is a normal default;
4. no atom outside G that G depends on is without a value.

```
for each group G, after every group that G depends on:
    if an application of G lists a clause with an atom in G:
        the clause rule in a cycle
    else if G depends on an atom without a value outside G,
            or an application of G lists an outside clause whose check cannot be decided:
        the procedure for G (below), whatever its form
    else if G is one atom that does not depend on itself:
        its state comes from the table of one atom
    else if G is a sweep group:
        every atom of G starts in ignorance
        repeat a sweep: compute every atom of G from the states of the sweep before,
            until a sweep changes nothing
    else if G has no cycle across signs:
        the procedure for G; an atom it leaves without a value is in ignorance
    else:
        the procedure for G
```

**The narrowing**, for a given set of applications of G. Literals of the atoms outside
G are read from their final states. For a literal L of G, an application for L has
head L, and an application against L has the opposite of L as its head. The **base**
literals are the usable literals of the outside atoms that G depends on and the
usable literal of every atom of G that the procedure below has fixed positive or
negative; an atom fixed in conflict and an outside atom without a value give nothing.
The check of a listed clause whose atoms are outside G is read from their final
states: an application with a contradicted check is excluded; a check that cannot be
decided is treated as an exception literal on an outside atom without a value.

1. Sure is the base literals. Possible is the base literals, both literals of every
   atom of G that is not fixed, and both literals of every outside atom without a
   value.
2. New sure: start from the base literals and repeatedly add a literal L of an atom
   that is not fixed when Section O11.6 gives L's atom the sign of L, counting the
   applications for L whose body literals are all in the set being built and whose
   exception literals are all outside the old possible set, and the applications
   against L whose body literals are all in the old possible set and whose exception
   literals are all outside the old sure set. Stop when nothing more can be added.
3. New possible: start from the base literals and both literals of every outside atom
   without a value, and repeatedly add a literal L of an atom of G that is not fixed
   when Section O11.6 gives L's atom the sign of L, counting the applications for L
   whose body literals are all in the set being built and whose exception literals are
   all outside the new sure set, and the applications against L whose body literals
   are all in the new sure set and whose exception literals are all outside the old
   possible set.
4. If neither set changed, go to step 5. Otherwise take the new sets as the old ones
   and repeat from step 2. Sure only grows, possible only shrinks, and sure stays
   inside possible.
5. Every atom that is not fixed and has no literal in sure, whose table gives conflict
   when both sides count their applications with body literals in possible and no
   exception literal in sure, is **fixed** in conflict. If any atom was fixed in this
   step, remove its literals from both sets and repeat from step 1 with the fixed
   atoms excluded.

A fact, or an application whose body literals are all base literals, has its body test
met in both computations, since nothing in G can remove it. Its exception literals and
its listed clauses are still tested.

**Selections.** When the atom of L has applications that are normal defaults,
"Section O11.6 gives the sign" is decided over selections of applications. For one
side, write C(B, E) for its applications whose body literals are all in B and whose
external exception literals are all outside E. Let S be the old sure set, P the old
possible set, X the new sure set while it is built, S' the finished new sure set, and
Y the new possible set while it is built. A selection R of a side must lie between two
sets:

| computation | side | allowed selections |
|---|---|---|
| step 2, new sure | the side of L | C(X, P) ⊆ R ⊆ C(P, S) |
| step 2, new sure | the opposing side | C(S, P) ⊆ R ⊆ C(P, S) |
| step 3, new possible | the side of L | R ⊆ C(Y, S') |
| step 3, new possible | the opposing side | C(S', P) ⊆ R ⊆ C(P, S') |

In step 2 the sign must hold for every pair of selections. In step 3 it must hold for
some pair. When the atom has no normal default, the strength of a side only grows with
its selection, so the single least favourable pair in step 2 and the single most
favourable pair in step 3 decide.

**The procedure for G.** It runs the narrowing once, or twice when G has normal
defaults.

1. If G has applications that are normal defaults, run the narrowing on the ordinary
   applications of G alone, and fix every atom that ends with a literal in sure, in
   that sign, and every atom fixed in conflict. Then run the narrowing on all
   applications, keeping the fixed atoms. Otherwise run the narrowing once, on all
   applications.
2. A fixed atom keeps its state. An atom with a literal in sure has that sign. An atom
   with neither literal in possible is in ignorance. Any other atom has **no value**;
   in a group without a cycle across signs that depends on no atom without a value,
   the list above reads it as ignorance.

**Example 17.** A sweep group: support that goes round a cycle is no support.

```
0.6::a.
b :- a.
c :- b.
b :- c.
```
Values: `b` (.6, 0, 0, .4), `c` (.6, 0, 0, .4).

**Example 18.** Two rules that block each other through ordinary exceptions.

```
a :- unless(b).
b :- unless(a).
```
Values: `a` (0, 0, 0, 1), `b` (0, 0, 0, 1).

**Example 19.** Two normal defaults on different atoms that exclude each other give
no value.

```
on(a) :- unless(-on(a)).
on(b) :- unless(-on(b)).
-on(a) ; -on(b).
```
Values: `on(a)` (0, 0, 0, 0; 1), `on(b)` (0, 0, 0, 0; 1).

### O11.8 The clause rule in a cycle

A proof by cases can establish a literal used to derive evidence against one of its listed clauses. The check of
Requirement 2 then depends on its own result. The rule, for one world and one group G
in which some application lists a clause with an atom in G:

1. Evaluate the group with no listed clause of the cycle counted as contradicted. A
   listed clause is *of the cycle* when an application whose head atom is in G lists
   it and it has an atom in G; the checks of other listed clauses keep their results.
   Premises, events and exceptions are checked as always. The atoms of G are evaluated
   in the groups they form when the checks of the cycle are taken as fixed, by the
   list of Section O11.7.
2. Collect all listed clauses that come out contradicted. If there are none, this is
   the result.
3. Leave out every proof that lists one of them, and evaluate again. Collect the
   contradicted listed clauses again, all at once.
4. If the clauses collected so far are still contradicted and no new one appeared,
   this is the result. If a new one appeared, add it and repeat step 3.
5. If a clause collected earlier is no longer contradicted, or a check cannot be
   decided, the rule has no result. This comes before step 4: it holds also when
   another clause has just become contradicted. Then an atom of the group that has had
   the same state in every evaluation of the group that the rule made keeps that
   state, and every other atom of the group has no value in this world. When the rule stops at a check that cannot be decided, one more
   evaluation is made before the comparison, with every listed clause whose check is
   open or contradicted counted as contradicted, so that both readings exist.

All checks of a round are made before any setting changes.

A listed clause of the cycle is evaluated only while one of its proofs could apply
otherwise: its body literals are usable, none of its exception literals is usable, and
no listed clause outside the cycle excludes it. The settings of the other clauses of
the cycle are ignored for this. When every proof that lists the clause is out
for another reason, the clause keeps its setting of the round before.

Only applications with head atoms in G count when deciding whether to recheck a clause
of the cycle. A setting is used only in the rounds of this invocation of the clause
rule, including evaluations of the smaller groups within G. After the rule returns, a
check outside G reads the final states of the atoms in G, including any atoms with no
value, and applies Section O11.6 using the applications remaining in the current
evaluation.

*A check that cannot be decided* is defined in Section O11.6. One literal that
certainly has no evidence against it makes the clause not contradicted, also when the
check of another literal is open.

If including the proof and omitting it would each reproduce that choice on evaluation, the
procedure starts with the proof included.

**Example 20.** The proof of `q` is excluded; the values are those of the input
without `q :- r.`

```
p ; r.
q :- p.
q :- r.
-p :- q.
-r.
```
Values: `p` (0, 0, 1, 0), `q` (0, 0, 0, 1), `r` (0, 0, 1, 0).

**Example 21.** The same with an uncertain rule.

```
p ; r.
q :- p.
q :- r.
0.9::-p :- q.
-r.
```
Values: `p` (.1, 0, .9, 0), `q` (.1, 0, 0, .9), `r` (0, .1, .9, 0).

**Example 22.** An atom without a value whose opposite no rule concludes leaves the
clause uncontradicted.

```
t.
p :- t, unless(-p, 1).
w :- t, unless(-w, 1).
-p :- w.
d :- p.
a.
-a.
a ; d.
q :- a.
q :- d.
```
Values: `q` (1, 0, 0, 0), `d` (0, 0, 0, 0; 1).

**Example 23a.** The rule has no result, and only the atoms that differ lose their
value. In the worlds where all five uncertain statements hold, the proof of `q` by
cases gives `-a` and `-b`, which contradict its clause `a ; b`; without the proof the
clause is not contradicted. `q`, `a` and `b` differ between the two rounds and have no
value there. `p` is in the same group (through `p` from `q`, and `-a` from `q` and `p`),
but it is positive in both rounds, from its fact.

```
p.
0.9::p :- q.
0.9::a ; b.
0.9::q :- a.
0.9::q :- b.
0.9::-a :- q, p.
0.9::-b :- q.
```
Values: `p` (1, 0, 0, 0), `q` (.13851, 0, 0, .271; .59049), `a` (.06561, .06561, 0, .27829; .59049).

**Example 23.** Both settings are consistent; the proof applies.

```
p ; r.
q :- p.
q :- r.
-r.
s.
0.9::-p :- s.
0.9::-s :- q.
```
Values: `q` (.91, 0, 0, .09).

### O11.9 The exception pass: layers, removal, restore

Literals and applications get **layers**. A literal and its opposite are placed
separately.

- An application without an external exception literal has layer 0, also when its
  body literals have higher layers. A normal default whose only exception literal is
  the opposite of its head has layer 0.
- An application with external exception literals has layer 1 + the highest layer of
  those literals.
- The layer of a literal is the highest layer among the applications that conclude it,
  raised to the layer of every body literal of those applications and to the layer of
  the opposite of every literal of their listed clauses. A literal that no application
  concludes has layer 0.
- The layers are the smallest numbers that meet these three rules. Where the rules
  allow no finite number (exception literals that depend on each other in a cycle,
  and everything whose layer depends on them), the layer is the **top** layer, one
  above every finite layer.

The layers are computed once, from the applications that remain after Section O11.4,
before any world is looked at.

"Evaluate with some applications temporarily excluded (held out)" means: those applications are absent.
Among the others, exclude again the applications whose body can hold only when their
head already holds and the applications whose body can never hold (Section O11.4), now
tested without the absent ones; note again which literals some remaining application
can conclude; form the groups again from the dependencies of what remains; and compute
every state anew with the same numbers U and V. No state of an earlier evaluation is
kept. The same holds for an application that was removed: a removed rule is absent,
and what could be derived only through it can no longer be derived. The layers alone are not computed again: they fix the order of the
passes.

In each world:

1. For s = 1, 2, ... up to the top layer: evaluate (Sections O11.6 to O11.8) with the
   applications of layer s and above held out, and those removed before. Remove every
   application of layer s that has an external exception literal usable in that
   evaluation.
2. Evaluate all applications that are not removed.
3. Restore every removed application for which none of the exception literals that
   caused its removal is usable in the result of step 2, all such applications
   at once. If one was restored, repeat step 2. A restored application is not removed
   again. It is an application like any other: its body literals, its exception
   literals and its listed clauses are tested in the next evaluation.

The states of the last run of step 2 are the states of the world.

What the pass does:

- A rule is blocked where the evidence of the lower layers makes its exception usable.
  The consequences of the blocked rule cannot be used against the exception.
- A rule with an exception that is not removed counts like any other application.
- A rule comes back when other evidence has taken the support from its exception.

**Example 24.** The plain penguin.

```
bird(a).
penguin(a).
flies(X) :- bird(X), unless(penguin(X)).
-flies(X) :- penguin(X).
```
Values: `flies(a)` (0, 1, 0, 0), `penguin(a)` (1, 0, 0, 0).

**Example 25.** A rule with an exception that is not blocked meets a certain fact.

```
bird(a).
-flies(a).
flies(X) :- bird(X), unless(injured(X)).
```
Values: `flies(a)` (0, 0, 1, 0).

**Example 26.** Two layers: the exception is itself a default conclusion.

```
bird(a).
zoo(a).
penguin(X) :- zoo(X), unless(tropical(X)).
flies(X) :- bird(X), unless(penguin(X)).
-flies(X) :- penguin(X).
```
Values: `penguin(a)` (1, 0, 0, 0), `flies(a)` (0, 1, 0, 0).

**Example 26a.** Three layers.

```
a :- unless(b).
b :- unless(c).
c :- unless(d).
```
Values: `a` (1, 0, 0, 0), `b` (0, 0, 0, 1), `c` (1, 0, 0, 0).

**Example 26b.** A restored rule. `e` removes the rule for `p`. The rule against `e`
is not removed and puts `e` in conflict. The rule for `p` comes back.

```
e.
p :- unless(e).
-e :- unless(z).
```
Values: `p` (1, 0, 0, 0), `e` (0, 0, 1, 0).

**Example 26c.** A blocked rule cannot change a certain fact. The rule
`-q :- unless(e).` is removed, because `e` holds. Without it `-m` cannot be derived,
so the rule against `c` is excluded. The values are those of the input without the
blocked rule.

```
c.
e.
q :- m.
m :- unless(q).
-q :- unless(e).
-c :- -m, unless(z).
```
Values: `c` (1, 0, 0, 0), `m` (0, 0, 0, 1), `q` (0, 0, 0, 1).

**Example 27.** An uncertain exception.

```
0.3::e.
q :- p, unless(e).
q :- -p.
```
Values: `q` (.7, 0, 0, .3).

### O11.10 The report

For a ground question literal Q with atom A, the report is

    R(Q) = (P[A positive], P[A negative], P[A conflict], P[A ignorance])

where P is the share of worlds. Positive and negative are exchanged when Q is ¬A. The
share of worlds in which A has no value is reported beside the four numbers. The four
numbers sum to 1 minus that share, and they are not scaled up. A question with
variables gets one report for each ground instance over D, from the same worlds. An
instance whose atom is the head of no application has (0, 0, 0, 1); the reference tool
does not print such a row.

### O11.11 Stated limits

- **No rank rule across atoms.** Competing defaults on different atoms keep no value,
  also when their ranks differ.

```
a.
p :- a, unless(-p, 1).
q :- a, unless(-q, 2).
-p :- q.
```
Values: `p` (0, 0, 0, 0; 1), `q` (0, 0, 0, 0; 1).

- **A proof by cases whose normal defaults have different ranks** counts with the
  smallest of them.
- **Confidence 1 turns a written rule from directed into a certain clause.** Values
  need not be continuous at 1 (Examples 2 and 3).
- **A jump at confidence 1 in one example.** With two certain rules, the rules are
  clauses, they prove `-a`, and `e` loses its premise:

```
a.
e :- a.
-e :- a.
```
Values: `e` (0, 0, 0, 1), `a` (0, 0, 1, 0).

  With both rules at .99 the rules are directed, `a` stays certain, and `e` is in
  conflict:

```
a.
0.99::e :- a.
0.99::-e :- a.
```
Values: `e` (0, 0, .99, .01), `a` (1, 0, 0, 0).

- **Adding a clause that already follows from the input** can change a value on a
  contradictory input.
- **An abbreviation of an atom without a value shows conflict.** A rule that says
  nothing new changes no other atom (Section O11.4). But the abbreviation `q` itself is
  fixed in conflict by step 5 of the narrowing, where `on(a)` has no value:

```
on(a) :- unless(-on(a)).
on(b) :- unless(-on(b)).
-on(a) ; -on(b).
q :- on(a).
-q :- -on(a).
```
Values: `on(a)` (0, 0, 0, 0; 1), `on(b)` (0, 0, 0, 0; 1), `q` (0, 0, 1, 0).

- **Two rules that can never apply together can give conflict** when the atom they
  read has no value. Step 5 of the narrowing counts every application whose body is
  possible. Here one rule for `d` needs `p` and the other needs `-p`:

```
p :- unless(-p).
w :- unless(-w).
-p :- w.
0.8::d :- p.
0.8::-d :- -p.
```
Values: `d` (0, 0, .8, .2), `p` (0, 0, 0, 0; 1).

- **An atom fixed in the first stage of the procedure for a group stays**, also when
  its exception holds after the second stage. The first stage uses the ordinary
  applications alone and fixes `-c`; the second stage adds the normal default and gives
  `d`, the exception of the rule for `-c`:

```
d :- -c, unless(-d, 2).
-c :- unless(d).
```
Values: `c` (0, 1, 0, 0), `d` (1, 0, 0, 0).

- **An exception that can never hold can change a value in a cycle.** It gives its
  rule a layer, and the layer decides when the pass judges other exceptions. With
  `0.5::a.` in place of the first statement, `a` is (.375, .25, .125, .25):

```
0.5::a :- unless(fresh).
b.
e.
0.5::-b :- a.
0.5::-e :- b.
-a :- unless(e).
```
Values: `a` (.25, .25, .25, .25), `e` (.5, 0, .5, 0).

- **A rule that is removed in every world can still change a value.** The layers are
  computed once, from all applications. The rule `e :- unless(t).` is removed in every
  world, but it gives `e` a layer, and so the rule for `-a` is judged later. Without
  `e :- unless(t).`, `a` is (.225, .275, .275, .225). `t` keeps its value.

```
t.
e :- unless(t).
0.5::a :- unless(z).
0.9::b.
0.9::e.
0.5::-b :- a.
0.5::-e :- b.
-a :- unless(e).
```
Values: `a` (.35, .275, .15, .225), `t` (1, 0, 0, 0).

- Equality, function symbols, taxonomy priorities and gk's rank contexts have no rule
  in this text. The procedures are stated for finite ground inputs.
- The definition has no limit of time or size. The reference tool has a limit on its
  search for proofs and reports when it is reached; its values are then not the
  values of this text.

## O12 Details of gk's output and limits

This part gives the details of gk 1.3.2 that Section 6 of the paper refers to: the schedule and the checkpoints of
the general method, rank contexts and taxonomy priorities, one proof in full, the limits of the exact method and
of the evaluation, and every kind of note that an answer can carry.

### O12.1 The schedule and the checkpoints of the general method

[`../Doc/how_gk_works.md`](../Doc/how_gk_works.md) gives both in full: Section 6.1, "Checking the proof recursively", has the
tasks that each application creates, the checkpoints of the yellow-bill stage of the Tweety example, and the
control of the whole method in pseudocode; Section 6.2, "Sharing work and dividing the budget", has the contexts,
the exclusions, the allowances of the tasks and the division of the time limit. [`../Doc/recursive_output.md`](../Doc/recursive_output.md)
gives the fields of the answer line that report the schedule: the checkpoint whose evaluation gave the value
(`value_from`), why the schedule stopped (`stop`) and what the stop means for the value (`search`), and the option
`-checkpoints DIR`, which writes the dump of every checkpoint.

### O12.2 Rank contexts and taxonomy priorities

The general method checks the exception of a normal default inside a **rank context**: inside the check of a
normal default of rank k, a normal default of a lower positive rank cannot supply the objection. The prover
refuses such defaults in the task of the check, and the evaluator applies the same restriction. The semantics
compares ranks only at the same atom (Section 4.7 of the paper), so the restriction is an approximation. gk
records the note `context copies` only when one atom is read in two contexts and an application is admitted in one
of them and refused in the other. When the restriction removes evidence in one context only, the answer has no
note, and its value can differ from the semantics.

The exact method uses no rank context. On the rank-context example of [`../Doc/mcref.md`](../Doc/mcref.md), Section 6, it gives no
value and names the statement that it does not cover; the tool declines that input with the reason
`rank contexts`.

A **taxonomy priority** (a rank of the form `tax(name)`, which needs `-taxonomy`) compares defaults by the
specificity of classes in a loaded taxonomy. It is an extension of gk, and the semantics does not define it. The
exact method does not cover it, so the default sends such an input to the general method, and the general method
records no note for it.

### O12.3 One proof in full

The first Tweety stage (part O1, [`O1_tweety/inputs/stage1/gk.gkp`](O1_tweety/inputs/stage1/gk.gkp)):

```prolog
bird(tweety).
0.9::flies(X) :- bird(X), unless(-flies(X), 2).
-flies(X) :- penguin(X), unless(flies(X), 3).
0.8::seabird(tweety).
0.7::penguin(X) :- seabird(X).
query(flies(tweety)).
```

`gk gk.gkp` answers by the exact method (`"answer_from":"the exhaustive search"`), complete, with the value
(.396, .56, 0, .044). The field `proof` of its answer line, with one step per line:

```json
{"proof":{
 "for":[
  {"proves":["flies","tweety"],"confidence":0.9,"steps":[
    [1,["in","frm_1","axiom",1],[["bird","tweety"]]],
    [2,["in","frm_2","axiom",0.9],[["flies","?:X"],["-bird","?:X"],["$block",2,["$not",["flies","?:X"]]]]],
    [3,["mp",[2,1],1,"fromaxiom",0.9],[["flies","tweety"],["$block",2,["$not",["flies","tweety"]]]]],
    [4,["in","frm_6","goal",1],[["-flies","tweety"]]],
    [5,["mp",[3,0],4,"fromgoal",0.9],[["$block",2,["$not",["flies","tweety"]]]]]
  ]}
 ],
 "against":[
  {"proves":["-flies","tweety"],"confidence":0.56,"steps":[
    [1,["in","frm_4","axiom",0.8],[["seabird","tweety"]]],
    [2,["in","frm_5","axiom",0.7],[["penguin","?:X"],["-seabird","?:X"]]],
    [3,["mp",[2,1],1,"fromaxiom",0.56],[["penguin","tweety"]]],
    [4,["in","frm_3","axiom",1],[["-flies","?:X"],["-penguin","?:X"],["$block",3,["flies","?:X"]]]],
    [5,["mp",[4,1],3,"fromaxiom",0.56],[["-flies","tweety"],["$block",3,["flies","tweety"]]]],
    [6,["in","taskgoal","goal",1],[["flies","tweety"]]],
    [7,["mp",[5,0],6,"fromgoal",0.56],[["$block",3,["flies","tweety"]]]]
  ]}
 ]
}}
```

Each step is `[n, label, clause]`; the clause is a list of literals, and an exception `unless(L, k)` is the
literal `["$block", k, L]`.

- `["in", name, role, confidence]` is an input statement: `frm_1` is the first statement of the input, and the
  role is `axiom` or `goal`.
- `["mp", p1, p2, ..., "fromaxiom" or "fromgoal", confidence]` is a resolution step. A parent `[2,1]` is literal 1
  of step 2, counted from 0; a parent `1` is step 1.
- The proof for `flies(tweety)` resolves the flying default with `bird(tweety)` and then with the negated
  question. Its last clause keeps the exception of the default, `["$block",2,["$not",["flies","tweety"]]]`: the
  proof holds where `-flies(tweety)` is not established at rank 2.
- The proof against starts from `seabird(tweety)` and the uncertain rule for `penguin`, so its confidence is
  .8 × .7 = .56. It then uses the penguin default of rank 3, and its last clause keeps that default's
  exception. The goal `taskgoal` is the goal of the nested search for the complement of the question.

The evaluation counts these proofs as applications: the penguin default of rank 3 wins in .56 of the worlds, and
the flying default gives .9 in the other .44. `-fullproof` adds the proofs that the nested searches found to each
proof, under `subproofs`; [`../Doc/recursive_output.md`](../Doc/recursive_output.md), Section 3.1, describes the field.

### O12.4 The limits of the exact method and of the evaluation

The time limit T is set by `-seconds` (10 s by default); 90 % of it is the budget of a method. Under the default,
the exact method gets half of T. A limit named `GK_...` is changed in the environment or with
`-keyenv NAME=VALUE`; the general method's limits are changed by the strategy keys `recursive_...` (`-strategy` or
`-strategytext`). The other limits are fixed in gk 1.3.2.

**The exact method.**

| limit | default | what reaching it prints |
|---|---|---|
| the collection's share of the time | 60 % of the method's budget | the limit `tasks`: "the time budget of the collection" |
| the evaluation's share of the time | the rest of the budget, at least 1 s | the interruption `evaluation budget`; no value |
| ground statements of a task (`GK_KEY_GROUND`) | 500,000 | the limit `task limit`; during the binding by data or a full grounding, the input is `not covered` |
| derived clauses and resolvents of a task (`GK_KEY_TRIPLES`, `GK_KEY_RESOLVENTS`) | 300,000 and 3,000,000 | the limit `task limit` |
| symbolic states, their length, emitted clauses and unifications of a task (`GK_KEY_STATES`, `GK_KEY_STATELEN`, `GK_KEY_EMIT`, `GK_KEY_UNIFS`) | 1,000; 64; 200,000; 10,000 | without function terms the task moves to the ground search and no note is printed; with function terms, the limit `task limit` |
| the depth of terms (`GK_KEY_TERM_DEPTH`) | 16 levels above the deepest written term | the limit `term depth` |
| the memory of the collection (`GK_KEY_MEMORY_MB`) | 1,000 MB | the limit `memory of the collection` |
| the rounds of the binding by data | 100,000 | the limit `binding by data`; under the default, a switch to the general method |
| function terms (`GK_KEY_FUNCS`) | on | with 0, an input with a function symbol is `not covered` |
| the proofs printed (`GK_KEY_PROOFS`, `GK_KEY_PROOF_STEPS`, `GK_KEY_PROOF_BYTES`) | 10 proofs; 2,000 steps; 1,000,000 bytes | a list of the proofs left out; the value does not change |

**The evaluation, under both methods.** A value is computed over the cells of a block of atoms; a cell is a
choice of states of the atoms that the block reads.

| limit | default | what reaching it prints |
|---|---|---|
| cells of one evaluation step | 200,000 | in a group of the narrowing, the reading `cycle cut` (the general method); in a joined block of the exact method, the reading `complete mode` with `join_limit`; elsewhere the interruption `block allowance` |
| atoms of a group with a cycle | 21 when an atom of the group can end without a value, else 32 (the states of a group are kept in 64 bits) | as for the cells |
| exception-bearing applications of one step of the exception pass | 64 | as for the cells |
| atoms and views of one vertex | 32 | the interruption `block allowance` |
| exception literals of one application in a group of the exception pass | 64 | the reading `complete mode` (the exact method) |
| the depth of the recursion along the atom graph | 40,000 levels (20,000 in the WebAssembly build), and the room of the stack | the interruption `recursion depth`; no value |
| the memory of the evaluation (`GK_EVAL_MEMORY_MB`) | 8,192 MB | the interruption `memory`; no value |

**The general method.**

| limit | default | what reaching it prints |
|---|---|---|
| the first allowance of a task, L0, and its factor ρ per depth | 50 ms and .5; in round k at depth d the allowance is L0 × 2^k × ρ^d | a cut task (`a cut task`, why `allowance`) |
| the share of the first proof search, and the reserve for the evaluation | a quarter of the budget each | the `stop` texts of the answer line |
| answers of a task in round k | 4 × 2^k | a cut task (why `answers cap`) |
| the depth of a runnable task in round k | 4 + k | `a queued task not run` |
| applications in round k | 256 × 2^k | `a cap` |
| the rounds | 64 | the `stop` text `the round limit of 64` |
| further searches of one literal (`recursive_search_again`) | 4 | the reading `search again` |
| the steps of the replay of one derivation | 20,000 | `a pending step` (why `walk incomplete`) |

### O12.5 The notes of an answer

An answer carries notes of three kinds: **readings**, which say how gk evaluated the collected evidence;
**limits** of the exact method, which make an answer not complete; and the **unfinished work** of the general
method. The answer line holds the readings (`readings`), the limits of the exact method (`complete_mode.limits`,
and per answer `limits` for a question with variables), the reason of a switch of the default (`policy.reason`),
and the general method's `stop` and `search` texts and counts of tasks and steps. With `-dwdump`, the dump of the
general method lists every unfinished item (`status_facts.unfinished`) and every approximation
(`status_facts.approximation`), including the notes of the conversion of derivations. The column "can differ"
says whether a value with the note can differ from the value of the semantics for the input as gk reads it.

**Readings of the evaluation**, under both methods.

| reading | meaning | can differ |
|---|---|---|
| `narrowing` | The narrowing evaluated a group; the detail says whether the group has a cycle across signs and lists its atoms. | no |
| `no self-support` | Applications whose body can be derived only through applications with their own head literal were left out. | no |
| `backbone` | The exception pass removed and restored applications in some cells. | no |
| `blocked-rule repair` | Applications that rest on a removed application were left out in some cells. | no |
| `clause rule in a circle` | The clause rule in a cycle gave some atoms of a group no value in some cells. | no |
| `rank zero as equal rank` | Opposed normal defaults at one atom have no positive rank and are read as of equal rank. | no |
| `cycle cut` | A cyclic group above a limit of the narrowing lost the dependency edges that lead back into it; with `-eval125`, every cycle through an exception, through a normal default or across signs is cut. | yes |
| `backbone approximation` | The exception pass of a group read an outside atom in its final state. | yes |
| `context copies` | The general method only: an atom is read in two rank contexts, and an application is admitted in one and refused in the other (part O12.2). | yes |
| `priorities as equal rank` | The general method with `-taxonomy` only: the taxonomy priorities of an atom's normal defaults form a cycle or cannot be ordered, so all of them are read as one rank. | the semantics does not define taxonomy priorities |
| `complete mode` | The exact method only: a group or a joined block met a limit of the evaluation (for example the cells, with `join_limit`). | yes |
| `clause rule across groups` | The exact method only: the clause rule in a cycle ran on a block whose atoms belong to more than one group of the definition; the semantics evaluates such an atom after the cycle. | yes |

The kind `taxonomy ignored` exists in the code but is not printed by gk 1.3.2.

**Limits of the exact method** (`complete_mode.limits`). An answer with a limit is not complete.

| limit | meaning | can differ |
|---|---|---|
| `not covered` | The input is outside the exact method; the sentence names the reason, the statement and its line. | no value |
| `tasks` | The collection used its share of the time before every task ended. | yes |
| `memory of the collection` | The collection passed its memory limit. | yes |
| `no self-support` | The pass that leaves out self-supporting applications did not end in time. | yes |
| `task limit` | A task met one of its limits (O12.4); the sentence names the first. | yes |
| `binding by data` | The binding by data stopped after 100,000 rounds while it still derived new atoms. | yes |
| `function terms` | A variable ran through the written ground terms, or a constant has the text of a function term. | yes |
| `term depth` | Terms deeper than the depth limit were cut. | yes |
| `test switch` | A test switch withheld proof candidates. | yes |
| a reading | The readings `cycle cut`, `backbone approximation`, `complete mode` and `clause rule across groups` also count as limits. | yes |
| an interruption | The evaluation stopped (the table of interruptions below). | no value |

The reasons of `not covered` are: an equality between terms; a built-in condition or a predicate of gk's
machinery; a question written as a formula; a compound question; an answer literal outside the question; no
question; an attached knowledge base; an input with variables and without any constant; a taxonomy priority; an
exception with a rank above 0 on a statement without a written head, or one that is not the opposite of its
rule's head; an exception literal of another form; more ground statements than the limit of the exact method; and
the limits of the reader (more than 256 variables in one clause, a term nested deeper than 256 levels, a term or
an atom of another type).

**Notes of the general method's collection.** The first two are in the line's `readings`; the others are
approximations in the dump.

| note | meaning | can differ |
|---|---|---|
| `self exception` | An application whose exception is one of its own body literals was not registered. | no |
| `search again` | A literal reached the limit of 4 further searches. | yes |
| `residual variable represented by a fresh constant` | A variable that a proof left unbound got a fresh constant. | yes |
| `universal as one instance` | Derivations and applications that keep a variable are each read as one instance. | yes |
| `universal answer as one instance` | An answer comes from a universal statement, and its variable got a fresh constant. | yes |
| `built-in` | A built-in condition of an application cannot be decided. | yes |
| `a proof application with shared evidence` | A proof application shares input instances with the input or with another proof application. | yes |
| `an inconsistent antecedent context` | The assumed context of a conditional question makes an atom certain in both signs. | yes |

**Unfinished work of the general method** (`status_facts.unfinished`). The line counts the tasks
(`tasks_cut`, `tasks_queued`, `tasks_that_cannot_run`) and the steps (`pending_steps`,
`steps_not_represented`). Each kind below can mean that the value lacks evidence, so a value with it can differ.

| kind | meaning |
|---|---|
| `a cut task` | A search task was stopped by its allowance or by its cap of answers. |
| `a queued task not run` | A task was queued and never ran before the deadline. |
| `a task that cannot run` | A task could not be made, for example a literal that cannot be encoded or a context that could not be built. |
| `a pending step` | A derivation step that gk could not convert into an application of the semantics; the field `why` names the step, for example a case analysis through a default or a step used against the direction of a default. |
| `a step not represented` | A case analysis whose exceptions include its own case literal. |
| `an interrupted evaluation` | The newest evaluation stopped, or no budget was left for it; the value is that of the latest completed evaluation. |
| `the budget` | The deadline ended the schedule. |
| `a cap` | The applications reached their cap of the round. |
| `a question with variables: the recursion did not run`, `a compound question: the recursion did not run` | No proof of the question was found; the line has no value. |
| `the question's form was read from the clause heads`, `a variable class of the definition is ambiguous`, `the question's form is not supported` | The form of a question with variables or of a conditional question. |
| `a conditional form without a connection`, `a refutation not read in a declared context`, `a conditional form's groundings capped`, `an assumption conflict` | A conditional question, which the definition does not cover. |
| `a nested definition not supported`, `fresh constant prefix` | Inputs that define a question inside another, and a change of the prefix of fresh constants. |

The kind `direction` (a default or an uncertain rule used only towards its written head) is also in this list;
the semantics uses such a rule in the same way, so it does not make the value differ.

**Interruptions of the evaluation.** Under the general method the line names them in `evaluation.why`, and the
value is that of the latest completed evaluation. Under the exact method they appear in `complete_mode.limits`,
and the answer has no value.

| interruption | meaning |
|---|---|
| `evaluation budget` | The evaluation used its share of the time. |
| `recursion depth` | The recursion along the atom graph passed 40,000 levels or the room of the stack. |
| `memory` | The evaluation passed its memory limit. |
| `block allowance` | A step passed the cells or atoms of one block (O12.4). |
| `block fixpoint` | The rounds of a block did not settle within their bound. |
| `narrowing` | The narrowing did not settle within its bound of rounds. |
| `narrowing size` | More than 1,000 groups were too large for the narrowing. |
| `assumption context` | A conditional question's assumptions could not be evaluated. |
| `readings` | The rounds of the readings did not settle. |

**The default's reasons** (`policy.reason`). The default keeps the exact method's answer when its collection
ended and its evaluation gave a value. Otherwise the general method answers, and its value is a budgeted
estimate.

| reason | when |
|---|---|
| a reason of `not covered`, `a function symbol with arguments` or `an equality between terms`, with the statement and its line | before the exact method starts: the general method answers at once |
| `the exhaustive search did not end: ...` with `the time budget of the collection`, `memory of the collection`, the first task limit, or `the binding by data stopped after 100000 rounds` | a switch after the exact method's collection |
| `the pass that leaves out self-supporting applications (no self-support) did not end` | a switch |
| `no time of N was left for the evaluation` | a switch |
| `the evaluator gave no value: ...` | a switch after an interruption of the evaluation |

A reading that counts as a limit does not cause a switch; the default then prints the exact method's answer, not
complete. When the time limit ends the general method under the default before it has a value, gk prints
`{"result": "time limit, proof not found"}`.
