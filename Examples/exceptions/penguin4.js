[

[["flyingpenguin", "?:X1"], "=>" ,["penguin", "?:X1"]],
[["penguin", "?:X1"], "=>" ,["bird", "?:X1"]],
[["bird", "?:X1"], "=>" ,["organism", "?:X1"]],
[["organism", "?:X1"], "=>" ,["object", "?:X1"]],

[["penguin", "?:X1"], "<=>" ,["penguin", ["father","?:X1"]]],
[["bird", "?:X1"], "<=>" ,["bird", ["father","?:X1"]]],
[["flyingpenguin", "?:X1"], "<=>" ,["flyingpenguin", ["father","?:X1"]]],

[["flyingpenguin", "?:X1"], "=>" ,[["fly", "?:X1"],"|",["$block",["$","penguin",3],["$not",["fly", "?:X1"]]]]],
[["penguin", "?:X1"], "=>" ,[["-fly", "?:X1"],"|",["$block",["$","penguin",2],["fly", "?:X1"]]]],
[["bird", "?:X1"], "=>" ,[["fly", "?:X1"],"|",["$block",["$","bird"],["$not",["fly", "?:X1"]]]]],
[["organism", "?:X1"], "=>" ,[["-fly", "?:X1"],"|",["$block",["$","organism"],["fly", "?:X1"]]]],


["flyingpenguin","fp"],
["penguin","p"],
["bird","b"],
["organism","o"],


//{"@question": ["fly",["father","?:X"]]}
//{"@question": ["fly","?:X"]}
{"@question": ["fly",["father", ["father","p"]]]}


]
