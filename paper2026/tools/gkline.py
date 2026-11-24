"""gkline.py: read the first output line of gk and the output object of the tool (mcref).

The scripts of this folder share these readers: check_gk.py, which reruns gk and the tool, and summarize.py,
which computes the tables of the part READMEs from the results.csv files.

gk prints one JSON line first. Under the default (`gk FILE`) and the exact method (`gk -exact FILE`) the line
holds the object `complete_mode` when the exact method answered; its field `complete` is the mark complete. The
object `policy` names the method that answered: `"answer_from": "the exhaustive search"` is the exact method,
`"ordinary gk"` the general method. The general method (`gk -general FILE`) has no mark complete.

A value is a list of four shares (for, against, conflict, ignorance); gk prints the unresolved share apart.
Python 3.9 or later, no other package.
"""
import json
import re


def term_text(t):
  if isinstance(t, list):
    if not t:
      return "[]"
    return str(t[0]) + ("(" + ",".join(term_text(x) for x in t[1:]) + ")" if len(t) > 1 else "")
  return str(t)


def lit_text(lit):
  """a literal in gk's JSON form (["-flies","tweety"]) as text (-flies(tweety))"""
  if isinstance(lit, str):
    return lit
  return term_text(lit)


def norm(t):
  """a literal without spaces and quotes, for comparisons"""
  return re.sub(r"[\s\"']", "", t or "")


def negate(lit):
  lit = norm(lit)
  return lit[1:] if lit.startswith("-") else "-" + lit


def parse_gk(out):
  """the first result object of gk's standard output, as a dict:
  kind: "recursive" (a value line), "result" (a line without a value), "error", "no line";
  answered_by: "exact" or "general"; complete: the mark of the exact method (None for the general method);
  limits: the exact method's limits; not_covered: the reason when the exact method does not cover the input;
  answers: [{"lit", "value", "unresolved", "complete", "limits"}];
  tasks_cut, tasks_queued, search, unfinished: the general method's fields."""
  r = {"kind": "no line", "answers": [], "answered_by": None, "complete": None, "limits": [], "not_covered": None,
       "covered": None, "policy": None}
  obj = None
  for line in (out or "").split("\n"):
    s = line.strip()
    if s.startswith('{"recursive"'):
      try:
        obj = json.loads(s)["recursive"]
        r["kind"] = "recursive"
      except ValueError:
        r["kind"] = "bad line"
      break
    if s.startswith('{"result"'):
      try:
        o = json.loads(s)
      except ValueError:
        o = {}
      r["kind"] = "result"
      r["result"] = o.get("result")
      r["policy"] = o.get("policy")
      if r["policy"]:
        r["answered_by"] = {"the exhaustive search": "exact", "ordinary gk": "general"}.get(
          r["policy"].get("answer_from"))
      break
    if s.startswith('{"error"'):
      try:
        r["error"] = json.loads(s)["error"]
      except ValueError:
        r["error"] = s[:300]
      r["kind"] = "error"
      break
  if obj is None:
    return r
  cm = obj.get("complete_mode")
  pol = obj.get("policy")
  r["policy"] = pol
  line_method = "exact" if cm is not None else "general"
  r["answered_by"] = {"the exhaustive search": "exact", "ordinary gk": "general"}.get(
    (pol or {}).get("answer_from"), line_method)
  for k in ("search", "tasks_cut", "tasks_queued", "unfinished", "stop", "applications", "readings"):
    if k in obj:
      r[k] = obj[k]
  if cm is not None:
    nc = cm.get("not_covered")
    r["covered"] = cm.get("covered")
    r["not_covered"] = (nc or {}).get("reason") if isinstance(nc, dict) else nc
    r["complete"] = cm.get("complete")
    r["limits"] = cm.get("limits") or []
    r["class"] = cm.get("class")
    r["exact_search"] = cm.get("search")
    for k in ("ground_statements", "ground_full", "tasks", "tasks_ended", "rounds"):
      r[k] = cm.get(k)
  answers = []
  if "answers" in obj:
    for a in obj["answers"]:
      answers.append({"lit": lit_text(a.get("answer")), "value": a.get("value"),
                      "unresolved": a.get("unresolved") or 0, "complete": a.get("complete"),
                      "limits": a.get("limits") or []})
  elif "question" in obj:
    answers.append({"lit": lit_text(obj["question"]), "value": obj.get("value"),
                    "unresolved": obj.get("unresolved") or 0,
                    "complete": (cm or {}).get("complete") if cm is not None else None,
                    "limits": (cm or {}).get("limits") or []})
  r["answers"] = answers
  return r


def flip(v):
  """the value of the opposite literal: for and against exchanged"""
  return [v[1], v[0], v[2], v[3]] + list(v[4:])


def gk_value(pg, lit):
  """(four shares, unresolved) of gk's answer for the literal lit, or (None, None); an answer for the
  opposite literal is turned around"""
  for a in pg.get("answers") or []:
    if a.get("value") is None:
      continue
    v = [float(x) for x in a["value"][:4]]
    if norm(a["lit"]) == norm(lit):
      return v, float(a.get("unresolved") or 0)
    if norm(a["lit"]) == negate(lit):
      return flip(v), float(a.get("unresolved") or 0)
  return None, None


def limit_text(x):
  if isinstance(x, list):
    return "%s: %s" % (x[0], x[1]) if len(x) > 1 else str(x[0])
  return str(x)


def ended_by_itself(pg, timed_out=False):
  """(True | False | None, reason) for one gk run. The exact method ended by itself when every answer is
  complete; the general method when no search was cut or left queued and the evaluation finished (gk then
  prints the search state "no further proof found within the budget")."""
  if timed_out:
    return False, "the time limit of the run"
  if pg is None or pg.get("kind") in ("no line", "bad line"):
    return None, "no line"
  if pg.get("kind") == "error":
    return None, "error: " + str(pg.get("error"))[:80]
  if pg.get("kind") == "result":
    return False, "no value: %s" % pg.get("result")
  if pg.get("answered_by") == "exact":
    if pg.get("covered") is False:
      return False, "not covered: " + str(pg.get("not_covered"))[:100]
    if pg.get("answers") and all(a.get("complete") is True for a in pg["answers"]):
      return True, "complete"
    lim = [limit_text(x) for a in pg.get("answers") or [] for x in a.get("limits") or []]
    lim += [limit_text(x) for x in pg.get("limits") or []]
    return False, "not complete: " + (lim[0] if lim else "no limit named")[:160]
  if pg.get("unfinished"):
    return False, "evaluation not finished"
  if (pg.get("tasks_cut") or 0) > 0 or (pg.get("tasks_queued") or 0) > 0:
    return False, "searches stopped: %s cut, %s queued" % (pg.get("tasks_cut") or 0, pg.get("tasks_queued") or 0)
  if pg.get("search") == "no further proof found within the budget":
    return True, "no search stopped"
  return None, "search state: " + str(pg.get("search"))[:80]


def parse_tool(out):
  """the tool's output object: {"mode", "bound", "unsupported", "limit", "answers": {literal: (four, unresolved)},
  "atoms": {atom: (four, unresolved)}, "error"}. "limit" is the stated limit of the tool's proof search
  (field proofs.limit); a value with such a limit is not an exact value of the semantics."""
  r = {"mode": None, "bound": None, "unsupported": None, "limit": None, "answers": {}, "atoms": {}, "error": None}
  d = None
  for line in (out or "").split("\n"):
    if line.startswith('{"mcref"'):
      try:
        d = json.loads(line)["mcref"]
      except ValueError:
        r["error"] = "bad JSON"
      break
  if d is None:
    r["error"] = r["error"] or "no output object"
    return r
  r["mode"] = d.get("mode")
  r["version"] = d.get("version")
  r["bound"] = float(d.get("error_bound") or 0.0)
  r["unsupported"] = d.get("unsupported")
  r["limit"] = (d.get("proofs") or {}).get("limit")
  for a in d.get("answers") or []:
    if a.get("value") is not None:
      r["answers"][norm(a.get("instance"))] = ([float(x) for x in a["value"][:4]], float(a.get("unstable") or 0))
  for a in d.get("atom_values") or []:
    if a.get("value") is not None:
      r["atoms"][norm(a.get("atom"))] = ([float(x) for x in a["value"][:4]], float(a.get("unstable") or 0))
  return r


def tool_value(tr, lit):
  """(four shares, unresolved) of the tool for the literal lit, or (None, None)"""
  for table in (tr.get("answers") or {}, tr.get("atoms") or {}):
    if norm(lit) in table:
      return table[norm(lit)]
    if negate(lit) in table:
      v, u = table[negate(lit)]
      return flip(v), u
  return None, None


def fmt(v):
  """a value as text: (0.396, 0.56, 0, 0.044)"""
  if v is None:
    return ""
  return "(" + ", ".join(num(x) for x in v) + ")"


def num(x):
  s = "%.10g" % float(x)
  if s in ("-0", "-0.0"):
    s = "0"
  return s


def read_value(text):
  """the four shares of a value written by fmt, or None"""
  t = (text or "").strip()
  if not (t.startswith("(") and t.endswith(")")):
    return None
  try:
    v = [float(x) for x in t[1:-1].split(",")]
  except ValueError:
    return None
  return v if len(v) == 4 else None


def close(u, v, tol):
  return u is not None and v is not None and len(u) == len(v) and all(
    abs(float(a) - float(b)) <= tol + 1e-12 for a, b in zip(u, v))
