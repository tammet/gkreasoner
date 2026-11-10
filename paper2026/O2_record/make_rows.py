"""Build rows.tsv of part O2 from the stored runs: one row per answer.

tools/collect.py calls build() with a function that returns the stored
output of a run. For every input of inputs.tsv this script reads gk's
output (the line {"recursive": ...} and the dump that follows it) and the
reference tool's output, pairs their answers, and classifies each answer
row as Section 7.1 of the paper counts it:

- an answer row is one ground answer; a question with variables gives a
  row for each instance that either side lists;
- a row agrees when each of its four shares differs from the tool's
  estimate by at most e = sqrt(ln(8/.05) / (2 n)), .011264 for n = 20,000;
- a row is settled when both sides give a value and the tool's
  unresolved share is 0;
- a differing row is classed by the first of: a reading that gk records,
  a contrapositive use of a certain rule, a step not represented, none.

The classes and flags are those of the record of 2026-11-09. Run
count_rows.py on rows.tsv for the counts of the paper.
"""
import json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "tools"))
import gkout as G  # noqa: E402

READINGS = ("taxonomy ignored", "same-atom exception", "mixed kinds as ordinary", "context copies", "cycle cut",
            "rank zero as equal rank", "residual variable represented by a fresh constant")
DIFFER = ("differ, gk records a reading", "differ, gk used a contrapositive", "differ, gk used a step not represented",
          "differ, no flag")
COLUMNS = ("input", "set", "answer", "class", "gk", "mcref", "unresolved", "tolerance", "max_difference", "flags",
           "readings", "searches_cut", "stop", "gk_exit", "gk_run", "mcref_run", "pending_steps")


def hoeffding(n):
  return math.sqrt(math.log(8 / 0.05) / (2 * n)) if n else 1.0


def json_objects(t):
  dec, i, out = json.JSONDecoder(), 0, []
  while True:
    j = t.find("{", i)
    if j < 0:
      return out
    try:
      o, k = dec.raw_decode(t[j:])
      out.append(o)
      i = j + k
    except ValueError:
      i = j + 1


def read_dump(text):
  i = text.find('{"@format":"gk_dump_v1"')
  if i < 0:
    return None
  try:
    return json.loads(text[i:])
  except ValueError:
    return json.JSONDecoder().raw_decode(text[i:])[0]


def contrapositive(dump):
  """gk applied a certain directed statement at another literal than its
  written head"""
  if not dump:
    return None
  for a in dump.get("applications") or []:
    if a.get("orientation") == "another literal" and str(a.get("confidence")) in ("1", "1.0") and \
       '"@kind":"directed"' in (a.get("text") or ""):
      return True
  return False


def close(x, y, e):
  return x is not None and y is not None and all(a is not None and b is not None and abs(a - b) <= e
                                                 for a, b in zip(x, y))


def gk_record(stdout):
  r = G.gk_line(stdout) or {}
  dump = read_dump(stdout)
  sf = (dump or {}).get("status_facts") or {}
  approximation = sorted({(x.get("by") or "") + ":" + (x.get("reading") or "") for x in sf.get("approximation", [])})
  names = [x[0] for x in (r.get("readings") or []) if isinstance(x, list) and x]
  names += [s.split(":", 1)[-1] for s in approximation]
  hits = sorted({n for n in names if n in READINGS})
  return r, names, hits, contrapositive(dump)


def fmt(v):
  return G.shares_text([round(x, 6) for x in v]) if v is not None else ""


def name_counts(names):
  c = {}
  for n in names:
    c[n] = c.get(n, 0) + 1
  return "; ".join("%s x%d" % (n, k) if k > 1 else n for n, k in c.items())


def rows_of(inp, st, gk_e, mc_e, gk_run, mc_run):
  r, names, hits, contra = gk_record(gk_e["stdout"])
  m = G.mcref_object(mc_e["stdout"]) or {}
  e = hoeffding(m.get("samples") or 0)
  snr = bool(r.get("steps_not_represented"))
  flags = list(hits) + (["contrapositive use of a certain rule"] if contra else []) + \
    (["step not represented"] if snr else [])
  base = {"input": inp, "set": st, "tolerance": "%.6f" % e, "readings": name_counts(names), "flags": "; ".join(flags),
          "searches_cut": str(r.get("tasks_cut", 0) or 0), "pending_steps": str(r.get("pending_steps", 0) or 0),
          "stop": r.get("stop") or "",
          "gk_exit": str(gk_e["status"]["exit"]), "gk_run": gk_run, "mcref_run": mc_run}
  if m.get("unsupported") or m.get("error") or not m:
    return [dict(base, answer="", **{"class": "tool declined: " + str(m.get("unsupported") or m.get("error"))})]
  answers = m.get("answers") or []
  texts = {}
  for a in answers:
    texts.setdefault(G.key_text(a["key"]), []).append(a["instance"])
  if not m.get("variables"):
    a = answers[0] if answers else None
    rvals = {G.key_text(a["key"]): r.get("value")} if a else {}
  else:
    rvals = {G.lit_text(x.get("answer")): x.get("value") for x in (r.get("answers") or [])}
  out, seen = [], set()
  for a in answers:
    pt = G.key_text(a["key"])
    seen.add(pt)
    rec = rvals.get(pt)
    only_mcref = pt not in rvals and bool(m.get("variables"))
    if len(texts[pt]) > 1:
      cls = "not comparable: two answers print alike"
    elif a["unstable"] > 0:
      cls = "incomplete: unstable worlds" + (", binding only in mcref" if only_mcref else "")
    elif only_mcref:
      subst = a["value"][0] > e or a["value"][1] > e or a["value"][2] > e
      cls = "binding only in mcref" + (" (with support)" if subst else " (ignorance)")
    elif rec is None:
      cls = "recursive has no value"
    elif close(a["value"], rec, e):
      cls = "agree with recursive"
    elif hits:
      cls = DIFFER[0]
    elif contra:
      cls = DIFFER[1]
    elif snr:
      cls = DIFFER[2]
    else:
      cls = DIFFER[3]
    md = max(abs(x - y) for x, y in zip(rec, a["value"])) if rec is not None else None
    out.append(dict(base, answer=pt, gk=fmt(rec), mcref=fmt(a["value"]), unresolved="%g" % a["unstable"],
                    max_difference="%.6f" % md if md is not None else "", **{"class": cls}))
  for inst, v in rvals.items():
    if inst not in seen:
      out.append(dict(base, answer=inst, gk=fmt(v), **{"class": "binding only in the record"}))
  if not answers and not rvals:
    out.append(dict(base, answer="", **{"class": "no answer in either"}))
  return out


def build(folder, entry_of, runs):
  """write rows.tsv; returns the number of inputs without both stored runs"""
  lines = open(os.path.join(folder, "inputs.tsv"), encoding="utf-8").read().rstrip("\n").split("\n")
  cols = lines[0].split("\t")
  rows, missing = [], 0
  for line in lines[1:]:
    x = dict(zip(cols, line.split("\t")))
    rel = x["input"][len("inputs/"):]
    gk_run, mc_run = rel + ".gk", rel + ".mcref"
    gk_e, mc_e = entry_of(gk_run), entry_of(mc_run)
    if gk_e is None or mc_e is None:
      missing += 1
      continue
    rows += rows_of(x["input"], x["set"], gk_e, mc_e, gk_run, mc_run)
  with open(os.path.join(folder, "rows.tsv"), "w", encoding="utf-8") as f:
    f.write("\t".join(COLUMNS) + "\n")
    for r in rows:
      f.write("\t".join(str(r.get(c, "")) for c in COLUMNS) + "\n")
  print("O2_record/rows.tsv: %d rows from %d inputs; %d inputs without both stored runs" % (
    len(rows), len(lines) - 1 - missing, missing))
  return 1 if missing else 0
