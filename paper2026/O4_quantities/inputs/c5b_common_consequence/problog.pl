p(a) :- \+b(a).
b(a) :- \+p(a).
q :- p(a).
q :- b(a).
query(q).
