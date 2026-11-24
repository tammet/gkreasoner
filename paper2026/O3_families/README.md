# O3: the benchmark families, and the table of limits

This part holds the benchmark families: Bayesian networks, a university knowledge base, delivery plans,
equipment with equality, Smokers, grids, chains and trees of defaults, cascades, cyclic inputs and five cases of
the comparison table. gk 1.3.2 answers each input under the default, the general method and the exact method, at
the time limit of 10 s. Each input has a target, whose kind `results.csv` names. The part also holds the table
of limits in both directions, which reads the results of this part and of parts O1, O14, O15 and O20.

## Where the inputs come from

| family | source |
|---|---|
| `bn` | five networks of the bnlearn Bayesian network repository (Asia, Cancer, Earthquake, Win95pts, Andes), converted to gk input; the network files are not included, `inputs/bn/` and `inputs/tools/` name them |
| `university` | a LUBM-style university base: the vocabulary and rules of the Univ-Bench ontology of the Lehigh University Benchmark, with generated facts |
| `smokers` | the Smokers example of Markov logic and ProbLog |
| `grids` | paths in grids of uncertain edges |
| `delivery`, `equipment` | written for this paper: delivery plans with function terms, equipment with equality |
| `chains_trees`, `cascades`, `cyclic` | written for this paper: chains and trees of defaults, cascades of priorities, rings, random programs and argumentation frameworks |
| `comparison` | five cases of the comparison table of part O5 (their inputs are in `../O5_comparisons/inputs/gk/`) |

The folders under `inputs/` also hold the encodings of the other systems that the earlier comparison ran
(ProbLog programs, SPINdle and DEFT theories) and the scripts that computed targets (`inputs/tools/`).

## Rerun

From the folder `paper2026/`:

```sh
cd O3_families/inputs/grids && $GK gk_corner16.gkp
```

The first line holds `"value":[0.617081,0,0,0.382919]`, answered by the exact method and complete; the target
is .6171 (40441/65536).

To rerun every gk and tool run of this part and compare each value with `results.csv`:

```sh
python3 check_gk.py --part O3_families --gk PATH/TO/gk --mcref PATH/TO/mcref.py
```

Its last line names the values compared and how many differ. Every value is expected to be equal, except that
a value can change from run to run when the recorded run did not end by itself or the rerun reports cut or
queued searches; the check reports such a difference apart. The runs and values that it compares:

<!-- table check -->
| gk runs | tool runs | runs with a recorded value | values compared | of these, on runs that did not end by themselves |
|---|---|---|---|---|
| 418 | 0 | 391 | 406 | 117 |
<!-- end table -->

`$GK` stands for the gk binary and `$MCREF` for the tool's `mcref.py`. Every command of `runs.tsv` runs
in the folder that its column `cwd` names, relative to this folder's parent (`paper2026/`).

## Results

The families, with the target of each input. "Meets" means within half a unit of the target's last printed
decimal, or within the tool's bound where the tool gives the target.

<!-- table families -->
| family | inputs | kind of target | the default meets the target (answered by) | the general method meets | the exact method meets / complete |
|---|---|---|---|---|---|
| bn | 13 | answer of pgmpy 1.1.2 (variable elimination on the network); calculated | 12 (exact 12, general 0) | 9 | 12 / 9 |
| university | 12 | calculated | 12 (exact 12, general 0) | 12 | 12 / 12 |
| delivery | 21 | calculated | 21 (exact 4, general 17) | 21 | 21 / 17 |
| equipment | 13 | calculated | 9 (exact 0, general 9) | 9 | 0 / 0 |
| smokers | 3 | answer of ProbLog 2.3.0 (the recorded run of the earlier folder) | 0 (exact 0, general 0) | 0 | 0 / 0 |
| grids | 8 | answer of ProbLog 2.3.0 (the recorded run of the earlier folder); calculated | 8 (exact 8, general 0) | 1 | 8 / 8 |
| chains_trees | 3 | calculated | 3 (exact 3, general 0) | 0 | 3 / 3 |
| cascades | 2 | calculated | 2 (exact 2, general 0) | 0 | 2 / 2 |
| cyclic | 26 | calculated; exact value of the tool; sampled value of the tool, bound 0.005037 | 23 (exact 18, general 5) | 23 | 18 / 17 |
| comparison | 5 | answer of ProbLog 2.2.10 (the recorded run of the earlier comparison) | 5 (exact 4, general 1) | 5 | 5 / 5 |
<!-- end table -->

### The table of limits, in both directions

All rows are runs at the time limit of 10 s. "Right" means equal to the target of the input. A time is given
only for runs that ended by themselves; a range is over those runs.

**A. The exact method answers; the general method does not.**

<!-- table limits_a -->
| inputs | the exact method | the general method | the default |
|---|---|---|---|
| 8 grids with a target (ProbLog) | 8 of 8 right, 8 complete, .05 to 4.12 s | 1 of 8 right, 0 ended by themselves | 8 of 8 right; answered by the exact method 8, by the general method 0 |
| a chain of 1,000 defaults; trees of 364 and 2,047 nodes | 3 of 3 right, 3 complete, .07 to .12 s | 0 of 3 right, 3 ended by themselves (1.83 to 1.88 s) | 3 of 3 right; answered by the exact method 3, by the general method 0 |
| the route with contrary reports, 5 to 200 links (part O14) | 6 of 6 right, 6 complete, .06 to .1 s | 1 of 6 right, 6 ended by themselves (1.88 to 2.82 s) | not run |
<!-- end table -->

**B. The exact method gives no complete answer.**

<!-- table limits_b -->
| inputs | the exact method | the general method | the default |
|---|---|---|---|
| the university base plus one certain contradiction about a new individual, variant (a) (part O15) | 5 of 8 right, 0 complete | 8 of 8 right, 6 ended by themselves (.3 to 1.73 s) | 8 of 8 right; answered by the exact method 0, by the general method 8 |
| delivery plans of 16 and 32 legs, function terms | 4 of 4 right, 0 complete | 4 of 4 right, 0 ended by themselves | 4 of 4 right; answered by the exact method 0, by the general method 4 |
| the Tweety lineage, function terms (part O1) | 3 of 3 right, 0 complete | 3 of 3 right, 0 ended by themselves | 3 of 3 right; answered by the exact method 0, by the general method 3 |
| equipment with equality | 0 of 13 right, 0 complete, 13 not covered | 9 of 13 right, 13 ended by themselves (.65 to 5.87 s) | 9 of 13 right; answered by the exact method 0, by the general method 13 |
| Smokers with 5, 8 and 12 persons | 0 of 3 right, 0 complete, no value on 3 | 0 of 3 right, 3 ended by themselves (2.34 to 6.31 s) | 0 of 3 right; answered by the exact method 0, by the general method 3 |
| 4 deep queries on large Bayesian networks | 3 of 4 right, 0 complete, no value on 1 | 0 of 4 right, 0 ended by themselves | 3 of 4 right; answered by the exact method 3, by the general method 1 |
| cyclic inputs: the ring of 30, the program of 40, argumentation frameworks of 20 and 40 arguments | 1 of 9 right, 0 complete, no value on 8 | 6 of 9 right, 1 ended by themselves (4.85 s) | 6 of 9 right; answered by the exact method 1, by the general method 8 |
| the route with certain rules and a default, 5, 10 and 20 links (part O14) | 2 of 3 right, 0 complete | 2 of 3 right, 2 ended by themselves (1.95 to 2.78 s) | not run |
| the exact method outside both classes, 24 inputs (part O20) | 4 of 24 right, 2 complete, .15 to .38 s | 24 of 24 right, 22 ended by themselves (.39 to 4.27 s) | 24 of 24 right; answered by the exact method 2, by the general method 22 |
<!-- end table -->

**C. The verdict can depend on the time limit** (part O6): "Does John eat berries?"

<!-- table limits_c -->
| limit | method | value | answered by | ended by itself |
|---|---|---|---|---|
| 10 s | default | (.98, 0, 0, .02) | general | no |
| 10 s | general | (.98, 0, 0, .02) | general | no |
| 60 s | default | (0, .98, 0, .02) | general | no |
| 60 s | general | (0, .98, 0, .02) | general | no |
<!-- end table -->

### ProbLog on the twelve university queries

<!-- table problog -->
| input | question | gk 1.3.2, the default | ProbLog 2.3.0 | ProbLog's time |
|---|---|---|---|---|
| gk_dept1_scale0.25_employee.gkp | employee(full1_d0) | (.997644, 0, 0, .002356), complete, by the exact method, 0.06 s | 0.99764394 | 0.11 s |
| gk_dept1_scale0.25_memberOf.gkp | memberOf(full1_d0,dept0) | (.49, 0, 0, .51), complete, by the exact method, 0.06 s | 0.49 | 0.10 s |
| gk_dept1_scale0.25_organization.gkp | organization(dept0) | (1, 0, 0, 0), complete, by the exact method, 0.06 s | 1.0 | 0.13 s |
| gk_dept1_scale0.25_person.gkp | person(grad9_d0) | (.983935, 0, 0, .016065), complete, by the exact method, 0.06 s | 0.983935 | 0.11 s |
| gk_dept1_scale1_employee.gkp | employee(full1_d0) | (.999414, 0, 0, .000586), complete, by the exact method, 0.11 s | 0.9994135 | 0.17 s |
| gk_dept1_scale1_memberOf.gkp | memberOf(full1_d0,dept0) | (.49, 0, 0, .51), complete, by the exact method, 0.11 s | 0.49 | 0.16 s |
| gk_dept1_scale1_organization.gkp | organization(dept0) | (1, 0, 0, 0), complete, by the exact method, 0.11 s | 1.0 | 0.39 s |
| gk_dept1_scale1_person.gkp | person(grad39_d0) | (.963204, 0, 0, .036796), complete, by the exact method, 0.10 s | 0.96320384 | 0.17 s |
| gk_dept3_scale1_employee.gkp | employee(full1_d0) | (.999781, 0, 0, .000219), complete, by the exact method, 0.48 s | 0.99978095 | 0.31 s |
| gk_dept3_scale1_memberOf.gkp | memberOf(full1_d0,dept0) | (.36, 0, 0, .64), complete, by the exact method, 0.43 s | 0.36 | 0.31 s |
| gk_dept3_scale1_organization.gkp | organization(dept0) | (1, 0, 0, 0), complete, by the exact method, 0.46 s | 1.0 | 0.54 s |
| gk_dept3_scale1_person.gkp | person(grad39_d0) | (.966422, 0, 0, .033578), complete, by the exact method, 0.45 s | 0.96642184 | 0.32 s |
<!-- end table -->

### The fixed strategies of the general method

<!-- table strategies -->
| input | strategy | value | target | against the target | ended by itself |
|---|---|---|---|---|---|
| bn/gk_andes_snode_151.gkp | hyper | (.4501, 0, 0, .5499) | (.7955, 0, 0, .2045) | another value | no |
| bn/gk_andes_snode_151.gkp | query_focus | (.6301, 0, 0, .3699) | (.7955, 0, 0, .2045) | another value | no |
| bn/gk_andes_snode_74.gkp | hyper | (.2829, 0, 0, .7171) | (.8971, 0, 0, .1029) | another value | no |
| bn/gk_andes_snode_74.gkp | query_focus | (.5723, 0, 0, .4277) | (.8971, 0, 0, .1029) | another value | no |
| bn/gk_win95pts_pc2prt.gkp | hyper | (.3451, 0, 0, .6549) | (.7766, 0, 0, .2234) | another value | no |
| bn/gk_win95pts_pc2prt.gkp | query_focus | (.005, 0, 0, .995) | (.7766, 0, 0, .2234) | another value | no |
| bn/gk_win95pts_problem1.gkp | hyper | (.7195, 0, 0, .2805) | (.5726, 0, 0, .4274) | another value | no |
| bn/gk_win95pts_problem1.gkp | query_focus | (.6953, 0, 0, .3047) | (.5726, 0, 0, .4274) | another value | no |
| cascades/gk_cascade200_equal.gkp | hyper | (1, 0, 0, 0) | (1, 0, 0, 0) | meets the target | no |
| cascades/gk_cascade200_equal.gkp | query_focus | (0, 0, 0, 1) | (1, 0, 0, 0) | another value | no |
| cascades/gk_cascade200_priorities.gkp | hyper | (0, 1, 0, 0) | (1, 0, 0, 0) | another value | no |
| cascades/gk_cascade200_priorities.gkp | query_focus | (0, 1, 0, 0) | (1, 0, 0, 0) | another value | no |
| chains_trees/gk_chain1000.gkp | query_focus | (0, 0, 0, 1) | (1, 0, 0, 0) | another value | no |
| chains_trees/gk_tree2047.gkp | query_focus | (0, 0, 0, 1) | (1, 0, 0, 0) | another value | no |
| chains_trees/gk_tree364.gkp | query_focus | (1, 0, 0, 0) | (1, 0, 0, 0) | meets the target | no |
| cyclic/gk_af10_in_x3.gkp | query_focus | (1, 0, 0, 0) | (1, 0, 0, 0) | meets the target | no |
| cyclic/gk_af10_out_x0.gkp | query_focus | (0, 0, 0, 1) | (0, 0, 0, 1) | meets the target | no |
| cyclic/gk_af10_undec_x6.gkp | query_focus | (0, 0, 0, 1) | (0, 0, 0, 1) | meets the target | no |
| cyclic/gk_af10_undec_x6_att.gkp | query_focus | (0, 0, 0, 1) | (0, 0, 0, 1) | meets the target | no |
| cyclic/gk_af20_undec_x0.gkp | query_focus | (1, 0, 0, 0) | (0, 0, 0, 1) | another value | no |
| cyclic/gk_af20_undec_x0_att.gkp | query_focus | (0, 0, 0, 1) | (0, 0, 0, 1) | meets the target | no |
| cyclic/gk_af40_in_x12.gkp | query_focus | (1, 0, 0, 0) | (1, 0, 0, 0) | meets the target | no |
| cyclic/gk_af40_out_x9.gkp | query_focus | (0, 0, 0, 1) | (0, 0, 0, 1) | meets the target | no |
| cyclic/gk_af40_out_x9_att.gkp | query_focus | (1, 0, 0, 0) | (1, 0, 0, 0) | meets the target | no |
| cyclic/gk_af40_undec_x0.gkp | query_focus | (0, 0, 0, 1) | (0, 0, 0, 1) | meets the target | no |
| cyclic/gk_af40_undec_x0_att.gkp | query_focus | (1, 0, 0, 0) | (0, 0, 0, 1) | another value | no |
| cyclic/gk_af6_in_x2.gkp | query_focus | (1, 0, 0, 0) | (1, 0, 0, 0) | meets the target | yes |
| cyclic/gk_af6_out_x0.gkp | query_focus | (0, 0, 0, 1) | (0, 0, 0, 1) | meets the target | yes |
| cyclic/gk_af6_undec_x1.gkp | query_focus | (1, 0, 0, 0) | (1, 0, 0, 0) | meets the target | yes |
| delivery/gk_background10.gkp | hyper | (.4655, 0, 0, .5345) | (.4655, 0, 0, .5345) | meets the target | yes |
| delivery/gk_background10.gkp | query_focus_equality | (.4655, 0, 0, .5345) | (.4655, 0, 0, .5345) | meets the target | yes |
| delivery/gk_background200.gkp | hyper | (.4655, 0, 0, .5345) | (.4655, 0, 0, .5345) | meets the target | yes |
| delivery/gk_background200.gkp | query_focus_equality | (.4655, 0, 0, .5345) | (.4655, 0, 0, .5345) | meets the target | yes |
| delivery/gk_background50.gkp | hyper | (.4655, 0, 0, .5345) | (.4655, 0, 0, .5345) | meets the target | yes |
| delivery/gk_background50.gkp | query_focus_equality | (.4655, 0, 0, .5345) | (.4655, 0, 0, .5345) | meets the target | yes |
| delivery/gk_exception_chain1.gkp | hyper | (.4655, 0, 0, .5345) | (.4655, 0, 0, .5345) | meets the target | yes |
| delivery/gk_exception_chain1.gkp | query_focus_equality | (.4655, 0, 0, .5345) | (.4655, 0, 0, .5345) | meets the target | yes |
| delivery/gk_exception_chain20.gkp | hyper | (.4655, 0, 0, .5345) | (.4655, 0, 0, .5345) | meets the target | yes |
| delivery/gk_exception_chain20.gkp | query_focus_equality | (.4655, 0, 0, .5345) | (.4655, 0, 0, .5345) | meets the target | yes |
| delivery/gk_exception_chain5.gkp | hyper | (.4655, 0, 0, .5345) | (.4655, 0, 0, .5345) | meets the target | yes |
| delivery/gk_exception_chain5.gkp | query_focus_equality | (.4655, 0, 0, .5345) | (.4655, 0, 0, .5345) | meets the target | yes |
| delivery/gk_exception_chain50.gkp | hyper | (.4655, 0, 0, .5345) | (.4655, 0, 0, .5345) | meets the target | yes |
| delivery/gk_exception_chain50.gkp | query_focus_equality | (.4655, 0, 0, .5345) | (.4655, 0, 0, .5345) | meets the target | yes |
| delivery/gk_legs16_control.gkp | hyper | (0, 0, 0, 1) | (.1584, 0, 0, .8416) | another value | no |
| delivery/gk_legs16_control.gkp | query_focus_equality | (.1584, 0, 0, .8416) | (.1584, 0, 0, .8416) | meets the target | yes |
| delivery/gk_legs16_opposed.gkp | hyper | (0, 0, 0, 1) | (.1232, 0, 0, .8768) | another value | no |
| delivery/gk_legs16_opposed.gkp | query_focus_equality | (.1232, 0, 0, .8768) | (.1232, 0, 0, .8768) | meets the target | yes |
| delivery/gk_legs2_control.gkp | hyper | (.6925, 0, 0, .3075) | (.6926, 0, 0, .3074) | meets the target | yes |
| delivery/gk_legs2_control.gkp | query_focus_equality | (.6925, 0, 0, .3075) | (.6926, 0, 0, .3074) | meets the target | yes |
| delivery/gk_legs2_control_flat.gkp | hyper | (.6925, 0, 0, .3075) | (.6926, 0, 0, .3074) | meets the target | no |
| delivery/gk_legs2_control_flat.gkp | query_focus_equality | (.6925, 0, 0, .3075) | (.6926, 0, 0, .3074) | meets the target | yes |
| delivery/gk_legs2_opposed.gkp | hyper | (.5386, 0, 0, .4613) | (.5387, 0, 0, .4613) | meets the target | yes |
| delivery/gk_legs2_opposed.gkp | query_focus_equality | (.5386, 0, 0, .4613) | (.5387, 0, 0, .4613) | meets the target | yes |
| delivery/gk_legs2_opposed_flat.gkp | hyper | (.5386, 0, 0, .4613) | (.5387, 0, 0, .4613) | meets the target | no |
| delivery/gk_legs2_opposed_flat.gkp | query_focus_equality | (.5386, 0, 0, .4613) | (.5387, 0, 0, .4613) | meets the target | yes |
| delivery/gk_legs32_control.gkp | hyper | (0, 0, 0, 1) | (.0294, 0, 0, .9706) | another value | no |
| delivery/gk_legs32_control.gkp | query_focus_equality | (.0294, 0, 0, .9706) | (.0294, 0, 0, .9706) | meets the target | yes |
| delivery/gk_legs32_opposed.gkp | hyper | (0, 0, 0, 1) | (.0228, 0, 0, .9772) | another value | no |
| delivery/gk_legs32_opposed.gkp | query_focus_equality | (.0228, 0, 0, .9772) | (.0228, 0, 0, .9772) | meets the target | yes |
| delivery/gk_legs4_control.gkp | hyper | (.561, 0, 0, .439) | (.561, 0, 0, .439) | meets the target | yes |
| delivery/gk_legs4_control.gkp | query_focus_equality | (.561, 0, 0, .439) | (.561, 0, 0, .439) | meets the target | yes |
| delivery/gk_legs4_control_flat.gkp | hyper | (.7695, 0, 0, .2305) | (.561, 0, 0, .439) | another value | no |
| delivery/gk_legs4_control_flat.gkp | query_focus_equality | (.561, 0, 0, .439) | (.561, 0, 0, .439) | meets the target | yes |
| delivery/gk_legs4_opposed.gkp | hyper | (.4363, 0, 0, .5637) | (.4363, 0, 0, .5637) | meets the target | yes |
| delivery/gk_legs4_opposed.gkp | query_focus_equality | (.4363, 0, 0, .5637) | (.4363, 0, 0, .5637) | meets the target | yes |
| delivery/gk_legs4_opposed_flat.gkp | hyper | (.7695, 0, 0, .2305) | (.4363, 0, 0, .5637) | another value | no |
| delivery/gk_legs4_opposed_flat.gkp | query_focus_equality | (.4363, 0, 0, .5637) | (.4363, 0, 0, .5637) | meets the target | yes |
| delivery/gk_legs8_control.gkp | hyper | (.368, 0, 0, .632) | (.368, 0, 0, .632) | meets the target | no |
| delivery/gk_legs8_control.gkp | query_focus_equality | (.368, 0, 0, .632) | (.368, 0, 0, .632) | meets the target | yes |
| delivery/gk_legs8_opposed.gkp | hyper | (.2863, 0, 0, .7137) | (.2863, 0, 0, .7137) | meets the target | no |
| delivery/gk_legs8_opposed.gkp | query_focus_equality | (.2863, 0, 0, .7137) | (.2863, 0, 0, .7137) | meets the target | yes |
| equipment/gk_background10.gkp | query_focus_equality | (.5508, 0, 0, .4492) | (.5508, 0, 0, .4492) | meets the target | yes |
| equipment/gk_background200.gkp | query_focus_equality | (.5508, 0, 0, .4492) | (.5508, 0, 0, .4492) | meets the target | yes |
| equipment/gk_background50.gkp | query_focus_equality | (.5508, 0, 0, .4492) | (.5508, 0, 0, .4492) | meets the target | yes |
| equipment/gk_components16.gkp | query_focus_equality | (.1021, 0, 0, .8979) | (.1021, 0, 0, .8979) | meets the target | no |
| equipment/gk_components2.gkp | query_focus_equality | (.4461, 0, 0, .5539) | (.4461, 0, 0, .5539) | meets the target | yes |
| equipment/gk_components4.gkp | query_focus_equality | (.3614, 0, 0, .6386) | (.3614, 0, 0, .6386) | meets the target | yes |
| equipment/gk_components8.gkp | query_focus_equality | (.2371, 0, 0, .7629) | (.2371, 0, 0, .7629) | meets the target | no |
| equipment/gk_equality_chain1.gkp | query_focus_equality | (.5508, 0, 0, .4492) | (.5508, 0, 0, .4492) | meets the target | yes |
| equipment/gk_equality_chain10.gkp | query_focus_equality | (.5508, 0, 0, .4492) | (.5508, 0, 0, .4492) | meets the target | no |
| equipment/gk_equality_chain20.gkp | query_focus_equality | (.5508, 0, 0, .4492) | (.5508, 0, 0, .4492) | meets the target | no |
| equipment/gk_equality_chain3.gkp | query_focus_equality | (.5508, 0, 0, .4492) | (.5508, 0, 0, .4492) | meets the target | yes |
| equipment/gk_equality_chain6.gkp | query_focus_equality | (.5508, 0, 0, .4492) | (.5508, 0, 0, .4492) | meets the target | yes |
| equipment/gk_second_supply.gkp | query_focus_equality | (.3966, 0, 0, .6034) | (.3966, 0, 0, .6034) | meets the target | yes |
| grids/gk_corner16.gkp | hyper | (.6171, 0, 0, .3829) | (.6171, 0, 0, .3829) | meets the target | no |
| grids/gk_corner33.gkp | hyper | (.5233, 0, 0, .4767) | (.5652, 0, 0, .4348) | another value | no |
| grids/gk_corner56.gkp | hyper | (.2339, 0, 0, .7661) | (.5323, 0, 0, .4677) | another value | no |
| grids/gk_full_d2.gkp | hyper | (.6171, 0, 0, .3829) | (.6171, 0, 0, .3829) | meets the target | no |
| grids/gk_full_d3.gkp | hyper | (.4844, 0, 0, .5156) | (.5652, 0, 0, .4348) | another value | no |
| grids/gk_full_d4.gkp | hyper | (.1346, 0, 0, .8654) | (.5323, 0, 0, .4677) | another value | no |
| grids/gk_full_d5.gkp | hyper | (.0707, 0, 0, .9293) | (.5089, 0, 0, .4911) | another value | no |
| smokers/gk_smokers12.gkp | hyper | (.5733, 0, 0, .4267) | (.6475, 0, 0, .3525) | another value | no |
| smokers/gk_smokers5.gkp | hyper | (.4535, 0, 0, .5465) | (.4796, 0, 0, .5204) | another value | no |
| smokers/gk_smokers8.gkp | hyper | (.5461, 0, 0, .4539) | (.5904, 0, 0, .4096) | another value | no |
<!-- end table -->

## Where the paper's numbers are

- The table of the three methods (Section 7.6): the tables above; each cell counts rows of `results.csv` of the part
  that the row names, columns `class`, `complete`, `answered_by`, `ended_by_itself` and `time_s`.
- The university queries against ProbLog: the rows with `system` ProbLog 2.3.0, columns `value` and `time_s`,
  and the default's rows of the same input.
- The Bayesian networks, 12 of 13 queries: the rows of `family` bn, `method` default, column `class`.
- The two sentences on the fixed strategies: the rows with a `strategy`.

`results.csv` has one row per run and answer. The columns are described on the first page of the
folder ([`../README.md`](../README.md), section "The tables of a part").
