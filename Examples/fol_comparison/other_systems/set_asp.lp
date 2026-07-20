% Mechanical Herbrand translation of set.p.
% Unbounded term generation preserves the source's function terms.

term(a).
term(aIb).
term(b).
term(c).
term(cD_aIb).
term(cDa).
term(cDb).
term(g(T0,T1,T2)) :- term(T0), term(T1), term(T2).
term(h(T0,T1,T2)) :- term(T0), term(T1), term(T2).
term(k(T0,T1,T2)) :- term(T0), term(T1), term(T2).
term(member_of_1_not_of_2(T0,T1)) :- term(T0), term(T1).

% subsets_are_set_equal_sets
equal_sets(X1,X0) :- subset(X0,X1), subset(X1,X0), term(X0), term(X1).
% set_equal_sets_are_subsets2
subset(X0,X1) :- equal_sets(X1,X0), term(X0), term(X1).
% membership_in_subsets
member(X2,X1) :- subset(X0,X1), member(X2,X0), term(X0), term(X1), term(X2).
% set_equal_sets_are_subsets1
subset(X0,X1) :- equal_sets(X0,X1), term(X0), term(X1).
% subsets_axiom2
subset(X0,X1) :- member(member_of_1_not_of_2(X0,X1),X1), term(X0), term(X1).
% subsets_axiom1
member(member_of_1_not_of_2(X0,X1),X0) | subset(X0,X1) :- term(X0), term(X1).
% member_of_union_is_member_of_one_set
member(X0,X2) | member(X0,X3) :- member(X0,X1), union(X3,X2,X1), term(X0), term(X1), term(X2), term(X3).
% member_of_set1_is_member_of_union
member(X3,X2) :- union(X0,X1,X2), member(X3,X0), term(X0), term(X1), term(X2), term(X3).
% union_axiom2
union(X0,X1,X2) :- member(g(X0,X1,X2),X2), member(g(X0,X1,X2),X0), term(X0), term(X1), term(X2).
% union_axiom3
union(X0,X1,X2) :- member(g(X0,X1,X2),X1), member(g(X0,X1,X2),X2), term(X0), term(X1), term(X2).
% union_axiom1
member(g(X0,X1,X2),X0) | member(g(X0,X1,X2),X1) | member(g(X0,X1,X2),X2) | union(X0,X1,X2) :- term(X0), term(X1), term(X2).
% member_of_set2_is_member_of_union
member(X0,X2) :- member(X0,X1), union(X3,X1,X2), term(X0), term(X1), term(X2), term(X3).
% intersection_axiom1
member(h(X0,X1,X2),X0) | intersection(X0,X1,X2) | member(h(X0,X1,X2),X2) :- term(X0), term(X1), term(X2).
% member_of_both_is_member_of_intersection
member(X3,X2) :- intersection(X0,X1,X2), member(X3,X1), member(X3,X0), term(X0), term(X1), term(X2), term(X3).
% member_of_intersection_is_member_of_set2
member(X3,X1) :- intersection(X0,X1,X2), member(X3,X2), term(X0), term(X1), term(X2), term(X3).
% member_of_intersection_is_member_of_set1
member(X0,X2) :- member(X0,X1), intersection(X2,X3,X1), term(X0), term(X1), term(X2), term(X3).
% intersection_axiom2
member(h(X0,X1,X2),X1) | intersection(X0,X1,X2) | member(h(X0,X1,X2),X2) :- term(X0), term(X1), term(X2).
% intersection_axiom3
intersection(X0,X1,X2) :- member(h(X0,X1,X2),X0), member(h(X0,X1,X2),X1), member(h(X0,X1,X2),X2), term(X0), term(X1), term(X2).
% difference_axiom1
difference(X0,X1,X2) | member(k(X0,X1,X2),X2) :- member(k(X0,X1,X2),X1), term(X0), term(X1), term(X2).
% member_of_difference
member(X0,X2) :- member(X0,X1), difference(X2,X3,X1), term(X0), term(X1), term(X2), term(X3).
% difference_axiom3
difference(X0,X1,X2) | member(k(X0,X1,X2),X1) :- member(k(X0,X1,X2),X0), member(k(X0,X1,X2),X2), term(X0), term(X1), term(X2).
% not_member_of_difference
:- member(X0,X1), difference(X2,X3,X1), member(X0,X3), term(X0), term(X1), term(X2), term(X3).
% difference_axiom2
member(k(X0,X1,X2),X2) | member(k(X0,X1,X2),X0) | difference(X0,X1,X2) :- term(X0), term(X1), term(X2).
% member_of_difference_or_set2
member(X0,X2) | member(X0,X3) :- member(X0,X1), difference(X1,X2,X3), term(X0), term(X1), term(X2), term(X3).
% a_intersection_b
intersection(a,b,aIb).
% c_minus_a
difference(c,a,cDa).
% c_minus_b
difference(c,b,cDb).
% c_minus_aIb
difference(c,aIb,cD_aIb).

% Query: union(cDa,cDb,cD_aIb)
% ProbLog reads this as its query directive. ASP systems treat it
% as an unrelated fact, which does not affect the queried predicate.
query(union(cDa,cDb,cD_aIb)).
