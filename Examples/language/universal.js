// John likes all boxers. Mike is a boxer. John likes Mike?
// Expected answer: True
// Uses the shared background knowledge base axioms_std.js.
// Run from the repository root:
//   ./bin/gk Examples/language/axioms_std.js Examples/language/universal.js \
//     -strategytext '{"strategy": ["negative_pref", "posunitpara"], "query_preference": 1}' \
//     -seconds 3 -confidence 0.1 -keepconfidence 0.1
[
{"@name": "sent_S1", "@logic": ["isa", "person", "#:John 1"], "@nl": "John 1 likes all boxers."},
{"@name": "sent_S1", "@logic": [["-isa", "boxer", "?:X"], ["has degree rel2", "like", "#:John 1", "?:X", "none", "?:Fv15", ["$ctxt", "?:Fv4", "?:Fv3", "?:Fv1", "?:Fv2"]]], "@nl": "John 1 likes all boxers."},
{"@name": "sent_S2", "@logic": ["isa", "person", "#:Mike 2"], "@nl": "Mike 2 is a boxer."},
{"@name": "sent_S2", "@logic": ["isa", "boxer", "#:Mike 2"], "@nl": "Mike 2 is a boxer."},
{"@name": "sent_S3", "@sourcetype": "question", "@logic": [["-$defq0"], ["has degree rel2", "like", "#:John 1", "#:Mike 2", "none", "?:Fv21", ["$ctxt", "present", "?:Fv9", "?:Fv7", "?:Fv8"]]]},
{"@name": "sent_S3", "@sourcetype": "question", "@logic": [["-has degree rel2", "like", "#:John 1", "#:Mike 2", "none", "?:Fv22", ["$ctxt", "present", "?:Fv9", "?:Fv7", "?:Fv8"]], ["$defq0"]]},
{"@name": "sent_S3", "@question": ["$defq0"]},
{"@name": "sent_S3", "@sourcetype": "question_bridge", "@confidence": 0.95, "@logic": [["-has degree rel2", "like", "#:John 1", "#:Mike 2", "none", "?:Fv18", ["$ctxt", "past", "?:W", "?:L", "?:K"]], ["has degree rel2", "like", "#:John 1", "#:Mike 2", "none", "?:Fv19", ["$ctxt", "present", "?:W", "?:L", "?:K"]], ["$block", 0, ["$not", ["has degree rel2", "like", "#:John 1", "#:Mike 2", "none", "?:Fv20", ["$ctxt", "present", "?:W", "?:L", "?:K"]]]]], "@nl": "Does John 1 like Mike 2?"},
{"@name": "sent_S1", "@sourcetype": "populate", "@logic": ["-isa", "boxer", "$some_not_boxer"], "@nl": "[population: from input]"}
]
