[
 {
  "@logic": [
   "bird",
   "t"
  ]
 },
 {
  "@logic": [
   "injured",
   "t"
  ],
  "@confidence": 0.3
 },
 {
  "@logic": [
   "penguin",
   "t"
  ],
  "@confidence": 0.2
 },
 {
  "@logic": [
   [
    "bird",
    "?:X"
   ],
   "=>",
   [
    [
     [
      "flies",
      "?:X"
     ],
     "|",
     [
      "$block",
      0,
      [
       "injured",
       "?:X"
      ]
     ]
    ],
    "|",
    [
     "$block",
     0,
     [
      "penguin",
      "?:X"
     ]
    ]
   ]
  ],
  "@confidence": 0.9
 },
 {
  "@question": [
   "flies",
   "t"
  ]
 }
]
