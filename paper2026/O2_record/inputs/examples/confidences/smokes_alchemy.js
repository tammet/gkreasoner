/*

Smokes(Jerry)
Friends(Jerry, Elaine)
Friends(Elaine, George)

1.5 (!Smokes(x) v Cancer(x))
2.0 (!Friends(x,y) v !Friends(y,z) v Friends(x,z))
1.1 (!Smokes(x) v !Friends(x,y) v Smokes(y))

*/

[
{"@confidence":100,"@name":"a1","@logic": ["smokes","jerry"]},
{"@confidence":100,"@name":"a1","@logic": ["friends","jerry","elaine"]},
{"@confidence":100,"@name":"a1","@logic": ["friends","elaine","george"]},
{"@confidence":40,"@name":"a1","@logic": 
  [["-smokes","?:X"],["cancer","?:X"]] },
{"@confidence":100,"@name":"a1","@logic": 
  [["-friends","?:X","?:Y"],["-friends","?:Y","?:Z"],["friends","?:X","?:Z"]] },
{"@confidence":50,"@name":"a1","@logic": 
  [["-smokes","?:X"],["-friends","?:X","?:Y"],["smokes","?:Y"]] },
//{"@name":"q","@question": ["smokes","?:X"]}  
{"@name":"q","@question": ["cancer","?:X"]}
]