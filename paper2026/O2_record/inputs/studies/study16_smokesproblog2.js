// smoking social network example from problog


/*

0.3::stress(X) :- person(X).
0.2::influences(X,Y) :- person(X), person(Y).

smokes(X) :- stress(X).
smokes(X) :- friend(X,Y), influences(Y,X), smokes(Y).

0.4::asthma(X) :- smokes(X).

person(1).
person(2).
person(3).
person(4).

friend(1,2).
friend(2,1).
friend(2,4).
friend(3,2).
friend(4,2).

evidence(smokes(2),true).
evidence(influences(4,2),false).

query(smokes(1)).
query(smokes(3)).
query(smokes(4)).
query(asthma(1)).
query(asthma(2)).
query(asthma(3)).
query(asthma(4)).

result:

asthma(1)	 0.20350877
asthma(2)	 0.4
asthma(3)	 0.176
asthma(4)	 0.176
smokes(1)	 0.50877193
smokes(3)	 0.44
smokes(4)	 0.44 
*/

[
{"@confidence": 0.3, "@logic": [["person","?:X"],"=>",["stress","?:X"]]},
{"@confidence": 0.2, "@logic": [[["person","?:X"],"&",["person","?:Y"]],"=>",["influences","?:X","?:Y"]]},

{"@confidence": 1.0, "@logic": [["stress","?:X"],"=>",["smokes","?:X"]]},
{"@confidence": 1.0, "@logic": [[["friend","?:X","?:Y"],"&",["influences","?:Y","?:X"]],"=>",["smokes","?:Y"]]},

{"@confidence": 0.4, "@logic": [["smokes","?:X"],"=>",["asthma","?:X"]]},

{"@confidence": 1.0, "@logic": ["person",1]},
{"@confidence": 1.0, "@logic": ["person",2]},
{"@confidence": 1.0, "@logic": ["person",3]},
{"@confidence": 1.0, "@logic": ["person",4]},

{"@confidence": 1.0, "@logic": ["friend",1,2]},
{"@confidence": 1.0, "@logic": ["friend",2,1]},
{"@confidence": 1.0, "@logic": ["friend",2,4]},
{"@confidence": 1.0, "@logic": ["friend",3,2]},
{"@confidence": 1.0, "@logic": ["friend",4,2]},

{"@confidence": 1.0, "@logic": ["smokes",2]},
{"@confidence": 1.0, "@logic": ["-influences",4,2]},

{"@question": ["asthma","?:X"]}
]

/*

{"result": "proof found",

"answers": [
{
"answer": [["$ans",3]],
"confidence": 0.12,
"positive_proof":
[
[1,      4, ["in", "frm_5", "axiom", 0.4, 0, []], [["-smokes","?:X"], ["asthma","?:X"]]],
[2,      0, ["in", "frm_1", "axiom", 0.3, 0, []], [["-person","?:X"], ["stress","?:X"]]],
[3,      7, ["in", "frm_8", "axiom", 1, 0, []], [["person",3]]],
[4,     20, ["mp", 2, 3, "fromaxiom", 0.3, 0, [0,7]], [["stress",3]]],
[5,      2, ["in", "frm_3", "axiom", 1, 0, []], [["-stress","?:X"], ["smokes","?:X"]]],
[6,     24, ["mp", 4, 5, "fromaxiom", 0.3, 0, [0,7,2]], [["smokes",3]]],
[7,     25, ["mp", 1, 6, "fromaxiom", 0.12, 0, [4,0,7,2]], [["asthma",3]]],
[8,     16, ["in", "frm_17", "goal", 1, 0, []], [["-asthma","?:X"], ["$ans","?:X"]]],
[9,     30, ["mp", 7, 8, "fromgoal", 0.12, 0, [4,0,7,2]], [["$ans",3]]]
]},
{
"answer": [["$ans",4]],
"confidence": 0.16224,
"positive_proof":
[
[1,      3, ["in", "frm_4", "axiom", 1, 0, []], [["-friend","?:X","?:Y"], ["-influences","?:Y","?:X"], ["smokes","?:Y"]]],
[2,      1, ["in", "frm_2", "axiom", 0.2, 0, []], [["influences","?:X","?:Y"], ["-person","?:Y"], ["-person","?:X"]]],
[3,      6, ["in", "frm_7", "axiom", 1, 0, []], [["person",2]]],
[4,     36, ["mp", [2,1], 3, "fromaxiom", 0.2, 0, [1,6]], [["influences","?:X",2], ["-person","?:X"]]],
[5,      8, ["in", "frm_9", "axiom", 1, 0, []], [["person",4]]],
[6,     46, ["mp", [4,1], 5, "fromaxiom", 0.2, 0, [1,6,8]], [["influences",4,2]]],
[7,     75, ["mp", [1,1], 6, "fromaxiom", 0.2, 0, [3,1,6,8]], [["-friend",2,4], ["smokes",4]]],
[8,     11, ["in", "frm_12", "axiom", 1, 0, []], [["friend",2,4]]],
[9,     76, ["simp", 7, 8, "fromaxiom", 0.2, 0, [3,1,6,8,11]], [["smokes",4]]],
[10,      4, ["in", "frm_5", "axiom", 0.4, 0, []], [["-smokes","?:X"], ["asthma","?:X"]]],
[11,     86, ["mp", 9, 10, "fromaxiom", 0.08, 0, [3,1,6,8,11,4]], [["asthma",4]]],
[12,     16, ["in", "frm_17", "goal", 1, 0, []], [["-asthma","?:X"], ["$ans","?:X"]]],
[13,     91, ["mp", 11, 12, "fromgoal", 0.08, 0, [3,1,6,8,11,4]], [["$ans",4]]],
[14,      4, ["in", "frm_5", "axiom", 0.4, 0, []], [["-smokes","?:X"], ["asthma","?:X"]]],
[15,      0, ["in", "frm_1", "axiom", 0.3, 0, []], [["-person","?:X"], ["stress","?:X"]]],
[16,      8, ["in", "frm_9", "axiom", 1, 0, []], [["person",4]]],
[17,     19, ["mp", 15, 16, "fromaxiom", 0.3, 0, [0,8]], [["stress",4]]],
[18,      2, ["in", "frm_3", "axiom", 1, 0, []], [["-stress","?:X"], ["smokes","?:X"]]],
[19,     23, ["mp", 17, 18, "fromaxiom", 0.3, 0, [0,8,2]], [["smokes",4]]],
[20,     26, ["mp", 14, 19, "fromaxiom", 0.12, 0, [4,0,8,2]], [["asthma",4]]],
[21,     16, ["in", "frm_17", "goal", 1, 0, []], [["-asthma","?:X"], ["$ans","?:X"]]],
[22,     31, ["mp", 20, 21, "fromgoal", 0.12, 0, [4,0,8,2]], [["$ans",4]]],
[23,     93, ["cumul", 13, 22, "fromgoal", 0.16224, 0, [3,1,6,8,11,4,0,2]], [["$ans",4]]]
]},
{
"answer": [["$ans",1]],
"confidence": 0.16224,
"positive_proof":
[
[1,      3, ["in", "frm_4", "axiom", 1, 0, []], [["-friend","?:X","?:Y"], ["-influences","?:Y","?:X"], ["smokes","?:Y"]]],
[2,      1, ["in", "frm_2", "axiom", 0.2, 0, []], [["influences","?:X","?:Y"], ["-person","?:Y"], ["-person","?:X"]]],
[3,      6, ["in", "frm_7", "axiom", 1, 0, []], [["person",2]]],
[4,     36, ["mp", [2,1], 3, "fromaxiom", 0.2, 0, [1,6]], [["influences","?:X",2], ["-person","?:X"]]],
[5,      5, ["in", "frm_6", "axiom", 1, 0, []], [["person",1]]],
[6,     45, ["mp", [4,1], 5, "fromaxiom", 0.2, 0, [1,6,5]], [["influences",1,2]]],
[7,     77, ["mp", [1,1], 6, "fromaxiom", 0.2, 0, [3,1,6,5]], [["-friend",2,1], ["smokes",1]]],
[8,     10, ["in", "frm_11", "axiom", 1, 0, []], [["friend",2,1]]],
[9,     78, ["simp", 7, 8, "fromaxiom", 0.2, 0, [3,1,6,5,10]], [["smokes",1]]],
[10,      4, ["in", "frm_5", "axiom", 0.4, 0, []], [["-smokes","?:X"], ["asthma","?:X"]]],
[11,     87, ["mp", 9, 10, "fromaxiom", 0.08, 0, [3,1,6,5,10,4]], [["asthma",1]]],
[12,     16, ["in", "frm_17", "goal", 1, 0, []], [["-asthma","?:X"], ["$ans","?:X"]]],
[13,     92, ["mp", 11, 12, "fromgoal", 0.08, 0, [3,1,6,5,10,4]], [["$ans",1]]],
[14,      4, ["in", "frm_5", "axiom", 0.4, 0, []], [["-smokes","?:X"], ["asthma","?:X"]]],
[15,      0, ["in", "frm_1", "axiom", 0.3, 0, []], [["-person","?:X"], ["stress","?:X"]]],
[16,      5, ["in", "frm_6", "axiom", 1, 0, []], [["person",1]]],
[17,     18, ["mp", 15, 16, "fromaxiom", 0.3, 0, [0,5]], [["stress",1]]],
[18,      2, ["in", "frm_3", "axiom", 1, 0, []], [["-stress","?:X"], ["smokes","?:X"]]],
[19,     22, ["mp", 17, 18, "fromaxiom", 0.3, 0, [0,5,2]], [["smokes",1]]],
[20,     27, ["mp", 14, 19, "fromaxiom", 0.12, 0, [4,0,5,2]], [["asthma",1]]],
[21,     16, ["in", "frm_17", "goal", 1, 0, []], [["-asthma","?:X"], ["$ans","?:X"]]],
[22,     32, ["mp", 20, 21, "fromgoal", 0.12, 0, [4,0,5,2]], [["$ans",1]]],
[23,     94, ["cumul", 13, 22, "fromgoal", 0.16224, 0, [3,1,6,5,10,4,0,2]], [["$ans",1]]]
]},
{
"answer": [["$ans",2]],
"confidence": 0.518656,
"positive_proof":
[
[1,      3, ["in", "frm_4", "axiom", 1, 0, []], [["-friend","?:X","?:Y"], ["-influences","?:Y","?:X"], ["smokes","?:Y"]]],
[2,      1, ["in", "frm_2", "axiom", 0.2, 0, []], [["influences","?:X","?:Y"], ["-person","?:Y"], ["-person","?:X"]]],
[3,      5, ["in", "frm_6", "axiom", 1, 0, []], [["person",1]]],
[4,     37, ["mp", [2,1], 3, "fromaxiom", 0.2, 0, [1,5]], [["influences","?:X",1], ["-person","?:X"]]],
[5,      6, ["in", "frm_7", "axiom", 1, 0, []], [["person",2]]],
[6,     50, ["mp", [4,1], 5, "fromaxiom", 0.2, 0, [1,5,6]], [["influences",2,1]]],
[7,     72, ["mp", [1,1], 6, "fromaxiom", 0.2, 0, [3,1,5,6]], [["-friend",1,2], ["smokes",2]]],
[8,      9, ["in", "frm_10", "axiom", 1, 0, []], [["friend",1,2]]],
[9,     73, ["simp", 7, 8, "fromaxiom", 0.2, 0, [3,1,5,6,9]], [["smokes",2]]],
[10,      4, ["in", "frm_5", "axiom", 0.4, 0, []], [["-smokes","?:X"], ["asthma","?:X"]]],
[11,     85, ["mp", 9, 10, "fromaxiom", 0.08, 0, [3,1,5,6,9,4]], [["asthma",2]]],
[12,     16, ["in", "frm_17", "goal", 1, 0, []], [["-asthma","?:X"], ["$ans","?:X"]]],
[13,     90, ["mp", 11, 12, "fromgoal", 0.08, 0, [3,1,5,6,9,4]], [["$ans",2]]],
[14,      4, ["in", "frm_5", "axiom", 0.4, 0, []], [["-smokes","?:X"], ["asthma","?:X"]]],
[15,      0, ["in", "frm_1", "axiom", 0.3, 0, []], [["-person","?:X"], ["stress","?:X"]]],
[16,      6, ["in", "frm_7", "axiom", 1, 0, []], [["person",2]]],
[17,     17, ["mp", 15, 16, "fromaxiom", 0.3, 0, [0,6]], [["stress",2]]],
[18,      2, ["in", "frm_3", "axiom", 1, 0, []], [["-stress","?:X"], ["smokes","?:X"]]],
[19,     21, ["mp", 17, 18, "fromaxiom", 0.3, 0, [0,6,2]], [["smokes",2]]],
[20,     28, ["mp", 14, 19, "fromaxiom", 0.12, 0, [4,0,6,2]], [["asthma",2]]],
[21,     16, ["in", "frm_17", "goal", 1, 0, []], [["-asthma","?:X"], ["$ans","?:X"]]],
[22,     33, ["mp", 20, 21, "fromgoal", 0.12, 0, [4,0,6,2]], [["$ans",2]]],
[23,     98, ["cumul", 13, 22, "fromgoal", 0.16224, 0, [3,1,5,6,9,4,0,2]], [["$ans",2]]],
[24,      4, ["in", "frm_5", "axiom", 0.4, 0, []], [["-smokes","?:X"], ["asthma","?:X"]]],
[25,     14, ["in", "frm_15", "axiom", 1, 0, []], [["smokes",2]]],
[26,     29, ["mp", 24, 25, "fromaxiom", 0.4, 0, [4,14]], [["asthma",2]]],
[27,     16, ["in", "frm_17", "goal", 1, 0, []], [["-asthma","?:X"], ["$ans","?:X"]]],
[28,     34, ["mp", 26, 27, "fromgoal", 0.4, 0, [4,14]], [["$ans",2]]],
[29,    104, ["cumul", 23, 28, "fromgoal", 0.477875, 0, [3,1,5,6,9,4,0,2,14]], [["$ans",2]]],
[30,      3, ["in", "frm_4", "axiom", 1, 0, []], [["-friend","?:X","?:Y"], ["-influences","?:Y","?:X"], ["smokes","?:Y"]]],
[31,      1, ["in", "frm_2", "axiom", 0.2, 0, []], [["influences","?:X","?:Y"], ["-person","?:Y"], ["-person","?:X"]]],
[32,      7, ["in", "frm_8", "axiom", 1, 0, []], [["person",3]]],
[33,     39, ["mp", [31,1], 32, "fromaxiom", 0.2, 0, [1,7]], [["influences","?:X",3], ["-person","?:X"]]],
[34,      6, ["in", "frm_7", "axiom", 1, 0, []], [["person",2]]],
[35,     58, ["mp", [33,1], 34, "fromaxiom", 0.2, 0, [1,7,6]], [["influences",2,3]]],
[36,     64, ["mp", [30,1], 35, "fromaxiom", 0.2, 0, [3,1,7,6]], [["-friend",3,2], ["smokes",2]]],
[37,     12, ["in", "frm_13", "axiom", 1, 0, []], [["friend",3,2]]],
[38,     65, ["simp", 36, 37, "fromaxiom", 0.2, 0, [3,1,7,6,12]], [["smokes",2]]],
[39,      4, ["in", "frm_5", "axiom", 0.4, 0, []], [["-smokes","?:X"], ["asthma","?:X"]]],
[40,     83, ["mp", 38, 39, "fromaxiom", 0.08, 0, [3,1,7,6,12,4]], [["asthma",2]]],
[41,     16, ["in", "frm_17", "goal", 1, 0, []], [["-asthma","?:X"], ["$ans","?:X"]]],
[42,     88, ["mp", 40, 41, "fromgoal", 0.08, 0, [3,1,7,6,12,4]], [["$ans",2]]],
[43,    113, ["cumul", 29, 42, "fromgoal", 0.497368, 0, [3,1,5,6,9,4,0,2,14,7,12]], [["$ans",2]]],
[44,      3, ["in", "frm_4", "axiom", 1, 0, []], [["-friend","?:X","?:Y"], ["-influences","?:Y","?:X"], ["smokes","?:Y"]]],
[45,      1, ["in", "frm_2", "axiom", 0.2, 0, []], [["influences","?:X","?:Y"], ["-person","?:Y"], ["-person","?:X"]]],
[46,      8, ["in", "frm_9", "axiom", 1, 0, []], [["person",4]]],
[47,     38, ["mp", [45,1], 46, "fromaxiom", 0.2, 0, [1,8]], [["influences","?:X",4], ["-person","?:X"]]],
[48,      6, ["in", "frm_7", "axiom", 1, 0, []], [["person",2]]],
[49,     54, ["mp", [47,1], 48, "fromaxiom", 0.2, 0, [1,8,6]], [["influences",2,4]]],
[50,     68, ["mp", [44,1], 49, "fromaxiom", 0.2, 0, [3,1,8,6]], [["-friend",4,2], ["smokes",2]]],
[51,     13, ["in", "frm_14", "axiom", 1, 0, []], [["friend",4,2]]],
[52,     69, ["simp", 50, 51, "fromaxiom", 0.2, 0, [3,1,8,6,13]], [["smokes",2]]],
[53,      4, ["in", "frm_5", "axiom", 0.4, 0, []], [["-smokes","?:X"], ["asthma","?:X"]]],
[54,     84, ["mp", 52, 53, "fromaxiom", 0.08, 0, [3,1,8,6,13,4]], [["asthma",2]]],
[55,     16, ["in", "frm_17", "goal", 1, 0, []], [["-asthma","?:X"], ["$ans","?:X"]]],
[56,     89, ["mp", 54, 55, "fromgoal", 0.08, 0, [3,1,8,6,13,4]], [["$ans",2]]],
[57,    125, ["cumul", 43, 56, "fromgoal", 0.518656, 0, [3,1,5,6,9,4,0,2,14,7,12,8,13]], [["$ans",2]]]
]}
]}

*/