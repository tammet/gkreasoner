[
 {
  "@logic": [
   [
    "p",
    "b"
   ],
   "|",
   [
    "$block",
    3,
    [
     "$not",
     [
      "p",
      "b"
     ]
    ]
   ]
  ],
  "@confidence": 0.7
 },
 {
  "@logic": [
   "p",
   "c"
  ],
  "@confidence": 0.4
 },
 {
  "@logic": [
   [
    "p",
    "?:X"
   ],
   "=>",
   [
    "q"
   ]
  ]
 },
 {
  "@logic": [
   [
    "q"
   ],
   "=>",
   [
    [
     "h"
    ],
    "|",
    [
     "$block",
     2,
     [
      "q"
     ]
    ]
   ]
  ],
  "@confidence": 0.9
 },
 {
  "@question": [
   "h"
  ]
 }
]
