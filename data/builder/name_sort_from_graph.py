#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json
from operator import itemgetter

def main():
  if len(sys.argv)<2:
    print("give the generality graph json file as argument")
    sys.exit(0)
  fname=sys.argv[1]  
  pairs=[]
  with open(fname) as json_file:
    fdata = json.load(json_file)
    for key in fdata:
      row=[key,fdata[key]["sort"]]
      pairs.append(row)
  pairs.sort(key=itemgetter(0))
  for el in pairs:
    print(el[0]+","+str(el[1]))
    #if ("," in el[0]):
    #  print(el[0])
    
main()  
  

  
  