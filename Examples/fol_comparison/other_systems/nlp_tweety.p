% tweety_signature constant proved
% tweety_signature constant sk4
% tweety_signature constant sk5
% tweety_signature constant sk6
% tweety_signature constant sk7
% tweety_signature constant sk8
% tweety_signature constant sk9
% tweety_signature functor sk1 2
% tweety_signature functor sk10 1
% tweety_signature functor sk11 1
% tweety_signature functor sk2 2
% tweety_signature functor sk3 4
% tweety_signature predicate abstraction 2
% tweety_signature predicate actual_world 1
% tweety_signature predicate agent 3
% tweety_signature predicate animate 2
% tweety_signature predicate artifact 2
% tweety_signature predicate barrel 2
% tweety_signature predicate be 4
% tweety_signature predicate car 2
% tweety_signature predicate chevy 2
% tweety_signature predicate city 2
% tweety_signature predicate dirty 2
% tweety_signature predicate down 3
% tweety_signature predicate entity 2
% tweety_signature predicate eventuality 2
% tweety_signature predicate evt_pred 2
% tweety_signature predicate existent 2
% tweety_signature predicate fellow 2
% tweety_signature predicate frontseat 2
% tweety_signature predicate furniture 2
% tweety_signature predicate general 2
% tweety_signature predicate goal 1
% tweety_signature predicate group 2
% tweety_signature predicate hollywood_placename 2
% tweety_signature predicate human 2
% tweety_signature predicate human_person 2
% tweety_signature predicate impartial 2
% tweety_signature predicate in 3
% tweety_signature predicate instrumentality 2
% tweety_signature predicate living 2
% tweety_signature predicate location 2
% tweety_signature predicate lonely 2
% tweety_signature predicate male 2
% tweety_signature predicate man 2
% tweety_signature predicate member 3
% tweety_signature predicate multiple 2
% tweety_signature predicate nonexistent 2
% tweety_signature predicate nonhuman 2
% tweety_signature predicate nonliving 2
% tweety_signature predicate object 2
% tweety_signature predicate of 3
% tweety_signature predicate old 2
% tweety_signature predicate organism 2
% tweety_signature predicate placename 2
% tweety_signature predicate present 2
% tweety_signature predicate relation 2
% tweety_signature predicate relname 2
% tweety_signature predicate seat 2
% tweety_signature predicate set 2
% tweety_signature predicate singleton 2
% tweety_signature predicate specific 2
% tweety_signature predicate state 2
% tweety_signature predicate street 2
% tweety_signature predicate thing 2
% tweety_signature predicate transport 2
% tweety_signature predicate two 2
% tweety_signature predicate unisex 2
% tweety_signature predicate vehicle 2
% tweety_signature predicate way 2
% tweety_signature predicate white 2
% tweety_signature predicate young 2

fof(ax1,axiom,(! [VA,VB] : (instrumentality(VA,VB) | ~furniture(VA,VB)))).
fof(ax2,axiom,(! [VA,VB] : (furniture(VA,VB) | ~seat(VA,VB)))).
fof(ax3,axiom,(! [VA,VB] : (seat(VA,VB) | ~frontseat(VA,VB)))).
fof(ax4,axiom,(! [VA,VB] : (object(VA,VB) | ~location(VA,VB)))).
fof(ax5,axiom,(! [VA,VB] : (location(VA,VB) | ~city(VA,VB)))).
fof(ax6,axiom,(! [VA,VB] : (placename(VA,VB) | ~hollywood_placename(VA,VB)))).
fof(ax7,axiom,(! [VA,VB] : (unisex(VA,VB) | ~abstraction(VA,VB)))).
fof(ax8,axiom,(! [VA,VB] : (general(VA,VB) | ~abstraction(VA,VB)))).
fof(ax9,axiom,(! [VA,VB] : (nonhuman(VA,VB) | ~abstraction(VA,VB)))).
fof(ax10,axiom,(! [VA,VB] : (thing(VA,VB) | ~abstraction(VA,VB)))).
fof(ax11,axiom,(! [VA,VB] : (abstraction(VA,VB) | ~relation(VA,VB)))).
fof(ax12,axiom,(! [VA,VB] : (relation(VA,VB) | ~relname(VA,VB)))).
fof(ax13,axiom,(! [VA,VB] : (relname(VA,VB) | ~placename(VA,VB)))).
fof(ax14,axiom,(! [VA,VB] : (artifact(VA,VB) | ~way(VA,VB)))).
fof(ax15,axiom,(! [VA,VB] : (way(VA,VB) | ~street(VA,VB)))).
fof(ax16,axiom,(! [VA,VB] : (unisex(VA,VB) | ~object(VA,VB)))).
fof(ax17,axiom,(! [VA,VB] : (impartial(VA,VB) | ~object(VA,VB)))).
fof(ax18,axiom,(! [VA,VB] : (nonliving(VA,VB) | ~object(VA,VB)))).
fof(ax19,axiom,(! [VA,VB] : (entity(VA,VB) | ~object(VA,VB)))).
fof(ax20,axiom,(! [VA,VB] : (object(VA,VB) | ~artifact(VA,VB)))).
fof(ax21,axiom,(! [VA,VB] : (artifact(VA,VB) | ~instrumentality(VA,VB)))).
fof(ax22,axiom,(! [VA,VB] : (instrumentality(VA,VB) | ~transport(VA,VB)))).
fof(ax23,axiom,(! [VA,VB] : (transport(VA,VB) | ~vehicle(VA,VB)))).
fof(ax24,axiom,(! [VA,VB] : (vehicle(VA,VB) | ~car(VA,VB)))).
fof(ax25,axiom,(! [VA,VB] : (car(VA,VB) | ~chevy(VA,VB)))).
fof(ax26,axiom,(! [VA,VB] : (evt_pred(VA,VB) | ~barrel(VA,VB)))).
fof(ax27,axiom,(! [VA,VB] : (eventuality(VA,VB) | ~evt_pred(VA,VB)))).
fof(ax28,axiom,(! [VA,VB] : (evt_pred(VA,VB) | ~state(VA,VB)))).
fof(ax29,axiom,(! [VA,VB] : (unisex(VA,VB) | ~eventuality(VA,VB)))).
fof(ax30,axiom,(! [VA,VB] : (nonexistent(VA,VB) | ~eventuality(VA,VB)))).
fof(ax31,axiom,(! [VA,VB] : (specific(VA,VB) | ~eventuality(VA,VB)))).
fof(ax32,axiom,(! [VA,VB] : (thing(VA,VB) | ~eventuality(VA,VB)))).
fof(ax33,axiom,(! [VA,VB] : (eventuality(VA,VB) | ~state(VA,VB)))).
fof(ax34,axiom,(! [VA,VB] : (group(VA,VB) | ~two(VA,VB)))).
fof(ax35,axiom,(! [VA,VB] : (multiple(VA,VB) | ~set(VA,VB)))).
fof(ax36,axiom,(! [VA,VB] : (set(VA,VB) | ~group(VA,VB)))).
fof(ax37,axiom,(! [VA,VB] : (male(VA,VB) | ~man(VA,VB)))).
fof(ax38,axiom,(! [VA,VB] : (animate(VA,VB) | ~human_person(VA,VB)))).
fof(ax39,axiom,(! [VA,VB] : (human(VA,VB) | ~human_person(VA,VB)))).
fof(ax40,axiom,(! [VA,VB] : (living(VA,VB) | ~organism(VA,VB)))).
fof(ax41,axiom,(! [VA,VB] : (impartial(VA,VB) | ~organism(VA,VB)))).
fof(ax42,axiom,(! [VA,VB] : (existent(VA,VB) | ~entity(VA,VB)))).
fof(ax43,axiom,(! [VA,VB] : (specific(VA,VB) | ~entity(VA,VB)))).
fof(ax44,axiom,(! [VA,VB] : (singleton(VA,VB) | ~thing(VA,VB)))).
fof(ax45,axiom,(! [VA,VB] : (thing(VA,VB) | ~entity(VA,VB)))).
fof(ax46,axiom,(! [VA,VB] : (entity(VA,VB) | ~organism(VA,VB)))).
fof(ax47,axiom,(! [VA,VB] : (organism(VA,VB) | ~human_person(VA,VB)))).
fof(ax48,axiom,(! [VA,VB] : (human_person(VA,VB) | ~man(VA,VB)))).
fof(ax49,axiom,(! [VA,VB] : (man(VA,VB) | ~fellow(VA,VB)))).
fof(ax50,axiom,(! [VA,VB] : (~nonliving(VA,VB) | ~animate(VA,VB)))).
fof(ax51,axiom,(! [VA,VB] : (~nonexistent(VA,VB) | ~existent(VA,VB)))).
fof(ax52,axiom,(! [VA,VB] : (~human(VA,VB) | ~nonhuman(VA,VB)))).
fof(ax53,axiom,(! [VA,VB] : (~living(VA,VB) | ~nonliving(VA,VB)))).
fof(ax54,axiom,(! [VA,VB] : (~multiple(VA,VB) | ~singleton(VA,VB)))).
fof(ax55,axiom,(! [VA,VB] : (~general(VA,VB) | ~specific(VA,VB)))).
fof(ax56,axiom,(! [VA,VB] : (~male(VA,VB) | ~unisex(VA,VB)))).
fof(ax57,axiom,(! [VA,VB] : (~old(VA,VB) | ~young(VA,VB)))).
fof(ax58,axiom,(! [VA,VB,VC,VD] : (~of(VA,VB,VC) | VB = VD | ~placename(VA,VB) | ~of(VA,VD,VC) | ~placename(VA,VD) | ~entity(VA,VC)))).
fof(ax59,axiom,(! [VA,VB,VC,VD] : (VA = VB | ~be(VC,VD,VA,VB)))).
fof(ax60,axiom,(! [VA,VB] : (member(VA,sk1(VB,VA),VB) | ~two(VA,VB)))).
fof(ax60,axiom,(! [VA,VB,VC] : (VA = sk1(VB,VC) | VA = sk2(VB,VC) | ~member(VC,VA,VB) | ~two(VC,VB)))).
fof(ax60,axiom,(! [VA,VB] : (sk2(VA,VB) != sk1(VA,VB) | ~two(VB,VA)))).
fof(ax60,axiom,(! [VA,VB] : (member(VA,sk2(VB,VA),VB) | ~two(VA,VB)))).
fof(ax60,axiom,(! [VA,VB,VC,VD] : (member(VA,sk3(VB,VA,VC,VD),VB) | VD = VC | ~member(VA,VD,VB) | ~member(VA,VC,VB) | two(VA,VB)))).
fof(ax60,axiom,(! [VA,VB,VC,VD] : (sk3(VA,VB,VC,VD) != VC | VD = VC | ~member(VB,VD,VA) | ~member(VB,VC,VA) | two(VB,VA)))).
fof(ax60,axiom,(! [VA,VB,VC,VD] : (sk3(VA,VB,VC,VD) != VD | VD = VC | ~member(VB,VD,VA) | ~member(VB,VC,VA) | two(VB,VA)))).
fof(ax61,axiom,(! [VA,VB] : (~member(VA,VB,VB)))).
fof(co1,axiom,(actual_world(sk4) | goal(proved))).
fof(co1,axiom,(! [VA] : (young(sk4,VA) | ~member(sk4,VA,sk9) | goal(proved)))).
fof(co1,axiom,(! [VA] : (fellow(sk4,VA) | ~member(sk4,VA,sk9) | goal(proved)))).
fof(co1,axiom,(group(sk4,sk9) | goal(proved))).
fof(co1,axiom,(two(sk4,sk9) | goal(proved))).
fof(co1,axiom,(! [VA] : (in(sk4,sk11(VA),sk11(VA)) | ~member(sk4,VA,sk9) | goal(proved)))).
fof(co1,axiom,(! [VA] : (be(sk4,sk10(VA),VA,sk11(VA)) | ~member(sk4,VA,sk9) | goal(proved)))).
fof(co1,axiom,(! [VA] : (state(sk4,sk10(VA)) | ~member(sk4,VA,sk9) | goal(proved)))).
fof(co1,axiom,(! [VA] : (frontseat(sk4,sk11(VA)) | ~member(sk4,VA,sk9) | goal(proved)))).
fof(co1,axiom,(in(sk4,sk8,sk7) | goal(proved))).
fof(co1,axiom,(down(sk4,sk8,sk5) | goal(proved))).
fof(co1,axiom,(barrel(sk4,sk8) | goal(proved))).
fof(co1,axiom,(present(sk4,sk8) | goal(proved))).
fof(co1,axiom,(agent(sk4,sk8,sk7) | goal(proved))).
fof(co1,axiom,(evt_pred(sk4,sk8) | goal(proved))).
fof(co1,axiom,(old(sk4,sk7) | goal(proved))).
fof(co1,axiom,(dirty(sk4,sk7) | goal(proved))).
fof(co1,axiom,(white(sk4,sk7) | goal(proved))).
fof(co1,axiom,(chevy(sk4,sk7) | goal(proved))).
fof(co1,axiom,(placename(sk4,sk6) | goal(proved))).
fof(co1,axiom,(hollywood_placename(sk4,sk6) | goal(proved))).
fof(co1,axiom,(city(sk4,sk7) | goal(proved))).
fof(co1,axiom,(of(sk4,sk6,sk7) | goal(proved))).
fof(co1,axiom,(lonely(sk4,sk5) | goal(proved))).
fof(co1,axiom,(street(sk4,sk5) | goal(proved))).
fof(frm_63,conjecture,(goal(proved))).
