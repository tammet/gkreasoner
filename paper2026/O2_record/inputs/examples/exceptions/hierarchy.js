[
{"@logic": ["bird","b"]},
{"@logic": ["penguin","p"]},
{"@logic": ["object","o"]},

{"@logic": [["-penguin","?:X"],["bird","?:X"]]},
{"@logic": [["-bird","?:X"],["object","?:X"]]},

{"@logic": [["-penguin","?:X"],["-flies","?:X"]]},

{"@logic": [["-bird","?:X"],["flies","?:X"], ["$block", 3, ["$not", ["flies", "?:X"]]]]},
{"@logic": [["-object","?:X"],["-flies","?:X"], ["$block", 2, ["flies", "?:X"]]]},

{"@question": ["-flies","?:X"]}
]

/*

thing
bird
penguin

pingiivid on väga väike alamhulk lindudest  

eranditega reeglitel peaks olema hierarhia (mitte ehk puu, vaid 
tsükliteta suunatud graaf DAG)

   A  B
     X
   C  D
*/

