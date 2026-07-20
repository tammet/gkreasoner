% GKC clausification of the NLP inconsistency problem. The quantified
% conjecture is represented by a fresh goal(proved) wrapper.

cnf(ax1,axiom,(instrumentality(X0,X1) | ~furniture(X0,X1))).
cnf(ax2,axiom,(furniture(X0,X1) | ~seat(X0,X1))).
cnf(ax3,axiom,(seat(X0,X1) | ~frontseat(X0,X1))).
cnf(ax4,axiom,(object(X0,X1) | ~location(X0,X1))).
cnf(ax5,axiom,(location(X0,X1) | ~city(X0,X1))).
cnf(ax6,axiom,(placename(X0,X1) | ~hollywood_placename(X0,X1))).
cnf(ax7,axiom,(unisex(X0,X1) | ~abstraction(X0,X1))).
cnf(ax8,axiom,(general(X0,X1) | ~abstraction(X0,X1))).
cnf(ax9,axiom,(nonhuman(X0,X1) | ~abstraction(X0,X1))).
cnf(ax10,axiom,(thing(X0,X1) | ~abstraction(X0,X1))).
cnf(ax11,axiom,(abstraction(X0,X1) | ~relation(X0,X1))).
cnf(ax12,axiom,(relation(X0,X1) | ~relname(X0,X1))).
cnf(ax13,axiom,(relname(X0,X1) | ~placename(X0,X1))).
cnf(ax14,axiom,(artifact(X0,X1) | ~way(X0,X1))).
cnf(ax15,axiom,(way(X0,X1) | ~street(X0,X1))).
cnf(ax16,axiom,(unisex(X0,X1) | ~object(X0,X1))).
cnf(ax17,axiom,(impartial(X0,X1) | ~object(X0,X1))).
cnf(ax18,axiom,(nonliving(X0,X1) | ~object(X0,X1))).
cnf(ax19,axiom,(entity(X0,X1) | ~object(X0,X1))).
cnf(ax20,axiom,(object(X0,X1) | ~artifact(X0,X1))).
cnf(ax21,axiom,(artifact(X0,X1) | ~instrumentality(X0,X1))).
cnf(ax22,axiom,(instrumentality(X0,X1) | ~transport(X0,X1))).
cnf(ax23,axiom,(transport(X0,X1) | ~vehicle(X0,X1))).
cnf(ax24,axiom,(vehicle(X0,X1) | ~car(X0,X1))).
cnf(ax25,axiom,(car(X0,X1) | ~chevy(X0,X1))).
cnf(ax26,axiom,(event(X0,X1) | ~barrel(X0,X1))).
cnf(ax27,axiom,(eventuality(X0,X1) | ~event(X0,X1))).
cnf(ax28,axiom,(event(X0,X1) | ~state(X0,X1))).
cnf(ax29,axiom,(unisex(X0,X1) | ~eventuality(X0,X1))).
cnf(ax30,axiom,(nonexistent(X0,X1) | ~eventuality(X0,X1))).
cnf(ax31,axiom,(specific(X0,X1) | ~eventuality(X0,X1))).
cnf(ax32,axiom,(thing(X0,X1) | ~eventuality(X0,X1))).
cnf(ax33,axiom,(eventuality(X0,X1) | ~state(X0,X1))).
cnf(ax34,axiom,(group(X0,X1) | ~two(X0,X1))).
cnf(ax35,axiom,(multiple(X0,X1) | ~set(X0,X1))).
cnf(ax36,axiom,(set(X0,X1) | ~group(X0,X1))).
cnf(ax37,axiom,(male(X0,X1) | ~man(X0,X1))).
cnf(ax38,axiom,(animate(X0,X1) | ~human_person(X0,X1))).
cnf(ax39,axiom,(human(X0,X1) | ~human_person(X0,X1))).
cnf(ax40,axiom,(living(X0,X1) | ~organism(X0,X1))).
cnf(ax41,axiom,(impartial(X0,X1) | ~organism(X0,X1))).
cnf(ax42,axiom,(existent(X0,X1) | ~entity(X0,X1))).
cnf(ax43,axiom,(specific(X0,X1) | ~entity(X0,X1))).
cnf(ax44,axiom,(singleton(X0,X1) | ~thing(X0,X1))).
cnf(ax45,axiom,(thing(X0,X1) | ~entity(X0,X1))).
cnf(ax46,axiom,(entity(X0,X1) | ~organism(X0,X1))).
cnf(ax47,axiom,(organism(X0,X1) | ~human_person(X0,X1))).
cnf(ax48,axiom,(human_person(X0,X1) | ~man(X0,X1))).
cnf(ax49,axiom,(man(X0,X1) | ~fellow(X0,X1))).
cnf(ax50,axiom,(~nonliving(X0,X1) | ~animate(X0,X1))).
cnf(ax51,axiom,(~nonexistent(X0,X1) | ~existent(X0,X1))).
cnf(ax52,axiom,(~human(X0,X1) | ~nonhuman(X0,X1))).
cnf(ax53,axiom,(~living(X0,X1) | ~nonliving(X0,X1))).
cnf(ax54,axiom,(~multiple(X0,X1) | ~singleton(X0,X1))).
cnf(ax55,axiom,(~general(X0,X1) | ~specific(X0,X1))).
cnf(ax56,axiom,(~male(X0,X1) | ~unisex(X0,X1))).
cnf(ax57,axiom,(~old(X0,X1) | ~young(X0,X1))).
cnf(ax58,axiom,(~of(X0,X1,X2) | X1 = X3 | ~placename(X0,X1) | ~of(X0,X3,X2) | ~placename(X0,X3) | ~entity(X0,X2))).
cnf(ax59,axiom,(X0 = X1 | ~be(X2,X3,X0,X1))).
cnf(ax60,axiom,(member(X0,sk1(X1,X0),X1) | ~two(X0,X1))).
cnf(ax60,axiom,(X0 = sk1(X1,X2) | X0 = sk2(X1,X2) | ~member(X2,X0,X1) | ~two(X2,X1))).
cnf(ax60,axiom,(sk2(X0,X1) != sk1(X0,X1) | ~two(X1,X0))).
cnf(ax60,axiom,(member(X0,sk2(X1,X0),X1) | ~two(X0,X1))).
cnf(ax60,axiom,(member(X0,sk3(X1,X0,X2,X3),X1) | X3 = X2 | ~member(X0,X3,X1) | ~member(X0,X2,X1) | two(X0,X1))).
cnf(ax60,axiom,(sk3(X0,X1,X2,X3) != X2 | X3 = X2 | ~member(X1,X3,X0) | ~member(X1,X2,X0) | two(X1,X0))).
cnf(ax60,axiom,(sk3(X0,X1,X2,X3) != X3 | X3 = X2 | ~member(X1,X3,X0) | ~member(X1,X2,X0) | two(X1,X0))).
cnf(ax61,axiom,(~member(X0,X1,X1))).
cnf(co1,axiom,(actual_world(sk4) | goal(proved))).
cnf(co1,axiom,(young(sk4,X0) | ~member(sk4,X0,sk9) | goal(proved))).
cnf(co1,axiom,(fellow(sk4,X0) | ~member(sk4,X0,sk9) | goal(proved))).
cnf(co1,axiom,(group(sk4,sk9) | goal(proved))).
cnf(co1,axiom,(two(sk4,sk9) | goal(proved))).
cnf(co1,axiom,(in(sk4,sk11(X0),sk11(X0)) | ~member(sk4,X0,sk9) | goal(proved))).
cnf(co1,axiom,(be(sk4,sk10(X0),X0,sk11(X0)) | ~member(sk4,X0,sk9) | goal(proved))).
cnf(co1,axiom,(state(sk4,sk10(X0)) | ~member(sk4,X0,sk9) | goal(proved))).
cnf(co1,axiom,(frontseat(sk4,sk11(X0)) | ~member(sk4,X0,sk9) | goal(proved))).
cnf(co1,axiom,(in(sk4,sk8,sk7) | goal(proved))).
cnf(co1,axiom,(down(sk4,sk8,sk5) | goal(proved))).
cnf(co1,axiom,(barrel(sk4,sk8) | goal(proved))).
cnf(co1,axiom,(present(sk4,sk8) | goal(proved))).
cnf(co1,axiom,(agent(sk4,sk8,sk7) | goal(proved))).
cnf(co1,axiom,(event(sk4,sk8) | goal(proved))).
cnf(co1,axiom,(old(sk4,sk7) | goal(proved))).
cnf(co1,axiom,(dirty(sk4,sk7) | goal(proved))).
cnf(co1,axiom,(white(sk4,sk7) | goal(proved))).
cnf(co1,axiom,(chevy(sk4,sk7) | goal(proved))).
cnf(co1,axiom,(placename(sk4,sk6) | goal(proved))).
cnf(co1,axiom,(hollywood_placename(sk4,sk6) | goal(proved))).
cnf(co1,axiom,(city(sk4,sk7) | goal(proved))).
cnf(co1,axiom,(of(sk4,sk6,sk7) | goal(proved))).
cnf(co1,axiom,(lonely(sk4,sk5) | goal(proved))).
cnf(co1,axiom,(street(sk4,sk5) | goal(proved))).
cnf(frm_63,conjecture,(goal(proved))).
