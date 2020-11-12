#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import selenium as selenium
import time
import re
import sys
import argparse
from datetime import datetime
import math
import plotly.graph_objects as go
import matplotlib


def timedayparse(time,day):
    t = time.split("-")
    start, end =t[0],t[1]
    if t[0] =='TBA':
        return "avoid"
    scheduletimestart = "07:00 am"
    schedulestart_timeobj = datetime.strptime(scheduletimestart, "%I:%M %p")
    beginning_timeobj=datetime.strptime(start,"%I:%M %p")
    end_timeobj = datetime.strptime(end,"%I:%M %p")
    classtime = end_timeobj - beginning_timeobj
    #time between the beginning of our schedule 7:00am and the beginning of the class
    schedule_classstart = beginning_timeobj-schedulestart_timeobj
    blocks_of_class = math.ceil(classtime.total_seconds()/60/15)
    blocks_from_start = math.ceil(schedule_classstart.total_seconds()/60/15)
    """     print(f"Number of minutes from 07:00am until the class start = {schedule_classstart.total_seconds()/60} minutes")
    print(f"Which means from the beginning of the schedule it takes ({math.ceil(schedule_classstart.total_seconds()/60/15)}) 15-minutes block until the class starts")

    print(f"This class is {int(classtime.total_seconds()/60)} minutes long")
    print(f"Which means the class covers ({math.ceil(classtime.total_seconds()/60/15)}) 15-minutes blocks")
    print("="*100) """
    for i in range(blocks_of_class+1):
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
            Z[i+blocks_from_start][days.index(day)] += 1                


parser = argparse.ArgumentParser()
parser.add_argument("username",help="PatriotWeb user",type=str)
parser.add_argument("password",help="PatriotWeb pass",type=str)
parser.add_argument("-m", '--major',help="list of major(s) codes (e.g. CS CYSE IT). https://catalog.gmu.edu/courses/",nargs="*",type=str,required=True)
parser.add_argument("-y","--year",help="Catalog year",type=str,required=True)
parser.add_argument("-s","--semester",help="Fall/Spring/Summer",type=str,required=True)
parser.add_argument("-o","--output",help="outfile of classdata",default="classdata.txt",type=str)

args = parser.parse_args()

browser = webdriver.Chrome("/home/nulltop/Downloads/chromedriver")

browser.get("https://patriotweb.gmu.edu/")
time.sleep(5)
button = browser.find_element_by_xpath("/html/body/table[2]/tbody/tr[2]/td[1]/table/tbody/tr[3]/td[2]/a/img")
button.click()

#submit user:pass and login
username=args.username
user_field = browser.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div/form/section[1]/div/input")
user_field.send_keys(username)
password=args.password
pass_field = browser.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div/form/section[2]/div/input")
pass_field.send_keys(password)
login = browser.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div/form/section[5]/input[4]")
login.click()
time.sleep(2)
if "invalid credentials" in browser.page_source:
    print("Check your username and password")
    sys.exit(0)
#go to Student Services
student_serv = browser.find_element_by_partial_link_text('Student Services')
student_serv.click()
#go to registration
registration = browser.find_element_by_partial_link_text('Registration')
registration.click()
#go to Search for Classes
class_search = browser.find_element_by_partial_link_text('Search for Classes')
class_search.click()
#drop down "Search by Term"
#search page source to find the option@value for the user-specified year and semester
season = args.semester
year = args.year
optionvalue = 0
src = browser.page_source.split("\n")
for line in src:
    if season.lower() in line.lower():
        if year in line:
            optionvalue = (re.findall(r'\"(.+?)\"',line))[0]
            print("value = " + optionvalue)
try:
    select_term = browser.find_element_by_xpath('//option[@value="'+optionvalue+'"]')
except:
    print("Make sure you spelled your semester (Fall/Spring/Summer) correctly")
    sys.exit(0)
select_term.click()
#submit year and semester
submit_term = browser.find_element_by_xpath('//input[@value="Submit"]')
submit_term.click()
rows = [] #list of every class' row info

print("AWEFAWEFAWEF")

print(args.major)
subjects = sorted(args.major,reverse=True)
print(subjects)
#go through every class of every major the user asked for in the -m flag
for sub in subjects:
    print("SUB:" + sub)
    subject = browser.find_element_by_xpath("//option[@value='"+sub+"']")
    print("SUB:" + sub)
    subject.click()
    course_search = browser.find_element_by_xpath("//input[@value='Course Search']")
    course_search.click()
    #first view
    #view sections of each class using this full xpath format: /html/body/div[4]/table[2]/tbody/tr[i]/td[3]/form/input[30] where i = 3-15
    for i in range(3,100):
        try:
            view_section = browser.find_element_by_xpath(f"/html/body/div[4]/table[2]/tbody/tr[{i}]/td[3]/form/input[30]")
        except selenium.common.exceptions.NoSuchElementException:
            print("That shit don't exist!")
            break
        view_section.click()
        time.sleep(1)
        html = browser.page_source
        soup = BeautifulSoup(html)
        line = 1
        row = ""
        for ele in soup.find_all("td",class_="dddefault"):
            if "worksheet" in ele.text or "simulta" in ele.text or ele.text=="C" or ele.text==chr(0xa0) :
                continue
            else:
                row = row + ele.text + "$"
                print(ele.text+" ",end="")
                if line % 17 ==0:
                    print("\n")
                    rows.append(row)
                    row = ""
                line+=1
        browser.back()
    browser.back()

f = open(args.output,"w")
for n in rows:
        x = n.split("$")
        print(x[1:3]+x[6:9])
        row=str((x[1:3]+x[6:9]))
        f.write(row+"\n")
f.close()

days=['M','T','W','R','F']  
# D = X-axis and T = Y-axis
D = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
T = ['7:00','7:15','7:30','7:45','8:00','8:15','8:30','8:45','9:00','9:15','9:30','9:45','10:00','10:15','10:30','10:45','11:00','11:15','11:30','11:45',
    '12:00','12:15','12:30','12:45','13:00','13:15','13:30','13:45','14:00','14:15','14:30','14:45','15:00','15:15','15:30','15:45','16:00','16:15','16:30',
    '16:45','17:00','17:15','17:30','17:45','18:00','18:15','18:30','18:45','19:00','19:15','19:30','19:45','20:00','20:15','20:30','20:45','21:00','21:15',
    '21:30','21:45','22:00','22:15','22:30','22:45','23:00']
# z[0]=7:00 ... z[61]=23:00
# z[n][0]=Monday ... z[n][4]=Friday
Z=[[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],
   [0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],
   [0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],
   [0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],
   [0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],
   [0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],
   [0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0]
  ]

#populate the Z array
f = open(args.output)
for rows in f:
    ele = rows.split(",")
    pretime = ele[-1]
    preday = ele[-2]
    time = pretime[pretime.index("'"):pretime.rfind("'")].strip()[1:]
    day = preday[preday.index("'"):pretime.rfind("'")].strip()[1:-1]
    try:
        timedayparse(time,day)
    except:
        print(f"The row [{rows}] was discarded")
        continue

#create heat map using 6 different color schemes for the user to choose from
colors = ['aggrnyl', 'algae','hot','mygbm','picnic','ylorrd']
for i in range(len(colors)):
    fig = go.Figure(data=go.Heatmap(
        x=D,
        y=T,
        z=Z,
        colorscale=colors[i]
        ))
    fig.update_layout(title=colors[i])
    fig.show()










