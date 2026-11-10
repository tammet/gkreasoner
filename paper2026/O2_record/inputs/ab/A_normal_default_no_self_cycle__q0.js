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
  "@question": [
   "flies",
   "t"
  ]
 }
]
