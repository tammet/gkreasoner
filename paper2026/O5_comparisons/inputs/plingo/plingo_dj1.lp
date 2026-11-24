% DJ1: an uncertain classical disjunction opposed on one disjunct.
p(a) ; q(a) :- &problog("0.8").
-p(a) :- &problog("0.9").

&query(q(a)).
