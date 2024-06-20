# -*- coding: utf-8 -*-
"""
Created on Wed June 05 10:53:55 2024

@author: Micah Angelo Bacani
"""

import requests
import pandas as pd

# initialize global variables
base_url = "https://lngconnectionapi.cheniere.com/api/Capacity/GetCapacity?tspNo=200&cycleId=0&locationId=0&beginDate="
column_headers_keys = []
key_list = []

# get input date
print ("Please enter the gas day you want data from.")
day = input("Day (dd): ")
month = input("Month (mm): ")
year = input("Year (yyyy): ")
url = base_url + month + '/' + day + '/' + year

# get json through xhr mimic
response = requests.get(url)

# parse as json object
data = response.json()

#parse as pandas dataframe
df = pd.DataFrame.from_records(data["report"])

# check if data is retrieved
if data["report"] == []:
    print ("Unable to retrieve data. Check the date entered and make sure the format is correct and the date is valid (up to current day only).")
    exit()

# put keys in a list
for key in data["report"][0]:
    key_list.append(key)

# getting header data
header_keys = key_list[0:5]
header_keys.append(key_list[11])
header_data = df[header_keys][0:1]
header_data.to_csv('CreoleTrail-OperationallyAvailable-' + month + '-' + day + '-' + year + '.csv', index = False)

# extract table column keys
for i in range (7, 19):
    if key_list[i] != "meaS_BASIS":     
        column_headers_keys.append(key_list[i])

# getting table data
table_data = df[column_headers_keys]
table_data.to_csv('CreoleTrail-OperationallyAvailable-' + month + '-' + day + '-' + year + '.csv', mode = 'a')
