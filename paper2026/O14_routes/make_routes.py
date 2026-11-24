#!/usr/bin/env python3
"""make_routes.py: write the route inputs of this part, or check that the files in inputs/ equal them.

  python3 make_routes.py OUT_FOLDER     write every route input into OUT_FOLDER
  python3 make_routes.py --check        compare every route input with the file of the same name in inputs/

The four route families, for K links from n0 to nK:
  route_c1b_K.gkp  K uncertain links 0.99::link(ni,ni+1); the uncertain reach rules (base and recursive) of .99;
                   the default 0.8::open(X) :- reach(n0,X), unless(closed(X)); 0.5::closed(nK); the question
                   open(nK). The support of the question is .99^(2K) x .4.
  rt_c2_K.gkp      K links of .9 and the certain reach rules; the question reach(n0,nK); support .9^K.
  rt_mix_K.gkp     K links of .9, the certain reach rules, the default and closed(nK) as above; support .9^K x .4.
  route_opp_K.gkp  route_c1b_K with a contrary report 0.3::-link(ni,ni+1) after every tenth link (i = 0, 10, ...).
                   With m such links, the support is .99^(K-m) x .69^m x .99^K x .4.
The other systems' files:
  pl_route_K.pl, pl_mix_K.pl  the same input for ProbLog, the exception written as \\+ closed(X)
  asp_route_K.lp              route_c1b_K for clingo's grounder: each link a choice {link(ni,ni+1)}, the rules
                              without weights, the exception as not closed(X), the choice {closed(nK)}
Python 3.9 or later, no other package.
"""
import os
import sys

ROUTE_K = (5, 20, 40, 60, 80, 200)
MIX_K = (5, 10, 20, 80, 200)
OPP_K = (5, 10, 20, 40, 60, 80, 200)
C2_K = (5, 20, 40, 60, 80, 200)


def c1b(k):
  t = "".join("0.99::link(n%d,n%d).\n" % (i, i + 1) for i in range(k))
  t += "0.99::reach(X,Y) :- link(X,Y).\n0.99::reach(X,Z) :- link(X,Y), reach(Y,Z).\n"
  t += "0.8::open(X) :- reach(n0,X), unless(closed(X)).\n0.5::closed(n%d).\nquery(open(n%d)).\n" % (k, k)
  return t


def c2(k):
  t = "".join("0.9::link(n%d,n%d).\n" % (i, i + 1) for i in range(k))
  t += "reach(X,Y) :- link(X,Y).\nreach(X,Z) :- link(X,Y), reach(Y,Z).\n"
  t += "query(reach(n0,n%d)).\n" % k
  return t


def mix(k):
  t = "".join("0.9::link(n%d,n%d).\n" % (i, i + 1) for i in range(k))
  t += "reach(X,Y) :- link(X,Y).\nreach(X,Z) :- link(X,Y), reach(Y,Z).\n"
  t += "0.8::open(X) :- reach(n0,X), unless(closed(X)).\n0.5::closed(n%d).\nquery(open(n%d)).\n" % (k, k)
  return t


def to_problog(t):
  return t.replace("unless(closed(X))", "\\+ closed(X)")


def to_asp(t):
  out = []
  for line in t.split("\n"):
    s = line.strip()
    if not s or s.startswith("query("):
      continue
    if s.startswith("0.99::link("):
      out.append("{%s}." % s[len("0.99::"):-1])
    elif s.startswith("0.5::closed("):
      out.append("{%s}." % s[len("0.5::"):-1])
    elif "::" in s:
      out.append(s.split("::", 1)[1].replace("unless(closed(X))", "not closed(X)"))
    else:
      out.append(s)
  return "\n".join(out) + "\n"


def opp(k):
  out = []
  for line in c1b(k).split("\n"):
    if not line:
      continue
    out.append(line)
    if line.startswith("0.99::link(n"):
      i = int(line[len("0.99::link(n"):].split(",")[0])
      if i % 10 == 0:
        out.append("0.3::-link(n%d,n%d)." % (i, i + 1))
  return "\n".join(out) + "\n"


def files():
  out = {}
  for k in sorted(set(ROUTE_K) | set(OPP_K)):
    out["route_c1b_%d.gkp" % k] = c1b(k)
  for k in ROUTE_K:
    out["pl_route_%d.pl" % k] = to_problog(c1b(k))
    out["asp_route_%d.lp" % k] = to_asp(c1b(k))
  for k in C2_K:
    out["rt_c2_%d.gkp" % k] = c2(k)
  for k in MIX_K:
    out["rt_mix_%d.gkp" % k] = mix(k)
    out["pl_mix_%d.pl" % k] = to_problog(mix(k))
  for k in OPP_K:
    out["route_opp_%d.gkp" % k] = opp(k)
  return out


def main():
  here = os.path.dirname(os.path.abspath(__file__))
  if len(sys.argv) == 2 and sys.argv[1] == "--check":
    bad = 0
    fs = files()
    for name, text in sorted(fs.items()):
      p = os.path.join(here, "inputs", name)
      if not os.path.exists(p) or open(p).read() != text:
        print("differs: " + name)
        bad += 1
    print("%d files compared, %d differ" % (len(fs), bad))
    sys.exit(1 if bad else 0)
  if len(sys.argv) != 2:
    print(__doc__)
    sys.exit(2)
  os.makedirs(sys.argv[1], exist_ok=True)
  for name, text in sorted(files().items()):
    open(os.path.join(sys.argv[1], name), "w").write(text)


if __name__ == "__main__":
  main()
