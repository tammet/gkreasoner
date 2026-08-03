#!/usr/bin/env python3
"""
threshold_worlds.py -- shared-threshold sampling for the four-component
report.

Estimates the shared-threshold reference construction (support_for,
support_against, conflict, ignorance) for a query by random sampling, with
no gk subprocess. It estimates the reference model on the restricted
fragment described below; it does not estimate every GK report.

Each ground atom that has evidence draws an acceptance threshold U in
[0,1], independent across atoms. The evidence for the atom is pooled
(noisy-or) into one strength a, the evidence against it into one strength
b. The same threshold U decides both sides:

    supported for      iff  b < U <= a      (only the for-side clears U)
    supported against  iff  a < U <= b      (only the against-side clears U)
    conflict           iff  U <= min(a, b)  (both sides clear U)
    ignorance          iff  U >  max(a, b)  (neither side clears U)

Averaging these outcomes over many draws gives the four components. A
shared atom has one threshold, so evidence that passes through the same
atom is correlated; this reproduces the treatment of shared and contested
support.

Each atom draws a second, independent threshold for the local combination
rules of defaults and opposing evidence: a default opposed by ordinary
evidence takes the exclusive split, two equal-rank defaults block each
other symmetrically, and unequal ranks take the strict-priority override on
the shared threshold.

Rules and exception conditions: a ground rule instance (a directed
application) holds in a draw iff every body atom is usable in the required
polarity and no exception condition on another atom fires. A blocker
["$block", s, B] fires iff atom B is usable on its for-side; ["$block", s,
["$not", B]] fires iff atom B is usable on its against-side. Atoms are
evaluated in dependency order; a cyclic group is evaluated by least-fixpoint
iteration per draw.

Unsupported cases are reported as not scored rather than guessed: a
dependency cycle through an exception condition away from the query, a
cycle through a contested atom, and a rank-restricted exception check whose
content is protected at a strictly weaker rank.

Public API:
  evaluate(pool, confs, query_atom, query_sign, trials, seed) -> dict with
    support_for / support_against / conflict / ignorance (and a
    'not_scored' reason for an unsupported case).

Input contract: original clauses with the head as the LAST ordinary
literal (facts are their own head), or the implication form
[antecedent(s), "=>", consequent], whose consequent is the head; a clause
with more than one positive literal is rejected as ambiguous. Constants only (no function terms); the
query atom of evaluate() must be ground.
"""
import random
from itertools import product

import gkmc      # reuse clause_vars / clause_consts / substitute


# --------------------------------------------------------------- literal parsing

def _split_sign(pred):
    if isinstance(pred, str) and pred.startswith("-"):
        return pred[1:], "-"
    return pred, "+"


def parse_literal(lit):
    """Return one of:
       ("block", priority:int, (batom, bsign))   for a $block marker
       ("lit",   sign:str, atom_key)             for an ordinary literal
    atom_key = (pred, args_tuple); a bare string is a 0-ary atom."""
    if isinstance(lit, str):
        if lit.lstrip("-").startswith("$"):
            raise SystemExit(f"built-in predicate not supported by threshold sampling: {lit}")
        pred, sign = _split_sign(lit)
        return ("lit", sign, (pred, ()))
    if isinstance(lit, list) and lit and lit[0] == "$block":
        strength = lit[1]
        target = lit[2]
        if isinstance(target, list) and target and target[0] == "$not":
            batom = _atom_of(target[1])
            return ("block", _priority(strength), (batom, "-"))
        batom = _atom_of(target)
        return ("block", _priority(strength), (batom, "+"))
    if not (isinstance(lit, list) and lit and isinstance(lit[0], str)):
        raise SystemExit(f"non-clausal formula not supported by threshold sampling: {lit!r}")
    if lit[0].lstrip("-").startswith("$"):
        raise SystemExit(
            f"built-in predicate not supported by threshold sampling: {lit[0]}")
    if any(isinstance(arg, list) for arg in lit[1:]):
        raise SystemExit(f"function terms not supported in v1: {lit!r}")
    return ("lit",) + _lit_sign_atom(lit)


def _priority(strength):
    if isinstance(strength, int):
        return strength
    raise SystemExit(
        f"unsupported blocker priority form {strength!r}: only plain "
        f"integer priorities are supported by threshold sampling")


def _lit_sign_atom(lit):
    pred, sign = _split_sign(lit[0])
    return (sign, (pred, tuple(lit[1:])))


def _atom_of(lit):
    if isinstance(lit, str):
        pred, _ = _split_sign(lit)
        return (pred, ())
    pred, _ = _split_sign(lit[0])
    return (pred, tuple(lit[1:]))


def complement(sign):
    return "-" if sign == "+" else "+"



def _negate_atom(a):
    if isinstance(a, str) and not a.startswith("$"):
        return a[1:] if a.startswith("-") else "-" + a
    if isinstance(a, list) and a and isinstance(a[0], str):
        p = a[0]
        return ([p[1:]] if p.startswith("-") else ["-" + p]) + a[1:]
    raise SystemExit(f"unsupported antecedent in an implication: {a!r}")


def _normalize(logic):
    """Convert the implication form [antecedent(s), "=>", consequent] into a
    head-last clause: the consequent is the head, each antecedent atom is
    negated into the body. Clause-form input is returned unchanged."""
    if not (isinstance(logic, list) and "=>" in logic):
        return logic
    i = logic.index("=>")
    left, right = logic[:i], logic[i + 1:]
    if len(right) != 1 or "=>" in right:
        raise SystemExit(f"unsupported implication form: {logic!r}")
    if (len(left) == 1 and isinstance(left[0], list) and left[0]
            and isinstance(left[0][0], list)):
        left = left[0]          # a conjunction given as a list of atoms
    return [_negate_atom(a) for a in left] + [right[0]]


# --------------------------------------------------------------- model building

class DirectedApplication:
    __slots__ = ("head_atom", "head_sign", "strength", "body", "blockers",
                 "mutual", "orig", "paired_main")

    def __init__(self, head_atom, head_sign, strength, body, blockers, mutual,
                 orig):
        self.head_atom = head_atom      # atom_key it concludes
        self.head_sign = head_sign      # "+" -> pro pool, "-" -> con pool
        self.strength = strength
        self.body = body                # [(atom_key, required_sign)]
        self.blockers = blockers        # distinct-atom [(atom_key, block_sign, prio)]
        self.mutual = mutual            # [(prio, block_sign)] mutual (same-atom) blocks
        self.orig = orig
        self.paired_main = False        # set if this is a consumed paired exception


def ground_original(stmts, max_ground=None):
    """Ground the ORIGINAL @logic clauses over the named constants,
    preserving literal order: the input contract puts the head last, and gk
    -clausify reorders literals, so the sampler grounds the originals
    itself. Stops with an error when the pool exceeds max_ground.
    Returns (pool, confs, questions)."""
    consts = set()
    clauses = []
    questions = []
    for is_q, conf, item in stmts:
        logic = item.get("@question") if is_q else item.get("@logic")
        if is_q:
            questions.append({"@question": logic})
            # question constants join the Herbrand pool: a KB of purely
            # non-ground clauses (0.8::bird(X)) must still ground onto the
            # queried individual bird(a)
            gkmc.clause_consts(_as_clause(logic), consts)
            continue
        logic = _normalize(logic)
        _validate_clause(logic)
        clauses.append((len(clauses), conf, logic))
        gkmc.clause_consts(_as_clause(logic), consts)
    consts = sorted(consts, key=str) or ["c0"]
    confs = [conf for _idx, conf, _logic in clauses]   # indexed by clause idx
    pool = []
    for idx, conf, logic in clauses:
        cl = _as_clause(logic)
        vs = gkmc.clause_vars(cl)
        seen = set()
        for tup in product(consts, repeat=len(vs)):
            g = gkmc.substitute(logic, dict(zip(vs, tup)))
            key = repr(g)
            if key in seen:
                continue
            seen.add(key)
            pool.append((idx, g))
            if max_ground is not None and len(pool) > max_ground:
                raise SystemExit(f"ground pool exceeds --max-ground "
                                 f"{max_ground}; refusing to truncate")
    return pool, confs, questions


def _validate_clause(logic):
    """Reject syntax that the small directional evaluator does not implement."""
    if isinstance(logic, str):
        parse_literal(logic)
        return
    if not isinstance(logic, list) or not logic:
        raise SystemExit(f"unsupported logic item in threshold sampling: {logic!r}")
    if isinstance(logic[0], str):
        parse_literal(logic)
        return
    ordinary = []
    for item in logic:
        if not isinstance(item, list):
            raise SystemExit(
                f"non-clausal formula not supported by threshold sampling: {logic!r}")
        if item and item[0] == "$block":
            if isinstance(item[1], list):
                raise SystemExit(
                    "taxonomy-valued blocker strengths are not supported by "
                    "threshold sampling")
            parse_literal(item)
        else:
            parse_literal(item)
            ordinary.append(item)
    positive = [item for item in ordinary
                if isinstance(item[0], str) and not item[0].startswith("-")]
    if len(positive) > 1:
        raise SystemExit(
            "threshold sampling needs a directional clause with an unambiguous "
            f"head; found several positive literals in {logic!r}")


def _as_clause(logic):
    """gkmc's walk helpers expect a list of literals; wrap a single-literal
    fact. Implication-form input is converted first."""
    logic = _normalize(logic)
    if isinstance(logic, list) and logic and isinstance(logic[0], str):
        return [logic]
    return logic


def clause_literals(raw):
    """Split a ground @logic value into (ordinary literals, block markers).
    A single-literal fact is `["-bird","a"]` (first element a predicate string);
    a multi-literal clause is a list of literal-lists (possibly with $block
    markers). The head is the last ordinary literal (the input contract of
    this sampler: `[-body1, ..., -bodyk, head]`); preceding ordinary
    literals are the body, each contributing (atom, complement sign)."""
    if isinstance(raw, list) and raw and isinstance(raw[0], str) \
            and raw[0] not in ("$block", "$not"):
        return [("lit",) + _lit_sign_atom(raw)], []
    lits, blocks = [], []
    for item in raw:
        kind = parse_literal(item)
        if kind[0] == "block":
            blocks.append((kind[1], kind[2]))       # (priority, (batom, bsign))
        else:
            lits.append(kind)                        # ("lit", sign, atom)
    return lits, blocks


def build_applications(pool, confs, query_atom, query_sign):
    """From the ground pool build the directed applications reachable from
    the query by backward chaining. The head of each clause is its last
    ordinary literal (no contrapositives); indexing by head atom collects
    BOTH polarities of a contested atom (a `¬bird` fact and a `bird:-wings`
    rule both index under atom bird) without generating spurious reverse
    rules. Returns (apps, atoms)."""
    by_head_atom = {}
    for orig, raw in pool:
        lits, blocks = clause_literals(raw)
        if not lits:
            continue
        _tag, hsign, hatom = lits[-1]
        body = [(a, complement(s)) for (_t, s, a) in lits[:-1]]
        dist_blk, mutual = [], []
        for (prio, (batom, bsign)) in blocks:
            if batom == hatom:
                mutual.append((prio, bsign))
            else:
                dist_blk.append((batom, bsign, prio))
        by_head_atom.setdefault(hatom, []).append(
            (hsign, confs[orig], body, dist_blk, mutual, orig))

    applications = []
    frontier = [query_atom]
    atoms = set()
    while frontier:
        atom = frontier.pop()
        if atom in atoms:
            continue
        atoms.add(atom)
        for (hsign, strength, body, dist_blk, mutual, orig) in \
                by_head_atom.get(atom, []):
            applications.append(
                DirectedApplication(atom, hsign, strength, body, dist_blk, mutual, orig))
            for (ba, _bs) in body:
                frontier.append(ba)
            for (batom, _bsign, _p) in dist_blk:
                frontier.append(batom)
    _mark_pairs(applications)
    return applications, atoms


def _mark_pairs(applications):
    """A directed application is a paired exception of a main rule when:
    same head atom, opposite head sign, and the main rule carries a
    distinct-atom blocker whose atom occurs in the exception's body
    (syntactic detection)."""
    by_atom = {}
    for t in applications:
        by_atom.setdefault(t.head_atom, []).append(t)
    for atom, ts in by_atom.items():
        for main in ts:
            if not main.blockers:
                continue
            blk_atoms = {b[0] for b in main.blockers}
            for exc in ts:
                if exc.head_sign == main.head_sign:
                    continue
                body_atoms = {b[0] for b in exc.body}
                if blk_atoms & body_atoms:
                    exc.paired_main = True


# --------------------------------------------------------------- world evaluation

def _has_rank_restricted_blocker(applications, by_head):
    """Detect a rank-restricted exception check: a distinct-atom blocker at
    rank r whose content atom's support flows through a rule self-protected
    at a rank strictly below r. GK's search refuses that support inside the
    check; this model carries no enclosing check rank and would let it
    block, so the case must be reported as unsupported rather than
    mis-scored. Returns (content_atom, check_rank, protect_rank) or None."""
    for t in applications:
        for (batom, bsign, prio) in t.blockers:
            for s_t in by_head.get(batom, []):
                if s_t.head_sign != bsign or not s_t.mutual:
                    continue
                for (mprio, _msign) in s_t.mutual:
                    if 0 < mprio < prio:
                        return (batom, prio, mprio)
    return None


def evaluate(pool, confs, query_atom, query_sign, trials, seed):
    applications, atoms = build_applications(pool, confs, query_atom, query_sign)
    order = _topo_order(applications, atoms)
    plan = None
    if order is None:
        plan, why = _scc_plan(applications, atoms, query_atom)
        if plan is None:
            return {"support_for": None, "support_against": None,
                    "conflict": None, "ignorance": None,
                    "not_scored": f"{why} (cycle through a blocker or contested atom); not scored"}
    by_head = {}
    for t in applications:
        by_head.setdefault(t.head_atom, []).append(t)

    # Unequal mutual ranks are scored by the strict-priority override. The
    # rank-restricted DISTINCT-atom check is not modelled: this sampler
    # carries an application's own mutual rank, not a guard evaluated under
    # an enclosing check rank, so it would let a lower-rank-protected
    # support fire such a check and silently return the admissible-exception
    # value for the inadmissible case. It reports the case as unsupported
    # instead.
    rank_note = _has_rank_restricted_blocker(applications, by_head)
    if rank_note:
        return {"support_for": None, "support_against": None,
                "conflict": None, "ignorance": None,
                "not_scored": (
                    f"blocker check at rank {rank_note[1]} targets "
                    f"{rank_note[0]}, whose support is protected at the "
                    f"strictly weaker rank {rank_note[2]}: gk's search-side "
                    f"rank restriction excludes that support inside the check, "
                    f"and this model does not carry the enclosing check "
                    f"priority; not scored")}
    tally = {"for": 0, "against": 0, "conflict": 0, "ignorance": 0}
    rng = random.Random(seed)
    atoms_ordered = sorted(atoms, key=repr)   # canonical draw order: the seed
    # must fully determine each atom's U regardless of set hash randomization
    # (PYTHONHASHSEED) across processes -- else the table is not reproducible.
    for _ in range(trials):
        u = {a: (rng.random(), rng.random()) for a in atoms_ordered}
        state = {}     # atom -> (pro_usable, con_usable)
        if order is not None:
            for atom in order:
                state[atom] = _eval_atom(atom, by_head.get(atom, []), state, u)
        else:
            for unit in plan:
                if len(unit) == 1:
                    state[unit[0]] = _eval_atom(unit[0],
                                                by_head.get(unit[0], []),
                                                state, u)
                elif unit[0] == "credulous":
                    _eval_scc_credulous(unit[1:], query_atom, by_head,
                                        state, u)
                else:
                    _eval_scc_fixpoint(unit, by_head, state, u)
        pro_u, con_u, cflt = _classify(query_atom, query_sign,
                                        by_head.get(query_atom, []), state, u)
        if query_sign == "-":
            pro_u, con_u = con_u, pro_u
        if pro_u:
            tally["for"] += 1
        elif con_u:
            tally["against"] += 1
        elif cflt:
            tally["conflict"] += 1
        else:
            tally["ignorance"] += 1
    out = {k2: tally[k1] / trials for k1, k2 in
           (("for", "support_for"), ("against", "support_against"),
            ("conflict", "conflict"), ("ignorance", "ignorance"))}
    return out


def _present(t, state):
    for (batom, bsign) in t.body:
        st = state.get(batom, (False, False))
        ok = st[0] if bsign == "+" else st[1]
        if not ok:
            return False
    for (batom, bsign, _prio) in t.blockers:
        st = state.get(batom, (False, False))
        fires = st[0] if bsign == "+" else st[1]
        if fires:
            return False
    return True


def _is_cycle_member(t):
    """A RECIPROCAL priority-zero default: its mutual block's content is the
    COMPLEMENT of its own head (`p :- ..., unless(-p)`) and carries no priority
    claim.  Priority zero means INCOMPARABLE, so such a block cannot be
    resolved by rank; the two blocker edges of a same-atom pair are the
    internal edges of a cycle.  A block whose content EQUALS the head
    (`p :- ..., unless(p)`) is the self-defeating form, not this."""
    return any(prio < 1 and bsign == complement(t.head_sign)
               for (prio, bsign) in t.mutual)


def _pools(head_atom, ts, state):
    """Return (a, b, a_cyc, b_cyc, a_ext, b_ext, filled, rank_pro, rank_con):
    pooled pro/con strengths of the PRESENT directed applications, the same
    pools split into reciprocal priority-zero CYCLE members and EXTERNAL
    evidence, whether a paired-exception residual fill applies, and each
    side's rank. A side's rank is the maximum mutual-block rank of its
    present applications when EVERY present application on that side
    carries one (a self-protected default); it is 0 when the side has any
    present unranked application -- mirroring GK's rank convention."""
    pro, con = [], []
    pro_cyc, con_cyc, pro_ext, con_ext = [], [], [], []
    filled = False
    rank_pro = rank_con = -1          # -1: no present application
    main_pro_blocked = any(t.head_sign == "+" and (t.blockers) and not _present(t, state)
                           for t in ts)
    for t in ts:
        if not _present(t, state):
            continue
        trank = max((prio for (prio, _s) in t.mutual), default=0)
        cyc = _is_cycle_member(t)
        if t.head_sign == "+":
            pro.append(t.strength)
            (pro_cyc if cyc else pro_ext).append(t.strength)
            rank_pro = (0 if (trank < 1 or rank_pro == 0)
                        else max(rank_pro, trank))
            if trank < 1:
                rank_pro = 0
        else:
            con.append(t.strength)
            (con_cyc if cyc else con_ext).append(t.strength)
            rank_con = (0 if (trank < 1 or rank_con == 0)
                        else max(rank_con, trank))
            if trank < 1:
                rank_con = 0
            if t.paired_main and main_pro_blocked:
                filled = True

    def pool(ws):
        r = 1.0
        for w in ws:
            r *= (1 - w)
        return 1 - r

    return (pool(pro), pool(con), pool(pro_cyc), pool(con_cyc),
            pool(pro_ext), pool(con_ext), filled, rank_pro, rank_con)


def _net(a, b, u2, filled, rank_pro, rank_con,
         a_cyc=0.0, b_cyc=0.0, a_ext=None, b_ext=None):
    """(pro_usable, con_usable, conflict) for one atom in one world.
    u2 = (u_pro, u_con): two independent uniforms per atom. Ordinary
    opposition uses the SHARED threshold u_pro for both sides; the default
    cases use both thresholds:

      both sides self-protected, unequal ranks -> the strict-priority
        override on the shared threshold (the higher rank takes the
        overlap, the lower keeps its excess);
      both sides self-protected, equal ranks   -> symmetric mutual
        blocking: each side fires on its own threshold and survives only
        if the other missed;
      one side self-protected                  -> the exclusive split: the
        plain side fires on its own threshold, the protected side survives
        only off the plain side's mass; conflict 0 (exclusive regions).

    The independent second threshold is what makes for = a(1-b) a product;
    a single shared threshold cannot express it."""
    ul, ur = u2
    lo = min(a, b)
    gated_pro = (rank_pro is not None and rank_pro >= 1)
    gated_con = (rank_con is not None and rank_con >= 1)
    if a > 0.0 and b > 0.0 and gated_pro and gated_con and rank_pro != rank_con:
        # strict-priority override on the shared threshold: the
        # strictly-higher side takes the region U <= min(a,b); the lower
        # keeps its excess.
        if rank_pro > rank_con:
            pro = ul <= a
            con = a < ul <= b
            return pro, con, False
        con = ul <= b
        pro = b < ul <= a
        return pro, con, False
    if a > 0.0 and b > 0.0 and gated_pro and gated_con:
        # equal ranks: symmetric mutual blocking; both-fire and
        # neither-fire regions are ignorance (the certain limit is the
        # Nixon case)
        fp = ul <= a
        fc = ur <= b
        return (fp and not fc), (fc and not fp), False
    if a > 0.0 and b > 0.0 and gated_pro:
        # one-sided: the con evidence fires the pro default's contrary
        # exception condition
        fc = ur <= b
        pro = (ul <= a) and not fc
        return pro, fc, False
    if a > 0.0 and b > 0.0 and gated_con:
        # the mirror case: the default is on the con side
        fp = ul <= a
        con = (ur <= b) and not fp
        return fp, con, False
    if a_cyc > 0.0 or b_cyc > 0.0:
        # ---- the priority-zero layer --------------------------------------
        # Priority zero is INCOMPARABLE, not the lowest rank, so a
        # reciprocal rank-0 pair cannot be resolved by the ranked branches
        # above.  The internal edges of the cycle are dependencies, not
        # undercutting attacks: the cycle pools meet by ordinary opposition
        # on their own threshold.  Evidence from OUTSIDE the cycle keeps
        # undercutting -- it suppresses the cycle side it attacks exactly
        # where it is itself usable -- so a lone rank-0 default against an
        # ordinary contrary fact keeps the exclusive split a(1-b) / b / 0
        # instead of becoming an opposition.
        ae = a if a_ext is None else a_ext
        be = b if b_ext is None else b_ext
        ext_pro = (be < ul <= ae)
        ext_con = (ae < ul <= be)
        ext_cfl = (ul <= min(ae, be))
        cyc_pro = (b_cyc < ur <= a_cyc)
        cyc_con = (a_cyc < ur <= b_cyc)
        cyc_cfl = (ur <= min(a_cyc, b_cyc))
        pro = ext_pro or (cyc_pro and not ext_con)
        con = ext_con or (cyc_con and not ext_pro)
        return pro, con, ((not pro and not con) and (ext_cfl or cyc_cfl))
    pro = (b < ul <= a)
    con = (a < ul <= b)
    conflict = (ul <= lo)
    if filled and ul > b and not pro:
        pro = True                      # paired-exception residual fill
    return pro, con, (conflict and not pro and not con)


def _eval_atom(atom, ts, state, u):
    a, b, ac, bc, ae, be, filled, rp, rc = _pools(atom, ts, state)
    pro, con, _ = _net(a, b, u[atom], filled, rp, rc, ac, bc, ae, be)
    return (pro, con)


def _classify(atom, sign, ts, state, u):
    a, b, ac, bc, ae, be, filled, rp, rc = _pools(atom, ts, state)
    return _net(a, b, u[atom], filled, rp, rc, ac, bc, ae, be)


def _atom_deps(applications, atoms):
    """The static atom dependency graph: head atom -> {body atoms,
    distinct-atom blocker atoms}. Mutual (same-atom) blocks are self-loops
    and ignored."""
    deps = {a: set() for a in atoms}
    for t in applications:
        for (ba, _s) in t.body:
            if ba != t.head_atom:
                deps[t.head_atom].add(ba)
        for (ba, _s, _p) in t.blockers:
            if ba != t.head_atom:
                deps[t.head_atom].add(ba)
    return deps


def _topo_order(applications, atoms):
    """Kahn topological sort over distinct-atom dependencies (body + distinct
    blockers). Returns None on a genuine cycle (the caller then falls back to
    the SCC/fixpoint plan of _scc_plan)."""
    deps = _atom_deps(applications, atoms)
    indeg = {a: len(deps[a]) for a in atoms}
    rdeps = {a: [] for a in atoms}
    for a in atoms:
        for d in deps[a]:
            rdeps[d].append(a)
    order = []
    ready = [a for a in atoms if indeg[a] == 0]
    while ready:
        a = ready.pop()
        order.append(a)
        for b in rdeps[a]:
            indeg[b] -= 1
            if indeg[b] == 0:
                ready.append(b)
    if len(order) != len(atoms):
        return None
    return order


# ------------------------------------------------- cyclic KBs: fixpoint evaluation

def _sccs(deps, atoms):
    """Iterative Tarjan over the dependency graph (edges head -> dependency).
    Returns the strongly connected components dependency-first: every SCC is
    emitted after every SCC it depends on, so evaluating in emission order sees
    all dependencies already settled."""
    index, low = {}, {}
    onstack, stack = set(), []
    sccs = []
    counter = [0]
    for root in atoms:
        if root in index:
            continue
        index[root] = low[root] = counter[0]
        counter[0] += 1
        stack.append(root)
        onstack.add(root)
        work = [(root, iter(deps[root]))]
        while work:
            v, it = work[-1]
            pushed = False
            for w in it:
                if w not in index:
                    index[w] = low[w] = counter[0]
                    counter[0] += 1
                    stack.append(w)
                    onstack.add(w)
                    work.append((w, iter(deps[w])))
                    pushed = True
                    break
                if w in onstack:
                    low[v] = min(low[v], index[w])
            if pushed:
                continue
            work.pop()
            if work:
                pv = work[-1][0]
                low[pv] = min(low[pv], low[v])
            if low[v] == index[v]:
                comp = []
                while True:
                    w = stack.pop()
                    onstack.discard(w)
                    comp.append(w)
                    if w == v:
                        break
                sccs.append(comp)
    return sccs


def _scc_plan(applications, atoms, query_atom=None):
    """Evaluation plan for a KB whose static atom graph is cyclic (equivalences,
    mutual rules): the SCC condensation in dependency-first order. Singleton SCCs
    evaluate exactly as on the acyclic path; each group of mutually dependent atoms is evaluated per
    world by least fixpoint (application presence = existence of a
    well-founded derivation in that world). The fixpoint is monotone --
    hence unique and equal to the derivability reading -- ONLY when the
    cycle contains no blocker and no contested atom. A cyclic group WITH an
    internal blocker edge is defined when it contains the QUERY atom: GK's
    blocker check voids an exception argument whose own validity depends on
    defeating the queried candidate, so the group evaluates credulously for
    the query -- the query atom first with in-group blockers voided, then
    the rest by fixpoint given it (plan entry ("credulous", atoms)). A
    blocker cycle NOT containing the query, or any cyclic group with a
    CONTESTED atom, stays unscored. Returns (plan, None) or (None, reason)."""
    deps = _atom_deps(applications, atoms)
    by_head = {}
    for t in applications:
        by_head.setdefault(t.head_atom, []).append(t)
    plan = []
    for comp in _sccs(deps, atoms):
        if len(comp) == 1:
            plan.append((comp[0],))
            continue
        cset = set(comp)
        for a in comp:
            if len({t.head_sign for t in by_head.get(a, [])}) > 1:
                return None, f"contested atom {a} inside a dependency cycle"
        has_blocker = False
        for t in applications:
            if t.head_atom in cset:
                for (ba, _bs, _p) in t.blockers:
                    if ba in cset:
                        has_blocker = True
        if has_blocker:
            if query_atom is not None and query_atom in cset:
                plan.append(("credulous",) + tuple(sorted(comp, key=repr)))
                continue
            return None, ("blocker cycle away from the query atom; the "
                          "credulous resolution is defined relative to the "
                          "query only")
        plan.append(tuple(sorted(comp, key=repr)))
    return plan, None


def _eval_scc_credulous(comp, query_atom, by_head, state, u):
    """A blocker cycle containing the query resolves credulously for the
    query. Phase 1 evaluates the query atom with every in-group blocker
    voided (GK voids the exception argument that depends on defeating the
    queried candidate); phase 2 fixpoints the remaining atoms normally
    given the committed query state, so the defeated side of the loop comes
    out blocked exactly as GK reports it."""
    cset = set(comp)
    for a in comp:
        state[a] = (False, False)
    ts = by_head.get(query_atom, [])
    stripped = []
    for t in ts:
        blk = [bl for bl in t.blockers if bl[0] not in cset]
        if len(blk) == len(t.blockers):
            stripped.append(t)
        else:
            t2 = DirectedApplication(t.head_atom, t.head_sign, t.strength,
                           t.body, blk, t.mutual, t.orig)
            t2.paired_main = t.paired_main
            stripped.append(t2)
    state[query_atom] = _eval_atom(query_atom, stripped, state, u)
    rest = [a for a in comp if a != query_atom]
    for _ in range(2 * len(comp) + 2):
        changed = False
        for a in rest:
            new = _eval_atom(a, by_head.get(a, []), state, u)
            if new != state[a]:
                state[a] = new
                changed = True
        if not changed:
            return
    raise AssertionError(f"credulous fixpoint failed to converge on {comp}")


def _eval_scc_fixpoint(comp, by_head, state, u):
    """Least-fixpoint evaluation of one monotone cyclic SCC in one world: start
    every atom non-usable, sweep _eval_atom until nothing changes. All atoms in
    the SCC are one-sided and no intra-SCC blocker exists (checked by _scc_plan),
    so pools only grow and usability only flips False -> True: at most 2*|SCC|
    flips can happen, and the sweep bound below cannot be reached before
    convergence. Atoms with support that needs bootstrapping through the cycle
    stay non-usable: the well-founded reading."""
    for a in comp:
        state[a] = (False, False)
    for _ in range(2 * len(comp) + 2):
        changed = False
        for a in comp:
            new = _eval_atom(a, by_head.get(a, []), state, u)
            if new != state[a]:
                state[a] = new
                changed = True
        if not changed:
            return
    raise AssertionError(f"fixpoint failed to converge on monotone SCC {comp}")
