# Implemented-system comparison

This directory contains the inputs, command records, cell classifications, and
captured outputs behind the implemented-system comparison table of the gk
uncertainty paper. It does not contain external-system binaries, libraries,
source trees, or harness code.

Related material elsewhere in this repository: gk's own default and confidence
examples are in [`../Examples/`](../Examples/README.md); separate comparisons
on the birds workload and on first-order clause problems are in
[`../Examples/asp_comparison/`](../Examples/asp_comparison/README.md) and
[`../Examples/fol_comparison/`](../Examples/fol_comparison/README.md); native
TweetyProject, PASTA, and I-DLV inputs with their own commands are in
[`../Examples/system_comparison/`](../Examples/system_comparison/README.md);
the samplers are in [`../montecarlo/`](../montecarlo/README.md).

## Package contents

- `manifest.json` maps all 108 row/system cells to the displayed result,
  N/E/A/U classification, input file, query, and run identifier.
- `results/table_results.tsv` is a flat, machine-readable rendering of all
  table cells.
- `results/run_records.json` records each command, exit status, check result,
  and raw-output path.
- `results/raw/` contains the captured stdout and stderr.
- `gk/`, `tweety/`, and `idlv/` contain declarative system-specific inputs; the other
  `.pl` and `.lp` files are the combined external-system inputs.
- `fixtures/` contains the two captured reference outputs used when
  TweetyProject or I-DLV is not rerun.

The experiment uses these systems:

- gk, from this repository;
- ProbLog 2.2.10;
- PASTA 1.0.1;
- plingo 1.1.0;
- smProbLog 2.1.0.42;
- TweetyProject 1.31;
- clingo 5.6.2;
- DLV 2.1.1 and I-DLV 1.1.6;
- s(CASP) 1.1.4.

The exact commands used are data entries in `manifest.json` and
`results/run_records.json`; no installed executable is part of this
directory. The checked run summary is:

```text
{"captured_reference": 2, "pass": 62}
```

## Reproducing

`manifest.json`, `results/run_records.json`, and the captured files under
`results/raw/` retain the commands used, so some commands and `clingo`
grounder messages contain absolute paths from the execution environment. To
re-run from this repository, substitute the repository's own binary and this
directory for those paths. A gk cell can be run as follows:

```sh
./bin/gk implemented_systems/gk/c1.gkp -detail -outformat json
```

and likewise for `c2`, `d1`, `d2`, `d3`, `d4`, `d4sm_pos`, `d4sm_neg`, `d5`,
`d6_undercut`, `d6_rebut`, `d7`, `n1_study4`, and `n2_study10`. These inputs
reproduce their recorded table cells with the gk 1.0.8 binary in
[`../bin/`](../bin/README.md); the signed
confidence displayed in the table is `support_for - support_against` from the
`detail` block.

The external-system cells need the corresponding system installed. Take the
command from its `run_records.json` entry and replace the input path with the
matching file in this directory — for example
`problog implemented_systems/problog_cases.pl`, or
`clingo implemented_systems/asp_cases.lp 0`. Versions are listed above; other
versions may return different results. The two `fixtures/` files are used in
place of a rerun for TweetyProject and I-DLV, which need a Java or C++ toolchain
rather than a single executable.

## Interpretation

N is a native case in the selected formalism, E an exact translation on the
stated fragment, A a non-equivalent analogue, and U a cell for which no
faithful encoding is claimed. U is not a missing run. Each U cell has its
reason in `manifest.json` and `results/table_results.tsv`.

The analogue inputs make only the following finite comparisons:

- D1 compiles the simple exception to negation as failure.
- D2 contains weighted facts and a weighted default. Its external analogues
  use independent probabilistic activation and a crisp blocker.
- D3 adds a negation-as-failure guard to the contested positive premise.
- D5 compiles the higher-ranked activation into a guard on the lower-ranked
  conclusion; the Tweety case uses specificity.
- D6 gives both rules the same unopposed negation-as-failure form, so it does
  not expose the undercut/rebut distinction.
- D7 states the paired residual branch as rules over the source probabilities;
  it does not provide a native paired-reference-class operator.

Within paired result cells, the order is positive query / explicit opposite
query. In D6 it is arbitrary-exception input / contrary-exception input. The
s(CASP) D4 `yes/yes` result means that the two queries succeed in separate
partial stable models.

D4-P has probabilistic Nixon premises and unweighted default rules. PASTA,
plingo, and smProbLog evaluate the probabilistic stable-model input natively;
the gk entry is an equal-priority contrary-exception analogue. In D6, `1/1`
is the numeric result pair. Undercut and rebut name the blocker roles, not
output values.

## Non-ground cases

N1 is Study 4. Its open query `twobirds(X,Y)` returns the ordered
per-binding vector

```text
(a,a): .50   (a,b): .30   (b,a): .30   (b,b): .60
```

N2 is Study 10. Its open recursive query `smokes(X)` returns

```text
ann: .80   bob: .688   carl: .1376
```

gk, ProbLog, PASTA, plingo, and smProbLog agree on these per-binding
probabilities. The clingo, DLV, and s(CASP) analogues return the corresponding
binding sets without probabilities. The concrete inputs and captured outputs
are indexed by `manifest.json` and `results/table_results.tsv`.
