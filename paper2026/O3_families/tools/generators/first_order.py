"""Generation functions of the delivery and equipment families, copied unchanged from
the trial's generator of 2026-11-04."""



def equip_lines(ident_chain=1, extra_components=0, background=0, distinct=False):
  """version A with a chain of ident_chain equalities from maintenance_id to b7,
  extra components on the same supply, background installations, or distinct supplies"""
  L = ['supply(pump) = b7.', 'supply(controller) = b7.' if not distinct else 'supply(controller) = b8.']
  chain = ['maintenance_id'] + [f'm{j}' for j in range(1, ident_chain)] + ['b7']
  L += [f'{chain[j]} = {chain[j+1]}.' for j in range(len(chain) - 1)]
  L += ['component(pump).', 'component(controller).', '0.9::charged(b7).', '0.2::-charged(maintenance_id).',
        '0.1::-works(pump).', '0.15::-works(controller).']
  if distinct:
    L += ['maint8 = b8.', '0.9::charged(b8).', '0.2::-charged(maint8).']
  comps = ['pump', 'controller']
  for i in range(extra_components):
    L += [f'supply(c{i}) = b7.', f'component(c{i}).', f'0.1::-works(c{i}).']; comps.append(f'c{i}')
  for i in range(background):
    L += [f'supply(pump_{i}) = b_{i}.', f'supply(ctrl_{i}) = b_{i}.', f'maint_{i} = b_{i}.', f'component(pump_{i}).', f'component(ctrl_{i}).',
          f'0.9::charged(b_{i}).', f'0.2::-charged(maint_{i}).', f'0.1::-works(pump_{i}).', f'0.15::-works(ctrl_{i}).',
          f'ready_{i} :- works(pump_{i}), works(ctrl_{i}).']
  L += ['works(X) :- component(X), charged(supply(X)), unless(-works(X), 1).']
  if len(comps) <= 2:
    L += ['cooling_ready :- works(pump), works(controller).']
  else:
    L += ['ok(0).'] + [f'ok({i+1}) :- ok({i}), works({c}).' for i, c in enumerate(comps)] + [f'cooling_ready :- ok({len(comps)}).']
  L += ['query(cooling_ready).']
  return L


def equip_targets(extra_components=0, distinct=False):
  """(one-atom target, two-atom target): the charged premise usable at .7 under the
  one-atom normalization of the proposal, .72 under gk's reading with the contrary report
  at its own atom"""
  f = [.1, .15] + [.1] * extra_components
  prod = 1
  for x in f: prod *= 1 - x
  if distinct:
    return (.7 * .9 * .7 * .85, .72 * .9 * .72 * .85)
  return (.7 * prod, .72 * prod)


def deliv_lines(n_legs=1, h=.1, opposed=False, exc_chain=0, background=0, flat=False):
  """a plan of n_legs legs with warming strength h each (the short plan of the proposal is
  n_legs=1, h=.3); exc_chain: the warming event of leg 1 is derived through a chain of that
  length; background: unrelated parcels with their own one-leg plans"""
  L = ['parcel(p1).', '0.9::cold(p1, s0).'] + (['0.2::-cold(p1, s0).'] if opposed else [])
  legs = [f'leg{i}' for i in range(1, n_legs + 1)]
  sits = ['s0']
  for i, a in enumerate(legs):
    sits.append(f'do({a}, {sits[-1]})' if not flat else f's{i+1}')
  for i, a in enumerate(legs):
    L.append(f'plan_step(p1, {a}, {sits[i]}).')
    if flat: L.append(f'succ({sits[i]}, {a}, {sits[i+1]}).')
    if i == 0 and exc_chain:
      L.append(f'{h}::storm0.')
      L += [f'storm{j} :- storm{j-1}.' for j in range(1, exc_chain + 1)]
      L.append(f'warmed(p1, {a}, {sits[i]}) :- storm{exc_chain}.')
    else:
      L.append(f'{h}::warmed(p1, {a}, {sits[i]}).')
  L.append(f'0.95::handover_ok(p1, {sits[-1]}).')
  for b in range(background):
    L += [f'parcel(q{b}).', f'0.9::cold(q{b}, s0).', f'plan_step(q{b}, bleg{b}, s0).', f'0.3::warmed(q{b}, bleg{b}, s0).']
    if flat: L.append(f'succ(s0, bleg{b}, bs{b}).')
    L.append(f'0.95::handover_ok(q{b}, {"bs%d" % b if flat else "do(bleg%d, s0)" % b}).')
  if flat:
    L.append('cold(P, S2) :- cold(P, S), plan_step(P, A, S), succ(S, A, S2), unless(warmed(P, A, S)).')
  else:
    L.append('cold(P, do(A, S)) :- cold(P, S), plan_step(P, A, S), unless(warmed(P, A, S)).')
  L.append('delivered_cold(P, S) :- cold(P, S), handover_ok(P, S).')
  L.append(f'query(delivered_cold(p1, {sits[-1]})).')
  return L


def deliv_target(n_legs=1, h=.1, opposed=False):
  return (.7 if opposed else .9) * (1 - h) ** n_legs * .95


def to_problog(lines):
  out = []
  for l in lines:
    if l.startswith('0.2::-cold'): return None   # outside the class
    out.append(l.replace('unless(warmed(P, A, S))', '\\+warmed(P, A, S)'))
  return out


