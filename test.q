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
]Else:[
  Print(`Wrong password@:`&entered_password&Space&`Not matched`&Line);
  Return 0;
]
Jump(20)Condition(a>0);