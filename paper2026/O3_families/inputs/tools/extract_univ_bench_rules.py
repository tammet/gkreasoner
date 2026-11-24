#!/usr/bin/env python3
"""Datalog rules from the Univ-Bench ontology (subclass, subproperty, domain, range,
inverse, transitive), written as gk/ProbLog rules over binary `p(S,O)` and unary
`c(X)` predicates. The OWL file is data read with rdflib; the rules are ours."""
import re, sys
from rdflib import Graph, RDF, RDFS, OWL, Namespace
g = Graph(); g.parse(sys.argv[1], format='xml')
UB = Namespace('http://swat.cse.lehigh.edu/onto/univ-bench.owl#')
def nm(u):
  s = str(u).split('#')[-1]
  s = re.sub(r'[^A-Za-z0-9_]', '_', s)
  return s[0].lower() + s[1:]
rules = []
for s, o in g.subject_objects(RDFS.subClassOf):
  if (s, RDF.type, OWL.Class) in g or (s, RDF.type, OWL.Class) or True:
    if str(o).startswith(str(UB)) and str(s).startswith(str(UB)):
      rules.append(f'{nm(o)}(X) :- {nm(s)}(X).')
for s, o in g.subject_objects(RDFS.subPropertyOf):
  rules.append(f'{nm(o)}(X,Y) :- {nm(s)}(X,Y).')
for s, o in g.subject_objects(RDFS.domain):
  if str(o).startswith(str(UB)): rules.append(f'{nm(o)}(X) :- {nm(s)}(X,Y).')
for s, o in g.subject_objects(RDFS.range):
  if str(o).startswith(str(UB)): rules.append(f'{nm(o)}(Y) :- {nm(s)}(X,Y).')
for s, o in g.subject_objects(OWL.inverseOf):
  rules.append(f'{nm(o)}(Y,X) :- {nm(s)}(X,Y).'); rules.append(f'{nm(s)}(Y,X) :- {nm(o)}(X,Y).')
for s in g.subjects(RDF.type, OWL.TransitiveProperty):
  rules.append(f'{nm(s)}(X,Z) :- {nm(s)}(X,Y), {nm(s)}(Y,Z).')
# intersection / restriction classes are skipped (noted)
rules = sorted(set(rules))
open('lubm_rules.pl', 'w').write('\n'.join(rules) + '\n')
print(len(rules), 'rules')
cls = set(nm(c) for c in g.subjects(RDF.type, OWL.Class) if str(c).startswith(str(UB)))
props = set(nm(p) for p in g.subjects(RDF.type, OWL.ObjectProperty))
print(len(cls), 'classes;', len(props), 'object properties')
print('\n'.join(rules[:12]))
