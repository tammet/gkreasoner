# O5: what each system can state (the earlier comparison table)

Section 7.4 of the paper and the row "five common-class cases" of the families tables (families reached)
use the earlier comparison table of this repository: 16 cases, each
stated in gk and in the languages of nine other systems. The table, its
inputs, every command, the classification of each cell and the raw
captures of every run are in [`../../comparisons/`](../../comparisons/README.md).
This part adds only the run lists of gk 1.2.5 and of the reference tool
on the table's 18 gk inputs, so that the run store holds these runs too.
The runs read the inputs in place, in `comparisons/inputs/gk/`; no file
of `comparisons/` was changed.

## Rerun

From the repository root:

```sh
./bin/gk comparisons/inputs/gk/e1.gkp
python3 mcref/mcref.py comparisons/inputs/gk/c1.gkp --samples 100000 --seed 1
python3 paper2026/check_gk.py --part O5 --mcref
comparisons/check_gk_cells.sh
```

The last command compares gk's output on the 18 inputs with the captures
in `comparisons/results/raw/`.

## Results

`results.tsv` has one gk row per input, with the four shares that
`comparisons/README.md` prints, and one mcref row per input with the
tool's estimate at 100,000 worlds and seed 1.

- gk 1.2.5 prints the table's four shares on all 18 inputs. The two
  values that Section 7.4 of the paper quotes are among them: EQ1, an
  uncertain equality with opposed evidence, gives (.396, .056, .504, .044)
  for `p(a)`, and F1, a recursive rule over function terms, gives .576 for
  `bird(f(f(a)))`.
- The reference tool accepts 16 of the 18 inputs; it declines EQ1 for
  equality and F1 for function symbols. On the 16, each of the 84 shares
  it estimates lies within e = .00504 of gk's share, the bound for
  100,000 worlds; the largest difference is .0043 (N1, `twobirds(b,b)`).
- On N1 and N2, the questions with variables, gk answers for each
  binding: four and three answers. gk lists `twobirds(b,b)` first; the
  tool lists it last.

The table's other cells, for ProbLog, PASTA, plingo, smProbLog,
TweetyProject, clingo, DLV, I-DLV and s(CASP), keep their recorded runs;
`comparisons/manifest.json` gives each command and
`comparisons/results/table_results.tsv` each result.
