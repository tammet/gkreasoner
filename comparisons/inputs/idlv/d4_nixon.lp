quaker(nixon).
republican(nixon).

pacifist(nixon) :- quaker(nixon), not nonpacifist(nixon).
nonpacifist(nixon) :- republican(nixon), not pacifist(nixon).
