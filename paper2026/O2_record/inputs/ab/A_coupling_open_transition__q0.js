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
     3,
     [
      "$not",
      [
       "f"
      ]
     ]
    ]
   ]
  ],
  "@confidence": 0.8
 },
 {
  "@logic": [
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
  ],
  "@confidence": 0.5
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
    "f"
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
      "f"
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
