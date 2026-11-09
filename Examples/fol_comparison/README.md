# First-order comparison

These inputs were adapted from the
[GKC](https://github.com/tammet/gkc) example collection. They test the
first-order prover underneath gk's uncertainty and default machinery.

The commands below use `-plain`, which prints a classical proof without
confidences and runs gk's direct method. The recursive method, gk's
default, does not find these proofs: without `-plain -nonegative` it
reports (0, 0, 0, 1) for the three clause problems and no answer for the
planning example.

## Clause problems

| Input | Main first-order features | GK result |
|---|---|---|
| [`nlp_query.p`](nlp_query.p) | non-Horn clauses, equality, disequality, Skolem functions, quantified cardinality axioms | theorem, 33 proof clauses |
| [`dreadbury_safe_query.p`](dreadbury_safe_query.p) | non-Horn clauses, equality, disequality, nested Skolem functions | theorem, 35 proof clauses |
| [`set.p`](set.p) | set-theory clauses, four witness functions, unrestricted term depth | theorem, 74 proof clauses |

## GK commands

NLP:

```sh
./bin/gk Examples/fol_comparison/nlp_query.p \
  -plain -nonegative -firstanswer -seconds 30 -mbsize 1000 \
  -strategytext '{"strategy":["negative_pref","posunitpara"],"query_preference":1}'
```

Dreadbury:

```sh
./bin/gk Examples/fol_comparison/dreadbury_safe_query.p \
  -plain -nonegative -firstanswer -seconds 30 -mbsize 1000 \
  -strategytext '{"strategy":["unit"],"query_preference":1}'
```

Set theory:

```sh
./bin/gk Examples/fol_comparison/set.p \
  -plain -nonegative -firstanswer -seconds 30 -mbsize 1000 \
  -strategytext '{"strategy":["negative_pref","posunitpara"],"query_preference":1}'
```

Five runs of each command with gk 1.2.3, including process startup,
produced:

| Input | Median wall time | Peak resident memory |
|---|---:|---:|
| NLP | 0.03 s | 25.8 MiB |
| Dreadbury | 0.03 s | 23.9 MiB |
| set theory | 0.10 s | 33.1 MiB |

All three runs report confidence 1 in plain mode.

## Results in other reasoners

The translations, commands, resource bounds, and results for
[ProbLog](https://dtai.cs.kuleuven.be/problog/editor.html),
[PASTA](https://github.com/damianoazzolini/pasta),
[TweetyProject](https://tweetyproject.org/),
[clingo](https://potassco.org/clingo/),
[DLV](https://www.dlvsystem.it/dlvsite/dlv/),
[I-DLV](https://github.com/DeMaCS-UNICAL/I-DLV), and
[s(CASP)](https://github.com/JanWielemaker/sCASP) are in
[`other_systems/`](other_systems/README.md). The inputs retain unrestricted
function depth.

## Planning example

[`blocks.gkp`](blocks.gkp) is a blocks-world planning problem with situation
terms, action terms, frame axioms, explicit negative literals, and an
unbounded query variable. GK returns this four-action situation term:

```text
do(putdown(c,b),do(pickup(c),do(putdown(b,a),do(pickup(b),s0))))
```

The command is:

```sh
./bin/gk Examples/fol_comparison/blocks.gkp -plain -nonegative \
  -firstanswer -seconds 30 -mbsize 1000 \
  -strategytext '{"strategy":["hardness_pref"],"weight_select_ratio":100,"query_preference":0}'
```
