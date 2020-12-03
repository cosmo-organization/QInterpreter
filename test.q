a=DB.user;
Print(a&Line);
DB.user=`acccess`;
a=DB.user;
Print(a&Line);
Print(DB.user&Space&DB.password&Line);
BACKUP=`files`;
BACKUP.files=`*.png`;
BACKUP.myname=`donut`;
If 1:[
  BACKUP=`backup`;
]
Print(BACKUP&Space&BACKUP.files&Space&BACKUP.myname&Line);
user=(id=`Sonu`,pass=`@@$$`);
user.id=12345;
Print(user.id&Line);