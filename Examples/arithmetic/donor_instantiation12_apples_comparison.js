[
  [
    [
      "probe"
    ],
    [
      "-=",
      [
        "$sum",
        "?:X",
        2
      ],
      10
    ],
    [
      "-$less",
      "?:X",
      10
    ]
  ],
  {
    "@role": "question",
    "@logic": [
      "probe"
    ]
  }
]
