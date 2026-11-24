[
 {
  "@name": "sent_S1",
  "@logic": [
   [
    "-isa",
    "bear",
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
  "@nl": "Bears eat berries."
 },
 {
  "@name": "sent_S1",
  "@logic": [
   [
    "-isa",
    "bear",
    "?:X"
   ],
   [
    "has type",
    [
     "sk0",
     "?:X"
    ],
    "eat",
    [
     "$ctxt",
     "?:Fv4",
     "?:Fv3",
     "?:Fv1",
     "?:Fv2"
    ]
   ]
  ],
  "@nl": "Bears eat berries."
 },
 {
  "@name": "sent_S1",
  "@logic": [
   [
    "-isa",
    "bear",
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
  "@nl": "Bears eat berries."
 },
 {
  "@name": "sent_S1",
  "@logic": [
   [
    "-isa",
    "bear",
    "?:X"
   ],
   [
    "isa",
    "berry",
    [
     "sk1",
     "?:X"
    ]
   ]
  ],
  "@nl": "Bears eat berries."
 },
 {
  "@name": "sent_S1",
  "@logic": [
   [
    "-isa",
    "bear",
    "?:X"
   ],
   [
    "has target",
    [
     "sk0",
     "?:X"
    ],
    [
     "sk1",
     "?:X"
    ],
    [
     "$ctxt",
     "?:Fv4",
     "?:Fv3",
     "?:Fv1",
     "?:Fv2"
    ]
   ]
  ],
  "@nl": "Bears eat berries."
 },
 {
  "@name": "sent_S1",
  "@logic": [
   [
    "-isa",
    "bear",
    "?:X"
   ],
   [
    "typical",
    [
     "sk0",
     "?:X"
    ],
    [
     "$ctxt",
     "?:Fv4",
     "?:Fv3",
     "?:Fv1",
     "?:Fv2"
    ]
   ],
   [
    "$block",
    [
     "$",
     "bear",
     1
    ],
    [
     "$not",
     [
      "typical",
      [
       "sk0",
       "?:X"
      ],
      [
       "$ctxt",
       "?:Fv4",
       "?:Fv3",
       "?:Fv1",
       "?:Fv2"
      ]
     ]
    ]
   ]
  ],
  "@confidence": 0.98,
  "@nl": "Bears eat berries."
 },
 {
  "@name": "sent_S2",
  "@logic": [
   [
    "-isa",
    "baby bear",
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
    "eat",
    [
     "$ctxt",
     "?:Fv8",
     "?:Fv7",
     "?:Fv5",
     "?:Fv6"
    ]
   ],
   [
    "-has actor",
    "?:E",
    "?:X",
    [
     "$ctxt",
     "?:Fv8",
     "?:Fv7",
     "?:Fv5",
     "?:Fv6"
    ]
   ],
   [
    "-isa",
    "berry",
    "?:Y"
   ],
   [
    "-has target",
    "?:E",
    "?:Y",
    [
     "$ctxt",
     "?:Fv8",
     "?:Fv7",
     "?:Fv5",
     "?:Fv6"
    ]
   ],
   [
    "-typical",
    "?:E",
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
     "baby bear",
     4
    ],
    [
     "typical",
     "?:E",
     [
      "$ctxt",
      "?:Fv8",
      "?:Fv7",
      "?:Fv5",
      "?:Fv6"
     ]
    ]
   ]
  ],
  "@confidence": 0.98,
  "@nl": "Baby bears do not eat berries."
 },
 {
  "@name": "sent_S3",
  "@logic": [
   "isa",
   "baby bear",
   "#:John 1"
  ],
  "@nl": "John 1 is a baby bear."
 },
 {
  "@name": "sent_S4",
  "@sourcetype": "question",
  "@logic": [
   [
    "-$defq0"
   ],
   [
    "isa",
    "activity",
    "sk2_activity"
   ]
  ],
  "@nl": "Does John 1 eat berries?"
 },
 {
  "@name": "sent_S4",
  "@sourcetype": "question",
  "@logic": [
   [
    "-$defq0"
   ],
   [
    "has type",
    "sk2_activity",
    "eat",
    [
     "$ctxt",
     "?:Fv14",
     "?:Fv13",
     "?:Fv11",
     "?:Fv12"
    ]
   ]
  ],
  "@nl": "Does John 1 eat berries?"
 },
 {
  "@name": "sent_S4",
  "@sourcetype": "question",
  "@logic": [
   [
    "-$defq0"
   ],
   [
    "has actor",
    "sk2_activity",
    "#:John 1",
    [
     "$ctxt",
     "?:Fv14",
     "?:Fv13",
     "?:Fv11",
     "?:Fv12"
    ]
   ]
  ],
  "@nl": "Does John 1 eat berries?"
 },
 {
  "@name": "sent_S4",
  "@sourcetype": "question",
  "@logic": [
   [
    "-$defq0"
   ],
   [
    "isa",
    "berry",
    "sk3_berry"
   ]
  ],
  "@nl": "Does John 1 eat berries?"
 },
 {
  "@name": "sent_S4",
  "@sourcetype": "question",
  "@logic": [
   [
    "-$defq0"
   ],
   [
    "has target",
    "sk2_activity",
    "sk3_berry",
    [
     "$ctxt",
     "?:Fv14",
     "?:Fv13",
     "?:Fv11",
     "?:Fv12"
    ]
   ]
  ],
  "@nl": "Does John 1 eat berries?"
 },
 {
  "@name": "sent_S4",
  "@sourcetype": "question",
  "@logic": [
   [
    "-$defq0"
   ],
   [
    "typical",
    "sk2_activity",
    [
     "$ctxt",
     "?:Fv14",
     "?:Fv13",
     "?:Fv11",
     "?:Fv12"
    ]
   ]
  ],
  "@nl": "Does John 1 eat berries?"
 },
 {
  "@name": "sent_S4",
  "@sourcetype": "question",
  "@logic": [
   [
    "-isa",
    "activity",
    "?:E"
   ],
   [
    "-has type",
    "?:E",
    "eat",
    [
     "$ctxt",
     "?:Fv14",
     "?:Fv13",
     "?:Fv11",
     "?:Fv12"
    ]
   ],
   [
    "-has actor",
    "?:E",
    "#:John 1",
    [
     "$ctxt",
     "?:Fv14",
     "?:Fv13",
     "?:Fv11",
     "?:Fv12"
    ]
   ],
   [
    "-isa",
    "berry",
    "?:Y"
   ],
   [
    "-has target",
    "?:E",
    "?:Y",
    [
     "$ctxt",
     "?:Fv14",
     "?:Fv13",
     "?:Fv11",
     "?:Fv12"
    ]
   ],
   [
    "-typical",
    "?:E",
    [
     "$ctxt",
     "?:Fv14",
     "?:Fv13",
     "?:Fv11",
     "?:Fv12"
    ]
   ],
   [
    "$defq0"
   ]
  ],
  "@nl": "Does John 1 eat berries?"
 },
 {
  "@name": "sent_S4",
  "@question": [
   "$defq0"
  ],
  "@nl": "Does John 1 eat berries?"
 },
 {
  "@name": "sent_S1",
  "@sourcetype": "populate",
  "@logic": [
   "isa",
   "bear",
   "$some_bear"
  ],
  "@nl": "[population: from input]"
 },
 {
  "@name": "sent_S1",
  "@sourcetype": "populate",
  "@logic": [
   "-isa",
   "bear",
   "$some_not_bear"
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
  "@name": "sent_S1",
  "@sourcetype": "populate",
  "@logic": [
   "isa",
   "berry",
   "$some_berry"
  ],
  "@nl": "[population: from input]"
 },
 {
  "@name": "sent_S1",
  "@sourcetype": "populate",
  "@logic": [
   "-isa",
   "berry",
   "$some_not_berry"
  ],
  "@nl": "[population: from input]"
 },
 {
  "@name": "sent_S2",
  "@sourcetype": "populate",
  "@logic": [
   "-isa",
   "baby bear",
   "$some_not_baby_bear"
  ],
  "@nl": "[population: from input]"
 },
 {
  "@name": "compound_sub",
  "@logic": [
   [
    "-isa",
    "baby bear",
    "?:X"
   ],
   [
    "isa",
    "bear",
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
    "bear",
    "?:X"
   ],
   [
    "isa",
    "baby bear",
    "?:X"
   ]
  ],
  "@confidence": 0.95,
  "@nl": "[generated: compound_comp]"
 }
]