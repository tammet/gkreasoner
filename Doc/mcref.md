# The reference tool `mcref`

`mcref` is a standalone program that computes the support report of a
question as the support semantics defines it. It has two methods. **Exact
evaluation** splits the world space into cells and evaluates one world per
cell; its result is the report itself, with no sampling error. **Sampling**
draws N worlds and counts the states; its result is an estimate with an
error bound. The tool shares no code with gk and calls no prover. For
gk's clause syntaxes it calls gk only as a parser.

The tool is the executable form of the definition. It gives a numerical
check of hand calculations, and of gk's methods on the inputs that it
accepts: the complete answers of gk's exact method must equal its exact
values, and the answers of the general method can be measured against
them.

This page explains what the tool computes, its two methods, what it
declines, how to read its output, and how its numbers are compared with
gk's. The definition is in [support_semantics.md](support_semantics.md);
this page uses its terms and cites its sections as §1 to §15. Its §13
describes the tool in short. The tool is in
[`../mcref/`](../mcref/README.md), with its command-line reference. This
page describes version 1.3.1.
Versions 1.1.0 to 1.1.2 computed an earlier form of the definition,
without the proofs of several statements and without the exception pass in
layers; records made with them keep their values.

The main terms, in short. An **atom** is a predicate applied to
arguments, such as `flies(t)`; it is **ground** when it has no variables. A
**literal** is an atom or its negation; the **opposite** of a literal is
the same atom with the other sign. A **statement** is one input fact, rule
or disjunction, with its **confidence** (1 when none is written). An
**application** is a standing possibility to conclude one literal: it has
a head, body literals that must be usable, exception literals that must
not be usable, and a strength.

## 1. A first run

The input `Examples/semantics/default_vs_fact.gkp` has a normal default and
an uncertain contrary fact:

```prolog
bird(t).
0.3::-flies(t).
0.9::flies(X) :- bird(X), unless(-flies(X), 2).
query(flies(t)).
```

Run from the repository root:

```
python3 mcref/mcref.py Examples/semantics/default_vs_fact.gkp
```

The tool prints one JSON line. Shortened:

```json
{"mcref": {"version": "1.3.1", "mode": "exact", "rules": "8",
  "cells": 9, "error_bound": 0.0,
  "answers": [{"instance": "flies(t)", "value": [0.63, 0.3, 0.0, 0.07], "unstable": 0.0}],
  "unsupported": null, ...}}
```

The method was exact evaluation over 9 cells. flies(t) is positive in a
share .63 of the worlds, negative in .3, in conflict in none and in
ignorance in .07. The share of worlds without a value (`unstable`) is 0.

The three applications are the fact bird(t), the fact ¬flies(t) with
confidence .3, and the default "flies(t) from bird(t)" with confidence .9.
The default's exception ¬flies(t) is the opposite of its head, so the
default is a normal default of rank 2. In a world with U = .2 for
flies(t), the contrary fact applies (.2 < .3), and flies(t) is negative.
In a world with U = .5 and V = .4, the contrary fails, the default is
tested on V (.4 < .9), and flies(t) is positive. So the report is
(.3 · 0 + .7 · .9, .3, 0, .7 · .1) = (.63, .3, 0, .07).

With `--mode sampling` the tool draws 100,000 worlds:

```json
{"mcref": {"version": "1.3.1", "mode": "sampling", "worlds": 100000, "seed": 1,
  "answers": [{"instance": "flies(t)", "counts": [63054, 29801, 0, 7145, 0],
    "value": [0.63054, 0.29801, 0.0, 0.07145], "unstable": 0.0,
    "interval_95": [[0.6255, 0.6356], [0.2930, 0.3030], [0.0, 0.0050], [0.0664, 0.0765]]}],
  "error_bound": 0.005037, ...}}
```

Each share of the estimate lies within the error bound .005 of the exact
value.

## 2. What the tool computes

The tool prepares a finite ground problem, builds the applications and the
proofs, and computes the state of every atom in a world by the rules of
the support semantics. This section names the steps; the reference
definitions of `support_semantics.md` §11 give the rules.

### 2.1 Grounding

D is the set of constants of the input, the question's constants included.
Every variable of a statement's ordinary literals is replaced by a constant
of D, in every combination (§11.2).

- A variable that occurs only in exception literals is not instantiated
  per statement. All its instances are exceptions of the one ground
  statement, and any usable one blocks it.
- A built-in condition such as `X < 10` is computed after instantiation. A
  true condition is dropped; a false one drops the ground statement.
- Two choices of constants for the ordinary variables of one statement are
  two ground statements, also when they give the same clause.
- A statement with confidence 0 is excluded.
- Constants keep their JSON type: `1`, `1.0` and `"1"` are three different
  constants.

The grounding work is counted before any ground statement is made: for
each statement, the number of constants to the power of its variables,
summed over the statements. Above 200,000 (`--max-ground N`) the input is
declined with `unsupported: grounding limit`.

### 2.2 The single applications

The kinds of statement and their single applications (§11.3):

| statement | single applications |
|---|---|
| a fact L | head L, empty body, the fact's confidence |
| a rule with a written head H that is uncertain or has an exception | head H, body the opposites of its other literals, the rule's confidence |
| a certain clause, also a certain rule without an exception | one application per literal L: head L, body the opposites of the other literals, strength 1 |
| an uncertain clause with several literals and no written head, confidence c | an event s, a new atom with one fact of confidence c; one application per literal as above, with s added to its body, strength 1 |
| a clause with an exception and no written head | as the two rows above; each application keeps the exception literals |

So `flies(X) :- bird(X)` with X := t gives `flies(t)` from `bird(t)` and
`-bird(t)` from `-flies(t)`, as classical logic does. `0.9::flies(X) :-
bird(X)` gives the first application only. The tool names the events
`$src_1`, `$src_2`, ... in the order of the ground statements.

An application whose head's opposite is among its exception literals is a
**normal default**, and that literal's rank is the application's rank.
Every other exception literal is **external**. An uncertain rule with a
written head and a body literal has a **rule identity**: a rule that is
used in several applications holds or fails once.

For a statement whose consequent is a disjunction, the head is read from
its exception: `flies(X) ; -bird(X) :- unless(-flies(X)).` is read as
`flies(X) :- bird(X), unless(-flies(X)).` For a `.gkp` input gk's
converter reads this head; for JSON input the tool's reader does.

### 2.3 Proofs of several statements

A consequence that needs several statements at once, such as a proof by
cases, is evidence too (§3.3, §11.4). The tool finds these proofs by resolution on
clauses that keep the set of statements they were derived from. A derived
clause is discarded when another derived clause has a subset of its
literals and a subset of its statements. A rule with a written head that
is uncertain or has an exception takes part only in the search for its own
head, and is never resolved on the atom of its head.

The **non-goal clauses** of a proof of Q are the clauses of its statements
that do not contain Q. The application of a proof of Q has the head Q; as
body every single literal that the premises and the non-goal clauses
imply; the exception
literals of all its statements; the non-goal clauses as **listed
clauses**, which must not be contradicted; and the identities of its
uncertain rules, with the product of their confidences as strength. A
proof whose application another application makes redundant is dropped.

Example: `0.8::r. 0.2::-p. p :- r. q :- p. q :- -r.` The single
applications give q in the worlds where p is positive or r is negative:
a share .68. The proof by cases over r ({`q :- p.`, `p :- r.`,
`q :- -r.`}, no premise) lists the clause `p ; -r`. It applies also where r
and p are both in ignorance, a share .2 · .8 = .16, so q is
(.84, 0, 0, .16). gk's exact method gives the same value.

### 2.4 Applications that are left out

The rules of §11.3 and §11.4 (in words: §5.7):

- **The self-exception rule.** An application whose external exception
  literal is also one of its body literals never applies; the tool does not
  create it. A rule with a written head that blocks itself in this way
  takes part in no proof either.
- **A redundant proof.** The application of a proof is dropped when another
  application of the same literal requires no more.
- **No self-support.** An application with head L is left out when
  one of its body literals cannot be derived without the applications that
  have head L. In `0.5::a :- unless(-a). 0.2::-a. 0.5::a :- b. b :- a.` the
  rule `0.5::a :- b.` can hold only when a already holds, so it is ignored,
  and a is (.4, .2, 0, .4).
- **A body that can never hold.** An application with a body literal that
  no chain of applications derives from the facts (exceptions and
  opposition ignored) is present in no world. The tool removes it before
  the groups are formed, so that it decides no dependence.

### 2.5 One world

For every ground atom A, events included, a world gives two numbers U_A
and V_A, each uniform on [0, 1). A literal is **usable** when its atom is
in the state of its sign. The applications of a literal that apply form a
**side**; its strength is the probability that at least one of them
succeeds, each rule identity counted once. The state of an atom follows
from the strengths and kinds of its two sides and from U_A and V_A, by the
table of §11.6 (in words: §5.4). The kind of a side is decided in each
world (§5.5).

The calculation for one world, with the exception pass of §11.9:

```
take the numbers U_A and V_A of every ground atom
for each layer of exceptions, lowest first:
    evaluate without the applications of that layer and above,
        and without those removed before;
    remove the applications of the layer whose external exception is usable
evaluate all applications that are not removed
restore a removed application whose exceptions are no longer usable,
    and evaluate again, until nothing is restored
record each atom: positive, negative, conflict, ignorance or no value
```

One evaluation handles the **groups** of atoms (the strongly connected
components of the dependencies), each after the groups it depends on
(§11.7):

```
for each group G, after every group that G depends on:
    if an application of G lists a clause with an atom in G:
        the clause rule in a cycle
    else if G depends on an atom without a value outside G:
        the narrowing; an atom it leaves open has no value
    else if G is one atom that does not depend on itself:
        its state comes from the table of one atom
    else if G is a sweep group:
        every atom starts in ignorance; repeat a sweep until it changes nothing
    else if G has no cycle across signs:
        the narrowing; an atom it leaves open is in ignorance
    else:
        the narrowing; an atom it leaves open has no value
```

A **sweep group** has no cycle across signs, no exception literal inside
it, no normal default, and no outside atom without a value. The
**narrowing** keeps a set of sure literals and a set of possible literals
and rebuilds both until neither changes. The **clause rule in a cycle**
handles a proof whose listed clause can be contradicted by evidence that
the proof itself helps to derive (§11.8). After the rule, with a result
or without one, a proof outside the group that lists one of its clauses
reads the check of that clause on the final states. When an evaluation leaves out
some applications, the rules of Section 2.4 and the groups are applied
again on the applications that remain. §7 explains the three procedures on
examples. In a sweep group the sweeps settle after at most one sweep more
than the group has atoms (the sweep lemma, §12); a sweep group that
changes a state later stops the run with an internal error.

No number is drawn again when an atom is used a second time or a cycle
returns to it.

### 2.6 The report

For a ground question literal Q with atom A, the report (§11.10) is the
share of worlds in which A is positive, negative, in conflict and in ignorance, with
positive and negative exchanged when Q is negated. The share of worlds in
which A has no value is reported beside the four shares, in the field
`unstable`. The four shares sum to one minus it; nothing is rescaled. A
question with variables gets one report per ground instance over D, from
the same worlds. The tool prints an instance when its atom is the head of
an application.

## 3. Exact evaluation

The tests of one atom compare U_A and V_A with the strengths of sets of
its applications. These thresholds cut each unit interval into pieces, and
the pieces of all atoms together split the world space into **cells**.
Within one cell every test has the same outcome, so every state is the
same. The tool evaluates one world at the midpoint of each cell and adds
the volume of the cell to the state it finds for each atom. The result is
the report itself, exact up to the rounding of floating-point numbers.

The number of cells is the product over the atoms of the number of pieces
of U_A and V_A. It grows fast with the uncertain statements that depend on
each other. With `--mode auto` (the default) the tool uses exact
evaluation when the cells are at most `--max-cells` (300,000 by default)
and sampling above it; the field `exact_not_used` then names the cell
count. The tool also falls back to sampling when an atom has more than 16
applications of one sign. With `--mode exact` the tool gives no value above
the limit, and the field `too_many_cells` says why.

Exact evaluation needs time in proportion to the cells. The inputs of
`Examples/semantics/` have at most 48 cells each and take well under one
second; `Examples/confidences/alarm_v2.js` has 4,608 cells.

## 4. Sampling

The tool draws N worlds (`--samples N`, 100,000 by default) and divides
each count by N. The first four fractions estimate the report; the fifth
is the share of worlds without a value.

- **The error bound.** By Hoeffding's inequality and a union bound, the
  interval `p ± e` with e = √(ln(8 / .05) / (2N)) holds at 95 % for the
  four shares of one answer together. e is .0113 at 20,000 worlds and .0050
  at 100,000. The bound covers the sampling error of one answer only, and
  agreement within it does not establish exactness.
- **The random numbers.** The numbers come from a seeded 64-bit generator
  (splitmix64, `--seed`, default 1) in a fixed order of the atoms. The same
  input, seed and sample count give the same counts.
- **The same quantity.** A sampled world falls into a cell with the
  probability of the cell's volume, so the sampled fractions tend to the
  exact values as N grows. The two methods share the reading of the input,
  the construction of the applications and the evaluation of one world;
  they differ only in which worlds they evaluate.

Drawing more worlds narrows the interval. It does no more inference and
gives no value to the worlds without one.

## 5. Examples

`Examples/semantics/mutual_block_half.gkp`:

```prolog
0.5::p(a) :- unless(b(a)).
0.5::b(a) :- unless(p(a)).
query(p(a)).
```

The group {p(a), b(a)} has a cycle through exception literals only, so it
is not a sweep group, and the narrowing evaluates it. In a world where both
rules pass their thresholds, the narrowing finds neither literal sure,
since each rule's exception stays possible, and both atoms are in
ignorance. Exact evaluation gives p(a) (.25, 0, 0, .75).

The certain Yale shooting (`Examples/semantics/yale.gkp`): alive(s2) and
loaded(s1) form a cycle across signs through the shooting law used in both
directions. Each inertia default meets a possible ordinary application,
and neither atom becomes sure. alive(s2) has no value in any world:
(0, 0, 0, 0) with the share 1 without a value. An atom that depends on it
has no value either: `walks(s2) :- alive(s2).` gives walks(s2) the share 1
without a value (`Examples/semantics/yale_walks.gkp`).

`Examples/semantics/combined.js` is the vet's note of
`support_semantics.md` §9.2. Exact evaluation over 48 cells gives flies(t)
(.45, 0, 0, .55) and flies(p) (0, 1, 0, 0).

`Examples/semantics/tweety_3a_gull_rule.gkp`, stage 3a of Tweety in
§9.1 (the disjunction and the .9 gull rule), gives flies(tweety)
(.6984, .224, 0, .0776).

## 6. What the tool declines, and its limits

The tool ends with `"unsupported": reason` and no value for:

- equality, function symbols, taxonomy strengths;
- a built-in whose variable ranges outside D, and an unknown built-in;
- variables in an input without constants;
- a compound or conditional question, several questions, no question;
- the grounding limit, and input forms it does not read: an existential
  quantifier, an uncertain formula that gives several clauses, `@report`
  or `@marginal` declarations, JSON-LD structure;
- **rank contexts.** Inside an exception check of strength k, gk does not
  count defaults of positive rank below k. The tool does not model this.
  It walks everything that the external exceptions of each default of
  positive rank k depend on, and declines the input when a default of a
  positive rank below k is there. The walk errs toward declining. With
  `--all-atoms`, any other affected atom is printed with `unsupported` and
  no value.

The complete list of reasons: `function symbols`, `grounding limit`,
`equality`, `taxonomy strength`, `compound question`, `conditional
question`, `unknown built-in`, `rank contexts`, `no constants`, `built-in
over an open domain`, `existential quantifier`, `uncertain formula with
several clauses`, `JSON-LD structure`, `@report or @marginal declaration`,
`no question`, `several questions`, `unsupported formula form`, `empty
ground clause`, `conversion failed`, `include not found` and `not JSON`.
None is approximated.

A rank-context example: a rank-3 default "a bird flies unless not flying
is established at rank 3, and unless the bird is injured" (confidence .9),
with `hurt(t)` and the rank-1 default "a hurt individual is injured,
unless not injured is established at rank 1" (confidence .5). The tool
declines the input: `rank contexts: a rank-1 default for injured(t) inside
a rank-3 exception check`. gk's exact method gives no value for it either
and names the statement it does not cover.

**The limits of the proof search.** The search for proofs of several
statements stops at 3,000,000 resolvents, 300,000 kept clauses or 20,000
proofs of one input. When a limit is reached, the tool evaluates the input
with the single applications only and says so in a reading
(`LIMIT: the proofs of several statements are incomplete`); its values are
then not those of the definition.

**The cost** grows with the cells or the worlds and with the size of the
groups. The proof search can use about 2 GB of memory before it reaches
its resolvent limit: `Examples/asp_comparison/gbirds_trans_scasp.js` reaches
the limit after 11 s with a peak of 2.2 GB. The domain is the constants of the input, so the lineage with
function terms of the paper's Tweety example needs a reduction to a finite
input first; the tool does not find that reduction.

## 7. The output

The output is one JSON line, `{"mcref": {...}}`. The fields depend on the
method.

**Both methods:** `mode` (`exact` or `sampling`), `rules` (`8` for the
definition, `1.1` for `--rules 1.1`), `error_bound`, `error_bound_text`,
`input`, `answers`, `unsupported`, `evaluated_atoms`, `readings` and
`proofs` (the counts of the proof search). When a proof lists a clause
inside a cycle, `clause_rule_in_circle` gives the share of worlds (exact
evaluation) or the number of worlds (sampling) where the clause rule in a
cycle had no result. Each answer has `instance`, `value` (positive, negative,
conflict, ignorance), `unstable` (the share without a value) and, for a
question with variables, `binding`. With `--all-atoms` also `atom_values`,
one entry per ground atom; an atom that fails the rank-context test has
`unsupported` and no value.

**Exact evaluation** adds `cells` (the number of cells), `too_many_cells`
(the reason when exact evaluation could not be used) and `groups` (the
groups that are not single atoms, with their procedure). Its `error_bound`
is 0, and `error_bound_text` reads "exact up to the rounding of
floating-point numbers".

**Sampling** adds `worlds` and `samples` (the count), `seed`,
`exact_not_used` (why the default command sampled), `error_bound_text`
("Hoeffding's inequality with a union bound: 95 per cent for the four
shares of one answer together"), and for each answer
`counts` (positive, negative, conflict, ignorance, no value), `key`
(`[sign, predicate, arguments]` as typed JSON values) and `interval_95`
(`p ± e` per share, clipped to [0, 1]). It also gives the counts of the
input: `question`, `variables`, `constants`, `ground_clauses`, `atoms`,
`applications`, `self_exception_applications`, `components`,
`longest_sweeps` (the most sweeps or narrowing rounds of one group in one
world); `backbone` (the counts of the exception pass: applications removed
and restored); `left_out_by_no_self_support` (the applications that the
no-self-support rule left out although their body literals can be
derived); `interpretation`; and
`provenance`, the sha256 of the tool's files and of every file read: the
input, included files, the gk binary and the converted text.

**The readings** are notes of the run, each a pair (name, text):

| name | meaning |
|---|---|
| `proofs` | the applications that proofs of several statements gave; or `LIMIT: ...` when the search reached a limit and the input was evaluated with the single applications only |
| `self exception` | an application that the self-exception rule dropped, with its statement and literal |
| `clause rule in a circle` | sampling: the worlds where the clause rule in a cycle had no result, and the groups |
| `backbone` | sampling: the applications that the exception pass removed or restored |
| `cases` | with `--cases`: the applications of the proofs by cases |

The names `backbone`, `clause rule in a circle` and `self exception` are
the names of the same notes in gk's output (`support_semantics.md`
§10.5).

**The field `interpretation`** (sampling) holds one text per part of the
definition, under a plain name, with a pointer to the section of
`support_semantics.md`: `semantics`, `exception pass`, `rules with a
written head`, `clauses`, `clauses without a written head`, `no
self-support`, `blocked-rule repair`, `clause rule without a result`,
`head read from a default`, `not represented`, `domain`, `kind of a side`,
`groups`, `no value`, `rank contexts` and `self exception`; with the
default command also `proofs of several statements`, and with `--cases`
`conclusions by cases`. The text of `exception pass` names the variant in
use: the layers of the default command, or `judge` or `fix` with
`--rules 1.1`.

## 8. The comparison with gk

gk 1.3.1 has three methods for the support semantics. **Exact** (`gk -exact
FILE`) searches exhaustively; when it says `"complete": true`, its value is
the value of the definition for the input as gk reads it. **General**
(`gk -general FILE`) searches within a time budget and gives an estimate.
**Auto** (`gk FILE`, the default) gives Exact's answer when Exact ends
within half of the time limit, and otherwise General's. The legacy direct
method (`gk -direct`) computes another quantity; the tool is not compared
with it. The paper's theorem on the exact method states that a
complete answer of Exact equals the report of the definition, so it must
equal the tool's exact value.

On 2026-11-22, `gk -exact` of gk 1.3.1 and the tool's exact evaluation
were compared on 40 inputs of gk's examples and regression cases
where Exact reported a complete answer and the tool gave an exact value.
All 48 answers agreed to the sixth decimal. A wider run over all 165 such
inputs of those folders, 203 answers, agreed too. The tool declined 11
further inputs (JSON-LD structure, an unsupported formula form, equality,
`@report` declarations, an uncertain formula with several clauses), and
one input had too many cells.

A comparison script of gk's source repository, `mcref_compare.py`, runs
the tool, with sampling at 20,000 worlds, on every input of a record of
gk runs and compares each answer with the record's value. The script and
the records of gk runs are not in this repository. Each answer row gets a
class:

| class | condition |
|---|---|
| not comparable: two answers print alike | as named; not scored |
| incomplete: unstable worlds | the tool's share without a value is above 0; not scored; `within_bounds` says whether gk's value lies within `[settled, settled + no value] ± e` |
| incomplete: unstable worlds, binding only in mcref | the same, for a binding the record lacks |
| binding only in mcref (with support / ignorance) | a settled binding the record lacks |
| agree with recursive | every share within e of gk's value |
| differ, gk records a reading | the first flag is a reading of gk's run |
| differ, gk used a contrapositive | no reading; gk used a certain rule with a written head at another literal |
| differ, gk used a step not represented | no reading, no contrapositive; a step gk could not turn into an application |
| differ, no flag | the rest |
| binding only in the record; no answer in either; recursive has no value | as named |

The flags are observed features of gk's run, not shown causes.

- **The record.** A record has `compare_*.json` with gk's values, readings
  and `steps_not_represented` of each input, and the raw outputs
  `raw/<set>/*.rec.out.gz` and `*.dir.out.gz`. The flag "contrapositive"
  reads the dump of the general method in `*.rec.out.gz` (format
  `gk_dump_v1`); gk 1.3.1 prints that dump only with `gk -general
  -dwdump`. The second raw file holds the answers of gk's legacy direct
  method, which the table counts apart.
- **The cache.** A result in `OUTDIR/mcref/` is reused only when its sample
  count and seed are the ones asked for, the sha256 of every file of the
  tool equals the current one, and every file of its provenance still has
  the recorded sha256.
- **The keys.** gk prints answers without type marks, so an answer of the
  tool is matched by its key printed the same way. Two answers of one
  input that print alike (`p(1)` and `p("1")`) are not compared.

Agreement within e shows that gk found the applications that the tool
built, as far as they matter for the answer, and that both evaluated them
by the same rules. The interval covers sampling error only, and the tool
covers only the inputs it accepts.

## 9. Options for tests and comparisons

The default command (`--rules 8`) computes the definition. Other options
keep other rules for tests:

- `--rules 1.1`: no proofs of several statements and no layers in the
  exception pass; the exception pass removes in one step the applications
  whose external exception the applications without exceptions establish.
  `--proofs` and `--layers` then turn each part on.
- `--cases` (with `--rules 1.1`): proofs by cases from the classical
  clauses, an earlier way to represent consequences of several statements.
- `--backbone fix` (with `--rules 1.1`): a variant of the exception pass
  that keeps the states the applications without exceptions establish.
- `--ranks`: a candidate rule for ranks across atoms; not part of the
  definition.

Environment switches turn single rules of the definition off for tests;
[`../mcref/README.md`](../mcref/README.md) lists them.

## 10. Reading gk's inputs

The tool reads the JSON-LD-LOGIC form of gk's input language
([json_ld_logic.md](json_ld_logic.md)): a list of statements, each with
`@logic`, an optional `@confidence` (default 1; an integer is a
percentage, as in gk; 0 excludes the statement) and an optional `@name`;
`$block` literals with a rank; the question as `@question`, as `@role`
`question` or `conjecture`, as a goal clause with `$ans`, or as `@role`
`negated_conjecture`. `@include` files are read.

For `.gkp`, `.gks`, Prolog and TPTP inputs the tool runs
`gk FILE -writejson -recursive`: gk's parser only, never its reasoning.
The binary is the repository's `bin/gk`; the environment variable
`MCREF_GK` names another. The converter keeps the written head of a rule
as `"@dirhead": k`, the position of the head in the literal list. The
output of sampling names the conversion in `converted_by`.

Variables are `?:X` strings; constants are other strings and numbers, each
kept with its JSON type. A name listed in a `forall`
(`["forall", ["X", "Y"], body]`) is a bound variable in the argument
positions of the body, also without `?:`, as gk reads it. A bare string
atom (`"p"`) and the array form (`["p"]`) are different atoms, as in gk.

The written head follows gk's input rules (the comment before
`wr_js_dir_isconn` in `Builtparser/jsparse_dir.c`): a literal list with
`@dirhead`; `[body, "=>", head]` and `[head, "<=", body]`, also under a
top-level `forall`, with a literal or a conjunction of literals as body
and a literal, possibly followed by `|` and `$block` literals, as head;
`["if", conditions, "then", head]` with literal conditions. One ordinary
literal is a fact. Anything else is a clause, which the tool turns into
clauses by negation normal form and distribution.

## 11. The tests

The acceptance cases of the tool are in gk's source repository: 151
cases in seven sets, each with an expected value from a hand calculation,
checked with exact evaluation and with sampling.
