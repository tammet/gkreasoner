# Examples/semantics

The runnable inputs of [`../../Doc/support_semantics.md`](../../Doc/support_semantics.md),
in the order of that page. Run one from the repository root:

```sh
./bin/gk Examples/semantics/penguin.gkp            # the default choice
./bin/gk -exact Examples/semantics/penguin.gkp     # the exact method
./bin/gk -general Examples/semantics/penguin.gkp   # the general method
python3 mcref/mcref.py Examples/semantics/penguin.gkp
```

The last command runs the reference tool [`mcref`](../../mcref/README.md),
by exact evaluation by default.

| file | section | answer (for, against, conflict, ignorance) |
|---|---|---|
| `uncertain_fact.gkp` | 1 | flies(t) (.72, 0, 0, .28) |
| `certain.gkp` | 1 | flies(t) (1, 0, 0, 0) |
| `equal_reports.gkp` | 1 | flies(a) (0, 0, 0, 1); bird(a) (0, 0, .5, .5) |
| `against_same_atom.gkp` | 1, 5.2 | flies(a) (.3, 0, .4, .3) |
| `uncertain_rule_direction.gkp` | 2.1 | bird(a) (1, 0, 0, 0); flies(a) (0, .1, .9, 0) |
| `headless_default.gkp` | 2.1 | bird(a) (0, 0, 1, 0) |
| `head_from_default.gkp` | 2.1 | bird(os) (0, 0, 0, 1) |
| `classical_first.gkp` | 2.2 | flies(a) (0, 1, 0, 0); penguin(a) (1, 0, 0, 0) |
| `unblocked_vs_fact.gkp` | 2.2 | flies(a) (0, 0, 1, 0) |
| `unused_exception.gkp` | 2.3 | p (.7, 0, 0, .3) |
| `conflict_premise.gkp` | 2.4 | q (0, 0, 0, 1); p (0, 0, 1, 0) |
| `disjunction.gkp` | 3.1 | injured(t) (.6, 0, 0, .4) |
| `disjunction_certain.gkp` | 3.1 | injured(t) (1, 0, 0, 0) |
| `self_blocking_rule.gkp` | 3.1 | r (0, 0, 0, 1) |
| `proof_by_cases.gkp` | 3.3 | q (1, 0, 0, 0) |
| `rule_identities.gkp` | 3.3 | q (.72, 0, 0, .28) |
| `cases_unknown.gkp` | 3.3 | q (.42, 0, 0, .58) |
| `premise_by_cases.gkp` | 3.3 | q (.81, 0, 0, .19) |
| `two_routes.gkp` | 4 | r(c) (.8, 0, 0, .2) |
| `shared_evidence.gkp` | 4 | q (.5, 0, 0, .5) |
| `instances.gkp` | 4 | q (.81, 0, 0, .19) |
| `external_exception.gkp` | 4 | flies(t) (.45, 0, 0, .55) |
| `contested_premise.gkp` | 5.2 | flies(a) (.18, 0, 0, .82) |
| `contested_premise_bird.gkp` | 5.2 | bird(a) (.2, 0, .3, .5) |
| `contradicted_clause.gkp` | 5.3 | q (0, 0, 0, 1) |
| `clause_in_part.gkp` | 5.3 | q (.7416, 0, 0, .2584) |
| `default_vs_fact.gkp` | 5.4 | flies(t) (.63, .3, 0, .07) |
| `rule_vs_fact.gkp` | 5.4 | flies(t) (.6, 0, .3, .1) |
| `penguin.gkp` | 5.4 | flies(t) (.9, 0, 0, .1); flies(p) (0, 1, 0, 0) |
| `nixon.gkp` | 5.4 | pacifist(n) (0, 0, 0, 1) |
| `nixon_uncertain.gkp` | 5.4 | pacifist(n) (.32, .12, 0, .56) |
| `nixon_ranks.gkp` | 5.4 | pacifist(n) (1, 0, 0, 0) |
| `tiny_clue.gkp` | 5.5 | flies(t) (.6001, 0, .3, .0999) |
| `mixed_kinds.gkp` | 5.5 | flies(t) (.65, 0, .3, .05) |
| `absent_route.gkp` | 5.5 | flies(t) (.63, .3, 0, .07) |
| `default_by_cases.gkp` | 5.5 | q (.7, .3, 0, 0) |
| `uncertain_defaults_cases.gkp` | 5.5 | flies (.64, 0, 0, .36) |
| `exception_variable.gkp` | 5.6 | q(a) (.225, 0, 0, .775) |
| `plain_penguin.gkp` | 5.6 | flies(a) (0, 1, 0, 0) |
| `two_layers.gkp` | 5.6 | flies(a) (0, 1, 0, 0) |
| `restored_rule.gkp` | 5.6 | p (1, 0, 0, 0); e (0, 0, 1, 0) |
| `blocked_rule.gkp` | 5.6 | c (1, 0, 0, 0) |
| `self_support.gkp` | 5.7 | a (.4, .2, 0, .4); b (.4, 0, 0, .6) |
| `withdrawn_support_default.gkp` | 5.7 | b (.4, 0, 0, .6) |
| `contraposition.gkp` | 6 | -bird(t) (1, 0, 0, 0) |
| `modular.gkp` | 6 | r (0, 0, 1, 0); p and q (1, 0, 0, 0) |
| `rule_vs_certain_fact.gkp` | 6, 7.2 | p (.64, .04, .16, .16); r the same |
| `chain_vs_certain_fact.gkp` | 6 | q (.64, .04, .16, .16); r and p the same |
| `bird_uncertain.gkp` | 6 | bird(t) (0, .2, .8, 0) |
| `bird_uncertain_sings.gkp` | 6 | sings(t) (1, 0, 0, 0) |
| `positive_loop.gkp` | 7.1 | b (.5, 0, 0, .5) |
| `mutual_block.gkp` | 7.2 | p(a) (0, 0, 0, 1) |
| `mutual_block_half.gkp` | 7.2 | p(a) (.25, 0, 0, .75) |
| `exception_cycle.gkp` | 7.2 | p (0, 0, 0, 1) |
| `same_atom.gkp` | 7.2 | p (0, 0, 0, 1) |
| `withdrawn_support.gkp` | 7.2 | p (0, 0, 0, 1) |
| `no_value.gkp` | 7.3 | on(a) no value in every world |
| `yale.gkp` | 7.3 | alive(s2) no value in every world |
| `yale_walks.gkp` | 7.3 | walks(s2) no value in every world |
| `clause_rule.gkp` | 7.4 | q (0, 0, 0, 1) |
| `clause_rule_no_result.gkp` | 7.4 | q (.13851, 0, 0, .271), no value .59049 |
| `undefined_in_wfm.gkp` | 7.6 | g (1, 0, 0, 0) |
| `function_limit.gkp` | 8 | p(a) (.666667, 0, 0, .333333) from the general method |
| `function_alternating.gkp` | 8 | p(a) (1, 0, 0, 0) from the general method |
| `jump_at_one.gkp` | 8 | e (0, 0, 0, 1) |
| `jump_below_one.gkp` | 8 | e (0, 0, .99, .01) |
| `tweety_1_exception.gkp` | 9.1 | flies(tweety) (.396, .56, 0, .044) |
| `tweety_2_disjunction.gkp` | 9.1 | flies(tweety) (.396, .56, 0, .044) |
| `tweety_3a_gull_rule.gkp` | 9.1 | flies(tweety) (.6984, .224, 0, .0776) |
| `tweety_3b_certain_gull_rule.gkp` | 9.1 | flies(tweety) (.6984, .224, 0, .0776) |
| `tweety_4_lineage.gkp` | 9.1 | flies(tweety) (.396, .56, 0, .044) from the general method |
| `tweety_4b_lineage_gull_rule.gkp` | 9.1 | flies(tweety) (.6984, .224, 0, .0776) from the general method |
| `combined.js` | 9.2 | flies(t) (.45, 0, 0, .55); flies(p) (0, 1, 0, 0) |

The values are the values of the semantics. The reference tool `mcref`
1.3.0 computed them by exact evaluation. gk 1.3.1 gives the same values
under the default choice, the exact method and the general method, and
the exact method marks each of these answers complete. The tool declines
the four inputs with function terms (`function_limit.gkp`,
`function_alternating.gkp`, `tweety_4_lineage.gkp`,
`tweety_4b_lineage_gull_rule.gkp`). Their values are those of gk's general
method at its default deadline. On the two lineage inputs the general
method stops four lineage searches; `Doc/support_semantics.md` Section 9.1
says why these searches cannot change the value.
