# Input Languages

GK reads four notations and converts them to the same internal clause
representation. This document describes the common forms through examples; it
is not a formal grammar.

| Notation | Suffixes | Description |
|---|---|---|
| GKP | `.gkp`, `.pl`, `.pro`, `.prolog` | Prolog-style surface notation |
| JSON-LD-LOGIC | `.js` | Native JSON representation |
| GKS | `.gks` | Premise-to-consequence notation |
| TPTP CNF | `.p`, `.ax`, `.tptp`, `.cnf` | TPTP clauses with GK annotations |

Use `-informat json`, `prolog`, `simple`, or `tptp` to override automatic
detection. `-writejson` prints the converted JSON-LD-LOGIC input without
running the prover.

## GKP

GKP is intended for hand-written examples. It uses Prolog notation for terms
and rules, a [ProbLog](https://dtai.cs.kuleuven.be/problog/editor.html)-style
confidence prefix, and `unless` for exceptions.

### Facts and negation

```prolog
bird(robin).
0.95::bird(tweety).
-bird(airplane).
```

An omitted confidence means 1. GKP confidences are decimals from 0 to 1. A
leading `-` or `~` is classical negation: `-bird(airplane)` is evidence for the
negative literal, not a failure to prove the positive literal.

### Rules

```prolog
bird(X) :- penguin(X).
0.9::flies(X) :- bird(X), healthy(X).
```

The rule head is on the left of `:-`; the body contains comma-separated
conditions. Variables begin with an uppercase letter. Lowercase identifiers
are constants or predicate and function names.

A rule without a head is a constraint:

```prolog
:- penguin(X), flies(X).
```

A semicolon separates alternative conclusions:

```prolog
male(X) ; female(X) :- person(X).
```

### Queries

```prolog
query(flies(tweety)).
query(flies(X)).
query(-flies(tux)).
```

A ground query asks for a truth assessment. A query containing variables asks
for substitutions. A normal proof task contains one query.

### Defaults

`unless` adds a blocker to a rule:

```prolog
flies(X) :- bird(X), unless(-flies(X), 2).
```

This reads: derive `flies(X)` from `bird(X)` unless a priority-2 argument for
`-flies(X)` blocks the derivation.

Competing defaults can use different numeric priorities:

```prolog
flies(X)  :- bird(X),   unless(-flies(X), 3).
-flies(X) :- object(X), unless(flies(X), 2).
```

A taxonomy can supply the priority:

```prolog
0.8::isa(X, bird) :- has_part(X, feathers),
                     unless(-isa(X, bird), tax(bird)).
```

Taxonomy priorities require `-defaults` and the auxiliary files
`gk_name_number.txt` and `gk_taxonomy_packed.txt`. `tax(name, N)` supplies a
numeric fallback. An `unless` expression without a priority is incomparable
with explicitly ordered defaults.

### Equality and arithmetic

```prolog
f(a) = g(b).
a != b.
few(P) :- apples(P, N), N < 5.
johnhad(X) :- X + 2 = 10.
```

Comparisons are `<`, `>`, `=<`, and `>=`. Arithmetic expressions use `+`, `-`,
`*`, and `/`. Ground expressions are evaluated directly. Finding numeric
values for variables requires the bounded arithmetic strategy described in
[`../Examples/arithmetic/README.md`](../Examples/arithmetic/README.md).

### Names, roles, includes, and comments

```prolog
normal_birds_fly: 0.9::flies(X) :- bird(X), unless(-flies(X), 2).
route(a, b) [role(assumption)].
:- include("taxonomy.gkp").

% line comment
/* block comment */
```

Statement names appear in provenance. Roles affect clause queues and proof
labels. Included paths are resolved by the input loader.

GKP does not provide Prolog execution features such as cut, `is`, dynamic
assertion, or negation as failure. Use an explicit negative literal or an
`unless` blocker instead of `not` or `\+`.

## JSON-LD-LOGIC

JSON-LD-LOGIC is GK's native input and output representation. Files may contain
JSON comments. A variable is a string beginning with `?:`.

```jsonc
[
  ["bird", "robin"],
  {"@logic": ["bird", "tweety"], "@confidence": 0.95},
  {"@logic": [["bird", "?:X"], "=>", ["flies", "?:X"]]},
  {"@question": ["flies", "?:X"]}
]
```

The implication may also be written directly as a clause. Negated body
literals and a positive head form a disjunction:

```jsonc
{"@logic": [["-bird", "?:X"], ["flies", "?:X"]]}
```

The principal correspondences are:

| Construct | GKP | JSON-LD-LOGIC |
|---|---|---|
| Fact | `bird(tweety).` | `["bird", "tweety"]` |
| Negative fact | `-bird(a).` | `["-bird", "a"]` |
| Variable | `X` | `"?:X"` |
| Confidence | `0.9::bird(a).` | `{"@logic":["bird","a"], "@confidence":0.9}` |
| Rule | `flies(X) :- bird(X).` | `{"@logic":[["bird","?:X"],"=>",["flies","?:X"]]}` |
| Query | `query(flies(X)).` | `{"@question":["flies","?:X"]}` |

JSON confidences may be decimals from 0 to 1 or integer percentages from 2 to
100. Thus `"@confidence": 90` means `0.9`.

A blocker is a clause literal using `$block`. The negative exception in the
GKP rule below is represented by `$not`:

```prolog
flies(X) :- bird(X), unless(-flies(X), 2).
```

```jsonc
{"@logic": [
  ["-bird", "?:X"],
  ["flies", "?:X"],
  ["$block", 2, ["$not", ["flies", "?:X"]]]
]}
```

The example files use predicate arrays of this form. JSON-LD-LOGIC also
supports graph-oriented objects, but those are not needed for the introductory
examples.

## GKS

GKS places premises before `=>` and joins them with `&`:

```text
bird(robin).
0.8 :: penguin(tux).
penguin(X) => bird(X).
bird(X) & healthy(X) => flies(X).
bird(X) & unless(-flies(X), 2) => flies(X).
query(flies(X)).
```

`|` separates alternative conclusions. GKS is useful for short rule sets; GKP
provides statement names and annotation lists when those are required.
GKS uses `%` and `/* ... */` comments, as in GKP.

## TPTP

GK accepts TPTP clause normal form (CNF). Ordinary TPTP clauses require no
GK-specific syntax:

```tptp
cnf(bird_tux, axiom, bird(tux)).
cnf(birds_fly, axiom, (~bird(X) | flies(X))).
cnf(question, negated_conjecture, ~flies(tux)).
```

Confidence and blocker information can be carried in the annotation field:

```tptp
cnf(birds_fly, axiom, (~bird(X) | flies(X)),,
    [confidence(0.9), unless(~flies(X), 2)]).
```

TPTP input uses the plain TPTP/SZS-oriented result format by default. Use
`-outformat json` when JSON output is required.

TPTP `fof(...)` input is recognized but rejected with an instruction to
clausify it first. The current GK surface accepts `cnf(...)` problems only.

## Equivalent default rule

The following fragments express the same default rule.

GKP:

```prolog
0.9::flies(X) :- bird(X), unless(-flies(X), 2).
```

GKS:

```text
0.9 :: bird(X) & unless(-flies(X), 2) => flies(X).
```

JSON-LD-LOGIC:

```jsonc
{"@logic": [
  ["-bird", "?:X"],
  ["flies", "?:X"],
  ["$block", 2, ["$not", ["flies", "?:X"]]]
], "@confidence": 0.9}
```

TPTP:

```tptp
cnf(birds_fly, axiom, (~bird(X) | flies(X)),,
    [confidence(0.9), unless(~flies(X), 2)]).
```

See [`how_gk_works.md`](how_gk_works.md) for the interpretation of confidence
and blockers, and [`cli_reference.md`](cli_reference.md) for format-selection
options.
