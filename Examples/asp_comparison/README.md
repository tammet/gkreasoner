# Birds benchmark: gk and ASP systems

This directory contains a bird/penguin example, two recursion variants, and a
generator for a normalized scaling workload. The committed generated inputs
contain 1,000 constants. The same generator was used to measure 2,000- and
100,000-constant inputs; those larger generated files are not kept in the
repository.

The examples compare query-directed first-order proof search with grounded and
query-directed Answer Set Programming (ASP). They measure query focus, not
general performance.

## Basic problem

`b1` is a bird. `p1` is a penguin, penguins are birds, and penguins do not fly.
The default says that a bird flies unless its failure to fly can be established.
The query is `flies(b1)`.

The gk clause for the default is:

```json
[["-bird","?:X"], ["flies","?:X"],
 ["$block",3,["$not",["flies","?:X"]]]]
```

The corresponding ASP rule is:

```prolog
flies(X) :- bird(X), not -flies(X).
```

All four systems establish the expected result on the basic input. The
[clingo](https://potassco.org/clingo/) file tests the query by adding the
constraint `:- flies(b1).`; its successful result is therefore
`UNSATISFIABLE`, meaning that no counterexample stable model exists.
[DLV](https://www.dlvsystem.it/dlvsite/dlv/) is run in cautious-query mode.
[s(CASP)](https://swish.swi-prolog.org/example/scasp.swinb) and gk query
`flies(b1)` directly.

## Systems represented here

- clingo and DLV ground these finite inputs before stable-model evaluation.
- [I-DLV](https://github.com/DeMaCS-UNICAL/I-DLV) evaluates stratified
  programs directly and uses Magic Sets when answering a supplied query; it
  can also act as a grounder for a separate stable-model solver.
- s(CASP) searches from the query without grounding the complete program first.
- gk performs first-order proof search for the query and checks the default's
  blocker separately.

The descriptions and measurements below apply only to the named versions,
inputs, commands, and limits.

## Normalized scaling workload

For a requested even number `N`, `make_constants.py` creates two father chains
containing exactly `N` named constants in total. Each system receives the same
facts and rules in its own syntax, including:

```prolog
anc(X,Y) :- father(X,Y).
anc(X,Y) :- anc(X,Z), anc(Z,Y).
```

The transitive closure has quadratically many ancestor pairs. The derivation of
`flies(b1)` does not use them. The benchmark records whether a system evaluates
the closure before answering the query.

## Current normalized results

These are single runs on an Intel Core i7-10875H with 8 cores, 16 hardware
threads, and 30 GiB of memory. Wall time and maximum resident set size came from
`/usr/bin/time`. The implementations were:

- gk 1.0.0, SHA-256
  `a639b29a8a9578bb8b01cd6b96614f1e93ada7b98fa7f26eec6f058393a716d1`;
- clingo 5.6.2;
- I-DLV 1.1.6, SHA-256
  `4fcf0dd01fae22b82e3b52a4421d3c5c0b2a377486450b6175d30b209ffec32a`;
- the official legacy DLV x86-64 static download, which does not report a
  semantic version, SHA-256
  `e26fe0c89c329e68c5cfa7c719e25ad6adab7d07082461a8b47cd3400ee00c11`;
- s(CASP) 1.1.4 on [SWI-Prolog](https://www.swi-prolog.org/) 9.2.9.

| Constants | gk | clingo | DLV | I-DLV | s(CASP) |
|---:|---|---|---|---|---|
| 1,000 | `true`; 0.32 s; 181,672 KiB | `UNSATISFIABLE`; 10.34 s; 42,472 KiB | cautiously true; 27.80 s; 90,824 KiB | `flies(b1)`; `<0.01 s`; 5,668 KiB | 30 s limit; 716,468 KiB |
| 2,000 | `true`; 0.33 s; 200,904 KiB | `UNSATISFIABLE`; 99.95 s; 146,288 KiB | 180 s limit; 256,108 KiB | `flies(b1)`; `<0.01 s`; 6,180 KiB | 1 GiB stack limit after 27.55 s; 1,337,852 KiB |
| 100,000 | `true`; 4.92 s; 345,548 KiB | 30 s limit; 56,284 KiB | 30 s limit; 962,624 KiB | `flies(b1)`; 0.24 s; 52,172 KiB | 1 GiB stack limit after 19.70 s; 1,635,540 KiB |

`/usr/bin/time` printed `0.00` for the two smaller I-DLV runs; the table records
that at the command's hundredth-of-a-second resolution as `<0.01 s`.

For gk, the search limits were one second for the two smaller inputs and ten
seconds for the largest input; all three returned an answer within their
limits. The 100,000-constant clingo and DLV runs had 30-second external limits.
DLV had a 180-second external limit at 2,000 constants. All s(CASP) runs had a
30-second external limit; the two larger runs reached SWI-Prolog's default
stack limit first.

A limit records that the stated command did not return an answer within the
given resource bound. It does not establish nontermination.

clingo reported 0.00 seconds solving for both completed inputs. Its measured
time was spent reading and grounding. DLV also materializes the closure before
answering its cautious query. I-DLV's Magic Sets rewriting restricts evaluation
to the supplied query, so it does not materialize the ancestor closure, which
is not needed for the query. The I-DLV input uses `nonflies` as the explicit
exception predicate; for this program it has the same role as the
strong-negated `-flies` predicate in the other ASP files. gk likewise did not
materialize the closure. s(CASP) avoids complete grounding, but this
left-recursive encoding still leads it into deep recursive search.

## Historical results

The following table is transcribed from the old
[logictools.org comparison](https://logictools.org/gk/#comparison-with-the-asp-approach).
The source described the machine only as a laptop with a 10th-generation Intel
Core i7 and did not record a timeout or run protocol. These figures are kept
only as historical observations for the old versions and inputs.

| Published input label | clingo 5.4.0 | DLV 2.1.1 | s(CASP) 0.21.10.09 | gk |
|---|---:|---:|---:|---:|
| basic birds | succeeded | succeeded | succeeded | succeeded |
| function symbols | did not finish | did not finish | did not finish | 0.4 s |
| small transitivity input | not recorded | not recorded | did not finish | not recorded |
| 1k input | 8 s | 7 s | not recorded | 0.3 s |
| 2k input | 1 min 40 s | 1 min | not recorded | 0.3 s |
| 100k input | not recorded | not recorded | not recorded | 5 s |

The old large inputs were related but not identical:

- The clingo and DLV 1k/2k files contain two father chains with 1,000 or
  2,000 named constants. Some propagation rules are commented out in the
  clingo files.
- The gk files contain both propagation rules and a function-symbol rule. The
  files labelled 1k and 2k contain 1,002 and 2,002 named constants because each
  chain has one extra endpoint.
- The gk file labelled 100k contains 100,000 links in each of two chains, or
  200,002 named constants.

Those figures are not a controlled comparison. Links to the old inputs are
kept with the historical record in [`results.md`](results.md), rather than used
as dependencies for the current benchmark.

## Function-symbol variant

The two rules below generate `f(b1)`, `f(f(b1))`, and so on:

```prolog
bird(f(X)) :- bird(X).
penguin(f(X)) :- penguin(X).
```

For clingo and DLV, positive recursion through `f` requires an infinite ground
program. Their old runs did not finish. s(CASP) avoids full grounding, but its
old run on this recursive program also did not finish. This does not mean that
s(CASP) rejects function terms in general.

gk can prove `flies(b1)` directly from `bird(b1)` and the default clause. It
does not need to enumerate terms generated by the unrelated recursion.

## Files

| File | Contents |
|---|---|
| `gbirds.js` | basic gk input |
| `gbirds_funsymbs.js` | gk function-symbol input |
| `gbirds_trans.js` | older gk transitivity input, including a function rule |
| `gbirds_trans_scasp.js` | gk translation of the small s(CASP) transitivity input |
| `other_systems/` | retained clingo, DLV, and s(CASP) basic and recursion inputs |
| `generated/` | normalized 1,000-constant input in all five syntaxes |
| `make_constants.py` | normalized two-chain generator in all five syntaxes |
| `results.md` | detailed provenance and historical source links |

## Reproducing the normalized runs

The generator requires [Python 3](https://www.python.org/). From the repository
root, generate a size and syntax explicitly:

```sh
python3 Examples/asp_comparison/make_constants.py 2000 --system gk \
  --output /tmp/gbirds_2000.js
python3 Examples/asp_comparison/make_constants.py 2000 --system clingo \
  --output /tmp/clingo_birds_2000.lp
python3 Examples/asp_comparison/make_constants.py 2000 --system dlv \
  --output /tmp/dlv_birds_2000.dlv
python3 Examples/asp_comparison/make_constants.py 2000 --system idlv \
  --output /tmp/idlv_birds_2000.lp
python3 Examples/asp_comparison/make_constants.py 2000 --system scasp \
  --output /tmp/scasp_birds_2000.pl
```

Command forms used for the measurements were:

```sh
/usr/bin/time -f 'WALL_SECONDS=%e MAX_RSS_KB=%M' \
  ./bin/gk /tmp/gbirds_2000.js -seconds 1
/usr/bin/time -f 'WALL_SECONDS=%e MAX_RSS_KB=%M' \
  clingo /tmp/clingo_birds_2000.lp --stats=2
/usr/bin/time -f 'WALL_SECONDS=%e MAX_RSS_KB=%M' \
  timeout 180s dlv -cautious /tmp/dlv_birds_2000.dlv
/usr/bin/time -f 'WALL_SECONDS=%e MAX_RSS_KB=%M' \
  idlv --query --silent /tmp/idlv_birds_2000.lp
/usr/bin/time -f 'WALL_SECONDS=%e MAX_RSS_KB=%M' \
  timeout 30s scasp -s 1 /tmp/scasp_birds_2000.pl
```

The exact official DLV binary used above is available from the
[DLV download page](https://www.dlvsystem.it/dlvsite/dlv-download/). The larger
generated files and captured outputs used for this update were deleted after
the results were recorded. The I-DLV executable is available from its
[release page](https://github.com/DeMaCS-UNICAL/I-DLV/releases/tag/1.1.6).

A broader semantic comparison with probabilistic logic programming and ASP is
in [`../../Doc/comparison_with_other_systems.md`](../../Doc/comparison_with_other_systems.md).
