// John is a nice man. John has an apple. Mike is a nice man. Greg is a bad man. Mike has a pear. Which man has an apple?
// Expected answer: John
// Uses the shared background knowledge base axioms_std.js.
// Run from the repository root:
//   ./bin/gk Examples/language/axioms_std.js Examples/language/which_has_apple.js \
//     -strategytext '{"strategy": ["negative_pref", "posunitpara"], "query_preference": 1}' \
//     -seconds 3 -confidence 0.1 -keepconfidence 0.1
[
{"@name": "sent_S1", "@logic": ["isa", "man", "#:John 1"], "@nl": "John 1 is a nice man."},
{"@name": "sent_S1", "@logic": ["has degree property", "good", "#:John 1", "none", "person", ["$ctxt", "present", "W0", "?:Fv1", "?:Fv2"]], "@nl": "John 1 is a nice man."},
{"@name": "sent_S2", "@logic": ["isa", "person", "#:John 1"], "@nl": "John 1 has an apple 2."},
{"@name": "sent_S2", "@logic": ["isa", "apple", "#:apple 2"], "@nl": "John 1 has an apple 2."},
{"@name": "sent_S2", "@logic": ["have", "#:John 1", "#:apple 2", ["$ctxt", "present", "W0", "?:Fv3", "?:Fv4"]], "@nl": "John 1 has an apple 2."},
{"@name": "sent_S3", "@logic": ["isa", "man", "#:Mike 3"], "@nl": "Mike 3 is a nice man."},
{"@name": "sent_S3", "@logic": ["has degree property", "good", "#:Mike 3", "none", "person", ["$ctxt", "present", "W0", "?:Fv5", "?:Fv6"]], "@nl": "Mike 3 is a nice man."},
{"@name": "sent_S4", "@logic": ["isa", "man", "#:Greg 4"], "@nl": "Greg 4 is a bad man."},
{"@name": "sent_S4", "@logic": ["-has degree property", "good", "#:Greg 4", "none", "person", ["$ctxt", "present", "W0", "?:Fv7", "?:Fv8"]], "@nl": "Greg 4 is a bad man."},
{"@name": "sent_S5", "@logic": ["isa", "person", "#:Mike 3"], "@nl": "Mike 3 has a pear 5."},
{"@name": "sent_S5", "@logic": ["isa", "pear", "#:pear 5"], "@nl": "Mike 3 has a pear 5."},
{"@name": "sent_S5", "@logic": ["have", "#:Mike 3", "#:pear 5", ["$ctxt", "present", "W0", "?:Fv9", "?:Fv10"]], "@nl": "Mike 3 has a pear 5."},
{"@name": "sent_S6", "@sourcetype": "question", "@logic": [["-$defq0", "?:X"], ["isa", "man", "?:X"]]},
{"@name": "sent_S6", "@sourcetype": "question", "@logic": [["-$defq0", "?:X"], ["isa", "apple", ["sk0", "?:X"]]]},
{"@name": "sent_S6", "@sourcetype": "question", "@logic": [["-$defq0", "?:X"], ["have", "?:X", ["sk0", "?:X"], ["$ctxt", "present", "?:Fv19", "?:Fv11", "?:Fv12"]]]},
{"@name": "sent_S6", "@sourcetype": "question", "@logic": [["-isa", "man", "?:X"], ["-isa", "apple", "?:Y"], ["-have", "?:X", "?:Y", ["$ctxt", "present", "?:Fv24", "?:Fv11", "?:Fv12"]], ["$defq0", "?:X"]]},
{"@name": "sent_S6", "@question": ["$defq0", "?:X"]},
{"@name": "sent_S6", "@sourcetype": "question_bridge", "@confidence": 0.97, "@logic": [["-have", "?:Br1", "?:Br2", ["$ctxt", "past", "?:W", "?:L", "?:K"]], ["have", "?:Br1", "?:Br2", ["$ctxt", "present", "?:W", "?:L", "?:K"]], ["$block", 0, ["$not", ["have", "?:Br1", "?:Br2", ["$ctxt", "present", "?:W", "?:L", "?:K"]]]]], "@nl": "Which man has an apple?"},
{"@name": "frm_excl_isa", "@logic": [["-isa", "apple", "?:X"], ["-isa", "pear", "?:X"]], "@confidence": 0.95, "@nl": "[generated: frm_excl_isa]"},
{"@name": "frm_excl_isa", "@logic": [["-isa", "apple", "?:X"], ["-isa", "pear", "?:Y"], ["-=", "?:X", "?:Y"]], "@confidence": 0.95, "@nl": "[generated: frm_excl_isa]"},
{"@name": "pop_what", "@logic": ["isa", "pear", "$some_pear"], "@nl": "[population: class witnesses for what-query]"},
{"@name": "pop_what", "@logic": ["isa", "apple", "$some_apple"], "@nl": "[population: class witnesses for what-query]"},
{"@name": "pop_what", "@logic": ["isa", "person", "$some_person"], "@nl": "[population: class witnesses for what-query]"},
{"@name": "pop_what", "@logic": ["isa", "man", "$some_man"], "@nl": "[population: class witnesses for what-query]"}
]
