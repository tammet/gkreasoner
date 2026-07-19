bird(tweety).
penguin(opus).
bird(X) :- penguin(X).
nonflies(X) :- penguin(X).
flies(X) :- bird(X), not nonflies(X).

flies(tweety)?
