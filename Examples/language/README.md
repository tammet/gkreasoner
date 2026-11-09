# Natural-language reasoning examples

Each file here is a gk encoding of an English reasoning problem. The
[llmpipe commonsense-reasoning system](https://github.com/tammet/nlpsolver/tree/main/llmpipe)
automatically translates English into GK logic and uses GK for proof
search. These files contain clauses produced by that translation. Every example
runs together with the shared background knowledge base
[`axioms_std.js`](axioms_std.js), which supplies general axioms for taxonomy,
part-whole relations, degrees, events, and space.

The separate [nlformtasks collection](https://github.com/tammet/nlformtasks)
contains a larger set of language-translation examples runnable by gk.

The examples cover a range of language constructs: taxonomy, disjunction,
negation, quantifiers, comparison, possession, relative clauses, the passive,
concession, spatial containment, event change, wh-questions, defaults, and
probability words. Each shows gk deriving a yes/no verdict, an "unknown"
result, or a specific value. An input confidence in these files is a
calculation parameter supplied by the translation; it is not by itself a
probability that the sentence is true.

## Running an example

All examples use the same command. From the repository root:

```sh
./bin/gk Examples/language/axioms_std.js Examples/language/taxonomy.js \
  -strategytext '{"strategy": ["negative_pref", "posunitpara"], "query_preference": 1}' \
  -seconds 5 -confidence 0.1 -keepconfidence 0.1 \
  -taxonomy -datafolder data
```

The first file is the background knowledge base; the second is the example.
`-taxonomy -datafolder data` loads the taxonomy data from
[`../../data/`](../../data/README.md): the generated rules carry
taxonomy-form priorities, and the translation pipeline runs GK with the
taxonomy loaded. The same command line is repeated in a comment at the top
of each example file, together with that file's English sentence and
expected answer. Each example finishes in about 3.5 seconds with
`-seconds 5`. With `-seconds 3`, `which_cannot_fly.js` gets no answer: its
line says `the recursion did not run`.

## Reading the answer

gk 1.2.4 prints one line that starts with `{"recursive":`. Its `value`
holds the four shares in the order (for, against, conflict, ignorance).
An example asks either a yes/no question or a wh-question ("who", "which",
"where").

- A yes/no question is named `$defq0` in the line. (1, 0, 0, 0) means
  yes, (0, 1, 0, 0) means no, and (0, 0, 0, 1) means unknown: neither the
  statement nor its negation is derived.
- A wh-question gets an `answers` list with the values found. A value
  written `#:John 1` is a specific individual named in the text ("John"); a
  value written `$some_fox` is an existential one ("a fox"). When no value
  is found, the line says `the recursion did not run` and has no value: the
  "unknown" case of a wh-question.

Two examples:

```sh
./bin/gk Examples/language/axioms_std.js Examples/language/taxonomy.js \
  -strategytext '{"strategy": ["negative_pref", "posunitpara"], "query_preference": 1}' \
  -seconds 5 -confidence 0.1 -keepconfidence 0.1 \
  -taxonomy -datafolder data
```

"Elephants are animals. John is an elephant. John is an animal?" returns
`$defq0` (1, 0, 0, 0): yes.

```sh
./bin/gk Examples/language/axioms_std.js Examples/language/which_cannot_fly.js \
  -strategytext '{"strategy": ["negative_pref", "posunitpara"], "query_preference": 1}' \
  -seconds 5 -confidence 0.1 -keepconfidence 0.1 \
  -taxonomy -datafolder data
```

"Squirrels can fly. Foxes cannot fly. Squirrels and foxes are animals. Which
animal cannot fly?" returns `$defq0($some_fox)` (1, 0, 0, 0): a fox.

## File index

| File | Sentence | Expected | gk 1.2.4 |
|---|---|---|---|
| `taxonomy.js` | Elephants are animals. John is an elephant. John is an animal? | True | (1, 0, 0, 0) |
| `disjunction.js` | Elephants have trunks or tails. John is an elephant. John has no trunk. John has a tail? | True | (0, 0, 0, 1): no proof found; see below |
| `class_exclusion.js` | Elephants are not birds. John is an elephant. John is a bird? | False | (0, 1, 0, 0) |
| `no_information.js` | Elephants are big animals. John is an elephant. Who is nice? | Unknown | no answer |
| `who_question.js` | Elephants are animals. Who is an animal? | `$some_elephant` and `$some_animal` | both, (1, 0, 0, 0) each |
| `confidence.js` | Yellow and green elephants are nice. John is an elephant. John is yellow and green. John is nice? | True, .9 | (.9, 0, 0, .1) |
| `degree.js` | John is somewhat big. John is big? | True | (1, 0, 0, 0) |
| `conditional.js` | John is glad. If John is glad, then Mike is not glad. Is Mike glad? | False | (0, 1, 0, 0) |
| `possession.js` | The roof of John's house is green. John has a house? | True | (1, 0, 0, 0) |
| `universal.js` | John likes all boxers. Mike is a boxer. John likes Mike? | True | (1, 0, 0, 0) |
| `existential.js` | Some elephants are animals. Some elephants are not animals? | Unknown | (0, 0, 0, 1) |
| `comparison.js` | The mountain is higher than the hill. Is the hill higher than the mountain? | False | (0, 1, 0, 0) |
| `relative_clause.js` | John has a car which is nice and red. The red car is nice? | True | (1, 0, 0, 0) |
| `passive.js` | The letter was written by Eve. Eve wrote the letter? | True | (1, 0, 0, 0) |
| `concession.js` | Although John was tired, he finished the work. John finished the work? | True | (1, 0, 0, 0) |
| `spatial_containment.js` | Tallinn is in Estonia. Estonia is not outside Europe. Earth contains Europe. Estonia contains Tartu. Riga is not in Estonia. Riga is in Estonia? | False | (0, 1, 0, 0) |
| `event_change.js` | John stopped smoking. Does John smoke now? | False | (0, 1, 0, 0) |
| `which_cannot_fly.js` | Squirrels can fly. Foxes cannot fly. Squirrels and foxes are animals. Which animal cannot fly? | A fox | `$some_fox`, (1, 0, 0, 0) |
| `which_has_apple.js` | John is a nice man. John has an apple. Mike is a nice man. Greg is a bad man. Mike has a pear. Which man has an apple? | John | `#:John 1`, (1, 0, 0, 0) |
| `penguin_default.js` | Penguins are birds. Penguins do not fly. Birds fly. John is a penguin. John flies? | False | (0, 1, 0, 0) |
| `family_relations.js` | Father/child and grandfather rules over a small family. Who is a grandson of Luke? | Mike or Mickey | Mike and Mickey, (1, 0, 0, 0) each |
| `probability.js` | Tallinn is hardly in Latvia. Tallinn is in Latvia? | False, .6 | (0, .6, 0, .4) |

The recursive method of gk 1.2.4 finds no proof for `disjunction.js`, also
with `-seconds 10`; the direct method (`-direct`) answers it with true and
confidence .9735. Every other example gives the expected answer.

`axioms_std.js` is the shared background knowledge base loaded with every
example; it is not an example itself.

See [`../../Doc/how_gk_works.md`](../../Doc/how_gk_works.md) for how gk
reaches an answer, [`../../Doc/support_semantics.md`](../../Doc/support_semantics.md)
for the meaning of the four shares, and
[`../../Doc/input_languages.md`](../../Doc/input_languages.md) for the
JSON-LD-LOGIC notation these files use.
