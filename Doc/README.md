# Documentation

| File | Subject |
|---|---|
| [`support_semantics.md`](support_semantics.md) | What the four shares of an answer mean: the support semantics, on examples, and its rules stated precisely |
| [`how_gk_works.md`](how_gk_works.md) | How gk reaches an answer with the recursive method, gk's default since 1.2.0 |
| [`recursive_output.md`](recursive_output.md) | The output of the recursive method: the options `-direct`, `-recursive` and `-audit`, the `{"recursive": ...}` line, the readings and the status facts |
| [`mcref.md`](mcref.md) | The reference tool `mcref`, which computes the support semantics by sampling, and its comparison with gk |
| [`input_languages.md`](input_languages.md) | The four input notations, described through examples |
| [`json_ld_logic.md`](json_ld_logic.md) | The JSON-LD-LOGIC format: syntax, annotations, questions, `$block`, `@report` and `@marginal` |
| [`cli_reference.md`](cli_reference.md) | Command-line invocation and options |
| [`strategy_reference.md`](strategy_reference.md) | Automatic search, multi-run strategies and strategy keys |
| [`comparison_with_other_systems.md`](comparison_with_other_systems.md) | Comparison of outputs and supported cases with external reasoners |
| [`direct_method.md`](direct_method.md) | The direct method of gk 1.1.2, which `gk -direct` runs |

Suggested reading order: [`how_gk_works.md`](how_gk_works.md),
[`support_semantics.md`](support_semantics.md),
[`input_languages.md`](input_languages.md),
[`recursive_output.md`](recursive_output.md), then
[`cli_reference.md`](cli_reference.md) and
[`strategy_reference.md`](strategy_reference.md).

When two documents seem to disagree about the meaning of the four shares,
[`support_semantics.md`](support_semantics.md) decides.

The runnable tutorial is in [`../Examples/README.md`](../Examples/README.md).
The reference tool is in [`../mcref/`](../mcref/README.md). Installation,
repository contents and the papers are described in the
[top-level README](../README.md).
