# The reference tool `mcref`

`mcref` is a small standalone program that computes the support report of a
question by sampling worlds. Its purpose is an independent numerical check
of gk's recursive method on a stated, restricted class of inputs. It shares
no code with gk and calls no prover.

This page explains what the tool computes, how it obtains its applications,
what it rejects, how to read its output, and how its numbers are compared
with gk's. The definition the tool computes is the support semantics of
[support_semantics.md](support_semantics.md), which follows Section 4 and
Appendix A of the paper *Reasoning with Uncertain Evidence, Opposition and
Exceptions* (T. Tammet, 2026, in preparation); the paper's Section 5
describes the tool. This page assumes that semantics and cites the
sections of `support_semantics.md` as §1 to §15. The tool is in
[`../mcref/`](../mcref/README.md), with its command-line reference. This
page describes version 1.1.2
of 2026-11-10. It computes the cycle rule of 2026-11-10 (§14.6): sweeps
only for a sweep group, the narrowing for every other cycle group.
Version 1.1.1 of 2026-11-09 gave the same counts as version 1.1.0 of
2026-11-03; Section 12 lists what version 1.1.2 changed.

`mcref` is not one of the two older Monte Carlo programs in
[`../montecarlo/`](../montecarlo/README.md). Those check the direct method:
`gkmc.py` samples clause activations and runs gk on each world, and
`threshold_worlds.py` samples the shared-threshold model of the direct
method ([`../montecarlo/README.md`](../montecarlo/README.md) describes
both). `mcref` samples the support semantics, which the recursive method
computes.

The terms are those of the support semantics. An **atom** is a predicate
applied to arguments, such as `flies(t)`; it is **ground** when it has no
variables. A **literal** is an atom or its negation, and the **complement**
of a literal is the same atom with the opposite sign. A **clause** is one input fact, rule or
disjunction; `support_semantics.md` calls it a statement. A **confidence** is
the number in [0, 1] written on a clause.

## 1. A first run

The input `Examples/semantics/default_vs_fact.gkp` has a normal default and
an ordinary contrary fact:

```prolog
bird(t).
0.3::-flies(t).
0.9::flies(X) :- bird(X), unless(-flies(X), 2).
query(flies(t)).
```

Run from the repository root:

```
python3 mcref/mcref.py Examples/semantics/default_vs_fact.gkp --samples 100000
```

The tool prints one JSON line. Shortened:

```json
{"mcref": {"question": "flies(t)", "constants": 1, "ground_clauses": 3,
  "atoms": 2, "applications": 3, "samples": 100000, "seed": 1, "readings": [],
  "answers": [{"instance": "flies(t)", "counts": [63054, 29801, 0, 7145, 0],
    "value": [0.63054, 0.29801, 0.0, 0.07145], "unstable": 0.0,
    "interval_95": [[0.6255, 0.6356], [0.2930, 0.3030], [0.0, 0.0050], [0.0664, 0.0765]]}],
  "unsupported": null, ...}}
```

Of 100,000 sampled worlds, flies(t) was positive in 63,054, negative in
29,801, in conflict in none, and ignorant in 7,145; it was unresolved in
none. The value of the semantics is (.63, .3, 0, .07) (§6). Each
component of the estimate is within .005 of it, the half-width of
`interval_95` at this sample count.

The three applications are the fact bird(t), the fact ¬flies(t) with
confidence .3, and the default `flies(t) from bird(t)` with confidence .9.
The default's exception ¬flies(t) is the complement of its head, so it is a
normal-default application of rank 2. In a world with U = .2 for flies(t),
the contrary fact passes (.2 < .3), and flies(t) is negative. In a world
with U = .5 and V = .4, the contrary fails, the default is tested on V
(.4 < .9), and flies(t) is positive.

## 2. Two separate things

A support report is computed from a finite collection of ground
**applications**. An application is one way of using one ground clause to
derive one literal: it has a **head** (the literal derived), **body
literals** (conditions that must hold), optional **exception literals**
(conditions that must not hold) and a confidence. The rules of the
semantics say how a collection of applications receives a report. How the
collection is obtained is a separate question:

- gk's recursive method obtains applications from proofs. It may import a
  composite resolution inference as one application, and it finds only the
  applications its proofs produce within the time budget.
- `mcref` obtains them by a restricted construction: exhaustive grounding
  over the input's constants, one application per literal of an undirected
  clause and of a certain written-head rule without exceptions, and one
  application at the written head of every other rule (Section 3).

Agreement between gk and the tool therefore needs both the same collection
and the same evaluation rules. An application is not a proof step. A
resolution step is an event in one proof; an application is a standing
possibility, present in every world where its conditions hold.

## 3. How the tool builds the applications

### 3.1 Grounding

Let D be the set of constants in the input, the question's constants
included. Every variable of a clause's ordinary literals is replaced by a
constant from D in every combination. A clause with v such variables yields
up to |D|^v ground clauses before duplicates are merged; a repeated
variable gets the same constant in both places.

- A variable that occurs only in exception literals is not instantiated per
  clause. All its instances are exceptions of the one ground clause, and any
  usable one blocks it.
- A built-in condition such as `X < 10` is computed after instantiation. A
  true condition is dropped; a false one drops the ground clause.
- Two clauses with the same text are two clauses. One clause instantiated
  twice with the same substitution is one ground clause.
- Constants keep their JSON type: `1`, `1.0` and `"1"` are three different
  constants.

The tool stops with `unsupported: grounding limit` when the grounding work
passes 200,000 (`--max-ground N`). The work is counted before any ground
clause is made: for each clause, the number of constants to the power of
its variables in ordinary and exception literals, summed over the clauses.
An input with variables and no constants is `unsupported: no constants`.
A variable that occurs only in built-in literals is `unsupported: built-in
over an open domain`. The built-ins are `$less`, `$greater`,
`$lessorequal`, `$greaterorequal`, `$is_int`, `$is_real` and `$is_number`
(decision 66); an unknown built-in is unsupported.

### 3.2 From a ground clause to applications

| ground clause | applications |
|---|---|
| a fact: one ordinary literal | one application with that head and an empty body |
| a clause with a **written head** (`H :- B`, `B => H`), confidence below 1 or with exception literals | one application at its head; the body is the other literals negated |
| a certain clause with a written head and no exception literal | the same statement as the undirected clause of its literals (§7, §14.3): one application per literal L, head L, body the other literals negated, confidence 1 |
| a certain **undirected clause** (a plain disjunction such as `a ∨ b`) | one application per literal L: head L, body the other literals negated, confidence 1 |
| an uncertain undirected clause, confidence c | a **source event** s, a new atom with one fact of confidence c; one application per literal, with s added to its body, confidence 1 |

So `flies(X) :- bird(X)` with X := t gives `flies(t)` from `bird(t)` and
`-bird(t)` from `-flies(t)`, as classical logic does; `0.9::flies(X) :-
bird(X)` gives the first application only. Until version 1.0.0 the tool
used every written-head rule at its head only.

The source event keeps an uncertain disjunction one statement. Without it,
`.6:: a ∨ b` would give two applications with confidence .6 each, two
independent chances. With it, in a world the clause is in force (s
positive) or absent for both uses at once. The tool names source events
`$src_1`, `$src_2`, ... in the order of the ground clauses.

### 3.3 Exceptions

A clause may have exception literals, written `unless(E, k)` or
`$block(k, E)`, with an integer **strength** k ≥ 0. For each application of
the clause:

- If the complement of the head is among the exception literals, the
  application is a **normal-default application**, and that literal's
  strength is its **rank**. The literal itself is not treated as an
  exception; the rows of the state table handle the contrary.
- Every other exception literal is **external**: the application is
  present only when no external exception is usable.

The test is made per application. So one orientation of an undirected
clause can be a normal-default application while another is not.

### 3.4 Two conventions

**Self-exception** (decision 68). An application whose external exception
literal is also one of its body literals never applies, and the tool does
not create it. The test is made on the ground application, after the
expansion of exception-only variables, so an exception that matches a body
literal by binding only exception-only variables counts too. The output
lists each such application under `readings` as `self exception`. An
exception that follows from the body through other rules is not covered.

Example: `Examples/exceptions/penguin.js` has the flat clause
`[-bird(X), flies(X), $block(3, -flies(X))]`. Its orientation at -bird(o)
is `-bird(o) from -flies(o), unless -flies(o)`, which never applies. Asked
"who is not a bird" (the same clauses with the question `-bird(X)`),
the tool drops 6 such applications and gives ignorance for o, and the
negative state for the bird b and the penguin p.

**Unreachable applications** (§8, §14.3). A literal is **reachable** when
it is the head of a fact or the head of an application all of whose body
literals are reachable, exceptions and opposition ignored. An application
with a body literal that is not reachable is present in no world. The tool
removes it before the cycle groups are formed, so that it decides no
dependence; the removal changes no answer. In the penguin example the
certain rule `bird(X) :- penguin(X)` also gives `-penguin(p)` from
`-bird(p)`. No application derives `-bird(p)`, so that application is
removed, and bird(p) does not depend on penguin(p) through it.

**The kind of a side** is decided in each world from the applications
present in it (§8, §14.5): a side is normal when every present
application in it is a normal default, ordinary when at least one is not.
Until version 1.0.0 the tool read a side whose candidates mixed the two
kinds as ordinary once, before sampling, as gk does (the reading `mixed
kinds as ordinary`); the decision of 2026-11-03 replaced that reading by
the per-world kind, and the tool prints no such reading.

## 4. How the tool evaluates one world

For every ground atom A, the tool picks two random numbers U_A and V_A,
each uniform on [0, 1). One complete assignment of these numbers is a
**world**. In probability terms a world is one sample point; in ProbLog
terms it corresponds to a total choice.

A literal is **usable** when its atom is in the state of its sign: A in
state positive, ¬A in state negative. An application is **present** when
every body literal is usable and no external exception literal is usable.
The **positive support** a of A is the noisy-or of the confidences of the
present applications with head A, and the **negative support** b that of
the present applications with head ¬A. The state of A follows from a, b,
U_A, V_A and the kinds and ranks of the two sides, by the table of §6
and the steps of §14.5.

**Order and cycles.** Atom A **depends on** every atom in the bodies and
exceptions of A's applications; the head's complement of a normal default
is not an exception here. The tool groups the atoms into **cycle groups**
(strongly connected components) and handles the groups in an order in
which every group comes after the atoms it depends on, by the table of
§9 and the procedure of §14.6:

```
for each cycle group G, dependencies first:
    if G depends on an unresolved atom:
        the narrowing, with both literals of the unresolved atom possible
        and neither sure; an atom left possible but not sure is unresolved
    else if G is one atom without a cycle:
        its state comes from the tables
    else if G is a sweep group:
        every atom of G starts ignorant
        repeat a sweep: recompute every atom of G from the previous states
            the sweep changes nothing      -> G is settled; stop
    else if G has no cycle across signs:
        the narrowing, ordinary applications first when G has normal
        defaults; an atom left possible but not sure is ignorance
    else (a cycle across signs):
        the narrowing, ordinary applications first when G has normal
        defaults; an atom left possible but not sure is unresolved
```

A **sweep group** is a cycle group G with four properties: G has no cycle
across signs; no application for or against an atom of G has an exception
literal whose atom is in G (the complement of its own head on a normal
default does not count); no application for or against an atom of G is a
normal default; and no atom outside G that G depends on is unresolved. The
tool decides the first three once for each group, before sampling; the
fourth is the first test of the loop above.

The **narrowing** is the procedure of §9 and §14.6. In one world it keeps two
sets of literals of G: **sure**, the literals the computation has
justified, and **possible**, the literals it has not yet ruled out. Both
are rebuilt from the base literals (the usable literals outside G and the
fixed literals of G) upward, the sure set with the applications for a
literal read against the possible opposition, the possible set with the
applications for a literal read against the sure opposition, until neither
changes; an atom with no sure literal whose tables give conflict over the
possible applications is fixed in conflict and the rounds start again
without it. With normal defaults in G the procedure runs first on the
ordinary applications alone and fixes every atom that ends sure or in
conflict, then on all applications (§9). Section 11.3 gives the
pseudocode.

In a sweep group the set of atoms with the group's sign only grows from
sweep to sweep, and the side of the other sign is the same in every sweep.
So the states are final after at most |G|+1 sweeps, and sweep |G|+2
changes nothing (the sweep lemma of §14.6). The tool checks this bound: a
sweep group that changes a state in sweep |G|+2 stops the run with an
internal error that names the input and the group (exit status 3). The
bound has not been reached on any input.

Before version 1.1.2 the tool used sweeps for every group without a cycle
across signs and ran the narrowing only when the sweeps repeated a state.
Sweeps can let a group support itself when support is withdrawn later.
In `p :- unless(u). p :- p. u :- p. u.` the first sweep makes p positive
before u blocks p's default, and `p :- p` then keeps p positive: version
1.1.1 gave p (1, 0, 0, 0). The group {p, u} has the exception literal u
inside, so version 1.1.2 uses the narrowing: u is sure, p's default is
blocked, `p :- p` cannot make p possible, and p is in ignorance,
(0, 0, 0, 1). The well-founded model of the program has p false.

Example, `Examples/semantics/mutual_block_half.gkp`:

```prolog
0.5::p(a) :- unless(b(a)).
0.5::b(a) :- unless(p(a)).
query(p(a)).
```

The group has a cycle through exception literals only, so it is not a
sweep group, and the narrowing evaluates it. In a world where both rules
pass their thresholds, the narrowing finds neither literal sure, since
each rule's exception stays possible, and both atoms are read as
ignorance (§9).
With 100,000 samples the tool counts p(a) positive in 24,991 worlds and
ignorant in 75,009: value (.2499, 0, 0, .7501), the semantics' (.25, 0, 0,
.75). Until version 1.0.0 the tool reported the 25,015 worlds where both
rules pass as unresolved.

Example, the certain Yale shooting of §9 (`Examples/semantics/yale.gkp`): alive(s2) and loaded(s1)
form a cycle across signs through the shooting law used in both
directions, each inertia default is opposed by a possible ordinary
application, and neither atom becomes sure: alive(s2) is **unresolved** in
every world, (0, 0, 0, 0) with the unresolved share 1. An atom that
depends on it follows §9 and §14.6: `q. 0.9::q :- alive(s2).` gives q
(1, 0, 0, 0), since its fact makes it sure whatever alive(s2) is;
`walks(s2) :- alive(s2).` gives walks(s2) unresolved.

## 5. From counts to a report

For a ground question literal Q with atom A, the report is

    R(Q) = (P[positive], P[negative], P[conflict], P[ignorance]) over worlds,

with positive and negative exchanged when Q is negated, and separately the
fraction of worlds in which A is unresolved. The tool estimates it from N
sampled worlds:

```
ground the input; build the applications; apply the conventions
for each of N worlds:
    draw U_A and V_A for every atom the question depends on
    evaluate the cycle groups in dependency order
    count the state of each question instance:
        positive, negative, conflict, ignorance or unresolved
value = the first four counts / N;  unstable = the fifth count / N
```

- **No scaling.** The output's field `unstable` is the unresolved share.
  The four values sum to one minus it; nothing is rescaled.
- **Sampling error.** The interval `p ± e`, with
  e = sqrt(ln(8/.05) / (2N)) (Hoeffding's inequality), holds at 95 % for
  the four values of one answer at once: e = .005 at N = 100,000 and
  .011 at N = 20,000. It covers the sampling error only: not the grounding,
  the construction of the applications or the unresolved worlds.
- **Reproducibility.** The random numbers come from a seeded 64-bit
  generator (splitmix64, `--seed`, default 1) in a fixed atom order. The
  same input, seed and sample count give the same counts.
- **Questions with variables.** A question with variables gets one report
  per ground instance over D, from the same worlds. An instance is printed
  when its atom is the head of an application, also when its value is
  (0, 0, 0, 1).

## 6. What the tool rejects, and what it does not represent

**Rejected inputs.** The tool ends with `"unsupported": reason` and no value
for:

- equality, function symbols, taxonomy strengths;
- a built-in whose variable ranges outside D, an unknown built-in;
- variables in an input without constants;
- a compound or conditional question, several questions, no question;
- the grounding limit, and input forms it does not read (an existential
  quantifier, an uncertain formula that gives several clauses, `@report` or
  `@marginal` declarations, JSON-LD structure);
- **rank contexts** (decision 13). Inside an exception check of strength k,
  gk does not count defaults of positive rank below k. The tool does not
  model this. It walks everything the external exceptions of each default
  of positive rank k depend on, and rejects the input when a default of a
  positive rank below k is there. The walk errs toward rejecting.

The rank-context test in detail: a default of positive rank k (the largest
strength of its `$block` literals) is **affected** when the dependency
closure of one of its external exceptions, through bodies, exceptions and
rank-zero defaults, holds a default of any kind with a positive rank below
k. The normal marker is not an exception here. An atom whose own
dependency closure holds an affected default cannot be evaluated: when it
is a question instance the input is `unsupported: rank contexts`; with
`--all-atoms` any other such atom is printed with `unsupported` and no
value.

The complete list of reasons the output can name: `function symbols`,
`grounding limit`, `equality`, `taxonomy strength`, `compound question`,
`conditional question`, `unknown built-in`, `rank contexts`, `no
constants`, `built-in over an open domain`, `existential quantifier`,
`uncertain formula with several clauses` (gk splits the confidence of such
a formula), `JSON-LD structure`, `@report or @marginal declaration`, `no
question`, `several questions`, `unsupported formula form`, `empty ground
clause`, `conversion failed`, `include not found` and `not JSON`. None is
approximated.

A rank-context example: a rank-3 default "a bird flies unless not flying is
established at rank 3, and unless the bird is injured" (confidence .9), with
`hurt(t)` and the rank-1 default "a hurt individual is injured, unless not
injured is established at rank 1" (confidence .5). The tool rejects the
input: `rank contexts: a rank-1 default for injured(t) inside a rank-3
exception check`. gk 1.2.3 answers flies(t) with .9 for, because it does not
count the rank-1 default inside the rank-3 check. Without rank contexts the
support rules would give .45 for.

**Inferences the construction does not represent**, and does not detect: a
composite classical inference that no single application expresses, such
as q from `a ∨ b`, `¬a ∨ q`, `¬b ∨ q`. Resolution proves q; the
applications leave q at ignorance. On such inputs the tool's value is the
value of its applications, and the comparison with gk marks the
difference.

The output's `interpretation` field states these choices in every run.

## 7. The comparison with gk

A comparison script of gk's source repository, `mcref_compare.py`, runs
the tool on every input of a record of gk runs and compares each answer
with gk's recursive value. The script and the records of gk runs are not
in this repository. The current one is the rerun of 2026-11-09 with
gk 1.2.3 on the 360 inputs that the tool accepts, out of the project's
development collection of 1,022 inputs. Each answer row gets a class:

| class | meaning |
|---|---|
| agree with recursive | every component within e of gk's value |
| differ, gk records a reading | gk applied one of its approximations (for example `cycle cut`) |
| differ, gk used a contrapositive | gk used a certain written-head rule at another literal |
| differ, gk used a step not represented | gk's proof held a step its collector could not turn into an application |
| differ, no flag | none of the above |
| incomplete: unstable worlds | the tool's unstable share is above 0; not scored |

The flags are observed features of gk's run on the input, not shown causes.
A cause is claimed only where a run demonstrates it.

The result of version 1.1.0 at 20,000 samples per input, against gk 1.2.3
(2026-11-09; versions 1.1.1 and 1.1.2 give the same counts on all 360
inputs, and gk 1.2.5 the same values):

- 360 of the 1,022 inputs are inside the tool's scope. Equality (522
  inputs) and function symbols (86) are the largest rejection reasons; 7
  inputs are rejected for rank contexts. The 662 rejected inputs had no gk
  run in this comparison.
- The 360 inputs give 438 answer rows. On 395 rows both sides give a value
  for the same instance; on 394 of them the tool's unresolved share is 0.
  375 of these 394 agree, and 19 differ.
- Of the 19, 12 carry gk's reading `cycle cut`, 1 a residual variable
  represented by a fresh constant, and 1 a step not represented. 3 carry
  no reading, and gk cut searches there because of the budget. 2 carry no
  reading and no warning. No difference has a cause demonstrated by a
  controlled run.
- One answer has unresolved worlds, the Yale shooting
  (`nm3_yale_shooting`, unresolved in every world); gk's value (0, 1, 0, 0)
  lies within the bounds that the unresolved share allows.
- The 43 rows without a comparable value are instances that only the tool
  lists (35), instances that only gk lists (4), and inputs without an
  answer from either (4).

Earlier records, kept as history: against gk 1.2.0 (2026-10-27) 369 of
the same 394 rows agreed, and against gk 1.2.2 (2026-11-03) 374. gk 1.2.3
changed one of the 394 rows, an exception on the default's own atom, to
agreement. Version 1.0.0 of the tool (2026-10-31) gave 363 of 384 on the
record of gk 1.2.0.

## 8. What agreement shows

Agreement within e shows that gk's recursive method found the applications
that the tool built, as far as they matter for the answer, and that both
evaluated them by the same rules. It does not show more:

- the tool covers only its restricted construction (Section 2);
- the interval covers sampling error only;
- a settled world does not show that the settled states are the only fixed
  point, and an unresolved world does not show that no fixed point exists:
  another order of iteration could reach one;
- the tool is a reference for the semantics, not a reasoner for gk's full
  input language.

## 9. The combined example through the tool

`Examples/semantics/combined.js` is the combined example of
`support_semantics.md` §10. With `--samples 100000` the tool reports 2
constants, 12 ground clauses, 10 atoms, 16 applications (the certain rule
`bird(X) :- penguin(X)` gives two per instance) and 9 cycle groups, and
rejects nothing. flies(t) is positive in 44,974 worlds and ignorant in
55,026, so (.4497, 0, 0, .5503), within .005 of the value (.45, 0, 0, .55).
flies(p) is negative in all 100,000 worlds. The one group of two atoms,
injured(t) and sick(t), settles within three sweeps in every world. gk
1.2.3 gives (.45, 0, 0, .55) and (0, 1, 0, 0), with the reading `cycle cut`.

## 10. Why sampling

Sampling avoids exact summation over all combinations of shared evidence,
so the program stays small enough to read in one sitting: about 930 lines
for the algorithm, of which about 330 are the narrowing, and 670 for
reading and grounding, in plain Python 3 without third-party packages. A world reuses one pair of numbers per atom
wherever the atom occurs, which keeps the dependencies between
overlapping derivations. The price is the sampling error of Section 5.

## 11. Details: input forms, the procedures, the output and the comparison

This section holds the details that a reader of the tool's code or of its
output needs. The commands are in [`../mcref/README.md`](../mcref/README.md).

### 11.1 Input forms

The tool reads the JSON-LD-LOGIC form of gk's input language
([json_ld_logic.md](json_ld_logic.md)): a list of statements, each with
`@logic`, an optional `@confidence` (default 1; an integer is a
percentage, as in gk; 0 discards the statement) and an optional `@name`;
`$block` literals with a strength; the question as `@question`, as `@role`
`question` or `conjecture`, as a goal clause with `$ans`, or as `@role`
`negated_conjecture`. `@include` files are read.

For `.gkp`, `.gks`, Prolog and TPTP inputs the tool runs
`gk FILE -writejson -recursive`: gk's parser only, never its reasoning.
The binary is the repository's `bin/gk`; the environment variable
`MCREF_GK` names another. With the recursive flag the converters keep the
written head of a rule as `"@dirhead": k` (the position of the head in the
clause list); without it a `:-` rule becomes a flat clause and the head is
lost. The output names the conversion in `converted_by`.

Variables are `?:X` strings; constants are other strings and numbers, each
kept with its JSON type. A name listed in a `forall`
(`["forall", ["X", "Y"], body]`) is a bound variable in the argument
positions of the body, also without `?:`: gk reads it so, although
[json_ld_logic.md](json_ld_logic.md) calls a constant in the variable
position an error. A bare string atom (`"p"`) and the array form (`["p"]`)
are different atoms, as in gk.

The written head follows gk's input rules (the comment before
`wr_js_dir_isconn` in `Builtparser/jsparse.c`): a literal list with
`@dirhead`; `[body, "=>", head]` and `[head, "<=", body]`, also under a
top-level `forall`, with a literal or a conjunction of literals as body and
a literal, possibly followed by `|` and `$block` literals, as head (also
nested, `[[H, "|", B1], "|", B2]`, as gk's `wr_js_dir_head` reads it);
`["if", conditions, "then", head]` with literal conditions. One ordinary
literal is a fact; anything else is a clause, which the tool turns into
clauses by negation normal form and distribution.

Two forms are read where the texts leave them open. A built-in in a clause
is a condition: the clause literal is its complement; a built-in as the
written head or in an exception is unsupported. A goal clause with `$ans`
and one other literal is the question that literal's complement asks.

### 11.2 The static passes

Before sampling, the tool runs two passes: the rank-context test of
Section 6 and the removal of unreachable applications of Section 3.4. A
literal is reachable when some chain of applications derives it from the
facts, exceptions and opposition ignored: a least fixpoint over the
applications. The kind of a side is not decided here; it is decided in each
world (Section 3.4).

### 11.3 The procedures in pseudocode

```
draw(atoms, rng):
    for each evaluated ground atom A, in the order of the atom texts:
        U[A] = rng(); V[A] = rng()

usable(state, sign):  state == sign          # conflict and ignorance are usable for nothing

present(app, state):
    every body literal is usable
    and no external exception literal is usable

outcome(A, U, V):
    a = 1 - prod(1 - c) over present apps with head +A
    b = 1 - prod(1 - c) over present apps with head -A
    if no present app of either sign: IGN
    if only + present: POS if U < a else IGN
    if only - present: NEG if U < b else IGN
    the row of support_semantics.md §6 from the kinds and ranks of the two sides

world(U, V):
    for each cycle group G (a strongly connected component of the
            dependency graph), dependencies first:
        if G depends on an unresolved atom:
            narrow(G, all applications); an atom left possible but not
                sure is unresolved
        else if G is one atom without a cycle: outcome(A, U, V)
        else if G is a sweep group (decided once, before sampling):
            every atom of G starts as IGN
            for k in 1, 2, ...:
                sweep G, each atom from the previous sweep
                if the sweep changes nothing: G is settled; stop
                if k = |G| + 2: stop with an internal error
        else if G has no cycle across signs:
            narrow(G, all applications); an atom left possible but not
                sure is ignorance
        else:
            narrow(G, all applications); an atom left possible but not
                sure is unresolved

narrow(G, applications):
    if G has normal defaults: run the narrowing on the ordinary
        applications alone, and fix every atom with a literal in sure in
        that sign, and every atom fixed in conflict
    run the narrowing on all applications, the fixed atoms kept
    a fixed atom keeps its state; an atom with a literal in sure has that
        sign; an atom with neither literal in possible takes the state the
        tables give it with the sure literals; any other atom is left
        possible but not sure

the narrowing (support_semantics.md §14.6, steps 1 to 5):
    base = the usable literals of the atoms outside G that G depends on,
        and the fixed positive and negative literals of G
    sure = base; possible = base, both literals of every unfixed atom of G,
        and both literals of every unresolved outside atom
    repeat:
        new sure: from base upward, add a literal L when the tables give
            L's sign for every selection, with the applications for L
            reading bodies from the set being built and exceptions from
            the old possible set, and the applications against L reading
            bodies from the old possible set and exceptions from the old
            sure set
        new possible: from base upward (the unresolved outside literals
            included), add L when the tables give L's sign for some
            selection, with the applications for L reading bodies from the
            set being built and exceptions from the new sure set, and the
            applications against L reading bodies from the new sure set
            and exceptions from the old possible set
    until neither set changes
    every unfixed atom with no literal in sure whose tables give conflict,
        with both sides counting their applications with bodies in
        possible and no exception in sure, is fixed in conflict; if any
        was, repeat from the start with the fixed atoms left out

run(input, samples, seed):
    ground the input; orient the ground clauses; the static passes
    questions = the ground instances of the question literal
    rng = splitmix64(seed)
    counts[q] = [0, 0, 0, 0, 0] for each q      # +, -, conflict, ignorance, unresolved
    for t in 1..samples:
        U, V = draw(atoms, rng)
        states = world(U, V)
        for each q: counts[q][state of q's atom, or 4 when unresolved] += 1
    for a negative question literal: swap the first two counters
```

A **selection** is a choice between the applications that are certainly
present (bodies in the set the side reads bodies from, no exception in the
set it reads exceptions from) and those that are possibly present (the
same with the two sets exchanged). When no side holds a normal default,
the support of a side is monotone in the applications counted, and one
selection decides: the least favourable for sure, the most favourable for
possible. With normal defaults the tool enumerates the regimes a side can
take (present, kind, rank, the range of its support) and checks the row
for every pair of regimes (support_semantics.md §14.6, "Selections").

An exception literal outside the group is settled before the group that
reads it. A positive cycle without a seed stays ignorant. The output's
`longest_sweeps` is the largest number of sweeps or narrowing rounds one
group needed in one world. Version 1.1.1 also printed `sweep_cap_hits`,
the count of a safety stop of 100,000 sweeps; version 1.1.2 has the bound
|G|+2 of the sweep lemma instead, and the field is gone. The evaluated atoms are the question instances
and every atom their applications read, transitively (all ground atoms
with `--all-atoms`).

Two shortcuts change no count:

- A draw is computed only where it can change a state: U for an atom with
  an uncertain application or applications of both signs, V where a normal
  default meets the other sign. splitmix64's state advances by a fixed
  constant per draw, so the skipped draws are passed over by their offset,
  and every computed U and V is the value of the full stream.
- An application with a body literal that is not reachable is present in
  no world, and `outcome` does not check it.

### 11.4 Random numbers and the output

The random numbers come from splitmix64 seeded with `--seed` (default 1); a
64-bit draw becomes a number in [0, 1) by `(x >> 11) * 2**-53`. One set of
worlds serves every ground instance of the question. The same input, seed
and sample count give the same counts. With `--all-atoms` every atom is
drawn, so the question's counts can differ from a default run within the
sampling error.

The output is one JSON line, `{"mcref": {...}}`, with the fields
`version`, `input`, `converted_by`, `interpretation`, `question`,
`variables`, `constants`, `ground_clauses`, `atoms`, `applications`,
`self_exception_applications`, `evaluated_atoms`, `components`,
`longest_sweeps`, `samples`, `seed`, `readings`,
`answers`, `unsupported` and `provenance`; with `--all-atoms` also
`atom_values`, where an atom that fails the rank-context test has
`unsupported` and no value. Each answer has `instance`, `key`, `binding`,
`counts`, `value`, `unstable` and `interval_95`.

- `key` is `[sign, predicate, arguments]` and `binding` the values of the
  question's variables, both as typed JSON values. `instance` prints a
  number bare (`p(1)`, `p(1.0)`) and a string bare unless it reads as a
  number or holds a separator (`p("1")`).
- `value` is the first four counts divided by `samples`; `unstable` is the
  fifth fraction, the unresolved share (the name is kept from version
  1.0.0). The four values sum to one minus the unresolved share; nothing is
  rescaled.
- `interval_95` is `p ± e`, clipped to [0, 1], with
  e = √(ln(8 / .05) / (2N)). It holds at 95 % for the four components of
  one answer at once. For M answers at once, replace 8 by 8M.
- `provenance` holds the sha256 of `mcref.py` and `mcref_read.py` and of
  every file read: the input, included files, the gk binary and the
  converted text when `-writejson` was used.
- `interpretation` states the reading of the semantics in every run: the
  semantics memo of 2026-11-03 (now stated in
  [support_semantics.md](support_semantics.md)), certain written-head rules
  in every direction, one source event per uncertain flat ground clause,
  composite consequences not represented, the domain of the input's
  constants, the kind of a side per world, the cycle procedures, the
  unresolved rule, rank contexts not covered, and the self-exception rule.

### 11.5 The comparison script

The comparison script `mcref_compare.py` (not in this repository) reads a
record of gk runs: `compare_*.json` with the
recursive values, readings and `steps_not_represented` of each input, and
the raw outputs `raw/<set>/*.dir.out.gz` (the direct method) and
`*.rec.out.gz` (the recursive method's dumps). It runs the tool once per
distinct input with `--samples 20000 --seed 1` and writes `rows.json`,
`tables.json`, `tables.md`, `differ_no_flag.json`, `incomplete.json` and
`contrapositive_inputs.json`. The records of gk runs are not in the
repository.

- **Cache.** A result in `OUTDIR/mcref/` is reused only when its sample
  count and seed are the ones asked for, the sha256 of `mcref.py` and
  `mcref_read.py` equals the current one, and every file of its provenance
  still has the recorded sha256; otherwise the tool runs again. The
  tolerance e of a row is computed from the sample count of the result
  used.
- **Keys.** gk's recursive record prints answers without type marks, so an
  answer of the tool is matched by its key printed the same way. Two
  answers of one input that print alike (`p(1)` and `p("1")`) are not
  compared. The direct method's JSON bindings are matched by typed keys.
- **Flags.** A differing row lists every flag: the readings gk records, a
  contrapositive use (an application with orientation "another literal"
  from a directed statement of confidence 1 in the dump), and a step not
  represented (`steps_not_represented` above 0).

| class | condition |
|---|---|
| not comparable: two answers print alike | as named; not scored |
| incomplete: unstable worlds | the tool's unresolved share is above 0 (decision B3); not scored; `within_bounds` says whether the recursive value lies within `[settled, settled + unresolved] ± e` |
| incomplete: unstable worlds, binding only in mcref | the same, for a binding the record lacks |
| binding only in mcref (with support / ignorance) | a settled binding the record lacks |
| agree with recursive | every component within e |
| differ, gk records a reading | the first flag is a reading: taxonomy ignored, same-atom exception, mixed kinds as ordinary, context copies, cycle cut, rank zero as equal rank, residual variable represented by a fresh constant; gk 1.2.3 no longer prints `same-atom exception` or `mixed kinds as ordinary` |
| differ, gk used a contrapositive | no reading; a contrapositive use |
| differ, gk used a step not represented | no reading, no contrapositive; a step not represented |
| differ, no flag | the rest |
| binding only in the record; no answer in either; recursive has no value | as named |

The tables count distinct inputs and records apart, since one input can
belong to two sets. They give agreement both among the settled comparable
answers and among all answers with a recorded value, next to the answers
without a comparable value. Agreement with the direct method is counted on
the scored rows only.

## 12. History

The tool was written in the gk 1.2 work. The tasks, reports and design log
of the steps below are not in the repository. The 148 acceptance cases
of the steps, with their runner, are in gk's source repository.

- Step 16 (2026-10-29): the tool.
- Step 16b (2026-10-30): the corrections of a review of step 16.
- Step 17b (2026-10-30): decision 68, decisions B2 and B3, and a review of
  step 16b.
- Step 17c (2026-10-31): repeated-state detection instead of a sweep bound.
- Step 17d (2026-10-31): the two shortcuts of Section 11.3.
- 2026-10-31: the default gk binary became the repository's own, so that
  the tool runs from any clone; the counts did not change.
- 2026-11-01: version 1.0.0, printed in the output field `version`.
- Step 19 (2026-11-03): version 1.1.0 computes the semantics memo of
  2026-11-03, now stated in [support_semantics.md](support_semantics.md),
  ported from a prototype of 2026-11-02. New: a certain written-head rule
  without exceptions in every direction; the removal of unreachable
  applications before the groups are formed; the narrowing for a cycle
  across signs, ordinary applications first with normal defaults; sweeps
  for a one-sign or exception-only group, the narrowing with ignorance when
  they repeat; the kind of a side per world; a group that depends on an
  unresolved atom runs the narrowing with that atom's literals possible and
  never sure. The prototype's switches do not exist: the tool has one
  semantics. The acceptance set `step19` and its changes file were added.
- 2026-11-09: the record of gk 1.2.3 (Section 7). The tool's results equal
  those of step 19 on all 360 inputs; the tool's code did not change.
- 2026-11-09: version 1.1.1 for the public repository. The output field
  `interpretation.semantics` names `Doc/support_semantics.md`; the tool also
  finds gk at `../bin/gk`, the layout of the gkreasoner repository. The
  counts did not change: the 135 acceptance cases pass, and the 39 inputs of
  `Examples/semantics/` give the counts of 1.1.0 at 20,000 samples.
- 2026-11-10: version 1.1.2 computes the cycle rule of 2026-11-10
  (support_semantics.md §14.6): sweeps only for a sweep group, the
  narrowing for every other group without a cycle across signs, with an
  undecided atom read as ignorance. The repeated-state test of step 17c and
  the safety stop of 100,000 sweeps (`sweep_cap_hits`) are gone; a sweep
  group that changes a state in sweep |G|+2 stops the run with an internal
  error. The acceptance set `step112` (13 cases) was added, and its
  changes file sets the step-17c case `s17c_late_settlement` to
  (0, 0, 0, 1): the group has exception literals inside. All 148 cases pass. With the same seeds and sample counts, the
  39 inputs of `Examples/semantics/` and the 360 inputs of the record give
  the counts of 1.1.1. Of the 532 runs of the tool in the paper's
  reproduction folder, 5 changed, all on the cyclic benchmark families: the
  random programs of 8 and 40 facts (.222 to .219, .665 to .679) and three
  undecided arguments of frameworks with 6, 10 and 20 arguments.
