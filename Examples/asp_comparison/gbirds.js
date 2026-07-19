// Basic birds example: birds fly by default; penguins are birds that do not fly.
// Baseline for the system comparison in this folder's README.md.
//
// Run: ./bin/gk Examples/asp_comparison/gbirds.js
// Expected: flies(b1) is true (the default applies, nothing blocks it);
// the penguin p1 does not fly.

[

["bird","b1"],
["penguin","p1"],

[["penguin","?:X"],"=>",["bird","?:X"]],
[["-bird","?:X"],["flies","?:X"], ["$block", 3, ["$not", ["flies", "?:X"]]]],
[["penguin","?:X"],"=>",["-flies","?:X"]],

{"@question": ["flies","b1"]}

]
