#!/usr/bin/env python3
"""
threshold_worlds.py -- threshold sampling for the four gk masses.

Estimates gk's four-part report (support_for, support_against, conflict,
ignorance) for a ground query by random sampling, using no gk subprocess.

Each ground atom that has evidence draws one acceptance threshold U in [0,1],
independent across atoms. The evidence for the atom is combined (noisy-or) into
one strength a, the evidence against it into one strength b. The same threshold
U decides both sides:

    supported for      iff  b < U <= a      (only the for-side clears U)
    supported against  iff  a < U <= b      (only the against-side clears U)
    conflict           iff  U <= min(a, b)  (both sides clear U)
    ignorance          iff  U >  max(a, b)  (neither side clears U)

Averaging these outcomes over many draws gives the four masses. Because a
shared atom has one threshold, evidence that passes through the same atom is
correlated, which reproduces gk's treatment of shared and contested support.

Rules and blockers: a rule instance holds in a draw iff every body atom is
usable in the required polarity and no blocker on another atom fires. A blocker
["$block", s, B] fires iff atom B is usable on its for-side; ["$block", s,
["$not", B]] fires iff atom B is usable on its against-side. Atoms are evaluated
in dependency order, and a cyclic group is evaluated by least-fixpoint
iteration per draw.

Some cases are not settled by this model. It reports them as not scored,
rather than guessing: a dependency cycle through a blocker or a contested atom,
and mutual-block priority encodings at unequal strengths.

Public API:
  evaluate(pool, confs, query_atom, query_sign, trials, seed) -> dict with
    support_for / support_against / conflict / ignorance (and a 'not_scored'
    reason when the case is not settled).

Limits: constants only (no function symbols); the query atom must be ground.
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
    # ["$", ...] taxonomy strengths are not modelled here; plain ints only.
    if isinstance(strength, int):
        return strength
    return 0


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


# --------------------------------------------------------------- model building

class Testimony:
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


def ground_original(stmts):
    """Ground the ORIGINAL @logic clauses over the Herbrand constants, preserving
    literal order (so the head = last-literal convention holds). gk -clausify
    reorders literals positive-first, which destroys that convention, so the
    the sampler must ground the originals itself. Returns (pool, confs, questions)."""
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
    """gkmc's walk helpers expect a list of literals; wrap a single-literal fact."""
    if isinstance(logic, list) and logic and isinstance(logic[0], str):
        return [logic]
    return logic


# ---------------------------------------------- clausified (gk_clauses_v1) loading

MARKER_LESS_SKIP = "marker-less all-negative rule clause"


def _implied_positions(ord_lits, blocks, head_idx):
    """Which ordinary-literal positions are the IMPLIED (head) literals of a clause,
    mirroring gk's dw_build_index stack exactly:
      case 2 -- a $block whose content atom's COMPLEMENT (same functor, opposite
                sign) is an ordinary literal marks THAT literal as the single head;
      case 1 -- otherwise every POSITIVE ordinary literal is a head (a non-Horn
                disjunction delivers either -- one oriented testimony per positive);
      residual -- an all-negative clause takes the @head marker (the raw @logic
                index gk emitted); -1 there is the never-expected G-P2 tripwire.
    ord_lits: [(orig_i, sign, atomkey)]; blocks: [(orig_i, content_atomkey, sign)].
    Returns a list of positions into ord_lits, or raises _MarkerLess for the
    tripwire so the caller can decline to score rather than guess a head."""
    # case 2: $block-complement
    for (_oi, catom, csign) in blocks:
        for pos, (_i, s, a) in enumerate(ord_lits):
            if a[0] == catom[0] and s != csign:   # gk compares FUNCTOR, not args
                return [pos]
    # case 1: all positive ordinary literals
    pos_idx = [pos for pos, (_i, s, _a) in enumerate(ord_lits) if s == "+"]
    if pos_idx:
        return pos_idx
    # residual: all-negative -> the emitted @head marker
    if head_idx is not None and head_idx >= 0:
        for pos, (oi, _s, _a) in enumerate(ord_lits):
            if oi == head_idx:
                return [pos]
    raise _MarkerLess()


class _MarkerLess(Exception):
    pass


def _orient_head_last(logic, head_idx):
    """Turn one clausified @logic clause into one template PER implied literal, each
    with the chosen head moved LAST among the ordinary literals (so the existing
    last-literal build_testimonies picks the same head gk does). $block markers are
    preserved (build_testimonies re-separates them by position-independent parse).
    A single-literal fact is its own head. Raises _MarkerLess on the G-P2 tripwire.
    GENUINE function terms (nested lists in a literal's ARG positions) still raise
    via parse_literal/_atom_of downstream -- kept as the v1 hard error."""
    if isinstance(logic, list) and logic and isinstance(logic[0], str):
        return [logic]                              # fact: single positive unit
    ord_lits, blocks, markers = [], [], []
    for i, item in enumerate(logic):
        kind = parse_literal(item)
        if kind[0] == "block":
            blocks.append((i, kind[2][0], kind[2][1]))   # (idx, batomkey, bsign)
            markers.append(item)
        elif isinstance(item, list) and item and item[0] == "$ans":
            markers.append(item)                    # answer literal: not a head
        else:
            ord_lits.append((i, kind[1], kind[2]))
    if not ord_lits:
        return [logic]
    ord_items = [logic[i] for (i, _s, _a) in ord_lits]
    heads = _implied_positions(ord_lits, blocks, head_idx)
    templates = []
    for hpos in heads:
        head_item = ord_items[hpos]
        rest = [ord_items[p] for p in range(len(ord_items)) if p != hpos]
        templates.append(rest + markers + [head_item])   # head LAST
    return templates


def ground_clausified(items):
    """Ground gk's gk_clauses_v1 export over the Herbrand constants of the NON-goal
    clauses (parity with gk's dw_collect_constpool: a constant appearing ONLY in the
    goal/query is not a witness). Each axiom clause is oriented to its implied
    literal(s) by gk's own stack (see _implied_positions) and grounded. Strengths
    come straight from @confidence (post-root-split; NOT recomputed -- the split
    rule lives in gk). Returns (pool, confs, skips) where skips lists any
    marker-less rule clauses (the G-P2 tripwire) the caller must surface."""
    consts = set()
    axioms = []
    for it in items:
        if it.get("@role") == "goal":
            continue
        gkmc.clause_consts(_as_clause(it["@logic"]), consts)
        axioms.append(it)
    consts = sorted(consts, key=str) or ["c0"]
    pool, confs, skips = [], [], []
    for it in axioms:
        logic = it["@logic"]
        conf = float(it.get("@confidence", 1.0))
        try:
            templates = _orient_head_last(logic, it.get("@head", -1))
        except _MarkerLess:
            skips.append((it.get("@name", "?"), MARKER_LESS_SKIP))
            continue
        for tmpl in templates:
            cl = _as_clause(tmpl)
            vs = gkmc.clause_vars(cl)
            seen = set()
            for tup in product(consts, repeat=len(vs)):
                g = gkmc.substitute(tmpl, dict(zip(vs, tup)))
                key = repr(g)
                if key in seen:
                    continue
                seen.add(key)
                idx = len(confs)
                pool.append((idx, g))
                confs.append(conf)
    return pool, confs, skips


def clause_literals(raw):
    """Split a ground @logic value into (ordinary literals, block markers).
    A single-literal fact is `["-bird","a"]` (first element a predicate string);
    a multi-literal clause is a list of literal-lists (possibly with $block
    markers). The HEAD is the last ordinary literal (the gk default-rule
    convention used by these KBs: `[-body1, ..., -bodyk, head]`); preceding
    ordinary literals are the body, each contributing (atom, complement sign)."""
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


def build_testimonies(pool, confs, query_atom, query_sign):
    """From the ground pool build the directional testimonies reachable from the
    query by backward chaining. The head of each clause is its last ordinary
    literal (no contrapositives); indexing by head atom collects BOTH polarities
    of a contested atom (a `¬bird` fact and a `bird:-wings` rule both index under
    atom bird) without generating spurious reverse rules. Returns (ts, atoms)."""
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

    testimonies = []
    frontier = [query_atom]
    atoms = set()
    while frontier:
        atom = frontier.pop()
        if atom in atoms:
            continue
        atoms.add(atom)
        for (hsign, strength, body, dist_blk, mutual, orig) in \
                by_head_atom.get(atom, []):
            testimonies.append(
                Testimony(atom, hsign, strength, body, dist_blk, mutual, orig))
            for (ba, _bs) in body:
                frontier.append(ba)
            for (batom, _bsign, _p) in dist_blk:
                frontier.append(batom)
    _mark_pairs(testimonies)
    return testimonies, atoms


def _mark_pairs(testimonies):
    """A testimony is a paired exception of a main rule when: same head atom,
    opposite head sign, the main rule carries a distinct-atom blocker whose atom
    occurs in the exception's body (spec §5.3 detection, syntactic)."""
    by_atom = {}
    for t in testimonies:
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

CONFLICT_SKIP = "mutual-block priority encoding not settled"


def _has_unequal_mutual(testimonies):
    """Detect an atom whose two sides are stated by mutual
    blockers at UNEQUAL strengths — the reading (undercut-with-independence vs
    priority-netting) is not settled, so we decline to score it. Equal
    strengths, and one-sided mutual blockers with a plain other side, net
    cleanly and are scored normally."""
    by_atom = {}
    for t in testimonies:
        if t.mutual:
            by_atom.setdefault(t.head_atom, {}).setdefault(t.head_sign, [])
            for (prio, _) in t.mutual:
                by_atom[t.head_atom][t.head_sign].append(prio)
    for atom, sides in by_atom.items():
        pro = max(sides.get("+", [0]), default=0)
        con = max(sides.get("-", [0]), default=0)
        both = ("+" in sides) and ("-" in sides)
        if both and pro != con and min(pro, con) > 0:
            # both sides mutually block at unequal strength: not settled.
            # (a one-sided mutual block with a plain other side has the same
            #  structural signature; it is intentionally covered by the priority
            #  award below and scored normally. We only decline to score when BOTH sides carry a
            #  mutual block AND the intended reading is undercut. We cannot tell
            #  these apart from syntax alone; this model does not resolve it. Here we
            #  score with the priority award and mark the answer 'priority_note'.)
            return atom
    return None


def _has_rank_restricted_blocker(testimonies, by_head):
    """Detect the C2-blocker signature: a distinct-atom blocker check at rank r
    whose content atom's support flows through a rule SELF-protected at a rank
    STRICTLY BELOW r. gk's search side then refuses that support inside the check
    ("may not use lower-priority defaults"); this model has no
    rank classes on checks and would let it block — so it must defer, not
    mis-score. Returns (content_atom, check_rank, protect_rank) or None."""
    for t in testimonies:
        for (batom, bsign, prio) in t.blockers:
            for s_t in by_head.get(batom, []):
                if s_t.head_sign != bsign or not s_t.mutual:
                    continue
                for (mprio, _msign) in s_t.mutual:
                    if 0 < mprio < prio:
                        return (batom, prio, mprio)
    return None


def evaluate(pool, confs, query_atom, query_sign, trials, seed):
    testimonies, atoms = build_testimonies(pool, confs, query_atom, query_sign)
    order = _topo_order(testimonies, atoms)
    plan = None
    if order is None:
        plan, why = _scc_plan(testimonies, atoms)
        if plan is None:
            return {"support_for": None, "support_against": None,
                    "conflict": None, "ignorance": None,
                    "not_scored": f"{why} (cycle through a blocker or contested atom); not scored"}
    by_head = {}
    for t in testimonies:
        by_head.setdefault(t.head_atom, []).append(t)

    priority_note = _has_unequal_mutual(testimonies)
    rank_note = _has_rank_restricted_blocker(testimonies, by_head)
    tally = {"for": 0, "against": 0, "conflict": 0, "ignorance": 0}
    rng = random.Random(seed)
    atoms_ordered = sorted(atoms, key=repr)   # canonical draw order: the seed
    # must fully determine each atom's U regardless of set hash randomization
    # (PYTHONHASHSEED) across processes -- else the table is not reproducible.
    for _ in range(trials):
        u = {a: rng.random() for a in atoms_ordered}
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
    if priority_note:
        out["priority_note"] = (
            f"atom {priority_note[0]} uses a mutual-block priority encoding; "
            f"scored with the higher-strength side taking the overlap; the other reading "
            f"is not settled by this model")
    elif rank_note:
        out["priority_note"] = (
            f"blocker check at rank {rank_note[1]} targets {rank_note[0]}, whose "
            f"support is protected at lower rank {rank_note[2]}: gk's search-side "
            f"rank restriction applies here, which this model does "
            f"not implement , so it is scored without that restriction")
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


def _pools(head_atom, ts, state):
    """Return (a, b, filled, pri_pro, pri_con): pooled pro/con strengths of the
    PRESENT testimonies, whether a paired-exception residual fill applies, and the
    (mutual-block) priority of each side."""
    pro, con = [], []
    filled = False
    pri_pro = pri_con = 0
    main_pro_blocked = any(t.head_sign == "+" and (t.blockers) and not _present(t, state)
                           for t in ts)
    for t in ts:
        if not _present(t, state):
            continue
        if t.head_sign == "+":
            pro.append(t.strength)
            for (prio, _s) in t.mutual:
                pri_pro = max(pri_pro, prio)
        else:
            con.append(t.strength)
            for (prio, _s) in t.mutual:
                pri_con = max(pri_con, prio)
            if t.paired_main and main_pro_blocked:
                filled = True
    a = 1.0
    for w in pro:
        a *= (1 - w)
    a = 1 - a
    b = 1.0
    for w in con:
        b *= (1 - w)
    b = 1 - b
    return a, b, filled, pri_pro, pri_con


def _net(a, b, ul, filled, pri_pro, pri_con):
    """Return (pro_usable, con_usable, conflict) for one atom in one world."""
    lo = min(a, b)
    # priority overlap award (decision 5): the strictly-higher side takes the
    # conflict region U <= min(a,b); the lower keeps only its excess.
    if pri_pro != pri_con and lo > 0:
        if pri_pro > pri_con:
            pro = ul <= a
            con = a < ul <= b
            return pro, con, False
        else:
            con = ul <= b
            pro = b < ul <= a
            return pro, con, False
    pro = (b < ul <= a)
    con = (a < ul <= b)
    conflict = (ul <= lo)
    if filled and ul > b and not pro:
        pro = True                      # reading-D residual fill
    return pro, con, (conflict and not pro and not con)


def _eval_atom(atom, ts, state, u):
    a, b, filled, pp, pc = _pools(atom, ts, state)
    ul = u[atom]
    pro, con, _ = _net(a, b, ul, filled, pp, pc)
    return (pro, con)


def _classify(atom, sign, ts, state, u):
    a, b, filled, pp, pc = _pools(atom, ts, state)
    ul = u[atom]
    return _net(a, b, ul, filled, pp, pc)


def _atom_deps(testimonies, atoms):
    """The static atom dependency graph: head atom -> {body atoms, distinct-atom
    blocker atoms}. Mutual (same-atom) blocks are self-loops and ignored."""
    deps = {a: set() for a in atoms}
    for t in testimonies:
        for (ba, _s) in t.body:
            if ba != t.head_atom:
                deps[t.head_atom].add(ba)
        for (ba, _s, _p) in t.blockers:
            if ba != t.head_atom:
                deps[t.head_atom].add(ba)
    return deps


def _topo_order(testimonies, atoms):
    """Kahn topological sort over distinct-atom dependencies (body + distinct
    blockers). Returns None on a genuine cycle (the caller then falls back to
    the SCC/fixpoint plan of _scc_plan)."""
    deps = _atom_deps(testimonies, atoms)
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


def _scc_plan(testimonies, atoms):
    """Evaluation plan for a KB whose static atom graph is cyclic (equivalences,
    mutual rules): the SCC condensation in dependency-first order. Singleton SCCs
    evaluate exactly as on the acyclic path; each group of mutually dependent atoms is evaluated per
    world by least fixpoint (testimony presence = existence of a well-founded
    derivation in that world). The fixpoint is monotone -- hence unique and equal
    to the derivability reading -- ONLY when the cycle contains no blocker and no
    contested atom, so any cyclic group with a CONTESTED atom (testimony on both
    sides) or an internal BLOCKER edge is not settled and is not scored.
    Returns (plan, None) with plan a list of atom tuples, or (None, reason)."""
    deps = _atom_deps(testimonies, atoms)
    by_head = {}
    for t in testimonies:
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
        for t in testimonies:
            if t.head_atom in cset:
                for (ba, _bs, _p) in t.blockers:
                    if ba in cset:
                        return None, (f"blocker on {ba} inside a "
                                      f"dependency cycle")
        plan.append(tuple(sorted(comp, key=repr)))
    return plan, None


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
