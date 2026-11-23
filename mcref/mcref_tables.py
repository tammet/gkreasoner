"""mcref_tables: the state of one atom in mcref. The states POS, NEG, CON, IGN, UNRES; the tuple of an
application (tuple_of()); the support of a side, each rule identity counted once (pool(), support()); the table
of the state of one atom (rows(), outcome(), outcome_sets_plain()); and the selections of a side that the
narrowing reads (wf_side_usable(), side_regimes(), row_side_holds())."""
import itertools

from mcref_apps import CHECK_SUPPORT, PCACHE, PCACHE_LIMIT, RULE_W


POS, NEG, CON, IGN, UNRES = 0, 1, 2, 3, 4


# ------------------------------------------------------------------ the tables

# ------------------------------------------------------------------ the support of a side
#
# An application is a tuple (sign, 1 - confidence, body, exceptions, normal,
# rank). When an input has an application with rule identities (the
# application of a proof or a case application that uses uncertain rules),
# that application and every uncertain rule with an identity get a seventh
# entry: the set of rule identities (a proof or a case application: the
# rules it uses; a rule: itself). The support of a side is the probability
# that at least one present application has all its rules, each identity
# counted once and different identities independent. An application of six
# entries has an identity of its own. When the present identities are
# disjoint, that probability is 1 - (product of 1 - confidence); it is
# computed so, and an input without such applications has six-entry tuples
# only.

def tuple_of(x, idx, part4):
  """the tuple of the application x for byatom, with the atom indices idx;
  part4: the input has an application with rule identities"""
  body = [(idx[a], POS if s == 0 else NEG) for s, a in x.body]
  exc = [(idx[a], POS if s == 0 else NEG) for s, a in x.exc]
  if x.cls:
    exc += [(idx[k], POS) for k in x.cls]   # requirement 2: blocked where the clause node is positive (contradicted)
  t = (x.hsign, 1.0 - x.conf, body, exc, x.normal, x.rank)
  if part4 and (x.ids or x.rid is not None):
    t += (x.ids if x.ids else frozenset([x.rid]),)
  return t


def dnf_prob(terms):
  """the probability that some set of terms has all its identities true,
  the identities independent with the confidences RULE_W (Shannon expansion
  on the most frequent identity, independent parts multiplied, memoized)"""
  key = frozenset(terms)
  r = PCACHE.get(key)
  if r is not None:
    return r
  ts = sorted(key, key=len)
  mins = []
  for t in ts:
    if not any(m <= t for m in mins):
      mins.append(t)
  if not mins:
    r = 0.0
  elif not mins[0]:
    r = 1.0
  elif len(mins) == 1:
    r = 1.0
    for i in sorted(mins[0]):
      r *= RULE_W[i]
  else:
    parts, seen = [], set()
    for t in mins:   # the independent parts: the terms connected by shared identities
      if t in seen:
        continue
      part, todo, idsp = [t], [t], set(t)
      seen.add(t)
      while todo:
        todo.pop()
        for t2 in mins:
          if t2 not in seen and not idsp.isdisjoint(t2):
            seen.add(t2)
            part.append(t2)
            todo.append(t2)
            idsp |= t2
      parts.append(part)
    if len(parts) > 1:
      q = 1.0
      for part in parts:
        q *= 1.0 - dnf_prob(part)
      r = 1.0 - q
    else:
      cnt = {}
      for t in mins:
        for i in t:
          cnt[i] = cnt.get(i, 0) + 1
      v = max(sorted(cnt), key=lambda i: cnt[i])
      c = RULE_W[v]
      r = c * dnf_prob([t - {v} for t in mins]) + (1.0 - c) * dnf_prob([t for t in mins if v not in t])
  if len(PCACHE) < PCACHE_LIMIT:
    PCACHE[key] = r
  return r


def dnf_brute(terms):
  """dnf_prob() by a sum over every assignment of the identities (the test
  setting CHECK_SUPPORT)"""
  ids = sorted(set().union(*terms)) if terms else []
  tot = 0.0
  for bits in itertools.product((0, 1), repeat=len(ids)):
    on = {i for i, b in zip(ids, bits) if b}
    if any(t <= on for t in terms):
      w = 1.0
      for i, b in zip(ids, bits):
        w *= RULE_W[i] if b else 1.0 - RULE_W[i]
      tot += w
  return tot


SUPPORT_CHECKS = [0, 0, 0.0]   # CHECK_SUPPORT: calls with shared identities, mismatches above 1e-12, largest difference


def pool(r6, p7):
  """the support of a side: r6 is the product of 1 - confidence of its
  present six-entry applications, p7 its present seven-entry ones"""
  seen = set()
  for x in p7:
    if not seen.isdisjoint(x[6]):
      break
    seen |= x[6]
  else:
    r = r6
    for x in p7:
      r *= x[1]
    return 1.0 - r
  terms = [x[6] for x in p7]
  s7 = dnf_prob(terms)
  if CHECK_SUPPORT:
    d = abs(s7 - dnf_brute(terms))
    SUPPORT_CHECKS[0] += 1
    if d > 1e-12:
      SUPPORT_CHECKS[1] += 1
    SUPPORT_CHECKS[2] = max(SUPPORT_CHECKS[2], d)
  return 1.0 - r6 * (1.0 - s7)


def support(present):
  """the support of a side from its present applications"""
  r6, p7 = 1.0, []
  for x in present:
    if len(x) > 6:
      p7.append(x)
    else:
      r6 *= x[1]
  return pool(r6, p7) if p7 else 1.0 - r6


def rows(np, nn, ordp, ordn, rp, rn, a, b, u, v):
  """the state of an atom from its two sides: np, nn applications present
  for and against it, ordp, ordn of them ordinary, rp, rn the largest ranks
  of the normal defaults, a, b the supports (the table of the state of one
  atom). The kind of a side is decided here, from the present
  applications."""
  if not np and not nn:
    return IGN
  if not nn:
    return POS if u < a else IGN
  if not np:
    return NEG if u < b else IGN
  normp = ordp == 0
  normn = ordn == 0
  if not normp and not normn:
    if b <= u < a:
      return POS
    if a <= u < b:
      return NEG
    return CON if u < min(a, b) else IGN
  if normp and not normn:
    return NEG if u < b else (POS if v < a else IGN)
  if normn and not normp:
    return POS if u < a else (NEG if v < b else IGN)
  if rp == rn or rp == 0 or rn == 0:
    p, q = u < a, v < b
    return POS if p and not q else (NEG if q and not p else IGN)
  if rp > rn:
    return POS if u < a else (NEG if u < b else IGN)
  return NEG if u < b else (POS if u < a else IGN)


def outcome(apps, state, u, v):
  """the state of one atom from the final states of the atoms it reads: an
  application is present when its body literals are usable and none of its
  exceptions is. apps holds (sign, 1 - confidence, body,
  exceptions, normal, rank) with body and exception entries (atom, state)."""
  ra = rb = 1.0
  np = nn = 0
  ordp = ordn = 0
  rp = rn = 0
  p7 = n7 = None
  for x in apps:
    ok = True
    for a, s in x[2]:
      if state[a] != s:
        ok = False
        break
    if ok:
      for a, s in x[3]:
        if state[a] == s:
          ok = False
          break
    if not ok:
      continue
    if x[0] == 0:
      np += 1
      if len(x) > 6:
        p7 = (p7 or []) + [x]
      else:
        ra *= x[1]
      if x[4]:
        rp = max(rp, x[5])
      else:
        ordp += 1
    else:
      nn += 1
      if len(x) > 6:
        n7 = (n7 or []) + [x]
      else:
        rb *= x[1]
      if x[4]:
        rn = max(rn, x[5])
      else:
        ordn += 1
  return rows(np, nn, ordp, ordn, rp, rn, pool(ra, p7) if p7 else 1.0 - ra, pool(rb, n7) if n7 else 1.0 - rb, u, v)


def outcome_sets_plain(apps, u, v, bset, eset):
  """outcome_sets() without the rank rule"""
  ra = rb = 1.0
  np = nn = 0
  ordp = ordn = 0
  rp = rn = 0
  p7 = n7 = None
  for x in apps:
    hs, q, body, exc, normal, rank = x[:6]
    ok = True
    for j, s in body:
      if (j, s) not in bset:
        ok = False
        break
    if ok:
      for j, s in exc:
        if (j, s) in eset:
          ok = False
          break
    if not ok:
      continue
    if hs == 0:
      np += 1
      if len(x) > 6:
        p7 = (p7 or []) + [x]
      else:
        ra *= q
      if normal:
        rp = max(rp, rank)
      else:
        ordp += 1
    else:
      nn += 1
      if len(x) > 6:
        n7 = (n7 or []) + [x]
      else:
        rb *= q
      if normal:
        rn = max(rn, rank)
      else:
        ordn += 1
  return rows(np, nn, ordp, ordn, rp, rn, pool(ra, p7) if p7 else 1.0 - ra, pool(rb, n7) if n7 else 1.0 - rb, u, v)




# ------------------------------------------------------------------ the narrowing
#
# Literals are (atom index, POS or NEG). The sets: X is the set being built,
# L the old sure set, U the old possible set. An application's side reads
# bodies from one set and exceptions from another, as the steps of the new
# sure set and the new possible set say.

def wf_side_usable(sign, apps, u_val, v_val, body_own, exc_own, body_opp, exc_opp):
  """whether the tables give the atom the sign, for sides without normal
  defaults: the rows reduce to b <= u < a and a <= u < b, which are monotone
  in the own side's applications and antitone in the opposing side's, so
  one selection decides."""
  ra = rb = 1.0
  np = nn = 0
  p7 = n7 = None
  for x in apps:
    hs, q, body, exc = x[:4]
    if hs == sign:
      bset, eset = body_own, exc_own
    else:
      bset, eset = body_opp, exc_opp
    ok = True
    for j, s in body:
      if (j, s) not in bset:
        ok = False
        break
    if ok:
      for j, s in exc:
        if (j, s) in eset:
          ok = False
          break
    if not ok:
      continue
    if hs == 0:
      np += 1
      if len(x) > 6:
        p7 = (p7 or []) + [x]
      else:
        ra *= q
    else:
      nn += 1
      if len(x) > 6:
        n7 = (n7 or []) + [x]
      else:
        rb *= q
  a = pool(ra, p7) if p7 else 1.0 - ra
  b = pool(rb, n7) if n7 else 1.0 - rb
  if sign == 0:
    if not np:
      return False
    return (u_val < a) if not nn else (b <= u_val < a)
  if not nn:
    return False
  return (u_val < b) if not np else (a <= u_val < b)


def side_regimes(apps_side, bmin, emax, bmax, emin, require_nonempty_min=False):
  """the regimes (present, normal, rank, least support, largest support)
  that a side can take over the selections between its certainly present
  applications (bodies in bmin, no exception in emax) and its possibly
  present ones (bodies in bmax, no exception in emin): the selections of
  the narrowing for a side with normal defaults. A selection changes the
  side's support, its
  kind and its rank; one regime per reachable (kind, rank) with the range
  of supports it can have."""
  s_min, s_max = [], []
  for x in apps_side:
    in_max = all(l in bmax for l in x[2]) and not any(e in emin for e in x[3])
    if not in_max:
      continue
    s_max.append(x)
    if bmin is not None and all(l in bmin for l in x[2]) and not any(e in emax for e in x[3]):
      s_min.append(x)
  regs = []
  if not s_min and not require_nonempty_min:
    regs.append((False, False, 0, 0.0, 0.0))
  if not s_max:
    return regs
  if any(len(x) > 6 for x in s_max):
    return side_regimes_p4(s_min, s_max, regs)
  r_smin = 1.0
  min_has_ord = False
  for x in s_min:
    r_smin *= x[1]
    if not x[4]:
      min_has_ord = True
  max_ords = [x for x in s_max if not x[4]]
  if max_ords:
    r_smax = 1.0
    for x in s_max:
      r_smax *= x[1]
    if min_has_ord:
      r_ord_max = r_smin
    else:
      s_min_ids = {id(x) for x in s_min}
      r_ord_max = r_smin * max(x[1] for x in max_ords if id(x) not in s_min_ids)
    regs.append((True, False, 0, 1.0 - r_ord_max, 1.0 - r_smax))
  if not min_has_ord:
    n_max = [x for x in s_max if x[4]]
    if n_max:
      r_base = max((x[5] for x in s_min), default=None)
      ranks = sorted({x[5] for x in n_max if r_base is None or x[5] >= r_base})
      s_min_ids = {id(x) for x in s_min}
      for rk in ranks:
        r_rk_min = 1.0
        for x in n_max:
          if x[5] <= rk:
            r_rk_min *= x[1]
        if r_base is not None and rk == r_base:
          r_rk_max = r_smin
        else:
          r_rk_max = r_smin * max(x[1] for x in n_max if x[5] == rk and id(x) not in s_min_ids)
        regs.append((True, True, rk, 1.0 - r_rk_max, 1.0 - r_rk_min))
  return regs


def side_regimes_p4(s_min, s_max, regs):
  """side_regimes() for a side with seven-entry applications (rule
  identities): the
  same regimes, with the supports computed by support(). The support grows
  with the set of present applications, so the least support of a regime
  that needs one more application adds the one that gives the least."""
  min_has_ord = any(not x[4] for x in s_min)
  max_ords = [x for x in s_max if not x[4]]
  s_min_ids = {id(x) for x in s_min}
  if max_ords:
    if min_has_ord:
      lo = support(s_min)
    else:
      lo = min(support(s_min + [x]) for x in max_ords if id(x) not in s_min_ids)
    regs.append((True, False, 0, lo, support(s_max)))
  if not min_has_ord:
    n_max = [x for x in s_max if x[4]]
    if n_max:
      r_base = max((x[5] for x in s_min), default=None)
      ranks = sorted({x[5] for x in n_max if r_base is None or x[5] >= r_base})
      for rk in ranks:
        hi = support([x for x in n_max if x[5] <= rk])
        if r_base is not None and rk == r_base:
          lo = support(s_min)
        else:
          lo = min(support(s_min + [x]) for x in n_max if x[5] == rk and id(x) not in s_min_ids)
        regs.append((True, True, rk, lo, hi))
  return regs


def row_side_holds(sign, own_reg, a_own, opp_reg, b_opp, u_val, v_val):
  """whether the row selected by the two regimes gives the atom the sign,
  with the own side's support a_own and the opposing side's b_opp (the
  table of the state of one atom, read for one sign)"""
  p_own, norm_own, r_own = own_reg
  p_opp, norm_opp, r_opp = opp_reg
  if not p_own:
    return False
  if not p_opp:
    return u_val < a_own
  if sign == 0:
    a, b, normp, normn, rp, rn = a_own, b_opp, norm_own, norm_opp, r_own, r_opp
    if not normp and not normn:
      return b <= u_val < a
    if normp and not normn:
      return (u_val >= b) and (v_val < a)
    if normn and not normp:
      return u_val < a
    if rp == rn or rp == 0 or rn == 0:
      return (u_val < a) and (v_val >= b)
    if rp > rn:
      return u_val < a
    return b <= u_val < a
  a, b, normp, normn, rp, rn = b_opp, a_own, norm_opp, norm_own, r_opp, r_own
  if not normp and not normn:
    return a <= u_val < b
  if normp and not normn:
    return u_val < b
  if normn and not normp:
    return (u_val >= a) and (v_val < b)
  if rp == rn or rp == 0 or rn == 0:
    return (v_val < b) and (u_val >= a)
  if rp > rn:
    return a <= u_val < b
  return u_val < b
