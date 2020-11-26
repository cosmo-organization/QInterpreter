Include(`command.q`);
a=0  And 1 Or 1 And 4;
b=15+4;
c d = 4 5;
b=c;
c=c+a+c+d;
If b != 4:[
   b=c;
   f=44;
   b=(f+b)*5;
]
Elseif b > 8 Or b <8 And 0:[
   b = 9999999;
]
Elseif b ==4 And 0:[
   b = 999990000;
]
Else:[
   a=4444;
   c=990;
   f=99+a*c;
   a=f*f;
]
If a == 19356999316281:[
  a=9;
  small=(noo=99);
  List(small);
]