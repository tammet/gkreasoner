"""Readers of the outputs of gk and of the reference tool mcref.

gk prints the line {"recursive": ...} first. Its field "value" holds the
four shares (for, against, conflict, ignorance) of a closed question; for a
question with variables the field "answers" holds one entry per answer,
each with "answer" (the literal in gk's JSON form, such as
["flies","tweety"]) and "value". mcref prints one JSON object {"mcref": ...}
whose field "answers" holds one entry per answer, with "key" (sign,
predicate, arguments) and "value", or the field "unsupported" with the
reason why the tool declines the input.

Used by check_gk.py, tools/collect.py and O2_record/make_rows.py. Python 3.8
or later, standard library only.
"""
import json, re


def num_text(x):
  """a float as gk prints it in text: the shortest %g form that reads back
  as the same number, with ".0" when it has no point or exponent"""
  s = repr(x)
  for p in range(1, 18):
    s = "%.*g" % (p, x)
    if float(s) == x:
      break
  if not any(c in s for c in ".eni"):
    s += ".0"
  return s


def term_text(t):
  """a term of gk's JSON form as text: [f, a1, ..., an] is f(a1,...,an)"""
  if isinstance(t, bool):
    return "true" if t else "false"
  if isinstance(t, int):
    return str(t)
  if isinstance(t, float):
    return num_text(t)
  if isinstance(t, str):
    if t.startswith("?:X"):
      return "_V" + t[3:]
    if t.startswith(":"):
      return t[1:]
    return t
  if isinstance(t, list) and t:
    head = term_text(t[0])
    if len(t) == 1:
      return head
    return head + "(" + ",".join(term_text(a) for a in t[1:]) + ")"
  return str(t)


def lit_text(x):
  """a question or answer literal of gk's line as text; text and None stay"""
  if x is None or isinstance(x, str):
    return x
  return term_text(x)


def gk_line(stdout):
  """the object of the line {"recursive": ...}, or None"""
  for line in (stdout or "").split("\n"):
    if line.startswith('{"recursive"'):
      try:
        return json.loads(line)["recursive"]
      except (ValueError, KeyError):
        return None
  return None


def gk_answers(stdout):
  """[(answer text, four shares)] in the order gk prints them: one entry
  for a closed question, one per answer for a question with variables"""
  r = gk_line(stdout)
  if r is None:
    return None
  if r.get("answers") is not None:
    return [(lit_text(a.get("answer")), a.get("value")) for a in r["answers"]]
  if r.get("value") is None:
    return []
  return [(lit_text(r.get("question")), r["value"])]


def mcref_object(stdout):
  try:
    return json.loads(stdout)["mcref"]
  except (ValueError, KeyError, TypeError):
    return None


def key_text(key):
  """an answer of mcref as text: sign, predicate and arguments"""
  sign, pred, args = key
  t = ("-" if sign == "-" else "") + pred
  return t + ("(" + ",".join(str(a) for a in args) + ")" if args else "")


def mcref_answers(stdout):
  """[(answer text, four estimates)], or None when the tool declined or
  printed no result"""
  m = mcref_object(stdout)
  if m is None or m.get("unsupported") or m.get("error"):
    return None
  return [(key_text(a["key"]), a["value"]) for a in m.get("answers") or []]


def shares_text(v):
  return "[" + ",".join(json.dumps(x) for x in v) + "]" if v is not None else "none"


NUM = re.compile(r"-?\d*\.\d+|-?\d+")


def numbers(text):
  """the numbers of a printed result, each with the tolerance of its
  printed precision: .396 stands for every value from .3955 to .3965"""
  out = []
  for s in NUM.findall(text):
    dec = len(s.split(".")[1]) if "." in s else 0
    out.append((float(s), 0.5 * 10 ** -dec + 1e-9))
  return out


def matches(printed, values):
  """the printed result equals the values at its precision; values is a
  list of four-tuples"""
  flat = [x for v in values for x in v]
  exp = numbers(printed)
  return len(flat) == len(exp) and all(abs(x - e) <= tol for x, (e, tol) in zip(flat, exp))
