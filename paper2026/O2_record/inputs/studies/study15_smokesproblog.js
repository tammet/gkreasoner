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

{"@question": ["smokes","?:X"]}
]

/*
*/