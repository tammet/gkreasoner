# Measurement protocol

This file records the measurement protocol behind the result table in
[`README.md`](README.md). Wall times are single runs; they are not
statistical performance measurements.

The inputs were produced by `make_constants.py`. The 1,000-constant inputs
are committed under [`generated/`](generated/); the 2,000- and
100,000-constant inputs are regenerated on demand.

`/usr/bin/time` supplied wall time and maximum resident set size. gk used
`-seconds 1` at 1,000 and 2,000 constants and `-seconds 10` at 100,000.
clingo used `--stats=2`; its completed runs reported 0.00 seconds solving.
DLV used `-cautious`. I-DLV used `--query --silent`, which enabled its
Magic Sets rewriting. External limits were applied with `timeout` as stated
in the README.

The s(CASP) 2,000-constant run reported 2,140 stack frames and a possible
non-terminating recursion before reaching the default stack limit. The
100,000-constant run reached the same limit while maintaining a large
ordered set during disequality evaluation. These are the observed failure
paths for the specified runs.

The generator requires [Python 3](https://www.python.org/):

```sh
python3 Examples/asp_comparison/make_constants.py SIZE --system SYSTEM \
  --output OUTPUT
```

`SIZE` must be an even integer of at least four. `SYSTEM` is one of `gk`,
`clingo`, `dlv`, `idlv`, or `scasp`.
