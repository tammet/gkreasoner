quaker(n).
republican(n).
pacifist_pos(n) :- quaker(n), \+pacifist_neg(n).
pacifist_neg(n) :- republican(n), \+pacifist_pos(n).
query(pacifist_pos(n)).
