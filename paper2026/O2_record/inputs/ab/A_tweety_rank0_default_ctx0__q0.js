[
 {
  "@logic": [
   "bird",
   "t"
  ]
 },
 {
  "@logic": [
   [
    "bird",
    "t"
   ],
   "=>",
   [
    [
     "flies",
     "t"
    ],
    "|",
    [
     "$block",
     0,
     [
      "$not",
      [
       "flies",
       "t"
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
    "bird",
    "t"
   ],
   "=>",
   [
    [
     "q"
    ],
    "|",
    [
     "$block",
     0,
     [
      "flies",
      "t"
     ]
    ]
   ]
  ],
  "@confidence": 0.9
 },
 {
  "@question": [
   "q"
  ]
 }
]
