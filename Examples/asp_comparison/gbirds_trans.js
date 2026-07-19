// Retained historical gk transitivity input. It combines an
// ancestor relation, two propagation rules, and one function-symbol rule.
// The s(CASP) transitivity input in other_systems/ is different: it has no
// function-symbol rule and only propagates penguin. Do not compare these two
// files as an otherwise identical pair.
//
// Run: ./bin/gk Examples/asp_comparison/gbirds_trans.js -seconds 5
// Expected: flies(b1) is true.

[

["father","b1","b2"],
["father","p1","p2"],

["bird","b1"],
["penguin","p1"],

[["penguin","?:X"],"=>",["bird","?:X"]],
[["-bird","?:X"],["flies","?:X"], ["$block", 3, ["$not", ["flies", "?:X"]]]],
[["penguin","?:X"],"=>",["-flies","?:X"]],

[["father","?:X","?:Y"],"=>",["anc","?:X","?:Y"]],
[[["anc","?:X","?:Z"],"&",["anc","?:Z","?:Y"]],"=>",["anc","?:X","?:Y"]],
[[["anc","?:Y","?:X"],"&",["penguin","?:Y"]],"=>",["penguin","?:X"]],
[[["anc","?:Y","?:X"],"&",["bird","?:Y"]],"=>",["bird","?:X"]],
[["bird","?:X"],"=>",["bird",["f","?:X"]]],

{"@question": ["flies","b1"]}

]
