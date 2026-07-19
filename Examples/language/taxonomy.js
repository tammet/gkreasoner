// Elephants are animals. John is an elephant. John is an animal?
// Expected answer: True
// Uses the shared background knowledge base axioms_std.js.
// Run from the repository root:
//   ./bin/gk Examples/language/axioms_std.js Examples/language/taxonomy.js \
//     -strategytext '{"strategy": ["negative_pref", "posunitpara"], "query_preference": 1}' \
//     -seconds 3 -confidence 0.1 -keepconfidence 0.1
[
{"@name": "sent_S1", "@logic": [["-isa", "elephant", "?:X"], ["isa", "animal", "?:X"]], "@nl": "Elephants are animals."},
{"@name": "sent_S2", "@logic": ["isa", "elephant", "#:John 1"], "@nl": "John 1 is an elephant."},
{"@name": "sent_S3", "@sourcetype": "question", "@logic": [["-$defq0"], ["isa", "animal", "#:John 1"]]},
{"@name": "sent_S3", "@sourcetype": "question", "@logic": [["-isa", "animal", "#:John 1"], ["$defq0"]]},
{"@name": "sent_S3", "@question": ["$defq0"]},
{"@name": "sent_S1", "@sourcetype": "populate", "@logic": ["-isa", "elephant", "$some_not_elephant"], "@nl": "[population: from input]"},
{"@name": "sent_S1", "@sourcetype": "populate", "@logic": ["isa", "animal", "$some_animal"], "@nl": "[population: from input]"},
{"@name": "sent_S1", "@sourcetype": "populate", "@logic": ["-isa", "animal", "$some_not_animal"], "@nl": "[population: from input]"}
]
