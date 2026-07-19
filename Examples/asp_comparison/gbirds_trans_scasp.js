// gk translation of other_systems/scasp_birds_trans.pl. This file deliberately
// has no function-symbol rule, so it isolates the small transitivity input used
// in the historical s(CASP) run.
//
// Run: ./bin/gk \
//   Examples/asp_comparison/gbirds_trans_scasp.js -seconds 1
// Expected: flies(b1) is true.

[

["father","b1","b2"],
["father","p1","p2"],

["bird","b1"],
["penguin","p1"],

[["penguin","?:X"],"=>",["bird","?:X"]],
[["-bird","?:X"],["flies","?:X"],
  ["$block",3,["$not",["flies","?:X"]]]],
[["penguin","?:X"],"=>",["-flies","?:X"]],

[["father","?:X","?:Y"],"=>",["anc","?:X","?:Y"]],
[[["anc","?:X","?:Z"],"&",["anc","?:Z","?:Y"]],
  "=>",["anc","?:X","?:Y"]],
[[["anc","?:Y","?:X"],"&",["penguin","?:Y"]],
  "=>",["penguin","?:X"]],

{"@question":["flies","b1"]}

]
