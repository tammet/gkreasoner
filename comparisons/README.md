# Implemented-system comparison

This directory contains 16 comparison cases with their inputs, system
versions, relation classifications, and captured outputs. gk is compared
with nine external tools in eight external table columns; DLV and I-DLV
share a column. Results retain each system's native output form. The
claims concern the listed inputs, translations, system versions, and
captured outputs.

## GK in this comparison

gk is a first-order reasoner. It provides:

- input confidences on facts and rules, written `0.9::p(a)` or
  `0.9::h :- b`;
- query-directed non-ground first-order proof search;
- equality, function terms, and classical disjunction;
- same-polarity aggregation that preserves shared proof provenance;
- opposition resolution at the premise where the opposition occurs;
- recursively evaluated exception conditions and prioritized defaults;
- separate undercutting and rebutting attacks;
- four-component reports: positive support, negative support, conflict,
  and ignorance.

GK combines query-directed first-order resolution with input confidences,
explicit opposition, and recursively evaluated prioritized exceptions. It
returns proofs and four-component reports without global grounding.

The signed confidence of a query Q is

```text
C(Q) = s+(Q) - s-(Q)
```

positive support minus negative support; |C(Q)| is the confidence in the
reported verdict. A default rule is written with an exception condition,
for example `0.9::h :- unless(b)`: the rule applies unless `b` holds, and
the support for `b` is evaluated recursively against its opposing
evidence. An optional second argument of `unless` is a priority rank.

## Compared systems

| System | Version | Output used here | Project page |
|---|---|---|---|
| gk | 1.0.10 | signed confidence with a four-component report | this repository |
| ProbLog | 2.2.10 | scalar probability | <https://dtai.cs.kuleuven.be/problog/> |
| PASTA | 1.0.1 | lower/upper probability interval | <https://github.com/damianoazzolini/pasta> |
| plingo | 1.1.0 | scalar probability | <https://github.com/potassco/plingo> |
| smProbLog | 2.1.0.42 | scalar probability and inconsistent-worlds mass | <https://github.com/PietroTotis/smProblog> |
| TweetyProject | 1.31 | argument status | <https://tweetyproject.org/> |
| clingo | 5.6.2 | stable models | <https://potassco.org/clingo/> |
| DLV / I-DLV | 2.1.1 / 1.1.6 | DLV: stable models; I-DLV: grounding used for the D4 reference result | DLV: <https://dlv.demacs.unical.it/>; I-DLV: <https://github.com/DeMaCS-UNICAL/I-DLV> |
| s(CASP) | 1.1.4 | query success and bindings | <https://gitlab.software.imdea.org/ciao-lang/sCASP> |

## How to read the table

Each cell carries a relation prefix classifying how faithful the input is
to the case:

- `N:` native case in the system's own formalism;
- `E:` exact translation on the stated fragment;
- `A:` non-equivalent analogue: the input reproduces selected finite
  outcomes of the case without preserving its construct;
- `U`: no faithful encoding is claimed; the reason is recorded in
  `manifest.json` and `results/table_results.tsv`.

Result notation:

| Notation | Meaning |
|---|---|
| scalar | result for the displayed query |
| x/y | displayed query / explicit opposite query |
| [l,u] | lower / upper probability |
| 0 (ign.) | signed confidence zero with pure ignorance |
| 0 (bal.) | signed confidence zero with balanced positive and negative support |
| (v1,...,vn) | per-binding results of an open query, in the stated binding order |
| {b1,...,bn} | binding set of an open query, without probabilities |
| error | the system's reported error on the stated input |
| grounding timeout | grounding did not complete within the recorded ten-second limit |
| no models | the system reports that the program has no models |
| inc m | smProbLog probability mass on worlds without stable models |
| 2 models | two stable models were returned |
| undec. | TweetyProject constructs opposed arguments and warrants neither conclusion |

Different output kinds are not numerically comparable.

## Main findings

- C1, C2, N1, N2: gk and the numerical probabilistic systems (ProbLog,
  PASTA, plingo, smProbLog) agree on the translated fragment.
- F1: gk and ProbLog return the same probability .576. gk uses
  query-directed non-ground proof search and ProbLog grounds on demand;
  the ground-and-solve systems reach the grounding timeout on this
  program.
- D1–D7: the analogue translations omit recursive exception evaluation
  (D2), premise-level opposition resolution (D3), strict priority (D5),
  or the paired exception operation (D7).
- EQ1: gk combines an uncertain equality with opposed evidence; the
  tested encodings produce an inconsistent world or do not encode the
  input.
- X1: an unrelated contradiction does not affect gk's query proof; the
  ASP-based systems reject the program, renormalize, or report
  inconsistent mass.
- DJ1: gk evaluates a confidence on a classical disjunction at .72; the
  PASTA interval [.72,.80] has that value as its lower bound.

Other native outputs include PASTA probability intervals, smProbLog
inconsistent-world mass, and TweetyProject argument statuses. D4-P tests
the probabilistic stable-model semantics; the gk entry is an analogue.

## Results

Probabilistic cases:

| ID | Case | gk | ProbLog | PASTA | plingo | smProbLog | Tweety | clingo | DLV/I-DLV | s(CASP) |
|---|---|---|---|---|---|---|---|---|---|---|
| C1 | independent causes | N: .80 | E: .80 | E: [.80,.80] | E: .80 | E: .80 | U | U | U | U |
| C2 | conjunctive causes | N: .30 | E: .30 | E: [.30,.30] | E: .30 | E: .30 | U | U | U | U |
| N1 | open join query | N: (.50,.30,.30,.60) | E: (.50,.30,.30,.60) | E: ([.50,.50],[.30,.30],[.30,.30],[.60,.60]) | E: (.50,.30,.30,.60) | E: (.50,.30,.30,.60) | U | A: {aa,ab,ba,bb} | A: {aa,ab,ba,bb} | A: {aa,ab,ba,bb} |
| N2 | open recursive query | N: (.80,.688,.1376) | E: (.80,.688,.1376) | E: ([.80,.80],[.688,.688],[.1376,.1376]) | E: (.80,.688,.1376) | E: (.80,.688,.1376) | U | A: {ann,bob,carl} | A: {ann,bob,carl} | A: {ann,bob,carl} |

Defaults and opposition:

| ID | Case | gk | ProbLog | PASTA | plingo | smProbLog | Tweety | clingo | DLV/I-DLV | s(CASP) |
|---|---|---|---|---|---|---|---|---|---|---|
| D1 | uncertain contrary exception | N: -.80 | A: .10/.90 | A: [.10,.10]/[.90,.90] | A: .10/.90 | A: .10/.90 | U | A: no/yes | A: no/yes | A: no/yes |
| D2 | facts and a default, all with confidences | N: .54 | A: .27 | A: [.27,.27] | A: .27 | A: .27 | U | A: no | A: no | A: no |
| D3 | contested premise | N: 0 (ign.) | A: .225 | A: [.225,.225] | A: .225 | A: .225 | U | A: no | A: no | A: no |
| D4 | Nixon defaults | N: 0 (ign.) | U | N: [0,1]/[0,1] | N: .50/.50 | N: .50/.50 | N: undec./undec. | N: 2 models | N: 2 models | N: yes/yes |
| D4-P | probabilistic Nixon premises | A: +.20/-.20 | U | N: [.32,.80]/[.12,.60] | N: .54054/.40540 | N: .56/.36 | U | U | U | U |
| D5 | strict priority | N: .30 | A: .63/.30 | A: [.63,.63]/[.30,.30] | A: .63/.30 | A: .63/.30 | A: no/yes | A: no/yes | A: no/yes | A: no/yes |
| D6 | undercut vs. rebut | N: undercutting 1; rebutting 1 | A: undercutting 1; rebutting 1 | A: undercutting [1,1]; rebutting [1,1] | A: undercutting 1; rebutting 1 | A: undercutting 1; rebutting 1 | U | A: undercutting yes; rebutting yes | A: undercutting yes; rebutting yes | A: undercutting yes; rebutting yes |
| D7 | paired exception | N: 0 (bal.) | A: .48/.48 | A: [.48,.48]/[.48,.48] | A: .48/.48 | A: .48/.48 | U | U | U | U |

First-order and conflict cases:

| ID | Case | gk | ProbLog | PASTA | plingo | smProbLog | Tweety | clingo | DLV/I-DLV | s(CASP) |
|---|---|---|---|---|---|---|---|---|---|---|
| EQ1 | uncertain equality, opposed evidence | N: .34 | U | A: error | A: .79839 | A: .82, inc .504 | U | A: no models | A: no models | A: no models |
| X1 | unrelated contradiction tolerance | N: 1.0 | U | A: error | A: 1.0 | A: 1.0, inc .42 | U | A: no models | A: no models | A: no models |
| F1 | recursion over function terms | N: .576 | E: .576 | A: grounding timeout | A: grounding timeout | E: grounding timeout | U | A: grounding timeout | A: grounding timeout | A: yes |
| DJ1 | uncertain classical disjunction | N: .72 | U | E: [.72,.80] | E: error | A: .76 | U | A: yes | A: yes | A: yes |

In paired cells the order is displayed query / explicit opposite query.

## Case index

Detailed descriptions, inputs, and per-case commentary are in
[CASES.md](CASES.md).

| ID | Case | gk input | Details |
|---|---|---|---|
| C1 | independent causes | [`inputs/gk/c1.gkp`](inputs/gk/c1.gkp) | [CASES.md](CASES.md#c1-independent-causes) |
| C2 | conjunctive causes | [`inputs/gk/c2.gkp`](inputs/gk/c2.gkp) | [CASES.md](CASES.md#c2-conjunctive-causes) |
| D1 | uncertain contrary exception | [`inputs/gk/d1.gkp`](inputs/gk/d1.gkp) | [CASES.md](CASES.md#d1-uncertain-contrary-exception) |
| D2 | facts and a default, all with confidences | [`inputs/gk/d2.gkp`](inputs/gk/d2.gkp) | [CASES.md](CASES.md#d2-facts-and-a-default-all-with-confidences) |
| D3 | contested premise | [`inputs/gk/d3.gkp`](inputs/gk/d3.gkp) | [CASES.md](CASES.md#d3-contested-premise) |
| D4 | Nixon defaults | [`inputs/gk/d4.gkp`](inputs/gk/d4.gkp) | [CASES.md](CASES.md#d4-nixon-defaults) |
| D4-P | probabilistic Nixon premises | [`inputs/gk/d4sm_pos.gkp`](inputs/gk/d4sm_pos.gkp), [`inputs/gk/d4sm_neg.gkp`](inputs/gk/d4sm_neg.gkp) | [CASES.md](CASES.md#d4-p-probabilistic-nixon-premises) |
| D5 | strict priority | [`inputs/gk/d5.gkp`](inputs/gk/d5.gkp) | [CASES.md](CASES.md#d5-strict-priority) |
| D6 | undercut vs. rebut | [`inputs/gk/d6_undercut.gkp`](inputs/gk/d6_undercut.gkp), [`inputs/gk/d6_rebut.gkp`](inputs/gk/d6_rebut.gkp) | [CASES.md](CASES.md#d6-undercutting-and-rebutting-forms) |
| D7 | paired exception | [`inputs/gk/d7.gkp`](inputs/gk/d7.gkp) | [CASES.md](CASES.md#d7-paired-reference-class-exception) |
| N1 | open join query | [`inputs/gk/n1_study4.gkp`](inputs/gk/n1_study4.gkp) | [CASES.md](CASES.md#n1-open-join-query) |
| N2 | open recursive query | [`inputs/gk/n2_study10.gkp`](inputs/gk/n2_study10.gkp) | [CASES.md](CASES.md#n2-open-recursive-query) |
| EQ1 | uncertain equality, opposed evidence | [`inputs/gk/e1.gkp`](inputs/gk/e1.gkp) | [CASES.md](CASES.md#eq1-uncertain-equality-opposed-evidence) |
| X1 | unrelated contradiction tolerance | [`inputs/gk/x1.gkp`](inputs/gk/x1.gkp) | [CASES.md](CASES.md#x1-unrelated-contradiction-tolerance) |
| F1 | recursion over function terms | [`inputs/gk/f1.gkp`](inputs/gk/f1.gkp) | [CASES.md](CASES.md#f1-recursion-over-function-terms) |
| DJ1 | uncertain classical disjunction | [`inputs/gk/dj1.gkp`](inputs/gk/dj1.gkp) | [CASES.md](CASES.md#dj1-uncertain-classical-disjunction) |

## Reproduction

A gk cell runs with the binary from [`../bin/`](../bin/README.md):

```sh
./bin/gk comparisons/inputs/gk/c1.gkp -detail -outformat json
```

The gk input of each case is listed in the case index. The printed
`confidence` is non-negative: the absolute value of positive support
minus negative support (fields `support_for` and `support_against` in the
`detail` block). The table restores the query-oriented sign. For D1 the
JSON reports `confidence: 0.8` with `answer: false`; the table shows
-.80.

The `run_definitions` of `manifest.json` record every run for which a
command is available, with executable name and relative input path; the
recorded working directory is this folder, and `gk` is the repository
binary `../bin/gk` from here. The versions are in the systems table
above. The TweetyProject and I-DLV entries are capture-only references:
`results/raw/tweety_reference.txt` and `results/raw/idlv_reference.txt`.

## Folder layout

```text
comparisons/
  README.md
  CASES.md               per-case descriptions
  manifest.json          index: cells, run definitions, reference records
  inputs/
    gk/                  gk input of each case
    problog/  pasta/  plingo/  smproblog/  scasp/
                         external probabilistic inputs, one folder per system
    asp/                 shared clingo and DLV inputs
    tweety/  idlv/       TweetyProject and I-DLV inputs
  results/
    table_results.tsv    flat rendering of all 144 table cells
    run_records.json     per-run outcome and capture check
    raw/                 captured stdout and stderr of every run
```

`manifest.json` is the authoritative record: it maps each of the 144
row/system cells to its result, relation classification, input files,
queries, and run identifiers, and defines every run command.
`results/table_results.tsv` is its flat rendering.
`results/run_records.json` records the outcome of each run (completed,
timeout, error, no_models, or captured_reference) and the check that the
capture matches the recorded expectations.

## Related material in this repository

gk's own default and confidence examples are in
[`../Examples/`](../Examples/README.md); separate comparisons on the birds
workload and on first-order clause problems are in
[`../Examples/asp_comparison/`](../Examples/asp_comparison/README.md) and
[`../Examples/fol_comparison/`](../Examples/fol_comparison/README.md); native
TweetyProject, PASTA, and I-DLV inputs with their own commands are in
[`../Examples/system_comparison/`](../Examples/system_comparison/README.md);
the samplers are in [`../montecarlo/`](../montecarlo/README.md).
