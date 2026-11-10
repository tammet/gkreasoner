[
 {
  "@logic": [
   "link",
   "a",
   "b"
  ],
  "@confidence": 0.9
 },
 {
  "@logic": [
   "link",
   "b",
   "c"
  ],
  "@confidence": 0.8
 },
 {
  "@logic": [
   "link",
   "c",
   "d"
  ],
  "@confidence": 0.7
 },
 {
  "@logic": [
   "link",
   "d",
   "e"
  ],
  "@confidence": 0.9
 },
 {
  "@logic": [
   "link",
   "e",
   "f"
  ],
  "@confidence": 0.6
 },
 {
  "@logic": [
   [
    "link",
    "?:X",
    "?:Y"
   ],
   "=>",
   [
    "path",
    "?:X",
    "?:Y"
   ]
  ],
  "@confidence": 0.9
 },
 {
  "@logic": [
   [
    [
     "link",
     "?:X",
     "?:Y"
    ],
    "&",
    [
     "path",
     "?:Y",
     "?:Z"
    ]
   ],
   "=>",
   [
    "path",
    "?:X",
    "?:Z"
   ]
  ],
  "@confidence": 0.8
 },
 {
  "@question": [
   "path",
   "a",
   "f"
  ]
 }
]
