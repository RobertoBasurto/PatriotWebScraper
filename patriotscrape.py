    #!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import selenium as selenium
import time

browser = webdriver.Chrome("/home/nulltop/Downloads/chromedriver")

browser.get("https://patriotweb.gmu.edu/")
time.sleep(5)
button = browser.find_element_by_xpath("/html/body/table[2]/tbody/tr[2]/td[1]/table/tbody/tr[3]/td[2]/a/img")
button.click()

#submit user:pass and login
username="rbasurt2"
user_field = browser.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div/form/section[1]/div/input")
user_field.send_keys(username)
password="WwOQj2+slNQ:"
pass_field = browser.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div/form/section[2]/div/input")
pass_field.send_keys(password)
login = browser.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div/form/section[5]/input[4]")
login.click()

#go to class search
student_serv = browser.find_element_by_xpath("/html/body/div[4]/table[1]/tbody/tr[2]/td[2]/a")
student_serv.click()
time.sleep(1)
registration = browser.find_element_by_xpath("/html/body/div[4]/table[1]/tbody/tr[2]/td[2]/a")
registration.click()
class_search = browser.find_element_by_xpath("/html/body/div[4]/table[1]/tbody/tr[4]/td[2]/a")
class_search.click()

#drop down "Search by Term"
select_term = browser.find_element_by_xpath("/html/body/div[4]/form/table[1]/tbody/tr/td/select/option[2]")
select_term.click()
submit = browser.find_element_by_xpath("/html/body/div[4]/form/input[3]")
submit.click()

#select CYSE
cyse = browser.find_element_by_xpath("/html/body/div[4]/form/table[1]/tbody/tr/td[2]/select/option[41]")
cyse.click()
course_search = browser.find_element_by_xpath("/html/body/div[4]/form/input[17]")
course_search.click()


#first view
#view sections of each class using this full xpath format: /html/body/div[4]/table[2]/tbody/tr[i]/td[3]/form/input[30] where i = 3-15
rows = [] #list of every class' row info
for i in range(3,17):
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
        row = row + ele.text + "$"
        print(ele.text+" ",end="")
        if line % 18 ==0:
            print("\n")
            rows.append(row)
            row = ""
        line+=1
    print(rows)

    browser.back()



f = open("ClassData.txt","w")
for n in rows:
        x = n.split("$")
        print(x[2:4]+x[7:10])
        row=str((x[2:4]+x[7:10]))
        f.write(row+"\n")


browser.back()
#/html/body/div[4]/table[2]/tbody/tr[30]/td[3]/form/input[30]
cs = browser.find_element_by_xpath('/html/body/div[4]/form/table[1]/tbody/tr/td[2]/select/option[34]')
cs.click()
course_search = browser.find_element_by_xpath('/html/body/div[4]/form/input[17]')
course_search.click()
rows = [] #list of every class' row info
for i in range(3,31):
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
        row = row + ele.text + "$"
        print(ele.text+" ",end="")
        if line % 18 ==0:
            print("\n")
            rows.append(row)
            row = ""
        line+=1
    print(rows)
    browser.back()

f = open("ClassData.txt","a")
for n in rows:
        x = n.split("$")
        print(x[2:4]+x[7:10])
        f.write(row+"\n")


#NR	17225	CS	367	004	FX	4.000	Computer Systems and Programm	TR	09:00 am-10:15 am	68	0	68	N/A	Yutao Zhong (P)	01/21-05/13	IN 132	1
#NR	11184	CS	351	001	FX	3.000	Visual Computing	TR	10:30 am-11:45 am	60	0	60	0	Lap Fai Yu (P)	01/21-05/13	LH 2	1







