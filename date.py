from datetime import date,timedelta
from datetime import datetime

date1 = (date.today())
date_new = str(date.today()).split('-')
#print date1
#print date_new[0]
Now = str(datetime.now().time()).split(':')
print Now[0]
#print Now[1]
#Hour = (int(Now[0]) - 6)
#Now1 = str(datetime.now().time())
#print Now1
#print Hour
Newdate = date_new[2] + date_new[1] + date_new[0][-2:]
Newtime = Now[0] + Now[1]

print Newdate
print Newtime

date2 = (date.today()+ timedelta(5))
print date2


new = date.today()+ timedelta(30)
print new
