# Taxonomy data

Runtime data for GK's taxonomy-based default priorities: a default whose
priority names a more specific class defeats one naming a more general
class (the comparison rules are in the defaults section of
[`../Doc/how_gk_works.md`](../Doc/how_gk_works.md)). Load the data with:

```sh
./bin/gk INPUT -taxonomy -datafolder data
```

`-defaults` is an accepted synonym of `-taxonomy`. Without `-datafolder`,
GK looks for the files in the current working directory. An input that
uses taxonomy-form priorities such as `tax(name)` or `tax(name, nr)`
without loaded tables is an error; numeric priorities never need this
data.

## Files

| File | Contents |
|---|---|
| `gk_name_number.txt` | `name,number` lines mapping WordNet-style synset names (and their bare names before the first dot) to taxonomy numbers |
| `gk_taxonomy_packed.txt` | the packed parent graph over those numbers: one integer per line — total count, class count, one index per class, then per class its parent count and parent indices |

The two files are one generated pair: the numbering is a topological
order assigned at generation time and differs between generation runs, so
the files must always be replaced together. GK validates the pair at load
time and stops with an error on a mismatch. A regenerated pair encodes
the same taxonomy under different numbers; it is interchangeable with
this one only as a pair, never file by file.

Checksums of the shipped pair (sha256):

```text
41b8a37e330820d352c2436365c2d07e02c6d85109929c83d1ab975cdfdabba4  gk_name_number.txt
d206f28565f97007ffaff383626a5a0546ad0d658450f28061826aed9f69fc6b  gk_taxonomy_packed.txt
```

The same pair, byte-identical, is used by the private GK source tree and
by [logictools.org](https://logictools.org/commonsense.html), whose page
downloads gzip-compressed copies, decompresses them, and writes them into
the WebAssembly filesystem before running GK.

## Source and generation

The taxonomy is the WordNet noun hypernym graph, read through the
[NLTK](https://www.nltk.org/) WordNet interface. The builder, written by
Priit Järv, is in [`builder/`](builder/):

| File | Role |
|---|---|
| `wngraph.py` | reads WordNet via NLTK, builds the synset graph, assigns the topological numbering, writes a JSON graph |
| `name_sort_from_graph.py` | emits the `name,number` table from the JSON graph |
| `taxonomy.py` | packs the JSON graph into the integer-array format (`-p` output) |
| `taxonomy.c` | reference C implementation for reading and searching the packed graph |

Regeneration (requires Python 3 with `nltk` and its `wordnet` download):

```sh
python3 data/builder/wngraph.py wn_graph.json
python3 data/builder/name_sort_from_graph.py wn_graph.json > gk_name_number.txt
python3 data/builder/taxonomy.py -p gk_taxonomy_packed.txt wn_graph.json
```

Both output files must then replace the shipped pair together.

WordNet is used under the Princeton WordNet license: WordNet 3.0
Copyright 2006 by Princeton University, all rights reserved; provided
"as is" without representations or warranties. See
<https://wordnet.princeton.edu/license-and-commercial-use>.
