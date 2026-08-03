// Function-symbol variant: bird(X) => bird(f(X)) and penguin(X) => penguin(f(X)).
// These rules make the set of ground terms infinite. gk answers the specific
// query without constructing every term; the grounding-based systems do not
// finish on the corresponding other_systems/ inputs.
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
