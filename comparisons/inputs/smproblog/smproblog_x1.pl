% X1: an uncertain contradictory pair beside an unrelated crisp fact.
% The syntax has no classical negation and reads ":- body" as a
% directive, so a fresh atom and the odd-loop idiom state the
% incompatibility: a world holding both facts has no stable model and
% its mass goes to the inconsistency column.  The unrelated fact is
% written as a probability-1.0 fact because purely deterministic atoms
% are left out of the report.
0.7::p(a).
0.6::np(a).
inc :- p(a), np(a), \+ inc.
1.0::q(b).

query(q(b)).
