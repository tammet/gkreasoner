[
  ["heavy_block", "A"],
  ["heavy_block", "B"],
  ["heavy_block", "C"],
  [["heavy_block", "?:X"], "=>", [["located_on", "?:X", "table"], "|",
    ["$block", 0, ["$not", ["located_on", "?:X", "table"]]]]],
  [["-located_on", "A", "table"], ["-located_on", "B", "table"]],
  {"@question": ["located_on", "C", "table"]}
]
