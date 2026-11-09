# The support semantics, explained on examples

gk answers a question with four numbers: support for the statement,
support against it, conflict, and ignorance. This page explains what the
four numbers mean. It builds the meaning up from small examples, each of
which you can run. Section 14 states the same rules without examples.

This page is the normative statement of the semantics in this repository.
It follows the paper *Reasoning with Uncertain Evidence, Opposition and
Exceptions: Support Semantics in Three Layers and a First-Order Inference
Method* (T. Tammet, 2026, in preparation). The paper defines the semantics
in its Section 4 and its Appendix A, the reference tool in its Section 5,
and gk's method in its Section 6. Where another document describes the
meaning of the four numbers differently, this page decides. The output of
the recursive method is described in [recursive_output.md](recursive_output.md).
The older direct method is described in [direct_method.md](direct_method.md).

The semantics has three layers. Each layer adds to the previous one and
leaves its answers unchanged.

| layer | what it adds | sections |
|---|---|---|
| 1 | uncertain facts and rules, several routes, shared evidence | 2, 3 |
| 2 | evidence against, exceptions, normal defaults and their ranks, directed rules and classical clauses | 4 to 8 |
| 3 | atoms that depend on each other in a cycle | 9 |

Every number on this page was checked twice, on 2026-11-09. One check used
gk 1.2.3 (the recursive method, `gk FILE`). The other used the standalone
reference tool `mcref` 1.1.1 ([`mcref/`](../mcref/README.md)), which
computes the semantics by random sampling and shares no code with gk's
proof search. The tool ran with 20,000 samples, and its sampling error is
then at most ±.0113 per share for one answer. The two agree on every
example within that error, except on three cycles that Section 9 names.
The inputs are in `Examples/semantics/`.

The examples use the GKP notation: `0.8::bird(t).` is a fact with
confidence .8, `flies(X) :- bird(X).` a rule, `-flies(t)` a negated
statement, `unless(...)` an exception, `;` a classical disjunction, and
`query(...)` the question. The same statements can be written in
JSON-LD-LOGIC ([json_ld_logic.md](json_ld_logic.md)).

## 1. The four states

Take the simplest input:

```prolog
bird(t).
flies(X) :- bird(X).
query(flies(t)).
```

gk answers `flies(t)` with (1, 0, 0, 0): support 1 for the statement,
0 against, 0 conflict, 0 ignorance. Every statement in the input is
certain, and the rule derives the answer.

The four numbers are the shares of four states:

| state | meaning |
|---|---|
| positive | the statement can be used in further reasoning |
| negative | its negation can be used |
| conflict | evidence for both sides passed; neither can be used |
| ignorance | nothing established either side |

The four numbers sum to 1, except where a cycle leaves an atom without a
state (Section 9). The missing share is then reported beside the four
numbers as the **unresolved** share.

"Can be used" is the point of the whole construction. A rule whose body
needs `bird(t)` can apply only where `bird(t)` is in the positive state.
Conflict and ignorance both make the statement unusable; they differ in
why. The numbers are not probabilities that the statement is true in the
world. They say how much of the evidence, under the stated rules, ends in
each of the four states. The **signed confidence**, when one number is
wanted, is the support for minus the support against. Reasoning between
atoms uses the states, not that difference.

**Reading gk's output.** `gk FILE` prints one JSON line that starts with
`{"recursive":`, then a dump. The four numbers are in `value`, in the
order positive, negative, conflict, ignorance. For the opposed facts of
Section 4 the line reads, shortened:

```json
{"recursive":{"question":"flies(a)","value":[0.3,0,0.4,0.3],
  "applications":2,"tasks":2,"tasks_cut":0,
  "stop":"no task can become runnable under a later allowance", ...}}
```

`applications` counts the applications gk found, `tasks` the nested
searches it ran, and `tasks_cut` how many of them a budget stopped. A
cut task means that some evidence may be missing, and the dump names it.
`stop` says why the search ended. A question with a variable gets
`"value": null` and a list `answers`, one entry per instance found:

```json
"answers":[{"answer":"flies(t)","value":[0.9,0,0,0.1]},
           {"answer":"flies(p)","value":[0,1,0,0]}]
```

When gk applied an approximation or a convention of the implementation
to the answer, a list `readings` names it, for example `["cycle cut", ...]`.
Section 12 explains the readings, and
[recursive_output.md](recursive_output.md) lists them.

## 2. An uncertain fact, and what a "world" is

```prolog
0.8::bird(t).
0.9::flies(X) :- bird(X).
query(flies(t)).
```

The answer is (.72, 0, 0, .28). The .72 is .8 × .9. The way the semantics
reaches it is worth seeing, because every later example uses the same
picture.

For every ground statement that evidence can touch (every **atom**, such
as `bird(t)` or `flies(t)`), draw one random number U between 0 and 1,
once for the whole calculation. A complete set of these numbers, one per
atom, is a **world**. In a world, the fact `0.8::bird(t)` establishes
`bird(t)` when its number is below .8: `bird(t)` is positive in 80 % of
worlds and in ignorance in the other 20 %. In a world where `bird(t)` is
positive, the rule applies, and it establishes `flies(t)` with strength
.9: `flies(t)` is positive when its own number is below .9. Over all
worlds, `flies(t)` is positive in .8 × .9 = 72 % of them and in ignorance
in the rest. The report is the share of worlds in each state.

Two remarks. First, a confidence is a **strength of support**, not a
probability that the statement is true: the fact says that evidence of
strength .8 speaks for `bird(t)`. For an unopposed statement the number
behaves like a probability, which is why .72 is also what the
probabilistic logic ProbLog gives for this input. The difference shows
only when evidence is opposed (Section 4). Second, the random numbers
define the shares; they are not part of gk's computation. gk computes the
shares without sampling. The reference tool does sample worlds, and that
is how it estimates the shares and checks gk.

## 3. Several routes to one conclusion

**Two independent routes combine by noisy-or.**

```prolog
0.5::p(heads1).
0.6::p(heads2).
r(c) :- p(heads1).
r(c) :- p(heads2).
query(r(c)).
```

The answer is (.8, 0, 0, .2). In a world, `r(c)` fails to be established
only when both routes fail: (1 − .5) × (1 − .6) = .2. So the support is
1 − .2 = .8. In general the strengths c1, ..., ck of the applications
present for one atom combine into one level, 1 − (1 − c1) × ... × (1 − ck),
and that level is compared once with the atom's number. This is noisy-or:
the side fails only when every present route fails. Two routes of
strength .8 and .6 would give 1 − .2 × .4 = .92; one route alone gives
its own strength.

**Shared evidence counts once.**

```prolog
0.5::a.
b :- a.
c :- a.
q :- b, c.
query(q).
```

The answer is (.5, 0, 0, .5), not (.25, ...). `b` and `c` both come from
`a`, and in every world they read the same state of `a`: both hold in
the half of the worlds where `a` holds, and `q` holds there too. A
calculation that multiplied .5 by .5 would treat the two uses of `a` as
two independent events. The one-number-per-atom rule prevents that: `a`
has one number in each world, and every rule that needs `a` looks at
that same number. Finding the same application in two proofs does not
add its strength twice either.

**Each instance of a rule or fact is its own event.**

```prolog
0.9::p(X).
q :- p(a), p(b).
query(q).
```

The answer is (.81, 0, 0, .19). The uncertain fact `0.9::p(X)` stands for
`p(a)` with strength .9 and `p(b)` with strength .9, and the two have
separate numbers. The fact is not one switch for the whole sentence. The
same holds for a rule: `0.9::flies(X) :- bird(X)` contributes strength .9
at every bird separately.

**Agreement with probabilistic logic programs.** A **positive** program
has facts and rules without negated literals, disjunctions or exceptions.
On every finite positive ground program, cycles included, the semantics
gives the same joint distribution of the positive atoms as the
distribution semantics of ProbLog. A question with probability p there
has the report (p, 0, 0, 1 − p) here (the paper, Theorem 1). The agreement
extends to rules with exceptions on positive atoms when the exceptions
are **stratified**: the atoms can be given levels such that every body
atom of a rule has at most the level of its head and every exception atom
a strictly lower level (the paper, Proposition 1). Only the states
positive and ignorance then occur.

## 4. Evidence against

**Opposed evidence at one atom.**

```prolog
0.7::flies(a).
0.4::-flies(a).
query(flies(a)).
```

The answer is (.3, 0, .4, .3): support .3, conflict .4, ignorance .3. The
evidence for `flies(a)` has strength a = .7 and the evidence against it
strength b = .4. Both are tested against the **same** number U of the atom
`flies(a)`:

| U in | what passes | state |
|---|---|---|
| [0, .4) | both | conflict, share .4 |
| [.4, .7) | only the stronger side | positive, share .3 |
| [.7, 1) | neither | ignorance, share .3 |

This is the second basic rule of the semantics, after
one-number-per-atom: **one shared number for both sides of an atom**.
The weaker side never passes alone; it either passes together with the
stronger side, which is conflict, or fails. In general, with strengths a
for and b against, both sides ordinary:

    positive  = max(a − b, 0)
    negative  = max(b − a, 0)
    conflict  = min(a, b)
    ignorance = 1 − max(a, b)

The shared number is a choice of the semantics, distinct from the
independence inside noisy-or. With a = .8 and b = .3 it gives conflict .3
and positive .5. Two independent tests, one number per side, would give
conflict .24 and positive .56. The confidences alone do not decide between
the two. The paper proves which property singles out the shared number:
among all joint laws of two tests with success chances a and b, it is the
only one under which the weaker test never succeeds alone (the paper,
Proposition 2). Its reading: the weaker evidence can cast doubt on the
stronger, producing conflict, but cannot prevail alone.

**Opposed evidence at a premise.** The contrary report matters even when
it never establishes the negation:

```prolog
0.5::bird(a).
0.3::-bird(a).
0.9::flies(X) :- bird(X).
query(flies(a)).
```

For `bird(a)`: a = .5, b = .3, so `bird(a)` is positive in .2 of the
worlds, conflict in .3, ignorance in .5. Asking `bird(a)` gives
(.2, 0, .3, .5). The rule applies only where `bird(a)` is positive, so
`flies(a)` is positive in .2 × .9 = .18 of the worlds: the answer is
(.18, 0, 0, .82). Nothing speaks against `flies(a)` itself, so its
negative and conflict shares are 0. The .3 of contrary evidence about the
bird did not prove that a does not fly; it removed worlds in which the
bird premise could be used.

A reading of the same input as independent activation probabilities, in
which the contrary fact is simply never used, gives .45. The semantics
gives .18. This is the first place where it departs from ProbLog-style
probabilistic logic, by design.

## 5. Exceptions

A rule may say when it does not apply:

```prolog
bird(t).
0.5::injured(t).
0.9::flies(X) :- bird(X), unless(injured(X)).
query(flies(t)).
```

The answer is (.45, 0, 0, .55). The rule has an **exception** literal,
`injured(t)`. It applies in a world only when its body holds and the
exception is **not usable**, that is, `injured(t)` is not in the positive
state. `injured(t)` is positive in half the worlds. In the other half the
rule applies with strength .9, so `flies(t)` is positive in .5 × .9 = .45
of the worlds. Several exceptions on one rule mean that none of them may
be usable.

An exception is tested for usability, not for truth. An exception in the
conflict state or in ignorance does not block. That is why the contrary
evidence of Section 4 can matter for a default: it can move the
exception's atom out of the positive state. A positive exception
`unless(e)` blocks where `e` is positive; a negative exception
`unless(-e)` blocks where `e` is negative.

**An exception differs from a negated condition.** `-e` as a body literal
is a condition that `e` is negative. `unless(e)` is a condition that `e`
is not positive. The two differ where `e` is in conflict or in ignorance:
there a rule with `unless(e)` applies, and a rule with body `-e` does not.
Where `e` is negative both apply; where `e` is positive neither does.

**A variable that occurs only in the exception** is read as "any
instance":

```prolog
r(a).
0.5::s(a,b).
0.5::s(a,c).
0.9::q(X) :- r(X), unless(s(X,Y)).
query(q(a)).
```

The answer is (.225, 0, 0, .775). Y occurs in the exception only, so the
rule for `q(a)` is blocked when any `s(a,Y)` is usable. `s(a,b)` and
`s(a,c)` have separate numbers; at least one is positive in 1 − .25 = .75
of the worlds. The rule applies in the remaining .25, with strength .9.

## 6. Defaults against each other

Most exceptions in commonsense inputs are of one special shape: the
exception is the negation of the rule's own conclusion. "Birds fly
unless they do not fly" says: use this rule unless the contrary is
established. Such a rule is a **normal default**, after Reiter's normal
default, whose justification is its own conclusion. The number in the
exception is its **rank**, a strength that decides between competing
defaults. `unless(E)` without a number has rank 0. The head's complement
is written as an exception literal, but it is handled specially: it marks
the application as a normal default and supplies its rank, and it is not
used in the test whether the application is present.

**The penguin.**

```prolog
bird(t).
penguin(p).
bird(X) :- penguin(X).
0.9::flies(X) :- bird(X), unless(-flies(X), 2).
-flies(X) :- penguin(X), unless(flies(X), 3).
query(flies(X)).
```

The answers are `flies(t)` (.9, 0, 0, .1) and `flies(p)` (0, 1, 0, 0).
At t only the flying default applies: positive .9. At p both defaults
apply: the flying default with rank 2 and strength .9, the penguin rule
with rank 3 and strength 1. The higher rank wins where both pass; the
penguin rule passes in every world, so `flies(p)` is negative in every
world. Had the penguin rule a strength of .8, it would win in 80 % of
the worlds and the flying default would hold in .9 × .2 = 18 %.

**A default against an ordinary contrary.** The contrary of a default is
not always another default. Compare two inputs that differ in one word:

```prolog
bird(t).
0.3::-flies(t).
0.9::flies(X) :- bird(X), unless(-flies(X), 2).   % a normal default
query(flies(t)).
```

gives (.63, .3, 0, .07), while the same with an ordinary rule

```prolog
0.9::flies(X) :- bird(X).                           % an ordinary rule
```

gives (.6, 0, .3, .1). In the second case both sides are ordinary and
the shared-number rule of Section 4 applies: conflict .3, positive .6.
In the first case the rule says "unless the contrary is established", so
it **yields** to the contrary instead of fighting it: where the contrary
passes (.3 of the worlds) `flies(t)` is negative, with no conflict; where
it fails (.7), the default is tested on its own, and passes with .9: .7 ×
.9 = .63 positive. The remaining .07 is ignorance. A normal default is
tested on a second number of the atom, V, where the ordinary contrary
failed on U; this is how "yields" is made precise.

**Two defaults of equal rank block each other.** The Nixon diamond:

```prolog
quaker(n).
republican(n).
pacifist(X) :- quaker(X), unless(-pacifist(X), 1).
-pacifist(X) :- republican(X), unless(pacifist(X), 1).
query(pacifist(n)).
```

The answer is (0, 0, 0, 1): ignorance, not conflict. Each default is
tested on its own number; where both pass, each blocks the other and
neither is usable. With strengths .8 and .6 on the two rules the answer
is (.32, .12, 0, .56): the first default holds alone in .8 × .4 of the
worlds, the second alone in .6 × .2. If the ranks differ, the higher
one takes the overlap: with rank 2 on the pacifist rule the answer is
(1, 0, 0, 0).

The three cases of this section are the three groups of rows of the
semantics' table for two present sides: ordinary against ordinary (one
shared number, conflict possible), default against ordinary (the default
yields), default against default (equal ranks block each other; unequal
positive ranks nest, and the higher rank wins the overlap). Rank 0 is not
a lower rank: when either normal side has rank 0, the equal-rank row
applies.

**The table in full.** For one atom in one world, the present
applications with head A form the **side for A**, and those with head ¬A
the **side against A**. Let a be the noisy-or strength of the side for A
and b that of the side against A. A side is **normal** when every
application in it is a normal default, and **ordinary** when at least one
is not; this is the **kind** of the side, and it is decided in each world
(Section 8). The rank of a normal side is the largest rank among its
applications. U and V are the atom's two numbers.

| present sides | state |
|---|---|
| none | ignorance |
| for only | positive if U < a; else ignorance |
| against only | negative if U < b; else ignorance |
| both ordinary | positive if b ≤ U < a; negative if a ≤ U < b; conflict if U < min(a, b); else ignorance |
| row 1a: for normal, against ordinary | negative if U < b; else positive if V < a; else ignorance |
| row 1b: for ordinary, against normal | positive if U < a; else negative if V < b; else ignorance |
| row 2: both normal, equal ranks or a rank 0 | P = (U < a), N = (V < b): positive if P and not N; negative if N and not P; else ignorance |
| row 3a: both normal, higher positive rank for | positive if U < a; else negative if U < b; else ignorance |
| row 3b: both normal, higher positive rank against | negative if U < b; else positive if U < a; else ignorance |

A side alone is tested on U whatever its kind (rows "for only" and
"against only"). Averaged over U and V, the "both ordinary" row gives the
four formulas of Section 4. Check the penguin at p against row 3b: a = .9
(the flying default, rank 2), b = 1 (the penguin rule, rank 3); U < 1
always, so negative in every world. Check the default against the fact,
row 1a: negative when U < .3, else positive when V < .9, which is
.7 × .9 = .63.

## 7. Directed rules and classical clauses

The input language has two kinds of rule. A rule with a confidence below
1, or with an exception literal, is **directed**: it supports its written
head only. A certain rule without exceptions, and any clause written as a
disjunction, is **classical**: it can be used in every direction, as in
classical logic.

**A directed rule.** `0.9::flies(X) :- bird(X)` establishes flying from
birdness, and nothing else. A non-flying individual may be one of the
exceptional birds, so nothing follows about its being a bird. Even a
statistical statement that 80 % of birds fly would not fix the proportion
of non-fliers that are non-birds; that needs base rates. The confidence
gives the strength of the directed support, not a full statistical model.

**A disjunction.**

```prolog
0.6::injured(t) ; sick(t).
-sick(t).
query(injured(t)).
```

The answer is (.6, 0, 0, .4). The disjunction says that one of the two
holds, with strength .6. It is used in both directions: `injured(t)` from
`-sick(t)`, and `sick(t)` from `-injured(t)`. Here `-sick(t)` is a fact,
so the first direction gives `injured(t)`. With the disjunction certain
the answer is (1, 0, 0, 0).

An uncertain disjunction used in two directions must not become two
independent chances: it is one statement, in force or not as one thing.
The semantics gives each ground instance of the statement one **source
event**, a hidden atom with one fact of strength .6, and makes both
directions depend on it. In a world the disjunction is in force for both
uses at once, or for neither. A directed rule needs no source event: its
strength is applied at its head directly.

**A certain rule is a certain disjunction.** At confidence 1 without an
exception, `flies(X) :- bird(X)` and `-bird(X) ; flies(X)` are the same
statement, and both are used in every direction. Take

```prolog
flies(X) :- bird(X).
-flies(t).
query(-bird(t)).
```

The answer is (1, 0, 0, 0): `-bird(t)` from `-flies(t)`, the rule read
backwards. At confidence .99 the same question gives (0, 0, 0, 1),
because a directed rule supplies nothing at its body literals. Raising the
confidence of a rule without exceptions from .99 to 1 therefore changes
its meaning. A rule with an exception literal stays directed at
confidence 1.

**The inconsistent world.** Where a certain rule meets certain evidence
against its head, the two directions of the rule meet in one world:

```prolog
0.8::r.
0.2::-p.
p :- r.
query(p).
```

There are four cases, by which of the two facts pass. With r alone (.64),
p is positive. With -p alone (.04), r is negative, by the rule read
backwards. With neither (.16), both atoms are in ignorance. With both
(.16), the chain from r to p starts at an established r and ends at a p
whose complement is established: r and p are both in conflict. The
answer for p is (.64, .04, .16, .16), and the answer for r is the same.
The state of an atom in a world does not depend on which atom was asked.
The two atoms depend on each other through the two directions of the
rule, so they form a cycle, and Section 9 gives the procedure that
reaches these states.

One more rule in the chain does not move the conflict:

```prolog
0.8::r.
0.2::-q.
p :- r.
q :- p.
query(q).
```

The answer is (.64, .04, .16, .16) again, and r, p and q all have this
report: in the .16 of worlds where both facts pass, all three atoms are in
conflict. gk gives the same numbers on both inputs and records the reading
`cycle cut` (Section 9). Section 13 shows what ProbLog and plingo make of
the first input.

## 8. Applications that never apply, and the kind of a side

The semantics works on **applications**: one way of using one ground
statement to establish one literal, with a head, body literals,
exception literals and a strength. A rule gives one application per
ground instance; a disjunction with n literals gives n per instance.

**An exception on one of the application's own body literals.** An
application whose exception literal is one of its own body literals never
applies. Consider `Examples/exceptions/penguin.js`, where "birds fly
unless not flying is established at strength 3" is written as a headless
clause, `-bird(X) ∨ flies(X)` with that exception. Read backwards, it
gives the application "not a bird, from not flying, unless not flying":
its exception is its body. Asked "who is not a bird", gk 1.2.1 derived
`-bird(o)` for an object o that does not fly. Since gk 1.2.2, gk and the
reference tool give ignorance for o, and negative for the bird b and the
penguin p. gk lists the dropped application in its readings as
`self exception`. The rule also covers an exception that matches a body
literal by binding only variables that occur in the exception alone.

**An exception on the default's own atom.** An application whose
exception literal is its own head, with the head's sign, never applies
either:

```prolog
0.5::b.
p :- b, unless(p, 0).
query(p).
```

The answer is (0, 0, 0, 1). This is not a separate rule: the atom p
depends on itself through its exception, so it is a cycle of one atom
through an exception literal, and Section 9 says that such a cycle whose
states alternate leaves its atom in ignorance. With one more fact
`0.3::p` the answer is (.3, 0, 0, .7): the atom keeps only its other
evidence. gk 1.2.3 gives both values; until gk 1.2.2 it read the
exception as a veto by a copy of the atom and gave (.5, 0, 0, .5).

**The kind of a side is decided in each world.** The table of Section 6
needs the kind of each side. A side is normal when every application
present in it, in that world, is a normal default, and ordinary when at
least one present application is not. A consequence: when an ordinary
application and a normal default for the same literal are both present,
the side is ordinary in that world, and the normal default's yielding is
lost there, however small the ordinary application's strength.

```prolog
bird(t).
0.3::-flies(t).
0.9::flies(X) :- bird(X), unless(-flies(X), 2).
0.001::flies(t).
query(flies(t)).
```

The answer is (.6001, 0, .3, .0999). The fact `0.001::flies(t)` has an
empty body, so it is present in every world, and the side for `flies(t)`
is ordinary in every world. Both sides are ordinary, with a = 1 − (1 − .9)
(1 − .001) = .9001 and b = .3. Without the tiny fact the default yields,
and the answer is (.63, .3, 0, .07). The input `mixed_kinds.gkp`, the same
with `0.5::flies(t)`, gives (.65, 0, .3, .05) by the same row.

An ordinary application that is absent in a world does not change the
kind there:

```prolog
bird(t).
0.3::-flies(t).
0.9::flies(X) :- bird(X), unless(-flies(X), 2).
x(t).
-x(t).
0.8::flies(t) :- x(t).
query(flies(t)).
```

The answer is (.63, .3, 0, .07). The two certain facts put `x(t)` in
conflict in every world, so the rule from `x(t)` is present in no world,
and the side for `flies(t)` holds only the normal default. Until gk 1.2.2
gk decided the kind once, over all the applications that could ever
apply, and gave (.6, 0, .3, .1) with the reading `mixed kinds as
ordinary`; gk 1.2.3 gives (.63, .3, 0, .07).

**Unreachable applications.** Before any world is drawn, the semantics
removes every application with a body literal that no chain of
applications can derive from the facts. The chain starts from the facts
and ignores exception literals and opposing evidence. An application
removed this way is present in no world, so the removal changes no
answer. It decides which atoms depend on which (Section 9), and with it
the unused backward directions of certain rules drop out.

## 9. Cycles

Without cycles, the conditions of an atom can be evaluated before the
atom. With cycles, atoms that depend on each other must be evaluated
together.

**Groups and their order.** An atom A **depends on** every atom that
occurs in a body literal or an exception literal of an application with
head A or ¬A, after the removal of unreachable applications (Section 8).
The head's complement on a normal default does not count here, so a
normal default does not make its atom depend on itself. Two atoms are in
one **cycle group** when each depends on the other, directly or through
other atoms. In graph terms, the groups are the strongly connected
components of the dependency relation. The semantics evaluates the groups
in an order in which every group comes after all the atoms it depends on,
so a group reads only final states outside itself. A group of one atom
that does not depend on itself takes its state from the table of
Section 6 in one step. The other groups are of three shapes:

| the group | procedure |
|---|---|
| applications of one sign only, or a cycle through exception literals only | sweeps; if they repeat a state, the narrowing, with an undecided atom read as ignorance |
| a cycle across signs, without a normal default | the narrowing |
| a cycle across signs, with normal defaults | the narrowing, ordinary applications first |

A group has a **cycle across signs** when an application whose head is an
atom of the group has a body literal of the group with the other sign
than its head, or when two applications with a body literal in the group
have heads of opposite signs. Exception literals and facts do not count
in this test.

**One sign: sweeps.** A loop of positive rules settles:

```prolog
0.5::a.
a :- b.
b :- a.
query(b).
```

The answer is (.5, 0, 0, .5): `b` holds where `a` holds. Every atom of
the group starts in ignorance, and a **sweep** recomputes all of them at
once from the states of the previous sweep. When a sweep changes nothing,
the group is settled. Here the first sweep makes `a` positive from its
fact where its number is below .5, the second makes `b` positive from
`a`, and the third changes nothing. A positive cycle cannot support
itself, since the sweeps start from ignorance; this keeps the agreement
with ProbLog of Section 3, positive recursion included.

**Exceptions only: sweeps, then ignorance.** A loop through exceptions
need not settle:

```prolog
p(a) :- unless(b(a)).
b(a) :- unless(p(a)).
query(p(a)).
```

Both atoms start in ignorance, so neither exception is usable, so the
first sweep makes both positive. Now each exception is usable, so the
second sweep makes both ignorant again, and the states repeat. When the
sweeps of such a group repeat a state, the group is evaluated by the
narrowing below, and an atom that the narrowing leaves undecided is read
as **ignorance**. The answer is (0, 0, 0, 1) for both atoms. With
strength .5 on both rules it is (.25, 0, 0, .75): where one rule passes
alone, its head holds; where both pass, the two block each other, and
both atoms are in ignorance. The same holds for three atoms in a ring,
`p :- unless(q). q :- unless(r). r :- unless(p).`: every atom is
(0, 0, 0, 1). The exception on the default's own atom of Section 8 is the
case of one atom.

**Across signs: the narrowing.** For a cycle across signs the semantics
uses a **narrowing** of two sets of literals, an idea familiar from the
well-founded semantics of logic programming. It works in one fixed world,
in which all numbers are drawn and every atom outside the group has its
final state. **Sure** holds the literals of the group that the
computation has justified, and **possible** holds the literals it has not
yet ruled out. The **base** literals are the usable literals of the
outside atoms the group depends on, together with the fixed literals of
the group. Sure starts with the base literals, possible with the base
literals and both literals of every atom of the group. Then, in turn:

1. Rebuild sure from the base literals upward: add a literal when the
   table, counting the applications for it whose bodies are in the set
   being built and whose exceptions are outside the old possible set,
   against the applications against it whose bodies are in the old
   possible set and whose exceptions are outside the old sure set, gives
   its atom that sign.
2. Rebuild possible from the base literals upward in the same way, with
   the applications for the literal read against the new sure set and the
   applications against it read against the new sure set and the old
   possible set.
3. Repeat until neither set changes. Sure only grows, possible only
   shrinks, and sure stays inside possible.
4. An atom with no literal in sure whose table gives conflict, with both
   sides counting the applications with bodies in possible and no
   exception in sure, is **fixed** in conflict. Remove its literals and
   start again with the fixed atoms left out. A fixed conflict stays for
   the rest of the world: the atom supplies no usable literal, even if
   the evidence that produced the conflict becomes unusable later.

At the end an atom with a literal in sure has that sign; an atom with
neither literal in possible is in ignorance; any other atom is
**unresolved**. Section 14.6 states the steps precisely.

On the inconsistent world of Section 7, in the case where both facts
pass, sure stays empty: `r` has its fact for it, but the backward
application `-r` from `-p` is against it with a possible body, so the
table gives conflict, not positive. Possible becomes {r, -p}. Step 4 then
finds conflict at both atoms and fixes them: r and p are in conflict. In
the case where r alone passes, `-p` is not possible, since its fact
fails; in the next round r is sure, and then p is sure: both positive.

**Normal defaults in a cycle across signs.** The ordinary applications of
the group are evaluated first, alone, by the narrowing. Every atom that
ends positive, negative or in conflict is fixed in that state. Then the
normal defaults are added and the atoms still open are evaluated. A normal
default yields to ordinary evidence (Section 6), and this order keeps the
yielding when a normal default could use a certain rule backwards to
defeat the evidence that defeats it.

**Unresolved.** Some cycles leave two atoms each able to block the
other. Two such situations look alike and are reported differently. In
the first, the input has one reading, in which neither atom is
established: the answer is ignorance, as for the mutual pair above. In the
second, the input has two consistent readings that establish opposite
things, and no rule of the semantics prefers one: the procedure gives
the atom no state, and the report says so with the fifth share,
unresolved. The Yale shooting, written with certain rules, is the
standard case:

```prolog
alive(s0).  loaded(s0).  result(s0,s1).  result(s1,s2).  happens(shoot,s1).
alive(S2) :- alive(S1), result(S1,S2), unless(-alive(S2), 1).
loaded(S2) :- loaded(S1), result(S1,S2), unless(-loaded(S2), 1).
-alive(S2) :- happens(shoot,S1), loaded(S1), result(S1,S2).
query(alive(s2)).
```

The reference tool reports `alive(s2)` unresolved in every world: the
four shares are 0, and the unresolved share is 1. The four shares sum to
1 minus the unresolved share, and nothing is rescaled. A group that
depends on an unresolved atom is evaluated by the narrowing whatever its
shape, with the unresolved atom's two literals in possible and neither in
sure. An atom that the group establishes from other evidence gets its
state; an atom whose state would depend on the unresolved one is
unresolved too. So `walks(s2) :- alive(s2)` makes `walks(s2)` unresolved
in every world as well.

**What gk does on cycles.** gk does not implement the narrowing. For a
cycle across signs or through exception literals it applies a **cycle
cut**: it walks depth-first from the question atom over the applications
in the order its proofs produced them, removes an application whose body
literal leads back to an atom on the current path, and drops an exception
literal that does. It records the reading `cycle cut`. On most examples of
this page the cut leaves the value of the semantics. It does not on three:

| input | the semantics (reference tool) | gk 1.2.3 |
|---|---|---|
| `exception_cycle.gkp`, the ring of three exceptions | p (0, 0, 0, 1) | (1, 0, 0, 0), `cycle cut` |
| `yale.gkp` | alive(s2) unresolved 1 | (0, 1, 0, 0), `cycle cut` |
| `yale_walks.gkp` | walks(s2) unresolved 1 | (0, 0, 0, 1), `cycle cut` |

The cut depends on which atom was asked and on the order in which the
proofs were found, so these differences are a property of gk's method,
not of the semantics. Section 12 lists gk's readings.

## 10. Two combined examples

### 10.1 A vet's note

The example below uses many of the pieces: facts, a rule, a normal
default with an external exception, a higher-rank contrary, opposed
facts, and an uncertain disjunction. It needs two exceptions on one rule,
which GKP does not allow, so it is written in JSON-LD-LOGIC
(`Examples/semantics/combined.js`). In words:

    (1) t is a bird.                       (2) p is a penguin.
    (3) penguins are birds.
    (4) .9: a bird flies, unless not flying is established at rank 2,
        and unless the bird is injured.
    (5) a penguin does not fly, unless flying is established at rank 3.
    (6) .5: t is injured.                  (7) .3: t is not injured.
    (8) .6: a vet's note: t is injured or sick.
    (9) t is not sick.
    Question: who flies?

**The applications.** The constants are t and p. The rules (3), (4), (5)
are instantiated at both, which gives 12 ground statements and 14
applications over 10 atoms, the vet's note's source event counted. The
ones that can ever apply:

| from | application | kind | strength |
|---|---|---|---|
| (1), (2), (9) | bird(t); penguin(p); ¬sick(t) | facts | 1 |
| (6), (7) | injured(t); ¬injured(t) | facts | .5; .3 |
| (3) | bird(p) from penguin(p) | ordinary | 1 |
| (4) | flies(t) from bird(t), exception injured(t); the same at p | normal default, rank 2 | .9 |
| (5) | ¬flies(p) from penguin(p) | normal default, rank 3 | 1 |
| (8) | source event s; injured(t) from ¬sick(t) and s; sick(t) from ¬injured(t) and s | ordinary | s .6; the others 1 |

`bird(t) from penguin(t)` and `¬flies(t) from penguin(t)` exist as
applications, but nothing ever establishes `penguin(t)`, so they are
unreachable and present in no world.

**One world.** Take the numbers U = .40 for the source event, .45 for
`injured(t)` and .70 for `flies(t)`. The vet's note is in force (.40 <
.6). `sick(t)` is negative from its fact. `injured(t)` has two present
applications for it, the fact (.5) and the note's direction from
`¬sick(t)` (1), so its positive strength is 1; against it the fact, .3.
Both sides are ordinary and .3 ≤ .45 < 1: `injured(t)` is positive. The
flying default at t has a usable exception, so it is absent, and
`flies(t)` is in ignorance in this world. For p, `bird(p)` is positive
through the penguin, and the flying default (rank 2, .9) meets the
penguin rule (rank 3, 1): the higher rank wins and `flies(p)` is negative.

**All worlds.** When the note is in force (.6 of the worlds), `injured(t)`
has strengths 1 for and .3 against: positive .7, conflict .3. When it is
not (.4), the strengths are .5 and .3: positive .2, conflict .3,
ignorance .5. Together `injured(t)` gets (.5, 0, .3, .2). The flying
default at t is present where `injured(t)` is not positive, half the
worlds, and then passes with .9: `flies(t)` gets (.45, 0, 0, .55).
`flies(p)` gets (0, 1, 0, 0). The contrary injury report (7) never
establishes `¬injured(t)`, yet it matters: it turns .3 of the worlds into
conflict, where the exception does not block.

**The loop.** `injured(t)` depends on `sick(t)` through the note, and
`sick(t)` on `injured(t)` through its other direction. The pair is a
group of two across signs. The direction toward `sick(t)` is never
present, because `¬injured(t)` is never usable: the strength for injury
is at least .5 against .3.

gk 1.2.3 answers `flies(t)` (.45, 0, 0, .55) and `flies(p)` (0, 1, 0, 0),
with the reading `cycle cut` for the loop; the reference tool with 20,000
samples gives (.4534, 0, 0, .5466) and (0, 1, 0, 0).

### 10.2 Tweety, the worked example of the paper

The paper develops one question in four layers: does Tweety fly? The
inputs are `Examples/semantics/tweety_*.gkp`.

**Layer 1, an uncertain exception.** Tweety is a bird. Birds normally fly,
with confidence .9. Penguins normally do not, and the penguin default has
the higher rank. Tweety is a seabird with confidence .8, and a directed
rule supports that a seabird is a penguin with confidence .7:

```prolog
bird(tweety).
0.9::flies(X) :- bird(X), unless(-flies(X), 2).
-flies(X) :- penguin(X), unless(flies(X), 3).
0.8::seabird(tweety).
0.7::penguin(X) :- seabird(X).
query(flies(tweety)).
```

The answer is (.396, .56, 0, .044). Penguin has support .8 × .7 = .56, and
in the remaining .44 the flying default contributes .44 × .9 = .396.

**Layer 2, a disjunction.** Replace the .7 penguin rule by a classical
disjunction and evidence against gull:

```prolog
gull(X) ; penguin(X) :- seabird(X).
0.7::-gull(tweety).
```

The answer is again (.396, .56, 0, .044): the disjunction and the
negative gull evidence give a route to `penguin`. The disjunction alone
establishes neither species.

**Layer 3a, evidence against a premise.** Add a report of a yellow bill,
with confidence .6, and a directed rule with confidence .9 that supports
`gull` for seabirds with yellow bills:

```prolog
0.9::gull(X) :- seabird(X), yellow_bill(X).
0.6::yellow_bill(tweety).
```

Where seabird and yellow bill are established, `gull` has positive
support .9 and negative support .7. Below .7 its number makes both sides
pass: conflict. Between .7 and .9 it is positive. It is never negative in
those worlds, so the penguin proof loses its negative gull premise there.
Penguin now needs the seabird and the negative gull evidence without
usable yellow-bill evidence:

    n = .8 × .7 × (1 − .6) = .224,    p = (1 − n) × .9 = .6984

The answer is (.6984, .224, 0, .0776). There is no conflict at `flies`.

**Layer 3b, the certain gull rule.** Replace the .9 rule by the certain
rule `gull(X) :- seabird(X), yellow_bill(X)`. The rule is now classical:
with not-gull and seabird it supports not-yellow-bill, and with not-gull
and yellow bill it supports not-seabird. The three atoms form a cycle
across signs. In the .336 of worlds where the three input facts pass, the
narrowing fixes all three in conflict, none supplies a usable premise,
and the penguin proof fails there. The answer is again
(.6984, .224, 0, .0776). gk gives it with two `cycle cut` readings.

**Layer 4, a lineage with function terms.** Replace `bird(tweety)` by a
register entry and two certain lineage rules:

```prolog
bird(parent(parent(tweety))).
bird(parent(X)) :- bird(X).
bird(X) :- bird(parent(X)).
```

The ground instances are infinite, but the proof of `bird(tweety)` is
short. gk gives the values of layer 2 in about 7 s at its default
deadline, with four lineage searches cut by the budget. The reference tool
declines the input, because it grounds over constants. The paper argues
that the cut searches cannot change this value: no clause is a source of
negative bird evidence, and a further positive proof cannot raise a
certain support.

| layer | gk 1.2.3 | reference tool, 20,000 samples |
|---|---|---|
| 1 | (.396, .56, 0, .044) | (.3994, .5558, 0, .0449) |
| 2 | (.396, .56, 0, .044) | (.4012, .5567, 0, .0422) |
| 3a | (.6984, .224, 0, .0776) | (.6963, .2252, 0, .0786) |
| 3b | (.6984, .224, 0, .0776), `cycle cut` | (.6963, .2252, 0, .0786) |
| 4 | (.396, .56, 0, .044), four searches cut | declines function symbols |

**How gk reaches layer 3a.** gk's checkpoints show the recursive method
at work (Section 12). After the base proof of flying, the value is
(.9, 0, 0, .1). After the search for not-flying finds the penguin
default, it is (.396, .56, 0, .044). After the search for opposition to
the negative gull premise finds the yellow-bill rule, it is
(.6984, .224, 0, .0776). The last discovery is not another proof of
flying: it changes the state of a premise inside the opposing proof.

## 11. Variables, constants and grounding

The semantics is stated for ground statements. A statement with variables
stands for its instances over the constants of the input, D. A statement
with v variables in its ordinary literals gives up to |D|^v ground
statements: 3 variables over 10 constants give 1,000, most of which have
bodies that nothing establishes and which are never present. A variable
that occurs only in exception literals is not instantiated per
statement; its instances are all exceptions of the one ground statement
(Section 5). A built-in such as `X < 10` is computed after
instantiation. Two statements with the same text are two statements; one
statement instantiated twice with the same constants is one ground
statement.

## 12. How gk computes it, and where it can differ

gk does not enumerate worlds or ground statements. The **recursive
method**, the default since 1.2.0, has two parts.

**Recursive proof expansion.** gk searches for a proof of the question by
resolution and paramodulation, on clauses with variables, disjunctions,
equality and function terms. A proof keeps its parent clauses,
substitutions and steps. gk replays each proof into applications: one per
use of an input statement, with its conditions, exceptions, strength and
source. Different uses of the same ground application are merged, so
using `0.5::bird(a)` twice still refers to one piece of evidence. Each
application creates further search tasks: for its conclusion, a search
for opposition; for every condition, searches for opposition and for
other support; for every exception, searches for whether it holds and for
its opposition. The question itself is searched for further proofs. A
proof that a task returns adds applications and tasks of its own. Equal
tasks are shared. A refutation proof of Q starts from the assumption ¬Q;
it discharges that assumption, so it is not negative evidence about Q.

**The budget.** Work near the question comes first. A task at depth d in
round k has the cumulative allowance L0 × 2^k × ρ^d, with L0 = 50 ms and
ρ = .5, so a task at depth 1 has 25, 50 and 100 ms in the first three
rounds. Within a depth, opposition comes before other support. The
overall deadline is `-seconds` (default 10), and part of the budget is
kept for the evaluation. These are scheduling choices; the semantics does
not depend on them.

**Snapshot evaluation.** At checkpoints gk evaluates all the applications
collected so far, the **snapshot**, by the rules of this page. The
evaluation does not sample. It computes the four shares exactly, by
conditioning on shared atoms and by dynamic programming over each atom's
applications, on the class stated in the paper's Theorem 3: Horn-shaped
steps without composite steps, equality, arithmetic, taxonomy strength,
residual variables or rank contexts; every cycle group of one sign without
an exception inside it; and an evaluation that reaches none of its
resource limits and records no cycle cut. On that class the value is
exact for the evidence in the snapshot. It equals the answer for the
whole input only when the expansion has also found every application the
question depends on, and a finite budget need not find them all.

**What the output qualifies.** gk returns the value of the latest
completed evaluation and names its checkpoint. The status facts list the
unfinished work: searches that were cut or not run, pending steps and
interrupted evaluations. An ended search does not certify that no
objection exists. A value need not improve monotonically with time: the
checkpoints of Section 10.2 move in both directions, and an incomplete
snapshot can overestimate an answer, because it may lack an objection or
an exception.

**The readings.** Four readings mark departures from the semantics of
this page:

- **The cycle cut** (Section 9). gk cuts a cycle across signs or through
  exception literals instead of running the narrowing.
- **Rank contexts.** Inside the exception check of a normal default of
  rank k, gk does not let a normal default of positive rank below k supply
  the objection. This is a search rule. The semantics has no such context,
  and the reference tool declines inputs where it can matter. An atom read
  in two contexts gets the reading `context copies`.
- **A residual variable.** A variable that a proof leaves unbound is
  represented by a fresh constant. The reference tool, which grounds over
  the constants of the input, has no such instance.
- **Composite steps and steps not represented.** A proof by cases gives a
  combined application that no single statement provides: from
  `0.6::a ; b` and `0.7::-a ; b`, resolution derives `b` with support
  .6 × .7 = .42, and the semantics leaves `b` in ignorance. A proof step
  that gk cannot replay as an application enters as a marked **proof
  application**, with the reading `a step not represented`.

**The reference tool** `mcref` 1.1.1 builds all applications by grounding
over D, samples worlds, and counts the states ([mcref.md](mcref.md)). It
is independent of gk's search. To run it on an example:

    python3 mcref/mcref.py Examples/semantics/penguin.gkp --samples 20000

At N samples it reports intervals of half-width √(ln(8/.05) / (2N)) for
the four shares of one answer together, at 95 %: .0113 at 20,000 samples
and .0050 at its default of 100,000. The interval bounds the sampling
error of one answer. It is not a guarantee for all answers of a
collection together, and a value inside it is not thereby exact. The tool
declines equality, function symbols, taxonomy priorities, the rank
contexts above and a few further constructs, with a stated reason.

**The comparison record.** The project keeps a development collection of
1,022 inputs, which is not a held-out benchmark. The tool accepts 360 of
them. On these 360 inputs, gk 1.2.3 and the tool give 438 answer rows; on
394 rows both give a value for the same instance and the tool's
unresolved share is 0, and 375 of them agree within .0113. Of the 19
differences, 12 carry the reading `cycle cut`, 1 a residual variable and 1
a step not represented. 3 carry no reading but searches cut by the
budget, and 2 carry no warning at all. The readings mark an approximation
on the row; they are not a demonstrated cause of the difference.

## 13. Relation to other systems

On positive programs the semantics gives the numbers of the distribution
semantics of ProbLog, PRISM and related probabilistic logic languages
(Section 3). Beyond that fragment, the treatment of opposition (the
shared number), of exceptions and of ranks is a set of stated rules. They
are not consequences of probability theory and need not agree with other
encodings of negation, conflict or priority. The four labels resemble
Belnap's four information states; the rule that a conflicted statement
supports nothing further is this semantics' own. Normal defaults and
ranks relate to Reiter's defaults and Brewka's priorities as related
work, not as a derivation. Executable comparisons with ProbLog, PASTA,
TweetyProject, clingo, DLV and s(CASP) are in
[comparison_with_other_systems.md](comparison_with_other_systems.md).

**The conflict state has no counterpart.** The first example of the
inconsistent world in Section 7, `0.8::r`, `0.2::-p`, `p :- r`, shows
the difference on one case, the one with r and -p both in force (.16):

| system | p | what happens to the inconsistent case |
|---|---|---|
| gk, and this semantics | (.64, .04, .16, .16) | reported as its own share, conflict |
| ProbLog 2.3.0, `-p` written as a separate predicate `neg_p` | p .8, neg_p .2 | counted as p: ProbLog has no classical negation, so `neg_p` has no logical connection to p, and p holds exactly when r holds |
| ProbLog with the evidence "p and neg_p never both" | p .762, neg_p .048 | deleted, the rest scaled up: .64 / .84 and .04 / .84 |
| plingo 1.1.0 (answer sets with classical negation) | p .762, -p .048, neither .190 | deleted: the case has no stable model |

The same case is counted as positive, deleted, or kept apart as
conflict. The .64 of gk is the share where p holds and nothing stands
against it; gk's .64 plus its .16 conflict is ProbLog's .8. On the bird
example of Section 7 the logic-programming systems never derive
`-bird(t)`: a rule is a head and a body for them, and "not a bird" comes
from the closed world, with probability 1, whatever `-flies(t)` says. The
answer (1, 0, 0, 0) is the answer of classical logic.

**Classical reasoning on the certain statements, not in each world.** gk
reasons classically about the certain statements in its search, and
handles uncertain evidence by strengths and one number per atom. On the
bird example every statement is certain, so this looks like reasoning
inside a world of clauses. The two come apart as soon as a statement is
uncertain:

```prolog
0.8::bird(t).
flies(X) :- bird(X).
-flies(t).
query(bird(t)).
```

| treatment | bird(t) |
|---|---|
| gk 1.2.3, the reference tool, and this semantics | (0, .2, .8, 0) |
| a world of sampled clauses, the inconsistent case deleted (ProbLog with evidence, plingo) | bird(t) 0 |
| a world of sampled clauses, the inconsistent case kept as conflict | (0, .2, .8, 0), and every other atom in conflict in that .8 |

The contrapositive gives `-bird(t)` with strength 1, the fact gives
`bird(t)` with strength .8, and the table at `bird(t)` makes it conflict
when U < .8 and negative otherwise. The conflict stays at the atoms of
the cycle. Add an unrelated fact `sings(t)` and ask about it: gk and this
semantics give (1, 0, 0, 0). In a world of sampled clauses with the
conflict kept, the inconsistent case has no place for its conflict, so
`sings(t)` would be (.2, 0, .8, 0). The semantics keeps a contradiction
local (Section 14.9).

**Answer set systems with probabilities.** Where a choice of facts has
several stable models or none, PASTA reports an interval, smProbLog an
equal division of the choice's share among its stable models, and plingo
a normalization over all stable models. On layer 2 of the Tweety example
these give [.18, .396], .288 and .319, and the support share is .396.
These are different quantities, not approximations of one target.

## 14. The rules stated precisely

This section states the rules of the page without examples. It follows
the paper's Section 4 and Appendix A. The direct method's own model is
described in [direct_method.md](direct_method.md). Both of gk's methods approximate
the semantics of this page (Section 12).

**Terms.** An **atom** is a predicate applied to arguments, such as
`flies(t)`. It is **ground** when it has no variables. A **literal** is
an atom or its negation. The **complement** of a literal is the same atom
with the opposite sign. A **statement** is one input fact, rule or
disjunction; gk first turns a general formula into such statements. Its
**confidence** is the number in [0, 1] written on it, and 1 when none is
written.

### 14.1 Two parts

The report of a question is computed from a finite collection of ground
**applications**. Sections 14.2 and 14.3 say which collection the
semantics uses. Sections 14.4 to 14.7 say how a collection receives a
report. gk's methods obtain their applications from proofs instead, and
Section 12 lists where the two collections can differ. An application is
not a proof step. It is a standing possibility, present in every world
where its conditions hold.

### 14.2 Grounding

Let D be the set of constants of the input, the question's constants
included. Every variable of a statement's ordinary literals is replaced
by a constant of D, in every combination. A repeated variable gets the
same constant in each place.

- A variable that occurs only in exception literals is not instantiated
  per statement. All its instances are exceptions of the one ground
  statement, and any usable one blocks it.
- A built-in condition such as `X < 10` is computed after instantiation.
  A true condition is dropped. A false one drops the ground statement.
- Two statements with the same text are two statements. One statement
  instantiated twice with the same constants is one ground statement.

### 14.3 Applications

An application has a **head**, the literal it establishes; **body
literals**, which must be usable; **exception literals**, which must not
be usable; and a **strength** in [0, 1].

| ground statement | applications |
|---|---|
| a fact L | one application: head L, empty body, the fact's confidence |
| a rule with a written head (`H :- B`, `B => H`), with confidence below 1 or with an exception literal | one application: head H, body the literals of B, the rule's confidence (**directed**) |
| a certain rule with a written head and no exception literal | the applications of the certain disjunction of its literals, next row (**classical**) |
| a certain disjunction | one application per literal L: head L, body the complements of the other literals, strength 1 |
| an uncertain disjunction, confidence c | a **source event** s, a new atom with one fact of confidence c; one application per literal as in the row above, with s added to its body, strength 1; each ground instance of the statement has its own source event |

A directed rule is never used at another literal. The applications use
one statement at a time; a consequence that needs several statements at
once, such as a proof by cases, is not an application.

A statement may have exception literals, written `unless(E)`,
`unless(E, k)` or `$block(k, E)`, with an integer rank k ≥ 0;
`unless(E)` alone has rank 0. For each application of the statement:

- If the complement of the head is among the exception literals, the
  application is a **normal default**, and the rank of that literal is
  the application's **rank**. That literal is not used in the test
  whether the application is present: the rows of the table in Section 6
  handle the contrary.
- Every other exception literal is **external**. Every application that
  is not a normal default is **ordinary**.

The test is made per application. So one direction of a disjunction can
be a normal default while another direction is not.

Two kinds of application never apply:

- An application with an external exception literal that is also one of
  its body literals. The test is made after the expansion of
  exception-only variables, so an exception that matches a body literal
  by binding only exception-only variables counts too.
- An application whose body literal no chain of applications can derive
  from the facts. The chain starts from the facts and ignores exception
  literals and opposing evidence. These **unreachable** applications are
  removed before any world is drawn; the removal decides the dependency
  relation of Section 14.6 and changes no answer.

### 14.4 Worlds

For every ground atom A, source events included, take two numbers U_A
and V_A. Each is uniform on [0, 1). They are independent of each other
and of the numbers of every other atom. Nothing else is random, and no
number is drawn again when an atom is used a second time. One assignment
of all these numbers is a **world**. Sections 14.5 and 14.6 give every
atom a state in each world: positive, negative, conflict or ignorance, or
no state, when the atom is unresolved.

### 14.5 The state of one atom

A literal is **usable** when its atom is in the state of its sign: A
positive, or ¬A negative. Conflict and ignorance make neither literal
usable. An application is **present** when every body literal is usable
and no external exception literal is usable. With c the strength of an
application, let

    a = 1 − ∏ (1 − c)   over the present applications with head A
    b = 1 − ∏ (1 − c)   over the present applications with head ¬A

The present applications with head A form the side for A, and those with
head ¬A the side against A. A side is **normal** when every application
in it is a normal default, and **ordinary** when at least one is not; the
kind is decided in each world from the applications present in it. The
rank of a normal side is the largest rank among its applications. Then:

1. If no application with head A or ¬A is present, A is in ignorance.
2. If only one side is present, compare its strength with U_A: A has
   that side's sign when it passes, and is in ignorance otherwise,
   whatever the side's kind.
3. If both sides are present and neither is normal, use the row "both
   ordinary" of the table in Section 6.
4. If both sides are present and at least one is normal, use rows 1a to
   3b of that table. Rank 0 is not a lower rank: when either normal side
   has rank 0, row 2 applies.

### 14.6 Order and cycles

**Dependency.** Atom A depends on every atom in the body literals and the
external exception literals of the applications with head A or ¬A that
remain after Section 14.3. The **cycle groups** are the strongly connected
components of this relation; an atom that is in no cycle forms a group of
its own. In each world:

```
draw U_A and V_A for every ground atom
for each cycle group G, after every group that G depends on:
    if G depends on an unresolved atom outside G:
        run the procedure for G (below), whatever its shape
    else if G is one atom that does not depend on itself:
        its state comes from Section 14.5
    else if G has applications of one sign only, or is a cycle through exception literals only:
        every atom of G starts in ignorance
        repeat a sweep: recompute every atom of G from the states of the previous sweep
            the sweep changes nothing             -> G is settled; its states are final
            the states of G repeat earlier states -> run the procedure for G,
                                                     and read an unresolved atom of G as ignorance
    else:                                          (a cycle across signs)
        run the procedure for G
record the state of the question's atom, unresolved included
```

**The narrowing**, for a given set of applications of G. Literals of the
atoms outside G are read from their final states. For a literal L of G,
an application for L has head L, and an application against L has the
complement of L as its head. The **base** literals are the usable literals
of the outside atoms that G depends on and the literals of the fixed atoms
of G; for an outside atom that is unresolved, nothing.

1. Sure is the base literals. Possible is the base literals, both literals
   of every unfixed atom of G, and both literals of every unresolved
   outside atom.
2. New sure: start from the base literals and repeatedly add a literal L
   of an unfixed atom when Section 14.5 gives L's atom the sign of L,
   counting the applications for L whose body literals are all in the set
   being built and whose exception literals are all outside the old
   possible set, and the applications against L whose body literals are
   all in the old possible set and whose exception literals are all
   outside the old sure set. Stop when nothing more can be added.
3. New possible: start from the base literals and both literals of every
   unresolved outside atom, and repeatedly add a literal L of an unfixed
   atom of G when Section 14.5 gives L's atom the sign of L, counting the
   applications for L whose body literals are all in the set being built
   and whose exception literals are all outside the new sure set, and the
   applications against L whose body literals are all in the new sure set
   and whose exception literals are all outside the old possible set.
4. If neither set changed, go to step 5. Otherwise take the new sets as
   the old ones and repeat from step 2. Sure only grows, possible only
   shrinks, and sure stays inside possible.
5. Every unfixed atom with no literal in sure, whose table gives conflict
   when both sides count their applications with body literals in
   possible and no exception literal in sure, is **fixed** in conflict.
   If any atom was fixed in this step, remove its literals from both sets
   and repeat from step 1 with the fixed atoms left out.

A fact, or an application whose body literals are all base literals, is
counted in both computations, since nothing in G can remove it.

**Selections.** When a side holds normal defaults, "Section 14.5 gives
the sign" is decided over selections of applications. On a side, an
application is certainly present when its body literals are all in the
set that side reads bodies from and its exception literals are all
outside the set it reads exceptions from, and possibly present when the
same holds with the two sets exchanged. In step 2, each side ranges over
all selections between its certainly present and its possibly present
applications, and the sign must hold for every pair of selections. In
step 3, the side of L ranges over all subsets of its possibly present
applications, the opposing side over all selections between its
certainly present and its possibly present applications, and the sign
must hold for some pair. When no side holds a normal default, the single
least favourable selection in step 2 and the single most favourable in
step 3 decide.

**The procedure for G.**

1. If G has normal-default applications, run the narrowing on the
   ordinary applications of G alone, and fix every atom that ends with a
   literal in sure, in that sign, and every atom fixed in conflict. Then
   run the narrowing on all applications, keeping the fixed atoms.
   Otherwise run the narrowing once, on all applications.
2. A fixed atom keeps its state. An atom with a literal in sure has that
   sign. An atom with neither literal in possible is in ignorance. Any
   other atom is **unresolved**.

An atom fixed in conflict keeps that state for the rest of the world.

### 14.7 The report

For a ground question literal Q with atom A, the report is

    R(Q) = (P[A positive], P[A negative], P[A conflict], P[A ignorance])

where P is the share of worlds. Positive and negative are exchanged when
Q is ¬A. The share of worlds in which A is unresolved is reported beside
the four numbers. The four numbers sum to 1 minus that share, and they
are not scaled up. A question with variables gets one report for each
ground instance over D, from the same worlds.

### 14.8 What the rules leave out

- A classical consequence that needs several statements at once is not
  an application. From `a ∨ b`, `¬a ∨ q` and `¬b ∨ q`, resolution proves
  q, while the rules above leave q at ignorance.
- This section gives no rule for equality, function symbols, taxonomy
  priorities or gk's rank contexts (Section 12). The reference tool
  declines inputs that use them, with the reason. The cycle procedure is
  stated for finite ground programs only.

### 14.9 Properties

The paper proves the following for finite ground programs.

- **Agreement with the distribution semantics** (Theorem 1). On a
  positive program, cycles included, the support semantics and the
  distribution semantics give the same joint distribution of the positive
  atoms; a question with probability p has the report (p, 0, 0, 1 − p).
- **Stratified exceptions** (Proposition 1). The agreement extends to
  exceptions on positive atoms that lie at strictly lower levels than the
  heads they block.
- **The shared number** (Proposition 2). Among all joint laws of two
  tests with chances a and b, the shared number is the only one under
  which the weaker test never succeeds alone; both succeed with chance
  min(a, b).
- **A four-state Bayesian network** (Proposition 3). When the dependency
  relation has no cycle, the joint distribution of the states is that of
  a Bayesian network on it, with the conditional probabilities given by
  the table of Section 6. Exact computation of a marginal is therefore
  #P-hard in general. A demonstrator in gk's source repository implements
  both directions of this correspondence: finite acyclic support rules to a
  four-state network, and a finite binary network to support rules. It
  compares gk with the exact values.
- **Well-definedness** (Theorem 2). The narrowing terminates, gives every
  atom one state in each world, unresolved included, and the result does
  not depend on the order of the clauses, of the literals in a clause, or
  of the cycle groups.
- **Locality** (Proposition 4). The report of a question depends only on
  the atoms it depends on, directly or through others, and on their cycle
  groups. A contradiction or an unresolved cycle elsewhere cannot change
  it.

## 15. Glossary

| term | meaning |
|---|---|
| atom | a predicate applied to arguments, `flies(t)`; ground when it has no variables |
| literal | an atom or its negation |
| statement | one input fact, rule or disjunction, with its confidence |
| confidence, strength | the number in [0, 1] on a statement: the strength of the support it contributes where its conditions hold |
| application | one way of using one ground statement to establish one literal: head, body literals, exception literals, strength |
| directed rule | a rule with a written head and a confidence below 1 or an exception literal; used at its written head only |
| classical clause | a certain rule without exceptions, or a disjunction; used in every direction |
| present | an application in a world whose body literals are all usable and whose external exceptions are none usable |
| world | two random numbers U and V per atom (V matters only where a normal default is present); the semantics assigns every atom a state in every world, or none when the atom is unresolved |
| usable | a literal whose atom is in the state of its sign: positive for `A`, negative for `-A` |
| positive, negative, conflict, ignorance | the four states; the report is their shares over worlds |
| unresolved | an atom that the procedure for a cycle across signs leaves possible but not sure; its share is reported beside the four numbers |
| signed confidence | the support for minus the support against |
| noisy-or | the combination of the present applications of one side: 1 − ∏(1 − strength) |
| shared number | the one number U of an atom against which both sides are tested |
| side, kind | the present applications for or against an atom; normal when all are normal defaults, ordinary otherwise, decided in each world |
| normal default | an application whose exception is the complement of its own head; its rank is the number written in that exception |
| rank | the priority of a normal default; rank 0 counts as equal to every rank |
| external exception | any other exception literal; the application is present only when none is usable |
| source event | the hidden atom that makes the directions of an uncertain disjunction one event |
| unreachable | an application with a body literal that no chain of applications from the facts can derive; present in no world |
| depends on | atom A depends on every atom in a body or external exception literal of an application with head A or ¬A |
| cycle group | atoms that depend on each other in a circle (a strongly connected component of the dependency relation) |
| sweep | one recomputation of every atom of a group from the states of the previous sweep |
| narrowing | the computation of the sure and the possible literals of a cycle group (Section 14.6) |
| sure, possible | the literals the narrowing has justified, and the literals it has not yet ruled out |
| fixed | an atom whose final state the procedure has given in this world |
| reading | an approximation or convention of gk that acted on an answer, named in gk's output |
| cycle cut | gk's treatment of a cycle across signs or through exceptions: an application or exception that leads back to the current path is cut |
