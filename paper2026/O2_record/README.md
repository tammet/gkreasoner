# O2: our collection, and the inputs that the tool accepts

This part holds the collection of inputs that was written while the method was built. The tool accepts 360 of
its inputs. gk 1.3.2 answers each of them under the default, the general method and the exact method, and the
tool computes each of them, exactly or by sampling. The other inputs of the collection, which the tool declines,
are listed with the reason and with the answer of the default.

## Where the inputs come from

The inputs were written for gk while the method was built, or restated from documentation examples, published
studies and the literature. `inputs.csv` names the set and the source of every accepted input, and
`literature_sources.csv` the publication behind each input of the set `lit`.

<!-- table sets -->
| set | inputs | where they come from |
|---|---|---|
| ab | 109 | design probes of the recursive method (generated) |
| boundary | 2 | boundary cases of the recursive method |
| demo | 18 | demo/cumulate.js; and 17 other sources |
| examples | 97 | Examples/arithmetic/boundary_comparison.js; and 96 other sources |
| families | 54 | generated families of directed chains |
| lit | 39 | literature case bg/bg10_knowledgelight_d2_639.gkp; and 38 other sources |
| paper | 4 | worked examples of the method's design notes |
| studies | 21 | published study study10_smokes2ans.js; and 20 other sources |
| table | 16 | inputs of the extended comparison table |
| all | 360 |  |
<!-- end table -->

## Files

```text
inputs/<set>/...          the 360 inputs that the tool accepts
inputs/declined.tar.xz    the inputs that the tool declines; inputs/declined.files.tsv lists them
inputs.csv                the set, the source and the SHA-256 of every accepted input
literature_sources.csv    the publication behind each input of the set lit
declined.csv              one row per declined input: the tool's reason, the default's answer
runs.tsv  results.csv     the runs, and one row per run and answer
```

To read the declined inputs: `tar -xJf inputs/declined.tar.xz -C inputs`.

## Rerun

From the folder `paper2026/`:

```sh
cd O2_record/inputs/lit/nm && $GK nm3_yale_shooting.gkp
```

The first line holds `"value":[0,0,0,0]` and `"unresolved":1`: on the Yale shooting problem the share with no
value is 1.
The exact method answered, and the answer is complete.

To rerun every gk and tool run of this part and compare each value with `results.csv`:

```sh
python3 check_gk.py --part O2_record --gk PATH/TO/gk --mcref PATH/TO/mcref.py
```

Its last line names the values compared and how many differ. Every value is expected to be equal, except that
a value can change from run to run when the recorded run did not end by itself or the rerun reports cut or
queued searches; the check reports such a difference apart. The runs and values that it compares:

<!-- table check -->
| gk runs | tool runs | runs with a recorded value | values compared | of these, on runs that did not end by themselves |
|---|---|---|---|---|
| 1,742 | 1,022 | 1,396 | 1,636 | 70 |
<!-- end table -->

`$GK` stands for the gk binary and `$MCREF` for the tool's `mcref.py`. Every command of `runs.tsv` runs
in the folder that its column `cwd` names, relative to this folder's parent (`paper2026/`).

## Results

The answers by class. "Complete and equal" means equal within 1e-6 to an exact value of the tool. A value of the
tool with a stated limit of its proof search is not an exact value; its answers form a class of their own.

<!-- table classes -->
| class of the answer | the default | the general method | the exact method |
|---|---|---|---|
| another value | 0 | 10 | 0 |
| complete and equal | 0 | 0 | 352 |
| complete and within the sampling bound | 0 | 0 | 8 |
| equal to the tool | 0 | 381 | 0 |
| exhaustive search: complete and equal | 352 | 0 | 0 |
| exhaustive search: complete and within the sampling bound | 8 | 0 | 0 |
| exhaustive search: not complete | 28 | 0 | 0 |
| general: equal to the tool | 24 | 0 | 0 |
| general: no value of the tool | 1 | 0 | 0 |
| no answer named | 4 | 4 | 4 |
| no value of the tool | 0 | 4 | 0 |
| not complete | 0 | 0 | 32 |
| not covered | 0 | 0 | 26 |
| not listed by gk; the tool gives another value | 1 | 16 | 0 |
| not listed by gk; the tool gives ignorance (0, 0, 0, 1) | 13 | 19 | 13 |
| not listed by gk; the tool has no value | 3 | 0 | 3 |
| the tool's value has a stated limit: another value | 0 | 2 | 0 |
| the tool's value has a stated limit: equal to the tool | 0 | 2 | 0 |
| the tool's value has a stated limit: general: another value | 2 | 0 | 0 |
| the tool's value has a stated limit: general: equal to the tool | 2 | 0 | 0 |
| all answers | 438 | 438 | 438 |
<!-- end table -->

The general method's answers, by the kind of the tool's value:

<!-- table general -->
| the general method on the collection | answers |
|---|---|
| equal to an exact value of the tool | 351 |
| within the sampling bound of a sampled value of the tool | 30 |
| equal to a value of the tool with a stated limit of its proof search | 2 |
| another value than a value of the tool with a stated limit of its proof search | 2 |
| another value | 10 |
| an answer of the collection that gk does not list | 35 |
| no value of the tool, or no answer named | 8 |
| all answers | 438 |
<!-- end table -->

The answers whose value of the tool has a stated limit of its proof search, or is a sampled value with such a
limit:

<!-- table limited -->
| input | answer | method | gk 1.3.2 | the tool's value | class |
|---|---|---|---|---|---|
| gbirds_trans_scasp.js | flies(b1) | default | (1, 0, 0, 0) | (1, 0, 0, 0) | the tool's value has a stated limit: general: equal to the tool |
| near.js | near(c1,c10) | default | (.7432, 0, 0, .2568) | (1, 0, 0, 0) | the tool's value has a stated limit: general: another value |
| partcapability3.js | -capability(fly,any_bird_constant) | default | (.9986, .0013, 0, .0001) | (.9986, .0013, 0, .0001) | the tool's value has a stated limit: general: equal to the tool |
| near.json | near(c1,c10) | default | (.7432, 0, 0, .2568) | (1, 0, 0, 0) | the tool's value has a stated limit: general: another value |
| gbirds_trans_scasp.js | flies(b1) | general | (1, 0, 0, 0) | (1, 0, 0, 0) | the tool's value has a stated limit: equal to the tool |
| near.js | near(c1,c10) | general | (.7522, 0, 0, .2478) | (1, 0, 0, 0) | the tool's value has a stated limit: another value |
| partcapability3.js | -capability(fly,any_bird_constant) | general | (.9986, .0013, 0, .0001) | (.9986, .0013, 0, .0001) | the tool's value has a stated limit: equal to the tool |
| near.json | near(c1,c10) | general | (.7522, 0, 0, .2478) | (1, 0, 0, 0) | the tool's value has a stated limit: another value |
| gbirds_trans_scasp.js | flies(b1) | exact | (1, 0, 0, 0) | (1, 0, 0, 0) | not complete |
| near.js | near(c1,c10) | exact | - | (1, 0, 0, 0) | not complete |
| partcapability3.js | -capability(fly,any_bird_constant) | exact | (.9986, .0013, 0, .0001) | (.9986, .0013, 0, .0001) | not complete |
| near.json | near(c1,c10) | exact | - | (1, 0, 0, 0) | not complete |
<!-- end table -->

The times of the runs that ended by themselves:

<!-- table time -->
| method | runs | ended by themselves | median time of these | largest time of these |
|---|---|---|---|---|
| default | 360 | 324 | .06 s | .39 s |
| general | 360 | 350 | .26 s | 6.28 s |
| exact | 360 | 299 | .06 s | .21 s |
<!-- end table -->

The inputs that the tool declines, by its reason:

<!-- table declined -->
| why the tool declines the input | inputs |
|---|---|
| equality | 522 |
| function symbols | 86 |
| taxonomy strength | 11 |
| conversion failed | 8 |
| unknown built-in | 8 |
| rank contexts | 7 |
| built-in over an open domain | 5 |
| JSON-LD structure | 3 |
| no constants | 2 |
| no question | 2 |
| the input is not a list of statements | 2 |
| uncertain formula with several clauses | 2 |
| unsupported formula form | 2 |
| compound question | 1 |
| grounding limit | 1 |
| all | 662 |
<!-- end table -->

What the default does on them:

<!-- table declined_default -->
| the default on the declined inputs: what answered | inputs |
|---|---|
| the general method, direct | 470 |
| an input error (exit 1) | 184 |
| the exact method, phase 1 | 5 |
| the general method, switch | 3 |
<!-- end table -->

## Where the paper's numbers are

- The agreement with the tool on the collection (Section 7.4 of the paper): the rows of
  `results.csv` with `method` exact or default, column `class`. Part O13 counts them with the other parts of the
  agreement.
- The secondary sentence on the general method's record ("on the 438 answers ..."): the rows with `method`
  general, column `class`, and `target_kind` for the kind of the tool's value.
- The 1,022 inputs of the collection: `inputs.csv` (accepted) and `declined.csv` (declined), with the column
  `tool_reason`.

`results.csv` has one row per run and answer. The columns are described on the first page of the
folder ([`../README.md`](../README.md), section "The tables of a part").
