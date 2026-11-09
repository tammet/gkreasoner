#!/usr/bin/env python3
"""mcref_read: the input side of mcref (step 16b of the gk 1.2 work,
2026-10-30). It reads gk's JSON-LD-LOGIC input language, converts other
inputs with `gk FILE -writejson -recursive` (gk's parser only), turns
statements into clauses with a written head where gk sees one, and grounds
the clauses over the constants of the input.

The algorithm (orientation, one world, the rows, sampling) is mcref.py.
The description is README.md.

Entry point: read_input(path, max_ground) -> Input."""
import hashlib
import itertools
import json
import os
import subprocess

# the repository's gk: ../bin/gk in the gkreasoner layout (this folder is mcref/),
# ../../gk in the gk source layout (this folder is experiments/mc_reference);
# MCREF_GK overrides both
def _default_gk():
  here = os.path.dirname(os.path.abspath(__file__))
  cands = [os.path.normpath(os.path.join(here, "..", "bin", "gk")),
           os.path.normpath(os.path.join(here, "..", "..", "gk"))]
  for c in cands:
    if os.path.isfile(c) and os.access(c, os.X_OK):
      return c
  return cands[-1]


GK = os.environ.get("MCREF_GK", _default_gk())
CONNECTIVES = {"&", "|", "=>", "<=", "<=>", "and", "or", "not", "~", "forall", "exists", "xor", "nor", "nand",
               "<~>", "if", "then", "-"}
BUILTIN_TESTS = {"$less", "$greater", "$lessorequal", "$greaterorequal", "$is_int", "$is_real", "$is_number"}
ORDINARY_DOLLAR = {"$arc", "$narc"}


class Unsupported(Exception):
  pass


# ------------------------------------------------------------------ reading

def strip_comments(text):
  """C-style comments outside JSON strings"""
  out, i, n, instr = [], 0, len(text), False
  while i < n:
    c = text[i]
    if instr:
      out.append(c)
      if c == "\\" and i + 1 < n:
        out.append(text[i + 1]); i += 2; continue
      if c == '"':
        instr = False
      i += 1
    elif c == '"':
      instr = True; out.append(c); i += 1
    elif c == "/" and i + 1 < n and text[i + 1] == "/":
      while i < n and text[i] != "\n":
        i += 1
    elif c == "/" and i + 1 < n and text[i + 1] == "*":
      j = text.find("*/", i + 2)
      i = n if j < 0 else j + 2
    else:
      out.append(c); i += 1
  return "".join(out)


def sha256_file(path):
  with open(path, "rb") as f:
    return hashlib.sha256(f.read()).hexdigest()


def read_statements(path, conv, files=None):
  """the statement list of a file; conv collects the conversions used, files
  the files read with their sha256 (the provenance of the result)"""
  if files is not None:
    files.append([os.path.abspath(path), sha256_file(path)])
  ext = os.path.splitext(path)[1].lower()
  if ext in (".js", ".json"):
    with open(path, errors="replace") as f:
      text = strip_comments(f.read())
    try:
      data = json.loads(text)
    except ValueError as e:
      raise Unsupported("not JSON: %s" % str(e)[:80])
  else:
    cmd = [GK, os.path.basename(path), "-writejson", "-recursive"]
    try:
      p = subprocess.run(cmd, cwd=os.path.dirname(os.path.abspath(path)) or ".", capture_output=True, text=True,
                         errors="replace", timeout=120)
    except subprocess.TimeoutExpired:
      raise Unsupported("conversion failed: timeout")
    conv.append("gk -writejson -recursive")
    if files is not None:
      files.append(["gk", sha256_file(GK)])
      files.append(["converted", hashlib.sha256(p.stdout.encode()).hexdigest()])
    t = p.stdout.strip()
    try:
      data = json.loads(t[t.find("["):]) if "[" in t else None
    except ValueError:
      data = None
    if data is None:
      raise Unsupported("conversion failed: %s" % (p.stdout + p.stderr).strip()[:100])
  if not isinstance(data, list):
    raise Unsupported("the input is not a list of statements")
  out = []
  for item in data:
    if isinstance(item, dict) and "@include" in item and "@logic" not in item:
      inc = item["@include"]
      cands = [os.path.join(os.path.dirname(os.path.abspath(path)), inc), inc]
      if os.environ.get("TPTP"):
        cands.append(os.path.join(os.environ["TPTP"], inc))
      cands.append(os.path.join("/opt/TPTP", inc))
      f = next((c for c in cands if os.path.isfile(c)), None)
      if not f:
        raise Unsupported("include not found: %s" % inc)
      out += read_statements(f, conv, files)
    else:
      out.append(item)
  return out


# ------------------------------------------------------------------ formulas

def is_var(t):
  return isinstance(t, str) and t.startswith("?:")


# A constant is a typed value: ("s", string), ("i", integer) or ("r", real).
# JSON keeps 1, 1.0 and "1" apart, and so do grounding, atoms and answers.

def typed(v):
  if isinstance(v, str):
    return ("s", v)
  if isinstance(v, int):
    return ("i", v)
  return ("r", v)


def untyped(t):
  return t[1] if isinstance(t, tuple) else t


def term_text(t):
  """a term as printed: numbers bare (1, 1.0); a string bare unless it reads
  as a number or holds a separator, then in JSON quotes (p("1"))"""
  if not isinstance(t, tuple):
    return str(t)
  tag, v = t
  if tag == "i":
    return str(v)
  if tag == "r":
    return repr(v)
  try:
    float(v)
    return json.dumps(v)
  except ValueError:
    pass
  if not v or any(c in v for c in SEPARATORS):
    return json.dumps(v)
  return v


SEPARATORS = set(',()"\\ \t\n')


def lit_of(x):
  """('lit', sign, pred, args) for a literal form, else None. A bare string
  is a zero-arity atom that does not match the array form (args None)."""
  if isinstance(x, str):
    if x in CONNECTIVES:
      return None
    if x.startswith("-") and len(x) > 1:
      return ("lit", 1, x[1:], None)
    return ("lit", 0, x, None)
  if isinstance(x, list) and x and isinstance(x[0], str) and x[0] not in CONNECTIVES and x[0] != "$block":
    if any(isinstance(a, str) and a in ("=", "!=") for a in x[1:]):
      raise Unsupported("equality")
    pred = x[0]
    sign = 0
    if pred.startswith("-") and len(pred) > 1:
      sign, pred = 1, pred[1:]
    if pred in ("=", "!=", "$not"):
      raise Unsupported("equality" if pred != "$not" else "unsupported formula form: $not outside $block")
    for a in x[1:]:
      if isinstance(a, (list, dict)):
        raise Unsupported("function symbols")
      if isinstance(a, bool) or a is None:
        raise Unsupported("unsupported term: %r" % (a,))
    return ("lit", sign, pred, tuple(a if is_var(a) else typed(a) for a in x[1:]))
  return None


def block_of(x):
  """('block', strength, literal) for a $block element, else None"""
  if isinstance(x, list) and x and x[0] == "$block":
    if len(x) != 3:
      raise Unsupported("unsupported formula form: $block arity")
    s, target = x[1], x[2]
    if isinstance(s, list):
      raise Unsupported("taxonomy strength")
    if isinstance(s, bool) or not isinstance(s, int):
      raise Unsupported("unsupported $block strength %r" % (s,))
    if isinstance(target, list) and target and target[0] == "$not":
      l = lit_of(target[1])
      if not l:
        raise Unsupported("unsupported formula form: $block target")
      return ("block", s, ("lit", 1 - l[1], l[2], l[3]))
    l = lit_of(target)
    if not l:
      raise Unsupported("unsupported formula form: $block target")
    return ("block", s, l)
  return None


def bind_forall(x):
  """the body of ["forall", names, body]: a listed name without "?:" is a
  bound variable (gk reads ["forall", ["X"], ...] so) and becomes "?:name"
  in the argument positions of the body"""
  names = x[1] if isinstance(x[1], list) else [x[1]]
  ren = {n: "?:" + n for n in names if isinstance(n, str) and not n.startswith("?:")}
  if not ren:
    return x[2]
  def sub(t):
    if isinstance(t, list):
      if t and isinstance(t[0], str):
        return [t[0]] + [sub(e) for e in t[1:]]
      return [sub(e) for e in t]
    if isinstance(t, str):
      return ren.get(t, t)
    return t
  return sub(x[2])


def parse(x):
  """an AST: lit, block, ('and', [..]), ('or', [..]), ('not', a),
  ('imp', a, b), ('iff', a, b)"""
  l = lit_of(x)
  if l:
    return l
  b = block_of(x)
  if b:
    return b
  if not isinstance(x, list) or not x:
    raise Unsupported("unsupported formula form: %r" % (x,))
  h = x[0]
  if isinstance(h, str) and h in ("not", "~", "-") and len(x) == 2:
    return ("not", parse(x[1]))
  if h == "forall" and len(x) == 3:
    return ("forall", parse(bind_forall(x)))
  if h == "exists":
    raise Unsupported("existential quantifier")
  if h == "if":
    if "then" not in x:
      raise Unsupported("unsupported formula form: if without then")
    k = x.index("then")
    conds = [parse(c) for c in x[1:k]]
    cons = [parse(c) for c in x[k + 1:]]
    clits = [c for c in cons if c[0] == "lit"]
    cblocks = [c for c in cons if c[0] == "block"]
    if cblocks:
      # one head with its $block literals: a head chain, as gk reads it
      if len(clits) != 1 or len(clits) + len(cblocks) != len(cons):
        raise Unsupported("unsupported formula form: if-then with several heads and $block")
      head = ("or", clits + cblocks)
    else:
      head = cons[0] if len(cons) == 1 else ("and", cons)
    return ("imp", conds[0] if len(conds) == 1 else ("and", conds), head)
  ops = [e for i, e in enumerate(x) if i % 2 == 1 and isinstance(e, str) and e in CONNECTIVES]
  if ops and len(ops) == (len(x) - 1) // 2 and len(x) % 2 == 1:
    parts = [parse(e) for i, e in enumerate(x) if i % 2 == 0]
    if len(set(ops)) != 1:
      raise Unsupported("unsupported formula form: mixed connectives")
    op = ops[0]
    if op in ("&", "and"):
      return ("and", parts)
    if op in ("|", "or"):
      return ("or", parts)
    if len(parts) != 2:
      raise Unsupported("unsupported formula form: chained %s" % op)
    if op == "=>":
      return ("imp", parts[0], parts[1])
    if op == "<=":
      return ("imp", parts[1], parts[0])
    if op == "<=>":
      return ("iff", parts[0], parts[1])
    raise Unsupported("unsupported formula form: connective %s" % op)
  if all(isinstance(e, list) for e in x):
    return ("or", [parse(e) for e in x])
  raise Unsupported("unsupported formula form: %s" % json.dumps(x)[:60])


def neg_lit(l):
  return ("lit", 1 - l[1], l[2], l[3])


def nnf(a, neg=False):
  t = a[0]
  if t == "lit":
    return neg_lit(a) if neg else a
  if t == "block":
    if neg:
      raise Unsupported("unsupported formula form: negated $block")
    return a
  if t == "not":
    return nnf(a[1], not neg)
  if t == "forall":
    if neg:
      raise Unsupported("existential quantifier")
    return nnf(a[1], neg)
  if t in ("and", "or"):
    k = t if not neg else ("or" if t == "and" else "and")
    return (k, [nnf(p, neg) for p in a[1]])
  if t == "imp":
    return nnf(("or", [("not", a[1]), a[2]]), neg)
  if t == "iff":
    return nnf(("and", [("imp", a[1], a[2]), ("imp", a[2], a[1])]), neg)
  raise Unsupported("unsupported formula form")


def cnf(a):
  """a list of clauses, each a list of lit/block nodes"""
  t = a[0]
  if t in ("lit", "block"):
    return [[a]]
  if t == "and":
    out = []
    for p in a[1]:
      out += cnf(p)
    return out
  if t == "or":
    acc = [[]]
    for p in a[1]:
      cs = cnf(p)
      acc = [x + y for x in acc for y in cs]
      if len(acc) > 1000:
        raise Unsupported("unsupported formula form: clausification too large")
    return acc
  raise Unsupported("unsupported formula form")


def body_lits(a):
  """the literals of a body that is a literal or a conjunction of literals"""
  if a[0] == "lit":
    return [a]
  if a[0] == "and" and all(p[0] == "lit" for p in a[1]):
    return list(a[1])
  return None


def head_chain(a):
  """a head literal possibly followed by '|' and $block literals; a nested
  chain such as [[H, "|", B1], "|", B2] too, as gk's wr_js_dir_head reads it"""
  if a[0] == "lit":
    return a, []
  if a[0] == "or":
    leaves = []
    def flat(p):
      if p[0] == "or":
        for q in p[1]:
          flat(q)
      else:
        leaves.append(p)
    flat(a)
    lits = [p for p in leaves if p[0] == "lit"]
    blocks = [p for p in leaves if p[0] == "block"]
    if len(lits) == 1 and len(lits) + len(blocks) == len(leaves):
      return lits[0], blocks
  return None


def statement_clauses(logic, dirhead):
  """proto-clauses of one statement: dicts with lits (sign, pred, args),
  blocks (strength, lit) and head (an index into lits, or None). The written
  head follows gk's input rules (Builtparser/jsparse.c, the comment before
  wr_js_dir_isconn): a literal list with "@dirhead", [body, "=>", head],
  [head, "<=", body] and ["if", .., "then", head] with a literal or
  conjunctive body; one ordinary literal is a fact; anything else a clause"""
  x = logic
  while isinstance(x, list) and len(x) == 3 and x[0] == "forall":
    x = bind_forall(x)
  if isinstance(dirhead, int) and not isinstance(dirhead, bool) and isinstance(x, list) and x and isinstance(x[0], list):
    items = [parse(e) for e in x]
    lits = [e for e in items if e[0] == "lit"]
    blocks = [e for e in items if e[0] == "block"]
    if len(lits) + len(blocks) != len(items):
      raise Unsupported("unsupported formula form: @dirhead list")
    if not (0 <= dirhead < len(items)) or items[dirhead][0] != "lit":
      raise Unsupported("unsupported formula form: @dirhead index")
    hidx = [i for i, e in enumerate(items) if e[0] == "lit"].index(dirhead)
    return [{"lits": [l[1:] for l in lits], "blocks": [(b[1], b[2][1:]) for b in blocks], "head": hidx}]
  a = parse(x)
  while a[0] == "forall":
    a = a[1]
  rule = None
  if a[0] == "imp":
    body = body_lits(a[1])
    hc = head_chain(a[2])
    if body is not None and hc is not None:
      rule = (body, hc[0], hc[1])
  if rule:
    body, head, blocks = rule
    lits = [neg_lit(l)[1:] for l in body] + [head[1:]]
    return [{"lits": lits, "blocks": [(b[1], b[2][1:]) for b in blocks], "head": len(lits) - 1}]
  cls = cnf(nnf(a))
  out = []
  for c in cls:
    lits = [e[1:] for e in c if e[0] == "lit"]
    blocks = [(e[1], e[2][1:]) for e in c if e[0] == "block"]
    out.append({"lits": lits, "blocks": blocks, "head": 0 if len(lits) == 1 else None})
  return out


# ------------------------------------------------------------------ statements and the question

def confidence_of(st):
  c = st.get("@confidence", 1.0) if isinstance(st, dict) else 1.0
  if isinstance(c, bool) or not isinstance(c, (int, float)):
    raise Unsupported("unsupported confidence %r" % (c,))
  if isinstance(c, int):
    if not 0 <= c <= 100:
      raise Unsupported("unsupported confidence %r" % (c,))
    return c / 100.0
  if not 0 <= c <= 1:
    raise Unsupported("unsupported confidence %r" % (c,))
  return float(c)


def question_literal(f):
  """the literal of a question formula"""
  l = lit_of(f) if not (isinstance(f, list) and f and isinstance(f[0], list)) else None
  if l:
    return l[1:]
  try:
    a = parse(f)
  except Unsupported:
    raise Unsupported("compound question")
  s = json.dumps(f)
  if a[0] == "imp" or '"if"' in s or '"=>"' in s or '"<="' in s:
    raise Unsupported("conditional question")
  raise Unsupported("compound question")


def has_equality(x):
  """an "=" or "!=" anywhere in a formula (as a predicate or infix)"""
  if isinstance(x, str):
    return x in ("=", "!=", "-=")
  if isinstance(x, list):
    return any(has_equality(e) for e in x)
  return False


def classify(stmts):
  """(clauses with their confidence and statement index, question literal)"""
  clauses, questions = [], []
  for st in stmts:
    f = (st.get("@logic", st.get("@question")) if isinstance(st, dict) else st)
    if has_equality(f):
      raise Unsupported("equality")
  for si, st in enumerate(stmts):
    if isinstance(st, dict):
      if "@report" in st or "@marginal" in st:
        raise Unsupported("@report or @marginal declaration")
      if "@question" in st:
        questions.append(question_literal(st["@question"]))
        continue
      if "@logic" not in st:
        raise Unsupported("JSON-LD structure")
      role = st.get("@role")
      logic = st["@logic"]
      if role in ("question", "conjecture"):
        questions.append(question_literal(logic))
        continue
      dirhead = st.get("@dirhead")
    else:
      logic, role, dirhead = st, None, None
    conf = confidence_of(st)
    if conf == 0:
      continue
    # a goal clause with $ans: the question is the complement of its literal
    if isinstance(logic, list) and logic and isinstance(logic[0], list) and \
       any(isinstance(e, list) and e and e[0] == "$ans" for e in logic):
      rest = [e for e in logic if not (isinstance(e, list) and e and e[0] == "$ans")]
      if len(rest) != 1:
        raise Unsupported("compound question")
      l = lit_of(rest[0])
      if not l:
        raise Unsupported("compound question")
      questions.append(neg_lit(l)[1:])
      continue
    if role == "negated_conjecture":
      l = lit_of(logic)
      if not l:
        raise Unsupported("compound question")
      questions.append(neg_lit(l)[1:])
      continue
    pcs = statement_clauses(logic, dirhead)
    if len(pcs) > 1 and conf < 1:
      raise Unsupported("uncertain formula with several clauses")
    for pc in pcs:
      clauses.append((si, conf, pc))
  if not questions:
    raise Unsupported("no question")
  if len(questions) > 1:
    raise Unsupported("several questions")
  return clauses, questions[0]


# ------------------------------------------------------------------ grounding

def atom_text(pred, args):
  if not args:
    return pred
  return pred + "(" + ",".join(term_text(a) for a in args) + ")"


def lit_text(sign, pred, args):
  return ("-" if sign else "") + atom_text(pred, args)


def num(t):
  return isinstance(t, tuple) and t[0] in ("i", "r")


def builtin_value(pred, args):
  """the truth of a ground built-in condition over typed constants"""
  if pred in ("$less", "$greater", "$lessorequal", "$greaterorequal"):
    if len(args) != 2 or not (num(args[0]) and num(args[1])):
      raise Unsupported("unknown built-in: %s on non-numbers" % pred)
    a, b = args[0][1], args[1][1]
    return {"$less": a < b, "$greater": a > b, "$lessorequal": a <= b, "$greaterorequal": a >= b}[pred]
  if pred == "$is_int":
    return len(args) == 1 and args[0][0] == "i"
  if pred == "$is_real":
    return len(args) == 1 and args[0][0] == "r"
  if pred == "$is_number":
    return len(args) == 1 and num(args[0])
  raise Unsupported("unknown built-in: %s" % pred)


def is_builtin(pred):
  return pred.startswith("$") and pred not in ORDINARY_DOLLAR


def constants_of(clauses, qlit):
  cs = set()
  def add(args):
    for a in args or ():
      if not is_var(a):
        cs.add(a)
  for _si, _c, pc in clauses:
    for s, p, args in pc["lits"]:
      add(args)
    for _st, (s, p, args) in pc["blocks"]:
      add(args)
  add(qlit[2])
  return sorted(cs, key=lambda a: (a[0], str(a[1])))


def clause_vars(pc):
  """the variables of a proto-clause: (in ordinary literals, only in built-in
  literals, only in exception literals)"""
  ordv, bv, ev = [], [], []
  for _s, p, args in pc["lits"]:
    for a in args or ():
      if is_var(a):
        (bv if is_builtin(p) else ordv).append(a)
  for _st, (_s, _p, args) in pc["blocks"]:
    ev += [a for a in (args or ()) if is_var(a)]
  def uniq(xs):
    out = []
    for x in xs:
      if x not in out:
        out.append(x)
    return out
  ordv = uniq(ordv)
  return ordv, [a for a in uniq(bv) if a not in ordv], [a for a in uniq(ev) if a not in ordv and a not in bv]


def ground(clauses, consts, max_ground):
  """ground clauses: (statement index, conf, lits, blocks, head) with the
  built-in conditions computed (decision 66). A variable that occurs only in
  exception literals is not grounded per clause: for each grounding of the
  other variables its instances are all exceptions of one ground clause
  (decision 67, the existential reading). A variable that occurs only in
  built-in literals is unsupported: the built-in ranges over an open domain."""
  total = 0
  for _si, _c, pc in clauses:
    ordv, bv, ev = clause_vars(pc)
    if bv:
      raise Unsupported("built-in over an open domain")
    total += len(consts) ** (len(ordv) + len(ev))
    if total > max_ground:
      raise Unsupported("grounding limit")
  out = []
  for si, conf, pc in clauses:
    vs, _bv, ev = clause_vars(pc)
    etuples = list(itertools.product(consts, repeat=len(ev))) if ev else [()]
    seen = set()
    for tup in (itertools.product(consts, repeat=len(vs)) if vs else [()]):
      sub = dict(zip(vs, tup))
      def g(l, sub=sub):
        s, p, args = l
        return (s, p, None if args is None else tuple(sub.get(a, a) for a in args))
      lits = [g(l) for l in pc["lits"]]
      blocks = []
      for et in etuples:
        esub = dict(sub, **dict(zip(ev, et)))
        for st, l in pc["blocks"]:
          b = (st, g(l, esub))
          if b not in blocks:
            blocks.append(b)
      head = pc["head"]
      keep, drop = [], False
      for i, l in enumerate(lits):
        if is_builtin(l[1]):
          if head is not None and i == head:
            raise Unsupported("unknown built-in: %s as a head" % l[1])
          cond = builtin_value(l[1], l[2] or ())   # the condition is the complement of the clause literal
          true_cond = cond if l[0] == 1 else not cond
          if true_cond:
            continue
          drop = True
          break
        keep.append(l)
      if drop:
        continue
      for st, l in blocks:
        if is_builtin(l[1]):
          raise Unsupported("unknown built-in: %s in an exception" % l[1])
      if not keep:
        raise Unsupported("empty ground clause")
      # a clause is a set of literals: a repeated literal counts once
      hl = lits[head] if head is not None else None
      keep = [l for i, l in enumerate(keep) if l not in keep[:i]]
      nh = keep.index(hl) if hl is not None and hl in keep else None
      key = (tuple(keep), tuple(blocks), nh)
      if key in seen:
        continue
      seen.add(key)
      out.append((si, conf, keep, blocks, nh))
  return out


class Input:
  """a read and grounded input"""
  def __init__(self):
    self.files = []            # [path, sha256] of every file read; ["gk", sha256]; ["converted", sha256]
    self.converted_by = None
    self.question = None       # (sign, pred, args) with variables
    self.qvars = []            # the question's variables, in order
    self.constants = []
    self.ground = []           # ground clauses: (statement index, conf, lits, blocks, head)


def read_input(path, max_ground, files=None):
  """read, classify and ground an input; raises Unsupported. `files`, when
  given, collects the provenance also when the input is unsupported."""
  inp = Input()
  if files is not None:
    inp.files = files
  conv = []
  try:
    stmts = read_statements(path, conv, inp.files)
  finally:
    inp.converted_by = conv[0] if conv else None
  clauses, q = classify(stmts)
  inp.question = q
  qs, qp, qargs = q
  for a in qargs or ():
    if is_var(a) and a not in inp.qvars:
      inp.qvars.append(a)
  if is_builtin(qp) or qp in ("=", "!="):
    raise Unsupported("equality" if qp in ("=", "!=") else "unknown built-in: %s in the question" % qp)
  inp.constants = constants_of(clauses, q)
  has_vars = bool(inp.qvars) or any(any(clause_vars(pc)) for _si, _c, pc in clauses)
  if has_vars and not inp.constants:
    raise Unsupported("no constants")
  inp.ground = ground(clauses, inp.constants, max_ground)
  return inp
