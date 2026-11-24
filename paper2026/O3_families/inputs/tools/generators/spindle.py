"""The default chains, cycles, cascades, trees and disputed theories in SPINdle's DFL
syntax, copied unchanged from the trial's runner of 2026-11-04."""



def chain(n, strict):
  op = '->' if strict else '=>'
  return ['>> a0'] + [f'r{i}: a{i} {op} a{i+1}' for i in range(n)], f'a{n}'


def cycle(n):
  return [f'r{i}: a{i} => a{(i+1) % n}' for i in range(n)], 'a0'


def cascade(n, priorities):
  cl = [f'>> a{n}']
  for i in range(n, 0, -1):
    cl.append(f'd{i-1}: => a{i-1}')
    cl.append(f'r{i-1}: a{i} => -a{i-1}')
    if priorities:
      cl.append(f'r{i-1} > d{i-1}')
  return cl, 'a0'


def tree(b, d):
  cl = []; count = [0]

  def node(depth):
    count[0] += 1; me = f't{count[0]}'
    if depth == d:
      cl.append(f'>> {me}'); return me
    kids = [node(depth + 1) for _ in range(b)]
    cl.append(f'r{me}: ' + ','.join(kids) + f' => {me}')
    return me
  root = node(0)
  return cl, root, count[0]


def disputed(m):
  cl = []
  for i in range(m):
    cl.append(f'p{i}: => a{i}'); cl.append(f'n{i}: => -a{i}')
  return cl, 'a0'


