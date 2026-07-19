// Function-symbol variant: bird(X) => bird(f(X)) and penguin(X) => penguin(f(X)).
// These rules make the set of ground terms infinite. In the historical comparison,
// clingo 5.4.0 and DLV 2.1.1 did not finish grounding this input, and s(CASP)
// 0.21.10.09 did not finish its query-directed search. gk can answer the
// specific query without constructing every term.
//
// Run: ./bin/gk Examples/asp_comparison/gbirds_funsymbs.js -seconds 5
// Expected: flies(b1) is true.

[

["bird","b1"],
["penguin","p1"],

[["penguin","?:X"],"=>",["bird","?:X"]],
[["-bird","?:X"],["flies","?:X"], ["$block", 3, ["$not", ["flies", "?:X"]]]],
[["penguin","?:X"],"=>",["-flies","?:X"]],

[["penguin","?:X"],"=>",["penguin",["f","?:X"]]],
[["bird","?:X"],"=>",["bird",["f","?:X"]]],

{"@question": ["flies","b1"]}

]
