[
  ["heavy_block", "A"],
  [["heavy_block", "?:X"], "=>", [["located_on", "?:X", "table"], "|",
    ["$block", 0, ["$not", ["located_on", "?:X", "table"]]]]],
  ["-located_on", "A", "table"],
  {"@logic": [["forall", ["X"],
    [[["heavy_block", "X"], "&", ["X", "!=", "A"]], "=>", ["located_on", "X", "table"]]],
    "<=>", ["Q"]]},
  {"@question": ["Q"]}
]
