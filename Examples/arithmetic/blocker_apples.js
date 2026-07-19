[
  {
    "@name": "apples_bird",
    "@confidence": 0.8,
    "@logic": [["!=", ["$sum", "?:X", 2], 10], ["bird", "?:X"]]
  },
  {
    "@name": "bird_flies",
    "@confidence": 0.9,
    "@logic": [["-bird", "?:X"], ["flies", "?:X"], ["$block", 1, ["penguin", "?:X"]]]
  },
  {"@name": "penguin_8", "@confidence": 0.7, "@logic": ["penguin", 8]},
  {"@role": "question", "@logic": ["flies", "?:X"]}
]
