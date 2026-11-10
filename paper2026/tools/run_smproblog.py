"""Runs smProbLog from the clone in src/smProblog without changing it.
smProbLog 2.1.0.42 was written for Python 3.6 to 3.8. This script restores three names
that later Python versions removed, then starts problog's command line:
  collections.MutableSet, MutableMapping, Sequence -> the classes in collections.abc
  inspect.getargspec -> a wrapper of inspect.getfullargspec
It also registers an empty module pysdd. problog/sdd_formula.py imports pysdd at its top
without a try block. pysdd is optional, and the runs use -k ddnnf, which needs no pysdd.
The later imports from pysdd inside a try block then fail, as without pysdd installed.
In the same way problog/sdd_formula_explicit_defined.py imports aspmc at its top. Only the
SDD knowledge compilation with defined vtrees uses aspmc. The script registers stub
modules for aspmc; each stub name raises an error when called.
Use it with PyPy 3.11, which still has the modules imp and distutils.

Usage: SMPROBLOG_SRC=<clone of github.com/PietroTotis/smProblog> \
  pypy3 tools/run_smproblog.py -k ddnnf FILE.pl
"""
import collections, collections.abc, inspect, os, runpy, sys, types


def unavailable(*args, **kw):
  raise RuntimeError('aspmc is not installed; run_smproblog.py supplies only stub modules')


def setup():
  for name in ('MutableSet', 'MutableMapping', 'Sequence', 'Mapping', 'Iterable'):
    if not hasattr(collections, name):
      setattr(collections, name, getattr(collections.abc, name))
  if not hasattr(inspect, 'getargspec'):
    def getargspec(func):
      s = inspect.getfullargspec(func)
      return inspect.ArgSpec(s.args, s.varargs, s.varkw, s.defaults) if hasattr(inspect, 'ArgSpec') else (s.args, s.varargs, s.varkw, s.defaults)
    inspect.getargspec = getargspec
  sys.modules.setdefault('pysdd', types.ModuleType('pysdd'))

  for mod, names in (('aspmc', ()), ('aspmc.compile', ()), ('aspmc.compile.vtree', ('Vtree',)),
                     ('aspmc.compile.cnf', ('CNF',)), ('aspmc.compile.constrained_compile', ('tree_from_cnf',))):
    m = types.ModuleType(mod)
    for n in names:
      setattr(m, n, unavailable)
    sys.modules.setdefault(mod, m)
  sys.path.insert(0, os.environ['SMPROBLOG_SRC'])


if __name__ == '__main__':
  setup()
  sys.argv[0] = 'problog'
  runpy.run_module('problog', run_name='__main__', alter_sys=True)
