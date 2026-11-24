"""Conversion of a binary Bayesian network in BIF format into a gk input, copied
unchanged from the trial's generator of 2026-11-04 (family B). Needs pgmpy and networkx.
The first state listed in the BIF file is read as true. State true is positive
usability and state false is ignorance. Each CPT row with a positive probability
becomes a rule p::node :- ones, unless(g), where g holds when a parent that the row
sets to false holds."""
import itertools


def read_bif(path):
  """returns nodes in topological order: name, parents, states, cpt rows p_true per
  parent-state combination (parents' states in the BIF's listed order)."""
  from pgmpy.readwrite import BIFReader
  r = BIFReader(path)
  model = r.get_model()
  states = r.variable_states
  order = list(model.nodes())
  # topological order
  import networkx as nx
  order = list(nx.topological_sort(model))
  nodes = []
  for n in order:
    cpd = model.get_cpds(n)
    parents = list(cpd.variables[1:])
    vals = cpd.get_values()   # shape (card(n), prod(card(parents)))
    nodes.append(dict(name=n, parents=parents, states=states[n], card=cpd.cardinality.tolist(), values=vals.tolist(),
                      parent_states=[states[p] for p in parents]))
  return nodes, model


def atom(name):
  s = ''.join(c if c.isalnum() else '_' for c in name).lower()
  if not s[0].isalpha():
    s = 'v_' + s
  return s


def to_gkp(nodes):
  """binary network -> gk clauses (the construction of core.binary_to_program)."""
  import itertools
  cl = []
  for n in nodes:
    if any(c != 2 for c in n['card']):
      raise ValueError('not binary: ' + n['name'])
    name = atom(n['name']); parents = [atom(p) for p in n['parents']]
    k = len(parents)
    vals = n['values']   # vals[0][col] = P(first state | parent column col)
    # pgmpy column order: parents' states vary with the last parent fastest; state 0 = first = "true"
    for col, bits in enumerate(itertools.product((0, 1), repeat=k)):
      # bits index into parent states: 0 -> first state (true), 1 -> second (false)
      p = vals[0][col]
      if p <= 0:
        continue
      ones = [a for a, b in zip(parents, bits) if b == 0]
      zeros = [a for a, b in zip(parents, bits) if b == 1]
      body = list(ones)
      exc = None
      if len(zeros) == 1:
        exc = zeros[0]
      elif zeros:
        gate = f'aux_{name}_row{col}'
        for z in zeros:
          cl.append(f'{gate} :- {z}.')
        exc = gate
      conf = '' if p >= 1 else f'{p:.6g}::'
      if not body and not exc:
        cl.append(f'{conf}{name}.')
      else:
        parts = body + ([f'unless({exc})'] if exc else [])
        cl.append(f'{conf}{name} :- ' + ', '.join(parts) + '.')
  return cl


def depth_order(nodes):
  d = {}
  for n in nodes:
    d[n['name']] = 0 if not n['parents'] else 1 + max(d[p] for p in n['parents'])
  return d


