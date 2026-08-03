% DJ1 crisp counterpart. s(CASP) has no disjunctive heads; the
% standard even-loop idiom states the disjunction, classical negation
% removes the opposed branch.
p(a) :- not q(a).
q(a) :- not p(a).
-p(a).
