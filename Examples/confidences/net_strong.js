// Strong-vs-weak contest at one atom: 0.9 for, 0.3 against.
// gk answers p(a) with (.6, 0, .3, .1): for .6, conflict .3 and
// ignorance .1 (the four shares sum to 1).
//
// Run: ./bin/gk Examples/confidences/net_strong.js

[
{"@confidence": 0.9, "@logic": ["p","a"]},
{"@confidence": 0.3, "@logic": ["-p","a"]},
{"@question": ["p","a"]}
]
