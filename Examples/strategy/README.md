# Strategy examples

Strategy files are JSON configuration objects passed with `-strategy`. They
contain no logic and cannot be run as proof problems.

GK normally creates a strategy automatically:

```sh
./bin/gk Examples/exceptions/penguin.gkp
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
./bin/gk Examples/exceptions/penguin.gkp \
  -strategy Examples/strategy/query_focus.json
```

gk answers `flies(b)` with (1, 0, 0, 0) and `flies(p)` with (0, 1, 0, 0), as
with the automatic strategy.

## Negative-clause preference

[`negative_pref.json`](negative_pref.json) selects clauses containing negative
literals. It is a useful baseline for small resolution problems:

```sh
./bin/gk Examples/exceptions/penguin.gkp \
  -strategy Examples/strategy/negative_pref.json
```

This strategy returns the same two answers with the same values.

## Several runs

[`runs.json`](runs.json) attempts three searches in order:

1. one second of unit resolution;
2. four seconds with negative-clause preference;
3. fifteen seconds of query-focused search with weak SINE filtering.

```sh
./bin/gk Examples/exceptions/penguin.gkp \
  -strategy Examples/strategy/runs.json
```

The first run is sufficient for this problem. The answers are those of the
automatic strategy.

## Confidence combination

The key `independence` controls how the direct method (`-direct`) combines
alternative proofs. The recursive method, gk's default, combines the
proofs it finds by the support semantics:
[`../confidences/cumulate.gkp`](../confidences/cumulate.gkp) gives
(.8, 0, 0, .2) also with `"independence": 0`.

[`../../Doc/strategy_reference.md`](../../Doc/strategy_reference.md) lists the
strategy keys. [`../../Doc/how_gk_works.md`](../../Doc/how_gk_works.md)
describes how gk reaches an answer.
