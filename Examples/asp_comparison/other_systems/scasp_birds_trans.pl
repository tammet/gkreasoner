% Historical transitivity variant for s(CASP) 0.21.10.09. The recorded run did not
% finish. Unlike gbirds_trans.js, this input contains no function-symbol rule.

father(b1,b2).
father(p1,p2).

bird(b1).
penguin(p1).

bird(X) :- penguin(X).
flies(X) :- bird(X), not -flies(X).
-flies(X) :- penguin(X).

anc(X,Y) :- father(X,Y).
anc(X,Y) :- anc(X,Z), anc(Z,Y).

penguin(X) :- anc(Y,X), penguin(Y).

?- flies(b1).
