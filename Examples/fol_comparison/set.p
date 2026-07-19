% Clausified from GKC's Examples/set.txt. The original negated conjecture has
% been restored as the positive query expected by gk.

cnf(subsets_are_set_equal_sets,axiom,(~subset(X0,X1) | ~subset(X1,X0) | equal_sets(X1,X0))).
cnf(set_equal_sets_are_subsets2,axiom,(subset(X0,X1) | ~equal_sets(X1,X0))).
cnf(membership_in_subsets,axiom,(~subset(X0,X1) | member(X2,X1) | ~member(X2,X0))).
cnf(set_equal_sets_are_subsets1,axiom,(subset(X0,X1) | ~equal_sets(X0,X1))).
cnf(subsets_axiom2,axiom,(subset(X0,X1) | ~member(member_of_1_not_of_2(X0,X1),X1))).
cnf(subsets_axiom1,axiom,(member(member_of_1_not_of_2(X0,X1),X0) | subset(X0,X1))).
cnf(member_of_union_is_member_of_one_set,axiom,(~member(X0,X1) | member(X0,X2) | member(X0,X3) | ~union(X3,X2,X1))).
cnf(member_of_set1_is_member_of_union,axiom,(~union(X0,X1,X2) | ~member(X3,X0) | member(X3,X2))).
cnf(union_axiom2,axiom,(~member(g(X0,X1,X2),X2) | union(X0,X1,X2) | ~member(g(X0,X1,X2),X0))).
cnf(union_axiom3,axiom,(~member(g(X0,X1,X2),X1) | ~member(g(X0,X1,X2),X2) | union(X0,X1,X2))).
cnf(union_axiom1,axiom,(member(g(X0,X1,X2),X0) | member(g(X0,X1,X2),X1) | member(g(X0,X1,X2),X2) | union(X0,X1,X2))).
cnf(member_of_set2_is_member_of_union,axiom,(~member(X0,X1) | member(X0,X2) | ~union(X3,X1,X2))).
cnf(intersection_axiom1,axiom,(member(h(X0,X1,X2),X0) | intersection(X0,X1,X2) | member(h(X0,X1,X2),X2))).
cnf(member_of_both_is_member_of_intersection,axiom,(~intersection(X0,X1,X2) | ~member(X3,X1) | ~member(X3,X0) | member(X3,X2))).
cnf(member_of_intersection_is_member_of_set2,axiom,(~intersection(X0,X1,X2) | member(X3,X1) | ~member(X3,X2))).
cnf(member_of_intersection_is_member_of_set1,axiom,(~member(X0,X1) | member(X0,X2) | ~intersection(X2,X3,X1))).
cnf(intersection_axiom2,axiom,(member(h(X0,X1,X2),X1) | intersection(X0,X1,X2) | member(h(X0,X1,X2),X2))).
cnf(intersection_axiom3,axiom,(intersection(X0,X1,X2) | ~member(h(X0,X1,X2),X0) | ~member(h(X0,X1,X2),X1) | ~member(h(X0,X1,X2),X2))).
cnf(difference_axiom1,axiom,(difference(X0,X1,X2) | member(k(X0,X1,X2),X2) | ~member(k(X0,X1,X2),X1))).
cnf(member_of_difference,axiom,(~member(X0,X1) | member(X0,X2) | ~difference(X2,X3,X1))).
cnf(difference_axiom3,axiom,(difference(X0,X1,X2) | member(k(X0,X1,X2),X1) | ~member(k(X0,X1,X2),X0) | ~member(k(X0,X1,X2),X2))).
cnf(not_member_of_difference,axiom,(~member(X0,X1) | ~difference(X2,X3,X1) | ~member(X0,X3))).
cnf(difference_axiom2,axiom,(member(k(X0,X1,X2),X2) | member(k(X0,X1,X2),X0) | difference(X0,X1,X2))).
cnf(member_of_difference_or_set2,axiom,(~member(X0,X1) | member(X0,X2) | member(X0,X3) | ~difference(X1,X2,X3))).
cnf(a_intersection_b,assumption,(intersection(a,b,aIb))).
cnf(c_minus_a,assumption,(difference(c,a,cDa))).
cnf(c_minus_b,assumption,(difference(c,b,cDb))).
cnf(c_minus_aIb,assumption,(difference(c,aIb,cD_aIb))).
cnf(prove_cDa_union_cDb_is_cD_aIb,conjecture,(union(cDa,cDb,cD_aIb))).
