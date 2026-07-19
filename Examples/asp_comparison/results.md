# Benchmark provenance

This file records the implementations, commands, and historical sources behind
the tables in [`README.md`](README.md). Wall times are single runs, not
statistical performance measurements.

## Current normalized measurements

The inputs were produced by `make_constants.py` with SHA-256
`fe9a2ba69d02ddf1da9e51c44cc2825ba8b0b5df8c7f1bc37606bd85ffdfb191`.
The 1,000-constant inputs are committed under [`generated/`](generated/). The
2,000- and 100,000-constant inputs were generated in a temporary directory and
deleted after measurement.

The host was an Intel Core i7-10875H with 8 cores, 16 hardware threads, and
30 GiB of memory. The implementations were:

- gk 1.0.0, SHA-256
  `a639b29a8a9578bb8b01cd6b96614f1e93ada7b98fa7f26eec6f058393a716d1`;
- [clingo](https://potassco.org/clingo/) 5.6.2;
- [I-DLV](https://github.com/DeMaCS-UNICAL/I-DLV) 1.1.6, SHA-256
  `4fcf0dd01fae22b82e3b52a4421d3c5c0b2a377486450b6175d30b209ffec32a`;
- the official legacy [DLV](https://www.dlvsystem.it/dlvsite/dlv-download/)
  x86-64 static binary, which does not report a semantic version, SHA-256
  `e26fe0c89c329e68c5cfa7c719e25ad6adab7d07082461a8b47cd3400ee00c11`;
- [s(CASP)](https://swish.swi-prolog.org/example/scasp.swinb) 1.1.4 on
  [SWI-Prolog](https://www.swi-prolog.org/) 9.2.9.

| Constants | gk | clingo | DLV | I-DLV | s(CASP) |
|---:|---|---|---|---|---|
| 1,000 | `true`; 0.32 s; 181,672 KiB | `UNSATISFIABLE`; 10.34 s; 42,472 KiB | cautiously true; 27.80 s; 90,824 KiB | `flies(b1)`; `<0.01 s`; 5,668 KiB | 30 s limit; 716,468 KiB |
| 2,000 | `true`; 0.33 s; 200,904 KiB | `UNSATISFIABLE`; 99.95 s; 146,288 KiB | 180 s limit; 256,108 KiB | `flies(b1)`; `<0.01 s`; 6,180 KiB | 1 GiB stack limit after 27.55 s; 1,337,852 KiB |
| 100,000 | `true`; 4.92 s; 345,548 KiB | 30 s limit; 56,284 KiB | 30 s limit; 962,624 KiB | `flies(b1)`; 0.24 s; 52,172 KiB | 1 GiB stack limit after 19.70 s; 1,635,540 KiB |

`/usr/bin/time` printed `0.00` for the two smaller I-DLV runs; the table records
that at the command's hundredth-of-a-second resolution as `<0.01 s`.

`/usr/bin/time` supplied wall time and maximum resident set size. gk used
`-seconds 1` at 1,000 and 2,000 constants and `-seconds 10` at 100,000.
clingo used `--stats=2`; its completed runs reported 0.00 seconds solving. DLV
used `-cautious`. I-DLV used `--query --silent`, which enabled its Magic Sets
rewriting. External limits were applied with `timeout` as stated in the table
and README.

The s(CASP) 2,000-constant run reported 2,140 stack frames and a possible
non-terminating recursion before reaching the default stack limit. The
100,000-constant run reached the same limit while maintaining a large ordered
set during disequality evaluation. These are the observed failure paths for
the specified runs.

The generator requires [Python 3](https://www.python.org/). Recreate any size
and system syntax with:

```sh
python3 Examples/asp_comparison/make_constants.py SIZE --system SYSTEM \
  --output OUTPUT
```

`SIZE` must be an even integer of at least four. `SYSTEM` is one of `gk`,
`clingo`, `dlv`, `idlv`, or `scasp`.

## Historical source record

The historical table in [`README.md`](README.md) is transcribed from the old
[logictools.org comparison](https://logictools.org/gk/#comparison-with-the-asp-approach).
Its corresponding old inputs remain available at these source links:

- [clingo inputs](https://logictools.org/gk/asp/cbirds.txt), including
  [function symbols](https://logictools.org/gk/asp/cbirds_funsymbs.txt),
  [1k](https://logictools.org/gk/asp/cbirds_1k.txt), and
  [2k](https://logictools.org/gk/asp/cbirds_2k.txt);
- [DLV inputs](https://logictools.org/gk/asp/dbirds.txt), including
  [function symbols](https://logictools.org/gk/asp/dbirds_funsymbs.txt),
  [1k](https://logictools.org/gk/asp/dbirds_1k.txt), and
  [2k](https://logictools.org/gk/asp/dbirds_2k.txt);
- [s(CASP) inputs](https://logictools.org/gk/asp/sbirds.txt), including
  [function symbols](https://logictools.org/gk/asp/sbirds_funsymbs.txt) and
  [transitivity](https://logictools.org/gk/asp/sbirds_trans.txt);
- [gk inputs](https://logictools.org/gk/asp/gbirds.txt), including
  [function symbols](https://logictools.org/gk/asp/gbirds_funsymbs.txt),
  [1k](https://logictools.org/gk/asp/gbirds_1k.txt),
  [2k](https://logictools.org/gk/asp/gbirds_2k.txt), and
  [the file labelled 100k](https://logictools.org/gk/asp/gbirds_100k.txt).

These links support only the historical table. The current normalized results
do not depend on the old files.
