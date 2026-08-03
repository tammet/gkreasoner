% Transitivity variant for s(CASP); the recorded run did not finish. This
% input contains no function-symbol rule; gbirds_trans.js has one.

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
