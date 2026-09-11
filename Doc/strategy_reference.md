# Strategy Reference

A strategy controls proof search: clause selection, inference restrictions,
resource limits, and answer limits. It does not change the input logic.

## Automatic strategy

When neither `-strategy` nor `-strategytext` is given, GK constructs a strategy
sequence from the parsed problem. Each strategy has an initial time in which to
find a proof. A strategy that finds none is stopped at that limit. The first
successful strategy receives the remaining search time and is then used for
the query's blocker checks and searches for explicit negation.

The first strategy depends on the problem size: negative-clause preference for
small problems and query-focused selection for large ones. Alternatives use
the other selection method, unit restriction, query focus with SINE filtering
for larger axiom sets, and hardness preference. By default the first strategy
gets half of the search budget before it is abandoned without a proof; the
alternatives share the rest. With `-explore`, or automatically when `-seconds`
exceeds 30, every strategy gets the same short initial limit.

Use an explicit strategy when the search configuration must remain fixed.

`-parallel <n>` uses `n` total processes (1 to 8, Unix) for automatic
selection. The default is 1, with no parallel search. If several strategies
succeed, GK uses the first one in the order above. Explicit strategies disable
parallel search.

```sh
gk Examples/exceptions/penguin.gkp
```

### Running the ladder in parallel

With `-parallel N` (2 to 8) the ladder's alternative strategies run as N−1
probe processes concurrently with the in-process champion instead of one after
another. A probe reports only whether its strategy proved the query; no proofs
cross the process boundary. If the champion proves the query, the probes are
killed and the output is identical to the sequential run. If the champion
gives up, the parent replays — in ladder order — the first strategy a probe
proved, so which strategy's answer is reported never depends on process
timing. Only wall-clock latency changes: a query the champion cannot solve
reaches the winning strategy without first spending the champion's and the
earlier entries' give-up times in sequence.

This applies only to the automatic ladder; an explicit `-strategy` or
`-strategytext` turns it off. It works with `-usekb`. Probes are absent on
Windows and in the WebAssembly build.

## Multi-run strategies

A strategy object may contain a `runs` array. Each element is a complete or
partial strategy. GK tries the runs in order and stops when a run answers the
query. Top-level values act as defaults for the individual runs.

```json
{
  "total_seconds": 20,
  "runs": [
    {"max_seconds": 1, "strategy": ["unit"],
     "query_preference": 0},
    {"max_seconds": 4, "strategy": ["negative_pref"],
     "query_preference": 1},
    {"max_seconds": 15, "strategy": ["query_focus"],
     "query_preference": 1, "sine": 1}
  ]
}
```

```sh
gk Examples/exceptions/penguin.gkp \
  -strategy Examples/strategy/runs.json
```

Short restricted searches belong first; broader searches belong later. A
restricted run such as unit resolution is incomplete, so failure in one run
does not imply that the problem has no proof.

## Single-run strategies

A single-run file is one JSON object:

```json
{
  "max_seconds": 10,
  "strategy": ["query_focus"],
  "query_preference": 1,
  "max_distinct_answers": 10
}
```

Pass the file with `-strategy`:

```sh
gk Examples/exceptions/penguin.gkp \
  -strategy Examples/strategy/query_focus.json
```

The same object can be supplied inline:

```sh
gk Examples/exceptions/penguin.gkp \
  -strategytext '{"strategy":["query_focus"],"query_preference":1}'
```

Strategy files contain configuration only; running one as a logic problem
produces a missing-question error.

## Time limits

### `max_seconds`

Maximum time for one run, in seconds. The command-line `-seconds` value is used
by the automatic strategy.

### `total_seconds`

Maximum cumulative time across all runs.

### `max_dseconds`

Maximum runtime in deciseconds. A value below 20 triggers the strong
unit-cutoff optimisation.

### `giveup_dseconds`

No-proof give-up limit for one run, in tenths of a second. The run ends at
this limit only while it has proved nothing; once any proof is found, the run
continues under the ordinary limits, collecting further proofs and answers.
The automatic strategy sequence uses this key. It can also be used in
hand-written multi-run strategies.

## Answer and proof limits

### `max_answers`

Maximum number of stored proofs in total. Several proofs of one answer each
count. The automatic strategy commonly sets this to 10.

### `max_total_proofs`

Synonym for `max_answers`.

### `max_distinct_answers`

Stop after this many distinct answer substitutions have been found. This
corresponds to command-line `-maxanswers`.

### `max_proofs`

Retain at most this many proofs per distinct answer. This corresponds to
command-line `-maxproofs` and does not stop search by itself.

## Selection methods

The `strategy` value is a string or an array of strings. Array entries enable
several compatible preferences.

```json
{"strategy": ["query_focus", "positive_pref"]}
```

| Name | Effect |
|---|---|
| `negative_pref` | Prefer clauses containing negative literals |
| `positive_pref` | Prefer clauses containing positive literals |
| `query_focus` | Prefer clauses in the query/goal queues |
| `hardness_pref` | Prefer clauses whose literals are estimated cheap to resolve away; the estimate uses literal size, new variables, and the number of complementary-polarity occurrences of the predicate |
| `knuthbendix_pref` | Use a Knuth-Bendix-oriented preference for equational problems |
| `hyper` | Enable hyperresolution |
| `unit` | Restrict resolution arguments to unit clauses |
| `double` | Allow resolution arguments of length at most 2 |
| `triple` | Allow resolution arguments of length at most 3 |

`unit`, `double`, and `triple` impose inference restrictions and can make the
search incomplete.

## Query and clause queues

Clauses have goal, assumption, or axiom roles. `query_preference` (integer
0 to 4; default 0) determines how those roles map to selection queues:

| Value | Treatment |
|---:|---|
| `0` | Put all clauses in one queue |
| `1` | Keep the queues as marked by their roles |
| `2` | Move positive goal units and non-included axioms to the assumption queue |
| `3` | Keep only fully negative goal clauses in the goal queue |
| `4` | Treat all clauses as axioms regardless of role |

`query_focus` is the selection method that gives direct preference to the goal
queue.

### `weight_select_ratio`

Integer, 1 or greater; default 5. Ratio of priority-queue picks to
simple-order picks when the given clause is selected from a queue. The
accepted synonym is `given_queue_ratio`.

### `reverse_clauselist`

Integer, 0 or 1. Reverse the initial clause list without sorting, for
non-query problems.

## Clause roles and strategy

Each input clause carries a role assigned by the `@role` key, or inferred from
`@question`. The role influences proof search only through queue placement in
the given-clause loop:

- goal roles (`conjecture`, `negated_conjecture`, `question`) go to the GOAL
  queue;
- assumption roles (`assumption`, `hypothesis`) go to the ASSUMPTIONS queue;
- axiom roles (`axiom`, `extaxiom`) go to the AXIOMS queue;
- derived clauses with mixed parents go to a mixed queue matching the
  highest-priority parent class.

Whether the queues are actually kept separate depends on `query_preference`,
as tabulated above.

### Role semantics

How `@role` and `@question` interact at parse time; the input format itself
is described in [`input_languages.md`](input_languages.md).

- `@question` and `@role` are mutually exclusive in the same object, enforced
  by the parser rather than by convention.
- `@question` is macro-expanded to `@role: "question"` plus
  `@logic: <formula>`.
- `@role: "question"` is internally rewritten to `negated_conjecture`: the
  formula is negated automatically, and free variables are wrapped in
  `$ans(...)` for answer collection.
- `conjecture` and `negated_conjecture` share one internal role number; they
  differ only in whether the parser negates the formula. `conjecture` is
  negated, `negated_conjecture` is taken as it stands.
- `hypothesis` and `assumption` are indistinguishable internally.
- Role affects search only when the active strategy reads queue position, that
  is `query_focus` or any nonzero `query_preference`.

### `axiom` versus `extaxiom`

`extaxiom` marks an imported or background axiom. A clause gets the extaxiom
role in two ways: by an explicit `@role: "extaxiom"`, or by `@role: "axiom"`
(or no role) when the clause comes from an included file, in which case the
parser prefixes its `@name` with `$inc_` and upgrades the role. In practice
this happens for clauses loaded through the shared-memory KB (`-readkb` /
`-usekb`), not for a plain `./gk file.js` run.

The two roles share storage, weighting, indexing, SINE filtering and
confidence handling. They also collapse to the same derived-clause role,
`FROMAXIOM`, after the first inference: the extaxiom marker does not propagate
to children.

The one behavioural difference during search is in initial clause activation
under `query_preference: 2`. Normal `axiom` clauses are suppressed from
initial activation and pushed back into the regular selection queue, while
`extaxiom` clauses are always initially activated. This is the "trust the
background library more than the problem axioms" hook: with a large imported
KB and `query_preference: 2` in effect, the library's clauses are activated
immediately while the problem's own axioms are held back. Under
`query_preference` 0, 1, 3 or 4 there is no behavioural difference.

Proof output preserves the label, so the distinction stays useful for
provenance even where it has no operational effect.

## Derived-clause limits

Each key takes an integer, 0 or greater; 0 disables the corresponding
limit, and 0 is the default.

| Key | Limit |
|---|---|
| `max_size` | number of literals in a retained clause |
| `max_depth` | term nesting depth in a retained clause |
| `max_length` | number of arguments (the length) of a term in a retained clause |
| `max_weight` | calculated clause weight |

Restrictive values reduce memory use but may remove all proofs of an answer.

## Clause weighting

These keys control how clause weight is calculated, and therefore which
clauses are selected first.

| Key | Effect |
|---|---|
| `depth_penalty` | weight penalty per unit of term depth |
| `length_penalty` | weight penalty per unit of term length |
| `var_weight` | weight assigned to each variable occurrence |
| `repeat_var_weight` | additional weight for repeated variable occurrences |

### Planning terms counted as one constant

Five more keys make a whole term or literal weigh as much as one ordinary
constant (10) instead of the sum over its content. They are meant for
situation-calculus planning inputs, where the action history, the context term
and the blocker literals grow with the plan length without saying how general
the clause is. The three flags are 0 by default and `weight_const_funs` is
empty; with them off the weight function returns exactly the numbers it
returned before the keys existed.

| Key | Effect when 1 |
|---|---|
| `weight_action_const` | a term whose function symbol is `$do`, or is named in `weight_const_funs`, contributes 10 |
| `weight_const_funs` | array of function-symbol names read by the previous key, for example `["move","take","put_on"]`; empty by default |
| `weight_blocker_const` | 1: every nonlogical literal (`$ans`, `$block`, `$simblk`) in a rule clause contributes 10.  2: the blockers only — the same test, but an `$ans` literal keeps its full weight.  A unit clause keeps its weight of 1 either way |
| `weight_ctxt_const` | a term whose function symbol is `$ctxt` contributes 10 |
| `weight_plan_const` | shorthand: sets the three flags above to the given value |

Value 2 of `weight_blocker_const` exists because the `$ans` literal behaves
differently from a blocker.  Giving `$ans` the weight of one constant makes
the search keep clauses with many more variables, and on a plain
situation-calculus input that has no blockers at all it can drive the clause
builder into its renamed-variable limit.

Only the weight changes. The size, depth and length of the clause, the
variable marking that gives a repeated variable its higher weight, and every
keep-limit that reads size, depth or length stay as they are. Subsumption
does not read the weight and is unaffected.

Example:

```json
{"strategy": ["query_focus"], "query_preference": 1, "equality": 0,
 "weight_select_ratio": 20,
 "weight_blocker_const": 2, "weight_ctxt_const": 1}
```

## Equality and relevance filtering

### `equality`

Use `1` to enable equality reasoning and paramodulation, or `0` to disable it.
The automatic strategy enables it when required by the input.

### `rewrite`

Use `1` to rewrite terms with oriented equalities, or `0` to disable rewriting.

### `sine`

Apply SINE relevance filtering to the initial axioms:

| Value | Meaning |
|---:|---|
| `0` | no SINE filtering |
| `1` | weak filtering |
| `2` | strong filtering |

SINE is mainly useful for a small query against a large axiom set.

## Advanced search methods

| Key | Effect |
|---|---|
| `instgen` | integer 0 or 1; use the instantiation-based generation method |
| `propgen` | integer 0 or 1; use propositional generation with SAT-solver integration |

## Confidence-related keys

### `independence`

Integer, 0 to 100. In the provenance-aware retained-proof calculation, `0`
disables the combination of alternative proofs and any nonzero value
enables it; the overlap is measured from activation-event sets. With
`-oldcumulate`, the percentage scales the dependency-ratio discounting of
that option's noisy-or calculation.

### `keepconfidence`

Minimum confidence for retained derived clauses, as an integer percentage from
0 to 100.

### `cumulate_method`

Integer, 0 to 10, selecting how confidences of alternative proofs combine:

| Value | Method |
|---:|---|
| `0` | independence only, not ratios (old machinery) |
| `1` | list-membership percentage (old machinery) |
| `2` | probabilities ratio (old machinery) |
| `4` | per-instance event combination (the default) |

Setting 0 to 2 explicitly selects the old machinery, the same effect as the
command-line `-oldcumulate`. Setting 4, or leaving the field absent, selects
the default: one probabilistic event per ground instance of an uncertain input
clause, reconstructed from each proof by post-search replay, combined across
proofs by bounded inclusion-exclusion over the measured shared instances.

### `exact_cumulate`

Integer, 0 or 1. Explicit override of the method choice: `1` selects the
default per-instance method, `0` the old heuristic.

### `raw_proofs`

Set to `1` for raw-proof collection. The command-line form is `-rawproofs`.

## Arithmetic instantiation

### `arith_instantiation`

| Value | Meaning |
|---:|---|
| `0` | disabled |
| `1` | conservative one-variable instantiation |
| `2` | extended mode, including selected two-variable conditions |

The arithmetic README gives complete commands and examples. Additional
`arith_inst_*` limit keys exist for controlled experiments, but the three modes
above are the stable public interface.

### Limit keys

| Key | Range | Meaning and defaults |
|---|---|---|
| `arith_inst_max_vars` | 1-2 | explicit maximum variables in an instance; default 1 in mode 1, 2 in mode 2 |
| `arith_inst_candidate_limit` | 1-32 | ranked numeric candidates retained for one selected clause; default 4 in mode 1, 6 in mode 2 |
| `arith_inst_probe_limit` | 1-1024 | trial substitutions for one selected clause; default 16 in mode 1, 32 in mode 2 |
| `arith_inst_keep_limit` | 1-64 | calculator-progressing instances retained from one selected clause; default 2 in mode 1, 4 in mode 2 |
| `arith_inst_depth_limit` | 1-16 | consecutive arithmetic-instance ancestry; default 1 in mode 1, 2 in mode 2 |
| `arith_inst_global_limit` | 1-1000000 | attempted probes during one prover run; default 1000. Nested default and negative-evidence searches get their own run-local budget |

Candidates come from numeric constants, comparison boundaries and neighbours,
simple inverse equality hints, and the small fallback set `-1, 0, 1`. They are
deduplicated and must enable real calculator progress. The mode is intended
for compact exercises such as `X + 2 = 10`, not for broad integer enumeration.
Diagnostics are printed to stderr for enabled runs. Worked inputs are in
[`../Examples/arithmetic/`](../Examples/arithmetic/).

## Output control

| Key | Effect |
|---|---|
| `print` | integer 0 or 1; enable basic printout |
| `print_level` | integer 0 or greater; verbosity |
| `print_json` | integer 0 or 1; JSON output |
| `print_tptp` | integer 0 or 1; TPTP output |

`print_level` defaults to **15 inside a strategy file**, which differs from the
command-line default of `-print 10`. A strategy file that sets no
`print_level` therefore prints slightly more than a plain run; set it
explicitly when byte-comparable output matters.

## Default strategy

When no strategy file is given, GK selects a strategy from an analysis of the
input clauses. Use `-print 13` to see the automatically constructed strategy.
The automatic strategy may change in future versions.

For JSON-LD-LOGIC input, the typical gk case:

- `max_answers`: 10, or 1 with `-firstanswer`;
- `independence`: 100;
- `max_seconds`: the value of `-seconds`, default 10;
- selection by clause count: above 1000 clauses
  `"strategy": ["query_focus"], "query_preference": 1`, otherwise
  `"strategy": ["negative_pref"], "query_preference": 1`.

For TPTP input, classical theorem proving, the automatic strategy uses
`negative_pref` with no clause size limits and constructs a multi-run strategy
trying various combinations of strategies, queue ratios and clause limits.

When the automatic strategy is not used — for instance a strategy file was
given but contains no strategy key — the hardcoded fallback is:

```json
{"print": 1, "print_level": 15, "strategy": "negative_pref"}
```

## Supplied strategy files

| File | Contents |
|---|---|
| [`query_focus.json`](../Examples/strategy/query_focus.json) | query-focused single run |
| [`negative_pref.json`](../Examples/strategy/negative_pref.json) | negative-clause-preference single run |
| [`runs.json`](../Examples/strategy/runs.json) | three runs from restricted to broader search |

The files are described and exercised in
[`../Examples/strategy/README.md`](../Examples/strategy/README.md).

## Tips

- Small problems: `"strategy": ["unit"]` is fast but incomplete.
- Query answering: `"strategy": ["query_focus"]` with `"query_preference": 1`.
- Equational reasoning: add `"equality": 1` and
  `"strategy": ["knuthbendix_pref"]`.
- Large knowledge bases: use SINE filtering with `"sine": 1` or `2`.
- Finding multiple answers: set `"max_answers": 10` and increase
  `"max_seconds"`.
- Old-cumulation problems: adjust `"independence"` to how independent the
  evidence sources are.
