// Elephants are not birds. John is an elephant. John is a bird?
// Expected answer: False
// Uses the shared background knowledge base axioms_std.js.
// Run from the repository root:
//   ./bin/gk Examples/language/axioms_std.js Examples/language/class_exclusion.js \
//     -strategytext '{"strategy": ["negative_pref", "posunitpara"], "query_preference": 1}' \
//     -seconds 3 -confidence 0.1 -keepconfidence 0.1
[
{"@name": "sent_S1", "@logic": [["-isa", "elephant", "?:X"], ["-isa", "bird", "?:X"]], "@nl": "Elephants are not birds."},
{"@name": "sent_S2", "@logic": ["isa", "elephant", "#:John 1"], "@nl": "John 1 is an elephant."},
{"@name": "sent_S3", "@sourcetype": "question", "@logic": [["-$defq0"], ["isa", "bird", "#:John 1"]]},
{"@name": "sent_S3", "@sourcetype": "question", "@logic": [["-isa", "bird", "#:John 1"], ["$defq0"]]},
{"@name": "sent_S3", "@question": ["$defq0"]},
{"@name": "sent_S1", "@sourcetype": "populate", "@logic": ["-isa", "elephant", "$some_not_elephant"], "@nl": "[population: from input]"},
{"@name": "sent_S1", "@sourcetype": "populate", "@logic": ["isa", "bird", "$some_bird"], "@nl": "[population: from input]"},
{"@name": "sent_S1", "@sourcetype": "populate", "@logic": ["-isa", "bird", "$some_not_bird"], "@nl": "[population: from input]"}
]
