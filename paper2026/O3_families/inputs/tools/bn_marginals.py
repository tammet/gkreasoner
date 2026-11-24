#!/usr/bin/env python3
"""The pgmpy targets of the Bayesian networks of part O3.

Computes the unconditional marginal P(node = first state) of the 13 queries
of bn/ by variable elimination, as the trial did with pgmpy 1.1.2, and prints
one JSON object. Needs pgmpy and the BIF files of the bnlearn repository
(README.md, "The bnlearn networks"):

  python3 tools/bn_marginals.py BIF_FOLDER
"""
import json, os, sys

QUERIES = {"asia": ["xray", "bronc", "either"], "earthquake": ["JohnCalls", "Alarm"],
           "cancer": ["Xray", "Cancer"], "win95pts": ["PrtStatPaper", "Problem1", "PC2PRT"],
           "andes": ["RApp3", "SNode_151", "SNode_74"]}


def main():
  from pgmpy.readwrite import BIFReader
  from pgmpy.inference import VariableElimination
  out = {}
  for net, nodes in QUERIES.items():
    model = BIFReader(os.path.join(sys.argv[1], net + ".bif")).get_model()
    ve = VariableElimination(model)
    for n in nodes:
      out[f"{net}_{n.lower()}"] = float(ve.query([n], show_progress=False).values[0])
  print(json.dumps(out, indent=1))


if __name__ == "__main__":
  main()
