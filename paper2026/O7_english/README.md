# O7: cases translated from English

This part holds four English cases (N1 to N4) that a language-model pipeline translated into gk input, and the
303 tasks of the pipeline's regression set. gk 1.3.2 ran the two English cases of the paper's time-budget
paragraph (N2 with the translation of one model, and N4) and the 303 pipeline tasks under the default. The other
English inputs have no run of gk 1.3.2. The cells of DEFT and TweetyProject DeLP on the certain skeletons come
from the recorded runs of the earlier comparison.

## Where the inputs come from

`inputs/n1v1/`, `inputs/n2v2/`, `inputs/n3/` and `inputs/n4/` hold each case's English text, the model's
extraction and translation, the gk input and the certain skeleton for DEFT and DeLP. `inputs/pipeline/` holds the
background axioms and the strategy that the runs use. The pipeline tasks are packed in
`inputs/pipeline_tasks.tar.xz` (`inputs/pipeline_tasks.files.tsv` lists them); unpack them with
`tar -xJf inputs/pipeline_tasks.tar.xz -C inputs`. The runs of the pipeline tasks read the taxonomy data
(`-defaults`) from the repository's folder `data/`: the recorded runs read a copy of the same two files.

## Rerun

To rerun every gk and tool run of this part and compare each value with `results.csv`:

```sh
python3 check_gk.py --part O7_english --gk PATH/TO/gk --mcref PATH/TO/mcref.py
```

Its last line names the values compared and how many differ. Every value is expected to be equal, except that
a value can change from run to run when the recorded run did not end by itself or the rerun reports cut or
queued searches; the check reports such a difference apart. The runs and values that it compares:

<!-- table check -->
| gk runs | tool runs | runs with a recorded value | values compared | of these, on runs that did not end by themselves |
|---|---|---|---|---|
| 305 | 0 | 298 | 306 | 280 |
<!-- end table -->

`$GK` stands for the gk binary and `$MCREF` for the tool's `mcref.py`. Every command of `runs.tsv` runs
in the folder that its column `cwd` names, relative to this folder's parent (`paper2026/`).

## Results

<!-- table cases -->
| case | question | value of the default at 10 s | answered by | ended by itself | first limit |
|---|---|---|---|---|---|
| N2, deepseek | $defq0 | (.010993, .949195, 0, .039812) | general | no | searches stopped: 31 cut, 45 queued |
| N4 | $defq0 | (.98, 0, 0, .02) | general | no | searches stopped: 19 cut, 2 queued |
<!-- end table -->

The pipeline tasks, by set. A task is right when gk's label equals the expected label.

<!-- table pipeline -->
| set | tasks | right labels | answered by the general method | by the exact method | no value |
|---|---|---|---|---|---|
| core | 100 | 66 | 100 | 0 | 5 |
| folio | 203 | 135 | 201 | 0 | 2 |
<!-- end table -->

The other systems, from the recorded runs:

<!-- table others -->
| case | system | outcome | what the system printed | note |
|---|---|---|---|---|
| n1v1 | translation pipeline with gpt-5.1 | no answer | - | no extraction; every call hit the provider's rate limit (HTTP 429) |
| n2v2 | translation pipeline with gpt-5.1 | no answer | - | no extraction; every call hit the provider's rate limit (HTTP 429) |
| n3 | DEFT 1.0.0 | another quantity | defeasibly entailed | a verdict without a number; query fliesAndEats(mike); the run of 2026-11-04 has a memo rec |
| n3 | TweetyProject DeLP 1.27 | another quantity | yes | a verdict without a number; query fliesAndEats(mike); generalized specificity; the run of  |
| n3 | DEFT 1.0.0 | another quantity | not entailed | a verdict without a number; query fliesAndEats(john); the run of 2026-11-04 has a memo rec |
| n3 | TweetyProject DeLP 1.27 | another quantity | undecided | a verdict without a number; query fliesAndEats(john); generalized specificity; the run of  |
| n3 | DEFT 1.0.0 | another quantity | not entailed | a verdict without a number; query flies(john); the run of 2026-11-04 has a memo record onl |
| n3 | TweetyProject DeLP 1.27 | another quantity | no | a verdict without a number; query flies(john); generalized specificity; the run of 2026-11 |
| n4 | DEFT 1.0.0 | another quantity | not entailed; the negation entailed | a verdict without a number; query eatsBerries(john); the run of 2026-11-04 has a memo reco |
| n4 | TweetyProject DeLP 1.27 | another quantity | no; the negation yes | a verdict without a number; query eatsBerries(john); generalized specificity; the run of 2 |
| n2v2 | DEFT 1.0.0 | another quantity | not entailed; the negation strictly entailed | a verdict without a number; query mayEnter(nora); the run of 2026-11-04 has a memo record  |
| n2v2 | TweetyProject DeLP 1.27 | another quantity | no; the negation yes | a verdict without a number; query mayEnter(nora); generalized specificity; the run of 2026 |
| n1v1 | DEFT 1.0.0 | another quantity | not entailed | a verdict without a number; query certified(mara); the run of 2026-11-04 has a memo record |
| n1v1 | TweetyProject DeLP 1.27 | another quantity | undecided | a verdict without a number; query certified(mara); generalized specificity; the run of 202 |
| n1v1 | DEFT 1.0.0 | another quantity | defeasibly entailed | a verdict without a number; query labAccess(mara); the run of 2026-11-04 has a memo record |
| n1v1 | TweetyProject DeLP 1.27 | another quantity | undecided | a verdict without a number; query labAccess(mara); generalized specificity; the run of 202 |
| n1v1 | DEFT 1.0.0 | another quantity | defeasibly entailed | a verdict without a number; query mayUse(mara); the run of 2026-11-04 has a memo record on |
| n1v1 | TweetyProject DeLP 1.27 | another quantity | undecided | a verdict without a number; query mayUse(mara); generalized specificity; the run of 2026-1 |
<!-- end table -->

## Where the paper's numbers are

- The sentence on the 303 tasks from English text: the rows with a `set`, column `class`.
- The English cases of the time budget: part O6.

`results.csv` has one row per run and answer. The columns are described on the first page of the
folder ([`../README.md`](../README.md), section "The tables of a part").
