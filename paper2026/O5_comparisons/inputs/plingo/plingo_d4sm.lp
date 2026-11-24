quaker :- &problog("0.8").
republican :- &problog("0.6").

pacifist :- quaker, not nonpacifist.
nonpacifist :- republican, not pacifist.

&query(pacifist).
&query(nonpacifist).
