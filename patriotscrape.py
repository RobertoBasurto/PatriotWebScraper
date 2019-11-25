#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import selenium as selenium
import time
import re

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
student_serv = browser.find_element_by_partial_link_text('Student Services')
student_serv.click()
time.sleep(1)

registration = browser.find_element_by_partial_link_text('Registration')
registration.click()
class_search = browser.find_element_by_partial_link_text('Search for Classes')
class_search.click()

#drop down "Search by Term"
#search page source to find the option@value for the user-specified term
season = "spring"
year = "2020"
optionvalue = 0
src = browser.page_source.split("\n")
for line in src:
    if season.lower() in line.lower():
        if year in line:
            optionvalue = (re.findall(r'\"(.+?)\"',line))[0]
            print("value = " + optionvalue)

select_term = browser.find_element_by_xpath('//option[@value="'+optionvalue+'"]')
select_term.click()
#submit term
submit_term = browser.find_element_by_xpath('//input[@value="Submit"]')
submit_term.click()

#select subject
sub = "CS"
subject = browser.find_element_by_xpath("//option[@value='"+sub+"']")
subject.click()
course_search = browser.find_element_by_xpath("//input[@value='Course Search']")
course_search.click()


#first view
#view sections of each class using this full xpath format: /html/body/div[4]/table[2]/tbody/tr[i]/td[3]/form/input[30] where i = 3-15
rows = [] #list of every class' row info
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
        if "worksheet" in ele.text or "simulta" in ele.text:
            continue
        else:
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
""" browser.back()

cs = browser.find_element_by_xpath('/html/body/div[4]/form/table[1]/tbody/tr/td[2]/select/option[34]')
cs.click()
course_search1 = browser.find_element_by_xpath('/html/body/div[4]/form/input[17]')
course_search1.click()
#first class = /html/body/div[4]/table[2]/tbody/tr[3]/td[3]/form/input[30]
#last class (499) = /html/body/div[4]/table[2]/tbody/tr[30]/td[3]/form/input[30]

for n in range(3,31):
    time.sleep(1)
    try:
        view_section1 = browser.find_element_by_xpath(f"/html/body/div[4]/table[2]/tbody/tr[{i}]/td[3]/form/input[30]")
    except selenium.common.exceptions.NoSuchElementException:
        print("That shit don't exist!")
    view_section1.click()
    time.sleep(1)
    html = browser.page_source
    soup=BeautifulSoup(html)
for ele in soup.find_all("td",class_="dddefault"):
    row = row + ele.text + "$"
    print(ele.text+" ",end="")
    if line % 18 ==0:
        print("\n")
        rows.append(row)
        row = ""
    line+=1
print(rows) """










