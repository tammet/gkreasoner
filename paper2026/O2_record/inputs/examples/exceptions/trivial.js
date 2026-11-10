// Simplest possible example: plain facts and a closed question.
// p holds for a and b, does not hold for c; the question asks p(a).
//
// Run: ./gk Examples/exceptions/trivial.js

[
["p","a"],
["p","b"],
["-p","c"],
{"@question": ["p","a"]}
]

/*

gk output:

{"result": "answer found",

"answers": [
{
"answer": true,
"confidence": 1,
"positive proof":
[
[1, ["in", "frm_4", "goal", 1], [["-p","a"]]],
[2, ["in", "frm_1", "axiom", 1], [["p","a"]]],
[3, ["simp", 1, 2, "fromgoal", 1], false]
]}
]}

*/
