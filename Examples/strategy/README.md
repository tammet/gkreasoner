# Strategy examples

Strategy files are JSON configuration objects passed with `-strategy`. They
contain no logic and cannot be run as proof problems.

GK normally creates a strategy automatically:

```sh
./bin/gk Examples/core/grandfather.gkp
```

The supplied files demonstrate the two main explicit selection styles and a
sequence of runs.

## Query-focused search

[`query_focus.json`](query_focus.json) contains:

```json
{
  "max_seconds": 10,
  "strategy": ["query_focus"],
  "query_preference": 1,
  "max_distinct_answers": 10
}
```

`query_preference: 1` preserves the goal, assumption, and axiom queues;
`query_focus` gives preference to the goal queue.

```sh
./bin/gk Examples/core/grandfather.gkp \
  -strategy Examples/strategy/query_focus.json
```

Expected result: `mark`, confidence `0.684`.

## Negative-clause preference

[`negative_pref.json`](negative_pref.json) selects clauses containing negative
literals. It is a useful baseline for small resolution problems:

```sh
./bin/gk Examples/core/grandfather.gkp \
  -strategy Examples/strategy/negative_pref.json
```

This example also returns `mark` with confidence `0.684`. Strategy differences
usually become visible as differences in search time or clause count, not in
the answer to a small problem.

## Several runs

[`runs.json`](runs.json) attempts three searches in order:

1. one second of unit resolution;
2. four seconds with negative-clause preference;
3. fifteen seconds of query-focused search with weak SINE filtering.

```sh
./bin/gk Examples/core/grandfather.gkp \
  -strategy Examples/strategy/runs.json
```

The first run is sufficient for the grandfather problem. On a harder problem,
later runs broaden the search.

## Confidence combination

The current combiner reconstructs evidence-instance sets and measures overlap
between proofs. Strategy value `independence: 0` disables cumulation; nonzero
values enable the normal combiner. Intermediate percentages affect results
only with the compatibility option `-oldcumulate`.

[`../../Doc/strategy_reference.md`](../../Doc/strategy_reference.md) lists the
strategy keys. [`../../Doc/how_gk_works.md`](../../Doc/how_gk_works.md)
describes proof combination.
