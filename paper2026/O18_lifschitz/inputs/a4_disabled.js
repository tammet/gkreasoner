[
  ["heavy_block", "A"],
  ["heavy_block", "B"],
  [[["heavy_block", "?:X"], "&", ["?:X", "!=", "A"]], "=>",
    [["located_on", "?:X", "table"], "|",
     ["$block", 0, ["$not", ["located_on", "?:X", "table"]]]]],
  ["-located_on", "A", "table"],
  ["B", "!=", "A"],
  {"@question": ["located_on", "B", "table"]}
]
