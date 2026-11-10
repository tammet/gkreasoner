[
{"@logic": ["quaker","n"]},
{"@logic": ["republican","n"]},

{"@logic": [["-quaker","?:X"],["pacifist","?:X"],["$block",2, ["$not", ["pacifist", "?:X"]]]]},
{"@logic": [["-republican","?:X"],["-pacifist","?:X"],["$block",2, ["pacifist", "?:X"]]]},

[["-pacifist","?:X"],["dislikeswar","?:X"]],

{"@question": ["dislikeswar","?:X"]}
]


