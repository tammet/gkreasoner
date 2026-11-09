JSON-LD-LOGIC Input Format
==========================

JSON-LD-LOGIC is the primary input format for GK. It embeds logical
formulas in JSON, with optional semantic web compatibility via JSON-LD keys.

Files typically use the `.js` extension and are valid JSON with the
addition of C-style comments (`//` line comments and `/* ... */` block comments).

See also https://github.com/tammet/json-ld-logic for the format proposal.


File Structure
--------------

A GK input file is a JSON array of statements. Each statement is either:

  * A bare formula (JSON array): treated as an axiom with confidence 1.0
  * An annotated formula (JSON object): has metadata keys like `@logic`,
    `@confidence`, `@question`, etc.

Example:

    [
      // bare fact
      ["bird","tweety"],

      // annotated rule with confidence
      {"@logic": [["bird","?:X"], "=>", ["flies","?:X"]],
       "@confidence": 0.9},

      // question
      {"@question": ["flies","tweety"]}
    ]


Top-Level JSON Keys
--------------------

### Formula keys

  * **`@logic`** (array): The logical formula content. Required unless
    `@question` is used.

  * **`@question`** (array): Marks the formula as a question/goal to prove.
    Shorthand for `{"@logic": ..., "@role": "question"}`.

    The question may be a single literal or a quantifier-free compound
    formula (conjunction, disjunction, implication, equivalence). A
    compound question F is answered through an automatic definition
    (2026-07-16, `implementation/records/MEMO_query_formulas.md`): gk adds the certain axiom
    `$question(vars) <=> F` over F's free variables and asks
    `$question(vars)` — so the answer is exactly what an explicit
    hand-written definition of the same formula gives, the free variables
    become the reported bindings, and a ground compound question yields a
    true/false verdict. The `$question_def` axiom appears honestly in the
    printed proofs. Quantified questions (`exists`/`forall`) are rejected
    at load.

### Metadata keys

  * **`@confidence`** (number): Confidence value for the statement.
    - Float 0.0 to 1.0: direct confidence (e.g., `0.85`)
    - Integer 0 to 100: percentage (e.g., `85` means 0.85, and `1` means 0.01)
    - A numeric zero (`0` or `0.0`) marks an inert statement: gk discards it
      when it loads the input, as it discards a statement below
      `-keepconfidence`. A string, a negative number, a float above 1 and an
      integer above 100 are load errors.
    - Default: 1.0 (certain)

  * **`@name`** (string): Name identifier for the clause, used in
    proof output.

  * **`@role`** (string): Role of the statement in the problem. Values:
    - `"axiom"`: background knowledge (default if no role specified)
    - `"extaxiom"`: external axiom (from included files)
    - `"assumption"`: assumed true for this problem
    - `"hypothesis"`: hypothesis to test
    - `"conjecture"`: goal to prove (negated internally)
    - `"negated_conjecture"`: already-negated goal
    - `"question"`: question to answer (like conjecture but may seek
      variable bindings)

### Structural keys (JSON-LD compatibility)

  * **`@context`**: JSON-LD context for URI expansion
  * **`@graph`**: Contains a list of nested formula objects
  * **`@id`**: Identifier for JSON-LD objects
  * **`@type`**: Type annotation
  * **`@list`**: Marks a list structure
  * **`@set`**: Marks a set structure
  * **`@base`**: Base URI for relative references

### Include and similarity keys

  * **`@include`** (string): Path to a file to include. The file is parsed
    and its contents added to the problem. Searched in: current directory,
    `$TPTP` environment variable path, `/opt/TPTP/`.

  * **`@similarity`**: Similarity declarations for word-level matching.

### Shared-threshold-worlds declaration keys (active in the DEFAULT mode)

These load-time declarations are recognized whenever the shared-threshold-worlds
mechanism is active — which, since 2026-07-12, is gk's DEFAULT (no flag
needed; explicit `-defworlds` is accepted). They are silently ignored only
in the modes that disable the mechanism: `-legacy olduncertainty`, `-plain`, and
plain `-clausify`. Both are validated at load time — a violation is a load
**error** (the run aborts with a JSON `{"error": ...}`), not a warning.

  * **`@report`** (boolean, on a **fact**): declares the fact to be an independent
    calibrated report about its statement. Same-polarity reports about one ground
    atom are pooled by the odds product at load (e.g. `0.8` and `0.7` → `0.903`),
    rather than the noisy-or used for undeclared facts. The fact may be positive or
    negative (`["-bird","a"]`) — opposite-polarity reports are not pooled together;
    they enter the two polarities and are resolved against each other normally.
    The clause must be a **ground unit**;
    `@report` on a multi-literal rule, or on a non-ground fact, is a load error.

        {"@logic": ["bird","a"], "@confidence": 80, "@report": true}

  * **`@marginal`** (`[rho, pexc]`, on a **rule with a blocker**): declares that the
    rule's stated strength `PR` was measured on a population that included blocked
    cases, with blocking rate `rho` and exception strength `pexc`. The load-time
    rewrite reconstructs the exception-free strength
    `p0 = (PR − pexc·rho) / (1 − rho)`. Requires `0 < rho < 1` and
    `0 <= pexc <= 1`; a rule without a blocker, or out-of-range arguments,
    is a load error.

    **CLAMP CAVEAT (read before relying on `@marginal`):** if the declared
    triple implies a `p0` outside `[0,1]` (an incoherent PR/rho/pexc
    combination), the current loader CLAMPS `p0` into range with a warning —
    it does not reject the input, and the report carries no flag. A clamped
    declaration breaks the calibration identity the key promises (blocking
    at exactly rate `rho` no longer reproduces `PR`). Whether such triples
    should instead be rejected at load, or the clamp surfaced in the answer,
    is an open design decision; until
    it is settled, treat a clamped `@marginal` as a declaration error on the
    author's side.

        {"@logic": [["-bird","?:X"], ["flies","?:X"], ["$block", 1, ["penguin","?:X"]]],
         "@confidence": 50, "@marginal": [0.5, 0.1]}


Correspondence with the GKP surface
-----------------------------------

The same statements in the Prolog-style GKP notation and in JSON-LD-LOGIC.
The other surfaces and the full spec of all three are in `input_languages.md`.

| Construct | GKP | JSON-LD-LOGIC |
|---|---|---|
| Fact | `bird(tweety).` | `["bird", "tweety"]` |
| Negative fact | `-bird(a).` | `["-bird", "a"]` |
| Variable | `X` | `"?:X"` |
| Confidence | `0.9::bird(a).` | `{"@logic":["bird","a"], "@confidence":0.9}` |
| Rule | `flies(X) :- bird(X).` | `{"@logic":[["bird","?:X"],"=>",["flies","?:X"]]}` |
| Query | `query(flies(X)).` | `{"@question":["flies","?:X"]}` |
| Blocker | `flies(X) :- bird(X), unless(-flies(X), 2).` | `{"@logic":[["-bird","?:X"],["flies","?:X"],["$block",2,["$not",["flies","?:X"]]]]}` |

A confidence in `@confidence` may be a decimal from 0 to 1 or an integer
percentage from 0 to 100, so `"@confidence": 90` means 0.9. A statement with
no confidence has confidence 1, and an explicit `1.0` means the same. A
statement with confidence `0` or `0.0` is discarded at load: an application
with probability 0 never applies, and gk does not keep it in the knowledge
base, so that it cannot take part in the paired exception construction.

A taxonomy-form priority replaces the blocker's number with a `$` term:
`["$", "bird"]` is the JSON spelling of `tax(bird)` and `["$", "bird", 1]` of
`tax(bird, 1)`, as in `../Examples/exceptions/penguin3.js`.


Formulas
--------

Formulas are encoded as JSON arrays. The encoding depends on the
logical structure:

### Atoms (atomic formulas)

An atom is a JSON array with a predicate name followed by arguments:

    ["bird","tweety"]              // bird(tweety)
    ["father","john","pete"]       // father(john, pete)
    ["p"]                          // p (propositional)

Three conventions govern atoms and clauses:

  * An atom with no arguments is a one-element array everywhere it occurs:
    the fact `["raining"]`, the question `["raining"]`.
  * A clause is an array of literal arrays, so `[["-raining"], ["wet"]]` is
    `-raining | wet`. An array that starts with a string is a predicate
    application instead, so `["-raining", "wet"]` is the single atom
    `-raining(wet)`.
  * A bare string such as `"raining"` is also accepted as a fact, but it does
    not match the array form of the same name; one file must not mix the two
    spellings. The GKP and GKS converters produce the array form
    consistently.

### Negated atoms

Prefix the predicate name with `-`:

    ["-bird","tweety"]             // not bird(tweety)
    ["-flies","?:X"]               // not flies(X)

### Rules (implications)

Use `=>` as an infix operator in a three-element array:

    [["bird","?:X"], "=>", ["flies","?:X"]]

This is equivalent to the clause `["-bird","?:X"], ["flies","?:X"]`.

Reverse implication:

    [["flies","?:X"], "<=", ["bird","?:X"]]

### Biconditionals

    [["p","?:X"], "<=>", ["q","?:X"]]

### Disjunctions (OR)

A clause (disjunction of literals) is a JSON array of arrays:

    [["-bird","?:X"], ["flies","?:X"]]

This means: `not bird(X) OR flies(X)`.

Explicit OR operator:

    [["p","a"], "|", ["q","b"]]

### Conjunctions (AND)

    [["p","?:X"], "&", ["q","?:X"]]

### Negation

Prefix operators `not`, `~`, or `-` negate a formula:

    ["not", ["flies","?:X"]]
    ["~", ["flies","?:X"]]
    ["-", ["flies","?:X"]]

### Quantifiers

Explicit quantifiers (usually unnecessary since free variables are
implicitly universally quantified in clauses):

    ["forall", ["?:X","?:Y"], [["father","?:X","?:Y"], "=>", ["parent","?:X","?:Y"]]]
    ["exists", ["?:X"], ["bird","?:X"]]

A single quantified variable may also be written without the list:

    ["exists", "?:X", ["bird","?:X"]]

which is read as `["exists", ["?:X"], ["bird","?:X"]]`. A constant in the
variable position is an error, since it would bind nothing.

### Conditional (if-then)

    ["if", ["bird","?:X"], "then", ["flies","?:X"]]

With multiple conditions and consequences:

    ["if", ["bird","?:X"], ["small","?:X"], "then", ["canary","?:X"]]


Variables
---------

Variables are strings prefixed with `?:`:

    "?:X"       "?:Y"       "?:Name"       "?:Thing1"

Free variables in a clause are implicitly universally quantified.

Blank nodes (JSON-LD style) use `_:` prefix: `"_:node1"`.


Special Predicates
------------------

### $ans - Answer collection

The `$ans` predicate marks which variable bindings to report:

    ["-bird","?:X"], ["$ans","?:X"]

This asks "what X is a bird?" and reports the bindings found.

In annotated form:

    {"@question": ["-bird","?:X"], "$ans": ["?:X"]}

### $block - Default rule exceptions

Used in default (defeasible) rules to mark exception conditions:

    [["-bird","?:X"], ["flies","?:X"],
     ["$block", strength, ["$not", ["flies","?:X"]]]]

The `$block` literal says: this rule can be overridden if a stronger
rule proves the blocked literal.

**Strength** is the first argument of `$block`:

  * Integer `0`: incomparable with all other blockers
  * Integer `>0`: larger numbers are stronger/more specific
  * `["$", class_number]`: taxonomy-based, using class number
  * `["$", "word"]`: taxonomy-based, word is converted to class number
    via `gk_name_number.txt`
  * `["$", class_or_word, integer]`: combined; uses taxonomy for
    comparison with other taxonomy blockers, integer for comparison
    with integer-only blockers

Blockers with equal strength block each other mutually
(unless strength is 0).

### $not - Negation in blockers

`$not` is used **only** inside `$block` literals to negate the
blocked conclusion:

    ["$block", 1, ["$not", ["flies","?:X"]]]

means "this rule is blocked if flies(X) can be disproved."

    ["$block", 1, ["flies","?:X"]]

means "this rule is blocked if flies(X) can be proved."

### $arc and $narc - RDF triples

For semantic web / RDF data:

    ["$arc", subject, predicate, object]        // unnamed triple
    ["$narc", subject, predicate, object, id]   // named triple

### List operations

  * `["$list", head, tail]`: cons operation
  * `$first`: first element of a list
  * `$rest`: rest of a list (tail)
  * `$nil`: empty list
  * `$is_list`: test if argument is a list

Lists can also be written in bracket notation: `[1, 2, 3]` within terms.

### Arithmetic predicates

  * `$less`, `$greater`, `$lessorequal`, `$greaterorequal`: comparison
  * `$sum`, `$product`, `$difference`, `$quotient`, `$remainder`: operations
  * `$floor`, `$ceiling`, `$round`, `$truncate`: rounding
  * `$is_int`, `$is_real`, `$is_number`: type tests

Infix shorthand: `+`, `-`, `*`, `/` in terms.

### String predicates

  * `$is_distinct`: test if argument is a string (distinct symbol)
  * `$strlen`: string length
  * `$substr`: substring extraction
  * `$substrat`: character at position

### Equality

    ["=", "a", "b"]         // a equals b
    ["!=", "a", "b"]        // a does not equal b

Infix in terms: `["p", ["f","a"], "=", ["f","b"]]`


Logical Operators Summary
--------------------------

| Operator    | Meaning               | Position   |
|-------------|-----------------------|------------|
| `=>`        | Implication           | Infix      |
| `<=>`       | Biconditional         | Infix      |
| `<=`        | Reverse implication   | Infix      |
| `<~>`       | Negated equivalence   | Infix      |
| `&`, `and`  | Conjunction           | Infix      |
| `\|`, `or`  | Disjunction           | Infix      |
| `~\|`       | Negated disjunction   | Infix      |
| `~&`        | Negated conjunction   | Infix      |
| `not`,`~`,`-`| Negation             | Prefix     |
| `=`         | Equality              | Infix      |
| `!=`,`-=`,`~=`| Inequality          | Infix      |
| `forall`    | Universal quantifier  | Prefix     |
| `exists`    | Existential quantifier| Prefix     |
| `if...then` | Conditional           | Keyword    |


Comments
--------

GK's JSON parser supports C-style comments:

    // This is a line comment

    /* This is a
       block comment */

These are extensions to standard JSON, enabled by the YAJL parser.


Distinct Symbols (Strings)
----------------------------

Strings in double quotes are treated as distinct symbols (constants
that are unequal to all other distinct symbols):

    ["name", "\"John Smith\""]

The backslash-escaped quotes are needed because the value is inside
a JSON string.


Complete Example
-----------------

A file combining facts, rules, defaults, and a question:

    [
      // Facts with confidence
      {"@logic": ["bird","tweety"], "@confidence": 0.95},
      {"@logic": ["bird","polly"], "@confidence": 0.9},
      {"@logic": ["penguin","tux"], "@confidence": 0.99},

      // Penguins are birds
      [["penguin","?:X"], "=>", ["bird","?:X"]],

      // Default: birds fly (strength 1)
      {"@logic": [["-bird","?:X"], ["flies","?:X"],
                   ["$block", 1, ["$not", ["flies","?:X"]]]]},

      // Exception: penguins don't fly (strength 2, overrides birds)
      {"@logic": [["-penguin","?:X"], ["-flies","?:X"],
                   ["$block", 2, ["flies","?:X"]]]},

      // Question: what flies?
      {"@question": ["-flies","?:X"], "$ans": ["?:X"]}
    ]

Running:

    ./bin/gk example.js -taxonomy

Expected output: tweety and polly fly (with their respective confidences),
but tux does not fly (the penguin exception overrides the bird default).
