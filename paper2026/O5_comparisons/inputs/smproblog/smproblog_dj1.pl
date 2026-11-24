% DJ1: an uncertain classical disjunction opposed on one disjunct.
% The disjunction is stated by the standard even-loop idiom; the
% opposed disjunct uses a fresh atom and the odd-loop idiom, since the
% syntax has no classical negation and no ":- body" constraints.
0.8::d.
0.9::nd.
p(a) :- d, \+ q(a).
q(a) :- d, \+ p(a).
np(a) :- nd.
inc :- p(a), np(a), \+ inc.

query(q(a)).
