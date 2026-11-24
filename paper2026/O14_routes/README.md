# O14: the routes, and the search without grounding

This part holds four families of route queries and the counts that show how much of a full grounding the exact
method forms. A route has K uncertain links from n0 to nK and reach rules; the question asks about the end of
the route. gk 1.3.2 answers each route under the exact method, the exact method with a full grounding first
(`-exact -ground-first`) and the general method. ProbLog computes the same routes, and clingo's grounder writes
the ground instances of the recursive rule. The part also counts the ground statements on the university base
and the grids of part O3.

| family | links | rules | question |
|---|---|---|---|
| `route_c1b` | .99 each | uncertain reach rules; a default `0.8::open(X) :- reach(n0,X), unless(closed(X))` and `0.5::closed(nK)` | `open(nK)` |
| `rt_c2` | .9 each | certain reach rules, no default | `reach(n0,nK)` |
| `rt_mix` | .9 each | certain reach rules and the default | `open(nK)` |
| `route_opp` | as `route_c1b` | plus a contrary report `0.3::-link(ni,ni+1)` against every tenth link | `open(nK)` |

## Where the inputs come from

The routes were constructed for the paper. `make_routes.py` writes every route input and the ProbLog and clingo
files; `python3 make_routes.py --check` compares them with `inputs/`. The calculated values: `route_c1b`
.99^(2K) x .4; `rt_c2` .9^K; `rt_mix` .9^K x .4; `route_opp` .99^(K-m) x .69^m x .99^K x .4 with m contrary
reports. The tool checked the formula of `route_opp` at 5 links (exactly) and 10 links (by sampling).

## Rerun

From the folder `paper2026/`:

```sh
cd O14_routes/inputs && $GK route_opp_20.gkp -exact
```

The first line holds `"value":[0.129986,0,0,0.870014]`, complete, and `"class":1` in `complete_mode`: the exact
method matched rule bodies against facts.

To rerun every gk and tool run of this part and compare each value with `results.csv`:

```sh
python3 check_gk.py --part O14_routes --gk PATH/TO/gk --mcref PATH/TO/mcref.py
```

Its last line names the values compared and how many differ. Every value is expected to be equal, except that
a value can change from run to run when the recorded run did not end by itself or the rerun reports cut or
queued searches; the check reports such a difference apart. The runs and values that it compares:

<!-- table check -->
| gk runs | tool runs | runs with a recorded value | values compared | of these, on runs that did not end by themselves |
|---|---|---|---|---|
| 130 | 2 | 105 | 105 | 33 |
<!-- end table -->

`$GK` stands for the gk binary and `$MCREF` for the tool's `mcref.py`. Every command of `runs.tsv` runs
in the folder that its column `cwd` names, relative to this folder's parent (`paper2026/`).

## Results

The route families under the three ways of running gk:

<!-- table routes -->
| family | links | calculated value | the exact method | the exact method, ground first | the general method |
|---|---|---|---|---|---|
| route_c1b | 5 | (.361753, 0, 0, .638247) | (.361753, 0, 0, .638247), complete, 0.05 s, equal to the calculated value | (.361753, 0, 0, .638247), complete, 0.06 s, equal to the calculated value | (.361753, 0, 0, .638247), 2.78 s, equal to the calculated value |
| route_c1b | 20 | (.267589, 0, 0, .732411) | (.267589, 0, 0, .732411), complete, 0.05 s, equal to the calculated value | (.267589, 0, 0, .732411), complete, 0.07 s, equal to the calculated value | (0, 0, 0, 1), 1.95 s, another value |
| route_c1b | 40 | (.179009, 0, 0, .820991) | (.179009, 0, 0, .820991), complete, 0.06 s, equal to the calculated value | (.179009, 0, 0, .820991), complete, 0.18 s, equal to the calculated value | (0, 0, 0, 1), 1.95 s, another value |
| route_c1b | 60 | (.119752, 0, 0, .880248) | (.119752, 0, 0, .880248), complete, 0.06 s, equal to the calculated value | (.119752, 0, 0, .880248), complete, 0.53 s, equal to the calculated value | (0, 0, 0, 1), 1.89 s, another value |
| route_c1b | 80 | (.080111, 0, 0, .919889) | (.080111, 0, 0, .919889), complete, 0.06 s, equal to the calculated value | no value: not covered: more ground statements than the limit of the key mode (GK_KEY_GROUND) | (0, 0, 0, 1), 1.89 s, another value |
| route_c1b | 200 | (.00718, 0, 0, .99282) | (.00718, 0, 0, .99282), complete, 0.10 s, equal to the calculated value | no value: not covered: more ground statements than the limit of the key mode (GK_KEY_GROUND) | (0, 0, 0, 1), 2.00 s, another value |
| rt_c2 | 5 | (.59049, 0, 0, .40951) | (.59049, 0, 0, .40951), complete, 0.05 s, equal to the calculated value | (.59049, 0, 0, .40951), not complete, limit, equal to the calculated value | (.59049, 0, 0, .40951), 4.07 s, equal to the calculated value |
| rt_c2 | 20 | (.121577, 0, 0, .878423) | (.121577, 0, 0, .878423), complete, 0.06 s, equal to the calculated value | (0, 0, 0, 1), not complete, limit, another value | (.121577, 0, 0, .878423), limit, equal to the calculated value |
| rt_c2 | 40 | (.014781, 0, 0, .985219) | (.014781, 0, 0, .985219), complete, 0.05 s, equal to the calculated value | (0, 0, 0, 1), not complete, limit, another value | (.014781, 0, 0, .985219), limit, equal to the calculated value |
| rt_c2 | 60 | (.001797, 0, 0, .998203) | (.001797, 0, 0, .998203), complete, 0.06 s, equal to the calculated value | (0, 0, 0, 1), not complete, limit, another value | (.001797, 0, 0, .998203), limit, equal to the calculated value |
| rt_c2 | 80 | (.000218, 0, 0, .999782) | (.000218, 0, 0, .999782), complete, 0.07 s, equal to the calculated value | no value: not covered: more ground statements than the limit of the key mode (GK_KEY_GROUND) | (.000218, 0, 0, .999782), limit, equal to the calculated value |
| rt_c2 | 200 | (0, 0, 0, 1) | (0, 0, 0, 1), complete, 0.19 s, equal to the calculated value | no value: not covered: more ground statements than the limit of the key mode (GK_KEY_GROUND) | (0, 0, 0, 1), limit, equal to the calculated value |
| rt_mix | 5 | (.236196, 0, 0, .763804) | (.236196, 0, 0, .763804), not complete, limit, equal to the calculated value | (.236196, 0, 0, .763804), not complete, limit, equal to the calculated value | (.236196, 0, 0, .763804), 2.78 s, equal to the calculated value |
| rt_mix | 10 | (.139471, 0, 0, .860529) | (.139471, 0, 0, .860529), not complete, limit, equal to the calculated value | (.139471, 0, 0, .860529), not complete, limit, equal to the calculated value | (.139471, 0, 0, .860529), limit, equal to the calculated value |
| rt_mix | 20 | (.048631, 0, 0, .951369) | (0, 0, 0, 1), not complete, limit, another value | (0, 0, 0, 1), not complete, limit, another value | (0, 0, 0, 1), 1.95 s, another value |
<!-- end table -->

The route with contrary reports:

<!-- table opposed -->
| links | calculated value | the exact method | the exact method, ground first | the general method | the tool |
|---|---|---|---|---|---|
| 5 | (.252131, 0, 0, .747869) | (.252131, 0, 0, .747869), complete, 0.06 s | (.252131, 0, 0, .747869), complete, 0.06 s | (.252131, 0, 0, .747869), 2.82 s | (.252131, 0, 0, .747869), exact value of the tool |
| 10 | - | - | - | - | (.22737, 0, 0, .77263), sampled value of the tool, bound 0.005037 |
| 20 | (.129986, 0, 0, .870014) | (.129986, 0, 0, .870014), complete, 0.06 s | (.129986, 0, 0, .870014), complete, 0.08 s | (0, 0, 0, 1), 1.95 s | - |
| 40 | (.042241, 0, 0, .957759) | (.042241, 0, 0, .957759), complete, 0.06 s | (.042241, 0, 0, .957759), complete, 0.20 s | (0, 0, 0, 1), 1.95 s | - |
| 60 | (.013727, 0, 0, .986273) | (.013727, 0, 0, .986273), complete, 0.06 s | (.013727, 0, 0, .986273), complete, 0.52 s | (0, 0, 0, 1), 1.88 s | - |
| 80 | (.004461, 0, 0, .995539) | (.004461, 0, 0, .995539), complete, 0.06 s | no value: not covered: more ground statements than the limit of the key mode (GK_KEY_GROUND) | (0, 0, 0, 1), 1.89 s | - |
| 200 | (.000005, 0, 0, .999995) | (.000005, 0, 0, .999995), complete, 0.10 s | no value: not covered: more ground statements than the limit of the key mode (GK_KEY_GROUND) | (0, 0, 0, 1), 2.00 s | - |
<!-- end table -->

The grounding of `route_c1b`: what the exact method forms, what the full grounding has, and what clingo's grounder
writes:

<!-- table grounding -->
| links | instances of the recursive rule that clingo's grounder writes | all triples of constants | ground statements that the exact method forms | ground statements of the full grounding |
|---|---|---|---|---|
| 5 | 10 | 216 | 26 | 264 |
| 20 | 190 | 9,261 | 251 | 9,744 |
| 40 | 780 | 68,921 | 901 | 70,684 |
| 60 | 1,770 | 226,981 | 1,951 | 230,824 |
| 80 | 3,160 | 531,441 | 3,401 | 538,164 |
| 200 | 19,900 | 8,120,601 | 20,501 | 8,161,404 |
<!-- end table -->

ProbLog on the routes:

<!-- table problog -->
| family | links | ProbLog 2.3.0 | ProbLog's time | gk 1.3.2, the exact method |
|---|---|---|---|---|
| route_c1b | 5 | 0.36175283 | 0.10 s | (.361753, 0, 0, .638247), complete, 0.05 s |
| route_c1b | 20 | 0.2675887 | 0.12 s | (.267589, 0, 0, .732411), complete, 0.05 s |
| route_c1b | 40 | 0.17900929 | 0.18 s | (.179009, 0, 0, .820991), complete, 0.06 s |
| route_c1b | 60 | 0.11975216 | 0.24 s | (.119752, 0, 0, .880248), complete, 0.06 s |
| route_c1b | 80 | 0.080110811 | 0.28 s | (.080111, 0, 0, .919889), complete, 0.06 s |
| route_c1b | 200 | 0.0071802213 | 1.15 s | (.00718, 0, 0, .99282), complete, 0.10 s |
| rt_mix | 5 | 0.236196 | 0.10 s | (.236196, 0, 0, .763804), not complete, limit |
| rt_mix | 10 | 0.13947138 | 0.10 s | (.139471, 0, 0, .860529), not complete, limit |
| rt_mix | 20 | 0.048630662 | 0.12 s | (0, 0, 0, 1), not complete, limit |
| rt_mix | 80 | 8.73898e-05 | 0.17 s | not run |
| rt_mix | 200 | 2.8220316e-10 | 0.43 s | not run |
<!-- end table -->

The university base and the grids (inputs of part O3):

<!-- table university -->
| input | ground statements formed, of the full grounding | the exact method | the exact method, ground first | the general method |
|---|---|---|---|---|
| gk_dept1_scale0.25_person.gkp | 697 of 1,221,190 | (.983935, 0, 0, .016065), complete, 0.06 s | no value: not covered: more ground statements than the limit of the key mode (GK_KEY_GROUND) | (.983935, 0, 0, .016065), 0.75 s |
| gk_dept1_scale0.25_employee.gkp | 697 of 1,221,190 | (.997644, 0, 0, .002356), complete, 0.06 s | no value: not covered: more ground statements than the limit of the key mode (GK_KEY_GROUND) | (.997644, 0, 0, .002356), 1.00 s |
| gk_dept1_scale0.25_organization.gkp | 697 of 1,221,190 | (1, 0, 0, 0), complete, 0.06 s | no value: not covered: more ground statements than the limit of the key mode (GK_KEY_GROUND) | (1, 0, 0, 0), limit |
| gk_dept1_scale0.25_memberOf.gkp | 697 of 1,221,190 | (.49, 0, 0, .51), complete, 0.06 s | no value: not covered: more ground statements than the limit of the key mode (GK_KEY_GROUND) | (.49, 0, 0, .51), 0.31 s |
| gk_dept1_scale1_person.gkp | 2,909 of 55,062,113 | (.963204, 0, 0, .036796), complete, 0.10 s | no value: not covered: more ground statements than the limit of the key mode (GK_KEY_GROUND) | (.963204, 0, 0, .036796), 0.89 s |
| gk_dept1_scale1_employee.gkp | 2,909 of 55,062,113 | (.999414, 0, 0, .000586), complete, 0.11 s | no value: not covered: more ground statements than the limit of the key mode (GK_KEY_GROUND) | (.999414, 0, 0, .000586), 1.00 s |
| gk_dept1_scale1_organization.gkp | 2,909 of 55,062,113 | (1, 0, 0, 0), complete, 0.11 s | no value: not covered: more ground statements than the limit of the key mode (GK_KEY_GROUND) | (1, 0, 0, 0), limit |
| gk_dept1_scale1_memberOf.gkp | 2,909 of 55,062,113 | (.49, 0, 0, .51), complete, 0.12 s | no value: not covered: more ground statements than the limit of the key mode (GK_KEY_GROUND) | (.49, 0, 0, .51), 0.35 s |
| gk_dept3_scale1_person.gkp | 8,709 of 1,261,761,734 | (.966422, 0, 0, .033578), complete, 0.43 s | no value: not covered: more ground statements than the limit of the key mode (GK_KEY_GROUND) | (.966422, 0, 0, .033578), 1.13 s |
| gk_dept3_scale1_employee.gkp | 8,709 of 1,261,761,734 | (.999781, 0, 0, .000219), complete, 0.48 s | no value: not covered: more ground statements than the limit of the key mode (GK_KEY_GROUND) | (.999781, 0, 0, .000219), 1.75 s |
| gk_dept3_scale1_organization.gkp | 8,709 of 1,261,761,734 | (1, 0, 0, 0), complete, 0.45 s | no value: not covered: more ground statements than the limit of the key mode (GK_KEY_GROUND) | (1, 0, 0, 0), limit |
| gk_dept3_scale1_memberOf.gkp | 8,709 of 1,261,761,734 | (.36, 0, 0, .64), complete, 0.42 s | no value: not covered: more ground statements than the limit of the key mode (GK_KEY_GROUND) | (.36, 0, 0, .64), 0.54 s |
| gk_corner16.gkp | 61 of 826 | (.617081, 0, 0, .382919), complete, 0.05 s | (.617081, 0, 0, .382919), not complete, limit | (.359375, 0, 0, .640625), limit |
| gk_corner33.gkp | 189 of 4,385 | (.565177, 0, 0, .434823), complete, 0.05 s | (0, 0, 0, 1), not complete, limit | (.490222, 0, 0, .509778), limit |
| gk_corner56.gkp | 456 of 16,306 | (.53227, 0, 0, .46773), complete, 0.08 s | (0, 0, 0, 1), not complete, limit | (.180832, 0, 0, .819168), limit |
| gk_full_d1.gkp | 47,745 of 16,843,457 | (.71875, 0, 0, .28125), complete, 0.30 s | no value: not covered: more ground statements than the limit of the key mode (GK_KEY_GROUND) | (.71875, 0, 0, .28125), limit |
| gk_full_d2.gkp | 47,745 of 16,843,457 | (.617081, 0, 0, .382919), complete, 0.30 s | no value: not covered: more ground statements than the limit of the key mode (GK_KEY_GROUND) | (.359375, 0, 0, .640625), limit |
| gk_full_d3.gkp | 47,745 of 16,843,457 | (.565177, 0, 0, .434823), complete, 0.30 s | no value: not covered: more ground statements than the limit of the key mode (GK_KEY_GROUND) | (.434353, 0, 0, .565647), limit |
| gk_full_d4.gkp | 47,745 of 16,843,457 | (.53227, 0, 0, .46773), complete, 0.32 s | no value: not covered: more ground statements than the limit of the key mode (GK_KEY_GROUND) | (.194709, 0, 0, .805291), limit |
| gk_full_d5.gkp | 47,745 of 16,843,457 | (.508872, 0, 0, .491128), complete, 4.12 s | no value: not covered: more ground statements than the limit of the key mode (GK_KEY_GROUND) | (.061287, 0, 0, .938713), limit |
| gk_full_d6.gkp | 47,745 of 16,843,457 | no value: evaluation budget: the deadline of the evaluation passed | no value: not covered: more ground statements than the limit of the key mode (GK_KEY_GROUND) | (.030946, 0, 0, .969054), limit |
| gk_full_d8.gkp | 47,745 of 16,843,457 | no value: memory: the evaluator passed its memory budget of 8192 MB | no value: not covered: more ground statements than the limit of the key mode (GK_KEY_GROUND) | (.007794, 0, 0, .992206), limit |
<!-- end table -->

## Where the paper's numbers are

- The route table of Section 7.3 and the route with contrary reports (Section 7.2): the rows of `family` route_c1b and
  route_opp, columns `value`, `complete`, `time_s` and `target`.
- The two grounding counts: the rows of clingo's grounder, column `grounder_instances`, and of the exact method,
  columns `ground_statements` and `ground_full`.
- The university base, 8,709 ground statements of 1.26 billion: the rows of `family` university.
- The route with certain rules and a default (row B of the table of limits): the rows of `family` rt_mix.

`results.csv` has one row per run and answer. The columns are described on the first page of the
folder ([`../README.md`](../README.md), section "The tables of a part").
