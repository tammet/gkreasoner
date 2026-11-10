[
 {
  "@logic": [
   [
    "a"
   ],
   "|",
   [
    "$block",
    2,
    [
     "$not",
     [
      "a"
     ]
    ]
   ]
  ],
  "@confidence": 0.5
 },
 {
  "@logic": [
   [
    "-a"
   ],
   "|",
   [
    "$block",
    1,
    [
     "$not",
     [
      "-a"
     ]
    ]
   ]
  ],
  "@confidence": 0.1
 },
 {
  "@logic": [
   [
    "a"
   ],
   "=>",
   [
    [
     "q"
    ],
    "|",
    [
     "$block",
     2,
     [
      "a"
     ]
    ]
   ]
  ]
 },
 {
  "@question": [
   "q"
  ]
 }
]
