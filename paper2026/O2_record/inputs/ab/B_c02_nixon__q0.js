[
 {
  "@logic": [
   "quaker",
   "nixon"
  ]
 },
 {
  "@logic": [
   "republican",
   "nixon"
  ]
 },
 {
  "@logic": [
   [
    "quaker",
    "?:X"
   ],
   "=>",
   [
    [
     "pacifist",
     "?:X"
    ],
    "|",
    [
     "$block",
     1,
     [
      "$not",
      [
       "pacifist",
       "?:X"
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
    "republican",
    "?:X"
   ],
   "=>",
   [
    [
     "-pacifist",
     "?:X"
    ],
    "|",
    [
     "$block",
     1,
     [
      "$not",
      [
       "-pacifist",
       "?:X"
      ]
     ]
    ]
   ]
  ],
  "@confidence": 0.8
 },
 {
  "@question": [
   "pacifist",
   "nixon"
  ]
 }
]
