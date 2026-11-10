# O8: further examples of cycles

This part collects the examples of cycles that Appendix A of the paper
refers to as part O8. Each example gives an input, a question and the four
shares (for, against, conflict, ignorance) of the semantics, computed by
hand with the narrowing of Section 4.4 and the definitions of Appendix A.
The mutual pair of defaults (example 12) and the Yale shooting (example
13) are the two symmetric situations of Appendix A.2.4.

Each question has its own input file in `inputs/`, with the clauses of the
example only. gk 1.2.5 and the reference tool mcref 1.1.2 ran on every
file; the tables below give both values next to the hand value.

## Rerun

From the repository root:

```sh
./bin/gk paper2026/O8_cycles/inputs/01_chain_q.gkp
python3 mcref/mcref.py paper2026/O8_cycles/inputs/01_chain_q.gkp --samples 100000 --seed 1
python3 paper2026/check_gk.py --part O8 --mcref
```

The column "check" says whether gk prints the hand value at its printed
precision and whether each estimate of mcref lies within .0050 of the hand
value. .0050 is the half-width for 100,000 worlds (Section 5 of the
paper): each share lies within it with 95 % confidence.

## The six rules

The examples name six rules of the semantics:

- **Chain conflict.** A chain is a sequence of certain applications, each
  reading the head of the previous one. When the evidence establishes the
  start of a chain and the complement of its end, step 5 of the narrowing
  fixes every atom of the chain in conflict.
- **Chain stop.** A fact, or an application with a body established
  outside the group, counts in both the sure and the possible set. An atom
  with such opposing evidence of its own is in conflict, and the chain
  ends there.
- **Nothing from conflict.** An atom in conflict supplies no usable
  literal of either sign.
- **Ordinary first.** In a cycle across signs with normal defaults, the
  ordinary applications are evaluated alone first. Their settled atoms
  keep their states.
- **Sweep groups.** A cycle group of one sign, without an exception
  literal inside, without a normal default and without an unresolved
  outside atom, is a sweep group: its sweeps settle. Every other cycle
  group goes to the narrowing. In a group without a cycle across signs, an
  atom that the narrowing leaves undecided is in ignorance (the cycle rule of 2026-11-10;
  mcref 1.1.2 gives the same values as 1.1.1 on every example of this
  part).
- **Unresolved.** In a cycle across signs, an atom with a literal that is
  possible but not sure is unresolved. The unresolved share is a fifth
  number, and nothing is rescaled. mcref prints it as `unstable`; its four
  shares then sum to less than 1.

## Results

mcref's estimate lies within .0050 of the value in the paper on 33 of 33
questions. gk prints that value on 24 of 33 questions; on the other 9 gk
records the approximation note `cycle cut` on 9, and its value differs. The cycle cut
is the approximation of Section 6.5 of the paper; the paper prints no gk
value for these questions, except the Yale shooting, where Section 7.1
states gk's value (0, 1, 0, 0) with a cycle-cut note.

| input | question | value in the paper | gk 1.2.5 | gk's approximation notes | mcref 1.1.2, 100,000 worlds | check |
|---|---|---|---|---|---|---|
| `inputs/01_chain_q.gkp` | `q` | (.64, .04, .16, .16) | (.64, .04, .16, .16) | cycle cut | (.64038, .04076, .16018, .15868) | gk equals it; mcref within .0050 |
| `inputs/01_chain_p.gkp` | `p` | (.64, .04, .16, .16) | (.64, .04, .16, .16) | cycle cut | (.64038, .04076, .16018, .15868) | gk equals it; mcref within .0050 |
| `inputs/01_chain_r.gkp` | `r` | (.64, .04, .16, .16) | (.64, .04, .16, .16) | cycle cut | (.64038, .04076, .16018, .15868) | gk equals it; mcref within .0050 |
| `inputs/02_uncertain_bird_bird.gkp` | `bird(t)` | (0, .2, .8, 0) | (0, .2, .8, 0) | cycle cut | (0, .19948, .80052, 0) | gk equals it; mcref within .0050 |
| `inputs/02_uncertain_bird_flies.gkp` | `flies(t)` | (0, .2, .8, 0) | (0, .2, .8, 0) | cycle cut | (0, .19948, .80052, 0) | gk equals it; mcref within .0050 |
| `inputs/02_uncertain_bird_sings.gkp` | `sings(t)` | (1, 0, 0, 0) | (1, 0, 0, 0) | none | (1, 0, 0, 0) | gk equals it; mcref within .0050 |
| `inputs/03_chain_stop_q.gkp` | `q` | (.2, .3, .2, .3) | (.2, .3, .2, .3) | cycle cut | (.20069, .30027, .20069, .29835) | gk equals it; mcref within .0050 |
| `inputs/03_chain_stop_p.gkp` | `p` | (.2, .15, .6, .05) | (.2, .15, .6, .05) | cycle cut | (.20069, .15063, .59987, .04881) | gk equals it; mcref within .0050 |
| `inputs/03_chain_stop_certain_q.gkp` | `q` | (0, 1, 0, 0) | (0, 1, 0, 0) | cycle cut | (0, 1, 0, 0) | gk equals it; mcref within .0050 |
| `inputs/04_two_routes_q.gkp` | `q` | (.612, 0, 0, .388) | (.036, 0, 0, .964) | cycle cut | (.61173, 0, 0, .38827) | gk differs from the target; mcref within .0050 |
| `inputs/04_two_routes_swapped_q.gkp` | `q` | (.612, 0, 0, .388) (the same value in either order) | (.576, 0, 0, .424) | cycle cut | (.61173, 0, 0, .38827) | gk differs from the target; mcref within .0050 |
| `inputs/05_own_consequence_p.gkp` | `p` | (.1, 0, .9, 0) | (1, 0, 0, 0) | cycle cut x2 | (.0988, 0, .9012, 0) | gk differs from the target; mcref within .0050 |
| `inputs/05_own_consequence_q.gkp` | `q` | (.1, 0, 0, .9) | (1, 0, 0, 0) | cycle cut x2 | (.0988, 0, 0, .9012) | gk differs from the target; mcref within .0050 |
| `inputs/05_fact_against_fact_p.gkp` | `p` | (.1, 0, .9, 0) | (.1, 0, .9, 0) | none | (.09985, 0, .90015, 0) | gk equals it; mcref within .0050 |
| `inputs/05_own_consequence_default_p.gkp` | `p` | (1, 0, 0, 0) | (1, 0, 0, 0) | cycle cut x3 | (1, 0, 0, 0) | gk equals it; mcref within .0050 |
| `inputs/06_three_facts_p.gkp` | `p` | (0, 0, 1, 0) | (0, 0, 1, 0) | cycle cut x3 | (0, 0, 1, 0) | gk equals it; mcref within .0050 |
| `inputs/06_three_facts_q.gkp` | `q` | (0, 0, 1, 0) | (0, 0, 1, 0) | cycle cut x3 | (0, 0, 1, 0) | gk equals it; mcref within .0050 |
| `inputs/06_three_facts_r.gkp` | `r` | (0, 0, 1, 0) | (0, 0, 1, 0) | cycle cut x3 | (0, 0, 1, 0) | gk equals it; mcref within .0050 |
| `inputs/07_disjunction_cycle_b.gkp` | `b` | (.56, .06, .24, .14) | (.56, .06, .24, .14) | cycle cut | (.56021, .05952, .23925, .14102) | gk equals it; mcref within .0050 |
| `inputs/07_directed_rule_b.gkp` | `b` | (.5, 0, .3, .2) | (.5, 0, .3, .2) | none | (.50074, 0, .29801, .20125) | gk equals it; mcref within .0050 |
| `inputs/08_one_clause_q.gkp` | `q` | (.68, 0, 0, .32) | (1, 0, 0, 0) | cycle cut | (.68063, 0, 0, .31937) | gk differs from the target; mcref within .0050 |
| `inputs/09_default_certain_rule_flies.gkp` | `flies(p)` | (.18, .8, 0, .02) | (.18, .8, 0, .02) | cycle cut | (.17932, .80056, 0, .02012) | gk equals it; mcref within .0050 |
| `inputs/10_fact_default_rule_r.gkp` | `r` | (.5, .45, 0, .05) | (.05, .45, .45, .05) | cycle cut | (.50006, .45, 0, .04994) | gk differs from the target; mcref within .0050 |
| `inputs/10_fact_default_rule_p.gkp` | `p` | (.45, .5, 0, .05) | (.45, .5, 0, .05) | cycle cut | (.45, .50006, 0, .04994) | gk equals it; mcref within .0050 |
| `inputs/11_ordinary_first_p.gkp` | `p` | (.8, 0, 0, .2) | (.8, 0, 0, .2) | cycle cut x3 | (.80052, 0, 0, .19948) | gk equals it; mcref within .0050 |
| `inputs/12_mutual_pair_p.gkp` | `p(a)` | (0, 0, 0, 1) | (0, 0, 0, 1) | cycle cut x2 | (0, 0, 0, 1) | gk equals it; mcref within .0050 |
| `inputs/12_mutual_pair_b.gkp` | `b(a)` | (0, 0, 0, 1) | (0, 0, 0, 1) | cycle cut x2 | (0, 0, 0, 1) | gk equals it; mcref within .0050 |
| `inputs/12_mutual_pair_half_p.gkp` | `p(a)` | (.25, 0, 0, .75) | (.25, 0, 0, .75) | cycle cut x2 | (.24991, 0, 0, .75009) | gk equals it; mcref within .0050 |
| `inputs/13_yale_alive.gkp` | `alive(s2)` | (0, 0, 0, 0) (the reference tool: unresolved share 1) | (0, 1, 0, 0) | cycle cut x3 | (0, 0, 0, 0) | gk differs from the target; mcref within .0050 |
| `inputs/13_yale_099_alive.gkp` | `alive(s2)` | (.01, .99, 0, 0) | (.01, .99, 0, 0) | none | (.01034, .98966, 0, 0) | gk equals it; mcref within .0050 |
| `inputs/13_yale_q.gkp` | `q` | (1, 0, 0, 0) | (1, 0, 0, 0) | cycle cut x3 | (1, 0, 0, 0) | gk equals it; mcref within .0050 |
| `inputs/13_yale_walks.gkp` | `walks(s2)` | (0, 0, 0, 0) (the reference tool: unresolved share 1) | (0, 0, 0, 1) | cycle cut x3 | (0, 0, 0, 0) | gk differs from the target; mcref within .0050 |
| `inputs/13_yale_buried.gkp` | `buried(s2)` | (0, 0, 0, 0) (the reference tool: unresolved share 1) | (1, 0, 0, 0) | cycle cut x3 | (0, 0, 0, 0) | gk differs from the target; mcref within .0050 |


## Notes on the examples

1. **A longer chain** (`01_chain_*.gkp`): in the .16 share where both
   facts pass, all three atoms are in conflict. A chain of any length
   gives the same numbers.
2. **The uncertain bird** (`02_*.gkp`): in .8 of the worlds the chain from
   `bird(t)` to `flies(t)` starts at an established atom and ends at an
   atom with a fact against it. In the other .2, `-flies(t)` gives
   `-bird(t)` by the rule read backwards. The added fact `sings(t)` lies in
   another group and stays (1, 0, 0, 0).
3. **A chain stop** (`03_*.gkp`): where `r`, `-p` and `-q` all pass (.2),
   the chain from `r` reaches `p`; the fact `-p` is in force, so `p` is in
   conflict and the chain ends there; `q` keeps only its fact `-q`. Where
   `r` and `-q` pass and `-p` fails (.2), the chain runs to its end and all
   three atoms are in conflict. In the all-certain version `r` and `p` are
   in conflict and `q` is negative from its fact.
4. **Two routes from both sides of a conflict** (`04_*.gkp`): in .64 of
   the worlds `p` is positive and `q` has support .9; in .04 `r` is
   negative and `q` has support .9; in .16 `r` and `p` are both in
   conflict, and neither route is usable.
5. **A fact opposed by its own consequence** (`05_*.gkp`): in .9 of the
   worlds the fact, the certain rule and the uncertain rule are all in
   force, and `p` is in conflict. `q` has `p` as its only route. As a
   normal default, the opposing rule yields to the fact.
6. **Three facts that cannot all hold** (`06_*.gkp`): each atom is
   established, and a certain clause derives its complement from another
   atom.
7. **An uncertain disjunction in a cycle** (`07_*.gkp`): the disjunction
   has one source event with confidence .8. Where it passes, `b` has
   support 1 from `a`; `b` is in conflict where `-b` also passes (.24) and
   positive elsewhere (.56). Where it fails, `b` is negative where `-b`
   passes (.06) and in ignorance elsewhere (.14). The directed rule
   `0.8::b :- a` has no source event, and .8 and .3 meet on the one number
   of `b`.
8. **One clause at a time** (`08_one_clause_q.gkp`): classical logic proves
   `q` by cases on `r`. The applications of the semantics each use one
   clause, and no single application expresses the proof by cases.
9. **A normal default meets a certain rule** (`09_*.gkp`): in .8 of the
   worlds `penguin(p)` is positive and `-flies(p)` follows by the certain
   rule. That evidence is ordinary, so the normal default yields. Without
   the rule "ordinary first" the normal default would give `-penguin(p)`
   by the certain rule read backwards, and the value would be
   (.9, .08, 0, .02). This second value is a hand calculation; no version
   of the reference tool computes it.
10. **A fact, a normal default and a certain rule** (`10_*.gkp`): the
    certain rule also gives `-p` from `r`. Where `r` passes, `-p` follows
    and the normal default yields. Where `r` fails, the default holds in
    .9 and gives `-r`.
11. **The ordinary evidence is fixed first** (`11_*.gkp`): the fact fixes
    `p` positive before the normal default for `q` is considered.
12. **A mutual pair of defaults** (`12_*.gkp`): each rule applies when the
    head of the other rule is not usable. The group has exception literals
    inside, so the narrowing evaluates it, and it finds neither atom sure. With confidence .5 on both rules, `p(a)` is
    positive where its rule passes and the other rule fails.
13. **The Yale shooting** (`13_*.gkp`): the last rule is certain, so it
    also gives `-loaded(s1)` from `alive(s2)`. The atoms `alive(s2)` and
    `loaded(s1)` form one group with a cycle across signs. The input has
    two consistent accounts: the gun stays loaded and the shot kills, or
    the person stays alive and the gun was unloaded. Neither atom becomes
    sure, so the question is unresolved in every world: mcref prints the
    four shares (0, 0, 0, 0) and the unresolved share 1. With the last
    rule at .99 the rule is directed. The fact `q` makes `q` sure; the
    only route of `walks(s2)` needs the undecided atom; the exception of
    `buried(s2)` may or may not block.
