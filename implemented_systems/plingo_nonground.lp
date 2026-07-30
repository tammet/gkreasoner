n1_bird(a) :- &problog("0.5").
n1_bird(b) :- &problog("0.6").
n1_twobirds(X,Y) :- n1_bird(X), n1_bird(Y).

n2_stress(ann) :- &problog("0.8").
n2_stress(bob) :- &problog("0.4").
n2_influences(ann,bob) :- &problog("0.6").
n2_influences(bob,carl) :- &problog("0.2").
n2_smokes(X) :- n2_stress(X).
n2_smokes(X) :- n2_influences(Y,X), n2_smokes(Y).

&query(n1_twobirds(a,a)).
&query(n1_twobirds(a,b)).
&query(n1_twobirds(b,a)).
&query(n1_twobirds(b,b)).
&query(n2_smokes(ann)).
&query(n2_smokes(bob)).
&query(n2_smokes(carl)).
