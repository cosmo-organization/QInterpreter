a=5;
<#
name=`Hello`;
Id(55);
a=a+1;
Jump(55)Times(200000)Condition(a<100);
user = (id=8,m=9);
a=0;
Loop(a)Condition(a<100):[
  Print(key&`:`&value&Line);
  a=a+1;
  Loop(a)Condition(a<10):[
    Print(`Something is going good:`&key&`:`&value&Line);
    a=a+1;
  ]
]
Print(a&Line);#>
Max();
ToRadian(deg):[
  Return (deg*(22/7))/180;
];
ArcLength(deg&radius):[
  Return ToRadian(deg)*radius;
];
Perimeter(radius):[
  Return ArcLength(360&radius);
];
Print(Perimeter(700587877)&Line);
Max();