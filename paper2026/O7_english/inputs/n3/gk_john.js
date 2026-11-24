[
 {
  "@name": "sent_S1",
  "@logic": [
   [
    "-isa",
    "bird",
    "?:X"
   ],
   [
    "isa",
    "activity",
    [
     "sk0",
     "?:X"
    ]
   ]
  ],
  "@nl": "Birds can fly."
 },
 {
  "@name": "sent_S1",
  "@logic": [
   [
    "-isa",
    "bird",
    "?:X"
   ],
   [
    "has type",
    [
     "sk0",
     "?:X"
    ],
    "fly",
    [
     "$ctxt",
     "?:Fv4",
     "?:Fv3",
     "?:Fv1",
     "?:Fv2"
    ]
   ]
  ],
  "@nl": "Birds can fly."
 },
 {
  "@name": "sent_S1",
  "@logic": [
   [
    "-isa",
    "bird",
    "?:X"
   ],
   [
    "has actor",
    [
     "sk0",
     "?:X"
    ],
    "?:X",
    [
     "$ctxt",
     "?:Fv4",
     "?:Fv3",
     "?:Fv1",
     "?:Fv2"
    ]
   ]
  ],
  "@nl": "Birds can fly."
 },
 {
  "@name": "sent_S1",
  "@logic": [
   [
    "-isa",
    "bird",
    "?:X"
   ],
   [
    "capability",
    [
     "sk0",
     "?:X"
    ]
   ],
   [
    "$block",
    [
     "$",
     "bird",
     1
    ],
    [
     "$not",
     [
      "capability",
      [
       "sk0",
       "?:X"
      ]
     ]
    ]
   ]
  ],
  "@confidence": 0.9,
  "@nl": "Birds can fly."
 },
 {
  "@name": "sent_S2",
  "@logic": [
   [
    "-isa",
    "bird",
    "?:X"
   ],
   [
    "isa",
    "activity",
    [
     "sk1",
     "?:X"
    ]
   ]
  ],
  "@nl": "Birds eat."
 },
 {
  "@name": "sent_S2",
  "@logic": [
   [
    "-isa",
    "bird",
    "?:X"
   ],
   [
    "has type",
    [
     "sk1",
     "?:X"
    ],
    "eat",
    [
     "$ctxt",
     "?:Fv8",
     "?:Fv7",
     "?:Fv5",
     "?:Fv6"
    ]
   ]
  ],
  "@nl": "Birds eat."
 },
 {
  "@name": "sent_S2",
  "@logic": [
   [
    "-isa",
    "bird",
    "?:X"
   ],
   [
    "has actor",
    [
     "sk1",
     "?:X"
    ],
    "?:X",
    [
     "$ctxt",
     "?:Fv8",
     "?:Fv7",
     "?:Fv5",
     "?:Fv6"
    ]
   ]
  ],
  "@nl": "Birds eat."
 },
 {
  "@name": "sent_S2",
  "@logic": [
   [
    "-isa",
    "bird",
    "?:X"
   ],
   [
    "typical",
    [
     "sk1",
     "?:X"
    ],
    [
     "$ctxt",
     "?:Fv8",
     "?:Fv7",
     "?:Fv5",
     "?:Fv6"
    ]
   ],
   [
    "$block",
    [
     "$",
     "bird",
     1
    ],
    [
     "$not",
     [
      "typical",
      [
       "sk1",
       "?:X"
      ],
      [
       "$ctxt",
       "?:Fv8",
       "?:Fv7",
       "?:Fv5",
       "?:Fv6"
      ]
     ]
    ]
   ]
  ],
  "@confidence": 0.98,
  "@nl": "Birds eat."
 },
 {
  "@name": "sent_S3",
  "@logic": [
   [
    "-isa",
    "baby bird",
    "?:X"
   ],
   [
    "-isa",
    "activity",
    "?:E"
   ],
   [
    "-has type",
    "?:E",
    "fly",
    [
     "$ctxt",
     "?:Fv12",
     "?:Fv11",
     "?:Fv9",
     "?:Fv10"
    ]
   ],
   [
    "-has actor",
    "?:E",
    "?:X",
    [
     "$ctxt",
     "?:Fv12",
     "?:Fv11",
     "?:Fv9",
     "?:Fv10"
    ]
   ],
   [
    "-capability",
    "?:E"
   ]
  ],
  "@nl": "Baby birds cannot fly."
 },
 {
  "@name": "sent_S4",
  "@logic": [
   "isa",
   "baby bird",
   "#:John 1"
  ],
  "@confidence": 0.6,
  "@nl": "John 1 is a baby bird."
 },
 {
  "@name": "sent_S5",
  "@logic": [
   "isa",
   "bird",
   "#:Mike 2"
  ],
  "@nl": "Mike 2 is a bird."
 },
 {
  "@name": "sent_S6",
  "@logic": [
   "isa",
   "bird",
   "#:Eve 3"
  ],
  "@nl": "Eve 3 is a bird."
 },
 {
  "@name": "sent_S7",
  "@logic": [
   "isa",
   "bird",
   "#:John 1"
  ],
  "@nl": "John 1 is a bird."
 },
 {
  "@name": "sent_S8",
  "@sourcetype": "question",
  "@logic": [
   [
    "-$defq0",
    "?:X"
   ],
   [
    "isa",
    "activity",
    [
     "sk2",
     "?:X"
    ]
   ]
  ],
  "@nl": "Which entity can fly and eat?"
 },
 {
  "@name": "sent_S8",
  "@sourcetype": "question",
  "@logic": [
   [
    "-$defq0",
    "?:X"
   ],
   [
    "has type",
    [
     "sk2",
     "?:X"
    ],
    "fly",
    [
     "$ctxt",
     "?:Fv28",
     "?:Fv27",
     "?:Fv21",
     "?:Fv22"
    ]
   ]
  ],
  "@nl": "Which entity can fly and eat?"
 },
 {
  "@name": "sent_S8",
  "@sourcetype": "question",
  "@logic": [
   [
    "-$defq0",
    "?:X"
   ],
   [
    "has actor",
    [
     "sk2",
     "?:X"
    ],
    "?:X",
    [
     "$ctxt",
     "?:Fv30",
     "?:Fv29",
     "?:Fv21",
     "?:Fv22"
    ]
   ]
  ],
  "@nl": "Which entity can fly and eat?"
 },
 {
  "@name": "sent_S8",
  "@sourcetype": "question",
  "@logic": [
   [
    "-$defq0",
    "?:X"
   ],
   [
    "capability",
    [
     "sk2",
     "?:X"
    ]
   ]
  ],
  "@nl": "Which entity can fly and eat?"
 },
 {
  "@name": "sent_S8",
  "@sourcetype": "question",
  "@logic": [
   [
    "-$defq0",
    "?:X"
   ],
   [
    "isa",
    "activity",
    [
     "sk3",
     "?:X"
    ]
   ]
  ],
  "@nl": "Which entity can fly and eat?"
 },
 {
  "@name": "sent_S8",
  "@sourcetype": "question",
  "@logic": [
   [
    "-$defq0",
    "?:X"
   ],
   [
    "has type",
    [
     "sk3",
     "?:X"
    ],
    "eat",
    [
     "$ctxt",
     "?:Fv34",
     "?:Fv33",
     "?:Fv21",
     "?:Fv22"
    ]
   ]
  ],
  "@nl": "Which entity can fly and eat?"
 },
 {
  "@name": "sent_S8",
  "@sourcetype": "question",
  "@logic": [
   [
    "-$defq0",
    "?:X"
   ],
   [
    "has actor",
    [
     "sk3",
     "?:X"
    ],
    "?:X",
    [
     "$ctxt",
     "?:Fv36",
     "?:Fv35",
     "?:Fv21",
     "?:Fv22"
    ]
   ]
  ],
  "@nl": "Which entity can fly and eat?"
 },
 {
  "@name": "sent_S8",
  "@sourcetype": "question",
  "@logic": [
   [
    "-$defq0",
    "?:X"
   ],
   [
    "typical",
    [
     "sk3",
     "?:X"
    ],
    [
     "$ctxt",
     "?:Fv38",
     "?:Fv37",
     "?:Fv21",
     "?:Fv22"
    ]
   ]
  ],
  "@nl": "Which entity can fly and eat?"
 },
 {
  "@name": "sent_S8",
  "@sourcetype": "question",
  "@logic": [
   [
    "-isa",
    "activity",
    "?:E1"
   ],
   [
    "-has type",
    "?:E1",
    "fly",
    [
     "$ctxt",
     "?:Fv42",
     "?:Fv41",
     "?:Fv21",
     "?:Fv22"
    ]
   ],
   [
    "-has actor",
    "?:E1",
    "?:X",
    [
     "$ctxt",
     "?:Fv44",
     "?:Fv43",
     "?:Fv21",
     "?:Fv22"
    ]
   ],
   [
    "-capability",
    "?:E1"
   ],
   [
    "-isa",
    "activity",
    "?:E2"
   ],
   [
    "-has type",
    "?:E2",
    "eat",
    [
     "$ctxt",
     "?:Fv48",
     "?:Fv47",
     "?:Fv21",
     "?:Fv22"
    ]
   ],
   [
    "-has actor",
    "?:E2",
    "?:X",
    [
     "$ctxt",
     "?:Fv50",
     "?:Fv49",
     "?:Fv21",
     "?:Fv22"
    ]
   ],
   [
    "-typical",
    "?:E2",
    [
     "$ctxt",
     "?:Fv52",
     "?:Fv51",
     "?:Fv21",
     "?:Fv22"
    ]
   ],
   [
    "$defq0",
    "?:X"
   ]
  ],
  "@nl": "Which entity can fly and eat?"
 },
 {
  "@name": "sent_S8",
  "@question": [
   "$defq0",
   "#:John 1"
  ],
  "@nl": "Can John 1 fly and eat?"
 },
 {
  "@name": "sent_S1",
  "@sourcetype": "populate",
  "@logic": [
   "-isa",
   "bird",
   "$some_not_bird"
  ],
  "@nl": "[population: from input]"
 },
 {
  "@name": "sent_S1",
  "@sourcetype": "populate",
  "@logic": [
   "isa",
   "activity",
   "$some_activity"
  ],
  "@nl": "[population: from input]"
 },
 {
  "@name": "sent_S1",
  "@sourcetype": "populate",
  "@logic": [
   "-isa",
   "activity",
   "$some_not_activity"
  ],
  "@nl": "[population: from input]"
 },
 {
  "@name": "sent_S3",
  "@sourcetype": "populate",
  "@logic": [
   "-isa",
   "baby bird",
   "$some_not_baby_bird"
  ],
  "@nl": "[population: from input]"
 },
 {
  "@name": "compound_sub",
  "@logic": [
   [
    "-isa",
    "baby bird",
    "?:X"
   ],
   [
    "isa",
    "bird",
    "?:X"
   ]
  ],
  "@nl": "[generated: compound_sub]"
 },
 {
  "@name": "compound_comp",
  "@logic": [
   [
    "-isa",
    "baby",
    "?:X"
   ],
   [
    "-isa",
    "bird",
    "?:X"
   ],
   [
    "isa",
    "baby bird",
    "?:X"
   ]
  ],
  "@confidence": 0.95,
  "@nl": "[generated: compound_comp]"
 },
 {
  "@name": "frm_syn",
  "@logic": [
   [
    "-has type",
    "?:E",
    "fly",
    "?:Fv53"
   ],
   [
    "has type",
    "?:E",
    "go",
    "?:Fv53"
   ]
  ],
  "@confidence": 0.52,
  "@nl": "[generated: frm_syn]"
 },
 {
  "@name": "pop_what",
  "@logic": [
   "isa",
   "baby bird",
   "$some_baby_bird"
  ],
  "@nl": "[population: class witnesses for what-query]"
 },
 {
  "@name": "pop_what",
  "@logic": [
   "isa",
   "bird",
   "$some_bird"
  ],
  "@nl": "[population: class witnesses for what-query]"
 }
]