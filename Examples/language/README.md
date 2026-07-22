# Natural-language reasoning examples

Each file here is a gk encoding of an English reasoning problem. The
[llmpipe commonsense-reasoning system](https://github.com/tammet/nlpsolver/tree/main/llmpipe)
automatically translates English into gk logic and uses gk as its reasoning
engine. These files contain clauses produced by that pipeline. Every example
runs together with the shared background knowledge base
[`axioms_std.js`](axioms_std.js), which supplies general axioms for taxonomy,
part-whole relations, degrees, events, and space.

The separate [nlformtasks collection](https://github.com/tammet/nlformtasks)
contains a larger set of language-translation examples runnable by gk.

The examples cover a range of language constructs: taxonomy, disjunction,
negation, quantifiers, comparison, possession, relative clauses, the passive,
concession, spatial containment, event change, wh-questions, defaults, and
probability words. Each shows gk deriving a yes/no verdict, an "unknown"
result, or a specific value.

## Running an example

All examples use the same command. From the repository root:

```sh
./bin/gk Examples/language/axioms_std.js Examples/language/taxonomy.js \
  -strategytext '{"strategy": ["negative_pref", "posunitpara"], "query_preference": 1}' \
  -seconds 3 -confidence 0.1 -keepconfidence 0.1
```

The first file is the background knowledge base; the second is the example. The
same command line is repeated in a comment at the top of each example file,
together with that file's English sentence and expected answer.

## Reading the answer

An example asks either a yes/no question or a wh-question ("who", "which",
"where").

- A yes/no question returns `answer: true` or `answer: false`. When neither the
  statement nor its negation can be derived, the result is `no information` or
  `no answers found` — the "unknown" cases.
- A wh-question returns the value found, wrapped in `$ans`. A value written
  `#:John 1` is a specific individual named in the text ("John"); a value
  written `$some_fox` is an existential one ("a fox").

Two examples:

```sh
./bin/gk Examples/language/axioms_std.js Examples/language/taxonomy.js \
  -strategytext '{"strategy": ["negative_pref", "posunitpara"], "query_preference": 1}' \
  -seconds 3 -confidence 0.1 -keepconfidence 0.1
```

"Elephants are animals. John is an elephant. John is an animal?" returns
`answer: true`.

```sh
./bin/gk Examples/language/axioms_std.js Examples/language/which_cannot_fly.js \
  -strategytext '{"strategy": ["negative_pref", "posunitpara"], "query_preference": 1}' \
  -seconds 3 -confidence 0.1 -keepconfidence 0.1
```

"Squirrels can fly. Foxes cannot fly. Squirrels and foxes are animals. Which
animal cannot fly?" returns `$ans($some_fox)` — a fox.

## File index

| File | Sentence | Expected |
|---|---|---|
| `taxonomy.js` | Elephants are animals. John is an elephant. John is an animal? | True |
| `disjunction.js` | Elephants have trunks or tails. John is an elephant. John has no trunk. John has a tail? | True |
| `class_exclusion.js` | Elephants are not birds. John is an elephant. John is a bird? | False |
| `no_information.js` | Elephants are big animals. John is an elephant. Who is nice? | Unknown |
| `who_question.js` | Elephants are animals. Who is an animal? | `$some_elephant` and `$some_animal` |
| `confidence.js` | Yellow and green elephants are nice. John is an elephant. John is yellow and green. John is nice? | Probably true |
| `degree.js` | John is somewhat big. John is big? | True |
| `conditional.js` | John is glad. If John is glad, then Mike is not glad. Is Mike glad? | False |
| `possession.js` | The roof of John's house is green. John has a house? | True |
| `universal.js` | John likes all boxers. Mike is a boxer. John likes Mike? | True |
| `existential.js` | Some elephants are animals. Some elephants are not animals? | Unknown |
| `comparison.js` | The mountain is higher than the hill. Is the hill higher than the mountain? | False |
| `relative_clause.js` | John has a car which is nice and red. The red car is nice? | True |
| `passive.js` | The letter was written by Eve. Eve wrote the letter? | True |
| `concession.js` | Although John was tired, he finished the work. John finished the work? | True |
| `spatial_containment.js` | Tallinn is in Estonia. Estonia is not outside Europe. Earth contains Europe. Estonia contains Tartu. Riga is not in Estonia. Riga is in Estonia? | False |
| `event_change.js` | John stopped smoking. Does John smoke now? | False |
| `which_cannot_fly.js` | Squirrels can fly. Foxes cannot fly. Squirrels and foxes are animals. Which animal cannot fly? | A fox |
| `which_has_apple.js` | John is a nice man. John has an apple. Mike is a nice man. Greg is a bad man. Mike has a pear. Which man has an apple? | John |
| `penguin_default.js` | Penguins are birds. Penguins do not fly. Birds fly. John is a penguin. John flies? | False |
| `family_relations.js` | Father/child and grandfather rules over a small family. Who is a grandson of Luke? | Mike or Mickey |
| `probability.js` | Tallinn is hardly in Latvia. Tallinn is in Latvia? | Likely false |

`axioms_std.js` is the shared background knowledge base loaded with every
example; it is not an example itself.

See [`../../Doc/how_gk_works.md`](../../Doc/how_gk_works.md) for the reasoning
and uncertainty-support model, and
[`../../Doc/input_languages.md`](../../Doc/input_languages.md) for the
JSON-LD-LOGIC notation these files use.
