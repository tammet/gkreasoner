[
  ["heavy_block", "A"],
  ["heavy_block", "B"],
  [["heavy_block", "?:X"], "=>", [["located_on", "?:X", "table"], "|",
    ["$block", 0, ["$not", ["located_on", "?:X", "table"]]]]],
  ["-located_on", "A", "table"],
  ["has_color", "B", "red"],
  {"@question": ["located_on", "B", "table"]}
]
