# How GK Works

The reference tool `mcref` starts from a finite grounding of the input.
gk instead searches from the question. It finds proofs of the question and
of its opposite by resolution, and it records which input statements each proof
used. Then it searches again for the evidence on which those proofs depend:
further support, opposing evidence and exceptions. One calculation over all
the evidence found gives the four shares of the answer: support for,
support against, conflict and ignorance.

gk has two methods of this kind, the **exact method** (`gk -exact input`)
and the **general method** (`gk -general input`). Both read the input in
the same way and evaluate the same form of evidence. Neither grounds the
whole input before it searches. The default, `gk input`, is **Auto**: it
combines the two methods (Section 2).

This page follows the section "Computing support with gk" of the paper
"Reasoning with Uncertain Evidence, Opposition and Exceptions: Support
Semantics in Three Layers and a First-Order Inference Method" (T. Tammet).
[support_semantics.md](support_semantics.md) defines what the four shares
mean; its Section 10, "How gk computes the semantics", is a short version
of this page. [recursive_output.md](recursive_output.md) describes the
output.
Every value below is the output of gk 1.3.1 for the command shown, run from the
top folder of the repository.

## 1. Questions and answers

gk converts every input notation to the same internal clause form
([input_languages.md](input_languages.md)). A question is a literal, such
as `flies(tweety)` or `flies(X)`.

gk proves a question by refutation. It adds the negation of the question as
a goal and derives a contradiction. It combines clauses whose opposite
literals unify, applies the resulting substitution, and continues until it
derives the contradiction. For a question with variables, the goal has an
answer literal, and the proof gives the substitution of the variables.

A question without variables gets one value: four shares in the order
(for, against, conflict, ignorance). A question with variables gets one
value for each ground answer. Each answer also has its proofs for and
against (the field `proof`). A proof in the line shows its main structure:
the steps by which the proof search derived the answer. `-fullproof` adds
the proofs that the further searches found, nested under the steps they
concern ([recursive_output.md](recursive_output.md), Section 3.1).

A refutation proof of Q starts from the assumption ¬Q. The proof discharges
that assumption, so the assumption is not evidence against Q. A stated or
separately proved ¬Q is.

## 2. Two methods and the default choice

| | exact method (`-exact`) | general method (`-general`) |
|---|---|---|
| input | no function terms, no equality, no built-in condition | the whole language, with function terms and equality |
| search | exhaustive resolution; it keeps each distinct set of source statements that the answer needs; no grounding of the input | resolution and paramodulation under a time budget; the allowances shrink with the distance from the question |
| what an ended search means | every search task that the answer needs has ended | the search strategy finished that attempt; evidence can be missing |
| the answer | marked complete: the value of the support semantics for the input as read, to within 10^-6 | the value of the evidence found: an estimate, which can lie above or below the value of the input |
| what the output adds | the mark complete, or the limits that the run reached | the stopped searches, the approximation notes, the checkpoint of the value |
| not established | an answer within a given time: the search can be too large | that all evidence was found |

**Auto, the default choice.** Let T be the time limit of the run
(`-seconds`, 10 s by default), and N = T/2.

1. If a function symbol with arguments or an equality occurs anywhere in
   the input or the question, or the exact method does not cover the input
   for another reason, the general method runs with the whole time limit.
2. Otherwise the exact method runs alone within N. Its collection of
   evidence runs until at most .6 N, and its evaluation has the time that
   is left until N.
3. Its answer is printed when every task ended, no limit left required work
   undone, and the evaluation gave a value. The answer is then marked
   complete, or not complete with the approximation that the evaluator
   named.
4. In every other case the general method starts afresh with the time left
   until T.

The line's field `policy` names the method that answered:
`"answer_from":"the exhaustive search"` is the exact method,
`"answer_from":"ordinary gk"` the general method. The first test reads
the whole input, so a statement that the question cannot reach also sends
the input to the general method.

On the Tweety example of the tutorial, Auto answers the four finite stages
by the exact method in less than .1 s, each marked complete:

```sh
./bin/gk Examples/semantics/tweety_1_exception.gkp           # (.396, .56, 0, .044)
./bin/gk Examples/semantics/tweety_2_disjunction.gkp         # (.396, .56, 0, .044)
./bin/gk Examples/semantics/tweety_3a_gull_rule.gkp          # (.6984, .224, 0, .0776)
./bin/gk Examples/semantics/tweety_3b_certain_gull_rule.gkp  # (.6984, .224, 0, .0776)
```

The lineage stage has function terms. Auto sends it to the general method,
which answers in about 6.8 s:

```sh
./bin/gk Examples/semantics/tweety_4_lineage.gkp             # (.396, .56, 0, .044)
```

## 3. The evidence: applications

Both methods collect **applications** from proofs. An application is one
ground inference step that can conclude one literal. It has:

- a **head**: the literal it concludes;
- **body literals**: the premises that must be usable;
- **exception literals**: the `unless` literals of its statements;
- **listed clauses**: the clauses with several literals that a proof of
  several statements used and that must not be contradicted (Section 4);
- a **strength** in [0, 1];
- the identities of its sources: the input statement and the ground
  instance of its variables.

One input statement gives its **single applications**:

- A fact gives one application: its literal is the head, its confidence the
  strength.
- A rule with a written head that is uncertain or has an exception is
  **directed**. It gives one application: its head, its written body and
  its confidence.
- A certain clause without an exception is **classical**. It gives one
  application for each of its literals. That literal is the head, the
  opposites of the other literals form the body, and the strength is 1.
- An uncertain clause without a written head gives one application for
  each of its literals too. All of them share one **source event**: an atom
  that holds with the clause's confidence. The clause is in force in a world
  or not, as one thing.
- A clause with an exception and without a written head also gives one
  application for each of its literals, each with the exception.

To **import** a proof, gk replays its recorded substitutions and forms the
applications of its steps.

- Different uses of one ground application are merged. `0.5::bird(a)` used
  twice is one piece of evidence.
- The instances of `0.9::p(X)` at `a` and at `b` are two pieces of
  evidence.

In the disjunction stage of the Tweety example
([`tweety_2_disjunction.gkp`](../Examples/semantics/tweety_2_disjunction.gkp)),
a proof of `penguin(tweety)` uses `gull(X) ; penguin(X) :- seabird(X)` at
`X = tweety`. The dump of the general method (`-general -dwdump`) lists the
application `e4{_0=tweety}:penguin(tweety)`: entry 4 of the input, its
instance, and the use with the head `penguin(tweety)` and the body
`seabird(tweety)`, `-gull(tweety)`.

## 4. Proofs of several statements

A proof can need several statements together. A **proof** of a literal Q
is a pair of a set L of statements and a set G of premises, such that:

1. the clauses of L with G imply Q in classical logic;
2. the clauses of L with G are consistent;
3. no smaller L with the same G, and no smaller G with the same L, still
   implies Q;
4. every directed rule in L has Q as its written head.

The application of such a proof has the head Q. Its body holds every
literal that G and the clauses of L without Q imply. Its exceptions are the
exceptions of the statements of L. Its listed clauses are the clauses of L
with several literals that do not contain Q. Its strength is the product
of the confidences of the directed rules in L. gk keeps their identities,
so a shared rule counts once.

A proof by cases has an empty body
([`Examples/tutorial/by_cases.gkp`](../Examples/tutorial/by_cases.gkp)):

```prolog
0.6::q :- f.
0.7::q :- -f.
query(q).
```

`./bin/gk Examples/tutorial/by_cases.gkp` prints (.42, 0, 0, .58): the two rules
give `q` in either case of `f`, with strength .6 × .7.

A listed clause must not be contradicted. Its check fails when the opposite
of each of its literals has evidence (conflict is enough). From `p ; r.`,
`-p.`, `-r.`, `q :- p.` and `q :- r.`
([`contradicted_cases.gkp`](../Examples/tutorial/contradicted_cases.gkp)),
the proof of `q` by cases lists `p ; r`. The clause is contradicted in every
world, so `./bin/gk Examples/tutorial/contradicted_cases.gkp` prints
(0, 0, 0, 1).

An uncertain clause brings its source event as a premise. With
`0.8::p ; r.`, `q :- p.` and `q :- r.`
([`uncertain_cases.gkp`](../Examples/tutorial/uncertain_cases.gkp)), gk
prints (.8, 0, 0, .2).

A directed rule enters a proof only as the rule for its own head. From
`a ; b.`, `0.9::c :- a.`, `0.9::c :- b.` and `q :- c.`
([`nested_cases.gkp`](../Examples/tutorial/nested_cases.gkp)), the proof of
`q` takes `c` as a premise. A separate search proves `c` by cases, with
each rule counted once, and gk prints (.81, 0, 0, .19).

The **redundancy rule** drops the application of a proof when another
application with the same head requires no more: its body literals,
exception literals, listed clauses and uncertain rules are all among those
of the first. The other application must be certain, or have its
uncertainty in a body literal or in the identities of its uncertain rules.
In the certain chain `p.`, `q :- p.`, `s :- q.` the single application of
`s :- q` needs only `q`, so it makes the two-rule proof of `s` redundant.

## 5. The exact method

The exact method starts from the question, searches by resolution, records
the statements of each proof, and checks every premise and every exception
in turn. For each literal that it needs, it detects when the search for the
literal's applications is exhausted.

**The covered inputs.** An input is covered when it has finitely many
statements, no function symbol with arguments, no equality, no built-in
condition, and positive ranks only on normal defaults: every exception that
is not the opposite of its rule's head has rank 0. Facts, directed rules,
certain rules and clauses without a written head are all allowed, certain
or uncertain, with or without exceptions and variables. Cycles and
contradictory evidence are allowed. The question is one ground literal,
positive or negated. The variables range over the constants of the input
and the question. gk names the cause when it does not cover an input:

```sh
./bin/gk -exact Examples/core/grandfather_equality.js
```

The line's `complete_mode` says `"covered":false` and gives the reason "an
equality between terms", with the statement and its line.

**The procedure.** A **task** is the search for the applications of one
signed ground literal L. The procedure starts a task for the question and
one for its opposite. In plain pseudocode, on the ground statements:

```text
tasks := { the question Q, the opposite of Q }
while a task for a literal L has not ended:
  import every single application with head L
  assume that L is false
  resolve this assumption with every statement that contains L
      (a directed statement only where L is its written head):
      what is left of each statement is a residual clause
  resolve residual clauses with each other and with the background clauses
      (the undirected statements that contain neither L nor its opposite);
      every derived clause keeps its label: the set of statements used
  for every derived clause C from a residual, with a label of two or more statements:
      G := the opposites of the literals of C, and the source events of the label
      if (label, G) is a proof of L: import its application
  apply the redundancy rule to the applications with head L
  for every new application:
      start tasks for both signs of every atom in its body,
      its external exceptions and its listed clauses (one task per literal)
  the task for L has ended
leave out every application whose body can never hold
leave out every application whose body can hold only when its head already holds
evaluate the remaining applications once (Section 7)
```

A derived clause that contains a literal and its opposite is dropped. Two
equal derived clauses with different labels are both kept, unless the label
of one contains the label of the other. Then the ground search keeps the
clause with the smaller label. An exception is
**external** when it is not the opposite of the rule's own head. The
premises of a proof are not proved inside the task that finds the proof.
Each premise has its own task. The paper proves that on every covered input
every task ends, and the collected applications give the value of the
question in the whole ground input.

**A worked derivation.**
[`Examples/tutorial/worked_derivation.gkp`](../Examples/tutorial/worked_derivation.gkp)
has three statements:

```prolog
0.5::p ; r.
0.8::q :- p, unless(-q).
0.5::q :- r, unless(-q).
query(q).
```

Call the three statements c1, r2 and r3. The uncertain clause c1 has the
source event e1. The task for `q` imports the single applications of r2 and r3. It resolves
the assumption ¬q with both directed rules and then with the background
clause c1:

```text
1.  ¬p  [r2]          ¬r  [r3]        residual clauses of ¬q with r2 and r3
2.  r   [c1, r2]                      ¬p resolved with c1 = p ∨ r
3.  □   [c1, r2, r3]                  r resolved with ¬r
```

The empty clause with the label {c1, r2, r3} gives one application for
`q`. It is a normal default. Its only premise is e1. It has the listed
clause `p ; r`, the rule identities r2 and r3, and the strength
.8 × .5 = .4. The tasks for both signs of `p` and `r` find no opposition, so
`p ; r` is not contradicted. e1 holds in half of the worlds:

```sh
./bin/gk Examples/tutorial/worked_derivation.gkp     # (.2, 0, 0, .8), complete
```

**Searching without grounding.** A task of gk does not ground the input
first. It runs resolution and factoring with unification on the statements
as written, each use with fresh variables. Two additions keep the ground
procedure's result:

- Every derived clause keeps, for each statement used, the terms of all its
  ordinary variables, also of the variables that no longer occur in the
  clause. One statement used with two different bindings is two pieces of
  evidence. The same binding used in two proofs is one.
- When gk takes a ground proof from a derived clause, it instantiates every
  variable of these records that is still free over all input constants.
  It tests each resulting ground candidate as in the ground procedure.

The second addition is needed. From `0.6::q :- f(Y).` and
`0.7::q :- -f(Y).` resolution derives `q` once, with `Y` free. But each
constant gives its own proof by cases. With the two constants of
[`cases_per_constant.gkp`](../Examples/tutorial/cases_per_constant.gkp)
(`item(a).` and `item(b).`), the support is 1 − (1 − .42)²:

```sh
./bin/gk Examples/tutorial/cases_per_constant.gkp    # (.6636, 0, 0, .3364), complete
```

A task must also detect that its search is exhausted. The set of derived
clauses is **closed** when every factor, every pair of clauses (a clause
with a fresh copy of itself included) and every extraction of a candidate
has been processed, and nothing new arises up to variable renaming. A round
without a new clause does not show this. Symbolic search can also grow
without end: repeated uses of one statement with fresh variables can give
longer and longer clauses. When the symbolic search of a task reaches its
limits before it closes, gk finishes that task by an exhaustive ground
search. `complete_mode` counts the tasks of each kind (`tasks_closed`,
`tasks_by_ground_search`).

**Binding variables from facts and earlier answers.** On two classes of
input, single applications are enough. The first class has ground facts of
either sign and directed rules with a positive head and positive body
atoms, where every variable of the head occurs in the body. The second
class has positive ground facts and certain rules of that form without
exceptions, such as transitivity. gk detects these classes when it reads
the input. It then matches rule bodies against facts and earlier answers,
as tabled logic programming does, and keeps every ground instance that
matches. `complete_mode.search` then says `"class 1, binding by data"` or
`"class 2, binding by data"`; the input of the tutorial's Part 1 is in the
first class.

The second class needs the absence of negative input
([`link_opposed.gkp`](../Examples/tutorial/link_opposed.gkp)):

```prolog
link(X,Z) :- link(X,Y), link(Y,Z).
link(a,b).
0.5::link(b,c).
-link(a,c).
query(link(b,c)).
```

The certain rule has a backward use that opposes `link(b,c)`. The input is
in neither class, so the full search runs and finds the opposing proof:

```sh
./bin/gk Examples/tutorial/link_opposed.gkp          # (0, .5, .5, 0), complete
```

**Conditions for marking an answer complete.** The exact method runs its
tasks in rounds. Each task gets a work allowance in a round, four times
larger in each later round, and keeps its state between rounds. An answer
is **complete** only when every task ended, no count, time or memory limit
left required work undone, and the evaluation finished without an
approximation. Every complete run on one input gives the same value,
whatever its time limit. An answer that is not complete lists its limits in
`complete_mode.limits` ([recursive_output.md](recursive_output.md), Section
7, lists the kinds). Three of them:

- `clause rule across groups`: a proof outside a cycle lists a clause of
  that cycle. gk evaluated the proof's conclusion inside the cycle, in the
  rounds of the clause rule, and the semantics evaluates it after the
  cycle. The value can differ from the semantics.
- `recursion depth`: a chain of the dependency is longer than the
  evaluator's recursion allows. The evaluation gives no value.
- `binding by data`: the search that binds the variables of the rules by
  the facts stopped after 100,000 rounds while it still derived new atoms.

**Precision.** gk stores a confidence in units of 10^-7. It reads a
confidence of at least .9999995 as 1, which makes a rule without exceptions
classical. It reads a confidence of at most .0000005 as 0 and leaves the
statement out. `complete_mode.confidence_readings` names every such
statement ([recursive_output.md](recursive_output.md), Section 7.4). A
complete answer gives each share to within 10^-6 of the value for the
input as read.

**Function terms.** `gk -exact` also runs on an input with function terms,
with a limit on the depth of terms. It marks an answer complete when every
task ended, no term was cut at the depth limit, and no variable had to run
through the list of the ground terms written in the input. The paper's
proof of exactness covers only inputs without function terms. It makes no
claim for such an answer, and the reference tool declines function
symbols. A small input with a complete answer:

```prolog
0.8::bird(father(tweety)).
0.9::flies(X) :- bird(X).
query(flies(father(tweety))).
```

On it `gk -exact` prints (.72, 0, 0, .28) with `"complete":true`. On the
lineage stage, `./bin/gk -exact Examples/semantics/tweety_4_lineage.gkp`
prints (.396, .56, 0, .044) with `"complete":false` and the limits "task
limit" and "term depth". Section 9 explains why exactness excludes function
terms.

## 6. The general method

The general method searches with resolution and paramodulation, with
factoring and simplification. Resolution combines clauses by matching
opposite literals. Paramodulation substitutes with an equality. The search
works on clauses with variables, disjunctions, equality and function terms.
So it does not need the ground instances of the input before it starts.

A proof keeps its parent clauses, its substitutions and its inference steps,
also for a derived lemma. So the method can inspect the source statements
behind a compressed proof. The search uses each statement in the
directions of the semantics. A directed rule supplies its head only. So
does a normal default written as a disjunction whose exception is the
opposite of one of its literals. A certain clause without exceptions and a
clause without a written head can conclude any of their literals.

In the lineage stage
([`tweety_4_lineage.gkp`](../Examples/semantics/tweety_4_lineage.gkp)),
a proof derives `bird(tweety)` from the register entry
`bird(parent(parent(tweety)))` with two instances of the certain lineage
rule. The .9 flying default then gives a proof of `flies(tweety)`. The input
permits infinitely many lineage terms, but this proof needs two. The
derivation keeps the default's exception and rank, so the proof also names
the opposing literal to check: `-flies(tweety)`.

### 6.1 Checking the proof recursively

Each imported application creates search tasks:

- for its head: a search for opposition;
- for every body literal: a search for opposition and a search for
  further support;
- for every exception: a search for the exception and a search for
  opposition to it;
- for every literal of a listed clause: a search for the evidence for and
  against it.

The question is also searched for further proofs. A proof that a task finds
adds applications, and these create tasks of their own. Equal tasks are
shared: a literal reached twice gets one task.

The yellow-bill stage
([`tweety_3a_gull_rule.gkp`](../Examples/semantics/tweety_3a_gull_rule.gkp))
shows why the checks inside a proof matter. A **snapshot** is the
collection of applications at one moment. A **checkpoint** is the
evaluation of a snapshot after the first search or after a round of
further searches. `-checkpoints DIR` writes each snapshot into the folder
DIR:

```sh
mkdir cp
./bin/gk -general Examples/semantics/tweety_3a_gull_rule.gkp -checkpoints cp
```

| checkpoint | evidence collected | for | against | conflict | ignorance |
|---|---|---|---|---|---|
| 1 | the bird fact and the flying default | .9 | 0 | 0 | .1 |
| 2 | also the opposing penguin proof | .396 | .56 | 0 | .044 |
| 3 | also the yellow-bill support for gull | .6984 | .224 | 0 | .0776 |

- The first proof uses `bird(tweety)` and the flying default.
- The search for opposition to `flies(tweety)` finds the penguin default of
  rank 3. Its proof uses `seabird(tweety)`, `-gull(tweety)` and the
  disjunction. Penguin holds in .8 × .7 = .56 of the worlds, and there the
  higher rank wins.
- The search for opposition to the premise `-gull(tweety)` finds the
  yellow-bill rule. Where it gives `gull` positive support, `-gull(tweety)` is
  not usable, so the penguin proof does not apply there. The penguin proof
  stays in the collection. The against share falls to
  .8 × .7 × (1 − .6) = .224, and the for share rises to
  (1 − .224) × .9 = .6984.

The third discovery is not a new proof of flying. It changes the state of a
premise inside the opposing proof. The first two rows are estimates on
incomplete evidence: the for share falls and then rises. A run need not find
exactly one new proof per checkpoint.

The control of the whole method:

```text
input: the clauses, a ground question Q, the time budget
reserve part of the budget for evaluating the collected evidence
run a first proof search for Q with a bounded allowance
import its derivations into one shared set of applications S
queue Q, its opposite, and the tasks that the applications create
evaluate S; keep the result if the evaluation completes
for the rounds k = 0, 1, 2, ..., while search time remains:
  choose the runnable tasks: shallowest first, opposition before support
  for each chosen task, at depth d:
    search with the unused part of its allowance for round k and depth d
    import the new derivations into S; merge repeated applications
    queue the tasks that their heads, bodies and exceptions need
    record whether the attempt ended or was stopped by its allowance
  if S changed: evaluate S; keep the result if the evaluation completes
use the evaluation reserve for the latest snapshot not yet evaluated
return the latest completed evaluation, its snapshot, and the notes on unfinished work
```

An imported proof keeps its applications and their identities. It does not
become an independent probabilistic fact.

### 6.2 Sharing work and dividing the budget

**Contexts.** A task is a signed literal with a **context**: the
restrictions that the enclosing exception checks impose. Inside the check
of a normal default of rank k, a normal default of a lower positive rank
cannot supply the objection. So a weaker default cannot defeat a stronger
one through its exception check. The semantics compares ranks only at the
same atom, so this restriction is an approximation (Section 8). Equal tasks
are shared, and a source used in two tasks stays one piece of evidence.

**Exclusions.** A search for further proofs of a literal excludes the input
statements that produced the literal in the task's earlier derivations, at
the first resolution step only. So the search looks for additional evidence
and does not return the first proof again.

- A task has **ended** only after a search with all these exclusions,
  without a stop by its allowance, found nothing new.
- An ended task means that the search strategy finished its attempt. It
  does not mean that all evidence was enumerated.

**Allowances.** Work near the question comes first. In round k at depth d
the cumulative allowance of a task is L0 × 2^k × ρ^d, with L0 = 50 ms and
ρ = .5. A task at depth 1 has 25, 50 and 100 ms in the first three rounds;
each attempt gets the part of the allowance that is still unused. Within
one depth, opposition comes before alternative support, because an
objection can make a premise unusable.

The deadline is `-seconds` (10 s by default). The general method's budget is
9,000 ms of it. The first proof search gets a quarter of the budget, and
another quarter is reserved for the evaluations. The schedule decides which
searches end before the deadline, so it can change the estimate.

## 7. Evaluating the collected evidence

Both methods pass the whole snapshot to the same evaluator. It computes the
four shares analytically, without sampling. Each ground atom and each source
event has one identity, so overlapping proofs count shared evidence once.
For [`shared_evidence.gkp`](../Examples/semantics/shared_evidence.gkp):

```prolog
0.5::a.
b :- a.
c :- a.
q :- b, c.
query(q).
```

`./bin/gk Examples/semantics/shared_evidence.gkp` prints (.5, 0, 0, .5). Both
conditions of `q` depend on the same fact. The evaluator splits the
calculation into two cases. Where `a` is positive, `b`, `c` and `q` are
positive. Where `a` is in ignorance, none of them is established. The two
cases have the weights .5 and .5.

The evaluator groups the atoms that depend on each other. The groups form
a graph without cycles. The evaluator computes this graph by **recursive
conditioning**:

- the probabilities of independent premises multiply;
- for premises with common ancestors, it conditions on the separating or
  shared ancestors, averages the conditional results and caches them.

Within each case it applies the support levels, the kinds of the sides,
the ranks and the state tables of the semantics. It integrates the
comparisons with the numbers of the atoms exactly. A **sweep group** is a
cyclic group whose applications with a body literal inside the group all
conclude literals of one sign, without an exception literal or a normal
default in the group. It is evaluated by repeated passes until the states
stop changing. Any other cyclic group is evaluated cell by cell. A **cell** is a
part of the world space in which every test of the group has the same
outcome. In each cell gk runs the **clause rule**, the **exception pass**
and the two-stage **narrowing**. [support_semantics.md](support_semantics.md)
defines them in Section 5.6, "Exceptions and the exception pass", Section
7.2, "The narrowing", and Section 7.4, "The clause rule". In short:

- The **exception pass** gives layers to the applications with exceptions.
  For each layer it evaluates without the applications of that layer and
  above, and removes the applications of the layer whose exception is
  usable. Then it evaluates the rest, and restores a removed application
  whose exception is no longer usable.
- The **narrowing** grows a set of sure literals from the usable literals
  outside the group, and shrinks a set of possible literals, until both stop
  changing. A sure literal fixes the sign of its atom. An atom without a
  possible literal is in ignorance. Any other atom gets no value. With
  normal defaults in the group, the narrowing runs first on the ordinary
  applications and then on all applications.
- The **clause rule** handles a proof whose conclusion can contradict its
  own listed clause. It evaluates the group with no listed clause
  contradicted, collects the listed clauses that become contradicted, drops
  the proofs that list them, and repeats until no new clause appears.

**The exception pass.** An exception that is not the opposite of its
rule's head is judged before the rule it guards. The definition runs the
exception pass over the whole input. The general method runs it one group
at a time, and records the reading `backbone approximation` where this can
change a value. The exact method joins the atoms that one pass must judge
together, up to a size limit, and marks a larger case not complete.

**Limits.** The evaluator has fixed limits on the size of a group, the
number of applications with exceptions, the number of cells, the depth of
its recursion, memory and time. Under the general method an oversize cyclic group gets a **cycle
cut**: gk removes the dependency edges that lead back into the cycle, and
records the reading `cycle cut`. A memory or deadline stop leaves an
**interrupted** evaluation; the line then gives the latest completed
evaluation and its checkpoint (`value_from`).

**Guarantees of the evaluation.** Unless the output records an
approximation or an interrupted evaluation, the evaluator computes the
semantics of the collected snapshot. The four shares equal the value of the
whole input when the snapshot holds every relevant application. A search
that proves a literal once need not find all applications that support it:
it can drop a second derivation that brings independent support or an
exception. The exact method collects every relevant application. The
general method gives an estimate.

## 8. Guarantees and limits of an answer

Every answer names the method that gave it and includes its proofs for and
against.

**A complete answer of the exact method** is a certificate. Every search
and the evaluation ended without an approximation. The four shares are the
value of the support semantics for the input as read, to within 10^-6. An
answer of the exact method that is not complete names the limits that the
run reached.

**An answer of the general method** is a budgeted estimate: the latest
completed evaluation of the collected snapshot. The output qualifies it in
two ways.

- **Unfinished work.** The dump's `status_facts.unfinished` lists the
  searches that were stopped by their allowance (`a cut task`) or not run
  (`a queued task not run`), pending proof steps and interrupted
  evaluations. The line counts the stopped searches in `tasks_cut`, and its
  field `search` says whether more budget can change the value.
- **Approximation notes.** The readings in the line's `readings`, and in the
  dump's `status_facts.approximation`, name an approximation of the
  semantics:
  - `cycle cut`: dependency edges were removed in an oversize cyclic group
    (Section 7), or under `-eval125`, the evaluation of gk 1.2.5;
  - `backbone approximation`: the exception pass ran one group at a time
    where this can change a value (Section 7);
  - `context copies`: the rank context of Section 6.2 applied, and an atom
    read in two contexts was evaluated as two copies;
  - `residual variable represented by a fresh constant`: a proof left a
    variable unbound, and gk represented it by a constant that the input
    does not have;
  - a proof step that gk cannot turn into an application (for example an
    arithmetic instance) enters as one **proof application**, with the
    proof's confidence; the line counts such steps in
    `steps_not_represented` ([recursive_output.md](recursive_output.md),
    Section 4).

A value with an approximation note need not equal the semantics of the
snapshot. Other readings name rules of the semantics that applied: for
example `narrowing`, `rank zero as equal rank`, `self exception`, and
`no self-support` (the rule against self-support: an application whose
body can hold only when its head already holds is left out;
[support_semantics.md](support_semantics.md), Section 5.7).
[support_semantics.md](support_semantics.md), Section 10.5, "The readings",
explains the readings in the terms of the semantics, and
[recursive_output.md](recursive_output.md), Section 5, lists all of them.

**Not a bound.** Even when every search of the general method has ended,
an objection or an exception that it did not find can move the value in
either direction. The checkpoints of Section 6.1 move both ways. For a
positive probabilistic logic program, the proofs found so far give a lower
bound of the probability. Here no such bound holds: an opposing proof that
the search finds later can lower the support.

On [`smokes.js`](../Examples/confidences/smokes.js) every search of the
general method ends, and still its value differs from the exact one:

```sh
./bin/gk Examples/confidences/smokes.js             # (.37644, 0, 0, .62356), complete
./bin/gk -general Examples/confidences/smokes.js    # (.38036, 0, 0, .61964)
```

The general method's proof left a variable unbound. gk represented it by
the fresh constant `$k5_2`, and the instances at that constant add
support. The dump records the reading `residual variable represented by a
fresh constant`.

How much of the relevant evidence the search finds before the deadline is
an empirical question. It is separate from the correctness of the
evaluation on a snapshot.

## 9. Function terms and equality

**Why exactness excludes function terms.** With function terms the ground
instances can be infinite, and no finite part of them need settle the
answer. Two small inputs show this:

- [`child_limit.gkp`](../Examples/tutorial/child_limit.gkp):
  `0.5::p(X).` and `0.5::p(X) :- p(child(X)).` A cut at depth n gives
  x0 = .5 and x(n+1) = .5 + .25 × x(n). The values approach 2/3 and never
  reach it.
- [`alternating.gkp`](../Examples/tutorial/alternating.gkp):
  `p(X) :- unless(p(f(X))).` The finite cuts alternate between
  (1, 0, 0, 0) and (0, 0, 0, 1) and have no limit.

Auto sends both inputs to the general method, which answers under its
default budget:

```sh
./bin/gk Examples/tutorial/child_limit.gkp     # p(a): (.666667, 0, 0, .333333)
./bin/gk Examples/tutorial/alternating.gkp     # p(a): (1, 0, 0, 0)
```

Both answers come with stopped or queued searches, and `search` says that
more budget can change the number. The support semantics defines no report
for an infinite grounding. So these values are estimates of the general
method, not values of the semantics.

**An answer without a complete grounding.** The lineage stage
([`tweety_4_lineage.gkp`](../Examples/semantics/tweety_4_lineage.gkp)) has
infinitely many ground instances, but the proof that Tweety is a bird needs
two steps. gk prints (.396, .56, 0, .044), the value of the disjunction
stage, after about 6.8 s. The budget stops four lineage searches: three for
evidence against a bird atom and one for further support. They cannot
change the value here. The lineage gives a certain proof of
`bird(tweety)`, and no clause of the input can give evidence against a bird
atom. This argument holds for this input only. In general a stopped search
leaves the value open.

**Equality.** The semantics has no rule for equality, so the exact method
does not cover it. The general method uses equality by paramodulation. An
equality proof can give the application `p(b) <- p(a), a = b`, and the
equality is then a premise to check.
[`grandfather_equality.js`](../Examples/core/grandfather_equality.js)
states family relations as equalities between terms:

```sh
./bin/gk Examples/core/grandfather_equality.js  # grandfather(mark,mike), grandfather(mark,john): (.9, 0, 0, .1)
```

## 10. Defaults, ranks and taxonomy priorities

A default is a rule with an exception. In GKP:

```prolog
flies(X) :- bird(X), unless(-flies(X), 2).
```

The rule derives `flies(X)` from `bird(X)` unless `-flies(X)` is
established. The number 2 is the rank of the default. When the exception is
the opposite of the rule's own head, the rule is a **normal default**.
Between opposing normal defaults on one atom, the higher positive rank
wins. At equal ranks, or when one rank is 0, neither wins
([support_semantics.md](support_semantics.md), Section 5.4, "Normal
defaults and ranks"). In the Nixon example
([`nixon.gkp`](../Examples/exceptions/nixon.gkp)),

```prolog
quaker(n).
republican(n).
pacifist(X)  :- quaker(X),     unless(-pacifist(X), 2).
-pacifist(X) :- republican(X), unless(pacifist(X), 2).
dislikeswar(X) :- pacifist(X).
query(dislikeswar(X)).
```

the two defaults have equal rank, and `./bin/gk Examples/exceptions/nixon.gkp`
prints (0, 0, 0, 1) for `dislikeswar(n)`: neither default establishes its
head.

A rank can also name a class of the WordNet taxonomy, such as
`tax(penguin)`. Such an input needs `-taxonomy` and the data files of
[`../data/`](../data/README.md). Without `-taxonomy` it is an input error. The exact method does not cover a
taxonomy rank, so Auto sends such an input to the general method. The
general method compares taxonomy ranks by specificity: a more specific
class defeats a more general one.
[`taxonomy_ranks.gkp`](../Examples/tutorial/taxonomy_ranks.gkp) has the
facts `bird(t)` and `penguin(t)`, a flying default of rank `tax(bird)` and
a non-flying default of rank `tax(penguin)`:

```sh
./bin/gk Examples/tutorial/taxonomy_ranks.gkp -taxonomy -datafolder data   # flies(t): (0, 1, 0, 0)
```

The reading
`taxonomy ignored` (a taxonomy rank read as rank 0) applies only where the
evaluator cannot decide whether a taxonomy rank is allowed in the context
of an exception check. The support semantics has no taxonomy ranks.

## 11. Arithmetic

Ground arithmetic is simplified during proof search. For example, `2 + 3`
is evaluated to `5` when all operands are known.

Arithmetic conditions with variables need bounded instantiation. With
`arith_instantiation: 1`, gk considers selected one-variable conditions;
mode `2` also considers selected conditions with two variables. Candidate
and probe limits keep the procedure finite. It is meant for small integer
problems and is not a general constraint solver. The exact method does not
cover built-in conditions.

A proof step with an arithmetic instance enters the general method as a
proof application: one source event with the proof's confidence. The line
counts such steps in `steps_not_represented`
([recursive_output.md](recursive_output.md), Section 4).

## 12. Search control

Resolution is complete only when it runs without restrictive strategy
limits. Practical searches of the general method use time, clause-size and
selection controls. gk generates an ordered sequence of strategies from the
input. Each strategy gets an initial time in which to find a proof. The
first successful strategy gets the remaining time and is reused for the
question's later searches ([strategy_reference.md](strategy_reference.md)).
A strategy file can instead specify:

- clause selection preferences such as `negative_pref` or `query_focus`;
- goal, assumption and axiom queue treatment;
- limits on time, answers, clause size, depth, length and weight;
- equality, rewriting and SINE relevance filtering;
- several runs attempted in sequence.

The exact method does not use a strategy file. Its tasks have their own
work allowances (Section 5).

A fixed set of axioms can be parsed once into shared memory (`-readkb`) and
reused across many queries (`-usekb`). The exact method does not cover an
attached knowledge base, so Auto sends such a query to the general method,
which reads the knowledge base as part of the input
([recursive_output.md](recursive_output.md), Section 1). The options are
described in [`cli_reference.md`](cli_reference.md).

Unit resolution and other short-argument restrictions can be fast but are
incomplete. A timeout or a restrictive strategy therefore means only that
no proof was found under those limits.

## 13. Results without a proof

- A question without variables that gk cannot prove gets the value
  (0, 0, 0, 1): complete ignorance. For
  [`no_proof.gkp`](../Examples/tutorial/no_proof.gkp) (`p(a). query(q(a)).`)
  the line has `"value":[0,0,0,1]`.
- Under the general method, a question with variables without any proof
  gets no value and no answers. The field `stop` says `the recursion did
  not run`, and `unfinished` names the reason.
- The fields `stop` and `search` say why the nested searches stopped and
  what the last search of the question reported. The status facts of the
  dump list what the value does not include
  ([recursive_output.md](recursive_output.md), Section 5).

## 14. The direct method (legacy)

gk also keeps the older direct method of gk 1.1.2. `gk input -direct` runs
it. It does not compute the support semantics.
[direct_method.md](direct_method.md) describes it.

The command-line options are listed in [`cli_reference.md`](cli_reference.md).
Input examples are in [`input_languages.md`](input_languages.md), and
runnable examples are indexed by [`../Examples/README.md`](../Examples/README.md).

