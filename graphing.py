#!/usr/bin/env python3

from datetime import datetime
import math

f = open("ClassData.txt","r")
#z[0]=7:00 ... z[61]=23:00
Z=[[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],
   [0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],
   [0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],
   [0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],
   [0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],
   [0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],
   [0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0]
  ]

days=['M','T','W','R','F']



def timedayparse(time,day):
    print(day)
    t = time.split("-")
    if t[0] =='TBA':
        return "avoid"
    scheduletimestart = "07:00 am"
    schedulestart_timeobj = datetime.strptime(scheduletimestart, "%I:%M %p")
    start, end =t[0],t[1]
    beginning_timeobj=datetime.strptime(start,"%I:%M %p")
    end_timeobj = datetime.strptime(end,"%I:%M %p")
    print(start,end)
    classtime = end_timeobj - beginning_timeobj
    #time between the beginning of our schedule 7:00am and the beginning of the class
    schedule_classstart = beginning_timeobj-schedulestart_timeobj
    blocks_of_class = math.ceil(classtime.total_seconds()/60/15)
    blocks_from_start = math.ceil(schedule_classstart.total_seconds()/60/15)

    print(f"Number of minutes from 07:00am until the class start = {schedule_classstart.total_seconds()/60} minutes")
    print(f"Which means from the beginning of the scheudle it takes ({math.ceil(schedule_classstart.total_seconds()/60/15)}) 15-minutes block until the class starts")

    print(f"This class is {int(classtime.total_seconds()/60)} minutes long")
    print(f"Which means the class covers ({math.ceil(classtime.total_seconds()/60/15)}) 15-minutes blocks")
    print("="*100)


    for i in range(blocks_of_class):
        if day == 'TR':
            firstday = day[0]
            secondday=day[1]
            Z[i+blocks_from_start][days.index(firstday)] += 1
            Z[i+blocks_from_start][days.index(secondday)] += 1
        elif day == 'MW':
            firstday = day[0]
            secondday = day[1]
            Z[i+blocks_from_start][days.index(firstday)] += 1
            Z[i+blocks_from_start][days.index(secondday)] += 1
        else:
            print("DEBUG:",end='')
            print(blocks_from_start,blocks_of_class,i,len(Z))
            Z[i+blocks_from_start][days.index(day)] += 1
        
    print(Z)
        
    




for rows in f:
    ele = rows.split(",")
    pretime = ele[-1]
    preday = ele[-2]
    time = pretime[pretime.index("'"):pretime.rfind("'")].strip()[1:]
    day = preday[preday.index("'"):pretime.rfind("'")].strip()[1:-1]
    timedayparse(time,day)

    


D = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
T = ['8:00','8:15','8:30','8:45','9:00','9:15','9:30','9:45','10:00','10:15','10:30','10:45','11:00','11:15','11:30','11:45','12:00','12:15','12:30','12:45','13:00','13:15','13:30','13:45','14:00','14:15','14:30','14:45','15:00','15:15','15:30','15:45','16:00','16:15','16:30','16:45','17:00','17:15','17:30','17:45','18:00','18:15','18:30','18:45','19:00','19:15','19:30','19:45','20:00','20:15','20:30','20:45','21:00','21:15','21:30','21:45','22:00','22:15','22:30','22:45','23:00']



import plotly.graph_objects as go
import matplotlib
fig = go.Figure(data=go.Heatmap(
    x=D,
    y=T,
    z=Z
    ))
fig.show()

