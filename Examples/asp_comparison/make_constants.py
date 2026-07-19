#!/usr/bin/env python3
"""Generate the father-chain scaling workload used by the ASP comparison.

The argument is the total number of named constants. It must be even: half of
the constants form a b-chain and half form a p-chain. The generated programs
use the same facts and rules in the syntax of gk, clingo, DLV, I-DLV, or
s(CASP).

These normalized programs make the system inputs directly comparable. They do
not reproduce every detail of the historical files: those files commented out some
propagation rules for clingo and used slightly different chain lengths for gk.
See README.md and results.md before comparing timings.
"""

import argparse
import json
import sys
from pathlib import Path


def father_pairs(total):
    per_chain = total // 2
    for index in range(1, per_chain):
        yield (f"b{index}", f"b{index + 1}")
        yield (f"p{index}", f"p{index + 1}")


def gk_program(total):
    facts = [["father", left, right] for left, right in father_pairs(total)]
    program = facts + [
        ["bird", "b1"],
        ["penguin", "p1"],
        [["penguin", "?:X"], "=>", ["bird", "?:X"]],
        [["-bird", "?:X"], ["flies", "?:X"],
         ["$block", 3, ["$not", ["flies", "?:X"]]]],
        [["penguin", "?:X"], "=>", ["-flies", "?:X"]],
        [["father", "?:X", "?:Y"], "=>", ["anc", "?:X", "?:Y"]],
        [[["anc", "?:X", "?:Z"], "&", ["anc", "?:Z", "?:Y"]],
         "=>", ["anc", "?:X", "?:Y"]],
        [[["anc", "?:Y", "?:X"], "&", ["penguin", "?:Y"]],
         "=>", ["penguin", "?:X"]],
        [[["anc", "?:Y", "?:X"], "&", ["bird", "?:Y"]],
         "=>", ["bird", "?:X"]],
        {"@question": ["flies", "b1"]},
    ]
    return json.dumps(program, indent=2) + "\n"


def asp_program(total, system):
    negative_flies = "nonflies" if system == "idlv" else "-flies"
    lines = [f"father({left},{right})." for left, right in father_pairs(total)]
    lines += [
        "",
        "bird(b1).",
        "penguin(p1).",
        "",
        "bird(X) :- penguin(X).",
        f"flies(X) :- bird(X), not {negative_flies}(X).",
        f"{negative_flies}(X) :- penguin(X).",
        "",
        "anc(X,Y) :- father(X,Y).",
        "anc(X,Y) :- anc(X,Z), anc(Z,Y).",
        "",
        "penguin(X) :- anc(Y,X), penguin(Y).",
        "bird(X) :- anc(Y,X), bird(Y).",
        "",
    ]
    if system == "clingo":
        lines += [
            "% UNSATISFIABLE means no counterexample model exists.",
            ":- flies(b1).",
        ]
    elif system in ("dlv", "idlv"):
        lines.append("flies(b1)?")
    else:
        lines.append("?- flies(b1).")
    return "\n".join(lines) + "\n"


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("constants", type=int,
                        help="total constants across the b and p chains")
    parser.add_argument("--system",
                        choices=("gk", "clingo", "dlv", "idlv", "scasp"),
                        default="gk", help="output syntax (default: gk)")
    parser.add_argument("--output", type=Path,
                        help="write to this file instead of standard output")
    return parser.parse_args()


def main():
    args = parse_args()
    if args.constants < 4 or args.constants % 2:
        raise SystemExit("constants must be an even integer of at least 4")
    if args.system == "gk":
        output = gk_program(args.constants)
    else:
        output = asp_program(args.constants, args.system)
    if args.output:
        args.output.write_text(output)
    else:
        sys.stdout.write(output)


if __name__ == "__main__":
    main()
