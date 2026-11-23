# The support semantics

gk answers a question with four numbers: the support for the question,
the support against it, the share of conflict and the share of ignorance.
This page says what the four numbers mean. It is the repository's
description of the semantics of gk 1.3.1. It follows the paper
*Reasoning with Uncertain Evidence, Opposition and Exceptions: Support
Semantics in Three Layers and a First-Order Inference Method* (T. Tammet,
2026, in preparation) and uses the paper's terms. Where another document
describes the meaning of the four numbers differently, this page decides.

The page starts with a small complete example (Section 1) and the
principles of the definition (Section 2). Sections 3 to 8 give the
definition in the order of the paper, each part on small inputs. Section 9
works through two larger examples. Section 10 says how gk computes the
semantics. Section 11 states the definition as plain rules without
examples, and Section 12 lists the properties that the paper proves.
Section 13 describes the reference tool `mcref`, which computes the
definition directly. Section 15 is a glossary.

The semantics has three layers. Each layer adds constructs. On the inputs
of the layer before it, a layer gives the same answers as that layer.

| layer | what it adds | section |
|---|---|---|
| 1 | uncertain facts and rules, several routes to one conclusion, shared evidence | 4 |
| 2 | evidence against, normal defaults and their ranks, exceptions | 5 |
| 3 | atoms that depend on each other in a cycle | 7 |

**How the values were computed.** Two programs computed every value on
this page. The reference tool `mcref` 1.3.0 computed the value of the
definition by exact evaluation (Section 13). gk 1.3.1 computed its value
with the exact method (`gk -exact FILE`), and the exact method marked each
of these answers complete. The two programs agree on every input of the
page. Where a value comes from gk's general method, the text says so. The
inputs are in [`Examples/semantics/`](../Examples/semantics/README.md);
its README gives the file of each example.

**Notation.** The examples use gk's GKP notation. `0.8::bird(t).` is a fact
with the confidence .8. `flies(X) :- bird(X).` is a rule with the written
head `flies(X)`. `-flies(t)` is the explicit negation of `flies(t)`.
`unless(E)` and `unless(E, k)` are exception literals, the second with the
rank k. `;` is a classical disjunction, and `query(...)` is the question.
A statement without a number is certain: its confidence is 1. The same
statements can be written in JSON-LD-LOGIC
([json_ld_logic.md](json_ld_logic.md)).

## 1. A first example

Take an input with one uncertain fact and one uncertain rule:

```prolog
0.8::bird(t).
0.9::flies(X) :- bird(X).
query(flies(t)).
```

gk answers `flies(t)` with (.72, 0, 0, .28). The semantics reaches this
value in five steps.

1. The input has two ground atoms that evidence can reach: `bird(t)` and
   `flies(t)`. An **atom** is a predicate with its arguments. It is
   **ground** when it has no variables.
2. The semantics gives every ground atom a random number U, uniform
   between 0 and 1. One choice of all these numbers is a **world**. The
   numbers are drawn once for the whole calculation.
3. In a world, the fact `0.8::bird(t)` **passes** when the number of
   `bird(t)` is below .8. Then `bird(t)` is **positive**: it can serve as a
   premise. Otherwise nothing supports `bird(t)`, and it is in
   **ignorance**.
4. In a world where `bird(t)` is positive, the rule supports `flies(t)`
   with the strength .9. This support passes when the number of
   `flies(t)` is below .9.
5. So `flies(t)` is positive in .8 × .9 = .72 of the worlds and in
   ignorance in the rest.

The answer, the **report**, is the share of worlds in each state. With
certain statements only, `bird(t). flies(X) :- bird(X).`, the rule derives
`flies(t)` in every world, and `flies(t)` gets (1, 0, 0, 0). The
random numbers define the shares. gk computes the shares without drawing
numbers. On this input the value .72 is also the probability that
probabilistic logic programming, for example ProbLog, gives (Section 4).

**A contrary report.** Now let a second report contradict the premise:

```prolog
0.5::bird(a).
0.5::-bird(a).
0.9::flies(X) :- bird(X).
query(flies(a)).
```

Three numbers can be argued for `flies(a)`. A reading that ignores the
contrary report gives .5 × .9 = .45. A reading that tests the two reports
independently, and lets `bird(a)` hold where the positive report passes
and the negative one fails, gives .5 × .5 × .9 = .225. The semantics
tests all evidence about one atom on the one number of that atom. The two
reports have the same strength, so wherever one passes, the other passes
too:

| number U of `bird(a)` | what passes | state of `bird(a)` |
|---|---|---|
| below .5 | both reports | conflict |
| .5 or more | neither report | ignorance |

`bird(a)` gets (0, 0, .5, .5). A premise in conflict cannot be used, so
the flying rule never applies, and `flies(a)` gets (0, 0, 0, 1). The
conflict stays at `bird(a)`.

**The four states.** In each world every ground atom has one of four
states, or no value:

| state | meaning |
|---|---|
| positive | the evidence for the atom passed and the evidence against it did not; the atom can serve as a premise |
| negative | the evidence against the atom passed and the evidence for it did not; its negation can serve as a premise |
| conflict | evidence for both signs passed; neither the atom nor its negation can serve as a premise |
| ignorance | no evidence established either sign |

A literal is **usable** when its atom has the state of its sign: `A` is
usable when the atom A is positive, and `-A` when A is negative. The
report of a question gives four **shares**: for (the positive share),
against (the negative share), conflict and ignorance. The shares are
probabilities over worlds. They are not probabilities that the statement
is true. Some inputs with cycles leave an atom with **no value** in some
worlds (Section 7). The share of those worlds is reported beside the four
shares, and the four shares then sum to 1 minus it. The **signed
confidence** is the share for minus the share against. It cannot tell
complete conflict from complete ignorance: both have the signed
confidence 0.

**Reading gk's output.** gk prints one JSON line. For the input
[`against_same_atom.gkp`](../Examples/semantics/against_same_atom.gkp),
`0.7::flies(a). 0.4::-flies(a).`, the command `gk FILE` prints, shortened:

```json
{"recursive":{"method":"recursive","question":["flies","a"],"value":[0.3,0,0.4,0.3],
 "signed_confidence":0.3,"unresolved":0,"proof":{"for":[...],"against":[...]},
 "complete_mode":{"version":"1.3.1","covered":true,"complete":true,...},
 "policy":{"name":"keyfirst","answer_from":"the exhaustive search",...}}}
```

- `value` holds the four shares in the order for, against, conflict,
  ignorance.
- `unresolved` is the share of worlds in which the atom has no value.
- `proof` holds the proofs for and against the answer.
- `"complete": true` in `complete_mode` says that the exact method
  answered and that its value is the value of this semantics for the input
  as gk reads it (Section 10).
- `answer_from` in `policy` names the method that answered: `"the
  exhaustive search"` is the exact method, and `"ordinary gk"` is the
  general method.
- A question with variables gets a list `answers`, with one entry per
  ground answer.
- A list `readings` names procedures and approximations that acted on the
  value (Section 10.5).

[recursive_output.md](recursive_output.md) describes every field.

## 2. The principles

The definition follows three principles. This section states each one on
small inputs. Sections 3 to 7 give the rules.

1. **Uncertain evidence is shared.** An uncertain statement counts once
   wherever it is used. Between two ordinary opposing sides, the evidence
   for and against an atom is tested on one number of the atom. So the
   weaker test passes only where both tests pass (Sections 4 and 5).
2. **Certain clauses are classical, and other rules have a direction.** On
   consistent certain clauses the answers are those of classical logic. A
   rule that is uncertain or has an exception works only towards its
   written head (Sections 3 and 6).
3. **Exceptions are checked before the rules they guard.** The exception
   pass checks external exceptions in layers before it uses the
   applications that they guard, and proofs without exceptions come first.
   Normal defaults are decided directly in the state table of their head
   atom. Atoms that depend on each other get one outcome in each world,
   whatever the order of evaluation (Sections 5 and 7).

With the bird and penguin defaults of Section 9.1, a bird with no further
classification flies and a penguin does not. Two opposing certain facts
put their atom in conflict.

### 2.1 Direction

In a certain clause without an exception, any literal can serve as the
head of an application, and the notation of the clause does not change its
meaning. The certain rule `flies(X) :- bird(X)` with the fact `-flies(a)`
gives `-bird(a)`, the contrapositive inference: `bird(a)` gets
(0, 1, 0, 0).

An uncertain rule says what usually follows from its body. It does not say
what follows when its conclusion fails. In

```prolog
bird(a).
0.9::flies(X) :- bird(X).
-flies(a).
```

the bird `a` is a counterexample to the rule. `bird(a)` keeps
(1, 0, 0, 0), and `flies(a)` gets (0, .1, .9, 0). The rule supports
`flies(a)` with .9, and the certain fact opposes it with 1. The two are
tested on one number. Without the direction, the counterexample would
become evidence against the fact. With the rule written as the clause
`0.9::flies(a) ; -bird(a)`, which has no written head, `bird(a)` gets
(.1, 0, .9, 0).

A rule with an exception is a default. A default that fails for a reason
not listed among its exceptions gives no evidence against its premises.
With `bird(a)`, `-flies(a)` and `flies(X) :- bird(X), unless(penguin(X))`,
`bird(a)` keeps (1, 0, 0, 0). With the same rule written without a head,
`flies(a) ; -bird(a) :- unless(penguin(a))`, `bird(a)` gets (0, 0, 1, 0).
The notation leaves this choice to the author. A written head fixes the
direction. In a clause without a written head any literal can serve as the
head of an application, and the exception stays.

**A head read from a default.** A clause written as a disjunction can have
an exception literal that is the opposite of exactly one literal of its
written consequent. Then that literal is its written head.
`flies(X) ; -bird(X) :- unless(-flies(X))` is read as
`flies(X) :- bird(X), unless(-flies(X))`. The test is made on the
statement as written, before grounding. `p ; r :- b, unless(b)` keeps no
written head, because `-b` is not in its written consequent. In

```prolog
ostrich(os).
-bird(X) ; object(X).
flies(X) ; -bird(X) :- unless(-flies(X)).
-flies(X) ; -object(X) :- unless(flies(X)).
```

the two defaults get the heads `flies(X)` and `-flies(X)`. Nothing says
that `os` is a bird, and `bird(os)` and `flies(os)` both get (0, 0, 0, 1).
Without the reading, both defaults would work in every direction, and a
proof by cases on `flies(os)` would give evidence against `bird(os)`.

### 2.2 The classical proofs come first

A proof that uses no exception is accepted before any rule with an
exception is looked at, and every rule with an exception must accept its
result. In

```prolog
bird(a).
penguin(a).
flies(X) :- bird(X), unless(penguin(X)).
-penguin(X) :- flies(X).
```

the certain rule, read backwards from the fact `penguin(a)`, gives
`-flies(a)`. The flying rule is blocked for `a`. Its conclusion, and the
`-penguin(a)` that the certain rule would derive from it, cannot be used
against the fact. `flies(a)` gets (0, 1, 0, 0), and `penguin(a)` keeps
(1, 0, 0, 0).

A rule whose exception is not established still gives evidence, also
against a certain fact. With `bird(a)`, `-flies(a)` and
`flies(X) :- bird(X), unless(injured(X))`, nothing establishes
`injured(a)`, so the rule applies, and `flies(a)` gets (0, 0, 1, 0).

### 2.3 An exception that cannot hold is dropped

An exception changes an answer only in the worlds where it holds. Where
nothing supports it, the clause counts as the same clause without the
exception. From `p :- f, unless(x)` and `f`, `p` gets (1, 0, 0, 0). With
the fact `x` added, `p` gets (0, 0, 0, 1). With `0.3::x` added, `p` gets
(.7, 0, 0, .3). The principle holds for every input without dependency
cycles. In a cycle it has a limit, which Section 8 states.

### 2.4 Only a proof of the question counts, and its premises must be usable

A contradiction in one place proves nothing about other atoms. With `p`,
`-p` and `r`, an unrelated atom `q` stays at (0, 0, 0, 1), and `r` keeps
(1, 0, 0, 0). A proof may use a literal only when that literal is
established and nothing is established against it. From `p ; r`,
`p ; -r`, `-p` and `q :- p`, the atom `p` is in conflict, (0, 0, 1, 0), and
`q` gets (0, 0, 0, 1).

### 2.5 Nested classes

On positive programs the answers are those of the distribution semantics
of probabilistic logic programming (Section 4). On inputs without
dependency cycles they are the marginals of a Bayesian network whose nodes
have four states (Section 5.8). Sections 5 to 7 say how to evaluate the
inputs outside these classes.

## 3. Statements, applications and proofs

The semantics is stated for a finite set of ground statements. A
**statement** is one input clause: a fact, a rule or a disjunction. It has
its confidence, its written head if it has one, and its exception literals
if it has any. It is **certain** when its confidence is 1 and
**uncertain** otherwise. A statement with variables stands for its ground
instances over the constants of the input (Section 11.2).

| kind | example | how it is used |
|---|---|---|
| certain clause | `p ; r.` `q :- p.` `p.` | any literal can serve as the head of an application |
| uncertain fact | `0.8::p.` | evidence at its atom |
| uncertain clause without a written head | `0.8::p ; r.` | any literal can serve as the head; all uses of one ground instance share one source event |
| uncertain rule | `0.9::flies(a) :- bird(a).` | only towards its head |
| rule with an exception | `flies(a) :- bird(a), unless(penguin(a)).` | only towards its head; the exception stays |
| clause with an exception and no written head | `p ; -f :- unless(x).` | any literal can serve as the head; the exception stays |

Only a written head gives a direction, and only on a statement that is
uncertain or has an exception. A certain rule without an exception is a
certain clause. A rule with a confidence below 1 states a regularity that
admits exceptions, and it supports its written head only. Under
`0.99::flies(X) :- bird(X)` a non-flying individual may be one of the
exceptional birds, and nothing follows about its being a bird. A change of
the confidence from .99 to 1 changes the kind of the statement from a
directed rule to a classical clause (Section 6 shows both values). A rule
with an exception stays directed at confidence 1. An uncertain classical
implication is written as a disjunction with a confidence.

### 3.1 Applications

An **application** is a ground inference step that can conclude one
literal. It has five parts:

- a **head**, the literal it concludes;
- **body literals**, which must be usable;
- **exception literals**, which must not be usable;
- **listed clauses**, which must not be contradicted (only proofs of
  several statements have them, Section 3.3);
- a **strength** in [0, 1].

An application is a standing possibility: it applies in every world where
its requirements hold (Section 5.1).

The **single applications** of a statement:

| statement | its single applications |
|---|---|
| a fact L | one: head L, empty body, the fact's confidence |
| a rule with the written head H that is uncertain or has an exception | one: head H, its body literals, the rule's confidence (**directed**) |
| a certain clause | one for each literal L: head L, the opposites of the other literals as body, strength 1 |
| an uncertain clause without a written head, with the confidence c | a new atom s, its **source event**, with the fact `c::s`; one application for each literal as in the row above, with s added to its body, strength 1 |
| a clause with an exception and no written head | as the two rows above; each application has the exception literals |

Every application of a statement has the exception literals of the
statement.

**A source event makes one statement one event.** An uncertain clause used
in two directions must not become two independent chances. The source
event is in force in a world for every use of the clause, or for none. In

```prolog
0.8::p ; r.
-r.
```

`r` gets (0, 1, 0, 0), and `p` gets (.8, 0, 0, .2) from the clause and
`-r`. In the same way, `0.6::injured(t) ; sick(t)` with `-sick(t)` gives
`injured(t)` (.6, 0, 0, .4), and the certain clause
`injured(t) ; sick(t)` with `-sick(t)` gives (1, 0, 0, 0). A directed rule
needs no source event: its strength counts at its head.

**The identity of an uncertain rule.** An uncertain rule with a written
head and at least one body literal has an **identity**. Its single
application has that identity, and so has every proof that uses the rule.
A rule that several applications use is one rule: it holds or fails once.
A fact, and a rule without a body literal such as
`0.5::a :- unless(-a)`, have no identity. Their uncertainty is a strength
only.

**Normal defaults and external exceptions.** If the opposite of the head
of an application is among its exception literals, the application is a
**normal default**. The rank of that literal is the application's
**rank**. Every other exception literal is **external**. An application
that is not a normal default is **ordinary**. The test is made for each
application, so one direction of a clause without a written head can be a
normal default while another direction is not. Section 5 gives the rules
for both kinds.

**A rule that blocks itself.** A ground rule with a written head whose
external exception literal is also one of its body literals can never
apply. It is excluded, and it takes part in no proof:

```prolog
0.6::r :- e, unless(e).
0.6::r :- -e.
```

`r` gets (0, 0, 0, 1). If the first rule stayed, the two rules would
combine by cases on `e` into "`r`, with no premise, unless `e`", with the
strength .36. The second rule alone has no usable premise.

### 3.2 Premises are checked at their own atoms

In `a. b :- a. q :- b.` the application for `q` uses `b` as a premise. The
evaluator computes the state of `b` separately, at its own atom. In

```prolog
p.
0.8::q :- p.
s :- q.
```

`s` gets (.8, 0, 0, .2). The uncertain rule for `q` cannot enter a proof
of `s`, because it supports only its own head `q`. So `q` is checked as a
premise at its own atom, and the confidence .8 counts once.

### 3.3 Proofs of several statements

Several clauses can support a conclusion together, across alternatives:

```prolog
p ; r.
q :- p.
q :- r.
```

`q` gets (1, 0, 0, 0), while `p` and `r` stay at (0, 0, 0, 1). No single
statement concludes `q`. The three statements together prove it by cases.

A **proof** of a literal Q is a pair (L, G). L is a set of statements, and
G is a set of literals, the **premises**. Neither Q nor its opposite is in
G. The pair must meet four conditions:

1. the clauses of L together with G imply Q classically;
2. the clauses of L together with G are consistent;
3. no smaller L with the same G, and no smaller G with the same L, still
   implies Q;
4. every statement in L with a written head that is uncertain or has an
   exception has Q as its head.

The last condition keeps directed rules directed inside proofs. The
**non-goal clauses** of a proof are the clauses of L that do not contain
Q. The **application of the proof** has:

- the head Q;
- as body, every single literal that G and the non-goal clauses imply, G
  included; these intermediate literals must be usable too;
- the exception literals of every statement in L;
- as listed clauses, the non-goal clauses with several literals, so that
  their contradiction can be checked;
- as strength, the product of the confidences of the uncertain rules of L
  with a written head, whose identities it keeps, so that a shared rule
  counts once;
- as kind, a normal default when L holds a normal default of Q, with the
  smallest rank among them, and ordinary otherwise.

A fact enters a proof as a premise in G, and its confidence counts at its
own atom. An uncertain clause without a written head enters a proof as
"not s, or the clause", with its source event s as a premise. The
application lists the clause itself.

**Uncertain rules count once.** In

```prolog
0.5::p.
0.8::q :- p.
0.8::q :- -p.
```

`q` has two single applications and one proof by cases, which uses both
rules. The proof has an empty body and no listed clause, since both
clauses contain `q`. Its strength is .8 × .8 = .64, and it keeps both rule
identities. Where `p` is positive (a share of .5), the first rule's single
application has the strength .8. The proof by cases needs that rule too,
so the side for `q` has the strength .8. Where `p` is in ignorance (.5),
the proof by cases alone gives .64. The second single application never
applies, because nothing makes `-p` usable. Together:
.5 × .8 + .5 × .64 = .72, and `q` gets (.72, 0, 0, .28).

With nothing known about the case atom, the proof by cases alone gives the
support: `0.6::q :- f. 0.7::q :- -f.` gives `q` (.42, 0, 0, .58), while
`f` stays at (0, 0, 0, 1).

An uncertain clause in a proof brings its source event as a premise:
`0.8::p ; r. q :- p. q :- r.` gives `q` (.8, 0, 0, .2).

**A premise proved by cases.** In

```prolog
a ; b.
0.9::c :- a.
0.9::c :- b.
q :- c.
```

the two uncertain rules for `c` cannot enter a proof of `q`, because a
directed rule enters only a proof of its own head. The proof of `q` takes
`c` as a premise. A separate proof by
cases establishes `c`, with each rule counted once: .9 × .9 = .81. Both
`c` and `q` get (.81, 0, 0, .19).

**The redundancy rule.** The application of a proof of Q is dropped when
another application of Q requires no more. The body literals, exception
literals, listed clauses and uncertain rules of the other application are
all among those of the first. The other application must be certain, or have its uncertainty in a
body literal (an event) or in its rule identities. An application whose
uncertainty is a strength only absorbs nothing: an uncertain fact, and an
uncertain rule without a body literal. A normal default absorbs only a
normal default of the same rank.

In the certain chain `p. q :- p. s :- q.`, the proof of `s` from the two
rules with the premise `p` has the body {`p`, `q`} and lists the clause
`q :- p`. The single application of `s :- q` needs only `q`, has no listed
clause and is certain and ordinary. So the redundancy rule drops the
combined application, and `s` gets (1, 0, 0, 0). An uncertain fact does not
absorb a proof by cases:

```prolog
0.4::q.
0.8::q :- p.
0.6::q :- -p.
```

`q` gets 1 − (1 − .4) × (1 − .8 × .6) = .688, the report
(.688, 0, 0, .312).

## 4. Layer 1: probabilistic support and shared evidence

A **world** gives every ground atom A, source events included, two
numbers U_A and V_A in [0, 1). All numbers are drawn uniformly and
independently, once for the whole calculation. Layer 1 uses only U_A.
Layer 2 needs V_A for normal defaults. An uncertain fact **passes** in a
world when the number of its atom is below its confidence.

**Several routes combine by noisy-or.**

```prolog
0.5::p(heads1).
0.6::p(heads2).
r(c) :- p(heads1).
r(c) :- p(heads2).
query(r(c)).
```

`r(c)` gets (.8, 0, 0, .2). In a world `r(c)` fails only when both routes
fail: (1 − .5) × (1 − .6) = .2. When several applications support one atom
in a world, their strengths c1, ..., ck first combine into one **support
level**,

    1 − (1 − c1) × (1 − c2) × ... × (1 − ck),

and the support level is compared once with the number of the atom. When
proofs share an uncertain rule, the support level is the probability that
at least one application has all its rules, with each rule counted once
(Section 3.3, the example with .72).

**Shared evidence counts once.**

```prolog
0.5::a.
b :- a.
c :- a.
q :- b, c.
query(q).
```

`q` gets (.5, 0, 0, .5), not .25. Both `b` and `c` come from `a`, and in
every world they read the same state of `a`. A calculation that
multiplied .5 by .5 would treat the two uses of `a` as two independent
events. A shared premise has one state in each world.

**Each instance is its own event.** `0.9::p(X). q :- p(a), p(b).` gives
`q` (.81, 0, 0, .19). The uncertain fact stands for `p(a)` and `p(b)`, each
with the strength .9, and the two instances have separate numbers. A fact
in a proof is a premise, and its confidence counts once at its own atom:
`0.4::p. q :- p.` gives `q` (.4, 0, 0, .6).

**Agreement with the distribution semantics.** ProbLog places its random
choices on clause instances and not on atoms. On their common positive
case the two constructions agree. A **positive** program has facts and
rules without negated literals, disjunctions or exceptions. On every
finite positive ground program, cycles included, the support semantics
and the distribution semantics give the same joint distribution of the
set of atoms that come out positive. A question with the probability p
there has the report (p, 0, 0, 1 − p) here (Section 12).

The agreement extends to rules with exception literals `unless(E)` on
positive atoms when the exceptions are **stratified**. Then the atoms can
get levels so that every body atom of a rule has at most the level of its
head. Every exception atom has a strictly lower level. Only the states
positive and ignorance then occur. For example:

```prolog
bird(t).
0.5::injured(t).
0.9::flies(X) :- bird(X), unless(injured(X)).
query(flies(t)).
```

`flies(t)` gets (.45, 0, 0, .55). `injured(t)` is positive in half of the
worlds, and there the rule is blocked. In the other half the rule applies
with the strength .9: .5 × .9 = .45.

## 5. Layer 2: opposing evidence, defaults and exceptions

### 5.1 When an application applies

An atom can be positive, negative, in conflict or in ignorance. A positive
body literal needs the positive state, and a negated body literal needs the
negative state. In conflict and in ignorance neither literal of the atom
can be used.

A literal **has evidence** when its atom has its sign or is in conflict.
The **check of a listed clause** has three results:

- **contradicted**: the opposite of each literal of the clause has
  evidence;
- **not contradicted**: the opposite of some literal certainly has no
  evidence (its atom has a state without that evidence, or it has no value
  and no application can conclude the opposite);
- **cannot be decided**: otherwise. No literal certainly lacks evidence
  against it, and some atom of the clause has no value. The check then
  goes to the procedure of Section 7.

An application **applies** in a world when the exception pass has not
removed it (Section 5.6) and three requirements hold:

- **usable premises**: every body literal is usable;
- **no contradicted clause**: every listed clause is not contradicted;
- **no usable exception**: no external exception literal is usable.

The applications with the head A that apply form the **side for** A, and
those with the head ¬A the **side against** A. The **positive support** a
and the **negative support** b are the support levels of the two sides. A
nonempty side is **normal** when all its applications are normal defaults,
and **ordinary** otherwise. This is the **kind** of the side. The rank of
a normal side is the largest rank of its applications.

Evidence against the head of an application does not discard the
application. It counts as opposing evidence.

### 5.2 Two ordinary sides share one number

When one side is empty, or both sides are ordinary, this table gives the
state of A:

| applications with the head A or ¬A that apply | state of A |
|---|---|
| none | ignorance |
| for A only | positive if U_A < a; else ignorance |
| against A only | negative if U_A < b; else ignorance |
| both | positive if b ≤ U_A < a; negative if a ≤ U_A < b; conflict if U_A < min(a, b); else ignorance |

Both sides are tested on the same number U_A. For example:

```prolog
0.7::flies(a).
0.4::-flies(a).
query(flies(a)).
```

| U of `flies(a)` | what passes | state |
|---|---|---|
| below .4 | both sides | conflict, share .4 |
| .4 to .7 | only the stronger side | positive, share .3 |
| .7 or more | neither side | ignorance, share .3 |

`flies(a)` gets (.3, 0, .4, .3). The weaker side never passes alone. It
passes together with the stronger side, which is conflict, or it fails.
With the strengths a for and b against, both sides ordinary:

    positive  = max(a − b, 0)
    negative  = max(b − a, 0)
    conflict  = min(a, b)
    ignorance = 1 − max(a, b)

`0.8::p. 0.3::-p.` gives `p` (.5, 0, .3, .2). Two independent tests, one
number for each side, would give a conflict of .8 × .3 = .24 and a
positive share of .8 × .7 = .56. The confidences alone do not decide
between the two readings. The paper proves which property selects the
shared number. Take all joint laws of two tests with the success chances a
and b. The shared number gives the only one under which the test with the
smaller chance never succeeds alone (Section 12). The reading: weaker evidence can cast
doubt on stronger evidence and so produce conflict, but it cannot prevail
alone.

**Opposed evidence at a premise.** A contrary report matters even when it
never establishes the negation:

```prolog
0.5::bird(a).
0.3::-bird(a).
0.9::flies(X) :- bird(X).
query(flies(a)).
```

For `bird(a)`, a = .5 and b = .3, so `bird(a)` gets (.2, 0, .3, .5). The
rule applies only where `bird(a)` is positive, so `flies(a)` is positive
in .2 × .9 = .18 of the worlds: (.18, 0, 0, .82). Nothing speaks against
`flies(a)` itself. The contrary report did not prove that `a` does not
fly. It removed worlds in which the bird premise could be used. A reading
as independent activation probabilities, in which the contrary fact is
never used, gives .5 × .9 = .45. This is the first place where the
semantics departs from probabilistic logic programming, by design.

### 5.3 A contradicted listed clause

A premise must be usable: established without conflict. A listed clause
is contradicted as soon as the opposite of each of its literals has
evidence, and conflict counts as evidence. In

```prolog
p ; r.
-p.
-r.
q :- p.
q :- r.
query(q).
```

the proof of `q` by cases has an empty body and lists the clause `p ; r`.
In every world both `-p` and `-r` have evidence, so the clause is
contradicted, the application fails the check, and `q` gets (0, 0, 0, 1).

The check can hold in a part of the worlds:

```prolog
0.8::r.
0.2::-p.
p :- r.
0.9::q :- p.
0.9::q :- -r.
query(q).
```

`q` gets (.7416, 0, 0, .2584). The certain rule `p :- r` is a classical
clause, so `r` and `p` share their states, and the proof of `q` by cases
on `r` lists that clause. The four cases of the two facts:

| facts that pass | share | states of `r` and `p` | support of `q` |
|---|---|---|---|
| `r` only | .64 | positive | .9: the first rule, which the proof by cases also needs |
| `-p` only | .04 | negative | .9: the second rule, likewise |
| both | .16 | conflict | none: the listed clause `p ; -r` is contradicted |
| neither | .16 | ignorance | .81: the proof by cases alone |

.64 × .9 + .04 × .9 + .16 × .81 = .7416.

A proof without a non-goal clause has no listed clause, so it applies also
on a contradiction: `p. -p. q :- p. q :- -p.` gives `p` (0, 0, 1, 0) and
`q` (1, 0, 0, 0).

### 5.4 Normal defaults and ranks

A **normal default** has the opposite of its own conclusion as an
exception: "birds fly unless they are known not to fly". The number in that
exception is the **rank**, a priority between competing defaults. The
exception is written as an exception literal, but it is not tested as an
external exception. It marks the application as a normal default and
gives its rank. The competition is decided in the state table of the head
atom.

When both sides are nonempty and at least one is normal, this table gives
the state of A:

| the two sides | state of A |
|---|---|
| a normal default for A against ordinary evidence | negative if U_A < b; else positive if V_A < a; else ignorance |
| ordinary evidence for A against a normal default | positive if U_A < a; else negative if V_A < b; else ignorance |
| two normal sides of equal rank, or one of rank 0 | with P = (U_A < a) and N = (V_A < b): positive if P and not N; negative if N and not P; else ignorance |
| two normal sides of unequal positive ranks, the higher for A | positive if U_A < a; else negative if U_A < b; else ignorance |
| the same, the higher rank against A | negative if U_A < b; else positive if U_A < a; else ignorance |

Three rules decide the rows of the table.

1. **A default yields to ordinary evidence.** For mixed sides the
   evaluator tests the ordinary side on U_A first. If that test passes,
   the atom takes the sign of the ordinary side, without conflict. If it
   fails, the evaluator tests the normal side on the second number V_A.
   So where the ordinary evidence fails, the default keeps its full
   strength.
2. **Equal ranks block each other.** For two normal sides of equal rank,
   if both tests pass, on U_A and on V_A, the state is ignorance, not
   conflict.
3. **A higher rank wins the overlap.** Between two normal sides with
   unequal positive ranks, the evaluator tests the higher-rank side on U_A
   first. It tests the lower-rank side on U_A only where the first test
   fails.
   A lower-rank default then succeeds only on its strength above the
   higher-rank default.

An exception literal without a number has rank 0, which means that no
priority is stated. Only two positive ranks are compared: when either
normal side has rank 0, the row of equal ranks applies.

**A default against an ordinary contrary.** Compare two inputs that differ
in one exception:

```prolog
bird(t).
0.3::-flies(t).
0.9::flies(X) :- bird(X), unless(-flies(X), 2).
query(flies(t)).
```

gives `flies(t)` (.63, .3, 0, .07). The same input with the ordinary rule
`0.9::flies(X) :- bird(X)` gives (.6, 0, .3, .1). With the ordinary rule,
both sides are ordinary and share one number: conflict .3, positive .6.
With the default, the rule yields: where the contrary passes (.3 of the
worlds), `flies(t)` is negative, without conflict. Where it fails (.7),
the default is tested on V and passes with .9: .7 × .9 = .63.

**The penguin.**

```prolog
bird(t).
penguin(p).
bird(X) :- penguin(X).
0.9::flies(X) :- bird(X), unless(-flies(X), 2).
-flies(X) :- penguin(X), unless(flies(X), 3).
query(flies(X)).
```

The answers are `flies(t)` (.9, 0, 0, .1) and `flies(p)` (0, 1, 0, 0). At
`t` only the flying default applies. At `p` both defaults apply: the
flying default with rank 2 and strength .9, and the penguin default with
rank 3 and strength 1. The higher rank is tested first and passes in every
world. With the confidence .8 on the penguin default, `flies(p)` gets
(.1, .8, 0, .1). The penguin default passes where U < .8. The flying
default has only its strength above .8 left.

**Two defaults of equal rank block each other.** The Nixon diamond:

```prolog
quaker(n).
republican(n).
pacifist(X) :- quaker(X), unless(-pacifist(X), 1).
-pacifist(X) :- republican(X), unless(pacifist(X), 1).
query(pacifist(n)).
```

`pacifist(n)` gets (0, 0, 0, 1): ignorance, not conflict. With the
confidences .8 and .6 on the two defaults it gets (.32, .12, 0, .56). The
first default holds alone in .8 × .4 of the worlds, and the second alone in
.6 × .2. With rank 2 on the pacifist default, the higher rank takes the
overlap, and the answer is (1, 0, 0, 0).

### 5.5 The kind of a side is decided in each world

A side holding both an ordinary application and a normal default is
ordinary. A consequence: where an ordinary application and a normal
default for the same literal both apply, the default does not yield in
that world, however small the strength of the ordinary application.

```prolog
bird(t).
0.3::-flies(t).
0.9::flies(X) :- bird(X), unless(-flies(X), 2).
0.001::flies(t).
query(flies(t)).
```

`flies(t)` gets (.6001, 0, .3, .0999). The fact `0.001::flies(t)` has an
empty body, so it applies in every world, and the side for `flies(t)` is
ordinary in every world. Both sides are ordinary, with
a = 1 − (1 − .9) × (1 − .001) = .9001 and b = .3. Without the small fact
the default yields, and the answer is (.63, .3, 0, .07). The same input
with `0.5::flies(t)` in place of the small fact gives (.65, 0, .3, .05) by
the same row.

An ordinary application that does not apply in a world does not change the
kind there. Add `x(t)`, `-x(t)` and `0.8::flies(t) :- x(t)` to the default
and the contrary report. The two certain facts put `x(t)` in conflict in
every world, so the rule from `x(t)` applies in no world. The side for
`flies(t)` holds only the default, and `flies(t)` gets (.63, .3, 0, .07).

**Normal defaults in proofs of several statements.** A proof whose
statements include a normal default of Q is a normal default of the
smallest of their ranks. In

```prolog
q :- a, unless(-q, 1).
q :- -a.
0.3::-q.
query(q).
```

the proof of `q` by cases on `a` uses the default, so it is a normal
default of rank 1. It yields to the fact `0.3::-q`: `q` gets
(.7, .3, 0, 0). Without the fact, `q` gets (1, 0, 0, 0). An uncertain normal
default takes part in a proof like any other rule, with its identity:
`0.8::flies :- bird, unless(-flies).` and
`0.8::flies :- -bird, unless(-flies).` together give `flies`
(.64, 0, 0, .36), by cases on `bird`. The input

```prolog
d.
a :- -d, unless(f).
0.8::a :- d, unless(-a, 2).
```

gives `a` (.8, 0, 0, .2). The third statement supports `a` from the fact
`d`. It also takes part in a proof by cases on `d` with the second
statement. Both applications have the identity of the one rule, so the
support is .8. Counted as two sources it would be .96.

### 5.6 Exceptions and the exception pass

A rule may say when it does not apply. An external exception is tested
for usability, not for truth: the rule is blocked where the exception
literal is usable. An exception in conflict or in ignorance does not
block. A positive exception `unless(e)` blocks where `e` is positive, and a
negative exception `unless(-e)` blocks where `e` is negative.

**An exception differs from a negated condition.** `-e` as a body literal
is a condition that `e` is negative. `unless(e)` is a condition that `e` is
not positive. The two differ where `e` is in conflict or in ignorance. In

```prolog
0.5::e.
0.5::-e.
p :- unless(e).
r :- -e.
```

`e` is in conflict or in ignorance in every world, (0, 0, .5, .5). So the
rule for `p` applies everywhere, and `p` gets (1, 0, 0, 0), while the rule
for `r` never applies, and `r` gets (0, 0, 0, 1).

**A variable that occurs only in the exception** stands for any instance:

```prolog
r(a).
0.5::s(a,b).
0.5::s(a,c).
0.9::q(X) :- r(X), unless(s(X,Y)).
query(q(a)).
```

`q(a)` gets (.225, 0, 0, .775). The rule for `q(a)` is blocked when any
`s(a,Y)` is usable. `s(a,b)` and `s(a,c)` have separate numbers, and at
least one of them is positive in 1 − .5 × .5 = .75 of the worlds. The rule
applies in the other .25, with the strength .9.

**The exception pass.** An exception is judged before the rule it
guards. The order comes from **layers**. A literal and its opposite get
their layers separately.

- An application without an external exception literal has layer 0. A
  normal default whose only exception literal gives its rank has layer 0.
- An application with external exception literals has the layer 1 + the
  highest layer of those literals.
- The layer of a literal is the highest layer of the applications that
  conclude it, raised to the layer of every body literal of those
  applications and to the layer of the opposite of every literal of their
  listed clauses.
- Where no finite number meets these rules, the layer is the **top**
  layer, which comes after all finite layers.

In each world:

```
for s = 1, 2, ... up to the top layer:
    evaluate, with the applications of layer s and above held out,
        and with the applications removed before left out
    remove every application of layer s that has a usable external exception
evaluate all applications that were not removed
repeat:
    restore every removed application none of whose exceptions that
        removed it is usable now, all at once
    if one was restored, evaluate again
until nothing is restored
```

A restored application is not removed again. The states of the last
evaluation are the states of the world. An application that is held out or
removed is absent. What can be derived only through it counts as not
derivable, and the dependency graph of Section 5.7 is formed again
without it.

The pass has three effects:

- A rule is blocked where the evidence of the lower layers makes its
  exception usable. The consequences of the blocked rule cannot be used
  against the exception.
- A rule with an exception that is not removed counts like any other
  application.
- A rule comes back when other evidence takes the support away from its
  exception.

**The plain penguin.**

```prolog
bird(a).
penguin(a).
flies(X) :- bird(X), unless(penguin(X)).
-flies(X) :- penguin(X).
query(flies(a)).
```

The first evaluation holds out the flying rule of layer 1, establishes
`penguin(a)` and removes the flying rule. `flies(a)` gets (0, 1, 0, 0).
Two layers work the same way. With `zoo(a)`,
`penguin(X) :- zoo(X), unless(tropical(X))` in place of the fact
`penguin(a)`, the penguin rule is judged first, and `flies(a)` gets
(0, 1, 0, 0) again. Three layers:
`a :- unless(b). b :- unless(c). c :- unless(d).` gives `c` and `a`
(1, 0, 0, 0) and `b` (0, 0, 0, 1).

**A restored rule.**

```prolog
e.
p :- unless(e).
-e :- unless(z).
query(p).
```

The fact gives the literal `e` layer 0. The literal `-e` has its own
layer, so both rules have layer 1. At layer 1 both rules are held out: `e`
is positive and removes `p :- unless(e)`, while `-e :- unless(z)` stays.
The next evaluation has the fact `e` and the rule for `-e`, so `e` is in
conflict. The exception of the removed rule is no longer usable, and the
pass restores it: `p` gets (1, 0, 0, 0), and `e` gets (0, 0, 1, 0).

**A blocked rule cannot change a certain fact.**

```prolog
c.
e.
q :- m.
m :- unless(q).
-q :- unless(e).
-c :- -m, unless(z).
query(c).
```

The fact `e` removes `-q :- unless(e)`. Without that rule `-m` cannot be
derived, so the rule against `c` has a body that can never hold, and it is
left out. `c` keeps (1, 0, 0, 0). `m` and `q` get (0, 0, 0, 1).

**An uncertain exception.** `0.3::e. q :- p, unless(e). q :- -p.` gives
`q` (.7, 0, 0, .3). The proof of `q` by cases on `p` uses the first rule,
so it has the exception `e` too. Where `e` is positive (.3), the pass
removes both. Elsewhere the proof by cases applies with the strength 1.

**The classical proofs come first.** Let S be the certain statements of an
input that have no exception. S **blocks** a rule when S entails an
exception literal of the rule other than the opposite of its head. Suppose
that the clauses of S are consistent. Suppose also that every statement
outside S that S does not block is a fact or has a written head, and that
no such head is the opposite of a literal of S. Then the pass removes every
rule that S blocks and never restores it. Every literal that S entails is
usable, and every atom that S decides has its report in S alone (Section
12). The input of Section 2.2
is an example. A rule whose exception is not blocked still gives evidence:
`c` with `-c :- unless(-b)` gives `c` (0, 0, 1, 0).

### 5.7 The dependency graph, and applications that are left out

A literal is **derivable** from a set of applications when a chain of them
derives it from the applications without a body. The chain ignores
exception literals, listed clauses and opposing evidence. After the
proofs are built, two rules leave out applications:

1. **No self-support.** An application with the head L is left out when
   one of its body literals cannot be derived without the applications
   that have the head L. Its body can hold only when its head already
   holds.
2. **A body that can never hold.** An application with a body literal that
   is not derivable at all is left out.

The first rule is applied once, before the second. The **dependency
graph** has the ground atoms as nodes, events included. An atom A depends
on the atoms in the body literals, the external exception literals and the
listed clauses of the remaining applications for A or ¬A. The opposite of
the head on a normal default does not count.

```prolog
0.5::a :- unless(-a).
0.2::-a.
0.5::a :- b.
b :- a.
query(a).
```

`a` gets (.4, .2, 0, .4), and `b` gets (.4, 0, 0, .6). The last two rules
say nothing new about `a`: `a` from `b`, and `b` only from `a`. The rule
`0.5::a :- b` has a body that can hold only when `a` already holds, so it
is left out. `a` gets the value of the first two statements. The default
.5 yields to the fact .2, so `a` is negative in .2 of the worlds and
positive in .8 × .5 = .4. The rule `b :- b` added to this input changes no
value, and `0.5::d. d :- d.` gives `d` (.5, 0, 0, .5). The rule works on
applications, so the clause notation does not matter: `d :- d` and
`d ; -d` lose the same applications. An abbreviation `q :- a. -q :- -a.`
of an atom `a` keeps its two applications for `q` and loses the two for
`a`, when `q` has no other source.

gk prints this rule as the reading `no self-support` of the general method
and the count `left_out_by_no_self_support` of the exact method (Section 10.5).

### 5.8 Without cycles: a Bayesian network

When the dependency graph has no cycle, the answers are those of a
Bayesian network whose nodes have four states. The parents of an atom are
the atoms it depends on. Take an assignment of states to the parents. The
conditional probability of each state of the atom is then the measure of
the pairs (U_A, V_A) for which the two tables above give that state. Any
finite binary Bayesian network with explicit conditional probability
tables can be written at this layer, so the exact computation of a
marginal is #P-hard in general. The graph is built from the applications,
not from the written rules alone. A certain rule has contrapositive
applications too, and a proof by cases reads the atoms of its clauses.

## 6. Agreement with classical logic

Let K be a finite consistent set of certain ground clauses without
exceptions. For every ground atom A: if K entails A, the report of A is
(1, 0, 0, 0); if K entails ¬A, it is (0, 1, 0, 0); otherwise it is
(0, 0, 0, 1). No atom is in conflict, and no world leaves an atom without a
value (Section 12).

**Contraposition at confidence 1.**

```prolog
flies(X) :- bird(X).
-flies(t).
query(-bird(t)).
```

`-bird(t)` gets (1, 0, 0, 0): the certain rule read backwards. At the
confidence .99 the same question gives (0, 0, 0, 1), because a directed
rule supplies nothing at its body literals.

**Direction.** A statement r with a written head H that is uncertain or
has an exception is used only towards H. Every application that uses r,
single or of a proof, has the head H. In a proof that uses r, every other
literal that the proof implies is implied by its premises and its non-goal
clauses without r.

**Equivalent notation.** A change of the notation of a certain statement
without an exception changes no report. `p ; -f.`, `p :- f.` and
`-f :- -p.` give the same reports.

**What a directed statement can change.** A statement with a written head
that is uncertain or has an exception changes only the atom of its head
and the atoms that depend on that head. From `p`, `q :- p`,
`r :- p, unless(e)` and `-r :- p, unless(f)`, the two rules for `r`
contradict each other: `r` gets (0, 0, 1, 0), and `p` and `q` keep
(1, 0, 0, 0). A clause without a written head has no such limit (Section
2.1 shows one).

**The inconsistent world.** Where a certain rule meets evidence against its
head, the two directions of the rule meet in one world:

```prolog
0.8::r.
0.2::-p.
p :- r.
query(p).
```

There are four cases, by the facts that pass. With `r` alone (.64), `p`
is positive. With `-p` alone (.04), `r` is negative, by the rule read
backwards. With neither (.16), both atoms are in ignorance. With both
(.16), the chain from `r` to `p` starts at an established `r` and ends at a
`p` whose opposite is established: `r` and `p` are both in conflict. The
answer for `p` is (.64, .04, .16, .16), and the answer for `r` is the same.
The state of an atom in a world does not depend on which atom was asked.
The two atoms depend on each other through the two directions of the rule,
so they form a cycle, and Section 7 gives the procedure that reaches these
states. One more rule in the chain does not move the conflict: with
`0.2::-q`, `p :- r` and `q :- p`, the atoms `r`, `p` and `q` all get
(.64, .04, .16, .16).

**A contradiction stays local.**

```prolog
0.8::bird(t).
flies(X) :- bird(X).
-flies(t).
query(bird(t)).
```

`bird(t)` gets (0, .2, .8, 0). The contrapositive gives `-bird(t)` with
the strength 1, the fact gives `bird(t)` with .8, and the shared number
makes `bird(t)` conflict where U < .8 and negative elsewhere. `flies(t)`
gets the same report. Add the unrelated fact `sings(t)` and ask about it:
`sings(t)` gets (1, 0, 0, 0). The conflict stays at the atoms of the cycle
(the locality property, Section 12).

## 7. Layer 3: mutually dependent evidence

Without cycles, the conditions of an atom can be evaluated before the
atom. With cycles, atoms that depend on each other are evaluated together.

**Groups and their order.** The strongly connected components of the
dependency graph form **groups**. Each group is evaluated after every group
it depends on, so a group reads only final states outside itself. A single
atom that does not depend on itself is evaluated directly by the tables of
Section 5.

A group has a **cycle across signs** in two cases. In the first, an
application whose head is a literal of the group has a body literal in the
group with the other sign. In the second, two applications with body
literals in the group have heads of opposite signs in the group. Exception
literals and facts do not count in this test.

### 7.1 Sweep groups

A **sweep group** is a group whose applications with a body literal in the
group all have one sign. It has no exception literal in the group and no
normal default. No outside atom that it depends on is without a value. A
sweep group is evaluated by **sweeps**. Every atom of the group starts in
ignorance. One sweep computes every atom of the group from the states of
the sweep before, by the tables. The sweeps repeat until a sweep changes
nothing.

```prolog
0.6::a.
b :- a.
c :- b.
b :- c.
```

`b` and `c` get (.6, 0, 0, .4). Support that goes round a cycle is no
support. The sweeps start from ignorance, so a positive cycle without a
fact stays in ignorance, and `0.5::a. a :- b. b :- a.` gives `b`
(.5, 0, 0, .5). In a sweep group the set of atoms with the group's sign
only grows from sweep to sweep. So the sweeps settle after at most one
sweep more than the group has atoms (the sweep lemma, Section 12). This
keeps the agreement with probabilistic logic programming of Section 4,
positive recursion included.

### 7.2 The narrowing

Every other cyclic group is evaluated by the **narrowing**. The narrowing
follows the well-founded semantics of logic programming. It works in one
fixed world, in which all numbers are drawn and every atom outside the
group has its final state. It keeps two sets of literals of the group:

- **sure** holds the literals that the computation has justified. It is
  built upward from the usable literals outside the group, so no literal
  justifies itself. It only grows.
- **possible** holds the literals that the computation has not yet ruled
  out. It only shrinks.

In outline:

```
sure = the usable outside literals
possible = those, and both literals of every atom of the group
repeat until neither set changes:
    rebuild sure: add a literal when the tables give its atom that sign,
        counting for it the applications with bodies in sure and exceptions outside possible,
        and against it the applications with bodies in possible and exceptions outside sure
    rebuild possible: add a literal when the tables give its atom that sign,
        counting for it the applications with bodies in possible and exceptions outside sure,
        and against it the applications with bodies in sure and exceptions outside possible
fix in conflict every atom without a sure literal whose tables give conflict
    when both sides count their applications with bodies in possible
    and no exception in sure; if one was fixed, start again without it
```

Section 11.7 gives the exact steps. A fixed atom keeps its conflict for
the rest of the world: it supplies no usable literal. At the end, a
literal in sure gives its atom that sign. An atom with neither literal in
possible is in ignorance. Any other atom has **no value** in that world.
In a group without a cycle across signs that depends on no atom without a
value, such an atom is read as ignorance.

**Normal defaults in a group.** When a group contains normal defaults, the
narrowing runs first on the ordinary applications alone. Every atom that
ends with a literal in sure, or fixed in conflict, is fixed in that state.
Then the narrowing runs again on all applications. So the ordinary
conclusions are settled before the defaults are added, and a default
yields to ordinary evidence as in Section 5.4.

**The inconsistent world, again.** In the input `0.8::r. 0.2::-p. p :- r.`
of Section 6, take a world where both facts pass. `r` has its fact for it,
but the application of `-r` from `-p`, the rule read backwards, is against
it with a possible body. So the tables give conflict, not positive, and
sure stays empty. Possible becomes {`r`, `-p`}. The conflict test then
finds conflict at both atoms and fixes them: `r` and `p` are in conflict.
In a world where only `r` passes, `-p` is not possible, since its fact
fails. In the next round `r` is sure, and then `p` is sure: both are
positive.

**Mutual exceptions: ignorance.**

```prolog
a :- unless(b).
b :- unless(a).
```

Both exception literals lie in a cycle, so both rules are in the top
layer. With both held out, neither exception is usable, so the pass
removes nothing. The narrowing then finds neither atom sure and both
possible. The group has no cycle across signs, so both atoms are in
ignorance: `a` and `b` get (0, 0, 0, 1). With the strength .5 on both rules,
`p(a) :- unless(b(a))` and `b(a) :- unless(p(a))` give (.25, 0, 0, .75):
where one rule passes alone, its head holds. Where both pass, they block
each other, and both atoms are in ignorance. The ring
`p :- unless(q). q :- unless(r). r :- unless(p).` gives every atom
(0, 0, 0, 1).

**An exception on the rule's own head atom.** `0.5::b. p :- b, unless(p, 0).`
gives `p` (0, 0, 0, 1). The atom `p` depends on itself through the
exception. The narrowing finds `p` neither sure nor ruled out, and the group
has no cycle across signs, so `p` is in ignorance. With `0.3::p` added, `p`
gets (.3, 0, 0, .7). Where the fact passes, the exception pass removes the
rule, and the fact makes `p` positive. Elsewhere `p` is in ignorance as
before. The atom keeps only its other evidence.

**A withdrawn support.** `p :- unless(u). p :- p. u :- p. u.` gives `p`
(0, 0, 0, 1). The fact `u` makes the exception usable, so the exception
pass removes `p :- unless(u)`. The rule `p :- p` can support `p` only
where `p` already holds, so it is left out.

### 7.3 No value

Mutually excluding defaults without a priority, on different atoms, are
the main source of no value:

```prolog
on(a) :- unless(-on(a)).
on(b) :- unless(-on(b)).
-on(a) ; -on(b).
query(on(a)).
```

The input has two consistent readings, one with `on(a)` and one with
`on(b)`, and no rule of the semantics prefers one. Neither atom gets a
value in any world: `on(a)` and `on(b)` get (0, 0, 0, 0) with the no-value
share 1. Compare the mutual exceptions above. That input has one reading,
in which neither atom is established, and the answer is ignorance.

The Yale shooting, written with certain rules, is a standard case:

```prolog
alive(s0).  loaded(s0).  result(s0,s1).  result(s1,s2).  happens(shoot,s1).
alive(S2) :- alive(S1), result(S1,S2), unless(-alive(S2), 1).
loaded(S2) :- loaded(S1), result(S1,S2), unless(-loaded(S2), 1).
-alive(S2) :- happens(shoot,S1), loaded(S1), result(S1,S2).
query(alive(s2)).
```

`alive(s2)` has no value in every world: the four shares are 0, and the
no-value share is 1. Nothing is rescaled. A group that depends on an atom
without a value is evaluated by the narrowing, whatever its form. An atom
that the group establishes from other evidence gets its state. An atom
whose state would depend on the atom without a value has no value too. So
`walks(s2) :- alive(s2)` gives `walks(s2)` no value in every world.

### 7.4 The clause rule

A proof's conclusion can contribute to evidence against its own listed
clause. The check of the listed clause then depends on its own result. The
**clause rule** resolves this in each world:

1. Evaluate the group with no listed clause of the cycle counted as
   contradicted.
2. Collect the listed clauses that come out contradicted.
3. Leave out every proof that lists one of them, and evaluate again.
4. Repeat until no new clause appears. Then this is the result.
5. If a collected clause stops being contradicted, or a check cannot be
   decided, the rule ends without a result. An atom that had the same state
   in every evaluation of the rule keeps it, and the other atoms of the
   group have no value in that world.

```prolog
p ; r.
q :- p.
q :- r.
-p :- q.
-r.
query(q).
```

The proof of `q` by cases lists `p ; r`. With the proof, `q` holds and
gives `-p`, so both `-p` and `-r` have evidence, and the clause is
contradicted. The rule leaves the proof out. `q` gets (0, 0, 0, 1), and `p`
and `r` get (0, 0, 1, 0): the values of the input without `q :- r`. With
`0.9::-p :- q` in place of `-p :- q`, `p` gets (.1, 0, .9, 0), `q`
(.1, 0, 0, .9) and `r` (0, .1, .9, 0). When both settings are consistent,
the rule starts with the proof included, and the proof applies:

```prolog
p ; r.
q :- p.
q :- r.
-r.
s.
0.9::-p :- s.
0.9::-s :- q.
query(q).
```

`q` gets (.91, 0, 0, .09).

**The clause rule without a result.**

```prolog
p.
0.9::p :- q.
0.9::a ; b.
0.9::q :- a.
0.9::q :- b.
0.9::-a :- q, p.
0.9::-b :- q.
query(q).
```

Take the worlds where the five uncertain statements other than the rule for
`p` hold (.9^5 = .59049). There the proof of `q` by cases gives `-a` and
`-b`, which contradict its clause
`a ; b`. Without the proof the clause is not contradicted. `q`, `a` and
`b` differ between the two evaluations, so they have no value there. `p`
is in the same group, but it is positive in both evaluations, from its
fact. `q` gets (.13851, 0, 0, .271) with the no-value share .59049; `a` gets
(.06561, .06561, 0, .27829) with the same no-value share, and `p` keeps
(1, 0, 0, 0).

**A check that cannot be decided.**

```prolog
p :- unless(-p).
w :- unless(-w).
-p :- w.
c.
-c.
p ; c.
q :- p.
q :- c.
query(q).
```

`p` and `w` have no value, `-p` can be concluded, and `c` is in conflict.
So the check of the listed clause `p ; c` cannot be decided, and `q` has no
value in every world. `c` gets (0, 0, 1, 0). An atom without a value whose
opposite no rule concludes leaves a clause uncontradicted: in the input

```prolog
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

`d` has no value in every world, but no application concludes `-d`, so the
clause `a ; d` is not contradicted, and `q` gets (1, 0, 0, 0).

**After the rule.** The settings of the listed clauses exist only inside
the rule. An application outside the group checks a listed clause on the
final states of the group's atoms (Section 11.8):

```prolog
p ; r.
-p.
-r.
0.5::t.
0.9::q :- p, t.
0.9::q :- r, t.
0.9::-p :- q.
s :- p.
s :- r.
query(s).
```

`p`, `r` and `q` form one group, and `p` and `r` are in conflict in every
world. `s` is a group of its own after it. Its proof by cases lists
`p ; r`, which is contradicted on the final states, so that proof does not
apply. The rules `s :- p` and `s :- r` do not apply either, because a
literal of an atom in conflict is not usable. `s` gets (0, 0, 0, 1), with
either confidence of `t`.

### 7.5 The Tweety cycle

In the certain yellow-bill stage of Section 9.1, the contrapositive
applications of `gull(X) :- seabird(X), yellow_bill(X)` put `seabird`,
`yellow_bill` and `gull` in one group with a cycle across signs. In the
worlds where all three facts pass (.8 × .7 × .6 = .336), sure stays empty,
and possible converges to `seabird`, `yellow_bill` and `-gull`. The
narrowing fixes all three atoms in conflict at once. None is usable, the
penguin proof fails there, and `flies(tweety)` gets
(.6984, .224, 0, .0776).

### 7.6 Properties of the procedure

The paper proves four facts about the procedure. The narrowing reaches
unique fixed points. The exception pass ends. Every atom gets exactly one
of the states positive, negative, conflict, ignorance and no value. And
the result does not depend on the order of the statements, the order of
the literals in a clause, the names of the atoms or the order in which
independent groups are evaluated. Each group reads only the groups it
depends on. So a contradiction or an atom without a value elsewhere cannot
change an answer (locality, Section 12).

Take a group without a normal default whose clause rule, if it ran, ended
with a result. In such a group no atom is positive or negative only through
applications that lead back to its own literal (no self-support, Section
12).

**The well-founded semantics.** With exceptions inside cycles, the
semantics relates to the well-founded semantics of logic programming.
Take a program of certain positive rules, with the exceptions read as
negation as failure. Every atom that is true in its well-founded model gets
(1, 0, 0, 0). Every atom that is false in it gets (0, 0, 0, 1) (Section
12). An atom undefined in the well-founded model has no such
constraint. In `c :- unless(d). d :- unless(c). g :- unless(c).` all three
atoms are undefined in the well-founded model, while here `c` and `d` get
(0, 0, 0, 1), and `g` gets (1, 0, 0, 0).

## 8. Stated limits

The definition has limits of three kinds.

**Constructs outside the definition.**

- *Equality and function terms.* The semantics covers finite ground
  inputs over the constants of the input and the question. It has no rule
  for equality, and it defines no report for an infinite grounding. On
  `0.5::p(X). 0.5::p(X) :- p(child(X)).` a truncation at the depth n gives
  x0 = .5 and x(n+1) = .5 + .25 × x(n), which approaches 2/3 without
  reaching it. On `p(X) :- unless(p(f(X))).` the finite truncations
  alternate between (1, 0, 0, 0) and (0, 0, 0, 1). gk's general method gives
  `p(a)` (.666667, 0, 0, .333333) on the first input and (1, 0, 0, 0) on
  the second, at its default deadline.
- *No priority across atoms.* Ranks decide only between defaults on the
  same atom. Competing defaults on different atoms keep no value, also when
  their ranks differ: `a. p :- a, unless(-p, 1). q :- a, unless(-q, 2).
  -p :- q.` gives `p` and `q` no value in every world.

**Consequences of the design.**

- *A jump at confidence 1.* An exception-free rule becomes classical at
  confidence 1, so reports need not be continuous there. `a`, `e :- a`
  and `-e :- a` prove `-a`: `a` gets (0, 0, 1, 0), and `e` gets
  (0, 0, 0, 1). At the confidence .99 both rules stay directed: `a` stays
  certain, and `e` gets (0, 0, .99, .01).
- *Contradictory inputs.* Adding a derivable clause keeps the reports on
  consistent certain inputs, but not on contradictory ones. `-a`, `a`,
  `-d ; a` gives `d` (0, 0, 0, 1). With the resolvent `-d` added, `d` gets
  (0, 1, 0, 0).

**Behaviour on cyclic inputs.**

- *Conflict fixed on possible bodies.* An abbreviation
  `q :- on(a). -q :- -on(a).` of the atom `on(a)` without a value of
  Section 7.3 puts `q` in conflict, (0, 0, 1, 0), without an effect on any
  other atom. Two rules that can never apply together can give conflict in
  the same way: with `p :- unless(-p). w :- unless(-w). -p :- w.`, the
  rules `0.8::d :- p` and `0.8::-d :- -p` give `d` (0, 0, .8, .2).
- *Two stages with a normal default.* An atom fixed in the ordinary stage
  keeps its state, also when its exception holds after the default stage.
  `d :- -c, unless(-d, 2). -c :- unless(d).` gives `c` (0, 1, 0, 0) and `d`
  (1, 0, 0, 0). For this reason the no-self-support property excludes
  normal defaults.
- *An exception without supporting evidence, in a cycle.* An exception
  literal still gives its rule a layer, because the layers are fixed once
  from the input. The layer can change the order of evaluation:
  `0.5::a :- unless(fresh). b. e. 0.5::-b :- a. 0.5::-e :- b.
  -a :- unless(e).` gives `a` (.25, .25, .25, .25). With `0.5::a.` in place
  of the first statement, `a` gets (.375, .25, .125, .25).
- *A rule removed in every world* still takes part in the layers, and it
  can change atoms in a cycle that the certain part does not decide. In
  `t. e :- unless(t). 0.5::a :- unless(z). 0.9::b. 0.9::e. 0.5::-b :- a.
  0.5::-e :- b. -a :- unless(e).` the rule `e :- unless(t)` is removed in
  every world, and `a` gets (.35, .275, .15, .225). Without that rule, `a`
  gets (.225, .275, .275, .225).

## 9. Worked examples

### 9.1 Tweety in five stages

Does Tweety fly? The question develops in five stages. The inputs are
`Examples/semantics/tweety_*.gkp`.

**Stage 1: an uncertain exception.** Tweety is a bird. Birds normally fly,
with the confidence .9. Penguins normally do not, and the penguin default
has the higher rank. Tweety is a seabird with the confidence .8, and a
directed rule supports that a seabird is a penguin with the confidence .7:

```prolog
bird(tweety).
0.9::flies(X) :- bird(X), unless(-flies(X), 2).
-flies(X) :- penguin(X), unless(flies(X), 3).
0.8::seabird(tweety).
0.7::penguin(X) :- seabird(X).
query(flies(tweety)).
```

The two flying rules are normal defaults. They conclude opposite signs of
`flies(tweety)`, so their ranks, 3 and 2, are compared at that atom. The
answer is (.396, .56, 0, .044). `penguin(tweety)` has the support
.8 × .7 = .56, and there the rank-3 default establishes `-flies(tweety)`.
In the other .44 the flying default contributes .44 × .9 = .396.

**Stage 2: a disjunction.** Replace the .7 penguin rule by two statements.
In the colony under study every seabird is a gull or a penguin, and
evidence supports that Tweety is not a gull, with the confidence .7:

```prolog
gull(X) ; penguin(X) :- seabird(X).
0.7::-gull(tweety).
```

The answer is again (.396, .56, 0, .044). The disjunction and the negative
gull evidence give a route to `penguin`. The disjunction alone establishes
neither species.

**Stage 3a: evidence against a premise.** Add a report that Tweety has a
yellow bill, with the confidence .6. Add also a directed rule with the
confidence .9 that supports `gull` for seabirds with yellow bills:

```prolog
0.9::gull(X) :- seabird(X), yellow_bill(X).
0.6::yellow_bill(tweety).
```

The yellow-bill evidence supports `gull`, and so it opposes the premise
`-gull(tweety)` of the penguin proof. Where `seabird` and `yellow_bill` are
established, `gull` has the positive support .9 and the negative support
.7, tested on its one number U:

| U of `gull(tweety)` | state |
|---|---|
| below .7 | conflict: both sides pass |
| .7 to .9 | positive |
| .9 or more | ignorance |

`gull` is never negative in those worlds. So `-gull(tweety)` is not usable
there, and the penguin proof does not apply. Penguin now needs the seabird
evidence and the negative gull evidence without usable yellow-bill
evidence:

    n = .8 × .7 × (1 − .6) = .224,    p = (1 − n) × .9 = .6984

The answer is (.6984, .224, 0, .0776). There is no conflict at `flies`,
and the remaining .0776 is ignorance.

**Stage 3b: the certain gull rule.** Replace the .9 rule by the certain
rule `gull(X) :- seabird(X), yellow_bill(X)`. The rule is now classical.
With not-`gull` and `seabird` it supports not-`yellow_bill`, and with
not-`gull` and `yellow_bill` it supports not-`seabird`. The three atoms
form a cycle across signs, and Section 7.5 shows how the narrowing puts
them in conflict where all three facts pass. The answer is again
(.6984, .224, 0, .0776).

**Stage 4: a lineage with function terms.** Replace `bird(tweety)` by a
register entry and two certain lineage rules, where `parent(X)` denotes a
selected parent:

```prolog
bird(parent(parent(tweety))).
bird(parent(X)) :- bird(X).
bird(X) :- bird(parent(X)).
```

The register and the second rule establish that Tweety is a bird in two
steps. Together the two rules also give bird statements at arbitrarily deep
parent terms, so their ground instances are infinite, although the needed
proof is short. The default choice of gk sends the input to the general
method, because it has function terms. On the disjunction stage the
general method gives (.396, .56, 0, .044), and with the .9 yellow-bill rule
(`tweety_4b_lineage_gull_rule.gkp`) it gives (.6984, .224, 0, .0776). In
both runs the time budget stopped four lineage searches before they
ended. The reference tool declines the input, because it grounds over
constants.

The stopped searches cannot change these values. The lineage gives a
certain ordinary proof of `bird(tweety)`. No clause can give negative bird
evidence: the contrapositive applications of the lineage rules need a
negative bird literal to start from. And further positive proofs cannot
raise a certain support. This argument holds for this input only. In
general a stopped search leaves the value open.

| stage | the definition (mcref, exact evaluation) | gk |
|---|---|---|
| 1 | (.396, .56, 0, .044) | the same, the exact method, complete |
| 2 | (.396, .56, 0, .044) | the same, the exact method, complete |
| 3a | (.6984, .224, 0, .0776) | the same, the exact method, complete |
| 3b | (.6984, .224, 0, .0776) | the same, the exact method, complete, with the reading `narrowing` |
| 4, disjunction | the tool declines function symbols | (.396, .56, 0, .044), the general method, four searches stopped |
| 4, with the .9 gull rule | the tool declines function symbols | (.6984, .224, 0, .0776), the general method, four searches stopped |

Section 10.4 shows how the general method reaches the value of stage 3a.

### 9.2 A vet's note

This example uses many of the parts: facts, a rule, a normal default with
an external exception, a contrary default of higher rank, opposed facts and
an uncertain disjunction. It needs two exceptions on one rule, which GKP
does not allow, so it is written in JSON-LD-LOGIC
([`Examples/semantics/combined.js`](../Examples/semantics/combined.js)). In words:

    (1) t is a bird.                       (2) p is a penguin.
    (3) penguins are birds.
    (4) .9: a bird flies, unless not flying is established at rank 2,
        and unless the bird is injured.
    (5) a penguin does not fly, unless flying is established at rank 3.
    (6) .5: t is injured.                  (7) .3: t is not injured.
    (8) .6: a vet's note: t is injured or sick.
    (9) t is not sick.
    Question: who flies?

**The applications.** The constants are `t` and `p`. The rules (3), (4)
and (5) are instantiated at both constants, which gives 12 ground
statements. The applications that can ever apply:

| from | application | kind | strength |
|---|---|---|---|
| (1), (2), (9) | `bird(t)`; `penguin(p)`; `¬sick(t)` | facts | 1 |
| (6), (7) | `injured(t)`; `¬injured(t)` | facts | .5; .3 |
| (3) | `bird(p)` from `penguin(p)` | ordinary | 1 |
| (4) | `flies(t)` from `bird(t)`, external exception `injured(t)`; the same at `p` | normal default, rank 2 | .9 |
| (5) | `¬flies(p)` from `penguin(p)` | normal default, rank 3 | 1 |
| (8) | the source event s; `injured(t)` from `¬sick(t)` and s; `sick(t)` from `¬injured(t)` and s | ordinary | s .6; the others 1 |

`bird(t)` from `penguin(t)` and `¬flies(t)` from `penguin(t)` exist as
applications, but nothing establishes `penguin(t)`, so their bodies can
never hold, and they are left out.

**One world.** Take the numbers U = .40 for the source event, .45 for
`injured(t)` and .70 for `flies(t)`. The vet's note is in force
(.40 < .6). `sick(t)` is negative from its fact. `injured(t)` has two
applications for it that apply, the fact (.5) and the note's direction
from `¬sick(t)` (1), so its positive support is 1. Against it is the fact
with .3. Both sides are ordinary, and .3 ≤ .45 < 1, so `injured(t)` is
positive. The exception of the flying default at `t` is usable, so the
exception pass removes the default, and `flies(t)` is in ignorance in this
world. For `p`, `bird(p)` is positive through the penguin, and the flying
default (rank 2, .9) meets the penguin default (rank 3, 1). The higher rank
wins, and `flies(p)` is negative.

**All worlds.** When the note is in force (.6 of the worlds), `injured(t)`
has the strengths 1 for and .3 against: positive .7, conflict .3. When it
is not (.4), the strengths are .5 and .3: positive .2, conflict .3,
ignorance .5. Together `injured(t)` gets (.5, 0, .3, .2). The flying
default at `t` applies where `injured(t)` is not positive, half of the
worlds, and then passes with .9: `flies(t)` gets (.45, 0, 0, .55).
`flies(p)` gets (0, 1, 0, 0). The contrary injury report (7) never
establishes `¬injured(t)`, yet it matters: it turns .3 of the worlds into
conflict, where the exception does not block.

**The cycle.** `injured(t)` depends on `sick(t)` through the note, and
`sick(t)` depends on `injured(t)` through the note's other direction. The
pair is a group with a cycle across signs. The direction towards `sick(t)`
never applies, because `¬injured(t)` is never usable: the support for the
injury is at least .5, against .3. gk's exact method gives `flies(t)`
(.45, 0, 0, .55) with the reading `narrowing`, and `flies(p)`
(0, 1, 0, 0), both complete.

## 10. How gk computes the semantics

The reference tool starts from a finite grounding of the input. gk
searches from the question instead. It searches for proofs of the question
and of its opposite by resolution on the first-order clauses. It records
which statements each proof used. Then it searches again for the evidence
on which those proofs depend: further support, opposing evidence and
exceptions. One calculation over all the evidence found gives the shares
of the question. gk has two methods of this kind, the **exact method** and
the **general method**, and a default choice between them.

### 10.1 The two methods and the default choice

| | the exact method (`gk -exact FILE`) | the general method (`gk -general FILE`) |
|---|---|---|
| input | no function terms, no equality, no built-in condition | the whole language, with function terms and equality |
| search | exhaustive resolution that keeps the distinct sets of source statements of the answer; no grounding of the input | resolution and paramodulation under a time budget; the allowances shrink with the distance from the question |
| what an ended search means | every required search task for that literal has ended | the search strategy finished that attempt; evidence can be missing |
| the answer | marked complete: the report of the input, to within 10^-6 for the input as gk reads it | the report of the evidence found: an estimate that can lie above or below the report of the input |
| what the output adds | the mark complete, or the resource limits reached | the stopped searches, the readings, the checkpoint of the latest completed evaluation |

**The default choice** (`gk FILE`, also `gk -auto FILE`) combines the two.
Let T be the time limit of the run, `-seconds`, 10 s by default.

```
if the input or the question has a function symbol with arguments or an equality,
        or the exact method does not cover the input for another reason:
    run the general method for all of T
else:
    run the exact method within N = T/2 (its collection until 0.6 × N)
    if every task ended, no limit left required work undone,
            and the evaluation gave a value:
        print its answer: complete, or not complete with the name of an approximation
    else:
        run the general method with the time left until T, from a new search state
```

The answer names the method that produced it (`policy.answer_from`). Only
a complete answer of the exact method is the value of this semantics.
[recursive_output.md](recursive_output.md) Section 7.5 describes the
default choice in full.

### 10.2 The evidence and its evaluation

Both methods collect applications from proofs. To **import** a proof, gk
applies the recorded substitutions and gets ground applications. Each
keeps its input statement, its grounding, its head, its body literals, its
exception literals and its confidence. Different uses of the same ground
application are merged: `0.5::bird(a)` used twice counts once, while the
instances of `0.9::p(X)` at `a` and at `b` stay distinct. All uses of one
uncertain ground clause without a written head share its one source event.
A proof of several statements becomes one application with the body,
listed clauses and other parts of Section 3.3.

A refutation proof of Q starts from the assumption ¬Q and derives a
contradiction. The proof discharges that assumption, so it is not negative
evidence about Q. A supplied or separately proved ¬Q is.

Both methods pass the collected applications, the **snapshot**, to the same
evaluator. The evaluator does not sample. It keeps one identity for each
ground atom and each source event, so shared evidence counts once. It
groups the atoms that depend on each other, evaluates the resulting graph
without cycles by recursive conditioning, and caches the results. Within
each case it applies the support levels, kinds, ranks and state tables of
Section 5 and integrates the comparisons with U and V exactly. It
evaluates a sweep group by its sweeps. It evaluates any other cyclic group
cell by cell by the clause rule, the exception pass and the narrowing of
Section 7. The evaluator has fixed limits on group size, applications with
exceptions, cells, memory and time.

Unless the output records an approximation or an interrupted evaluation,
the evaluator computes the semantics of the snapshot. The value equals the
report of the whole input only when the snapshot holds every relevant
application. The exact method collects all of them. The general method
returns an estimate.

### 10.3 The exact method

The exact method starts from the question, searches by resolution, records
the statements of each proof, and checks every premise and every exception
in turn. An input is **covered** when it has no function symbol with
arguments, no equality, no built-in condition, and positive ranks only on
normal defaults. Facts, rules with a written head, certain rules and
clauses without a written head are all allowed, certain or uncertain, with
or without exceptions and variables. Dependency cycles and contradictory
evidence are allowed. The question is one ground literal, positive or
negated, or a question with variables, whose ground answers get one report
each.

A **task** is the search for one signed ground literal Q. The method
starts a task for the question and one for its opposite. A task does four
things:

```
1. single applications: import every single application with the head Q
2. search: assume ¬Q and resolve it with every statement that contains Q
       (a directed statement only where Q is its written head);
       resolve what is left with each other and with the background clauses,
       the statements without a direction that contain neither Q nor ¬Q;
       keep with every derived clause its label, the set of statements it came from
3. import: a derived clause with a label of two or more statements is a candidate
       proof (L, G); test the conditions of a proof, build its application,
       and apply the redundancy rule among all applications with the head Q
4. demands: start tasks for both signs of every atom of the body,
       the external exceptions and the listed clauses of each imported application
```

The premises of a proof are not proved inside the task that finds the
proof. Each premise has its own task. When every task has ended, the
applications whose body can never hold or can hold only when their head
already holds are left out, and the evaluator evaluates the rest once.

**A worked derivation.** Take three clauses, `c1` with its source event of
confidence .5:

```prolog
0.5::p ; r.                   % c1
0.8::q :- p, unless(-q).      % r2
0.5::q :- r, unless(-q).      % r3
query(q).
```

The task for `q` imports the single applications of `r2` and `r3`. It
resolves the assumption ¬q with both rules, which gives the residual
clauses ¬p with the label {r2} and ¬r with the label {r3}. Resolving ¬p
with `c1` gives r with the label {c1, r2}. Resolving r with ¬r gives the
empty clause with the label {c1, r2, r3}. From it the task imports one
normal-default application for `q`. It has no ordinary premise and the
source event of `c1` as premise. It lists the clause `p ; r`, and it has
the rule identities r2 and r3 and the strength .8 × .5 = .4. The tasks for `p` and `r` find no
opposition, so the listed clause is not contradicted. The event holds in
half of the worlds, and the exact evaluation gives `q` (.2, 0, 0, .8),
marked complete.

The paper proves that on every covered input every task of this procedure
ends. The collected applications then give the report of the question in
the whole ground input, all five shares included (Section 12).

**Searching without grounding.** gk runs the tasks on the statements as
written, with unification and factoring and fresh variables for each use.
Every derived clause keeps, for each statement it used, the terms of all
the ordinary variables of that statement. One statement used with two
different bindings is two pieces of evidence, and the same binding used in
two proofs is one. When gk extracts a ground proof candidate, it
instantiates every ordinary variable that is still free over all input
constants and tests each result. The second addition is required. With
`0.6::q :- f(Y)` and `0.7::q :- -f(Y)` and no evidence on `f`, resolution
derives `q` once, with Y free. Each constant gives one proof by cases from
its own pair of rule instances. So the support of `q` is
1 − (1 − .42)^n for n constants: .42 for one constant and .6636 for two. A
task is marked complete when its
symbolic search is closed, or when a ground search for that task finished
it.

**Binding variables from facts and earlier answers.** In two classes of
inputs, single applications suffice. gk detects them when it reads the
input and then matches rule bodies against facts and earlier answers,
without the labelled resolution:

- ground facts of either sign, and directed rules with a positive head and
  positive body atoms in which every variable of the head occurs in the
  body; the rules may be uncertain, may have exceptions of either sign and
  may be normal defaults;
- positive ground facts, certain or uncertain, and certain rules of that
  form without exceptions, such as transitivity.

The second class needs the absence of negative input. With the certain
rule `link(X,Z) :- link(X,Y), link(Y,Z)`, the facts `link(a,b)` and
`0.5::link(b,c)`, and the fact `-link(a,c)`, the rule has a contrapositive
application that opposes `link(b,c)`. Its report is (0, .5, .5, 0), not
(.5, 0, 0, .5). This input is outside both classes, and the full search of
the task finds the opposing proof.

**Marking an answer complete.** The exact method runs its tasks in rounds
whose allowance grows fourfold each round, and keeps the state of a task
between rounds. It marks an answer **complete** only when every task
ended, no count, time or memory limit left required work undone, and the
evaluation finished without an approximation. Every complete run on one
input gives the same report. An incomplete run names the limits it reached
in `complete_mode.limits`. Among them are three limits of the evaluation
and of the binding search: `clause rule across groups` (Section 10.5),
`recursion depth` (a chain of the dependency longer than the evaluator's
recursion allows: 40,000 links natively, fewer where the stack is smaller)
and `binding by data` (the binding of variables from facts stopped after
100,000 rounds). gk stores a confidence in units of 10^-7. A
confidence of .9999995 or more counts as 1, which makes an exception-free
rule with a written head classical. A confidence of .0000005 or less counts
as 0, which leaves the statement out. The output names every confidence
read in this way.

**Function terms.** With `-exact`, gk 1.3.1 also runs on an input with
function terms. It cuts terms at a depth limit. It marks an answer
complete when every task ended, no term was cut, and no variable had to
run through the list of the ground terms written in the input. The
paper's proof of exactness covers only inputs without function terms. It
makes no claim for such an answer, and the reference tool declines
function symbols. On the input `0.8::bird(father(tweety)).` and
`0.9::flies(X) :- bird(X).` with the question `flies(father(tweety))`,
`gk -exact` prints (.72, 0, 0, .28) as a complete answer. On the lineage
of Section 9.1 it cuts terms and prints the right value, but not as a
complete answer, with the limit `term depth`. The default choice sends
such an input to the general method. An input with
equality gets no value from the exact method
([recursive_output.md](recursive_output.md) Section 7).

### 10.4 The general method

The general method searches with resolution and paramodulation, with
factoring and simplification, on clauses with variables, disjunctions,
equality and function terms. A proof keeps its parent clauses,
substitutions and inference steps, also the ancestry of a derived lemma.
The search keeps the direction of Section 2.1. Directed rules and normal
defaults supply only their head. In certain clauses and in clauses without
a written head, any literal can serve as the head of an application.

**Recursively checking the proof.** Each imported application creates
further search tasks:

- for its conclusion: a search for opposition;
- for every condition: searches for opposition and for other support;
- for every exception: searches for whether it holds and for its
  opposition;
- for every literal of a listed clause: searches for the evidence for and
  against it.

The question itself is also searched for further proofs. A proof that a
task returns adds applications and creates the same kinds of tasks at its
own premises. Equal tasks are shared. A **checkpoint** is the point at
which gk evaluates the snapshot, after the first search and after each
round of further searches.

On stage 3a of the Tweety example, the general method's checkpoints show
the value change as it finds evidence (`gk -general -checkpoints DIR`):

| evidence collected | for | against | conflict | ignorance |
|---|---|---|---|---|
| the bird proof and the flying default | .9 | 0 | 0 | .1 |
| also the opposing penguin proof | .396 | .56 | 0 | .044 |
| also the yellow-bill support for gull | .6984 | .224 | 0 | .0776 |

The first two rows are incomplete estimates for the whole input. The third
discovery is not another proof of flying. It changes the state of a
premise inside the opposing proof. Wherever the yellow-bill rule supplies
positive gull evidence, `-gull(tweety)` is not usable, so the penguin proof
does not apply in those worlds.

**The budget.** Work near the question comes first. A task at depth d in
round k has the allowance L0 × 2^k × ρ^d, with L0 = 50 ms and ρ = .5.
Within one depth, opposition comes before other support, because an
objection can make a premise unusable. The deadline is `-seconds`. A
quarter of the general method's budget is kept for the evaluation. The
schedule decides which searches finish before the deadline, so it can
change the estimate.

**What an answer of the general method establishes.** It is the latest
completed evaluation of the collected snapshot. The output lists the
unfinished work: stopped or unrun tasks, pending imports and interrupted
evaluations. Even when every task of the general method ends, evidence
that the search did not find can move the value in either direction, as
the table above shows. So an incomplete snapshot is neither a lower nor an
upper bound.

### 10.5 The readings

gk's line can hold a list `readings`. Each entry names a procedure or an
approximation that acted on the value. Some readings name a procedure of
this definition. The value is then still the value of the semantics for
the snapshot:

| reading | meaning |
|---|---|
| `narrowing` | a group of atoms in a cycle was evaluated by the narrowing (Section 7.2) |
| `backbone` | the exception pass removed an application in some cells, and restored it in some (Section 5.6) |
| `blocked-rule repair` | applications whose bodies rest on held-out or removed applications were left out in some cells (Section 5.6) |
| `clause rule in a circle` | the clause rule ran in a group that holds a listed clause of a proof (Section 7.4) |
| `no self-support` | the general method left out applications by the no-self-support rule (Section 5.7) |
| `self exception` | an application whose exception is one of its own body literals never applies and was not registered (Section 3.1) |

Other readings name an approximation. A value with one of them need not be
the value of the semantics for the snapshot. The exact method marks an
answer with `cycle cut`, `backbone approximation`, `context copies`,
`taxonomy ignored` or `clause rule across groups` not complete:

| reading | meaning |
|---|---|
| `cycle cut` | a cyclic group too large for the narrowing was broken by removing dependency edges |
| `backbone approximation` | the general method ran the exception pass one group at a time, where the definition runs it over the whole input, and this can change the value |
| `context copies` | an atom was read in several rank contexts and got a copy for each; inside the check of an exception of a normal default of rank k, the general method does not let a normal default of a lower positive rank supply the objection, while the semantics compares ranks only at one atom |
| `taxonomy ignored` | a taxonomy rank was read as rank 0 |
| `clause rule across groups` | the exact method only: a proof outside a cycle lists a clause of that cycle; gk evaluated the proof's conclusion inside the cycle, in the rounds of the clause rule, and the semantics evaluates it after the cycle (Section 11.8) |
| `residual variable represented by a fresh constant` | a variable that a proof left unbound got a fresh constant; the semantics, which grounds over the input's constants, has no such instance |

A proof step that gk cannot turn into an application enters as one
**proof application**, and the line counts such steps in
`steps_not_represented`. [recursive_output.md](recursive_output.md)
Section 5 lists every reading and status fact.

### 10.6 Where to read more

- [how_gk_works.md](how_gk_works.md) describes the search, the import of
  proofs, the evaluator and the budget in more detail.
- [recursive_output.md](recursive_output.md) describes the output of the
  three methods field by field.
- [cli_reference.md](cli_reference.md) lists the options.

The older direct method is described in [direct_method.md](direct_method.md). It is the legacy method of
gk 1.1.2 (`gk -direct FILE`). It does not compute the semantics of this
page.

## 11. Reference definitions

This section states the definition as plain rules, without examples. It
follows the appendix of the paper. Sections 3 to 7 give the examples.

### 11.1 Terms

- An **atom** is a predicate applied to arguments, such as `flies(t)`. It
  is **ground** when it has no variables. A **literal** is an atom or its
  negation. The **opposite** of a literal is the same atom with the other
  sign.
- A **statement** is one input fact, rule or disjunction, with its
  **confidence** (the number written on it; 1 when none is written), its
  **written head** if it has one, and its **exception literals** if it has
  any. A statement is **certain** when its confidence is 1 and
  **uncertain** otherwise. A confidence is written on an input statement. A
  **strength** belongs to an application or to a side and is computed.
- `p :- f.` and `f => p` have the written head `p`. `p ; -f.` has no
  written head.
- **The head of a default whose consequent is a disjunction.** The
  **consequent** of a statement is what stands left of `:-` or right of
  `=>`. A statement written as a plain list of literals is all consequent.
  Take a statement with an exception literal whose consequent has several
  literals. If one literal L of the consequent is the opposite of the
  exception literal, L is its head, and from then on the statement counts
  as a statement with the written head L. The test is made on the
  statement as written, before grounding. If no literal of the consequent
  passes the test, the statement keeps no written head. A statement with
  several exception literals of which more than one has such a literal
  also keeps no written head.
- An exception literal is written `unless(E)`, `unless(E, k)` or
  `$block(k, E)`, with a **rank** k, an integer of 0 or more.
  `unless(E)` has rank 0.
- The **clause** of a statement is the disjunction of its literals without
  its exception literals: the clause of `p :- f, unless(x).` is `p ; -f`.

### 11.2 Grounding

Let D be the set of constants of the input, the question's constants
included. Every variable of a statement's ordinary literals is replaced by
a constant of D, in every combination. A repeated variable gets the same
constant in each place.

- A variable that occurs only in exception literals is not instantiated
  for each statement. All its instances are exceptions of the one ground
  statement.
- A built-in condition such as `X < 10` is computed after instantiation. A
  true condition is dropped. A false one drops the ground statement.
- A statement with the confidence 0 is excluded. It gives no support and
  no application, so it takes no part in deciding the kind or the rank of a
  side.
- Two statements with the same text are two statements: the position in
  the input identifies a statement. One statement instantiated twice with
  the same constants is one ground statement. Two different choices of
  constants for the ordinary variables of one statement are two ground
  statements, also when they give the same clause.
- **The order of the steps.** First the written head of a statement is
  read on the statement as written (Section 11.1). Then the statement is
  instantiated. In each ground statement a literal that occurs several
  times in the clause counts once, and a body literal that is the opposite
  of the head is the head literal again. Only then is the ground statement
  classified (Section 11.3). When one literal is left, the ground statement
  is a fact of that literal with the statement's confidence, also when it
  was written with several literals or as a rule: it has no event and no
  rule identity. A rule has a body literal only when a literal other than
  its head is left. The ground statement keeps its exception literals.
- Constants are typed: the integer `1`, the real `1.0` and the string
  `"1"` differ.
- A ground statement whose clause contains a literal and its opposite
  takes no part in a proof of several statements (Section 11.4). Its single
  applications remain.

From here on, "statement" means a ground statement. The number of ground
statements grows quickly: a statement with v variables over d constants
gives up to d^v instances.

### 11.3 The kinds of statement and their single applications

| kind | example | how it is used |
|---|---|---|
| certain clause | `p ; r.`, `q :- p.`, `p.` | in every direction |
| uncertain fact | `0.8::p.` | evidence at its atom |
| uncertain clause with several literals and no written head | `0.8::p ; r.` | in every direction; it holds or fails as one event, shared by all its uses |
| uncertain rule (written head) | `0.9::flies(a) :- bird(a).` | only towards its head; its confidence counts at its head |
| rule with an exception (written head) | `flies(a) :- bird(a), unless(penguin(a)).` | only towards its head; the exception stays |
| clause with an exception and no written head | `p ; -f :- unless(x).` | in every direction; the exception stays |

Only a written head gives a direction, and only on a statement that is
uncertain or has an exception. A certain rule without an exception is a
certain clause. A head read from a default (Section 11.1) is a written
head. An input **has heads on its exceptions** when every statement with an
exception has a head: its consequent is a single literal, or its
consequent is a disjunction and the head is read as in Section 11.1. The
definition covers the statements outside this subclass too. Results that
need heads on exceptions say so.

An **application** is a standing possibility to conclude one literal. It
has a **head**, the literal it concludes; **body literals**, which must be
usable; exception literals, which must not be usable; **listed clauses**,
which must not be contradicted (only proofs of several statements have
them, Section 11.4); a **strength** in [0, 1]; and, when it uses uncertain
rules, their identities.

**The identity of an uncertain rule.** An uncertain rule with a written
head and at least one body literal (counted as Section 11.2 says) has an
identity, also when it is a normal default. Its single application has
that identity, and so has every proof that uses the rule. A rule that
several applications use is one rule: it holds or fails once. A fact, and a
rule without a body literal such as `0.5::a :- unless(-a).`, have no
identity. Their uncertainty is a strength only.

The **single applications** of a statement:

| statement | applications |
|---|---|
| a fact L | head L, empty body, the fact's confidence |
| a rule with a written head H that is uncertain or has an exception | head H, body the opposites of its other literals, the rule's confidence (**directed**) |
| a certain clause | one application per literal L: head L, body the opposites of the other literals, strength 1 |
| an uncertain clause with several literals and no written head, confidence c | an event s, a new atom for this ground statement alone, with one fact of confidence c; one application per literal as in the row above, with s added to its body, strength 1; every use of the statement refers to that one atom |
| a clause with an exception and no written head | as the two rows above, certain or uncertain; each application has the exception literals |

Every application of a statement has the statement's exception literals.
An exception literal that is written several times counts once, with the
largest of its ranks. For each application:

- If the opposite of the head is among the exception literals, the
  application is a **normal default**, and the rank of that literal is the
  application's **rank**. That literal is not used in the test whether the
  application applies. The table of Section 11.6 handles the opposite
  evidence.
- Every other exception literal is **external**. An application that is
  not a normal default is **ordinary**.

The test is made for each application. One direction of a clause without a
written head can be a normal default while another direction is not.

An application with an external exception literal that is also one of its
body literals never applies and is excluded.

**A rule that blocks itself is excluded.** After grounding, and after the
instances of a variable that occurs only in exception literals are
collected, a rule with a written head is excluded when the same signed
literal is one of its body literals and one of its external exception
literals. This is done once, before the single applications are formed and
before the proofs of several statements are built, so the rule takes part
in none. This test differs from the one for a clause with a literal and
its opposite (Section 11.2), which keeps its single applications. A
statement without a written head is not excluded: one of its directions
can still apply.

### 11.4 Proofs of several statements

A consequence that needs several statements at once, such as a proof by
cases, is evidence too.

**A proof of a literal Q** is a pair (L, G). L is a set of statements. G is
a set of single literals, the **premises**. Neither Q nor its opposite is
in G. The conditions:

1. the clauses of L together with G imply Q classically;
2. the clauses of L together with G are consistent;
3. no statement can be left out of L and no literal out of G: no smaller L
   with the same G, and no smaller G with the same L, still implies Q;
4. every statement in L with a written head that is uncertain or has an
   exception has the signed literal Q as its head.

A fact `Q.` is the proof ({`Q.`}, {}). A single application is the proof
with one statement. It keeps the strength and the kind that Section 11.3
gives it. The construction below adds the applications of the proofs that
use several statements, each with two or more literals. A fact enters such
a proof as a premise: its literal is in G, and its confidence counts at its
own atom. The order of derivation steps does not matter: two derivations
with the same pair are the same proof.

The premises are not proved inside the proof. Each premise is tested at
its own atom.

A clause without a written head may take part in any proof, with or
without a confidence or an exception. An uncertain one, with the clause C
and the event s, is read in the proof as the clause "not s, or C", so the
proof has s as a premise. The event is never the goal of a proof. Where the
proof lists the clause, it lists C itself.

The **non-goal clauses** of a proof are the clauses of L that do not
contain Q.

**The application of a proof (L, G) of Q** has:

- the head Q;
- as body, every single literal that G and the non-goal clauses imply, the
  literals of G among them;
- as exception literals, those of every statement in L; the opposite of Q
  on a normal default of Q is the mark of a normal default, not an external
  exception of the proof;
- as listed clauses, the non-goal clauses with several literals;
- the identities of the uncertain rules of L, and as strength the product
  of their confidences;
- as kind: a normal default when L holds normal defaults of Q, with the
  smallest of their ranks, and ordinary otherwise. An uncertain normal
  default takes part like a certain one, with its identity. An exception of
  a clause without a written head stays an external exception of the
  proof, also when it is the opposite of Q, and it never makes the proof a
  normal default. The single application of such a clause towards Q is a
  normal default (Section 11.3). It does not absorb an ordinary proof that
  uses the clause.

An application with an exception literal that is also one of its body
literals never applies and is excluded.

**The redundancy rule.** The application of a proof of Q is excluded when
another application of Q requires no more: the body literals, the
exception literals, the listed clauses and the uncertain rules of the other
are all among those of the first. The other application must be certain,
or have its uncertainty in a body literal (an event) or in the identities
of its uncertain rules. An application whose uncertainty is a strength
only absorbs nothing: an uncertain fact, and an uncertain rule without a
body literal. An application that is a normal default absorbs only a normal
default of the same rank. Of several applications with equal requirements,
kind and rank, one is kept.

**A body that can never hold.** After the proofs are built, start with the
heads of the applications without a body. Add the head of an application
when all its body literals have been added. Exception literals, listed
clauses and opposing evidence are ignored. An application that needs a
literal outside this set is excluded. The dependencies of Section 11.7 are
formed from the applications that remain. "Can conclude" in Section 11.8
means that some remaining application has that head.

**No self-support.** An application with the head L is excluded when one
of its body literals cannot be derived, in the sense of the paragraph
above, without the applications that have the head L. The test is made
once, on all applications, before the applications whose body can never
hold are excluded. A second round would exclude nothing more. The rule
works on applications, so the clause notation does not matter.

A lemma of the paper: in a proof of Q no clause of L contains the opposite
of Q, and every single literal other than Q that some part of L and G
implies is implied by G and the non-goal clauses.

### 11.5 Worlds

For every ground atom A, the events of uncertain clauses included, take
two numbers U_A and V_A. Each is uniform on [0, 1). They are independent of
each other and of the numbers of every other atom. Nothing else is random,
and no number is drawn again when an atom is used a second time. A share of
worlds is a probability under these numbers. One assignment of all these
numbers is a **world**. Sections 11.6 to 11.9 give every atom a state in
each world: positive, negative, conflict or ignorance; or no state, when the
atom has **no value** in that world.

### 11.6 Applicability of an application and the state of one atom

A literal is **usable** when its atom is in the state of its sign: A
positive, or ¬A negative. Conflict and ignorance make neither literal
usable. A literal **has evidence** when its atom has its sign or is in
conflict.

**The check of a listed clause** has three results. The clause is
**contradicted** when the opposite of each of its literals has evidence.
It is **not contradicted** when the opposite of one of its literals
certainly has no evidence: the atom of that literal has a state without
such evidence, or it has no value and no application can conclude the
opposite of the literal. Otherwise the check **cannot be decided**: no
literal certainly lacks evidence against it, and some atom of the clause
has no value.

An application **applies** in a world when the exception pass (Section
11.9) has not removed it and:

- **usable premises**: every body literal is usable;
- **no contradicted clause**: every listed clause is not contradicted. An
  application with a check that cannot be decided neither applies nor is
  absent: the atom of its head is evaluated by the procedure of Section
  11.7, where the check counts as a dependency without a value;
- **no usable exception**: no external exception literal is usable.

The check of a listed clause is not an exception literal. It has no part in
the layers of Section 11.9. Evidence against the head is not a reason to
discard an application. It is opposition.

**The strength of a side.** The applications with the head A that apply
form the side for A. Those with the head ¬A form the side against A. The
strength of a side is the probability that at least one of its
applications succeeds. A single application succeeds with its strength. A
proof succeeds when all its uncertain rules succeed. Each uncertain rule
succeeds with its confidence, independently of the others, and a rule used
in several proofs is one rule. For applications that share no rule the
strength is 1 − ∏(1 − c). In general it is 1 − ∏_i(1 − c_i) × (1 − p), with
the product over the applications without identities and p the
probability that at least one of the others has all its rules. This
probability is a calculation of the strength. It adds no random number to
the world.

A side that is not empty is **normal** when every application in it is a
normal default, and **ordinary** when at least one is not. The kind is
decided in each world. The rank of a normal side is the largest rank among
its applications.

With a the strength of the side for A, b that of the side against A, and
U, V the two numbers of A:

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

### 11.7 Evaluation order and groups of atoms

**Dependency.** Atom A depends on every atom in the body literals, the
external exception literals and the listed clauses of the applications
with the head A or ¬A that remain after Section 11.4. The **groups** are
the strongly connected components of this relation. An atom that is in no
dependency cycle forms a group of its own. In each world the groups are
evaluated in the order of the dependency, each after every group it
depends on.

A group has a **cycle across signs** when an application whose head is a
literal of the group has a body literal in the group of the other sign, or
when two applications with body literals in the group have heads of
opposite signs in the group. Exception literals and facts do not count.

**Sweep groups.** A group G is a sweep group when

1. G has no cycle across signs;
2. no application of G has an exception literal whose atom is in G; the
   opposite of its own head on a normal default does not count;
3. no application of G is a normal default;
4. no atom outside G that G depends on is without a value.

```
for each group G, after every group that G depends on:
    if an application of G lists a clause with an atom in G:
        the clause rule (Section 11.8)
    else if G depends on an atom without a value outside G,
            or an application of G lists an outside clause whose check cannot be decided:
        the procedure for G (below), whatever its form
    else if G is one atom that does not depend on itself:
        its state comes from the table of Section 11.6
    else if G is a sweep group:
        every atom of G starts in ignorance
        repeat a sweep: compute every atom of G from the states of the sweep before,
            until a sweep changes nothing
    else if G has no cycle across signs:
        the procedure for G; an atom it leaves without a value is in ignorance
    else:
        the procedure for G
```

**The narrowing**, for a given set of applications of G. Literals of the
atoms outside G are read from their final states. For a literal L of G, an
application for L has the head L, and an application against L has the
opposite of L as its head. The **base** literals are the usable literals of
the outside atoms that G depends on and the usable literal of every atom
of G that the procedure below has fixed positive or negative. An atom fixed
in conflict and an outside atom without a value give nothing. The check of
a listed clause whose atoms are outside G is read from their final states:
an application with a contradicted check is excluded, and a check that
cannot be decided is treated as an exception literal on an outside atom
without a value.

1. Sure is the base literals. Possible is the base literals, both literals
   of every atom of G that is not fixed, and both literals of every outside
   atom without a value.
2. New sure: start from the base literals and repeatedly add a literal L of
   an atom that is not fixed when Section 11.6 gives L's atom the sign of
   L. Count the applications for L whose body literals are all in the set
   being built and whose exception literals are all outside the old
   possible set, and the applications against L whose body literals are all
   in the old possible set and whose exception literals are all outside the
   old sure set. Stop when nothing more can be added.
3. New possible: start from the base literals and both literals of every
   outside atom without a value, and repeatedly add a literal L of an atom
   of G that is not fixed when Section 11.6 gives L's atom the sign of L.
   Count the applications for L whose body literals are all in the set
   being built and whose exception literals are all outside the new sure
   set, and the applications against L whose body literals are all in the
   new sure set and whose exception literals are all outside the old
   possible set.
4. If neither set changed, go to step 5. Otherwise take the new sets as the
   old ones and repeat from step 2. Sure only grows, possible only shrinks,
   and sure stays inside possible.
5. Every atom that is not fixed and has no literal in sure, whose table
   gives conflict when both sides count their applications with body
   literals in possible and no exception literal in sure, is **fixed** in
   conflict. If any atom was fixed in this step, remove its literals from
   both sets and repeat from step 1 with the fixed atoms excluded.

A fact, or an application whose body literals are all base literals, has
its body test met in both computations, since nothing in G can remove it.
Its exception literals and its listed clauses are still tested.

**Selections.** When the atom of L has applications that are normal
defaults, "Section 11.6 gives the sign" is decided over selections of
applications. For one side, write C(B, E) for its applications whose body
literals are all in B and whose external exception literals are all outside
E. Let S be the old sure set, P the old possible set, X the new sure set
while it is built, S' the finished new sure set, and Y the new possible set
while it is built. A selection R of a side must lie between two sets:

| computation | side | allowed selections |
|---|---|---|
| new sure | the side of L | C(X, P) ⊆ R ⊆ C(P, S) |
| new sure | the opposing side | C(S, P) ⊆ R ⊆ C(P, S) |
| new possible | the side of L | R ⊆ C(Y, S') |
| new possible | the opposing side | C(S', P) ⊆ R ⊆ C(P, S') |

For the new sure set the sign must hold for every pair of selections. For
the new possible set it must hold for some pair. When the atom has no
normal default, the strength of a side only grows with its selection, so
the single least favourable pair for the new sure set and the single most
favourable pair for the new possible set decide.

**The procedure for G.** It runs the narrowing once, or twice when G has
normal defaults.

1. If G has applications that are normal defaults, run the narrowing on the
   ordinary applications of G alone. Fix every atom that ends with a
   literal in sure, in that sign, and every atom fixed in conflict. Then
   run the narrowing on all applications, keeping the fixed atoms.
   Otherwise run the narrowing once, on all applications.
2. A fixed atom keeps its state. An atom with a literal in sure has that
   sign. An atom with neither literal in possible is in ignorance. Any other
   atom has **no value**. In a group without a cycle across signs that
   depends on no atom without a value, the list above reads it as
   ignorance.

### 11.8 The clause rule in a cycle

A proof by cases can establish a literal that is used to derive evidence
against one of its listed clauses. The check of the listed clause then
depends on its own result. The rule, for one world and one group G in
which some application lists a clause with an atom in G:

1. Evaluate the group with no listed clause of the cycle counted as
   contradicted. A listed clause is **of the cycle** when an application
   whose head atom is in G lists it and it has an atom in G. The checks of
   other listed clauses keep their results. Premises,
   events and exceptions are checked as always. The atoms of G are
   evaluated in the groups they form when the checks of the cycle are
   taken as fixed, by the list of Section 11.7.
2. Collect all listed clauses that come out contradicted. If there are
   none, this is the result.
3. Leave out every proof that lists one of them, and evaluate again.
   Collect the contradicted listed clauses again, all at once.
4. If the clauses collected so far are still contradicted and no new one
   appeared, this is the result. If a new one appeared, add it and repeat
   step 3.
5. If a clause collected earlier is no longer contradicted, or a check
   cannot be decided, the rule has no result. This comes before step 4: it
   holds also when another clause has just become contradicted. Then an
   atom of the group that has had the same state in every evaluation that
   the rule made keeps that state, and every other atom of the group has no
   value in this world. When the rule stops at a check that cannot be
   decided, one more evaluation is made before the comparison, with every
   listed clause whose check is open or contradicted counted as
   contradicted, so that both readings exist.

All checks of a round are made before any setting changes.

A listed clause of the cycle is evaluated only while one of its proofs
could otherwise apply: its body literals are usable, none of its exception
literals is usable, and no listed clause outside the cycle excludes it. The
settings of the other clauses of the cycle are ignored for this. When every
proof that lists the clause is out for another reason, the clause keeps its
setting of the round before.

Only applications with head atoms in G count when deciding whether to
recheck a clause of the cycle. A setting is used only in the rounds of this
invocation of the clause rule, including evaluations of the smaller groups
within G. After the rule returns, a check outside G reads the final states
of the atoms in G, including any atoms with no value, and applies Section
11.6 using the applications remaining in the current evaluation.

One literal that certainly has no evidence against it makes the clause not
contradicted, also when the check of another literal is open. If including
the proof and leaving it out would each reproduce that choice on
evaluation, the procedure starts with the proof included.

### 11.9 The exception pass: layers, removal, restore

Literals and applications get **layers**. A literal and its opposite get
their layers separately.

- An application without an external exception literal has layer 0, also
  when its body literals have higher layers. A normal default whose only
  exception literal is the opposite of its head has layer 0.
- An application with external exception literals has the layer 1 + the
  highest layer of those literals.
- The layer of a literal is the highest layer among the applications that
  conclude it, raised to the layer of every body literal of those
  applications and to the layer of the opposite of every literal of their
  listed clauses. A literal that no application concludes has layer 0.
- The layers are the smallest numbers that meet these three rules. Where
  the rules allow no finite number (exception literals that depend on each
  other in a cycle, and everything whose layer depends on them), the layer
  is the **top** layer, one above every finite layer.

The layers are computed once, from the applications that remain after
Section 11.4, before any world is looked at.

"Evaluate with some applications **held out**" means: those applications
are absent. Among the others, exclude again the applications whose body
can hold only when their head already holds and the applications whose
body can never hold (Section 11.4), now tested without the absent ones.
Note again which literals some remaining application can conclude. Form the
groups again from the dependencies of what remains. Compute every state
anew with the same numbers U and V. No state of an earlier evaluation is
kept. The same holds for an application that was removed: a removed rule is
absent, and what could be derived only through it can no longer be
derived. Only the layers are not computed again: they fix the order of the
passes.

In each world:

1. For s = 1, 2, ... up to the top layer: evaluate (Sections 11.6 to 11.8)
   with the applications of layer s and above held out, and those removed
   before. Remove every application of layer s that has an external
   exception literal usable in that evaluation.
2. Evaluate all applications that are not removed.
3. Restore every removed application for which none of the exception
   literals that caused its removal is usable in the result of step 2, all
   such applications at once. If one was restored, repeat step 2. A
   restored application is not removed again. It is an application like any
   other: its body literals, its exception literals and its listed clauses
   are tested in the next evaluation.

The states of the last run of step 2 are the states of the world.

### 11.10 The report

For a ground question literal Q with the atom A, the report is

    R(Q) = (P[A positive], P[A negative], P[A conflict], P[A ignorance])

where P is the share of worlds. Positive and negative are exchanged when Q
is ¬A. The share of worlds in which A has no value is reported beside the
four numbers. The four numbers sum to 1 minus that share, and they are not
scaled up. A question with variables gets one report for each ground
instance over D, from the same worlds. An instance whose atom is the head
of no application has (0, 0, 0, 1). The reference tool does not print such
an instance.

## 12. Properties

The paper proves the following statements for finite ground inputs. The
names are those of the paper.

- **Agreement with the distribution semantics.** On every finite positive
  ground program, cycles included, the distribution semantics and the
  support semantics give the same joint distribution of the set of atoms
  that come out positive. A question with the distribution-semantics
  probability p has the report (p, 0, 0, 1 − p).
- **Stratified exceptions.** Let a finite ground program consist of facts
  and rules whose written heads, body literals and exception literals are
  all positive atoms. Suppose its atoms can get levels such that every body
  atom of a rule has at most the level of the head and every exception atom
  a strictly lower level. Then the support semantics agrees with the
  distribution semantics of the program in which each rule instance has one
  independent switch and each exception is a negation-as-failure test. Only
  the states positive and ignorance occur.
- **Characterization of the shared number.** Let two tests have the
  success chances a and b, and let q be the chance that both succeed. Among
  all joint laws with these marginals, exactly one never lets the test with
  the smaller chance succeed alone (either test, when the chances are
  equal). It has q = min(a, b), and it is the law of the two tests U < a
  and U < b on one uniform number U.
- **Primacy of the classical proofs.** Let S be the certain statements of
  an input that have no exception, with consistent clauses. Suppose that
  every statement outside S that S does not block is a fact or has a
  written head, and that none of these heads is the opposite of a literal
  that occurs in S. Then in every world every rule that S blocks is removed
  by the exception pass and never restored, every literal that S entails is
  usable, and every atom that S decides has the report it has in S alone.
- **A certain fact that nothing opposes.** Let `p.` be a certain fact of a
  ground input, and let no remaining application have the head ¬p. Then
  the report of p is (1, 0, 0, 0).
- **Classical agreement.** Let K be a finite consistent set of certain
  ground clauses without exceptions. For every ground atom A: if K entails
  A, the report of A is (1, 0, 0, 0); if K entails ¬A, it is (0, 1, 0, 0);
  otherwise it is (0, 0, 0, 1). No atom is in conflict, and no world leaves
  an atom without a value.
- **Direction.** Let r be a statement with a written head H that is
  uncertain or has an exception. Every application that uses r, single or
  of a proof, has the head H. In a proof that uses r, every literal other
  than H that the proof implies is implied by its premises and its non-goal
  clauses, without r.
- **Equivalent clause notation.** Replacing a certain statement without an
  exception by another notation of the same clause, with its identity kept,
  changes no report: for example `p ; -f.`, `p :- f.` or `-f :- -p.`.
- **What a directed statement can change.** Let J be a finite ground input
  I with one more directed statement, whose head atom is h. Let A be an atom
  other than h that does not depend on h, directly or through other atoms,
  in the dependency graph of J. Then A has the same state in every world of
  I and of J with the same numbers, and so the same report. In an input
  that has heads on its exceptions, adding a statement with an exception
  therefore changes only the atom of its head and the atoms that depend on
  it.
- **The clause rule.** For one world and one group with m listed clauses of
  the cycle, the clause rule makes at most m + 2 evaluations of the group.
  At a result with values, a proof that passes its other requirements is
  excluded exactly when one of its listed clauses is contradicted.
- **Well-definedness and order independence.** In the narrowing of a group
  G, the additions to the sure set and to the possible set are monotone and
  reach unique least fixed points. The sure set only grows, the possible
  set only shrinks, the sure set stays inside the possible set, and no atom
  has both its literals in the sure set. Fixing atoms in conflict restarts
  the narrowing at most |G| times. The exception pass ends and gives every
  atom exactly one of the states positive, negative, conflict, ignorance
  and no value. The result does not depend on the order of the statements,
  on the order of the literals in a clause, on the names of the atoms, or
  on the order in which groups that do not depend on each other are
  evaluated.
- **The sweep lemma.** Let G be a sweep group of an evaluation. All
  applications with a body literal in G have heads of one sign s, and their
  body literals in G have the sign s. From sweep to sweep the set of atoms
  of G in the state of sign s only grows. The states are final after at
  most |G| + 1 sweeps, and the set of atoms with the sign s is then the
  least fixed point of one sweep.
- **Locality and containment of inconsistency.** For a set of question
  atoms Q, let C(Q) be the smallest set of atoms, events included, that
  contains Q and is closed under adding the atoms of the body literals, the
  exception literals and the listed clauses of every application for A or
  ¬A with A in C(Q). Removing all applications whose head atom lies outside
  C(Q) leaves the state of every atom of C(Q) unchanged in every world, and
  so it keeps the joint report of Q.
- **No self-support.** In every world and for every group G without a
  normal default whose clause rule, if it ran, ended with a result, the
  literals of G whose atoms end with their sign can be numbered so that
  each of them has an application for it that applies and whose body
  literals are usable literals of atoms outside G or literals of G with a
  smaller number.
- **Agreement with the well-founded semantics.** Let a finite ground
  program consist of facts and rules whose written heads, body literals and
  exception literals are all positive atoms, with each exception read as a
  negation-as-failure test. If every clause has the confidence 1, every
  atom that is true in the well-founded model has the report (1, 0, 0, 0),
  and every atom that is false in it has (0, 0, 0, 1). If the well-founded
  model leaves no atom undefined, the positive atoms are exactly its true
  atoms. If every rule has the confidence 1, every atom has at most one
  fact, and for every choice of a subset of the facts the program of the
  chosen facts and the rules has a well-founded model without undefined
  atoms, then the support semantics and the distribution semantics give
  the same joint distribution of the set of atoms that come out positive.
- **A four-state Bayesian network for acyclic programs.** Let the
  dependency graph of a finite ground program have no dependency cycle.
  Under the support semantics, the joint distribution of the states of all
  ground atoms, events included, is that of a Bayesian network on the
  dependency graph. The parents of an atom are the atoms it depends on. For
  each assignment of states to the parents, the conditional probability of
  each state of the atom is the measure of the set of pairs (U_A, V_A) for
  which the tables of Section 11.6 give that state: the length of an
  interval where only U_A is read, an area where V_A is read too. The
  exact computation of a marginal is therefore
  #P-hard in general. A demonstrator in gk's source repository implements
  both directions of this correspondence: finite acyclic support rules to a
  four-state network, and a finite binary network to support rules. It
  compares gk with the exact values.
- **Cells.** Two worlds that lie in one cell (Section 13) give every atom
  the same state, or give it no value in both. **The exact value is the
  limit of sampling.** Draw N worlds independently, and let f_N be the
  fraction of them in which an atom A has a given state. Let e be the sum of
  the volumes of the cells in which A has that state. Then f_N tends to e
  with probability 1 as N grows, and for every ε > 0 the probability that
  |f_N − e| ≥ ε is at most 2 exp(−2Nε²).
- **Exactness of the procedure.** For every covered input and every signed
  ground question, every task of the exact method's procedure (Section
  10.3) ends. The report that the semantics gives to the collected
  applications, with all four shares and the share of worlds without a
  value, is the report of the question in the whole ground input. A run in
  rounds reaches the same report at a finite checkpoint when it keeps the
  pending work and the candidates of every task, eventually completes
  every inference, grounding and demand that the procedure requires,
  computes the rules that depend on the whole collection anew at each
  checkpoint, and completes the evaluation of the resulting collection.
  Later completed evaluations keep the report.
- **Lifting.** For a covered input and a task for H: every proof of H that
  the ground search accepts is extracted from some first-order derivation
  of the task, and every ground candidate that is extracted and accepted is
  such a proof. When the set of derived clauses with their records of
  statements is closed (every factor, every pair of clauses, a clause
  paired with a fresh copy of itself included, and every candidate
  extraction has been processed, and nothing new arises up to the renaming
  of variables), the task has every proof of H. Every proof that the ground
  search accepts has a ground derivation of a bounded height, so a
  terminating search without grounding exists. A search that only waits
  for the set to close has no guarantee that it ends.
- **Binding variables from facts and earlier answers.** In the two classes
  of Section 10.3, every proof of several statements is made redundant by a
  single application or has a body that can never hold. The report of a
  question then depends only on the ground facts and the successful ground
  instances of the rules, which a search that matches rule bodies against
  facts and earlier answers enumerates.

## 13. The reference tool

The reference tool `mcref` 1.3.0 computes the definition of this page
directly. It is a standalone Python 3 program in
[`../mcref/`](../mcref/README.md). Its evaluation code is independent of gk's.
For input in gk's clause syntaxes it calls gk only as a parser. It gives a
numerical check of hand derivations, and of both methods of gk on the
inputs that the tool accepts.

**Preparing the finite problem.** The tool grounds every statement over
the constants of the input and builds the single applications (Sections
11.2 and 11.3). It finds the proofs of several statements by resolution on
clauses that keep the set of statements they were derived from. A derived
clause is discarded when another derived clause has a subset of its
literals and a subset of its statements. A retained clause that contains Q
and was derived from the statements L is the proof (L, G) of Q, with G the
opposites of its other literals. A rule with a written head that is
uncertain or has an exception takes part only in the search for its own
head. The tool then applies the redundancy rule. It leaves out the
applications whose body can never hold or can hold only when their head
already holds. Last, it forms the groups and the layers.

**One world.**

```
take the numbers U_A and V_A of every ground atom
for each layer of exceptions:
    evaluate without the applications of that layer and above
    remove the applications of the layer whose exception is usable
evaluate all applications that are not removed: each group after the groups it
    depends on, by the tables, by sweeps, by the narrowing or by the clause rule
restore a removed application whose exception is no longer usable, and evaluate again
record each atom as positive, negative, conflict, ignorance or without a value
```

Take Tweety stage 3a (Section 9.1), and suppose that U is .3 for
`seabird(tweety)`, .6 for `gull(tweety)`, .5 for `yellow_bill(tweety)` and
.1 for `flies(tweety)`. The seabird fact and the yellow-bill fact pass.
`gull` has the positive support .9 and the negative support .7, and its
number .6 lies below both, so its state is conflict. Negative gull is not a
usable premise, so `penguin` is not established. The flying default then
passes, since .1 < .9, and the world counts as positive. Without the
yellow-bill statements the same numbers make `gull` negative and `penguin`
positive, the rank-3 default establishes `-flies(tweety)`, and the world
counts as negative. No number is drawn again when an atom is used a second
time or a cycle returns to it.

The tool has two methods.

- **Exact evaluation.** The tool splits the world space at the thresholds
  that its tests use: the support levels of sets of applications, for U_A
  and for V_A. The thresholds divide each unit interval into finitely many
  pieces, and the pieces of all atoms together divide the world space into
  **cells**. Within a cell every test has the same outcome, and every state
  is constant. The tool evaluates one world in each cell and adds the volume
  of the cell to the state it finds for each atom. The result is the report
  itself, exact up to the rounding of floating-point numbers, with no
  sampling error. The number of cells grows with the number of uncertain
  statements that depend on each other. The tool uses exact evaluation up
  to a set number of cells, 300,000 by default.
- **Sampling.** Above that limit, or on request, the tool draws N worlds
  and divides each count by N. The first four fractions estimate the
  report. The fifth is the share of worlds without a value, and nothing is
  rescaled. The tool reports 95 % intervals for the four shares of one
  answer together. By Hoeffding's inequality and a union bound their common
  half-width is √(ln(8/.05) / (2N)), which is .0113 at 20,000 worlds and
  .0050 at 100,000. The interval bounds the sampling error of one answer,
  not of all answers of a collection together, and a value inside it is not
  shown to be exact.

The two methods compute the same quantity. They share the reading of the
input, the construction of the applications and the evaluation of one
world, and they differ only in which worlds they evaluate. A sampled world
lies in a cell with the probability of the cell's volume, so the sampled
fractions tend to the exact values (Section 12).

**Running the tool.** From the repository root:

    python3 mcref/mcref.py Examples/semantics/penguin.gkp

| option | meaning | default |
|---|---|---|
| `--mode auto` | exact evaluation when the cells are at most `--max-cells`, sampling above it | `auto` |
| `--mode exact`, `--mode sampling` | one method only | |
| `--max-cells N` | the cell limit of exact evaluation | 300000 |
| `--samples N` | the number of sampled worlds | 100000 |
| `--seed N` | the seed of the random numbers | 1 |
| `--max-ground N` | the limit of the grounding work | 200000 |
| `--all-atoms` | also report every ground atom | off |

The tool prints one JSON line, `{"mcref": {...}}`. `answers` has one entry
per ground instance of the question, with `value` (the four shares) and
`unstable` (the share of worlds without a value). `mode` names the method,
and `error_bound` is 0 for exact evaluation and the half-width above for
sampling.

**Scope and limits.** The grounding is finite. A statement with v variables
over d constants has d^v instances, and the tool declines function
symbols, equality and some further constructs, with a stated reason. The
lineage of Section 9.1 is therefore outside the tool. The search for
proofs has limits on the number of derived clauses and of proofs. When a
limit is reached, the tool evaluates with the single applications only and
says so in its output. Its values are then not those of the definition.
The cost grows with the cells or the worlds and with the size of the
groups. More worlds narrow the interval, but they add no inference, and
they give no value to worlds without a value.

## 14. Relation to other systems

On positive programs the semantics gives the numbers of the distribution
semantics of ProbLog, PRISM and related probabilistic logic languages
(Section 4). Beyond that fragment, the treatment of opposition (the shared
number), of exceptions and of ranks is a set of stated rules. These rules
are not consequences of probability theory, and they need not agree with
other encodings of negation, conflict or priority. The four states
resemble Belnap's four values. The rule that a premise in conflict supports
nothing further is this semantics' own. Normal defaults and ranks relate to
Reiter's defaults and Brewka's priorities. The narrowing adapts the lower
and upper fixed point of the well-founded semantics to four states.
Executable comparisons with ProbLog, PASTA, TweetyProject, clingo, DLV and
s(CASP) are in
[comparison_with_other_systems.md](comparison_with_other_systems.md).

**The conflict state has no counterpart.** The inconsistent world of
Section 6, `0.8::r`, `0.2::-p`, `p :- r`, shows the difference on one case.
In this case `r` and `-p` are both in force, in .8 × .2 = .16 of the
worlds.

| treatment | `p` | what happens to the inconsistent case |
|---|---|---|
| this semantics (gk, the tool) | (.64, .04, .16, .16) | kept apart as its own share, conflict |
| `-p` written as a separate predicate without a logical connection to `p` | `p` .8 | counted as `p`: `p` holds exactly where `r` holds |
| the same with the constraint "not both" as evidence | `p` .64 / .84 ≈ .762 | deleted, and the rest scaled up |

The values of the other two rows follow from their definitions by hand.
The .64 of this semantics is the share where `p` holds and nothing stands
against it. The .64 plus the conflict .16 is the .8 of the first other
reading.

**Answer set systems with probabilities.** A choice of facts can have
several stable models or none. Then PASTA reports an interval, smProbLog
divides the share of the choice equally among its stable models, and plingo
normalizes over all stable models. On Tweety stage 2, take the .24 of
worlds where the seabird fact holds and the report against gull does not.
This share has two stable models, one with a gull and one with a
penguin. Flying holds in the
worlds without the seabird fact, .2 × .9 = .18, and in the gull model of
the two-model share, .24 × .9 = .216. So PASTA's interval is [.18, .396],
smProbLog's value is .18 + .216 / 2 = .288, and plingo's value is
(.18 + .216) / 1.24 ≈ .319. The support share is .396. These are different
quantities, not approximations of one target.

## 15. Glossary

| term | meaning |
|---|---|
| atom | a predicate applied to arguments, `flies(t)`; ground when it has no variables |
| literal | an atom or its negation; its opposite has the other sign |
| statement | one input fact, rule or disjunction, with its confidence, written head and exception literals |
| confidence, strength | the number in [0, 1] written on a statement; a strength belongs to an application or a side and is computed |
| written head | the head of a rule as written, or the head read from a default (Section 11.1) |
| directed rule | a rule with a written head that is uncertain or has an exception; used only towards its head |
| certain clause | a certain statement without an exception; used in every direction |
| source event | the hidden atom that makes all uses of an uncertain clause without a written head one event |
| identity of a rule | the mark of an uncertain rule with a body literal; a rule used in several applications holds or fails once |
| application | a ground inference step that can conclude one literal: head, body literals, exception literals, listed clauses, strength |
| single application | an application of one statement |
| proof of several statements | a pair (L, G) of statements and premises that implies a literal classically, with the four conditions of Section 11.4 |
| premise | a literal of G in a proof; it is tested at its own atom |
| listed clause | a non-goal clause with several literals of a proof; the application applies only where it is not contradicted |
| redundancy rule | the rule that drops the application of a proof when another application requires no more |
| no self-support | the rule that leaves out an application whose body can hold only when its head already holds |
| world | two random numbers U and V for every ground atom, events included |
| usable | a literal whose atom has the state of its sign |
| has evidence | a literal whose atom has its sign or is in conflict |
| contradicted | a listed clause the opposite of each of whose literals has evidence |
| applies | an application not removed by the exception pass, with usable premises, no contradicted listed clause and no usable external exception |
| side, kind | the applications for or against an atom that apply; normal when all are normal defaults, ordinary otherwise, decided in each world |
| support level | the strength of a side: noisy-or of its applications, each uncertain rule counted once |
| positive, negative, conflict, ignorance | the four states; the report gives their shares over worlds |
| no value | the outcome of an atom that the procedure for a cycle leaves without a state; its share is reported beside the four shares (gk's field `unresolved`) |
| signed confidence | the share for minus the share against |
| shared number | the one number U of an atom on which both ordinary sides are tested |
| normal default | an application whose exception is the opposite of its own head; its rank is the number in that exception |
| rank | the priority of a normal default; rank 0 states no priority |
| external exception | any other exception literal; the application applies only where none is usable |
| exception pass | the evaluation in layers that removes applications with usable external exceptions and restores them when the exceptions stop being usable |
| layer | the order of an application or a literal in the exception pass |
| held out | absent from one evaluation of the exception pass |
| dependency graph | atom A depends on the atoms of the body literals, external exception literals and listed clauses of the applications for A or ¬A |
| group | a strongly connected component of the dependency graph |
| cycle across signs | a group in which an application reads a literal of the other sign, or two applications have heads of opposite signs |
| sweep group | a group of one sign without an exception or a normal default inside; evaluated by sweeps |
| narrowing | the computation of the sure and the possible literals of a group |
| sure, possible | the literals the narrowing has justified, and the literals it has not yet ruled out |
| fixed | an atom whose final state the procedure has given in this world |
| clause rule | the procedure for a group in which a proof lists a clause of the group |
| cell | a part of the world space in which every test of the evaluation has the same outcome |
| snapshot | the applications that gk has collected at a checkpoint |
| complete | the mark of an answer of the exact method whose search and evaluation ended without a limit or an approximation |
| reading | the name of a procedure or an approximation that acted on gk's value, printed in `readings` |
