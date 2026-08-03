#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import defaultdict
import json

# one-time prep:
#import nltk
#nltk.download('wordnet')
from nltk.corpus import wordnet as wn

def synset_graph():
    no_incoming = set()
    G = {}
    for ss in wn.all_synsets():
        n = ss.name()
        parents = [s.name() for s in ss.hypernyms()]
        children = [s.name() for s in ss.hyponyms()]
        if not parents:
            if not children:
                continue
            else:
                no_incoming.add(n)
        G[n] = {
            "children" : [s.name()
            for s in ss.hyponyms()],
            "parents" : parents,
            }
    return G, no_incoming

def cleanup(G, no_incoming):
    deleted = []
    for k, v in G.items():
        p_del = []
        for p in v["parents"]:
            if k not in G[p]["children"]:
                p_del.append(p)
        c_del = []
        for c in v["children"]:
            if k not in G[c]["parents"]:
                c_del.append(c)
        for p in p_del:
            v["parents"].remove(p)
        for c in c_del:
            v["children"].remove(c)
        if p_del and not v["parents"]:
            if not v["children"]:
                deleted.append(k)
            no_incoming.add(k)        

    for k in deleted:
        del G[k]
        
    return G, no_incoming

def topo_sort(G, no_incoming):
    waiting = list(no_incoming)
    in_edge = dict((k, set(v["parents"]))
        for k, v in G.items())
    sortd = []
    while waiting:
        nxt = waiting.pop(0)
        sortd.append(nxt)
        for c in G[nxt]["children"]:
            in_edge[c].remove(nxt)
            if not in_edge[c]:
                waiting.append(c)

    cycle_in = dict((k, v) for k, v in in_edge.items() if len(v))
    if cycle_in:
        raise NotImplementedError("input graph had cycles, cannot handle")

    for i, k in enumerate(sortd):
        G[k]["sort"] = i
    
    return G

def make_graph():
    G, no_incoming = synset_graph()
    print("Wordnet synset graph: {} nodes".format(len(G)))
    G, no_incoming = cleanup(G, no_incoming)
    print("After cleanup: {} nodes".format(len(G)))
    G = topo_sort(G, no_incoming)
    return G

if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument('filenames', nargs=argparse.REMAINDER)
    args = p.parse_args()

    if len(args.filenames):
        with open(args.filenames[0], "w") as f:
            G = make_graph()
            json.dump(G, f, indent=2)
    else:
        p.print_help()
