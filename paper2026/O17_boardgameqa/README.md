# O17: BoardgameQA

This part holds the BoardgameQA benchmark, a public dataset of theories with contradicting rules and preferences
(Kazemi et al., "BoardgameQA: A Dataset for Natural Language Reasoning with Contradictory Information", NeurIPS
2023). A script converted the test examples of the three main sets (depth 1, 2 and 3) from the release's own
formal form into gk input, without a language model. gk 1.3.2 answers every example under the default; the
label of the release is the target. A second input per example adds confidences (.9 on facts, .8 on rules); it
has no label, and the tool computes the first examples of each set.

## Where the inputs come from

- The release: `https://storage.googleapis.com/gresearch/BoardgameQA/BoardgameQA.zip`, licensed CC BY (footnote
  1 of the paper above). Its SHA-256 is in `BoardgameQA.zip.sha256`.
- The converted inputs: `inputs/converted.tar.xz` (listing `inputs/converted.files.tsv`), with
  `converted/meta.json` (per example: the label, the goal, the question, the ranks, the conversion status and
  the result of the first knowledge test), `converted/counts.json` and `converted/blocking.json` (the second
  knowledge test). Unpack with `tar -xJf inputs/converted.tar.xz -C inputs`.
- `convert_boardgameqa.py` converts the release again: `python3 -I convert_boardgameqa.py BoardgameQA.zip OUT`.
  It reads the release's JSON files as data and writes the inputs and `meta.json`.
- `inputs/variant/`: one input of depth 3, example 628, with equal ranks for two conflicting rules that only the
  conversion's ranks order. `ranks.json` lists the conflicting pairs that the conversion orders and the release
  does not; `nine.json` holds the nine examples read by hand.

**Background knowledge.** Two tests mark the examples whose label needs knowledge that the theory does not
state. The first test (the one the paper uses): the release's proof applies a rule ("according to Rule n") of
which a body literal matches no fact and no rule head literally. The second test also marks an example where a
rule of higher preference has such a body literal and its head conflicts with the head of the rule it is
preferred over. Both tests are heuristics of ours.

## Rerun

To rerun every gk and tool run of this part and compare each value with `results.csv`:

```sh
python3 check_gk.py --part O17_boardgameqa --gk PATH/TO/gk --mcref PATH/TO/mcref.py
```

Its last line names the values compared and how many differ. Every value is expected to be equal, except that
a value can change from run to run when the recorded run did not end by itself or the rerun reports cut or
queued searches; the check reports such a difference apart. The runs and values that it compares:

<!-- table check -->
| gk runs | tool runs | runs with a recorded value | values compared | of these, on runs that did not end by themselves |
|---|---|---|---|---|
| 6,001 | 300 | 6,301 | 6,301 | 0 |
<!-- end table -->

`$GK` stands for the gk binary and `$MCREF` for the tool's `mcref.py`. Every command of `runs.tsv` runs
in the folder that its column `cwd` names, relative to this folder's parent (`paper2026/`).

## Results

<!-- table labels -->
| set | examples | answered by the exact method | complete | labels reproduced | reproduced, without the examples that need knowledge by test 1 | the same, by test 1 or test 2 | reproduced among the examples of test 1 |
|---|---|---|---|---|---|---|---|
| depth 1 | 1,000 | 1,000 | 1,000 | 686 | 686 of 686 | 475 of 475 | 0 of 314 |
| depth 2 | 1,000 | 1,000 | 1,000 | 608 | 608 of 613 | 269 of 269 | 0 of 387 |
| depth 3 | 1,000 | 1,000 | 1,000 | 539 | 485 of 489 | 111 of 111 | 54 of 511 |
| all | 3,000 | 3,000 | 3,000 | 1,833 | 1,779 of 1,788 | 855 of 855 | 54 of 1,212 |
<!-- end table -->

The examples that need no knowledge by the first test and whose label gk does not reproduce, with the cause
read by hand from the theory:

<!-- table nine -->
| example | label of the release | gk's label | the cause |
|---|---|---|---|
| depth 2, example 95 | unknown | proved | knowledge: 76 > 18 + 37, so Rule4 applies and blocks Rule3 |
| depth 2, example 116 | unknown | proved | knowledge: white is in the flag of Italy |
| depth 2, example 407 | unknown | proved | knowledge: two is less than five |
| depth 2, example 695 | unknown | disproved | knowledge: both names begin with B |
| depth 2, example 860 | unknown | proved | knowledge: the shark is older than twelve months |
| depth 3, example 161 | unknown | proved | knowledge: 97 > 44 + 50 |
| depth 3, example 287 | unknown | proved | knowledge: five is more than two |
| depth 3, example 386 | unknown | proved | knowledge: 64 > 62 |
| depth 3, example 938 | unknown | disproved | no cause found: literal matching of the rules gives disproved, as gk does; the release says unknown and gives no reason |
<!-- end table -->

The order that the conversion adds. The conversion gives each rule a rank from the release's preferences, so two
conflicting rules can get different ranks although the release orders neither over the other:

<!-- table order -->
| examples with a conflicting pair that only the conversion's ranks order | of these, with a pair whose two rules can both apply | the variant with equal ranks gives the same answer as the converted input |
|---|---|---|
| 9 | 1 | 1 of 1 |
<!-- end table -->

The inputs with confidences:

<!-- table conf -->
| inputs with confidences | complete answers | inputs with a value of the tool | gk equal to the tool's exact value |
|---|---|---|---|
| 3,000 | 3,000 | 300 | 300 |
<!-- end table -->

## Where the paper's numbers are

- The two sentences on BoardgameQA: the table above, from the rows of `c6_gk_crisp`, columns `class` and
  `knowledge_test_1`.
- The nine examples: the rows with `knowledge_test_1` no and `class` another label, column `cause`.
- The dependence on the order of the conversion: `ranks.json` and the run of the variant.

`results.csv` has one row per run and answer. The columns are described on the first page of the
folder ([`../README.md`](../README.md), section "The tables of a part").
