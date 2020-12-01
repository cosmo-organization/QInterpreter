original_password=`pass@1234`;
entered_password=`pass@1234`;
stored_hash=Hash(original_password);
Print(`Stored Hash:`&Space&stored_hash&Line);
calculated_hash=Hash(entered_password);

If stored_hash == calculated_hash:[
  Print(`Password matched`&Line);
]
Else:[
  Print(`Password not matched!`&Line);
  Print(entered_password&Space&`is not a correct password!`&Line);
]
a=-100;
Id(20);
a=a-1;
If stored_hash == calculated_hash:[
  Print(entered_password&Space&`Matched`&Line);
  m=`Hookdown`;
  m.Replace(`H`)With(`D`);
  Print(m&Line);
]Else:[
  Print(`Wrong password@:`&entered_password&Space&`Not matched`&Line);
  Return 0;
]
Jump(20)Condition(a>0);
python_code="a=88\nprint(a+a)\nwhile True:\n\tprint('Milestone is used to create nothing')\n\tbreak";#Pure python code string
Execute(python_code);
python_code.Replace(`88`)With(`99`);
#Print(`Hello`);
Print(python_code&Line);
python_code.Replace(`=`)With(`!=`);
Print(python_code&Line);
data=python_code.Replace(`!=`)With(`~`);
Print(python_code&Line);
Print(data&Line);