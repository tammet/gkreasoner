// Basic birds-fly/penguins-don't default logic example
// Used as baseline for ASP system comparison
// (see https://logictools.org/gk/ for comparison results)
//
// Run: ./gk Examples/exceptions/gbirds.js

[

["bird","b1"],
["penguin","p1"],

[["penguin","?:X"],"=>",["bird","?:X"]],
[["-bird","?:X"],["flies","?:X"], ["$block", 3, ["$not", ["flies", "?:X"]]]],
[["penguin","?:X"],"=>",["-flies","?:X"]],

{"@question": ["flies","b1"]}

]

/*

The same problem for an ASP system (clingo):

bird(b1).
penguin(p1).
bird(X) :- penguin(X).
flies(X) :- bird(X), not -flies(X).
-flies(X) :- penguin(X).
#show flies/1.
#show -flies/1.

clingo 5.4.0 (same output on 5.6.2):

Answer: 1
flies(b1) -flies(p1)
SATISFIABLE

gk:

{"result": "answer found",

"answers": [
{
"answer": true,
"blockers": [["$block",3,["$not",["flies","b1"]]]],
"confidence": 1,
"positive proof":
[
[1, ["in", "frm_4", "axiom", 1], [["$block",3,["$not",["flies","?:X"]]], ["-bird","?:X"], ["flies","?:X"]]],
[2, ["in", "frm_1", "axiom", 1], [["bird","b1"]]],
[3, ["in", "frm_6", "goal", 1], [["-flies","b1"]]],
[4, ["mp", [1,1], 2, 3, "fromgoal", 1], [["$block",3,["$not",["flies","b1"]]]]]
]}
]}

Both agree: the bird b1 flies (the default applies; nothing blocks it),
and the penguin p1 does not. Unlike ASP systems, gk also handles the
function-symbol variant (gbirds_funsymbs.js) and scales to large constant
sets -- see https://logictools.org/gk/ for timings vs clingo/dlv/s(CASP).

*/
