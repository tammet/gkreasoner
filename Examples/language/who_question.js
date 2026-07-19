// Elephants are animals. Who is an animal?
// Expected answer: An elephant
// Uses the shared background knowledge base axioms_std.js.
// Run from the repository root:
//   ./bin/gk Examples/language/axioms_std.js Examples/language/who_question.js \
//     -strategytext '{"strategy": ["negative_pref", "posunitpara"], "query_preference": 1}' \
//     -seconds 3 -confidence 0.1 -keepconfidence 0.1
[
{"@name": "sent_S1", "@logic": [["-isa", "elephant", "?:X"], ["isa", "animal", "?:X"]], "@nl": "Elephants are animals."},
{"@name": "sent_S2", "@question": ["isa", "animal", "?:X"]},
{"@name": "sent_S1", "@sourcetype": "populate", "@logic": ["isa", "elephant", "$some_elephant"], "@nl": "[population: from input]"},
{"@name": "sent_S1", "@sourcetype": "populate", "@logic": ["-isa", "elephant", "$some_not_elephant"], "@nl": "[population: from input]"},
{"@name": "sent_S1", "@sourcetype": "populate", "@logic": ["isa", "animal", "$some_animal"], "@nl": "[population: from input]"},
{"@name": "sent_S1", "@sourcetype": "populate", "@logic": ["-isa", "animal", "$some_not_animal"], "@nl": "[population: from input]"}
]
