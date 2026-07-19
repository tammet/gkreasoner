# Normalized 1,000-constant inputs

These five files contain the same two 500-node father chains and the same
rules, expressed in each system's syntax. They are generated fixtures, not the
slightly different inputs used for the historical timing table.

The external systems represented are
[clingo](https://potassco.org/clingo/),
[DLV](https://www.dlvsystem.it/dlvsite/dlv/),
[I-DLV](https://github.com/DeMaCS-UNICAL/I-DLV), and
[s(CASP)](https://swish.swi-prolog.org/example/scasp.swinb).

Regenerate them with [Python 3](https://www.python.org/) from the repository
root:

```sh
python3 Examples/asp_comparison/make_constants.py 1000 --system gk \
  --output Examples/asp_comparison/generated/gbirds_1000.js
python3 Examples/asp_comparison/make_constants.py 1000 --system clingo \
  --output Examples/asp_comparison/generated/clingo_birds_1000.lp
python3 Examples/asp_comparison/make_constants.py 1000 --system dlv \
  --output Examples/asp_comparison/generated/dlv_birds_1000.dlv
python3 Examples/asp_comparison/make_constants.py 1000 --system idlv \
  --output Examples/asp_comparison/generated/idlv_birds_1000.lp
python3 Examples/asp_comparison/make_constants.py 1000 --system scasp \
  --output Examples/asp_comparison/generated/scasp_birds_1000.pl
```

The clingo file uses a final constraint to test `flies(b1)`, so
`UNSATISFIABLE` is the successful result. The DLV and s(CASP) files use their
query syntax. The I-DLV variant represents the explicit exception with a
separate `nonflies` predicate. The gk file contains an `@question` object.
