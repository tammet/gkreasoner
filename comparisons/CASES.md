# Comparison cases

One section per row of the comparison table in [README.md](README.md). The
gk input of each case is quoted verbatim and can be copied and run as a
whole. The external input files of each cell are listed in
`manifest.json`.

Each gk result is the value of gk 1.2.3 run without options (gk 1.2.5 gives
the same values), which is the
recursive method. A value is written as four shares (for, against,
conflict, ignorance). The table shows the signed confidence, for minus
against. The explanations use the support semantics
([`../Doc/support_semantics.md`](../Doc/support_semantics.md)): each atom
has one number in a world, and the evidence for and against an atom is
tested against that one number.

## C1: independent causes

Purpose: same-polarity aggregation of two independent uncertain causes.

Input `inputs/gk/c1.gkp`:

```text
0.5::a.
0.6::b.

q :- a.
q :- b.

query(q).
```

gk result: (.80, 0, 0, .20). The two causes are independent, so the
share for is 1 - (1 - .5)(1 - .6) = .80.

Comparison: ProbLog, PASTA, plingo, and smProbLog return
1 - (1-.5)(1-.6) = .80. The non-probabilistic systems return no
probabilities (U).

## C2: conjunctive causes

Purpose: conjunction of two uncertain premises.

Input `inputs/gk/c2.gkp`:

```text
0.5::a.
0.6::b.

q :- a, b.

query(q).
```

gk result: (.30, 0, 0, .70); .30 = .5 x .6.

Comparison: same agreement and classification pattern as C1.

## D1: uncertain contrary exception

Purpose: a default opposed by evidence for the explicit negation, resolved
in one report.

Input `inputs/gk/d1.gkp`:

```text
bird(a).
0.9::-flies(a).

flies(X) :- bird(X), unless(-flies(X)).

query(flies(a)).
```

gk result: (.10, .90, 0, 0), signed confidence -.80. The fact
`-flies(a)` holds in .9 of the worlds; there it blocks the default, and
the share against is .90. In the other .1 the default applies.

Comparison: the probabilistic analogues compile the exception to negation
as failure and answer the two queries separately, .10 and .90. The crisp
encodings make the exception fact certain and answer no/yes.

## D2: facts and a default, all with confidences

Purpose: input confidences on facts and on a default rule, combined
through a recursively evaluated exception condition.

Input `inputs/gk/d2.gkp`:

```text
0.7::b.
0.3::-b.

0.9::h :- unless(b).

query(h).
```

gk result: (.54, 0, 0, .46). The evidence for `b` (.7) and against it
(.3) is tested against the one number of `b`, so `b` holds alone in
.7 - .3 = .4 of the worlds. The default is blocked there and applies
with .9 elsewhere: .9 x (1 - .4) = .54.

Comparison: the translations replace the default by an independent .9
activation guarded by the absence of `b`, giving .9 x (1 - .7) = .27,
with the `-b` fact disconnected. The recursive evaluation of the
exception condition is omitted, so the cells are A.

## D3: contested premise

Purpose: opposition resolved at the contested premise before propagation.

Input `inputs/gk/d3.gkp`:

```text
0.5::b.
0.5::-b.

0.9::h :- b.

query(h).
```

gk result: (0, 0, 0, 1), signed confidence 0 with pure ignorance. The
evidence for and against `b` is equally strong (.5), so `b` never holds
alone: where the evidence for `b` passes, the evidence against it passes
too. The rule for `h` never applies.

Comparison: the guarded translation counts the worlds where `b` is active
and its opposing atom inactive: .9 x .5 x (1 - .5) = .225. The crisp
encodings answer no.

## D4: Nixon defaults

Purpose: equally ranked opposed defaults; mutual blocking.

Input `inputs/gk/d4.gkp`:

```text
quaker(n).
republican(n).

pacifist(X) :- quaker(X), unless(-pacifist(X), 2).
-pacifist(X) :- republican(X), unless(pacifist(X), 2).

query(pacifist(n)).
```

gk result: (0, 0, 0, 1), signed confidence 0 with pure ignorance. The
two defaults have the same rank and block each other.

Comparison: the conflict is native in the stable-model and argumentation
systems, with differing output types: PASTA a credal interval [0,1] per
query, plingo and smProbLog .50/.50, TweetyProject two undecided
arguments, clingo and DLV two stable models, s(CASP) two queries
succeeding in separate partial stable models.

## D4-P: probabilistic Nixon premises

Purpose: probabilities on the Nixon premises; a negation-as-failure cycle
under probabilities.

Input `inputs/gk/d4sm_pos.gkp`:

```text
0.8::quaker(n).
0.6::republican(n).

pacifist(X) :- quaker(X), unless(-pacifist(X), 2).
-pacifist(X) :- republican(X), unless(pacifist(X), 2).

query(pacifist(n)).
```

Input `inputs/gk/d4sm_neg.gkp`: the same program with
`query(-pacifist(n)).`

gk result: (.32, .12, 0, .56) for `pacifist(n)` and (.12, .32, 0, .56)
for `-pacifist(n)`, signed confidences +.20 and -.20. Where only
`quaker(n)` holds (.8 x .4 = .32), the first default applies. Where only
`republican(n)` holds (.2 x .6 = .12), the second applies. Where both
hold (.48), the defaults have equal rank and block each other. These
worlds and those where neither holds (.08) give the ignorance .56. The
gk row uses an equal-priority analogue whose defaults use the contrary
conclusion as the exception condition, and is marked A. The shares for,
.32 and .12, equal the lower bounds of the PASTA intervals.

Comparison: PASTA, plingo, and smProbLog evaluate the probabilistic
stable-model input natively and return different quantities under their
respective semantics.

## D5: strict priority

Purpose: opposed defaults at different priority ranks.

Input `inputs/gk/d5.gkp`:

```text
0.9::l :- unless(-l, 2).
0.3::-l :- unless(l, 3).

query(l).
```

gk result: (.60, .30, 0, .10), signed confidence .30. The two defaults
are tested against the one number of `l`. Where both pass (.3), the
rank-3 default for `-l` wins. Where only the rank-2 default passes
(.9 - .3 = .6), `l` holds.

Comparison: the translations guard the positive rule by the absence of
the negative activation and answer .63 and .30 as separate queries. The
TweetyProject analogue uses specificity; the crisp encodings answer
no/yes.

## D6: undercutting and rebutting forms

Purpose: representation of the two exception forms. In the first input,
the separate exception atom can only undercut the rule application. In
the second, the exception condition is the explicit negation of the
conclusion; support for it rebuts the conclusion and blocks the default
application.

Input `inputs/gk/d6_undercut.gkp`:

```text
flies(a) :- unless(injured(a)).

query(flies(a)).
```

Input `inputs/gk/d6_rebut.gkp`:

```text
flies(a) :- unless(-flies(a)).

query(flies(a)).
```

gk result: (1, 0, 0, 0) for both forms; neither exception condition has
support in these inputs.

Comparison: every system that runs the case returns 1 or yes for both
forms. The translations give both rules one negation-as-failure form. The
case shows that gk represents the two forms; the outputs do not differ
numerically.

## D7: paired reference-class exception

Purpose: one uncertain condition that undercuts the general default and
supports the contrary conclusion.

Input `inputs/gk/d7.gkp`:

```text
bird(a).
0.6::penguin(a).

0.9::flies(X) :- bird(X), unless(penguin(X)).
0.8::-flies(X) :- penguin(X).

query(flies(a)).
```

gk result: (.36, .48, 0, .16), signed confidence -.12. Where
`penguin(a)` holds (.6), the exception blocks the default, and the rule
for `-flies(a)` applies with .8: the share against is .6 x .8 = .48.
Where it does not hold (.4), the default applies with .9: the share for
is .4 x .9 = .36. mcref gives the same shares within its sampling bound.

Comparison: the external encodings add a rule that applies the default
in the worlds where `penguin(a)` holds and the rule for `-flies(a)` does
not. This rule reproduces the direct method's paired branch: with it,
the encodings return .48/.48. The recursive method does not use such a
branch: an exception that holds blocks the default. So the external
values no longer match gk's value. The cells stay A.

Direct method: `gk -direct` gives signed confidence 0 with .48 for and
.48 against.

## N1: open join query

Purpose: an open query with several answer bindings. Source: Study 4 of
the gk test suite.

Input `inputs/gk/n1_study4.gkp`:

```text
0.5::bird(a).
0.6::bird(b).
twobirds(X,Y) :- bird(X), bird(Y).
query(twobirds(X,Y)).
```

gk result: (.50, .30, .30, .60) over the bindings (a,a), (a,b), (b,a),
(b,b); each binding has no share against or conflict, and the rest of
its value is ignorance.

Comparison: ProbLog, plingo, and smProbLog return the same values; PASTA
returns each value as both interval endpoints; clingo, DLV, and s(CASP)
return the binding set without probabilities.

## N2: open recursive query

Purpose: an open query over a recursive program. Source: Study 10 of the
gk test suite.

Input `inputs/gk/n2_study10.gkp`:

```text
0.8::stress(ann).
0.4::stress(bob).
0.6::influences(ann,bob).
0.2::influences(bob,carl).
smokes(X) :- stress(X).
smokes(X) :- influences(Y,X), smokes(Y).
query(smokes(X)).
```

gk result: ann .80, bob .688, carl .1376, as shares for; the rest of
each value is ignorance.

Comparison: same agreement pattern as N1.

## EQ1: uncertain equality, opposed evidence

Purpose: an input confidence on an equality combined with opposed
evidence.

Input `inputs/gk/e1.gkp`:

```text
0.9::p(a).
0.7::-p(b).
0.8::(a = b).

query(p(a)).
```

gk result: (.396, .056, .504, .044), signed confidence .34.
Paramodulation derives `-p(a)` from `-p(b)` and `a = b`. That evidence
against holds in .7 x .8 = .56 of the worlds and depends on the numbers
of `p(b)` and `a = b`, not on that of `p(a)`. So it is independent of the
fact `p(a)` (.9): conflict .9 x .56 = .504, for alone .9 x .44 = .396,
against alone .1 x .56 = .056, neither .1 x .44 = .044. The conflict
share equals smProbLog's inconsistent mass .504. mcref does not accept
equality, so no sampled value is recorded for this case.

Direct method: `gk -direct` gives the same signed confidence .34 with the
shares (.34, 0, .56, .10).

Comparison: the tested configurations do not accept an input confidence
on an equality. The encodings state it as a probabilistic fact with
substitution rules for both polarities of the one predicate; the joint
world derives `p(b)` and `-p(b)` and produces an inconsistent world.

- PASTA: reported error; its semantics is undefined when a world has no
  answer set.
- plingo: .79839 after renormalizing over the consistent worlds.
- smProbLog: .82; inconsistent mass .504.
- clingo, DLV: no models.
- s(CASP): no models with the acyclically directed substitution rules of
  the tested input; with symmetric rules the query does not terminate.
- ProbLog: U. The tested input does not encode explicit classical
  negation; the recorded file
  [`inputs/problog/problog_e1.pl`](inputs/problog/problog_e1.pl) keeps
  `-p(b)` as a fresh atom and returns .9 and .56 as two unrelated
  numbers.

## X1: unrelated contradiction tolerance

Purpose: contradictory evidence about one atom beside an unrelated query.

Input `inputs/gk/x1.gkp`:

```text
0.7::p(a).
0.6::-p(a).
q(b).

query(q(b)).
```

gk result: (1, 0, 0, 0). The contradiction is not used in the query
proof.

Comparison: the ASP-based encodings state the contradictory pair through
strong negation; smProbLog uses a fresh atom with an incompatibility
constraint.

- clingo, DLV: no models for the whole program.
- s(CASP): the query fails.
- PASTA: reported error.
- plingo: 1.0 after renormalizing away the inconsistent mass .42.
- smProbLog: 1.0; inconsistent mass .42.
- ProbLog: U. The tested input format does not encode the contradictory
  pair.

## F1: recursion over function terms

Purpose: a rule applied through a function term; query-directed non-ground
proof search compared with ground-and-solve.

Input `inputs/gk/f1.gkp`:

```text
0.9::bird(a).
0.8::bird(f(X)) :- bird(X).

query(bird(f(f(a)))).
```

gk result: (.576, 0, 0, .424); .576 = .9 x .8 x .8. mcref does not
accept function symbols, so no sampled value is recorded for this case.

Comparison:

- ProbLog: .576; grounds on demand, driven by the query.
- PASTA, plingo, smProbLog, clingo, DLV: grounding timeout at the
  recorded ten-second limit; these systems ground the full program before
  solving, and the function term generates an infinite set of ground
  terms. The PASTA and plingo files omit the rule confidence, which would
  need a probabilistic gate for every ground instance; their grounding
  reaches the timeout either way.
- s(CASP): top-down execution confirms the conclusion without a
  probability.

## DJ1: uncertain classical disjunction

Purpose: a confidence on a classical disjunction with one disjunct
opposed.

Input `inputs/gk/dj1.gkp`:

```text
0.8::p(a) ; q(a).
0.9::-p(a).

query(q(a)).
```

gk result: (.72, 0, 0, .28); .72 = .8 x .9 for the surviving disjunct.

Comparison:

- PASTA: credal interval [.72,.80]; states the disjunctive head directly.
  The lower bound equals the gk value; the upper bound comes from the
  worlds in which the unopposed disjunction leaves both disjuncts
  admissible.
- smProbLog: .76; states the disjunction by the standard even-loop idiom
  and splits each world's mass equally among its stable models.
- plingo: reported error on the disjunctive head.
- ProbLog: U. The tested syntax has no classical disjunction; an
  annotated disjunction distributes .8 among the disjuncts, a different
  statement.
- clingo, DLV, s(CASP): derive the surviving disjunct without a
  probability.
