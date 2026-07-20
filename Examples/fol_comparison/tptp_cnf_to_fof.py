#!/usr/bin/env python3
"""Rewrite TPTP CNF clauses as explicitly universally quantified FOF."""

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
    for index, char in enumerate(text):
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        elif char == separator and depth == 0:
            parts.append(text[start:index].strip())
            start = index + 1
    parts.append(text[start:].strip())
    return parts


def collect_term_symbols(
    term: str, constants: set[str], functions: set[tuple[str, int]]
) -> None:
    term = term.strip()
    if VARIABLE.fullmatch(term) or re.fullmatch(r"-?\d+(?:\.\d+)?", term):
        return
    opening = term.find("(")
    if opening < 0:
        constants.add(term)
        return
    arguments = split_top(term[opening + 1 : -1], ",")
    functions.add((term[:opening].strip(), len(arguments)))
    for argument in arguments:
        collect_term_symbols(argument, constants, functions)


def collect_formula_symbols(
    formula: str,
    constants: set[str],
    functions: set[tuple[str, int]],
    predicates: set[tuple[str, int]],
) -> None:
    for literal in split_top(formula, "|"):
        literal = literal.strip()
        if literal.startswith("~"):
            literal = literal[1:].strip()
        equality = re.match(r"^(.*?)(?:\s+!=\s+|\s+=\s+)(.*)$", literal)
        if equality:
            collect_term_symbols(equality.group(1), constants, functions)
            collect_term_symbols(equality.group(2), constants, functions)
            continue
        opening = literal.find("(")
        if opening < 0:
            predicates.add((literal, 0))
            continue
        arguments = split_top(literal[opening + 1 : -1], ",")
        predicates.add((literal[:opening].strip(), len(arguments)))
        for argument in arguments:
            collect_term_symbols(argument, constants, functions)


def normalize_for_tweety(formula: str) -> str:
    """Apply bijective symbol renamings accepted by Tweety's TPTP parser."""
    quoted: dict[str, str] = {}

    def replace_quoted(match: re.Match[str]) -> str:
        value = match.group(1)
        return quoted.setdefault(value, "q_" + re.sub(r"[^a-z0-9]+", "_", value.lower()))

    formula = re.sub(r"'([^']+)'", replace_quoted, formula)
    formula = re.sub(r"\bevent\(", "evt_pred(", formula)
    variables = sorted(set(VARIABLE.findall(formula)))
    for index, variable in enumerate(variables):
        replacement = "V" + chr(ord("A") + index)
        formula = re.sub(rf"\b{re.escape(variable)}\b", replacement, formula)
    return formula


def main() -> int:
    if len(sys.argv) != 3:
        print(f"usage: {Path(sys.argv[0]).name} INPUT.p OUTPUT.p", file=sys.stderr)
        return 2
    source = Path(sys.argv[1])
    destination = Path(sys.argv[2])
    output: list[str] = []
    formulas: list[tuple[str, str, str]] = []
    constants: set[str] = set()
    functions: set[tuple[str, int]] = set()
    predicates: set[tuple[str, int]] = set()
    for line_number, raw_line in enumerate(source.read_text().splitlines(), 1):
        line = raw_line.strip()
        if not line or line.startswith("%"):
            continue
        match = CNF.match(line)
        if not match:
            raise ValueError(f"{source}:{line_number}: unsupported statement: {line}")
        name, role, formula = match.groups()
        formula = normalize_for_tweety(formula)
        collect_formula_symbols(formula, constants, functions, predicates)
        formulas.append((name, role, formula))

    # TPTPParser infers arities one formula at a time and miscounts commas in
    # nested function terms. The comparison harness reads this exact signature
    # before asking TPTPParser to parse the formulas.
    for constant in sorted(constants):
        output.append(f"% tweety_signature constant {constant}")
    for name, arity in sorted(functions):
        output.append(f"% tweety_signature functor {name} {arity}")
    for name, arity in sorted(predicates):
        output.append(f"% tweety_signature predicate {name} {arity}")
    output.append("")

    for name, role, formula in formulas:
        variables = sorted(set(VARIABLE.findall(formula)))
        if variables:
            formula = f"! [{','.join(variables)}] : ({formula})"
        output.append(f"fof({name},{role},({formula})).")
    destination.write_text("\n".join(output) + "\n")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValueError as error:
        print(error, file=sys.stderr)
        raise SystemExit(1)
