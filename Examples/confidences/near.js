
// a chain of objects near each other

[
  
  {"@logic":["near","c1","c2"]},
  {"@logic":["near","c2","c3"]},
  {"@logic":["near","c3","c4"]},
  {"@logic":["near","c4","c5"]},
  {"@logic":["near","c5","c6"]},
  {"@logic":["near","c6","c7"]},
  {"@logic":["near","c7","c8"]},
  {"@logic":["near","c8","c9"]},
  {"@logic":["near","c9","c10"]},

  // add the following additional information
  // for seeing the effects of cumulating information

  // {"@logic":["near","c1","c5"], "@confidence": 50}, 
  // {"@logic":["near","c5","c10"], "@confidence": 50},
 
  {"@logic":[["-near","?:X","?:Y"],["-near","?:Y","?:Z"],["near","?:X","?:Z"]],
   "@confidence": 90},

  {"@question": ["near","c1","c10"]}

]
  
      