% GKC clausification of the Dreadbury problem. sk3 is the event witness
% introduced for the killing asserted in the background theory.

cnf(background,axiom,('AuntAgatha' != 'Butler')).
cnf(background,axiom,(~predicate2(X0,hate,X1,sk4(X1)))).
cnf(background,axiom,(predicate2(sk5(X0,X1),hate,'Butler',X1) | ~predicate2(X0,hate,'AuntAgatha',X1))).
cnf(background,axiom,(property2(sk7(X0),rich,comp_than,'AuntAgatha') | predicate2(sk6(X0),hate,'Butler',X0))).
cnf(background,axiom,(X0 = sk7(X0) | predicate2(sk6(X0),hate,'Butler',X0))).
cnf(background,axiom,(predicate2(sk8(X0),hate,'AuntAgatha',X0) | X0 = 'Butler')).
cnf(background,axiom,(~predicate2(X0,hate,'AuntAgatha','Butler'))).
cnf(background,axiom,(~predicate2(X0,hate,'Charles',X1) | ~predicate2(X2,hate,'AuntAgatha',X1))).
cnf(background,axiom,(X0 != X1 | ~property2(X1,rich,comp_than,X2) | ~predicate2(X3,kill,X0,X2))).
cnf(background,axiom,(predicate2(sk9(X0,X1,X2),hate,X0,X2) | ~predicate2(X1,kill,X0,X2))).
cnf(background,axiom,(X0 = 'Charles' | X0 = 'Butler' | X0 = 'AuntAgatha' | ~modifier_pp(X1,in,'DreadburyMansion') | ~predicate1(X1,live,X0))).
cnf(background,axiom,(predicate2(sk3,kill,sk2,'AuntAgatha'))).
cnf(background,axiom,(modifier_pp(sk1,in,'DreadburyMansion'))).
cnf(background,axiom,(predicate1(sk1,live,sk2))).
cnf(prove,conjecture,(predicate2(sk3,kill,'AuntAgatha','AuntAgatha'))).
