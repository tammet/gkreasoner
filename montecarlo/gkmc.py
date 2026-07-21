#!/usr/bin/env python3
"""
gkmc.py -- estimate gk confidences by random sampling.

Read a confidence c on a fact or rule as the probability that the statement
holds. In one trial, include each uncertain statement with probability equal
to its confidence and drop it otherwise; the included clauses (confidences
removed, their $block literals kept), together with the question, are decided
by a plain boolean run of gk. Over many trials, the fraction in which an answer
is provable estimates its confidence. This is inclusion sampling.

--draws per-instance (default): each ground instance of a clause is included by
its own draw. --draws shared: all instances of one input statement share a
single draw, matching how gk counts one statement as a single piece of
evidence.

--semantics subtract (default): per answer a, the fraction of trials with a
provable minus the fraction with the negation of a provable. This matches gk's
reported confidence, which also subtracts the support against an answer. With
no negative evidence the second term is zero and the number is plain
provability.
--semantics provable: the positive fraction (a provable) only.
--semantics gkdefault: the fraction of trials where a plain default gk run
accepts the closed answer instance.
--semantics threshold: a separate method (threshold_worlds.py), threshold
sampling. Each ground atom draws one random acceptance threshold in [0,1]; a
piece of evidence counts only if its confidence is above that threshold, and
the same threshold applies to evidence for and against the atom. It reports the
four masses support_for, support_against, conflict and ignorance for a ground
query and runs no gk subprocess.

--classify (ground single-literal question): also proves the negated question
per trial and prints the A-only / not-A-only / both / neither table.

usage: ./gkmc.py [-n TRIALS] [--seed S] [--draws per-instance|shared]
                 [--semantics subtract|provable|gkdefault|threshold]
                 [--classify] [--gk PATH] [--gk-args "..."]
                 [--gk-timeout SEC] [--jobs J] [--max-ground M]
                 [--keep-worlds DIR] [--json OUT] input.js

Limits: constants only (no function symbols). Threshold sampling and
--classify need a ground, single-literal question; ordinary inclusion sampling
also supports variables in a single-literal question. Results are estimates
with a sampling interval.
"""

import argparse
import json
import math
import os
import random
import re
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from itertools import product

# ---------------------------------------------------------------- input reading

def strip_comments(text):
    """Remove // and /* */ comments without changing quoted JSON strings."""
    out = []
    i = 0
    in_string = False
    escaped = False
    line_comment = False
    block_comment = False
    while i < len(text):
        ch = text[i]
        nxt = text[i + 1] if i + 1 < len(text) else ""
        if line_comment:
            if ch == "\n":
                line_comment = False
                out.append(ch)
            i += 1
            continue
        if block_comment:
            if ch == "*" and nxt == "/":
                block_comment = False
                i += 2
            else:
                if ch == "\n":
                    out.append(ch)
                i += 1
            continue
        if in_string:
            out.append(ch)
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
            i += 1
            continue
        if ch == '"':
            in_string = True
            out.append(ch)
            i += 1
        elif ch == "/" and nxt == "/":
            line_comment = True
            i += 2
        elif ch == "/" and nxt == "*":
            block_comment = True
            i += 2
        else:
            out.append(ch)
            i += 1
    return "".join(out)


def read_source(path):
    data = open(path, "rb").read()
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return data.decode("latin-1")

def norm_conf(v):
    v = float(v)
    return v / 100.0 if v > 1.0 else v

def load_original(path):
    """Ordered statements of the original file: (is_question, confidence, item)."""
    items = json.loads(strip_comments(read_source(path)))
    stmts = []
    for it in items:
        if isinstance(it, dict) and "@question" in it:
            stmts.append((True, 1.0, it))
        elif isinstance(it, dict) and it.get("@role") == "question":
            stmts.append((True, 1.0, {"@question": it["@logic"]}))
        elif isinstance(it, dict) and "@logic" in it:
            stmts.append((False, norm_conf(it.get("@confidence", 1.0)), it))
        elif isinstance(it, list):
            stmts.append((False, 1.0, {"@logic": it}))
        else:
            raise SystemExit(f"unsupported top-level item: {it!r}")
    return stmts

def clausify(gk, path):
    p = subprocess.run([gk, path, "-clausify"], capture_output=True, text=True,
                       timeout=60)
    try:
        return json.loads(p.stdout)
    except json.JSONDecodeError:
        raise SystemExit(f"gk -clausify failed on {path}:\n{p.stdout[:500]}{p.stderr[:500]}")

def load_clausified(gk, path):
    """Run `gk FILE -defworlds -clausify` and return the gk_clauses_v1 clause items
    (the array minus its leading meta object). ASSERTS the format header and fails
    loudly on drift (gk owns the clausifier and the root-split; this tool
    only consumes that serialization). Each item is a dict with
    @logic and, on the defworlds-side export, @confidence (post-split), @head
    (implied-literal index; fact 0, marker-less rule clause -1) and, on goals,
    @role:'goal'. Returns (items, meta)."""
    p = subprocess.run([gk, path, "-defworlds", "-clausify"],
                       capture_output=True, text=True, timeout=120)
    try:
        arr = json.loads(p.stdout)
    except json.JSONDecodeError:
        raise SystemExit(f"gk -defworlds -clausify failed on {path}:\n"
                         f"{p.stdout[:400]}{p.stderr[:400]}")
    if not (isinstance(arr, list) and arr and isinstance(arr[0], dict)
            and arr[0].get("format") == "gk_clauses_v1"):
        head = arr[0] if isinstance(arr, list) and arr else arr
        raise SystemExit(f"gk_clauses_v1 format header missing on {path}: "
                         f"got {head!r} -- this tool requires the versioned "
                         f"export (gk -defworlds -clausify)")
    return arr[1:], arr[0]

# ---------------------------------------------------------------- term walking

def walk_atom_args(term, on_const, on_var, depth=0):
    """Walk one atom/term list; constants and variables via callbacks.
    Handles $block/$not wrappers and rejects nested function terms."""
    if isinstance(term, str):
        if term.startswith("?:"):
            on_var(term)
        elif not term.startswith("$"):
            on_const(term)
        return
    if isinstance(term, (int, float)):
        on_const(term)
        return
    if not isinstance(term, list) or not term:
        return
    head = term[0]
    if head == "$not":
        for sub in term[1:]:
            walk_atom(sub, on_const, on_var)
        return
    raise SystemExit(f"function terms not supported in v1: {term!r}")

def walk_atom(atom, on_const, on_var):
    """atom = [pred, arg...] or [\"$block\", n, atom] or bare string."""
    if isinstance(atom, str):
        return  # propositional constant as literal: no args
    if not isinstance(atom, list) or not atom:
        return
    if atom[0] == "$block":
        for sub in atom[2:]:
            walk_atom(sub, on_const, on_var)
        return
    if atom[0] == "$not":
        for sub in atom[1:]:
            walk_atom(sub, on_const, on_var)
        return
    for arg in atom[1:]:
        walk_atom_args(arg, on_const, on_var)

def clause_vars(clause):
    vs = set()
    for lit in clause:
        walk_atom(lit, lambda c: None, vs.add)
    return sorted(vs)

def clause_consts(clause, acc):
    for lit in clause:
        walk_atom(lit, acc.add, lambda v: None)

def substitute(term, sub):
    if isinstance(term, str):
        return sub.get(term, term)
    if isinstance(term, list):
        return [substitute(x, sub) for x in term]
    return term

# ---------------------------------------------------------------- grounding

def ground_pool(clausified, stmts, max_ground):
    """Returns (pool, questions, warnings): pool = list of (orig_idx, clause);
    orig_idx indexes stmts; questions = original @question items."""
    # gk -clausify keeps input order and repeats one name on all clauses split
    # from one statement (original @name if present, generated frm_N otherwise):
    # group consecutive same-name runs; the k-th run maps to the k-th statement.
    # gk appends an $auto_negated_question artifact: drop it first.
    clausified = [st for st in clausified
                  if st.get("@name") != "$auto_negated_question"]
    runs = []
    for st in clausified:
        name = st.get("@name", "")
        if runs and runs[-1][0] == name:
            runs[-1][1].append(st)
        else:
            runs.append((name, [st]))
    if len(runs) != len(stmts):
        raise SystemExit(f"clausified statement runs {len(runs)} != "
                         f"original count {len(stmts)}: mapping unsafe")
    by_name = {k + 1: sts for k, (_, sts) in enumerate(runs)}
    order = list(by_name)
    consts = set()
    for st in clausified:
        clause_consts(st["@logic"], consts)
    consts = sorted(consts, key=str)
    if not consts:
        consts = ["c0"]  # degenerate: fully propositional input

    pool = []
    questions = []
    warnings = []
    total = 0
    for n in order:
        is_q = stmts[n - 1][0] or \
               any(st.get("@role") == "negated_conjecture" for st in by_name[n])
        if is_q:
            questions.append(stmts[n - 1][2])
            continue
        conf = stmts[n - 1][1]
        if len(by_name[n]) > 1 and conf < 1.0:
            warnings.append(
                f"frm_{n} (confidence {conf}) clausifies into {len(by_name[n])} "
                f"clauses; per-instance draws include each of its ground "
                f"clauses separately")
        seen = set()
        for st in by_name[n]:
            clause = st["@logic"]
            vs = clause_vars(clause)
            for tup in product(consts, repeat=len(vs)):
                sub = dict(zip(vs, tup))
                g = substitute(clause, sub)
                key = json.dumps(g, sort_keys=True)
                if key in seen:
                    continue
                seen.add(key)
                pool.append((n - 1, g))
                total += 1
                if total > max_ground:
                    raise SystemExit(f"ground pool exceeds --max-ground "
                                     f"{max_ground}; refusing to truncate")
    if not questions:
        raise SystemExit("no @question found: the oracle requires a goal")
    return pool, questions, warnings

# ---------------------------------------------------------------- world running

def norm_key(answer_text):
    t = answer_text.strip().rstrip(",")
    if t == "true":
        return "yes"
    if t == "false":
        return None  # a negation-only result does not prove the question
    args = re.findall(r'"\$ans"\s*((?:,\s*(?:"[^"]*"|[\w.-]+))+)', t)
    if args:
        vals = re.findall(r'"([^"]*)"|(-?\b[\w.]+\b)', args[0])
        return ",".join(a or b for a, b in vals)
    return t

def parse_world_answers(out):
    keys = []
    for line in out.splitlines():
        m = re.search(r'"answer":\s*(.+?),?\s*$', line)
        if m:
            k = norm_key(m.group(1))
            if k is not None:
                keys.append(k)
    return keys

def negate_question(qitem):
    q = qitem["@question"]
    if not (isinstance(q, list) and q and isinstance(q[0], str)):
        raise SystemExit("--classify needs a single-literal question")
    if any(isinstance(x, str) and x.startswith("?:") for x in q):
        raise SystemExit("--classify needs a ground (closed) question")
    neg = ["-" + q[0].lstrip("-") if not q[0].startswith("-") else q[0][1:]] + q[1:]
    neg[0] = q[0][1:] if q[0].startswith("-") else "-" + q[0]
    return {"@question": neg}

def question_var_order(q):
    """?:vars of a question literal in first-occurrence order -- the order in
    which gk lists their bindings in the $ans literal (verified empirically:
    r(a,b) queried with r(?:X,?:Y) answers $ans a,b)."""
    seen = []
    def walk(t):
        if isinstance(t, str):
            if t.startswith("?:") and t not in seen:
                seen.append(t)
        elif isinstance(t, list):
            for x in t:
                walk(x)
    walk(q)
    return seen

def parse_ans_value(v):
    # norm_key stringifies $ans bindings; input constants may be JSON numbers
    try:
        return int(v)
    except ValueError:
        try:
            return float(v)
        except ValueError:
            return v

def question_instances(qitem, anskey):
    """(positive, negated) ground instances of the question for one answer
    key: substitute the answer's bindings (first-occurrence variable order),
    and flip the sign for the negation -- the same per-answer negative check
    gk runs itself. anskey 'yes' = closed question, empty binding. BOTH sides
    of the pairing are decided from these closed instances: open questions
    are unreliable in contradictory worlds (the unit carrying the answer can
    be simplified away before the open goal uses it), closed ones are not."""
    q = qitem["@question"]
    if not (isinstance(q, list) and q and isinstance(q[0], str)):
        raise ValueError("subtraction needs a single-literal question")
    vars_ = question_var_order(q)
    vals = [] if anskey == "yes" else [parse_ans_value(v)
                                       for v in anskey.split(",")]
    if len(vals) != len(vars_):
        raise ValueError(f"answer '{anskey}' has {len(vals)} bindings but the "
                         f"question has {len(vars_)} variables")
    inst = substitute(q, dict(zip(vars_, vals)))
    neg = [inst[0][1:] if inst[0].startswith("-") else "-" + inst[0]] + inst[1:]
    return {"@question": inst}, {"@question": neg}

class Runner:
    def __init__(self, args, pool, confs, questions, neg_questions, tmpdir):
        self.args = args
        self.pool = pool
        self.confs = confs
        self.questions = questions
        self.neg_questions = neg_questions
        self.tmpdir = tmpdir

    def sample(self, trial):
        rng = random.Random(f"{self.args.seed}:{trial}")
        active = []
        shared = {}
        for orig, clause in self.pool:
            c = self.confs[orig]
            if c >= 1.0:
                active.append(clause)
                continue
            if self.args.coins == "shared":
                if orig not in shared:
                    shared[orig] = rng.random() < c
                ok = shared[orig]
            else:
                ok = rng.random() < c
            if ok:
                active.append(clause)
        return active

    def run_gk(self, path, gk_default=False):
        # world runs decide PURE PROVABILITY (with defaults/blockers): gk's own
        # negative-evidence subtraction must not run, or contradictory worlds
        # would report "evidence below limit" instead of "provable"; -plain
        # tells gk the input has no confidences and - when no blockers are
        # present - skips the blockers/defaults machinery too.
        # gk_default=True instead runs a PLAIN DEFAULT gk (no flags): world
        # clauses carry implicit confidence 1, the negative check is active,
        # so a contradictory world rejects the answer (pos-neg = 0, below
        # limit) - the world-level A-only verdict. -plain alone cannot do
        # this: use_confidence=0 zeroes all confidences and the 0.1 threshold
        # then rejects EVERYTHING, contradictory or not.
        # gkdefault emulates the LEGACY accepted-answer functional (pos-neg
        # with the threshold), so because gk now defaults to
        # the four-mass report, it must pin -olduncertainty explicitly. The
        # provable/subtract mode keeps -plain, which auto-disables the
        # four-mass machinery anyway.
        flags = ["-olduncertainty"] if gk_default else ["-nonegative", "-plain"]
        try:
            p = subprocess.run([self.args.gk, path] + flags
                               + self.args.gk_args,
                               capture_output=True, text=True,
                               timeout=self.args.gk_timeout)
        except subprocess.TimeoutExpired:
            return None
        return parse_world_answers(p.stdout)

    def run_question(self, t, questions, tag="", gk_default=False):
        path = os.path.join(self.tmpdir, f"world_{t}{tag}.js")
        with open(path, "w") as f:
            json.dump(self.world_doc(t) + questions, f)
        res = self.run_gk(path, gk_default)
        if not self.args.keep_worlds:
            os.unlink(path)
        return res

    def world_doc(self, t):
        # sample() is deterministic in t, so the same world can be re-decided
        # later against other questions (the per-answer negation pass)
        active = self.sample(t)
        return [{"@name": f"w{i}", "@logic": cl} for i, cl in enumerate(active)]

    def trial(self, t):
        pos = self.run_question(t, self.questions)
        neg = None
        if self.neg_questions is not None:
            neg = self.run_question(t, self.neg_questions, "n")
        return pos, neg

# ---------------------------------------------------------------- aggregation

def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))

def paired_diff_ci(pos_only, neg_only, n, z=1.96):
    """Normal-approximation CI for P(pos)-P(neg) estimated on the SAME worlds:
    the both/neither cells cancel, so the difference is (pos_only-neg_only)/n
    with variance (p1+p2-(p1-p2)^2)/n (paired multinomial; Wilson does not
    apply to a difference)."""
    if n == 0:
        return 0.0, (0.0, 0.0)
    p1, p2 = pos_only / n, neg_only / n
    diff = p1 - p2
    se = math.sqrt(max(0.0, p1 + p2 - diff * diff) / n)
    return diff, (diff - z * se, diff + z * se)

def gk_own_confidences(gk, path, extra):
    try:
        p = subprocess.run([gk, path] + extra, capture_output=True, text=True,
                           timeout=120)
    except subprocess.TimeoutExpired:
        return {}
    pairs = {}
    cur = None
    for line in p.stdout.splitlines():
        m = re.search(r'"answer":\s*(.+?),?\s*$', line)
        if m:
            cur = norm_key(m.group(1))
            continue
        m = re.search(r'"confidence":\s*(-?[0-9.eE+]+)', line)
        if m and cur is not None:
            pairs.setdefault(cur, float(m.group(1)))
            cur = None
    return pairs

MASS_FIELDS = ("support_for", "support_against", "conflict", "ignorance")


def _query_atom_sign(qitem):
    import threshold_worlds as sr
    q = qitem["@question"]
    if isinstance(q, str):
        if q.startswith("?:"):
            raise SystemExit("threshold sampling needs a ground query")
        pred, sign = sr._split_sign(q)
        return (pred, ()), sign
    if not (isinstance(q, list) and q and isinstance(q[0], str)):
        raise SystemExit("threshold sampling needs one predicate literal as its query")
    if q[0].startswith("$"):
        raise SystemExit("threshold sampling does not evaluate arithmetic or other built-in predicates")
    if question_var_order(q):
        raise SystemExit("threshold sampling needs a ground query")
    if any(isinstance(arg, list) for arg in q[1:]):
        raise SystemExit("threshold sampling does not support function terms in the query")
    pred, sign = sr._split_sign(q[0])
    return (pred, tuple(q[1:])), sign


def _load_expected_tsv(path):
    exp = {}
    with open(path) as f:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue
            ex, field, value, _src = line.rstrip("\n").split("\t")
            if field in MASS_FIELDS:
                exp.setdefault(ex, {})[field] = float(value)
    return exp


def run_threshold(args):
    """Threshold sampling. Prints the four masses (support_for,
    support_against, conflict, ignorance) for the query."""
    import threshold_worlds as sr
    seed = 0
    try:
        seed = int(args.seed)
    except (TypeError, ValueError):
        seed = hash(args.seed) & 0x7fffffff

    if args.check:
        expected = _load_expected_tsv(os.path.join(args.check, "expected.tsv"))
        npass = nfail = ndefer = 0
        for ex in sorted(expected):
            kb = os.path.join(args.check, ex + ".js")
            if not os.path.exists(kb):
                continue
            stmts = load_original(kb)
            pool, confs, questions = sr.ground_original(stmts)
            qatom, qsign = _query_atom_sign(questions[0])
            res = sr.evaluate(pool, confs, qatom, qsign, args.trials, seed)
            if res.get("not_scored"):
                print(f"NOT-SCORED {ex}: {res['not_scored']}")
                ndefer += 1
                continue
            exp = expected[ex]
            bad = [f"{f} got {res.get(f):.4f} exp {exp[f]:.4f}"
                   for f in MASS_FIELDS
                   if f in exp and (res.get(f) is None
                                    or abs(res[f] - exp[f]) > 0.005)]
            note = f"  [{res['priority_note']}]" if res.get("priority_note") else ""
            if bad and res.get("priority_note"):
                print(f"NOT-SCORED {ex}: " + "; ".join(bad) + note)
                ndefer += 1
            elif bad:
                print(f"FAIL  {ex}: " + "; ".join(bad) + note)
                nfail += 1
            else:
                print(f"OK    {ex}  " + " ".join(
                    f"{f.split('_')[-1][:3]}={res[f]:.4f}"
                    for f in MASS_FIELDS) + note)
                npass += 1
        print(f"\n{npass} pass, {nfail} fail, {ndefer} not scored "
              f"(n={args.trials}, seed={seed})")
        return 1 if nfail else 0

    stmts = load_original(args.input)
    pool, confs, questions = sr.ground_original(stmts)
    if not questions:
        raise SystemExit("threshold sampling needs exactly one @question")
    # P6 (settlement memo, 2026-07-21): an OPEN query is evaluated per closed
    # instance over the Herbrand constants of the non-goal clauses -- the same
    # per-answer instancing the inclusion sampler and gk's own open path use.
    q = questions[0]["@question"]
    qvars = []
    def _walkvars(t):
        if isinstance(t, str):
            if t.startswith("?:") and t not in qvars:
                qvars.append(t)
        elif isinstance(t, list):
            for x in t:
                _walkvars(x)
    _walkvars(q)
    instances = [questions[0]]
    if qvars:
        consts = set()
        for (is_q, _c, item) in stmts:
            if is_q:
                continue
            clause_logic = item.get("@logic")
            clause = sr._as_clause(clause_logic)
            gkmc_mod = sys.modules[__name__]
            gkmc_mod.clause_consts(clause, consts)
        consts = sorted(consts, key=str) or ["c0"]
        instances = []
        for tup in product(consts, repeat=len(qvars)):
            sub = dict(zip(qvars, tup))
            instances.append({"@question": substitute(q, sub)})
    print(f"# gkmc threshold sampling: {os.path.basename(args.input)}  "
          f"(n={args.trials}, seed={seed})")
    shown = 0
    for inst in instances:
        qatom, qsign = _query_atom_sign(inst)
        res = sr.evaluate(pool, confs, qatom, qsign, args.trials, seed)
        qname = (f"{qatom[0]}({','.join(map(str, qatom[1]))})"
                 if qatom[1] else qatom[0])
        if qsign == "-":
            qname = "-" + qname
        if res.get("not_scored"):
            print(f"query {qname}: not scored: {res['not_scored']}")
            shown += 1
            continue
        if qvars and all(res[f] < 0.0005 for f in MASS_FIELDS[:3]):
            continue    # an instance with no evidence either way: skip
        print(f"query {qname}:")
        for f in MASS_FIELDS:
            print(f"  {f:16s} {res[f]:.4f}")
        if res.get("priority_note"):
            print(f"  note: {res['priority_note']}")
        shown += 1
    if not shown:
        print("no instance has evidence on any side")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input")
    ap.add_argument("-n", "--trials", type=int, default=10000)
    ap.add_argument("--seed", default="0")
    ap.add_argument("--draws", dest="coins", choices=["per-instance", "shared"],
                    default="per-instance")
    ap.add_argument("--semantics",
                    choices=["subtract", "provable", "gkdefault", "threshold"],
                    default="subtract",
                    help="subtract (default): per answer, P(a provable) minus "
                         "P(the negated answer provable), matching gk's "
                         "reported confidence; provable: the positive frequency "
                         "only; gkdefault: the fraction of trials where a plain "
                         "default gk run accepts the closed answer; threshold: "
                         "the four masses support_for/against/conflict/ignorance "
                         "for a ground query, from a separate method that runs "
                         "no gk subprocess")
    ap.add_argument("--check", default=None,
                    help="threshold sampling only: a directory of knowledge bases "
                         "each with an expected.tsv; batch-check every one and "
                         "print OK/FAIL/NOT-SCORED per example instead of a single run")
    ap.add_argument("--classify", action="store_true")
    ap.add_argument("--gk",
                    default=os.path.join(
                        os.path.dirname(os.path.abspath(__file__)),
                        "..", "bin", "gk"))
    ap.add_argument("--gk-args", default="", help="extra args for world runs")
    ap.add_argument("--gk-timeout", type=float, default=10.0)
    ap.add_argument("--jobs", type=int, default=os.cpu_count() or 4)
    ap.add_argument("--max-ground", type=int, default=100000)
    ap.add_argument("--keep-worlds", default=None)
    ap.add_argument("--json", default=None, help="write machine-readable results here")
    args = ap.parse_args()
    args.gk_args = args.gk_args.split() if args.gk_args else []

    if args.semantics == "threshold":
        return run_threshold(args)

    stmts = load_original(args.input)
    clausified = clausify(args.gk, args.input)
    pool, questions, warnings = ground_pool(clausified, stmts, args.max_ground)
    confs = [c for _, c, _ in stmts]
    neg_questions = [negate_question(q) for q in questions] if args.classify else None

    n_uncertain = len({o for o, _ in pool if confs[o] < 1.0})
    print(f"# gkmc: {os.path.basename(args.input)}")
    print(f"ground pool: {len(pool)} clauses from {len(stmts)} statements "
          f"({n_uncertain} uncertain origins); draws: {args.coins}; "
          f"trials: {args.trials}; seed: {args.seed}")
    for w in warnings:
        print(f"WARNING: {w}")

    tmpdir = args.keep_worlds or tempfile.mkdtemp(prefix="gkmc_")
    if args.keep_worlds:
        os.makedirs(tmpdir, exist_ok=True)
    runner = Runner(args, pool, confs, questions, neg_questions, tmpdir)

    counts = {}
    pos_sets = {}   # valid trial -> set of proved answer keys (for pairing)
    cls = {"A_only": 0, "notA_only": 0, "both": 0, "neither": 0}
    timeouts = 0
    with ThreadPoolExecutor(max_workers=args.jobs) as ex:
        for t, (pos, neg) in enumerate(ex.map(runner.trial,
                                              range(args.trials))):
            if pos is None or (args.classify and neg is None):
                timeouts += 1
                continue
            pos_sets[t] = set(pos)
            for k in pos_sets[t]:
                counts[k] = counts.get(k, 0) + 1
            if args.classify:
                a, na = bool(pos), bool(neg)
                cls["A_only" if a and not na else
                    "notA_only" if na and not a else
                    "both" if a and na else "neither"] += 1

    n_ok = args.trials - timeouts

    # per-answer pairing pass (subtract semantics): re-decide the SAME worlds
    # against each discovered answer's closed positive and negated instances;
    # the paired cells give P(a) - P(not-a) = P(a-only) - P(nota-only), gk's
    # pos-neg functional. When the question is already closed, phase 1 ran
    # exactly the positive instance and its verdicts are reused.
    pairs = {}
    q_closed = bool(questions) and not question_var_order(
        questions[0].get("@question", []))
    if args.semantics == "subtract" and counts:
        if len(questions) != 1:
            print("WARNING: subtraction needs exactly one question; "
                  "reporting provability only")
        else:
            trials_v = sorted(pos_sets)
            for ki, k in enumerate(sorted(counts, key=lambda k: -counts[k])):
                try:
                    posq, negq = question_instances(questions[0], k)
                except ValueError as e:
                    print(f"WARNING: answer '{k}': {e}; provability only")
                    continue

                def decide(t, pq=posq, nq=negq, i=ki, key=k):
                    if q_closed:
                        p = key in pos_sets[t]
                    else:
                        rp = runner.run_question(t, [pq], f"p{i}")
                        if rp is None:
                            return None
                        p = bool(rp)
                    rn = runner.run_question(t, [nq], f"s{i}")
                    if rn is None:
                        return None
                    return p, bool(rn)

                cells = {"pos_only": 0, "neg_only": 0, "both": 0, "neither": 0}
                nk = 0
                with ThreadPoolExecutor(max_workers=args.jobs) as ex:
                    for res in ex.map(decide, trials_v):
                        if res is None:
                            continue
                        p, ng = res
                        cells["both" if p and ng else
                              "pos_only" if p else
                              "neg_only" if ng else "neither"] += 1
                        nk += 1
                pairs[k] = (cells, nk)

    # gkdefault pass: re-decide the same worlds with a PLAIN DEFAULT gk run on
    # each discovered answer's closed positive instance. The world verdict is
    # gk's own: an answer refuted in the same world is rejected (pos-neg = 0
    # below the confidence limit), so the frequency estimates P(a provable and
    # not refuted) = the A-only functional. Closed instances per answer avoid
    # both the open-question artifact in contradictory worlds and gk default's
    # legacy 10-total-proofs stop in multi-answer worlds; discovery via the
    # provability phase is complete since accepted implies provable.
    gkdef = {}
    if args.semantics == "gkdefault" and counts:
        if len(questions) != 1:
            print("WARNING: gkdefault needs exactly one question; "
                  "reporting provability only")
        else:
            trials_v = sorted(pos_sets)
            for ki, k in enumerate(sorted(counts, key=lambda k: -counts[k])):
                try:
                    posq, _ = question_instances(questions[0], k)
                except ValueError as e:
                    print(f"WARNING: answer '{k}': {e}; provability only")
                    continue
                acc, nk = 0, 0
                with ThreadPoolExecutor(max_workers=args.jobs) as ex:
                    for res in ex.map(
                            lambda t, q=posq, i=ki:
                                runner.run_question(t, [q], f"d{i}",
                                                    gk_default=True),
                            trials_v):
                        if res is None:
                            continue
                        nk += 1
                        if res:
                            acc += 1
                gkdef[k] = (acc, nk)

    own_new = gk_own_confidences(args.gk, args.input, [])

    print(f"\nvalid trials: {n_ok} (timeouts/errors: {timeouts})\n")
    if gkdef:
        print("| answer | MC gk-default | 95% CI | gk exact |")
        print("|---|---|---|---|")
        for k in sorted(counts, key=lambda k: -counts[k]):
            if k in gkdef:
                acc, nk = gkdef[k]
                lo, hi = wilson(acc, nk)
                print(f"| {k} | {acc/max(1,nk):.4f} | [{lo:.4f}, {hi:.4f}] "
                      f"| {own_new.get(k, '')} |")
            else:
                lo, hi = wilson(counts[k], n_ok)
                print(f"| {k} | {counts[k]/n_ok:.4f} (provability) "
                      f"| [{lo:.4f}, {hi:.4f}] "
                      f"| {own_new.get(k, '')} |")
        for k in sorted(set(own_new) - set(counts)):
            print(f"| {k} | 0.0000 | [0.0000, {wilson(0, n_ok)[1]:.4f}] "
                  f"| {own_new.get(k, '')} |")
    elif pairs:
        print("| answer | MC pos | MC neg | MC pos-neg | 95% CI "
              "| gk exact |")
        print("|---|---|---|---|---|---|")
        for k in sorted(counts, key=lambda k: -counts[k]):
            if k in pairs:
                cells, nk = pairs[k]
                pp = (cells["pos_only"] + cells["both"]) / max(1, nk)
                pn = (cells["neg_only"] + cells["both"]) / max(1, nk)
                diff, (lo, hi) = paired_diff_ci(cells["pos_only"],
                                                cells["neg_only"], nk)
                print(f"| {k} | {pp:.4f} | {pn:.4f} | {diff:.4f} "
                      f"| [{lo:.4f}, {hi:.4f}] "
                      f"| {own_new.get(k, '')} |")
            else:
                lo, hi = wilson(counts[k], n_ok)
                print(f"| {k} | {counts[k]/n_ok:.4f} |  | (provability) "
                      f"| [{lo:.4f}, {hi:.4f}] "
                      f"| {own_new.get(k, '')} |")
        for k in sorted(set(own_new) - set(counts)):
            print(f"| {k} | 0.0000 |  |  | [0.0000, {wilson(0, n_ok)[1]:.4f}] "
                  f"| {own_new.get(k, '')} |")
    else:
        print("| answer | MC freq | 95% CI | gk exact |")
        print("|---|---|---|---|")
        for k in sorted(counts, key=lambda k: -counts[k]):
            lo, hi = wilson(counts[k], n_ok)
            print(f"| {k} | {counts[k]/n_ok:.4f} | [{lo:.4f}, {hi:.4f}] "
                  f"| {own_new.get(k, '')} |")
        for k in sorted(set(own_new) - set(counts)):
            print(f"| {k} | 0.0000 | [0.0000, {wilson(0, n_ok)[1]:.4f}] "
                  f"| {own_new.get(k, '')} |")

    result = {"input": args.input, "trials": args.trials, "valid": n_ok,
              "seed": args.seed, "draws": args.coins,
              "semantics": args.semantics,
              "counts": counts, "gk_exact": own_new}
    if pairs:
        result["pairs"] = {k: {"cells": c, "n": nk}
                           for k, (c, nk) in pairs.items()}
        result["subtract"] = {
            k: paired_diff_ci(c["pos_only"], c["neg_only"], nk)[0]
            for k, (c, nk) in pairs.items()}
    if gkdef:
        result["gkdefault"] = {k: acc / max(1, nk)
                               for k, (acc, nk) in gkdef.items()}
        result["gkdefault_n"] = {k: nk for k, (acc, nk) in gkdef.items()}
    if args.classify:
        print("\ntrial classification (question provable = A, negated = notA):\n")
        print("| A only | notA only | both | neither |")
        print("|---|---|---|---|")
        print("| " + " | ".join(f"{cls[k]/n_ok:.4f}" for k in
                                ("A_only", "notA_only", "both", "neither")) + " |")
        pa = (cls["A_only"] + cls["both"]) / n_ok
        pna = (cls["notA_only"] + cls["both"]) / n_ok
        print(f"\nP(A provable) = {pa:.4f}   P(notA provable) = {pna:.4f}")
        print(f"P(A and not refuted) = {cls['A_only']/n_ok:.4f}   "
              f"P(A | not refuted) = "
              f"{cls['A_only']/max(1e-12, cls['A_only']+cls['neither']):.4f}   "
              f"subtraction pos-neg = {pa-pna:.4f}")
        result["classification"] = cls
    if args.json:
        with open(args.json, "w") as f:
            json.dump(result, f, indent=1)
        print(f"\n(json written to {args.json})")

if __name__ == "__main__":
    main()
