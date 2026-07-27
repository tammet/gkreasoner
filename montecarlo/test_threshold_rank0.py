#!/usr/bin/env python3
"""
Focused tests for the PRIORITY-ZERO layer and the contextual-priority decline
added to threshold_worlds.py on 2026-07-27.

These test the reference sampler ON ITS OWN, against closed forms derived by
hand -- they never consult gk.  That independence is the point: the same rule is
implemented twice, once as a closed-form configuration enumeration inside gk's
evaluator and once here as per-world sampling, so a formula error in either
shows up as a disagreement rather than as two copies of the same mistake.

What is pinned:

  rank0_cycle     two reciprocal priority-zero defaults about the two polarities
                  of one atom.  Priority zero is INCOMPARABLE, so neither block
                  is a priority bid and the two edges are the internal edges of
                  a cycle: what survives is ordinary unranked evidence meeting
                  by shared-threshold opposition, and the overlap is CONFLICT.
  rank0_onesided  ONE priority-zero default undercut by an ordinary contrary
                  fact.  No reciprocal partner, so this is a pure acyclic
                  undercut and keeps the exclusive F4 split, conflict 0.  This
                  is the case the pre-2026-07-27 sampler got wrong: it treated
                  every rank-0 mutual block as plain evidence and returned the
                  opposition tuple .32/.12/.48/.08 here too.
  rank0_mixed     both at once: the external fact still undercuts, the
                  reciprocal partner does not.
  rank0_certain   the certain limit of the cycle: conflict 1.
  ctx_test8       a rank-3 check whose exception is derivable only through a
                  rank-1 default.  gk's search excludes that support inside the
                  check; this model has no enclosing-check context, so it must
                  DECLINE -- never silently return the value of the admissible
                  variant below.
  ctx_test9       the same shape with the ranks reversed, where the exception IS
                  admissible: scored normally.

Usage:  python3 montecarlo/test_threshold_rank0.py [-n TRIALS] [--seed SEED]
Exit status 0 iff every case matches within tolerance.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import threshold_worlds as tw   # noqa: E402


def atom(pred, *args):
    return (pred, tuple(args))


# Each case: (name, clauses, confidences, query atom, query sign, expected or None)
# `clauses` are ORIGINAL @logic clauses, head LAST, exactly the form
# build_testimonies consumes; `confs` maps the clause id to its strength.
CASES = []


def case(name, clauses, confs, query, sign, expected, note=""):
    CASES.append((name, clauses, confs, query, sign, expected, note))


# --- reciprocal priority-zero cycle, premises .8 / .6 -----------------------
#   .8 quaker, .6 republican, both defaults present -> conflict .48;
#   quaker only .8*.4; republican only .2*.6; neither .08
_CYCLE = [
    ("q", ["quaker", "n"]),
    ("r", ["republican", "n"]),
    ("rp", [["-quaker", "n"], ["pacifist", "n"],
            ["$block", 0, ["$not", ["pacifist", "n"]]]]),
    ("rn", [["-republican", "n"], ["-pacifist", "n"],
            ["$block", 0, ["pacifist", "n"]]]),
]
case("rank0_cycle", _CYCLE, {"q": 0.8, "r": 0.6, "rp": 1.0, "rn": 1.0},
     atom("pacifist", "n"), "+", (0.32, 0.12, 0.48, 0.08),
     "the reciprocal cycle: ordinary opposition, overlap is conflict")

case("rank0_cycle_neg", _CYCLE, {"q": 0.8, "r": 0.6, "rp": 1.0, "rn": 1.0},
     atom("pacifist", "n"), "-", (0.12, 0.32, 0.48, 0.08),
     "the same atom asked the other way round: the exact mirror")

case("rank0_certain", _CYCLE, {"q": 1.0, "r": 1.0, "rp": 1.0, "rn": 1.0},
     atom("pacifist", "n"), "+", (0.0, 0.0, 1.0, 0.0),
     "certain limit of the cycle")

# --- one-sided acyclic undercut: the F4 boundary ----------------------------
#   the default lives only where the undercutter is absent: .8*.4 = .32;
#   the ordinary contrary fact stands on its full .6; conflict 0
_ONESIDED = [
    ("q", ["quaker", "n"]),
    ("rp", [["-quaker", "n"], ["pacifist", "n"],
            ["$block", 0, ["$not", ["pacifist", "n"]]]]),
    ("f", ["-pacifist", "n"]),
]
case("rank0_onesided", _ONESIDED, {"q": 0.8, "rp": 1.0, "f": 0.6},
     atom("pacifist", "n"), "+", (0.32, 0.60, 0.0, 0.08),
     "no reciprocal partner: the exclusive F4 split must survive")

case("rank0_onesided_neg", _ONESIDED, {"q": 0.8, "rp": 1.0, "f": 0.6},
     atom("pacifist", "n"), "-", (0.60, 0.32, 0.0, 0.08),
     "its mirror")

# --- the mixed case: a reciprocal cycle PLUS an independent contrary fact ---
#   both defaults present .48 -> cycle conflict, fact usable .5 -> con .24 cfl .24
#   pro only .32 -> fact usable .5 else pro          -> pro .16 con .16
#   con only .12 -> con either way                   -> con .12
#   neither  .08 -> fact usable .5 else ignorance    -> con .04 ign .04
_MIXED = _CYCLE + [("f", ["-pacifist", "n"])]
case("rank0_mixed", _MIXED,
     {"q": 0.8, "r": 0.6, "rp": 1.0, "rn": 1.0, "f": 0.5},
     atom("pacifist", "n"), "+", (0.16, 0.56, 0.24, 0.04),
     "external evidence entering the cycle still undercuts")

# --- contextual blocker priority -------------------------------------------
_CTX = lambda target_rank, exc_rank: [       # noqa: E731
    ("b", ["base", "a"]),
    ("c", ["cause", "a"]),
    ("rt", [["-base", "a"], ["target", "a"],
            ["$block", target_rank, ["exception", "a"]]]),
    ("re", [["-cause", "a"], ["exception", "a"],
            ["$block", exc_rank, ["$not", ["exception", "a"]]]]),
    ("f", ["-target", "a"]),
]
case("ctx_test8", _CTX(3, 1),
     {"b": 1.0, "c": 1.0, "rt": 1.0, "re": 0.9, "f": 0.2},
     atom("target", "a"), "+", None,
     "the exception is inadmissible in a rank-3 check: DECLINE, never score")
case("ctx_test9", _CTX(1, 3),
     {"b": 1.0, "c": 1.0, "rt": 1.0, "re": 0.9, "f": 0.2},
     atom("target", "a"), "+", (0.08, 0.18, 0.02, 0.72),
     "the exception IS admissible against a rank-1 check")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-n", "--trials", type=int, default=200000)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--tol", type=float, default=6e-3)
    args = ap.parse_args()

    fails = 0
    for name, clauses, confs, q, sign, expected, note in CASES:
        pool = [(cid, raw) for (cid, raw) in clauses]
        got = tw.evaluate(pool, confs, q, sign, args.trials, args.seed)
        declined = got.get("not_scored")
        if expected is None:
            ok = bool(declined)
            print(("OK   " if ok else "FAIL ") + f"{name}: " +
                  (f"declined ({declined[:60]}...)" if declined
                   else f"SCORED {got} but must decline"))
            fails += 0 if ok else 1
            continue
        if declined:
            print(f"FAIL {name}: declined but a value is pinned ({declined})")
            fails += 1
            continue
        vals = tuple(got[f] for f in ("support_for", "support_against",
                                      "conflict", "ignorance"))
        bad = [i for i in range(4) if abs(vals[i] - expected[i]) > args.tol]
        print(("OK   " if not bad else "FAIL ") +
              f"{name}: " + "/".join("%.4f" % v for v in vals) +
              "  expected " + "/".join("%.2f" % v for v in expected) +
              (f"   [{note}]" if note else ""))
        fails += 1 if bad else 0

    print(f"\ntest_threshold_rank0: {len(CASES)-fails} pass, {fails} fail "
          f"(n={args.trials}, seed={args.seed}, tol={args.tol})")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
