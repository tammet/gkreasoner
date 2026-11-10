// negation handling inconsistency part 3:
// add rules for deriving not flies
// this almost restores consistency
//
// notice the full ruleset cannot be written in problog
// NonGroundProbabilisticClause: Encountered a non-ground probabilistic clause at 10:7.

/*

% notice that problog does not accept
%% 0.1:: flies(X) :- not bird(X).

% Probabilistic facts:
0.5::bird(a).
0.5::not bird(a).
0.9:: flies(X) :- bird(X).
0.1:: not flies(X) :- bird(X).
%% 0.1:: flies(X) :- not bird(X).
0.9:: not flies(X) :- not bird(X).

% Queries:
query(flies(_)).

result:  
a  0.2025

*/

[

{"@confidence": 0.5, "@logic": ["bird","messy"]},
{"@confidence": 0.5, "@logic": ["-bird","messy"]},
{"@confidence": 1.0, "@logic": ["bird","tweety"]},
{"@confidence": 1.0, "@logic": ["penguin","pennie"]},

{"@confidence": 1.0, "@logic":   [["penguin","?:X"],"=>",["bird","?:X"]]},

{"@confidence": 0.001, "@logic": [["bird","?:X"],"=>",["penguin","?:X"]]},
{"@confidence": 0.999, "@logic": [["bird","?:X"],"=>",["-penguin","?:X"]]},

{"@confidence": 0.9, "@logic": [["bird","?:X"],"=>",["flies","?:X"]]},
{"@confidence": 0.1, "@logic": [["bird","?:X"],"=>",["-flies","?:X"]]},
{"@confidence": 0.1, "@logic": [["-bird","?:X"],"=>",["flies","?:X"]]},
{"@confidence": 0.9, "@logic": [["-bird","?:X"],"=>",["-flies","?:X"]]},


{"@confidence": 1.0,    "@logic": [["penguin","?:X"],"=>",["-flies","?:X"]]},
/*
{"@confidence": 0.1,    "@logic": [["-penguin","?:X"],"=>",["flies","?:X"]]},
{"@confidence": 0.9999, "@logic": [["-penguin","?:X"],"=>",["-flies","?:X"]]},
*/

{"@question": ["flies","?:X"]}

]


/*
{"result": "proof found",

"answers": [
{
"answer": [["$ans","?:X3"]],
"confidence": -0.41105,
"positive_proof":
[
[1,      7, ["in", "frm_8", "axiom", 0.9, 0, []], [["-bird","?:X"], ["flies","?:X"]]],
[2,      9, ["in", "frm_10", "axiom", 0.1, 0, []], [["flies","?:X"], ["bird","?:X"]]],
[3,     12, ["in", "frm_13", "goal", 1, 0, []], [["-flies","?:X"], ["$ans","?:X"]]],
[4,     21, ["mp", 2, 3, "fromgoal", 0.1, 0, [9]], [["$ans","?:X"], ["bird","?:X"]]],
[5,     57, ["mp", 1, [4,1], "fromgoal", 0.09, 0, [7,9]], [["$ans","?:X"], ["flies","?:X"]]],
[6,     12, ["in", "frm_13", "goal", 1, 0, []], [["-flies","?:X"], ["$ans","?:X"]]],
[7,     75, ["mp", [5,1], 6, "fromgoal", 0.09, 0, [7,9]], [["$ans","?:X3"]]],
[8,      6, ["in", "frm_7", "axiom", 0.999, 0, []], [["-penguin","?:X"], ["-bird","?:X"]]],
[9,      9, ["in", "frm_10", "axiom", 0.1, 0, []], [["flies","?:X"], ["bird","?:X"]]],
[10,     12, ["in", "frm_13", "goal", 1, 0, []], [["-flies","?:X"], ["$ans","?:X"]]],
[11,     21, ["mp", 9, 10, "fromgoal", 0.1, 0, [9]], [["$ans","?:X"], ["bird","?:X"]]],
[12,      5, ["in", "frm_6", "axiom", 0.001, 0, []], [["-bird","?:X"], ["penguin","?:X"]]],
[13,     22, ["mp", [11,1], 12, "fromgoal", 0.0001, 0, [9,5]], [["$ans","?:X"], ["penguin","?:X"]]],
[14,     33, ["mp", 8, [13,1], "fromgoal", 9.99e-05, 0, [6,9,5]], [["-bird","?:X"], ["$ans","?:X"]]],
[15,      9, ["in", "frm_10", "axiom", 0.1, 0, []], [["flies","?:X"], ["bird","?:X"]]],
[16,     12, ["in", "frm_13", "goal", 1, 0, []], [["-flies","?:X"], ["$ans","?:X"]]],
[17,     21, ["mp", 15, 16, "fromgoal", 0.1, 0, [9]], [["$ans","?:X"], ["bird","?:X"]]],
[18,     47, ["mp", 14, [17,1], "fromgoal", 1e-05, 0, [6,9,5]], [["$ans","?:X3"]]],
[19,    170, ["cumul", 7, 18, "fromgoal", 0.0900055, 0, [7,9,6,5]], [["$ans","?:X3"]]],
[20,      7, ["in", "frm_8", "axiom", 0.9, 0, []], [["-bird","?:X"], ["flies","?:X"]]],
[21,      9, ["in", "frm_10", "axiom", 0.1, 0, []], [["flies","?:X"], ["bird","?:X"]]],
[22,     12, ["in", "frm_13", "goal", 1, 0, []], [["-flies","?:X"], ["$ans","?:X"]]],
[23,     21, ["mp", 21, 22, "fromgoal", 0.1, 0, [9]], [["$ans","?:X"], ["bird","?:X"]]],
[24,     57, ["mp", 20, [23,1], "fromgoal", 0.09, 0, [7,9]], [["$ans","?:X"], ["flies","?:X"]]],
[25,     11, ["in", "frm_12", "axiom", 1, 0, []], [["-flies","?:X"], ["-penguin","?:X"]]],
[26,     71, ["mp", [24,1], 25, "fromgoal", 0.09, 0, [7,9,11]], [["-penguin","?:X"], ["$ans","?:X"]]],
[27,      9, ["in", "frm_10", "axiom", 0.1, 0, []], [["flies","?:X"], ["bird","?:X"]]],
[28,     12, ["in", "frm_13", "goal", 1, 0, []], [["-flies","?:X"], ["$ans","?:X"]]],
[29,     21, ["mp", 27, 28, "fromgoal", 0.1, 0, [9]], [["$ans","?:X"], ["bird","?:X"]]],
[30,      5, ["in", "frm_6", "axiom", 0.001, 0, []], [["-bird","?:X"], ["penguin","?:X"]]],
[31,     22, ["mp", [29,1], 30, "fromgoal", 0.0001, 0, [9,5]], [["$ans","?:X"], ["penguin","?:X"]]],
[32,     77, ["mp", 26, [31,1], "fromgoal", 9e-06, 0, [7,9,11,5]], [["$ans","?:X3"]]],
[33,    236, ["cumul", 19, 32, "fromgoal", 0.0900076, 0, [7,9,6,5,11]], [["$ans","?:X3"]]],
[34,      8, ["in", "frm_9", "axiom", 0.1, 0, []], [["-flies","?:X"], ["-bird","?:X"]]],
[35,      7, ["in", "frm_8", "axiom", 0.9, 0, []], [["-bird","?:X"], ["flies","?:X"]]],
[36,      9, ["in", "frm_10", "axiom", 0.1, 0, []], [["flies","?:X"], ["bird","?:X"]]],
[37,     12, ["in", "frm_13", "goal", 1, 0, []], [["-flies","?:X"], ["$ans","?:X"]]],
[38,     21, ["mp", 36, 37, "fromgoal", 0.1, 0, [9]], [["$ans","?:X"], ["bird","?:X"]]],
[39,     57, ["mp", 35, [38,1], "fromgoal", 0.09, 0, [7,9]], [["$ans","?:X"], ["flies","?:X"]]],
[40,    103, ["mp", 34, [39,1], "fromgoal", 0.009, 0, [8,7,9]], [["-bird","?:X"], ["$ans","?:X"]]],
[41,      9, ["in", "frm_10", "axiom", 0.1, 0, []], [["flies","?:X"], ["bird","?:X"]]],
[42,     12, ["in", "frm_13", "goal", 1, 0, []], [["-flies","?:X"], ["$ans","?:X"]]],
[43,     21, ["mp", 41, 42, "fromgoal", 0.1, 0, [9]], [["$ans","?:X"], ["bird","?:X"]]],
[44,    119, ["mp", 40, [43,1], "fromgoal", 0.0009, 0, [8,7,9]], [["$ans","?:X3"]]],
[45,    287, ["cumul", 33, 44, "fromgoal", 0.0904171, 0, [7,9,6,5,11,8]], [["$ans","?:X3"]]]
],
"negative_proof":
[
[1,     11, ["in", "frm_12", "axiom", 1, 0, []], [["-flies","?:X"], ["-penguin","?:X"]]],
[2,    410, ["in", "frm_13", "goal", 1, 0, []], [["flies","?:X"]]],
[3,     10, ["in", "frm_11", "axiom", 0.9, 0, []], [["-flies","?:X"], ["bird","?:X"]]],
[4,    420, ["mp", 3, 2, "fromgoal", 0.9, 0, [10]], [["bird","?:X"]]],
[5,      5, ["in", "frm_6", "axiom", 0.001, 0, []], [["-bird","?:X"], ["penguin","?:X"]]],
[6,    423, ["mp", 4, 5, "fromgoal", 0.0009, 0, [10,5]], [["penguin","?:X3"]]],
[7,    425, ["mp", 1, 2, 6, "fromgoal", 0.0009, 0, [11,10,5]], false],
[8,      1, ["in", "frm_2", "axiom", 0.5, 0, []], [["-bird","messy"]]],
[9,    424, ["mp", 4, 8, "fromgoal", 0.45, 0, [10,1]], false],
[10,    481, ["cumul", 7, 9, "fromgoal", 0.450297, 0, [11,10,5,1]], false],
[11,      6, ["in", "frm_7", "axiom", 0.999, 0, []], [["-penguin","?:X"], ["-bird","?:X"]]],
[12,    423, ["mp", 4, 5, "fromgoal", 0.0009, 0, [10,5]], [["penguin","?:X"]]],
[13,    420, ["mp", 3, 2, "fromgoal", 0.9, 0, [10]], [["bird","?:X3"]]],
[14,    426, ["mp", 11, 12, 13, "fromgoal", 0.0008092, 0, [6,10,5]], false],
[15,    502, ["cumul", 10, 14, "fromgoal", 0.450488, 0, [11,10,5,1,6]], false],
[16,      9, ["in", "frm_10", "axiom", 0.1, 0, []], [["flies","?:X"], ["bird","?:X"]]],
[17,    419, ["mp", 3, 16, "fromaxiom", 0.09, 0, [10,9]], [["bird","?:X"]]],
[18,    421, ["mp", 17, 5, "fromaxiom", 9e-05, 0, [10,9,5]], [["penguin","?:X"]]],
[19,    427, ["mp", 11, 18, 13, "fromgoal", 8.09e-05, 0, [6,10,9,5]], false],
[20,    522, ["cumul", 15, 19, "fromgoal", 0.450503, 0, [11,10,5,1,6,9]], false],
[21,      7, ["in", "frm_8", "axiom", 0.9, 0, []], [["-bird","?:X"], ["flies","?:X"]]],
[22,    439, ["mp", 21, 4, "fromgoal", 0.81, 0, [7,10]], [["flies","?:X"]]],
[23,    443, ["mp", 22, 1, 6, "fromgoal", 0.000729, 0, [7,10,11,5]], false],
[24,    571, ["cumul", 20, 23, "fromgoal", 0.450663, 0, [11,10,5,1,6,9,7]], false],
[25,      2, ["in", "frm_3", "axiom", 1, 0, []], [["bird","tweety"]]],
[26,    442, ["mp", 21, 25, "fromaxiom", 0.9, 0, [7,2]], [["flies","tweety"]]],
[27,    452, ["mp", 26, 1, "fromaxiom", 0.9, 0, [7,2,11]], [["-penguin","tweety"]]],
[28,    460, ["mp", 27, 12, "fromgoal", 0.00081, 0, [7,2,11,10,5]], false],
[29,    677, ["cumul", 24, 28, "fromgoal", 0.450811, 0, [11,10,5,1,6,9,7,2]], false],
[30,      8, ["in", "frm_9", "axiom", 0.1, 0, []], [["-flies","?:X"], ["-bird","?:X"]]],
[31,    464, ["mp", 30, 2, 13, "fromgoal", 0.09, 0, [8,10]], false],
[32,    718, ["cumul", 29, 31, "fromgoal", 0.490353, 0, [11,10,5,1,6,9,7,2,8]], false],
[33,      0, ["in", "frm_1", "axiom", 0.5, 0, []], [["bird","messy"]]],
[34,    441, ["mp", 21, 33, "fromaxiom", 0.45, 0, [7,0]], [["flies","messy"]]],
[35,    467, ["mp", 30, 34, "fromaxiom", 0.045, 0, [8,7,0]], [["-bird","messy"]]],
[36,    472, ["mp", 35, 4, "fromgoal", 0.0405, 0, [8,7,0,10]], false],
[37,    787, ["cumul", 32, 36, "fromgoal", 0.501467, 0, [11,10,5,1,6,9,7,2,8,0]], false]
]},
{
"answer": [["$ans","messy"]],
"confidence": 0.0090009,
"positive_proof":
[
[1,      9, ["in", "frm_10", "axiom", 0.1, 0, []], [["flies","?:X"], ["bird","?:X"]]],
[2,     12, ["in", "frm_13", "goal", 1, 0, []], [["-flies","?:X"], ["$ans","?:X"]]],
[3,     21, ["mp", 1, 2, "fromgoal", 0.1, 0, [9]], [["$ans","?:X"], ["bird","?:X"]]],
[4,      1, ["in", "frm_2", "axiom", 0.5, 0, []], [["-bird","messy"]]],
[5,     23, ["mp", [3,1], 4, "fromgoal", 0.05, 0, [9,1]], [["$ans","messy"]]],
[6,      6, ["in", "frm_7", "axiom", 0.999, 0, []], [["-penguin","?:X"], ["-bird","?:X"]]],
[7,      9, ["in", "frm_10", "axiom", 0.1, 0, []], [["flies","?:X"], ["bird","?:X"]]],
[8,     12, ["in", "frm_13", "goal", 1, 0, []], [["-flies","?:X"], ["$ans","?:X"]]],
[9,     21, ["mp", 7, 8, "fromgoal", 0.1, 0, [9]], [["$ans","?:X"], ["bird","?:X"]]],
[10,      5, ["in", "frm_6", "axiom", 0.001, 0, []], [["-bird","?:X"], ["penguin","?:X"]]],
[11,     22, ["mp", [9,1], 10, "fromgoal", 0.0001, 0, [9,5]], [["$ans","?:X"], ["penguin","?:X"]]],
[12,     33, ["mp", 6, [11,1], "fromgoal", 9.99e-05, 0, [6,9,5]], [["-bird","?:X"], ["$ans","?:X"]]],
[13,      9, ["in", "frm_10", "axiom", 0.1, 0, []], [["flies","?:X"], ["bird","?:X"]]],
[14,     12, ["in", "frm_13", "goal", 1, 0, []], [["-flies","?:X"], ["$ans","?:X"]]],
[15,     21, ["mp", 13, 14, "fromgoal", 0.1, 0, [9]], [["$ans","?:X"], ["bird","?:X"]]],
[16,     47, ["mp", 12, [15,1], "fromgoal", 1e-05, 0, [6,9,5]], [["$ans","?:X3"]]],
[17,    161, ["cumul", 5, 16, "fromgoal", 0.0500057, 0, [9,1,6,5]], [["$ans","messy"]]],
[18,      7, ["in", "frm_8", "axiom", 0.9, 0, []], [["-bird","?:X"], ["flies","?:X"]]],
[19,      9, ["in", "frm_10", "axiom", 0.1, 0, []], [["flies","?:X"], ["bird","?:X"]]],
[20,     12, ["in", "frm_13", "goal", 1, 0, []], [["-flies","?:X"], ["$ans","?:X"]]],
[21,     21, ["mp", 19, 20, "fromgoal", 0.1, 0, [9]], [["$ans","?:X"], ["bird","?:X"]]],
[22,     57, ["mp", 18, [21,1], "fromgoal", 0.09, 0, [7,9]], [["$ans","?:X"], ["flies","?:X"]]],
[23,     12, ["in", "frm_13", "goal", 1, 0, []], [["-flies","?:X"], ["$ans","?:X"]]],
[24,     75, ["mp", [22,1], 23, "fromgoal", 0.09, 0, [7,9]], [["$ans","?:X3"]]],
[25,    221, ["cumul", 17, 24, "fromgoal", 0.120337, 0, [9,1,6,5,7]], [["$ans","messy"]]],
[26,      7, ["in", "frm_8", "axiom", 0.9, 0, []], [["-bird","?:X"], ["flies","?:X"]]],
[27,      9, ["in", "frm_10", "axiom", 0.1, 0, []], [["flies","?:X"], ["bird","?:X"]]],
[28,     12, ["in", "frm_13", "goal", 1, 0, []], [["-flies","?:X"], ["$ans","?:X"]]],
[29,     21, ["mp", 27, 28, "fromgoal", 0.1, 0, [9]], [["$ans","?:X"], ["bird","?:X"]]],
[30,     57, ["mp", 26, [29,1], "fromgoal", 0.09, 0, [7,9]], [["$ans","?:X"], ["flies","?:X"]]],
[31,     11, ["in", "frm_12", "axiom", 1, 0, []], [["-flies","?:X"], ["-penguin","?:X"]]],
[32,     71, ["mp", [30,1], 31, "fromgoal", 0.09, 0, [7,9,11]], [["-penguin","?:X"], ["$ans","?:X"]]],
[33,      9, ["in", "frm_10", "axiom", 0.1, 0, []], [["flies","?:X"], ["bird","?:X"]]],
[34,     12, ["in", "frm_13", "goal", 1, 0, []], [["-flies","?:X"], ["$ans","?:X"]]],
[35,     21, ["mp", 33, 34, "fromgoal", 0.1, 0, [9]], [["$ans","?:X"], ["bird","?:X"]]],
[36,      5, ["in", "frm_6", "axiom", 0.001, 0, []], [["-bird","?:X"], ["penguin","?:X"]]],
[37,     22, ["mp", [35,1], 36, "fromgoal", 0.0001, 0, [9,5]], [["$ans","?:X"], ["penguin","?:X"]]],
[38,     77, ["mp", 32, [37,1], "fromgoal", 9e-06, 0, [7,9,11,5]], [["$ans","?:X3"]]],
[39,    242, ["cumul", 25, 38, "fromgoal", 0.120339, 0, [9,1,6,5,7,11]], [["$ans","messy"]]],
[40,      7, ["in", "frm_8", "axiom", 0.9, 0, []], [["-bird","?:X"], ["flies","?:X"]]],
[41,      0, ["in", "frm_1", "axiom", 0.5, 0, []], [["bird","messy"]]],
[42,     59, ["mp", 40, 41, "fromaxiom", 0.45, 0, [7,0]], [["flies","messy"]]],
[43,     12, ["in", "frm_13", "goal", 1, 0, []], [["-flies","?:X"], ["$ans","?:X"]]],
[44,     90, ["mp", 42, 43, "fromgoal", 0.45, 0, [7,0]], [["$ans","messy"]]],
[45,    269, ["cumul", 39, 44, "fromgoal", 0.49964, 0, [9,1,6,5,7,11,0]], [["$ans","messy"]]],
[46,      8, ["in", "frm_9", "axiom", 0.1, 0, []], [["-flies","?:X"], ["-bird","?:X"]]],
[47,      7, ["in", "frm_8", "axiom", 0.9, 0, []], [["-bird","?:X"], ["flies","?:X"]]],
[48,      9, ["in", "frm_10", "axiom", 0.1, 0, []], [["flies","?:X"], ["bird","?:X"]]],
[49,     12, ["in", "frm_13", "goal", 1, 0, []], [["-flies","?:X"], ["$ans","?:X"]]],
[50,     21, ["mp", 48, 49, "fromgoal", 0.1, 0, [9]], [["$ans","?:X"], ["bird","?:X"]]],
[51,     57, ["mp", 47, [50,1], "fromgoal", 0.09, 0, [7,9]], [["$ans","?:X"], ["flies","?:X"]]],
[52,    103, ["mp", 46, [51,1], "fromgoal", 0.009, 0, [8,7,9]], [["-bird","?:X"], ["$ans","?:X"]]],
[53,      9, ["in", "frm_10", "axiom", 0.1, 0, []], [["flies","?:X"], ["bird","?:X"]]],
[54,     12, ["in", "frm_13", "goal", 1, 0, []], [["-flies","?:X"], ["$ans","?:X"]]],
[55,     21, ["mp", 53, 54, "fromgoal", 0.1, 0, [9]], [["$ans","?:X"], ["bird","?:X"]]],
[56,    119, ["mp", 52, [55,1], "fromgoal", 0.0009, 0, [8,7,9]], [["$ans","?:X3"]]],
[57,    299, ["cumul", 45, 56, "fromgoal", 0.49991, 0, [9,1,6,5,7,11,0,8]], [["$ans","messy"]]]
],
"negative_proof":
[
[1,     11, ["in", "frm_12", "axiom", 1, 0, []], [["-flies","?:X"], ["-penguin","?:X"]]],
[2,    858, ["in", "frm_13", "goal", 1, 0, []], [["flies","messy"]]],
[3,     10, ["in", "frm_11", "axiom", 0.9, 0, []], [["-flies","?:X"], ["bird","?:X"]]],
[4,    868, ["mp", 3, 2, "fromgoal", 0.9, 0, [10]], [["bird","messy"]]],
[5,      5, ["in", "frm_6", "axiom", 0.001, 0, []], [["-bird","?:X"], ["penguin","?:X"]]],
[6,    873, ["mp", 4, 5, "fromgoal", 0.0009, 0, [10,5]], [["penguin","messy"]]],
[7,    877, ["mp", 1, 2, 6, "fromgoal", 0.0009, 0, [11,10,5]], false],
[8,    868, ["mp", 3, 2, "fromgoal", 0.9, 0, [10]], [["bird","messy"]]],
[9,      1, ["in", "frm_2", "axiom", 0.5, 0, []], [["-bird","messy"]]],
[10,    869, ["simp", 8, 9, "fromgoal", 0.45, 0, [10,1]], false],
[11,    956, ["cumul", 7, 10, "fromgoal", 0.450297, 0, [11,10,5,1]], false],
[12,      6, ["in", "frm_7", "axiom", 0.999, 0, []], [["-penguin","?:X"], ["-bird","?:X"]]],
[13,    873, ["mp", 4, 5, "fromgoal", 0.0009, 0, [10,5]], [["penguin","messy"]]],
[14,    880, ["mp", 12, 13, 8, "fromgoal", 0.0008092, 0, [6,10,5]], false],
[15,    973, ["cumul", 11, 14, "fromgoal", 0.450488, 0, [11,10,5,1,6]], false],
[16,      0, ["in", "frm_1", "axiom", 0.5, 0, []], [["bird","messy"]]],
[17,    860, ["mp", 5, 16, "fromaxiom", 0.0005, 0, [5,0]], [["penguin","messy"]]],
[18,    883, ["mp", 12, 17, 8, "fromgoal", 0.0004496, 0, [6,5,0,10]], false],
[19,    988, ["cumul", 15, 18, "fromgoal", 0.45057, 0, [11,10,5,1,6,0]], false],
[20,      9, ["in", "frm_10", "axiom", 0.1, 0, []], [["flies","?:X"], ["bird","?:X"]]],
[21,    867, ["mp", 3, 20, "fromaxiom", 0.09, 0, [10,9]], [["bird","?:X"]]],
[22,    870, ["mp", 21, 5, "fromaxiom", 9e-05, 0, [10,9,5]], [["penguin","?:X"]]],
[23,    878, ["mp", 12, 22, "fromaxiom", 8.99e-05, 0, [6,10,9,5]], [["-bird","?:X"]]],
[24,    887, ["mp", 23, 4, "fromgoal", 8.09e-05, 0, [6,10,9,5]], false],
[25,   1009, ["cumul", 19, 24, "fromgoal", 0.450588, 0, [11,10,5,1,6,0,9]], false],
[26,      8, ["in", "frm_9", "axiom", 0.1, 0, []], [["-flies","?:X"], ["-bird","?:X"]]],
[27,    922, ["mp", 26, 2, 8, "fromgoal", 0.09, 0, [8,10]], false],
[28,   1059, ["cumul", 25, 27, "fromgoal", 0.489047, 0, [11,10,5,1,6,0,9,8]], false],
[29,      7, ["in", "frm_8", "axiom", 0.9, 0, []], [["-bird","?:X"], ["flies","?:X"]]],
[30,    893, ["mp", 29, 21, "fromaxiom", 0.081, 0, [7,10,9]], [["flies","?:X"]]],
[31,    916, ["mp", 26, 30, "fromaxiom", 0.0081, 0, [8,7,10,9]], [["-bird","?:X"]]],
[32,    924, ["mp", 31, 4, "fromgoal", 0.00729, 0, [8,7,10,9]], false],
[33,   1101, ["cumul", 28, 32, "fromgoal", 0.490909, 0, [11,10,5,1,6,0,9,8,7]], false]
]},
{
"answer": [["$ans","tweety"]],
"confidence": 0.811421,
"positive_proof":
[
[1,      7, ["in", "frm_8", "axiom", 0.9, 0, []], [["-bird","?:X"], ["flies","?:X"]]],
[2,      2, ["in", "frm_3", "axiom", 1, 0, []], [["bird","tweety"]]],
[3,     60, ["mp", 1, 2, "fromaxiom", 0.9, 0, [7,2]], [["flies","tweety"]]],
[4,     12, ["in", "frm_13", "goal", 1, 0, []], [["-flies","?:X"], ["$ans","?:X"]]],
[5,     95, ["mp", 3, 4, "fromgoal", 0.9, 0, [7,2]], [["$ans","tweety"]]],
[6,      7, ["in", "frm_8", "axiom", 0.9, 0, []], [["-bird","?:X"], ["flies","?:X"]]],
[7,      9, ["in", "frm_10", "axiom", 0.1, 0, []], [["flies","?:X"], ["bird","?:X"]]],
[8,     12, ["in", "frm_13", "goal", 1, 0, []], [["-flies","?:X"], ["$ans","?:X"]]],
[9,     21, ["mp", 7, 8, "fromgoal", 0.1, 0, [9]], [["$ans","?:X"], ["bird","?:X"]]],
[10,     57, ["mp", 6, [9,1], "fromgoal", 0.09, 0, [7,9]], [["$ans","?:X"], ["flies","?:X"]]],
[11,     12, ["in", "frm_13", "goal", 1, 0, []], [["-flies","?:X"], ["$ans","?:X"]]],
[12,     75, ["mp", [10,1], 11, "fromgoal", 0.09, 0, [7,9]], [["$ans","?:X3"]]],
[13,      6, ["in", "frm_7", "axiom", 0.999, 0, []], [["-penguin","?:X"], ["-bird","?:X"]]],
[14,      9, ["in", "frm_10", "axiom", 0.1, 0, []], [["flies","?:X"], ["bird","?:X"]]],
[15,     12, ["in", "frm_13", "goal", 1, 0, []], [["-flies","?:X"], ["$ans","?:X"]]],
[16,     21, ["mp", 14, 15, "fromgoal", 0.1, 0, [9]], [["$ans","?:X"], ["bird","?:X"]]],
[17,      5, ["in", "frm_6", "axiom", 0.001, 0, []], [["-bird","?:X"], ["penguin","?:X"]]],
[18,     22, ["mp", [16,1], 17, "fromgoal", 0.0001, 0, [9,5]], [["$ans","?:X"], ["penguin","?:X"]]],
[19,     33, ["mp", 13, [18,1], "fromgoal", 9.99e-05, 0, [6,9,5]], [["-bird","?:X"], ["$ans","?:X"]]],
[20,      9, ["in", "frm_10", "axiom", 0.1, 0, []], [["flies","?:X"], ["bird","?:X"]]],
[21,     12, ["in", "frm_13", "goal", 1, 0, []], [["-flies","?:X"], ["$ans","?:X"]]],
[22,     21, ["mp", 20, 21, "fromgoal", 0.1, 0, [9]], [["$ans","?:X"], ["bird","?:X"]]],
[23,     47, ["mp", 19, [22,1], "fromgoal", 1e-05, 0, [6,9,5]], [["$ans","?:X3"]]],
[24,    170, ["cumul", 12, 23, "fromgoal", 0.0900055, 0, [7,9,6,5]], [["$ans","?:X3"]]],
[25,      7, ["in", "frm_8", "axiom", 0.9, 0, []], [["-bird","?:X"], ["flies","?:X"]]],
[26,      9, ["in", "frm_10", "axiom", 0.1, 0, []], [["flies","?:X"], ["bird","?:X"]]],
[27,     12, ["in", "frm_13", "goal", 1, 0, []], [["-flies","?:X"], ["$ans","?:X"]]],
[28,     21, ["mp", 26, 27, "fromgoal", 0.1, 0, [9]], [["$ans","?:X"], ["bird","?:X"]]],
[29,     57, ["mp", 25, [28,1], "fromgoal", 0.09, 0, [7,9]], [["$ans","?:X"], ["flies","?:X"]]],
[30,     11, ["in", "frm_12", "axiom", 1, 0, []], [["-flies","?:X"], ["-penguin","?:X"]]],
[31,     71, ["mp", [29,1], 30, "fromgoal", 0.09, 0, [7,9,11]], [["-penguin","?:X"], ["$ans","?:X"]]],
[32,      9, ["in", "frm_10", "axiom", 0.1, 0, []], [["flies","?:X"], ["bird","?:X"]]],
[33,     12, ["in", "frm_13", "goal", 1, 0, []], [["-flies","?:X"], ["$ans","?:X"]]],
[34,     21, ["mp", 32, 33, "fromgoal", 0.1, 0, [9]], [["$ans","?:X"], ["bird","?:X"]]],
[35,      5, ["in", "frm_6", "axiom", 0.001, 0, []], [["-bird","?:X"], ["penguin","?:X"]]],
[36,     22, ["mp", [34,1], 35, "fromgoal", 0.0001, 0, [9,5]], [["$ans","?:X"], ["penguin","?:X"]]],
[37,     77, ["mp", 31, [36,1], "fromgoal", 9e-06, 0, [7,9,11,5]], [["$ans","?:X3"]]],
[38,    236, ["cumul", 24, 37, "fromgoal", 0.0900076, 0, [7,9,6,5,11]], [["$ans","?:X3"]]],
[39,    273, ["cumul", 5, 38, "fromgoal", 0.906429, 0, [7,2,9,6,5,11]], [["$ans","tweety"]]],
[40,      8, ["in", "frm_9", "axiom", 0.1, 0, []], [["-flies","?:X"], ["-bird","?:X"]]],
[41,      7, ["in", "frm_8", "axiom", 0.9, 0, []], [["-bird","?:X"], ["flies","?:X"]]],
[42,      9, ["in", "frm_10", "axiom", 0.1, 0, []], [["flies","?:X"], ["bird","?:X"]]],
[43,     12, ["in", "frm_13", "goal", 1, 0, []], [["-flies","?:X"], ["$ans","?:X"]]],
[44,     21, ["mp", 42, 43, "fromgoal", 0.1, 0, [9]], [["$ans","?:X"], ["bird","?:X"]]],
[45,     57, ["mp", 41, [44,1], "fromgoal", 0.09, 0, [7,9]], [["$ans","?:X"], ["flies","?:X"]]],
[46,    103, ["mp", 40, [45,1], "fromgoal", 0.009, 0, [8,7,9]], [["-bird","?:X"], ["$ans","?:X"]]],
[47,      9, ["in", "frm_10", "axiom", 0.1, 0, []], [["flies","?:X"], ["bird","?:X"]]],
[48,     12, ["in", "frm_13", "goal", 1, 0, []], [["-flies","?:X"], ["$ans","?:X"]]],
[49,     21, ["mp", 47, 48, "fromgoal", 0.1, 0, [9]], [["$ans","?:X"], ["bird","?:X"]]],
[50,    119, ["mp", 46, [49,1], "fromgoal", 0.0009, 0, [8,7,9]], [["$ans","?:X3"]]],
[51,    301, ["cumul", 39, 50, "fromgoal", 0.906476, 0, [7,2,9,6,5,11,8]], [["$ans","tweety"]]]
],
"negative_proof":
[
[1,      8, ["in", "frm_9", "axiom", 0.1, 0, []], [["-flies","?:X"], ["-bird","?:X"]]],
[2,   1134, ["in", "frm_13", "goal", 1, 0, []], [["flies","tweety"]]],
[3,     10, ["in", "frm_11", "axiom", 0.9, 0, []], [["-flies","?:X"], ["bird","?:X"]]],
[4,   1144, ["mp", 3, 2, "fromgoal", 0.9, 0, [10]], [["bird","tweety"]]],
[5,   1197, ["mp", 1, 2, 4, "fromgoal", 0.09, 0, [8,10]], false],
[6,     11, ["in", "frm_12", "axiom", 1, 0, []], [["-flies","?:X"], ["-penguin","?:X"]]],
[7,   1144, ["mp", 3, 2, "fromgoal", 0.9, 0, [10]], [["bird","tweety"]]],
[8,      5, ["in", "frm_6", "axiom", 0.001, 0, []], [["-bird","?:X"], ["penguin","?:X"]]],
[9,   1148, ["mp", 7, 8, "fromgoal", 0.0009, 0, [10,5]], [["penguin","tweety"]]],
[10,   1151, ["mp", 6, 2, 9, "fromgoal", 0.0009, 0, [11,10,5]], false],
[11,   1233, ["cumul", 5, 10, "fromgoal", 0.0904914, 0, [8,10,11,5]], false],
[12,      6, ["in", "frm_7", "axiom", 0.999, 0, []], [["-penguin","?:X"], ["-bird","?:X"]]],
[13,   1148, ["mp", 7, 8, "fromgoal", 0.0009, 0, [10,5]], [["penguin","tweety"]]],
[14,   1154, ["mp", 12, 13, 4, "fromgoal", 0.0008092, 0, [6,10,5]], false],
[15,   1238, ["cumul", 11, 14, "fromgoal", 0.0908068, 0, [8,10,11,5,6]], false],
[16,      2, ["in", "frm_3", "axiom", 1, 0, []], [["bird","tweety"]]],
[17,   1137, ["mp", 8, 16, "fromaxiom", 0.001, 0, [5,2]], [["penguin","tweety"]]],
[18,   1155, ["mp", 12, 17, 4, "fromgoal", 0.0008991, 0, [6,5,2,10]], false],
[19,   1246, ["cumul", 15, 18, "fromgoal", 0.0910793, 0, [8,10,11,5,6,2]], false],
[20,      7, ["in", "frm_8", "axiom", 0.9, 0, []], [["-bird","?:X"], ["flies","?:X"]]],
[21,      9, ["in", "frm_10", "axiom", 0.1, 0, []], [["flies","?:X"], ["bird","?:X"]]],
[22,   1143, ["mp", 3, 21, "fromaxiom", 0.09, 0, [10,9]], [["bird","?:X"]]],
[23,   1168, ["mp", 20, 22, "fromaxiom", 0.081, 0, [7,10,9]], [["flies","?:X"]]],
[24,   1191, ["mp", 1, 23, "fromaxiom", 0.0081, 0, [8,7,10,9]], [["-bird","?:X"]]],
[25,   1199, ["mp", 24, 7, "fromgoal", 0.00729, 0, [8,7,10,9]], false],
[26,   1287, ["cumul", 19, 25, "fromgoal", 0.0950549, 0, [8,10,11,5,6,2,7,9]], false]
]},
{
"answer": [["$ans","pennie"]],
"confidence": 0.00399041,
"positive_proof":
[
[1,      7, ["in", "frm_8", "axiom", 0.9, 0, []], [["-bird","?:X"], ["flies","?:X"]]],
[2,      4, ["in", "frm_5", "axiom", 1, 0, []], [["-penguin","?:X"], ["bird","?:X"]]],
[3,      3, ["in", "frm_4", "axiom", 1, 0, []], [["penguin","pennie"]]],
[4,     19, ["mp", 2, 3, "fromaxiom", 1, 0, [4,3]], [["bird","pennie"]]],
[5,     58, ["mp", 1, 4, "fromaxiom", 0.9, 0, [7,4,3]], [["flies","pennie"]]],
[6,     12, ["in", "frm_13", "goal", 1, 0, []], [["-flies","?:X"], ["$ans","?:X"]]],
[7,     85, ["mp", 5, 6, "fromgoal", 0.9, 0, [7,4,3]], [["$ans","pennie"]]],
[8,      7, ["in", "frm_8", "axiom", 0.9, 0, []], [["-bird","?:X"], ["flies","?:X"]]],
[9,      9, ["in", "frm_10", "axiom", 0.1, 0, []], [["flies","?:X"], ["bird","?:X"]]],
[10,     12, ["in", "frm_13", "goal", 1, 0, []], [["-flies","?:X"], ["$ans","?:X"]]],
[11,     21, ["mp", 9, 10, "fromgoal", 0.1, 0, [9]], [["$ans","?:X"], ["bird","?:X"]]],
[12,     57, ["mp", 8, [11,1], "fromgoal", 0.09, 0, [7,9]], [["$ans","?:X"], ["flies","?:X"]]],
[13,     12, ["in", "frm_13", "goal", 1, 0, []], [["-flies","?:X"], ["$ans","?:X"]]],
[14,     75, ["mp", [12,1], 13, "fromgoal", 0.09, 0, [7,9]], [["$ans","?:X3"]]],
[15,      6, ["in", "frm_7", "axiom", 0.999, 0, []], [["-penguin","?:X"], ["-bird","?:X"]]],
[16,      9, ["in", "frm_10", "axiom", 0.1, 0, []], [["flies","?:X"], ["bird","?:X"]]],
[17,     12, ["in", "frm_13", "goal", 1, 0, []], [["-flies","?:X"], ["$ans","?:X"]]],
[18,     21, ["mp", 16, 17, "fromgoal", 0.1, 0, [9]], [["$ans","?:X"], ["bird","?:X"]]],
[19,      5, ["in", "frm_6", "axiom", 0.001, 0, []], [["-bird","?:X"], ["penguin","?:X"]]],
[20,     22, ["mp", [18,1], 19, "fromgoal", 0.0001, 0, [9,5]], [["$ans","?:X"], ["penguin","?:X"]]],
[21,     33, ["mp", 15, [20,1], "fromgoal", 9.99e-05, 0, [6,9,5]], [["-bird","?:X"], ["$ans","?:X"]]],
[22,      9, ["in", "frm_10", "axiom", 0.1, 0, []], [["flies","?:X"], ["bird","?:X"]]],
[23,     12, ["in", "frm_13", "goal", 1, 0, []], [["-flies","?:X"], ["$ans","?:X"]]],
[24,     21, ["mp", 22, 23, "fromgoal", 0.1, 0, [9]], [["$ans","?:X"], ["bird","?:X"]]],
[25,     47, ["mp", 21, [24,1], "fromgoal", 1e-05, 0, [6,9,5]], [["$ans","?:X3"]]],
[26,    170, ["cumul", 14, 25, "fromgoal", 0.0900055, 0, [7,9,6,5]], [["$ans","?:X3"]]],
[27,    254, ["cumul", 7, 26, "fromgoal", 0.906429, 0, [7,4,3,9,6,5]], [["$ans","pennie"]]],
[28,      7, ["in", "frm_8", "axiom", 0.9, 0, []], [["-bird","?:X"], ["flies","?:X"]]],
[29,      9, ["in", "frm_10", "axiom", 0.1, 0, []], [["flies","?:X"], ["bird","?:X"]]],
[30,     12, ["in", "frm_13", "goal", 1, 0, []], [["-flies","?:X"], ["$ans","?:X"]]],
[31,     21, ["mp", 29, 30, "fromgoal", 0.1, 0, [9]], [["$ans","?:X"], ["bird","?:X"]]],
[32,     57, ["mp", 28, [31,1], "fromgoal", 0.09, 0, [7,9]], [["$ans","?:X"], ["flies","?:X"]]],
[33,     11, ["in", "frm_12", "axiom", 1, 0, []], [["-flies","?:X"], ["-penguin","?:X"]]],
[34,     71, ["mp", [32,1], 33, "fromgoal", 0.09, 0, [7,9,11]], [["-penguin","?:X"], ["$ans","?:X"]]],
[35,      3, ["in", "frm_4", "axiom", 1, 0, []], [["penguin","pennie"]]],
[36,     80, ["mp", 34, 35, "fromgoal", 0.09, 0, [7,9,11,3]], [["$ans","pennie"]]],
[37,      8, ["in", "frm_9", "axiom", 0.1, 0, []], [["-flies","?:X"], ["-bird","?:X"]]],
[38,      7, ["in", "frm_8", "axiom", 0.9, 0, []], [["-bird","?:X"], ["flies","?:X"]]],
[39,      9, ["in", "frm_10", "axiom", 0.1, 0, []], [["flies","?:X"], ["bird","?:X"]]],
[40,     12, ["in", "frm_13", "goal", 1, 0, []], [["-flies","?:X"], ["$ans","?:X"]]],
[41,     21, ["mp", 39, 40, "fromgoal", 0.1, 0, [9]], [["$ans","?:X"], ["bird","?:X"]]],
[42,     57, ["mp", 38, [41,1], "fromgoal", 0.09, 0, [7,9]], [["$ans","?:X"], ["flies","?:X"]]],
[43,    103, ["mp", 37, [42,1], "fromgoal", 0.009, 0, [8,7,9]], [["-bird","?:X"], ["$ans","?:X"]]],
[44,      9, ["in", "frm_10", "axiom", 0.1, 0, []], [["flies","?:X"], ["bird","?:X"]]],
[45,     12, ["in", "frm_13", "goal", 1, 0, []], [["-flies","?:X"], ["$ans","?:X"]]],
[46,     21, ["mp", 44, 45, "fromgoal", 0.1, 0, [9]], [["$ans","?:X"], ["bird","?:X"]]],
[47,    119, ["mp", 43, [46,1], "fromgoal", 0.0009, 0, [8,7,9]], [["$ans","?:X3"]]],
[48,    244, ["cumul", 36, 47, "fromgoal", 0.090351, 0, [7,9,11,3,8]], [["$ans","pennie"]]],
[49,    408, ["cumul", 27, 48, "fromgoal", 0.910272, 0, [7,4,3,9,6,5,11,8]], [["$ans","pennie"]]]
],
"negative_proof":
[
[1,      6, ["in", "frm_7", "axiom", 0.999, 0, []], [["-penguin","?:X"], ["-bird","?:X"]]],
[2,      3, ["in", "frm_4", "axiom", 1, 0, []], [["penguin","pennie"]]],
[3,     10, ["in", "frm_11", "axiom", 0.9, 0, []], [["-flies","?:X"], ["bird","?:X"]]],
[4,   1303, ["in", "frm_13", "goal", 1, 0, []], [["flies","pennie"]]],
[5,   1313, ["mp", 3, 4, "fromgoal", 0.9, 0, [10]], [["bird","pennie"]]],
[6,   1328, ["mp", 1, 2, 5, "fromgoal", 0.8991, 0, [6,3,10]], false],
[7,     11, ["in", "frm_12", "axiom", 1, 0, []], [["-flies","?:X"], ["-penguin","?:X"]]],
[8,   1313, ["mp", 3, 4, "fromgoal", 0.9, 0, [10]], [["bird","pennie"]]],
[9,      5, ["in", "frm_6", "axiom", 0.001, 0, []], [["-bird","?:X"], ["penguin","?:X"]]],
[10,   1317, ["mp", 8, 9, "fromgoal", 0.0009, 0, [10,5]], [["penguin","pennie"]]],
[11,   1320, ["mp", 7, 4, 10, "fromgoal", 0.0009, 0, [11,10,5]], false],
[12,   1385, ["cumul", 6, 11, "fromgoal", 0.899161, 0, [6,3,10,11,5]], false],
[13,      9, ["in", "frm_10", "axiom", 0.1, 0, []], [["flies","?:X"], ["bird","?:X"]]],
[14,   1312, ["mp", 3, 13, "fromaxiom", 0.09, 0, [10,9]], [["bird","?:X"]]],
[15,   1314, ["mp", 14, 9, "fromaxiom", 9e-05, 0, [10,9,5]], [["penguin","?:X"]]],
[16,   1321, ["mp", 1, 15, "fromaxiom", 8.99e-05, 0, [6,10,9,5]], [["-bird","?:X"]]],
[17,   1330, ["mp", 16, 8, "fromgoal", 8.09e-05, 0, [6,10,9,5]], false],
[18,   1406, ["cumul", 12, 17, "fromgoal", 0.899163, 0, [6,3,10,11,5,9]], false],
[19,      8, ["in", "frm_9", "axiom", 0.1, 0, []], [["-flies","?:X"], ["-bird","?:X"]]],
[20,   1367, ["mp", 19, 4, 5, "fromgoal", 0.09, 0, [8,10]], false],
[21,   1434, ["cumul", 18, 20, "fromgoal", 0.90597, 0, [6,3,10,11,5,9,8]], false],
[22,      7, ["in", "frm_8", "axiom", 0.9, 0, []], [["-bird","?:X"], ["flies","?:X"]]],
[23,   1337, ["mp", 22, 14, "fromaxiom", 0.081, 0, [7,10,9]], [["flies","?:X"]]],
[24,   1361, ["mp", 19, 23, "fromaxiom", 0.0081, 0, [8,7,10,9]], [["-bird","?:X"]]],
[25,   1369, ["mp", 24, 8, "fromgoal", 0.00729, 0, [8,7,10,9]], false],
[26,   1454, ["cumul", 21, 25, "fromgoal", 0.906281, 0, [6,3,10,11,5,9,8,7]], false]
]}
]}



*/
/*

Summary of the Alchemy 2 implementation of the example.

::::::::::::::
studymln/mln/study23-lrn.mln
::::::::::::::
//predicate declarations
Obs2(c)
Obs(c)
Penguin(c)
Flies(c)
Bird(c)

// -4.53941  Obs(x) => Bird(x)
-4.53941  Bird(a1) v !Obs(a1)

// 8.10784  Obs2(x) => !Bird(x)
8.10784  !Bird(a1) v !Obs2(a1)

// Penguin(x) => Bird(x).
Bird(a1) v !Penguin(a1).

// -2.48726  Bird(x) => Penguin(x)
-2.48726  !Bird(a1) v Penguin(a1)

// 2.17445  Bird(x) => !Penguin(x)
2.17445  !Bird(a1) v !Penguin(a1)

// -0.844797  Bird(x) => Flies(x)
-0.844797  !Bird(a1) v Flies(a1)

// Penguin(x) => !Flies(x).
!Penguin(a1) v !Flies(a1).

// 1.63321  Bird(a1)
1.63321  Bird(a1)

// -2.17445  Penguin(a1)
-2.17445  Penguin(a1)

// -1.75495  Flies(a1)
-1.75495  Flies(a1)

// 0       Obs(a1)
0       Obs(a1)

// 0       Obs2(a1)
0       Obs2(a1)

::::::::::::::
studymln/mln/study23.db
::::::::::::::
Obs(Messy)
Obs2(Messy)
Bird(Tweety)
Penguin(Pennie)

::::::::::::::
studymln/RESULTS.tmp
::::::::::::::
infer:	Bird(Messy) 4.9995e-05
infer:	Bird(Pennie) 0.99995
infer:	Flies(Messy) 0.149035
infer:	Flies(Tweety) 0.0720428
infer:	Flies(Pennie) 4.9995e-05
infer:	Penguin(Messy) 4.9995e-05
infer:	Penguin(Tweety) 4.9995e-05
liftedinfer -ptpe:	Penguin(Messy) 0
liftedinfer -ptpe:	Penguin(Tweety) 0
liftedinfer -ptpe:	Flies(Messy) 0
liftedinfer -ptpe:	Flies(Tweety) 0
liftedinfer -ptpe:	Flies(Pennie) 0
liftedinfer -ptpe:	Bird(Messy) 0.913007
liftedinfer -ptpe:	Bird(Pennie) 0.913007
liftedinfer -lvg:	Penguin(Messy) 0
liftedinfer -lvg:	Penguin(Tweety) 0
liftedinfer -lvg:	Flies(Messy) 0.745255
liftedinfer -lvg:	Flies(Tweety) 0
liftedinfer -lvg:	Flies(Pennie) 0
liftedinfer -lvg:	Bird(Messy) 0
liftedinfer -lvg:	Bird(Pennie) 0.805195

*/

