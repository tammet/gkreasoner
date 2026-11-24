% Control: the content of the clingo skeleton (stage4/clingo_skeleton.lp of this part)
% in s(CASP) form: the disjunction gull | penguin as two rules with negation as failure. No report against gull.
bird(parent(X)) :- bird(X).
bird(X) :- bird(parent(X)).
bird(parent(parent(tweety))).
flies(X) :- bird(X), not penguin(X).
gull(X) :- seabird(X), not penguin(X).
penguin(X) :- seabird(X), not gull(X).
seabird(tweety).
