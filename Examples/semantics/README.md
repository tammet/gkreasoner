# Examples/semantics

The runnable inputs of [`../../Doc/support_semantics.md`](../../Doc/support_semantics.md),
one per example, in the order of that page. Run one from the repository root:

```sh
./bin/gk Examples/semantics/penguin.gkp
```

The reference tool [`mcref`](../../mcref/README.md) computes the same
semantics by sampling:

```sh
python3 mcref/mcref.py Examples/semantics/penguin.gkp --samples 20000
```

| file | section | answer (positive, negative, conflict, ignorance) |
|---|---|---|
| `certain.gkp` | 1 | flies(t) (1, 0, 0, 0) |
| `uncertain_fact.gkp` | 2 | flies(t) (.72, 0, 0, .28) |
| `two_routes.gkp` | 3 | r(c) (.8, 0, 0, .2) |
| `shared_evidence.gkp` | 3 | q (.5, 0, 0, .5) |
| `instances.gkp` | 3 | q (.81, 0, 0, .19) |
| `against_same_atom.gkp` | 4 | flies(a) (.3, 0, .4, .3) |
| `contested_premise.gkp` | 4 | flies(a) (.18, 0, 0, .82) |
| `contested_premise_bird.gkp` | 4 | bird(a) (.2, 0, .3, .5) |
| `external_exception.gkp` | 5 | flies(t) (.45, 0, 0, .55) |
| `exception_variable.gkp` | 5 | q(a) (.225, 0, 0, .775) |
| `penguin.gkp` | 6 | flies(t) (.9, 0, 0, .1); flies(p) (0, 1, 0, 0) |
| `default_vs_fact.gkp` | 6 | flies(t) (.63, .3, 0, .07) |
| `rule_vs_fact.gkp` | 6 | flies(t) (.6, 0, .3, .1) |
| `nixon.gkp` | 6 | pacifist(n) (0, 0, 0, 1) |
| `nixon_uncertain.gkp` | 6 | pacifist(n) (.32, .12, 0, .56) |
| `nixon_ranks.gkp` | 6 | pacifist(n) (1, 0, 0, 0) |
| `disjunction.gkp` | 7 | injured(t) (.6, 0, 0, .4) |
| `disjunction_certain.gkp` | 7 | injured(t) (1, 0, 0, 0) |
| `contraposition.gkp` | 7 | -bird(t) (1, 0, 0, 0) |
| `rule_vs_certain_fact.gkp` | 7 | p (.64, .04, .16, .16); r the same; gk with the reading `cycle cut` |
| `chain_vs_certain_fact.gkp` | 7 | q (.64, .04, .16, .16); r and p the same; gk with the reading `cycle cut` |
| `same_atom.gkp` | 8 | p (0, 0, 0, 1) |
| `tiny_clue.gkp` | 8 | flies(t) (.6001, 0, .3, .0999) |
| `mixed_kinds.gkp` | 8 | flies(t) (.65, 0, .3, .05) |
| `absent_route.gkp` | 8 | flies(t) (.63, .3, 0, .07) |
| `positive_loop.gkp` | 9 | b (.5, 0, 0, .5) |
| `mutual_block.gkp` | 9 | p(a) (0, 0, 0, 1); gk with the reading `cycle cut` |
| `mutual_block_half.gkp` | 9 | p(a) (.25, 0, 0, .75); gk with the reading `cycle cut` |
| `exception_cycle.gkp` | 9 | p (0, 0, 0, 1); **gk (1, 0, 0, 0)** with the reading `cycle cut` |
| `yale.gkp` | 9 | alive(s2) unresolved in every world; **gk (0, 1, 0, 0)** with the reading `cycle cut` |
| `yale_walks.gkp` | 9 | walks(s2) unresolved in every world; **gk (0, 0, 0, 1)** with the reading `cycle cut` |
| `combined.js` | 10.1 | flies(t) (.45, 0, 0, .55); flies(p) (0, 1, 0, 0); gk with the reading `cycle cut` |
| `tweety_1_exception.gkp` | 10.2 | flies(tweety) (.396, .56, 0, .044) |
| `tweety_2_disjunction.gkp` | 10.2 | flies(tweety) (.396, .56, 0, .044) |
| `tweety_3a_gull_rule.gkp` | 10.2 | flies(tweety) (.6984, .224, 0, .0776) |
| `tweety_3b_certain_gull_rule.gkp` | 10.2 | flies(tweety) (.6984, .224, 0, .0776); gk with two `cycle cut` readings |
| `tweety_4_lineage.gkp` | 10.2 | flies(tweety) (.396, .56, 0, .044) from gk, four searches cut by the budget; the reference tool declines function symbols |
| `bird_uncertain.gkp` | 13 | bird(t) (0, .2, .8, 0); gk with the reading `cycle cut` |
| `bird_uncertain_sings.gkp` | 13 | sings(t) (1, 0, 0, 0) |

The values are the values of the semantics, computed by hand. On
2026-11-09 gk 1.2.3 gave them exactly on every input except the three in
bold, where gk's cycle cut departs from the semantics. The reference tool
mcref 1.1.1 gave them within its sampling error (at most ±.0113 per share
at 20,000 samples, seed 1) on every input it accepts.
