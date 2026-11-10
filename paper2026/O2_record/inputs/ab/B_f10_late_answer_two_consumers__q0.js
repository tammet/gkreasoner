[
 {
  "@logic": [
   "s",
   "a"
  ],
  "@confidence": 0.5
 },
 {
  "@logic": [
   [
    "s",
    "?:X"
   ],
   "=>",
   [
    "r",
    "?:X"
   ]
  ]
 },
 {
  "@logic": [
   [
    "r",
    "?:X"
   ],
   "=>",
   [
    "q1"
   ]
  ],
  "@confidence": 0.6
 },
 {
  "@logic": [
   [
    "r",
    "?:X"
   ],
   "=>",
   [
    "q2"
   ]
  ],
  "@confidence": 0.7
 },
 {
  "@logic": [
   [
    [
     "q1"
    ],
    "&",
    [
     "q2"
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
   "h"
  ]
 }
]
