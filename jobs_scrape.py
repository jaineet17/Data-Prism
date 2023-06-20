#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 13:09:00 2022

@author: 
archoudh , dpatnaik , jaineets, namitb , niyatim

The purpose of this file is to scrape data from naukri.com, using selenium.

The below mentioned things are required to be imported to run this file.
"""

import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time,csv

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

#make an empty list
data = []
for i in range(1,31):
    #considering the url pattern of the website for every page
    url = "https://www.naukri.com/data-science-jobs-"+str(i)+"?k=data%20science" 
    driver.get(url)
    time.sleep(1)
    elts = driver.find_elements(By.XPATH, "//section[@class='listContainer fleft']//article")


    for elt in elts:
        try:
            title = elt.find_element(By.XPATH,".//a[@class='title fw500 ellipsis']").get_attribute('title').strip()
            link = elt.find_element(By.XPATH,".//a[@class='title fw500 ellipsis']").get_attribute('href').strip()

            yoe = elt.find_element(By.CLASS_NAME,"experience")
            yoe_2 = yoe.find_element(By.TAG_NAME,'span').text

            salary = elt.find_element(By.CLASS_NAME,"salary")
            salary_2 = salary.find_element(By.TAG_NAME,'span').text

            loc = elt.find_element(By.CLASS_NAME,"location")
            loc_2 = loc.find_element(By.TAG_NAME,'span').text

            jd = elt.find_element(By.CLASS_NAME,"job-description").text

            comp = elt.find_element(By.XPATH,".//div[@class='jobTupleHeader']")
            comp_2 = comp.find_element(By.CLASS_NAME,"companyInfo")
            comp_3 =comp_2.find_element(By.TAG_NAME,"a").get_attribute('title')

            tags = elt.find_element(By.XPATH,".//ul[@class='tags has-description']")
            tags_2 = tags.find_elements(By.TAG_NAME,"li")
            tags_3 = ""
            for i in tags_2:
                tags_3 = tags_3+"_"+(i.text)

            data.append([title,comp_3,loc_2,salary_2,jd,yoe_2,tags_3, link])
                
        except:
                continue

fields = ['Job Title','Company','Location','Salary','Requirements', 'Years of Experience','Tags','Link',]
filename = "jobs-raw.csv"

with open(filename, 'w') as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile)
    # writing the fields
    csvwriter.writerow(fields)
    # writing the data rows
    csvwriter.writerows(data)