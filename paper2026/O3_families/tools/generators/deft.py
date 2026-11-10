"""The default chains, trees, cascades and disputed theories in DEFT's DLGP syntax,
copied unchanged from the trial's runner of 2026-11-04."""



def chain(n):
  return ['a0(c).'] + [f'[DEFTr{i}] a{i+1}(X) :- a{i}(X).' for i in range(n)], [f'a{n}(c)']


def tree(b, d):
  cl = []; count = [0]

  def node(depth):
    count[0] += 1; me = f't{count[0]}'
    if depth == d:
      cl.append(f'{me}(c).'); return me
    kids = [node(depth + 1) for _ in range(b)]
    cl.append(f'[DEFTr{me}] {me}(X) :- ' + ', '.join(f'{k}(X)' for k in kids) + '.')
    return me
  root = node(0)
  return cl, [f'{root}(c)'], count[0]


def cascade(n, priorities):
  cl = ['top(c).', f'a{n}(c).']
  for i in range(n, 0, -1):
    cl.append(f'[DEFTd{i-1}] a{i-1}(X) :- top(X).')
    cl.append(f'[DEFTr{i-1}] na{i-1}(X) :- a{i}(X).')
    cl.append(f'! :- a{i-1}(X), na{i-1}(X).')
    if priorities:
      cl.append(f'[DEFTr{i-1}] > [DEFTd{i-1}].')
  return cl, ['a0(c)', 'na0(c)']


def disputed(m):
  cl = ['top(c).']
  for i in range(m):
    cl.append(f'[DEFTp{i}] a{i}(X) :- top(X).'); cl.append(f'[DEFTn{i}] na{i}(X) :- top(X).'); cl.append(f'! :- a{i}(X), na{i}(X).')
  return cl, ['a0(c)', 'na0(c)']


