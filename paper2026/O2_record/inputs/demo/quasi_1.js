// we get a positive evidence with confidence 1 and 
// negative evidence with confidence 0.918144
// hence output is {"result": "evidence below limit"}
// since current limit for output is confidence 0.1
//
// run it like this to see details of both positive/negative
//
// ./gk -usekb quasi_1.js -confidence 0

[

{"@role": "assumption", "@logic": ["be","man","manx1"]},

{"@question": ["hasa","nipple","manx1"]}

]

/*
  {
    "@role": "axiom",
    "@confidence": 1.0,
    "@logic": [
      [
        "be",
        "?:X1",
        "man"
      ],
      "=>",
      [
        "hasa",
        "?:X1",
        "nipple"
      ]
    ]
  },
*/