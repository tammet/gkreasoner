// from problog, mentioning
// Joerg Schoenfisch and Heiner Stuckenschmidt. Towards Large-Scale Probabilistic OBDA. SUM 2015,

/*

problog:

movie(X) :- moviedirectedbydirector(X,_).
movie(X) :- moviestaractor(X,_).
movie(X) :- movie_base(X).
moviedirectedbydirector(X,Y) :- directordirectedmovie(Y,X).
moviestaractor(X,Y) :- actorstarredinmovie(Y,X).
directordirectedmovie(X,Y) :- directordirectedmovie_base(X,Y).
actorstarredinmovie(X,Y) :- actorstarredinmovie_base(X,Y).

book(X) :- bookwriter(X,_).
book(X) :- book_base(X).
bookwriter(X,Y) :- bookwriter_base(X,Y).

0.9375::directordirectedmovie_base(ronhoward,abeautifulmind).
0.9959243650858862::movie_base(abeautifulmind).
0.9999990106516323::book_base(abeautifulmind).

0.9277725683823577::movie_base(casinoroyale).
0.9375::directordirectedmovie_base(martincampbell,casinoroyale).
0.99951171875::actorstarredinmovie_base(danielcraig,casinoroyale).
0.999996125::bookwriter_base(casinoroyale,ianfleming).
0.999998138106335::book_base(casinoroyale).

0.9375::actorstarredinmovie_base(dannyboyle,trainspotting).
0.9375::directordirectedmovie_base(dannyboyle,trainspotting).
0.9999995231628418::book_base(trainspotting).

0.9375::bookwriter_base(sleepyhollow,washingtonirving).
0.96875::actorstarredinmovie_base(christopherwalken,sleepyhollow).

0.9763532157207491::movie_base(theadventuresofrobinhood).
0.9999999999422124::bookwriter_base(theadventuresofrobinhood,howardpyle).

moviebook(X) :- movie(X), book(X).
query(moviebook(_)).

results: 

moviebook(abeautifulmind) 0.99974428
moviebook(casinoroyale)	 0.9999978
moviebook(sleepyhollow)	 0.90820312
moviebook(theadventuresofrobinhood)	 0.97635322
moviebook(trainspotting)	 0.99609328


*/

[

{"@confidence": 1.0, "@logic":[["moviedirectedbydirector","?:X","?:Y"],"=>",["movie","?:X"]]},
{"@confidence": 1.0, "@logic":[["moviestaractor","?:X","?:Y"],"=>",["movie","?:X"]]},
{"@confidence": 1.0, "@logic":[["movie_base","?:X"],"=>",["movie","?:X"]]},

{"@confidence": 1.0, "@logic":[["directordirectedmovie","?:X","?:Y"],"=>",["moviedirectedbydirector","?:Y","?:X"]]},
{"@confidence": 1.0, "@logic":[["actorstarredinmovie","?:X","?:Y"],"=>",["moviestaractor","?:Y","?:X"]]},
{"@confidence": 1.0, "@logic":[["directordirectedmovie_base","?:X","?:Y"],"=>",["directordirectedmovie","?:X","?:Y"]]},
{"@confidence": 1.0, "@logic":[["actorstarredinmovie_base","?:X","?:Y"],"=>",["actorstarredinmovie","?:X","?:Y"]]},

{"@confidence": 1.0, "@logic":[["bookwriter","?:X","?:Y"],"=>",["book","?:X"]]},
{"@confidence": 1.0, "@logic":[["book_base","?:X"],"=>",["book","?:X"]]},
{"@confidence": 1.0, "@logic":[["bookwriter_base","?:X","?:Y"],"=>",["bookwriter","?:X","?:Y"]]},


{"@confidence": 0.9375, "@logic":[["directordirectedmovie_base","ronhoward","abeautifulmind"]]},
{"@confidence": 0.9959243650858862, "@logic":[["movie_base","abeautifulmind"]]},
{"@confidence": 0.9999990106516323, "@logic":[["book_base","abeautifulmind"]]},

{"@confidence": 0.9277725683823577, "@logic":[["movie_base","casinoroyale"]]},
{"@confidence": 0.9375, "@logic":[["directordirectedmovie_base","martincampbell","casinoroyale"]]},
{"@confidence": 0.99951171875, "@logic":[["actorstarredinmovie_base","danielcraig","casinoroyale"]]},
{"@confidence": 0.999996125, "@logic":[["bookwriter_base","casinoroyale","ianfleming"]]},
{"@confidence": 0.999998138106335, "@logic":[["book_base","casinoroyale"]]},

{"@confidence": 0.9375, "@logic":[["bookwriter_base","sleepyhollow","washingtonirving"]]},
{"@confidence": 0.96875, "@logic":[["actorstarredinmovie_base","christopherwalken","sleepyhollow"]]},

{"@confidence": 0.9763532157207491, "@logic":[["movie_base","theadventuresofrobinhood"]]},
{"@confidence": 0.9999999999422124, "@logic":[["bookwriter_base","theadventuresofrobinhood","howardpyle"]]},


{"@confidence": 1.0, "@logic":[[["movie","?:X"],"&",["book","?:X"]],"=>",["moviebook","?:X"]]},

{"@question": ["moviebook","?:X"]}
]

/*

{"result": "proof found",

"answers": [
{
"answer": [["$ans","theadventuresofrobinhood"]],
"confidence": 0.976353,
"positive_proof":
[
[1, ["in", "frm_23", "axiom", 1], [["-book","?:X"], ["-movie","?:X"], ["moviebook","?:X"]]],
[2, ["in", "frm_10", "axiom", 1], [["-bookwriter_base","?:X","?:Y"], ["bookwriter","?:X","?:Y"]]],
[3, ["in", "frm_22", "axiom", 1], [["bookwriter_base","theadventuresofrobinhood","howardpyle"]]],
[4, ["mp", 2, 3, "fromaxiom", 1], [["bookwriter","theadventuresofrobinhood","howardpyle"]]],
[5, ["in", "frm_8", "axiom", 1], [["-bookwriter","?:X","?:Y"], ["book","?:X"]]],
[6, ["mp", 4, 5, "fromaxiom", 1], [["book","theadventuresofrobinhood"]]],
[7, ["mp", 1, 6, "fromaxiom", 1], [["-movie","theadventuresofrobinhood"], ["moviebook","theadventuresofrobinhood"]]],
[8, ["in", "frm_3", "axiom", 1], [["-movie_base","?:X"], ["movie","?:X"]]],
[9, ["in", "frm_21", "axiom", 0.976353], [["movie_base","theadventuresofrobinhood"]]],
[10, ["mp", 8, 9, "fromaxiom", 0.976353], [["movie","theadventuresofrobinhood"]]],
[11, ["simp", 7, 10, "fromaxiom", 0.976353], [["moviebook","theadventuresofrobinhood"]]],
[12, ["in", "frm_24", "goal", 1], [["-moviebook","?:X"], ["$ans","?:X"]]],
[13, ["mp", 11, 12, "fromgoal", 0.976353], [["$ans","theadventuresofrobinhood"]]]
]},
{
"answer": [["$ans","sleepyhollow"]],
"confidence": 0.908203,
"positive_proof":
[
[1, ["in", "frm_23", "axiom", 1], [["-book","?:X"], ["-movie","?:X"], ["moviebook","?:X"]]],
[2, ["in", "frm_10", "axiom", 1], [["-bookwriter_base","?:X","?:Y"], ["bookwriter","?:X","?:Y"]]],
[3, ["in", "frm_19", "axiom", 0.9375], [["bookwriter_base","sleepyhollow","washingtonirving"]]],
[4, ["mp", 2, 3, "fromaxiom", 0.9375], [["bookwriter","sleepyhollow","washingtonirving"]]],
[5, ["in", "frm_8", "axiom", 1], [["-bookwriter","?:X","?:Y"], ["book","?:X"]]],
[6, ["mp", 4, 5, "fromaxiom", 0.9375], [["book","sleepyhollow"]]],
[7, ["mp", 1, 6, "fromaxiom", 0.9375], [["-movie","sleepyhollow"], ["moviebook","sleepyhollow"]]],
[8, ["in", "frm_7", "axiom", 1], [["-actorstarredinmovie_base","?:X","?:Y"], ["actorstarredinmovie","?:X","?:Y"]]],
[9, ["in", "frm_20", "axiom", 0.96875], [["actorstarredinmovie_base","christopherwalken","sleepyhollow"]]],
[10, ["mp", 8, 9, "fromaxiom", 0.96875], [["actorstarredinmovie","christopherwalken","sleepyhollow"]]],
[11, ["in", "frm_5", "axiom", 1], [["-actorstarredinmovie","?:X","?:Y"], ["moviestaractor","?:Y","?:X"]]],
[12, ["mp", 10, 11, "fromaxiom", 0.96875], [["moviestaractor","sleepyhollow","christopherwalken"]]],
[13, ["in", "frm_2", "axiom", 1], [["-moviestaractor","?:X","?:Y"], ["movie","?:X"]]],
[14, ["mp", 12, 13, "fromaxiom", 0.96875], [["movie","sleepyhollow"]]],
[15, ["simp", 7, 14, "fromaxiom", 0.908203], [["moviebook","sleepyhollow"]]],
[16, ["in", "frm_24", "goal", 1], [["-moviebook","?:X"], ["$ans","?:X"]]],
[17, ["mp", 15, 16, "fromgoal", 0.908203], [["$ans","sleepyhollow"]]]
]},
{
"answer": [["$ans","abeautifulmind"]],
"confidence": 0.997834,
"positive_proof":
[
[1, ["in", "frm_23", "axiom", 1], [["-book","?:X"], ["-movie","?:X"], ["moviebook","?:X"]]],
[2, ["in", "frm_9", "axiom", 1], [["-book_base","?:X"], ["book","?:X"]]],
[3, ["in", "frm_13", "axiom", 0.999999], [["book_base","abeautifulmind"]]],
[4, ["mp", 2, 3, "fromaxiom", 0.999999], [["book","abeautifulmind"]]],
[5, ["mp", 1, 4, "fromaxiom", 0.999999], [["-movie","abeautifulmind"], ["moviebook","abeautifulmind"]]],
[6, ["in", "frm_6", "axiom", 1], [["-directordirectedmovie_base","?:X","?:Y"], ["directordirectedmovie","?:X","?:Y"]]],
[7, ["in", "frm_11", "axiom", 0.9375], [["directordirectedmovie_base","ronhoward","abeautifulmind"]]],
[8, ["mp", 6, 7, "fromaxiom", 0.9375], [["directordirectedmovie","ronhoward","abeautifulmind"]]],
[9, ["in", "frm_4", "axiom", 1], [["-directordirectedmovie","?:X","?:Y"], ["moviedirectedbydirector","?:Y","?:X"]]],
[10, ["mp", 8, 9, "fromaxiom", 0.9375], [["moviedirectedbydirector","abeautifulmind","ronhoward"]]],
[11, ["in", "frm_1", "axiom", 1], [["-moviedirectedbydirector","?:X","?:Y"], ["movie","?:X"]]],
[12, ["mp", 10, 11, "fromaxiom", 0.9375], [["movie","abeautifulmind"]]],
[13, ["mp", 5, 12, "fromaxiom", 0.937499], [["moviebook","abeautifulmind"]]],
[14, ["in", "frm_24", "goal", 1], [["-moviebook","?:X"], ["$ans","?:X"]]],
[15, ["mp", 13, 14, "fromgoal", 0.937499], [["$ans","abeautifulmind"]]],
[16, ["in", "frm_23", "axiom", 1], [["-book","?:X"], ["-movie","?:X"], ["moviebook","?:X"]]],
[17, ["in", "frm_9", "axiom", 1], [["-book_base","?:X"], ["book","?:X"]]],
[18, ["in", "frm_13", "axiom", 0.999999], [["book_base","abeautifulmind"]]],
[19, ["mp", 17, 18, "fromaxiom", 0.999999], [["book","abeautifulmind"]]],
[20, ["mp", 16, 19, "fromaxiom", 0.999999], [["-movie","abeautifulmind"], ["moviebook","abeautifulmind"]]],
[21, ["in", "frm_3", "axiom", 1], [["-movie_base","?:X"], ["movie","?:X"]]],
[22, ["in", "frm_12", "axiom", 0.995924], [["movie_base","abeautifulmind"]]],
[23, ["mp", 21, 22, "fromaxiom", 0.995924], [["movie","abeautifulmind"]]],
[24, ["simp", 20, 23, "fromaxiom", 0.995923], [["moviebook","abeautifulmind"]]],
[25, ["in", "frm_24", "goal", 1], [["-moviebook","?:X"], ["$ans","?:X"]]],
[26, ["mp", 24, 25, "fromgoal", 0.995923], [["$ans","abeautifulmind"]]],
[27, ["cumul", 15, 26, "fromgoal", 0.997834], [["$ans","abeautifulmind"]]]
]},
{
"answer": [["$ans","casinoroyale"]],
"confidence": 0.999962,
"positive_proof":
[
[1, ["in", "frm_23", "axiom", 1], [["-book","?:X"], ["-movie","?:X"], ["moviebook","?:X"]]],
[2, ["in", "frm_9", "axiom", 1], [["-book_base","?:X"], ["book","?:X"]]],
[3, ["in", "frm_18", "axiom", 0.999998], [["book_base","casinoroyale"]]],
[4, ["mp", 2, 3, "fromaxiom", 0.999998], [["book","casinoroyale"]]],
[5, ["mp", 1, 4, "fromaxiom", 0.999998], [["-movie","casinoroyale"], ["moviebook","casinoroyale"]]],
[6, ["in", "frm_7", "axiom", 1], [["-actorstarredinmovie_base","?:X","?:Y"], ["actorstarredinmovie","?:X","?:Y"]]],
[7, ["in", "frm_16", "axiom", 0.999512], [["actorstarredinmovie_base","danielcraig","casinoroyale"]]],
[8, ["mp", 6, 7, "fromaxiom", 0.999512], [["actorstarredinmovie","danielcraig","casinoroyale"]]],
[9, ["in", "frm_5", "axiom", 1], [["-actorstarredinmovie","?:X","?:Y"], ["moviestaractor","?:Y","?:X"]]],
[10, ["mp", 8, 9, "fromaxiom", 0.999512], [["moviestaractor","casinoroyale","danielcraig"]]],
[11, ["in", "frm_2", "axiom", 1], [["-moviestaractor","?:X","?:Y"], ["movie","?:X"]]],
[12, ["mp", 10, 11, "fromaxiom", 0.999512], [["movie","casinoroyale"]]],
[13, ["mp", 5, 12, "fromaxiom", 0.99951], [["moviebook","casinoroyale"]]],
[14, ["in", "frm_24", "goal", 1], [["-moviebook","?:X"], ["$ans","?:X"]]],
[15, ["mp", 13, 14, "fromgoal", 0.99951], [["$ans","casinoroyale"]]],
[16, ["in", "frm_23", "axiom", 1], [["-book","?:X"], ["-movie","?:X"], ["moviebook","?:X"]]],
[17, ["in", "frm_10", "axiom", 1], [["-bookwriter_base","?:X","?:Y"], ["bookwriter","?:X","?:Y"]]],
[18, ["in", "frm_17", "axiom", 0.999996], [["bookwriter_base","casinoroyale","ianfleming"]]],
[19, ["mp", 17, 18, "fromaxiom", 0.999996], [["bookwriter","casinoroyale","ianfleming"]]],
[20, ["in", "frm_8", "axiom", 1], [["-bookwriter","?:X","?:Y"], ["book","?:X"]]],
[21, ["mp", 19, 20, "fromaxiom", 0.999996], [["book","casinoroyale"]]],
[22, ["mp", 16, 21, "fromaxiom", 0.999996], [["-movie","casinoroyale"], ["moviebook","casinoroyale"]]],
[23, ["in", "frm_3", "axiom", 1], [["-movie_base","?:X"], ["movie","?:X"]]],
[24, ["in", "frm_14", "axiom", 0.927773], [["movie_base","casinoroyale"]]],
[25, ["mp", 23, 24, "fromaxiom", 0.927773], [["movie","casinoroyale"]]],
[26, ["simp", 22, 25, "fromaxiom", 0.927769], [["moviebook","casinoroyale"]]],
[27, ["in", "frm_24", "goal", 1], [["-moviebook","?:X"], ["$ans","?:X"]]],
[28, ["mp", 26, 27, "fromgoal", 0.927769], [["$ans","casinoroyale"]]],
[29, ["cumul", 15, 28, "fromgoal", 0.999895], [["$ans","casinoroyale"]]],
[30, ["in", "frm_23", "axiom", 1], [["-book","?:X"], ["-movie","?:X"], ["moviebook","?:X"]]],
[31, ["in", "frm_9", "axiom", 1], [["-book_base","?:X"], ["book","?:X"]]],
[32, ["in", "frm_18", "axiom", 0.999998], [["book_base","casinoroyale"]]],
[33, ["mp", 31, 32, "fromaxiom", 0.999998], [["book","casinoroyale"]]],
[34, ["mp", 30, 33, "fromaxiom", 0.999998], [["-movie","casinoroyale"], ["moviebook","casinoroyale"]]],
[35, ["in", "frm_6", "axiom", 1], [["-directordirectedmovie_base","?:X","?:Y"], ["directordirectedmovie","?:X","?:Y"]]],
[36, ["in", "frm_15", "axiom", 0.9375], [["directordirectedmovie_base","martincampbell","casinoroyale"]]],
[37, ["mp", 35, 36, "fromaxiom", 0.9375], [["directordirectedmovie","martincampbell","casinoroyale"]]],
[38, ["in", "frm_4", "axiom", 1], [["-directordirectedmovie","?:X","?:Y"], ["moviedirectedbydirector","?:Y","?:X"]]],
[39, ["mp", 37, 38, "fromaxiom", 0.9375], [["moviedirectedbydirector","casinoroyale","martincampbell"]]],
[40, ["in", "frm_1", "axiom", 1], [["-moviedirectedbydirector","?:X","?:Y"], ["movie","?:X"]]],
[41, ["mp", 39, 40, "fromaxiom", 0.9375], [["movie","casinoroyale"]]],
[42, ["mp", 34, 41, "fromaxiom", 0.937498], [["moviebook","casinoroyale"]]],
[43, ["in", "frm_24", "goal", 1], [["-moviebook","?:X"], ["$ans","?:X"]]],
[44, ["mp", 42, 43, "fromgoal", 0.937498], [["$ans","casinoroyale"]]],
[45, ["cumul", 29, 44, "fromgoal", 0.999962], [["$ans","casinoroyale"]]]
]}
]}


*/