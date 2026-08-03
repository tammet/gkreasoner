#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import numpy as np
from queue import Queue

def bfs(s1, s2, G):
    frontier = Queue()
    frontier.put(s1)
    upper_lim = G[s2]["sort"]
    while not frontier.empty():
        n = frontier.get()
        for p in G[n]["parents"]:
            # BFS can do exit on expand
            if p == s2:
                return True
            if G[p]["sort"] > upper_lim:
                frontier.put(p)
    return False

def is_more_general(s1, s2, G, algo=bfs):
    """is s2 more general than s1?
    s1, s2: synset names in WordNet"""
    if s1 not in G or s2 not in G:
        return False
    if G[s1]["sort"] <= G[s2]["sort"]:
        return False
    else:
        return algo(s1, s2, G)

def load_graph(f):
    return json.load(f)

def array_pack(G):
    """Pack graph as array
       for fast lookup in C code"""
    idmap = []
    packarr = []
    idx = len(G) + 1
    revlookup = dict((v["sort"], k) for k, v in G.items())
    for i in range(len(revlookup)):
        pmap = [idmap[G[p]["sort"]]
            for p in G[revlookup[i]]["parents"]]
        l = len(pmap)
        packarr.extend([l] + pmap)
        idmap.append(idx)
        idx += l + 1
    return [len(G)] + idmap + packarr

def save_array(f, packed):
    f.write("{:d}\n".format(len(packed)))
    for v in packed:
        f.write("{:d}\n".format(v))
    
if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument('-p', type=str, default="",
        help="packed array output filename")
    p.add_argument('filenames', nargs=argparse.REMAINDER)
    args = p.parse_args()

    if args.p and len(args.filenames):
        G = None
        with open(args.filenames[0]) as f:
            G = load_graph(f)
        if G:
            packed = array_pack(G)
            with open(args.p, "w") as f:
                save_array(f, packed)
    else:
        p.print_help()
