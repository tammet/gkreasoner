% X1: an uncertain contradictory pair beside an unrelated crisp fact.
% Strong negation carries the contradiction; the joint world has no
% stable model.
p(a) :- &problog("0.7").
-p(a) :- &problog("0.6").
q(b).

&query(q(b)).
