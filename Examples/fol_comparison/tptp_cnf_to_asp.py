#!/usr/bin/env python3
"""Translate equality-free TPTP CNF into a Herbrand ASP attempt.

The generated term/1 rules enumerate the full Herbrand universe. If the input
has function symbols, finite grounders are expected not to terminate. Equality
is rejected because ASP assignment/comparison is not first-order equality and
cannot replace equality resolution or paramodulation.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


CNF = re.compile(r"^cnf\(([^,]+),([^,]+),\((.*)\)\)\.$")
VARIABLE = re.compile(r"\b[A-Z][A-Za-z0-9_]*\b")


def split_top(text: str, separator: str) -> list[str]:
    parts: list[str] = []
    start = 0
    depth = 0
    quoted = False
    for index, char in enumerate(text):
        if char == "'":
            quoted = not quoted
        elif not quoted:
            if char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
            elif char == separator and depth == 0:
                parts.append(text[start:index].strip())
                start = index + 1
    parts.append(text[start:].strip())
    return parts


def collect_terms(term: str, constants: set[str], functions: set[tuple[str, int]]) -> None:
    term = term.strip()
    if VARIABLE.fullmatch(term) or re.fullmatch(r"-?\d+(?:\.\d+)?", term):
        return
    if term.startswith("'") and term.endswith("'"):
        constants.add(term)
        return
    opening = term.find("(")
    if opening < 0:
        constants.add(term)
        return
    name = term[:opening].strip()
    arguments = split_top(term[opening + 1 : -1], ",")
    functions.add((name, len(arguments)))
    for argument in arguments:
        collect_terms(argument, constants, functions)


def collect_atom_terms(atom: str, constants: set[str], functions: set[tuple[str, int]]) -> None:
    opening = atom.find("(")
    if opening < 0:
        return
    for argument in split_top(atom[opening + 1 : -1], ","):
        collect_terms(argument, constants, functions)


def main() -> int:
    if len(sys.argv) != 3:
        print(f"usage: {Path(sys.argv[0]).name} INPUT.p OUTPUT.lp", file=sys.stderr)
        return 2

    source = Path(sys.argv[1])
    destination = Path(sys.argv[2])
    rules: list[tuple[str, list[str], list[str], list[str]]] = []
    constants: set[str] = set()
    functions: set[tuple[str, int]] = set()
    query: str | None = None

    for line_number, raw_line in enumerate(source.read_text().splitlines(), 1):
        line = raw_line.strip()
        if not line or line.startswith("%"):
            continue
        match = CNF.match(line)
        if not match:
            raise ValueError(f"{source}:{line_number}: unsupported statement: {line}")
        name, role, formula = match.groups()
        literals = split_top(formula, "|")
        if any(" = " in literal or " != " in literal for literal in literals):
            raise ValueError(
                f"{source}:{line_number}: first-order equality has no "
                "semantics-preserving ASP rule translation: " + formula
            )
        if role == "conjecture":
            if len(literals) != 1 or literals[0].startswith("~"):
                raise ValueError(f"{source}:{line_number}: query is not a positive literal")
            query = literals[0]
            collect_atom_terms(query, constants, functions)
            continue

        positive: list[str] = []
        negative: list[str] = []
        for literal in literals:
            if literal.startswith("~"):
                atom = literal[1:].strip()
                negative.append(atom)
            else:
                atom = literal
                positive.append(atom)
            collect_atom_terms(atom, constants, functions)
        variables = sorted(set(VARIABLE.findall(formula)))
        rules.append((name, positive, negative, variables))

    if query is None:
        raise ValueError(f"{source}: no positive conjecture")

    output = [
        "% Mechanical Herbrand translation of " + source.name + ".",
        "% Unbounded term generation preserves the source's function terms.",
        "",
    ]
    for constant in sorted(constants):
        output.append(f"term({constant}).")
    for name, arity in sorted(functions):
        variables = [f"T{index}" for index in range(arity)]
        body = ", ".join(f"term({variable})" for variable in variables)
        output.append(f"term({name}({','.join(variables)})) :- {body}.")
    output.append("")

    for name, positive, negative, variables in rules:
        body = negative + [f"term({variable})" for variable in variables]
        head = " | ".join(positive)
        if head and body:
            rule = f"{head} :- {', '.join(body)}."
        elif head:
            rule = f"{head}."
        else:
            rule = f":- {', '.join(body)}."
        output.extend((f"% {name}", rule))
    output.extend(
        (
            "",
            f"% Query: {query}",
            "% ProbLog reads this as its query directive. ASP systems treat it",
            "% as an unrelated fact, which does not affect the queried predicate.",
            f"query({query}).",
            "",
        )
    )
    destination.write_text("\n".join(output))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValueError as error:
        print(error, file=sys.stderr)
        raise SystemExit(1)
