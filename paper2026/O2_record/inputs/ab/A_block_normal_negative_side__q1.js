[
 {
  "@logic": [
   "p"
  ],
  "@confidence": 0.6
 },
 {
  "@logic": [
   "q"
  ],
  "@confidence": 0.5
 },
 {
  "@logic": [
   [
    "q"
   ],
   "=>",
   [
    "p"
   ]
  ],
  "@confidence": 0.7
 },
 {
  "@logic": [
   [
    "p"
   ],
   "=>",
   [
    "q"
   ]
  ],
  "@confidence": 0.6
 },
 {
  "@logic": [
   [
    "-p"
   ],
   "|",
   [
    "$block",
    1,
    [
     "$not",
     [
      "-p"
     ]
    ]
   ]
  ],
  "@confidence": 0.4
 },
 {
  "@logic": [
   [
    [
     "p"
    ],
    "&",
    [
     "q"
    ]
   ],
   "=>",
   [
    "h"
   ]
  ]
 },
 {
  "@question": [
   "q"
  ]
 }
]
