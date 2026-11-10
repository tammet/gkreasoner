# How GK Works

GK uses first-order resolution to find proofs. It then looks for further
support, for opposing evidence and for exceptions, and reports four shares
for the answer: for, against, conflict and ignorance.

This page describes the **recursive method**, which `gk input` runs since
version 1.2.0. What the four shares mean is defined in
[support_semantics.md](support_semantics.md). The output is described in
[recursive_output.md](recursive_output.md). The values below are the output
of gk 1.2.5.

gk also keeps the older **direct method** of gk 1.1.2. `gk input -direct`
runs it, and [direct_method.md](direct_method.md) describes it.
`gk input -audit` runs both methods and prints the direct result as a
labelled comparison.

## 1. Questions and answers

gk converts every input notation to the same internal clause form
([input_languages.md](input_languages.md)). The question is a literal, such
as `flies(tweety)` or `flies(X)`.

gk proves a question by refutation. It adds the negation of the question as
a goal and derives a contradiction. It combines clauses whose complementary
literals unify, applies the resulting substitution, and continues until it
derives the contradiction. For a question with variables, the goal carries
an answer literal `$ans(X)`, and the proof gives the substitution for `X`.

A question without variables gets one value: four shares in the order
(for, against, conflict, ignorance), which sum to 1. A question with
variables gets one value for each ground answer. For
[`penguin.gkp`](../Examples/exceptions/penguin.gkp):

```prolog
bird(b).
penguin(p).
bird(X)   :- penguin(X).
object(X) :- bird(X).
-flies(X) :- penguin(X).
flies(X)  :- bird(X),   unless(-flies(X), 3).
-flies(X) :- object(X), unless(flies(X), 2).
query(flies(X)).
```

```sh
./bin/gk Examples/exceptions/penguin.gkp
```

gk prints one line that starts with `{"recursive":`, then a dump of the
evidence. Shortened, the line lists two answers:

```text
flies(b)  (1, 0, 0, 0)
flies(p)  (0, 1, 0, 0)
```

The ordinary bird `b` flies. For the penguin `p`, the strict rule
`-flies(X) :- penguin(X)` gives the answer "against".

Each answer in the line also carries its resolution proofs, for and against
(the field `proof`). A default proof shows the main structure of the proof:
the steps by which the proof search derived the answer. The nested searches
described below can find sub-proofs for or against these steps. The value
counts them, and `-fullproof` shows them
([recursive_output.md](recursive_output.md) Section 3.1).

## 2. Input confidences

An input confidence is a number between 0 and 1. GKP writes it as a prefix,
`0.8::bird(tweety).`; JSON-LD-LOGIC writes it in the field `@confidence`. A
statement without a confidence has confidence 1.

A confidence is a strength of support, not a probability that the
statement is true. For an unopposed statement it behaves like a probability
([support_semantics.md](support_semantics.md) Section 2). Two statements of
one fact are two routes to it, and they combine by noisy-or (Section 3 of
that page):

```prolog
0.5::bird(a).
0.6::bird(a).
query(bird(a)).
```

gk prints (.8, 0, 0, .2) for `bird(a)`: 1 − (1 − .5)(1 − .6) = .8. Two uses
of one ground statement count once. The instances of one rule at different
constants are different evidence (Section 4 below).

## 3. Two parts of the computation

The reference tool [`mcref`](mcref.md) begins with a finite grounding of
the input. gk instead begins with a proof of the question. It inspects the
proof's steps and searches for further support, for opposing evidence and
for exceptions. It inspects the new proofs in turn, with smaller search
allowances at greater depth. At intervals, one calculation over all the
evidence found so far gives the four shares. Proof search chooses which
evidence to investigate. The support semantics determines how that
evidence affects the answer.

The computation has two parts.

- **Recursive proof expansion** collects applications from proofs
  (Sections 4 to 6).
- **Snapshot evaluation** computes the four shares of the collection
  available so far, called a **snapshot**. It does not sample (Section 7).

A **checkpoint** is one evaluation, after the first search or after a round
of further searches. gk returns the value of the latest completed
evaluation. So a search or an evaluation that runs out of time does not
lose the value already computed.

Sections 3 to 9 describe a question without variables. A question with
variables can give several ground answers, and each gets its own four
shares.

## 4. From a proof to applications

gk searches with resolution and paramodulation, with factoring and
simplification. Resolution combines two clauses by matching opposite
literals. Paramodulation substitutes with an equality. The search works on
clauses with variables, disjunctions, equality and function terms. So gk
does not need all ground instances of the input before it starts.

A proof keeps its parent clauses, its substitutions and its inference
steps, also for a derived lemma. So the method can inspect the premises
behind a compressed proof. The search uses each clause in the directions
of the semantics: an uncertain directed rule and a default supply their
written head only; a certain clause without exceptions and a classical
disjunction can be used in every direction.

The lineage version of the Tweety example
([`tweety_4_lineage.gkp`](../Examples/semantics/tweety_4_lineage.gkp))
shows a first proof. It derives `bird(tweety)` from the register entry
`bird(parent(parent(tweety)))` with two instances of a certain lineage
rule. The .9 flying default then gives a proof of `flies(tweety)`. The
input permits infinitely many lineage terms, but this proof needs only
finitely many. The default's exception and rank stay with the derivation.
So the proof also names the objection to investigate: `-flies(tweety)`.

The **importer** replays the substitutions and forms **applications**. An
application is one use of one input clause. It records a conclusion (the
**head**), conditions (the **body**), exceptions, a confidence and the
identity of its source. The head is the literal of the ground instance that
the proof derives from it. The body is the complements of the other
literals.

- Different uses of one ground application are merged. `0.5::bird(a)` used
  twice is one piece of evidence.
- The instances of `0.9::p(X)` at `a` and at `b` are two pieces of
  evidence.
- An uncertain directed rule contributes its confidence once.
- The orientations of one uncertain classical ground clause share one
  **source event**. The clause is in force in a world or not, as one
  thing.

For example, in the disjunction version of the Tweety example a proof of
`penguin(tweety)` uses the clause `gull(X) ; penguin(X) :- seabird(X)` at
`X = tweety`. The importer records the application
`e4{_0=tweety}:penguin(tweety)`: entry 4 of the input, its ground instance,
and the orientation of that instance with the head `penguin(tweety)` and
the body `seabird(tweety)`, `-gull(tweety)`.

Classical reasoning can give more than a forward use of a rule. An
equality proof can give the application `p(b) <- p(a), a = b`, and the
equality is then a condition to investigate. A proof by cases gives one
combined application. From

```prolog
0.6::a ; b.
0.7::-a ; b.
query(b).
```

resolution derives `b` from both clauses together, and gk prints
(.42, 0, 0, .58), with support .6 × .7. The eliminated case literal `a` is
no condition that must be established. The dump lists the use as an
application with origin `composite`. The semantics builds applications from
one clause at a time and has no such application, so this is a departure
from it (Section 8).

A refutation proof of Q starts from the assumption ¬Q. The proof discharges
that assumption, so the assumption is no negative evidence about Q. A stated
or separately proved ¬Q is.

## 5. Checking the proof recursively

Each application creates search **tasks**:

- for its conclusion: a search for opposition;
- for every condition: a search for opposition and a search for further
  support;
- for every exception: a search for the exception and a search for
  opposition to it.

The question is also searched for further proofs. A proof that a task finds
adds applications, and these create tasks of their own. Equal tasks are
shared: a literal reached twice gets one task.

The yellow-bill version of the Tweety example shows why the checks inside a
proof matter
([`tweety_3a_gull_rule.gkp`](../Examples/semantics/tweety_3a_gull_rule.gkp)):

```prolog
bird(tweety).
0.9::flies(X) :- bird(X), unless(-flies(X), 2).
-flies(X) :- penguin(X), unless(flies(X), 3).
gull(X) ; penguin(X) :- seabird(X).
0.8::seabird(tweety).
0.7::-gull(tweety).
0.9::gull(X) :- seabird(X), yellow_bill(X).
0.6::yellow_bill(tweety).
query(flies(tweety)).
```

With `-checkpoints <dir>` gk writes the dump of each checkpoint:

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
  yellow-bill rule. Where it gives gull positive support, `-gull(tweety)` is
  no usable premise, and part of the penguin proof is defeated. The penguin
  support falls to .8 × .7 × (1 − .6) = .224, and flying gets
  (1 − .224) × .9 = .6984.

The last discovery is not a new proof of flying. It changes the state of a
premise inside the opposing proof. The first two rows are estimates on
incomplete evidence. The for share falls and then rises. A run need not
find exactly one new proof per checkpoint.

The control of the whole method, in pseudocode:

```text
input: the clauses, a ground question Q, the time budget
reserve part of the budget for the evaluations
run a first proof search for Q with a bounded allowance
import its derivations into one shared set of applications S
queue Q, its opposite, and the tasks that the applications create
evaluate S; keep the result if the evaluation completes
for the rounds k = 0, 1, 2, ..., while search time remains:
  choose the runnable tasks: shallowest first, opposition before support
  for each chosen task, at depth d:
    search with the unused part of its allowance A(k, d)
    import the new derivations into S; merge repeated applications
    queue the tasks that their conclusions, conditions and exceptions need
    record whether the attempt ended or was cut by its allowance
  if S changed: evaluate S; keep the result if the evaluation completes
use the evaluation reserve for the latest snapshot not yet evaluated
return the latest completed value, its checkpoint, and the status facts
```

To import a proof means to keep its applications and their identities. The
proof does not become an independent probabilistic fact.

## 6. Contexts, exclusions and the budget

Three choices control the expansion.

**Contexts.** A task is a signed literal with a **context**: the
restrictions inherited from the exception checks that enclose it. Inside
the exception check of a normal default of rank k, a normal default of a
positive rank below k cannot supply the objection. So a weaker default
cannot defeat a stronger one through its exception check. The same literal
in two contexts can need two searches. A source used in both stays one
piece of evidence.

- A normal default's own head complement (the `-flies(X)` of
  `unless(-flies(X), 2)` in a rule for `flies(X)`) is no exception in this
  sense. It marks the default and gives its rank, and it creates no
  exception-check context. The opposition to the default's conclusion is
  still searched, in the inherited context.
- Each other exception literal, and its complement, is searched in the
  context extended by the application's own rank restriction.

**Exclusions.** A search for further proofs of a literal excludes the
literal's known producers: the input entries whose applications concluded
that literal in the task's earlier derivations (and, for the question, in
the first search). The exclusion refuses only a root resolution step that
would derive the literal's ground instance, with its sign, from such an
entry. The entry stays available in every other role: for other instances
and at inner steps. Composite producers are not excluded. So the search
looks for additional evidence and does not return the first proof again.

- A task is **ended** only after a pass that was not cut, with the full
  exclusion set, found nothing new.
- An ended task means that the search strategy finished that attempt. It
  does not mean that all evidence was enumerated.
- A task that recurs on a dependency chain merges with the existing task.

**Allowances.** Work near the question comes first. At depth d in round k
the cumulative allowance of a task is A(k, d) = L0 × 2^k × ρ^d, with
L0 = 50 ms and ρ = .5. A task at depth 1 has 25, 50 and 100 ms in the first
three rounds; each attempt gets the part of the allowance that is still
unused. Within a depth, opposition is searched before alternative support,
because an objection can make an apparently good premise unusable.

The deadline is `-seconds` (default 10 s). The recursive method's budget is
9,000 ms of it. The first proof search gets a quarter of the budget
(2,250 ms at the default), and another quarter is kept for the
evaluations. These are scheduling choices for a useful estimate under a
budget. The semantics does not depend on them.

## 7. Evaluating the collected evidence

The evaluator works on the whole snapshot. Each ground atom and each
source event has one identity. The evaluator does not score separate
proofs and then combine the scores as if they were independent. For

```prolog
0.5::a.
b :- a.
c :- a.
q :- b, c.
query(q).
```

gk prints (.5, 0, 0, .5) for `q`, which is the support of `a`, not .5 × .5.
Both conditions of `q` depend on the same fact. Split the calculation into
two cases. Where `a` is positive, `b`, `c` and `q` are positive. Where `a`
is in ignorance, none of them is established. The two cases have the
weights .5 and .5.

This case split is the central operation. A few terms describe it.

- An **operand read** is one use, by an application, of a body or exception
  literal of another atom.
- The **usability indicator** of a read says whether the literal read is
  usable in a world.
- The **residual dependency closure** of an atom is the set of atoms, not
  yet conditioned on, that it depends on directly or through others.

The evaluator groups the atoms of the snapshot into the vertices of a graph
without cycles: each cycle group becomes one vertex. The orientations of
one uncertain flat ground clause get one two-state source-event vertex.
The evaluator then computes the graph by **recursive conditioning**.

- When the reads of a vertex have disjoint residual dependency closures,
  their usability indicators are independent.
- When two reads share ancestors that are not yet fixed, the evaluator
  conditions on one separator vertex, if one vertex lies on all shared
  paths. Otherwise it conditions on the lowest shared vertices, whose own
  closures are disjoint. It averages the resulting conditional
  distributions and caches repeated calculations.

Within each case the evaluator applies the same supports, kinds, ranks and
state tables as the semantics. For one atom outside a cycle, each
application is present with the probability that its body literals are
usable and its exception literals are not. The evaluator computes, over the
atom's applications, the exact distribution of each side's support, highest
rank and kind. It then averages the state table of the semantics over all
pairs of side states. It integrates the comparisons with the world's
numbers exactly. So the reference tool and gk compute the same quantity by
different means: the tool counts sampled worlds, gk sums weighted cases.

A cycle of one sign without internal exceptions is evaluated as a group.
For each atom of the group, the evaluator divides [0, 1) at the finitely
many support values that subsets of its applications can produce. On each
cell of this division the comparisons with the atom's numbers are
constant, so one sweep of the semantics' procedure gives one state per
cell. A cycle across signs or through exceptions gets a **cycle cut**
(Section 8). The number of cases or cells can be large, so the evaluation
has resource limits.

**When the evaluation is exact.** Call an input clause **Horn-shaped**
when it is a directed clause written with one head literal (a fact, a rule
with confidence below 1, or a default), or a classical clause with at most
one positive atom among its ordinary literals. This is the convention of
the paper behind [support_semantics.md](support_semantics.md), not the
classical definition. Suppose that the snapshot satisfies two conditions:

1. Every step is an instance of a Horn-shaped clause, without composite
   steps, equality, arithmetic or taxonomy ranks, without a residual
   variable and without a rank-context restriction.
2. Every cycle group is a single atom without a self-loop, or a cycle of
   one sign with no exception literal inside it, in which every application
   with a condition inside the cycle is ordinary and its head and inner
   conditions have that sign.

If the evaluation then completes without reaching a resource limit and
without an approximation, the four shares equal the semantics' value for
the evidence in the snapshot. Equality with the value for the whole input
also needs the expansion to have collected every relevant application.
Proving a literal once need not reveal all the applications that support
it, and a deadline need not leave time to find them.

**Eventual exactness.** Take a finite ground input whose relevant part
satisfies the two conditions, with one-sign cycles that settle in every
world. Suppose an unbounded run eventually imports, for every atom that a
task asks for, every reachable application for or against it, and asks for
their conditions and exceptions in turn. Then, with unbounded evaluation
allowances, after finitely many checkpoints gk returns the exact four
shares of the question for the whole input. This is a statement about the
expansion. It does not claim that a run under a deadline meets the
condition.

## 8. What the answer establishes, and what it leaves open

The `{"recursive": ...}` line gives the value of the latest completed
evaluation and the checkpoint it comes from (`value_from`). If the search
advances but the evaluation of the newest snapshot runs out of time, the
previous completed value stays, with its checkpoint number. The dump holds
the proof, the collected applications and the state of each atom.

The output qualifies a value in two ways.

- **Unfinished work** (`status_facts.unfinished`) lists searches that were
  cut or not run, pending proof steps and interrupted evaluations.
- A **reading** (`readings`, and `status_facts.approximation`) records an
  approximation or a convention that the evaluation applied.

An ended search does not certify that no objection exists. A value need not
improve with time: the rows of the table in Section 5 move in both
directions. The union of positive proofs, which ProbLog uses, is a lower
bound of support. An incomplete snapshot is no bound. It can overestimate
the answer, because it may lack an objection or an exception.

Four readings mark departures from the semantics. All four lie outside the
exactness conditions of Section 7.

- **The cycle cut** (`cycle cut`). For a cycle across signs or through
  exceptions, gk walks depth-first from the question atom over the
  applications, in the order its proofs produced them. An application whose
  condition leads back to an atom on the current path, in the same cycle
  group, is removed. An exception that leads back is dropped from its
  application, which stays. The result depends on the question and on the
  order of the proofs. On the certain-rule variant of the Tweety example
  ([`tweety_3b_certain_gull_rule.gkp`](../Examples/semantics/tweety_3b_certain_gull_rule.gkp))
  the cut leaves the semantics' value, (.6984, .224, 0, .0776). On other
  inputs it changes the value.
- **Rank contexts** (`context copies`). The context rule of Section 6 is a
  search rule. The semantics has no contexts. The evaluator copies an atom
  that occurs in two contexts.
- **A residual variable** (`residual variable represented by a fresh
  constant`). A variable that a proof leaves unbound gets a fresh constant.
  The reference tool grounds over the input's constants and has no such
  instance.
- **Composite steps and steps not represented.** A proof by cases gives a
  combined application (Section 4). A proof step that gk cannot yet turn
  into applications, such as a step of gk's word-similarity reasoning,
  enters as one **proof application**, with the proof's confidence as a
  source event and its exceptions attached. The record is removed when
  imported applications cover its evidence. The line counts such steps in
  `steps_not_represented`.

How much of the relevant evidence the search finds before the deadline is
an empirical question. It is separate from the correctness of the
calculation on a snapshot.

## 9. An answer without a complete grounding

[`tweety_4_lineage.gkp`](../Examples/semantics/tweety_4_lineage.gkp)
replaces `bird(tweety)` by a register entry and two certain lineage rules:

```prolog
bird(parent(parent(tweety))).
bird(parent(X)) :- bird(X).
bird(X) :- bird(parent(X)).
```

Their ground instances are infinite, but the proof that Tweety is a bird
needs two steps. gk prints (.396, .56, 0, .044), the value of the
disjunction layer, after about 6.8 s. Four lineage searches are cut by the
budget. They cannot change the value here: the lineage gives a certain proof
of `bird(tweety)`, and no clause of the input gives evidence against a bird
atom. The snapshot does not hold the infinite reachable program, and the
cut searches for evidence against a bird atom do not show that none
exists. In general a cut search leaves the value open.

## 10. Defaults, ranks and taxonomy priorities

A default is a rule with an exception. In GKP:

```prolog
flies(X) :- bird(X), unless(-flies(X), 2).
```

The rule derives `flies(X)` from `bird(X)` unless `-flies(X)` is
established. The number 2 is the rank of the default. When the exception
is the negation of the rule's own conclusion, the rule is a **normal
default**. Between opposing normal defaults, the one of the higher rank
wins; at equal rank neither wins
([support_semantics.md](support_semantics.md) Sections 5 and 6). In the
Nixon example,

```prolog
quaker(n).
republican(n).
pacifist(X)  :- quaker(X),     unless(-pacifist(X), 2).
-pacifist(X) :- republican(X), unless(pacifist(X), 2).
dislikeswar(X) :- pacifist(X).
query(dislikeswar(X)).
```

the two defaults have equal rank, and gk prints (0, 0, 0, 1) for
`dislikeswar(n)`: neither default establishes its conclusion.

A rank can also name a class of the WordNet taxonomy, such as
`tax(penguin)`. Such an input needs `-taxonomy` and the data files of
[`../data/`](../data/README.md); without `-taxonomy` it is an input error.
The recursive method's evaluator reads a taxonomy rank as rank 0 and
records the reading `taxonomy ignored`. The direct method compares taxonomy
ranks by specificity ([direct_method.md](direct_method.md) Section 6).

## 11. Arithmetic

Ground arithmetic is simplified during proof search. For example, `2 + 3`
is evaluated to `5` when all operands are known.

Arithmetic conditions containing variables require bounded instantiation.
With `arith_instantiation: 1`, gk considers selected one-variable
conditions; mode `2` also considers selected conditions with two variables.
Candidate and probe limits keep the procedure finite. It is intended for
small integer problems and is not a general constraint solver.

A proof step with an arithmetic instance enters the recursive method as a
**proof application**: one source event with the proof's confidence. The
line counts such steps in `steps_not_represented`
([recursive_output.md](recursive_output.md) Section 4).

## 12. Search control

Resolution is complete only when it runs without restrictive strategy
limits. Practical searches use time, clause-size and selection controls. gk
generates an ordered sequence of strategies from the input. Each strategy
gets an initial time in which to find a proof. The first successful
strategy gets the remaining time and is reused for the query's later
searches ([strategy_reference.md](strategy_reference.md)). A strategy file
can instead specify:

- clause selection preferences such as `negative_pref` or `query_focus`;
- goal, assumption and axiom queue treatment;
- limits on time, answers, clause size, depth, length and weight;
- equality, rewriting and SINE relevance filtering;
- several runs attempted in sequence.

The deadline is `-seconds` (default 10). The recursive method divides it
between the first proof search, the nested searches and the evaluations
(Section 6).

A fixed set of axioms can be parsed once into shared memory (`-readkb`) and
reused across many queries (`-usekb`). The recursive method runs on such a
knowledge base as on one input file
([recursive_output.md](recursive_output.md) Section 1). The options are
described in [`cli_reference.md`](cli_reference.md).

Unit resolution and other short-argument restrictions can be fast but are
incomplete. A timeout or a restrictive strategy therefore means only that no
proof was found under those limits.

## 13. Results without a proof

- A question without variables that gk cannot prove gets the value
  (0, 0, 0, 1): complete ignorance. For `bird(t). query(flies(t)).` the
  line has `"value":[0,0,0,1]`.
- A question with variables without any proof gets no value and no
  answers. The field `stop` says `the recursion did not run`, and
  `unfinished` names the reason.
- The fields `stop` and `search` say why the nested searches stopped and
  what the last search of the question reported. The status facts of the
  dump list what the value does not include
  ([recursive_output.md](recursive_output.md) Section 5).

The command-line options are listed in [`cli_reference.md`](cli_reference.md).
Input examples are in [`input_languages.md`](input_languages.md), and
runnable examples are indexed by [`../Examples/README.md`](../Examples/README.md).
