[
  ["heavy_block", "A"],
  ["heavy_block", "B"],
  [["heavy_block", "?:X"], "=>", [["located_on", "?:X", "table"], "|",
    ["$block", 0, ["$not", ["located_on", "?:X", "table"]]]]],
  [["heavy_block", "?:X"], "=>", [["has_color", "?:X", "red"], "|",
    ["$block", 0, ["$not", ["has_color", "?:X", "red"]]]]],
  ["-located_on", "A", "table"],
  ["-has_color", "B", "red"],
  {"@question": [["located_on", "B", "table"], "&", ["has_color", "A", "red"]]}
]
