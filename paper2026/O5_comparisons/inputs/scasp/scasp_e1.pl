% E1 crisp counterpart: equality carrying opposed evidence.  The
% substitution rules are written acyclically in the one direction the
% query needs: with the symmetric rule set of asp_e1.lp the
% goal-directed execution does not terminate.
p(a).
-p(b).
eq(a,b).
p(b) :- p(a), eq(a,b).
-p(a) :- -p(b), eq(a,b).
