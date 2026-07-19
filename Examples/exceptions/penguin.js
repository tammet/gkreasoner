[

["bird","b"],
["penguin","p"],
["object","o"],

[["-penguin","?:X"],["bird","?:X"]],
[["bird","?:X"],"=>",["object","?:X"]],

[["penguin","?:X"],"=>",["-flies","?:X"]],

[["-bird","?:X"],["flies","?:X"], ["$block", 3, ["$not", ["flies", "?:X"]]]],
[["-object","?:X"],["-flies","?:X"], ["$block", 2, ["flies", "?:X"]]],

{"@question": ["flies","?:X"]}  // who flies?
// {"@question": ["-flies","?:X"]}  // who does not fly?

]



