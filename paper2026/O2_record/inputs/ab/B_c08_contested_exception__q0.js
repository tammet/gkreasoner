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
  "@confidence": 0.7
 },
 {
  "@logic": [
   "-injured",
   "t"
  ],
  "@confidence": 0.3
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
