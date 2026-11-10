[
 {
  "@logic": [
   [
    "b"
   ],
   "|",
   [
    "$block",
    1,
    [
     "nb"
    ]
   ]
  ],
  "@confidence": 0.9
 },
 {
  "@logic": [
   [
    "b"
   ],
   "=>",
   [
    [
     "f"
    ],
    "|",
    [
     "$block",
     2,
     [
      "$not",
      [
       "f"
      ]
     ]
    ]
   ]
  ],
  "@confidence": 0.6
 },
 {
  "@logic": [
   [
    "-f"
   ],
   "|",
   [
    "$block",
    2,
    [
     "$not",
     [
      "-f"
     ]
    ]
   ]
  ],
  "@confidence": 0.7
 },
 {
  "@logic": [
   [
    "-f"
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
      "-f"
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
