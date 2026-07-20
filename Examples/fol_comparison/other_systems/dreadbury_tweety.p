% tweety_signature constant comp_than
% tweety_signature constant hate
% tweety_signature constant in
% tweety_signature constant kill
% tweety_signature constant live
% tweety_signature constant q_auntagatha
% tweety_signature constant q_butler
% tweety_signature constant q_charles
% tweety_signature constant q_dreadburymansion
% tweety_signature constant rich
% tweety_signature constant sk1
% tweety_signature constant sk2
% tweety_signature constant sk3
% tweety_signature functor sk4 1
% tweety_signature functor sk5 2
% tweety_signature functor sk6 1
% tweety_signature functor sk7 1
% tweety_signature functor sk8 1
% tweety_signature functor sk9 3
% tweety_signature predicate modifier_pp 3
% tweety_signature predicate predicate1 3
% tweety_signature predicate predicate2 4
% tweety_signature predicate property2 4

fof(background,axiom,(q_auntagatha != q_butler)).
fof(background,axiom,(! [VA,VB] : (~predicate2(VA,hate,VB,sk4(VB))))).
fof(background,axiom,(! [VA,VB] : (predicate2(sk5(VA,VB),hate,q_butler,VB) | ~predicate2(VA,hate,q_auntagatha,VB)))).
fof(background,axiom,(! [VA] : (property2(sk7(VA),rich,comp_than,q_auntagatha) | predicate2(sk6(VA),hate,q_butler,VA)))).
fof(background,axiom,(! [VA] : (VA = sk7(VA) | predicate2(sk6(VA),hate,q_butler,VA)))).
fof(background,axiom,(! [VA] : (predicate2(sk8(VA),hate,q_auntagatha,VA) | VA = q_butler))).
fof(background,axiom,(! [VA] : (~predicate2(VA,hate,q_auntagatha,q_butler)))).
fof(background,axiom,(! [VA,VB,VC] : (~predicate2(VA,hate,q_charles,VB) | ~predicate2(VC,hate,q_auntagatha,VB)))).
fof(background,axiom,(! [VA,VB,VC,VD] : (VA != VB | ~property2(VB,rich,comp_than,VC) | ~predicate2(VD,kill,VA,VC)))).
fof(background,axiom,(! [VA,VB,VC] : (predicate2(sk9(VA,VB,VC),hate,VA,VC) | ~predicate2(VB,kill,VA,VC)))).
fof(background,axiom,(! [VA,VB] : (VA = q_charles | VA = q_butler | VA = q_auntagatha | ~modifier_pp(VB,in,q_dreadburymansion) | ~predicate1(VB,live,VA)))).
fof(background,axiom,(predicate2(sk3,kill,sk2,q_auntagatha))).
fof(background,axiom,(modifier_pp(sk1,in,q_dreadburymansion))).
fof(background,axiom,(predicate1(sk1,live,sk2))).
fof(prove,conjecture,(predicate2(sk3,kill,q_auntagatha,q_auntagatha))).
