[
{"@logic": ["quaker","n"]},
{"@logic": ["republican","n"]},

{"@logic": [["-quaker","?:X"],["pacifist","?:X"],["$block",1, ["$not", ["pacifist", "?:X"]]]]},
{"@logic": [["-republican","?:X"],["-pacifist","?:X"],["$block",1, ["pacifist", "?:X"]]]},

{"@question": ["pacifist","n"]}
]

/*


1: ["pacifist","n"], ["$block",1, ["$not", ["pacifist", "?:n"]]]

2: ["-pacifist","n"],["$block",1, ["pacifist", "n"]]]},


----

1 is blocked by proving ["-pacifist","n"]:

   assuming ["pacifist","n"] gives ["$block",1, ["pacifist", "n"]]




*/