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
Quantum(a=90&b&d=70):[
  Global f=88;
];
Max();
Quantum(4&4+5);
Print(f&Line);