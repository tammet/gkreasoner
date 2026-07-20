% tweety_signature constant a
% tweety_signature constant aIb
% tweety_signature constant b
% tweety_signature constant c
% tweety_signature constant cD_aIb
% tweety_signature constant cDa
% tweety_signature constant cDb
% tweety_signature functor g 3
% tweety_signature functor h 3
% tweety_signature functor k 3
% tweety_signature functor member_of_1_not_of_2 2
% tweety_signature predicate difference 3
% tweety_signature predicate equal_sets 2
% tweety_signature predicate intersection 3
% tweety_signature predicate member 2
% tweety_signature predicate subset 2
% tweety_signature predicate union 3

fof(subsets_are_set_equal_sets,axiom,(! [VA,VB] : (~subset(VA,VB) | ~subset(VB,VA) | equal_sets(VB,VA)))).
fof(set_equal_sets_are_subsets2,axiom,(! [VA,VB] : (subset(VA,VB) | ~equal_sets(VB,VA)))).
fof(membership_in_subsets,axiom,(! [VA,VB,VC] : (~subset(VA,VB) | member(VC,VB) | ~member(VC,VA)))).
fof(set_equal_sets_are_subsets1,axiom,(! [VA,VB] : (subset(VA,VB) | ~equal_sets(VA,VB)))).
fof(subsets_axiom2,axiom,(! [VA,VB] : (subset(VA,VB) | ~member(member_of_1_not_of_2(VA,VB),VB)))).
fof(subsets_axiom1,axiom,(! [VA,VB] : (member(member_of_1_not_of_2(VA,VB),VA) | subset(VA,VB)))).
fof(member_of_union_is_member_of_one_set,axiom,(! [VA,VB,VC,VD] : (~member(VA,VB) | member(VA,VC) | member(VA,VD) | ~union(VD,VC,VB)))).
fof(member_of_set1_is_member_of_union,axiom,(! [VA,VB,VC,VD] : (~union(VA,VB,VC) | ~member(VD,VA) | member(VD,VC)))).
fof(union_axiom2,axiom,(! [VA,VB,VC] : (~member(g(VA,VB,VC),VC) | union(VA,VB,VC) | ~member(g(VA,VB,VC),VA)))).
fof(union_axiom3,axiom,(! [VA,VB,VC] : (~member(g(VA,VB,VC),VB) | ~member(g(VA,VB,VC),VC) | union(VA,VB,VC)))).
fof(union_axiom1,axiom,(! [VA,VB,VC] : (member(g(VA,VB,VC),VA) | member(g(VA,VB,VC),VB) | member(g(VA,VB,VC),VC) | union(VA,VB,VC)))).
fof(member_of_set2_is_member_of_union,axiom,(! [VA,VB,VC,VD] : (~member(VA,VB) | member(VA,VC) | ~union(VD,VB,VC)))).
fof(intersection_axiom1,axiom,(! [VA,VB,VC] : (member(h(VA,VB,VC),VA) | intersection(VA,VB,VC) | member(h(VA,VB,VC),VC)))).
fof(member_of_both_is_member_of_intersection,axiom,(! [VA,VB,VC,VD] : (~intersection(VA,VB,VC) | ~member(VD,VB) | ~member(VD,VA) | member(VD,VC)))).
fof(member_of_intersection_is_member_of_set2,axiom,(! [VA,VB,VC,VD] : (~intersection(VA,VB,VC) | member(VD,VB) | ~member(VD,VC)))).
fof(member_of_intersection_is_member_of_set1,axiom,(! [VA,VB,VC,VD] : (~member(VA,VB) | member(VA,VC) | ~intersection(VC,VD,VB)))).
fof(intersection_axiom2,axiom,(! [VA,VB,VC] : (member(h(VA,VB,VC),VB) | intersection(VA,VB,VC) | member(h(VA,VB,VC),VC)))).
fof(intersection_axiom3,axiom,(! [VA,VB,VC] : (intersection(VA,VB,VC) | ~member(h(VA,VB,VC),VA) | ~member(h(VA,VB,VC),VB) | ~member(h(VA,VB,VC),VC)))).
fof(difference_axiom1,axiom,(! [VA,VB,VC] : (difference(VA,VB,VC) | member(k(VA,VB,VC),VC) | ~member(k(VA,VB,VC),VB)))).
fof(member_of_difference,axiom,(! [VA,VB,VC,VD] : (~member(VA,VB) | member(VA,VC) | ~difference(VC,VD,VB)))).
fof(difference_axiom3,axiom,(! [VA,VB,VC] : (difference(VA,VB,VC) | member(k(VA,VB,VC),VB) | ~member(k(VA,VB,VC),VA) | ~member(k(VA,VB,VC),VC)))).
fof(not_member_of_difference,axiom,(! [VA,VB,VC,VD] : (~member(VA,VB) | ~difference(VC,VD,VB) | ~member(VA,VD)))).
fof(difference_axiom2,axiom,(! [VA,VB,VC] : (member(k(VA,VB,VC),VC) | member(k(VA,VB,VC),VA) | difference(VA,VB,VC)))).
fof(member_of_difference_or_set2,axiom,(! [VA,VB,VC,VD] : (~member(VA,VB) | member(VA,VC) | member(VA,VD) | ~difference(VB,VC,VD)))).
fof(a_intersection_b,assumption,(intersection(a,b,aIb))).
fof(c_minus_a,assumption,(difference(c,a,cDa))).
fof(c_minus_b,assumption,(difference(c,b,cDb))).
fof(c_minus_aIb,assumption,(difference(c,aIb,cD_aIb))).
fof(prove_cDa_union_cDb_is_cD_aIb,conjecture,(union(cDa,cDb,cD_aIb))).
