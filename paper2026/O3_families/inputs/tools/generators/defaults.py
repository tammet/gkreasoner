"""Generation functions of the default chains, the cascades and the trees (family D),
copied unchanged from the trial's generator of 2026-11-04. Rank 0 in a chain or a tree
is gk's equal rank; the cascades use ranks 1 and 2."""



def chain(n, strict):
  cl = ['a0.']
  for i in range(n):
    cl.append(f'a{i+1} :- a{i}.' if strict else f'a{i+1} :- a{i}, unless(-a{i+1}, 0).')
  return cl, f'a{n}', '(1, 0, 0, 0)'


def cascade(n, priorities):
  """a_n is a fact; for i = n..1: a_{i-1} holds by default; a_i attacks it with
  -a_{i-1}. With priorities the attacker (rank 1) beats the default (rank 0), so
  a_{n-k} holds iff k is even. Without priorities both have rank 0."""
  # rank 0 is not a rank in gk (reading 'rank zero as equal rank'): use 1 and 2
  cl = [f'a{n}.']
  ra = 2 if priorities else 1
  for i in range(n, 0, -1):
    cl.append(f'a{i-1} :- unless(-a{i-1}, 1).')
    cl.append(f'-a{i-1} :- a{i}, unless(a{i-1}, {ra}).')
  exp = ('(1, 0, 0, 0) if n even else (0, 1, 0, 0)' if priorities else 'equal ranks: ignorance at odd distance from a_n, true at even')
  return cl, 'a0', exp


def tree(b, d):
  """node derived from all its b children (defeasibly); leaves are facts."""
  cl = []
  count = [0]

  def node(depth):
    count[0] += 1
    me = f't{count[0]}'
    if depth == d:
      cl.append(f'{me}.')
      return me
    kids = [node(depth + 1) for _ in range(b)]
    cl.append(f'{me} :- ' + ', '.join(kids) + f', unless(-{me}, 0).')
    return me
  root = node(0)
  return cl, root, '(1, 0, 0, 0)', count[0]


