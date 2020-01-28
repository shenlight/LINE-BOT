from datetime import datetime,timedelta
from time import time

d1 = datetime.strptime('1600','%H%M')
d2 = datetime.strptime('2200','%H%M')

d3 = d2-d1
print(d3)
"""
"""
d1 = datetime.strptime('1600','%H%M')
print(type(d1))
t2 = d1+timedelta(minutes=30)
t3 = datetime.strftime(d1,'%H%M')  
t4 = datetime.strftime(t2,'%H%M')
print(type(t4))

now = datetime.now().strftime('%H%M')
print(type(now))
print("-----")

if(t3<"1615"<t4):
    print("GOOD")

d = datetime.now()
d1 = d.strftime('%H:%M')
d2 = "17:31"
if(d1>d2):
    print('done')
else:
    print('no')

a = "17:00"
a1 = datetime.now()
a2 = str(a1.hour)
a3 = str(a1.minute)
print(a3)
a4 = a2+a3
print(a4)
a5 = "16:59"
if(a4==a5):
    print('done')
else:
    print('not')

now = datetime.now()+timedelta(hours = 8)
now = now.strftime('%H%M')
print(now)