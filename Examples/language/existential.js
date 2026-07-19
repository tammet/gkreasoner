// Some elephants are animals. Some elephants are not animals?
// Expected answer: Unknown
// Uses the shared background knowledge base axioms_std.js.
// Run from the repository root:
//   ./bin/gk Examples/language/axioms_std.js Examples/language/existential.js \
//     -strategytext '{"strategy": ["negative_pref", "posunitpara"], "query_preference": 1}' \
//     -seconds 3 -confidence 0.1 -keepconfidence 0.1
[
{"@name": "sent_S1", "@logic": ["isa", "elephant", "sk0_elephant"], "@nl": "Some elephants are animals."},
{"@name": "sent_S1", "@logic": [["isa", "animal", "sk0_elephant"], ["$block", ["$", "$generic", 1], ["$not", ["isa", "animal", "sk0_elephant"]]]], "@confidence": 0.98, "@nl": "Some elephants are animals."},
{"@name": "sent_S2", "@sourcetype": "question", "@logic": [["-$defq0"], ["isa", "elephant", "sk1_elephant"]]},
{"@name": "sent_S2", "@sourcetype": "question", "@logic": [["-$defq0"], ["-isa", "animal", "sk1_elephant"]]},
{"@name": "sent_S2", "@sourcetype": "question", "@logic": [["-isa", "elephant", "?:X"], ["isa", "animal", "?:X"], ["$defq0"]]},
{"@name": "sent_S2", "@question": ["$defq0"]},
{"@name": "sent_S1", "@sourcetype": "populate", "@logic": ["isa", "elephant", "$some_elephant"], "@nl": "[population: from input]"},
{"@name": "sent_S1", "@sourcetype": "populate", "@logic": ["-isa", "elephant", "$some_not_elephant"], "@nl": "[population: from input]"},
{"@name": "sent_S1", "@sourcetype": "populate", "@logic": ["isa", "animal", "$some_animal"], "@nl": "[population: from input]"},
{"@name": "sent_S1", "@sourcetype": "populate", "@logic": ["-isa", "animal", "$some_not_animal"], "@nl": "[population: from input]"}
]
