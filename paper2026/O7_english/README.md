# O7: the English cases

This part reproduces the English case of Section 7.2 of the paper, the
English case of the budget paragraph in Section 7.4, and part O7 of the
online appendix. Four English texts went through the translation pipeline
of the project (`llmpipe` of <https://github.com/tammet/nlpsolver>), which
calls a language model. The pipeline translated each text into clauses.
gk ran on the extracted clauses unchanged, with the options and the search
strategy that the pipeline stores.

- Each case is one preserved extraction, with its provider and model
  recorded. The language-model calls are not rerun; the extractions are
  the files of this part.
- The reference tool declines the extractions, because they contain Skolem
  functions. Each reference value is the tool's value on a ground
  abstraction, written by hand from the extracted clauses. The
  correspondence between an abstraction and its extraction is not proved.
- The cases show the reasoning. They give no success rate over English
  inputs.
- The names N1 and N2 are names of English cases. The earlier comparison
  table (part O5) also has cases N1 and N2; those are different inputs.

## Files

```text
O7_english/
  results.tsv  runs.tsv
  pipeline/  axioms_std.js  strategy.json
  n1v1/  text.txt  gk_claude.js  gk_deepseek.js  gk_gemini.js  mcref_ground_claude.gkp
         skeleton/  deft.dlgp  delp.delp  gk_certified_mara.gkp  gk_labAccess_mara.gkp  gk_mayUse_mara.gkp
  n2v2/  text.txt  gk_deepseek.js  gk_claude.js  gk_gemini.js
         mcref_ground_deepseek.gkp  mcref_ground_claude.gkp  mcref_ground_gemini.gkp
         skeleton/  deft.dlgp  delp.delp  gk_mayEnter_nora.gkp  gk_not_mayEnter_nora.gkp
  n3/    text.txt  gk_who.js  gk_mike.js  gk_eve.js  gk_john.js  mcref_ground_john.gkp
         skeleton/  deft.dlgp  delp.delp  gk_fliesAndEats_mike.gkp  gk_fliesAndEats_john.gkp  gk_flies_john.gkp
  n4/    text.txt  gk.js  mcref_ground.gkp
         skeleton/  deft.dlgp  delp.delp  gk_eatsBerries_john.gkp  gk_not_eatsBerries_john.gkp
```

- `text.txt`: the English text of the case.
- `gk_*.js`: the extraction, the clauses that the pipeline gave to gk, in
  the JSON-LD-LOGIC syntax of gk. The name says the provider of the
  language model. For N3, `gk_who.js` is the stored extraction with the
  question "Who flies and eats?", and `gk_mike.js`, `gk_eve.js` and
  `gk_john.js` replace its question clause by a ground question for one
  person. Nothing else changed.
- `pipeline/axioms_std.js`: the standard axioms that the pipeline adds to
  every extraction (the same file for all four cases).
- `pipeline/strategy.json`: the search strategy that the pipeline stores,
  `{"strategy": ["negative_pref", "posunitpara"], "query_preference": 1}`.
  The runs of 2026-11-04 passed the same text with `-strategytext`; gk reads
  a `-strategy` file into the same text.
- `mcref_ground*.gkp`: the ground abstractions for the reference tool. gk
  also runs on them.
- `skeleton/`: the certain skeletons, written by hand: confidences dropped,
  the pipeline's priorities kept (as DEFT preferences, DeLP specificity or
  gk ranks), Skolem terms as constants. `deft.dlgp` is the DEFT input in the
  DLGP syntax, `delp.delp` the DeLP input, and each `gk_*.gkp` is the gk
  input for one question.

The comment lines of the ground abstractions were rewritten for this
folder, and the skeleton gk inputs got a header. Their clauses are the ones
that were run. The other files are the files that were run.

## Rerun gk and the reference tool

gk on an extraction, from the repository root:

```sh
./bin/gk paper2026/O7_english/pipeline/axioms_std.js \
  -strategy paper2026/O7_english/pipeline/strategy.json -seconds 10 \
  paper2026/O7_english/n2v2/gk_deepseek.js \
  -taxonomy -confidence 0.1 -keepconfidence 0.1 -datafolder data -recursive
```

The options are the pipeline's options:

- the axioms file comes first and the extraction second;
- `-taxonomy` loads the taxonomy data of `data/` in this repository. The
  extractions write priorities in taxonomy form, such as
  `["$","library member",1]`. The two recorded cases N3 and N4 use the
  synonym `-defaults`, as their stored records do;
- `-confidence 0.1 -keepconfidence 0.1` are the pipeline's confidence
  limits;
- `-recursive` selects the recursive method, which is also gk's default;
- `-seconds 10` is the deadline. N4 also ran with `-seconds 2` and
  `-seconds 60`, and N3 for John with `-seconds 60`.

`runs.tsv` writes the same command relative to the folder of the input:
`../pipeline/axioms_std.js`, `../pipeline/strategy.json` and
`-datafolder ../../../data`. Most runs on the extractions stop at the
deadline with searches stopped, so their values can depend on the machine
load; `runs.tsv` marks every run on an extraction `alone`.

gk and the reference tool on a ground abstraction or a skeleton:

```sh
./bin/gk paper2026/O7_english/n2v2/mcref_ground_deepseek.gkp
python3 mcref/mcref.py paper2026/O7_english/n2v2/mcref_ground_deepseek.gkp --samples 200000 --seed 1 --all-atoms
```

The reference tool ran with 200,000 samples and seed 1 in this part. Each
share then lies within .0036 of the exact value with 95 % confidence. On
the abstractions it ran with `--all-atoms`, which adds the value of every
atom to its output.

## N1v1: a contested premise

**Text.** "Mara is probably certified. Mara is probably not certified.
Certified people normally have laboratory access. People with laboratory
access normally may use the spectrometer. May Mara use the spectrometer?"

**Extraction** (claude-sonnet-4-6, `n1v1/gk_claude.js`). The certification
fact and its negation, each at .7746. Two normal defaults at .95, for the
access and for the permission.

| system | file | result |
|---|---|---|
| gk | `n1v1/gk_claude.js` | (0, 0, 0, 1), no approximation note |
| gk | `n1v1/gk_deepseek.js` (deepseek-v4-flash) | (0, 0, 0, 1) |
| gk | `n1v1/gk_gemini.js` (gemini-2.5-flash) | (0, 0, 0, 1) |
| mcref | `n1v1/mcref_ground_claude.gkp` | (0, 0, 0, 1); the certification atom `c`: (0, 0, .7735, .2265) |
| gk | `n1v1/mcref_ground_claude.gkp` | (0, 0, 0, 1) |

The extractions of deepseek-v4-flash and gemini-2.5-flash are also opposed
pairs. Two opposed facts of equal confidence on one atom give conflict and
no usable support, so neither default applies. For each provider the file
is the input that the pipeline saved for gk. For N1v1 the pipeline's first
attempt answered "Unknown", and the saved input comes from its second
route, a translation into relations.

## N2v2: an uncertain exception (the case of Section 7.2)

**Text.** "Library members normally may enter the archive. A library member
whose membership is suspended may not enter the archive. Nora is a library
member. Nora's membership is probably suspended. May Nora enter the
archive?"

**Extraction.** A certain membership, a normal default for the permission
at .96, a strict clause against the permission for a suspended membership,
and the suspension as an uncertain fact. The confidence of the suspension
differs by provider.

| provider and model | suspension | gk on the extraction | tool on the abstraction | gk on the abstraction |
|---|---|---|---|---|
| deepseek-v4-flash (the case of the paper) | .7746 | (.2164, .7746, 0, .0090), cycle cut | (.2167, .7744, 0, .0089) | (.2164, .7746, 0, .0090) |
| claude-sonnet-4-6 | .88 | (.0003, .8849, .1148, 0), cycle cut, three times | (.1155, .8798, 0, .0047) | (.1152, .88, 0, .0048) |
| gemini-2.5-flash | .8434 | (0, .9991, 0, .0009), cycle cut | (.1506, .8431, 0, .0063) | (.1503, .8434, 0, .0063) |

The files: `n2v2/gk_<provider>.js` and `n2v2/mcref_ground_<provider>.gkp`.
On the Claude extraction gk keeps the against share (.8849 for .8798). It
reports conflict .1148 where the abstraction has support .1155. On the
abstraction gk gives (.1152, .88, 0, .0048), also with cycle-cut notes.
So gk records the cut in both runs, and its value differs from the tool's
only on the extraction. No controlled run isolates the cause. The runs with
gpt-5.1 failed: every call hit the provider's rate limit.

## N3: three candidates (recorded case 1534)

**Text.** "Birds fly and eat. Baby birds do not fly. John is probably a baby
bird. Mike and Eve and John are birds. Who flies and eats?"

**Extraction.** A stored record of 2026-06-03 (claude-sonnet-4-6), 32
clauses. The flying default has strength .9, the eating default .98, and
the baby-bird fact .6.

On `n3/gk_who.js`, the question with a variable, gk prints "a question with
variables: the recursion did not run" and no value. The statement concerns
this input: on other inputs the recursive method answers such questions for
each binding (part O2). The three derived inputs ask a ground question for
each person.

| person | file | gk | reference | approximation notes |
|---|---|---|---|---|
| Mike | `n3/gk_mike.js` | (.882, 0, 0, .118) | hand value .9 × .98 = .882 | none |
| Eve | `n3/gk_eve.js` | (.882, 0, 0, .118) | the same | none |
| John | `n3/gk_john.js` | (0, .6, 0, .4), the same at 60 s | tool on `n3/mcref_ground_john.gkp`: (.3536, .5993, 0, .0471) | cycle cut, three times |

On the abstraction for John gk gives (.3528, .6, 0, .0472), which agrees
with the tool. On the extraction gk reports ignorance in the worlds where
the baby-bird fact does not pass.

## N4: a budget case (recorded case 1439)

**Text.** "Bears eat berries. Baby bears do not eat berries. John is a baby
bear. John eats berries?"

**Extraction.** A stored record of 2026-06-03 (claude-sonnet-4-6), 25
clauses. A normal default at .98 for bears has priority 1. A clause at .98
against it for baby bears has priority 4. John is a baby bear by a certain
fact.

| deadline | gk on `n4/gk.js` | note |
|---|---|---|
| 2 s | (.98, 0, 0, .02) | 17 of 18 tasks stopped |
| 10 s | (.98, 0, 0, .02) | 9 of 18 tasks stopped |
| 60 s | (.0004, .9608, .0192, .0196) | 14 applications |

The tool gives (0, .9801, 0, .0199) on `n4/mcref_ground.gkp`, and gk gives
(0, .98, 0, .02) there. The abstraction writes the two priorities as ranks
1 and 4. At the default deadline gk cuts the search for opposition, and the
answer is on the for side. At 60 s the value is near the tool's, with
.0192 of conflict. Each row is a single run; part O6 holds the same input
for the budget paragraph of Section 7.4.

## Certain skeletons: DEFT 1.0.0 and DeLP

DEFT 1.0.0, TweetyProject DeLP 1.27, gk and the tool ran on the
skeletons. DEFT has no classical negation: the skeleton names the negated
atom (`noBerries`, `noEnter`, `notCertified`, `noFly`) and adds a negative
constraint.

| case | question | DEFT 1.0.0 | DeLP 1.27 | gk and the tool |
|---|---|---|---|---|
| N3 | fliesAndEats(mike) | defeasibly entailed | yes | (1, 0, 0, 0) |
| N3 | fliesAndEats(john) | not entailed | undecided | (0, 0, 0, 1) |
| N3 | flies(john) | not entailed | no | (0, 1, 0, 0) |
| N4 | eatsBerries(john) | not entailed; the negation entailed | no; the negation yes | (0, 1, 0, 0) |
| N2v2 | mayEnter(nora) | not entailed; the negation strictly entailed | no; the negation yes | (0, 1, 0, 0), cycle-cut notes in gk |
| N1v1 | certified(mara) | not entailed | undecided | (0, 0, 0, 1) |
| N1v1 | labAccess(mara), mayUse(mara) | defeasibly entailed | undecided | (0, 0, 0, 1) |

gk and the tool also answer the negated questions of N4 and N2v2
(`gk_not_eatsBerries_john.gkp`, `gk_not_mayEnter_nora.gkp`) with
(1, 0, 0, 0).

The four systems give the same verdict on every row except the last. There
DEFT entails the access and the permission from a certification that it
does not entail. DeLP, gk and the tool leave both undecided. The comparison
is qualitative and checks no number. A skeleton also changes the question:
the certification skeleton has opposed defaults, where the extraction has
opposed uncertain facts.

The DEFT and DeLP runs of 2026-11-04 have no saved output; the record holds
their verdicts only. `runs.tsv` therefore lists them for a new run, and the
run store ran them on 2026-11-10 with DEFT 1.0.0 and TweetyProject DeLP
1.27: every rerun printed the recorded verdicts. The
commands, from a skeleton folder (the two small Java drivers `DeftRun.java`
and `DelpRun.java` are in part O3):

```sh
java -Xmx8g -cp "DEFT-1.0.0.jar:DEFT_CLASSPATH" DeftRun.java deft.dlgp "eatsBerries(john)" "noBerries(john)"
java -cp "TWEETY_LIBS/*" DelpRun.java delp.delp "eatsBerries(john)" "~eatsBerries(john)"
```

`DeftRun` loads the file, saturates it and prints the entailment status of
each query atom. `DelpRun` answers each query with generalized specificity
as yes, no, undecided or unknown. [`../SYSTEMS.md`](../SYSTEMS.md) says how
to install DEFT and TweetyProject.

## Provenance and versions

- N3 and N4 come from the pipeline's stored run of 2026-06-03 (nlpsolver
  tag `core-2026-06-03`, commit `585e8b0`, model claude-sonnet-4-6). N1v1
  and N2v2 were translated on 2026-11-04 with the pipeline at nlpsolver
  commit `b1a7298`, by claude-sonnet-4-6, deepseek-v4-flash and
  gemini-2.5-flash. The full dataset holds the pipeline transcripts and the
  two stored records.
- The ground abstractions and the skeletons were written by hand on
  2026-11-04.
- The paper's gk and mcref values came from gk 1.2.3 and mcref 1.1.0 on
  2026-11-04. Every gk and mcref row of this part names a run of gk 1.2.5
  or mcref 1.1.2 of 2026-11-10 in the run store (30 gk runs, 16 mcref
  runs); each gives the printed value.
