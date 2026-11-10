[

[["flyingpenguin", "?:X1"], "=>" ,["penguin", "?:X1"]],
[["penguin", "?:X1"], "=>" ,["bird", "?:X1"]],
[["bird", "?:X1"], "=>" ,["organism", "?:X1"]],
[["organism", "?:X1"], "=>" ,["object", "?:X1"]],


[["flyingpenguin", "?:X1"], "=>" ,[["fly", "?:X1"],"|",["$block",6,["$not",["fly", "?:X1"]]]]],
[["penguin", "?:X1"], "=>" ,[["-fly", "?:X1"],"|",["$block",5,["fly", "?:X1"]]]],
[["bird", "?:X1"], "=>" ,[["fly", "?:X1"],"|",["$block",4,["$not", ["fly", "?:X1"]]]]],
[["organism", "?:X1"], "=>" ,[["-fly", "?:X1"],"|",["$block",3,["fly", "?:X1"]]]],


["flyingpenguin","fp"],
["penguin","p"],
["bird","b"],
["organism","o"],


{"@question": ["fly","?:X"]}


]
