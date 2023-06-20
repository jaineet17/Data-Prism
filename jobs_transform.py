#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 13:09:00 2022

@author: 
archoudh , dpatnaik , jaineets, namitb , niyatim

Only pandas needs to be imported for this file to run. 

This python file is needed to transform and clean the raw data and create a new file of cleaned data.
"""

import pandas as pd

df=pd.read_csv('jobs-raw.csv') #csv file for jobs raw data 

for i in range(len(df)):
    a=df[['Tags'][0]][i].replace("_",", ")
    df[['Tags'][0]][i]=a[1:]

# Basic data cleaning for column - Location
for i in range(len(df)):
    if (df['Location'][i] == 'Bangalore/Bengaluru' or df['Location'][i] == 'Bangalore/Bengaluru(BTM Layout)' or df['Location'][i] == 'Bangalore/Bengaluru(Electronics City Phase 1)' or df['Location'][i] == 'Bangalore/Bengaluru(Whitefield)' or df['Location'][i] == 'Bangalore/Bengaluru(Lalbagh Road)') :
        df['Location'][i] = 'Bangalore'
        
    if df['Location'][i] == 'Hyderabad/Secunderabad' or df['Location'][i] == 'Hyderabad/Secunderabad(Erragadda +1)':
        df['Location'][i] = 'Hyderabad'
    
    if df['Location'][i] == 'Gurgaon/Gurugram':
        df['Location'][i] = 'Gurgaon'
        
    if df['Location'][i] == 'Kochi/Cochin':
        df['Location'][i] = 'Kochi'
        
    if df['Location'][i] == 'remote':
        df['Location'][i] = 'Remote'

    if df['Location'][i] == 'Mumbai (All Areas)' or df['Location'][i] == 'Andheri' or df['Location'][i] == 'Navi Mumbai':
        df['Location'][i] = 'Mumbai'
        
    if (df['Location'][i] == 'Faridabad, Gurgaon/Gurugram, Delhi / NCR' or df['Location'][i] == 'Faridabad, Gurgaon/Gurugram') or df['Location'][i] == 'Noida, New Delhi, Gurgaon/Gurugram' or df['Location'][i] == 'Delhi NCR/Gurgaon/Gurugram' or df['Location'][i] == 'Delhi / NCR':
        df['Location'][i] = 'Delhi NCR'
        
    a=df['Location'][i].split(',')
    if len(a)>1:
        df['Location'][i] = 'Multiple'
        
    b=df['Location'][i].split('-')
    if b[0] == 'Hybrid ':
        df['Location'][i] = 'Hybrid'
    if b[0] == 'Temp. WFH ':
        df['Location'][i] = 'Temp. WFH'
        
        
#to identify all the unique locations in the dataset
#print(set(df['Location']))

final_df=df.drop(['Salary'], axis=1)  # because most comapnies havent disclosed the compensation.
final_df


final_df.to_csv('jobs_cleaned_data.csv')