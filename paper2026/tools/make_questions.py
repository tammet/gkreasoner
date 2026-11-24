#!/usr/bin/env python3
"""make_questions.py: write the question files of part O13_conformance from its inputs and its lists of questions.

  python3 tools/make_questions.py                 write O13_conformance/questions/
  python3 tools/make_questions.py --help          this text
  python3 tools/make_questions.py --check FOLDER  compare the written files with FOLDER/sets, FOLDER/keychk,
                                                  FOLDER/missed_evidence and FOLDER/new (the question files of an
                                                  earlier run)

Unpack the inputs first: cd O13_conformance && for a in inputs/*.tar.xz; do tar -xJf $a -C inputs; done

A question file is an input with its question replaced by one atom. Three lists name the questions:
  questions_sets.csv(.gz)          set, question_file, input, atom. The question file is the input without its
                                   question, one fact zz_question_constant(c) for each constant c of the input's own
                                   question (these constants stay in the domain), and the question of the atom.
                                   A .js or .json input is a JSON list of statements; comments are removed first.
  questions_keychk.csv             question_file, input, atom, asked. The question file is the input without its
                                   query lines, and query(ASKED).
  questions_missed_evidence.csv    set, question_file, input, atom. The input without its query lines, and
                                   query(ATOM).
  questions_new.csv(.gz)           group, generator, question_file, input, atom: the further questions on new
                                   inputs, written as those of questions_sets.csv.
All paths are relative to the folder paper2026/. Python 3.9 or later, no other package.
"""
import csv
import gzip
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PART = os.path.join(ROOT, "O13_conformance")


def read(name):
  p = os.path.join(PART, name)
  f = gzip.open(p + ".gz", "rt", newline="") if not os.path.exists(p) else open(p, newline="")
  with f:
    return list(csv.DictReader(f))


def strip_comments(text):
  """C-style comments outside JSON strings (as the tool's reader removes them)"""
  out, i, n, instr = [], 0, len(text), False
  while i < n:
    c = text[i]
    if instr:
      out.append(c)
      if c == "\\" and i + 1 < n:
        out.append(text[i + 1])
        i += 2
        continue
      if c == '"':
        instr = False
      i += 1
    elif c == '"':
      instr = True
      out.append(c)
      i += 1
    elif c == "/" and i + 1 < n and text[i + 1] == "/":
      while i < n and text[i] != "\n":
        i += 1
    elif c == "/" and i + 1 < n and text[i + 1] == "*":
      j = text.find("*/", i + 2)
      i = n if j < 0 else j + 2
    else:
      out.append(c)
      i += 1
  return "".join(out)


def lit_json(atom):
  m = re.match(r"^([^()]+)(?:\((.*)\))?$", atom)
  p, args = m.group(1), m.group(2)
  return [p] + ([x.strip() for x in args.split(",")] if args else [])


def q_consts(f, text):
  """the constants of the input's own question"""
  if f.endswith(".json") or f.endswith(".js"):
    cs = []
    for s in json.loads(strip_comments(text)):
      if isinstance(s, dict) and "@question" in s:
        def walk(x):
          if isinstance(x, list):
            for y in x[1:] if x and isinstance(x[0], str) else x:
              walk(y)
          elif isinstance(x, str) and not x.startswith("?:"):
            cs.append(x)
        walk(s["@question"])
    return cs
  cs = []
  for line in text.split("\n"):
    m = re.match(r"^\s*query\((.*)\)\.\s*$", line)
    if m:
      inner = re.sub(r"^-", "", m.group(1).strip())
      mm = re.match(r"^[^()]+\((.*)\)$", inner)
      if mm:
        cs += [x.strip() for x in mm.group(1).split(",")
               if x.strip() and not x.strip()[0].isupper() and not x.strip().startswith("_")]
  return cs


def with_question(f, text, atom):
  cs = q_consts(f, text)
  if f.endswith(".json") or f.endswith(".js"):
    d = [s for s in json.loads(strip_comments(text)) if not (isinstance(s, dict) and "@question" in s)]
    return json.dumps(d + [{"@logic": ["zz_question_constant", c]} for c in cs] + [{"@question": lit_json(atom)}])
  ls = [x for x in text.split("\n") if x.strip() and not x.strip().startswith("query(")]
  ls += ["zz_question_constant(%s)." % c for c in cs]
  return "\n".join(ls) + "\nquery(%s).\n" % atom


def replaced(text, asked):
  ls = [x for x in text.split("\n") if x.strip() and not x.strip().startswith("query(")]
  return "\n".join(ls) + "\nquery(%s).\n" % asked


def missed(text, atom):
  return "".join(line for line in text.splitlines(True) if not line.startswith("query(")) + "query(%s).\n" % atom


def files():
  cache = {}

  def src(p):
    if p not in cache:
      cache[p] = open(os.path.join(ROOT, p)).read()
    return cache[p]
  for r in read("questions_sets.csv"):
    yield r["question_file"], with_question(r["input"], src(r["input"]), r["atom"])
  for r in read("questions_keychk.csv"):
    yield r["question_file"], replaced(src(r["input"]), r["asked"])
  for r in read("questions_missed_evidence.csv"):
    yield r["question_file"], missed(src(r["input"]), r["atom"])
  if any(os.path.exists(os.path.join(PART, "questions_new.csv" + z)) for z in ("", ".gz")):
    cache.clear()
    for r in read("questions_new.csv"):
      yield r["question_file"], with_question(r["input"], src(r["input"]), r["atom"])


def main():
  check = None
  if len(sys.argv) == 2 and sys.argv[1] in ("-h", "--help"):
    print(__doc__)
    sys.exit(0)
  if len(sys.argv) == 3 and sys.argv[1] == "--check":
    check = sys.argv[2]
  elif len(sys.argv) != 1:
    print(__doc__)
    sys.exit(2)
  n = bad = 0
  for rel, text in files():
    n += 1
    if check:
      sub = os.path.relpath(rel, "O13_conformance/questions")
      p = os.path.join(check, sub)
      if not os.path.exists(p) or open(p).read() != text:
        bad += 1
        if bad <= 10:
          print("differs: " + sub)
      continue
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w") as f:
      f.write(text)
  if check:
    print("%d question files compared, %d differ" % (n, bad))
    sys.exit(1 if bad else 0)
  print("%d question files written under O13_conformance/questions/" % n)


if __name__ == "__main__":
  main()
