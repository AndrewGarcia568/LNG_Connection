# -*- coding: utf-8 -*-
"""
Created on Wed June 05 10:53:55 2024

@author: Micah Angelo Bacani
"""

import requests
import csv

# initialize global variables
base_url = "https://lngconnectionapi.cheniere.com/api/Capacity/GetCapacity?tspNo=200&cycleId=0&locationId=0&beginDate="
header_info = []
column_headers = []
column_headers_keys = []
rows = []
key_list = []

# get input date
print ("Please enter the gas day you want data from.")
day = input("Day (dd): ")
month = input("Month (mm): ")
year = input("Year (yyyy): ")
url = base_url + month + '/' + day + '/' + year

# get json through xhr mimic
response = requests.get(url)

# parse as dict object
data = response.json()

# check if data is retrieved
if data["report"] == []:
    print ("Unable to retrieve data. Check the date entered and make sure the format is correct and the date is valid (up to current day only).")
    exit()

# put keys in a list
for key in data["report"][0]:
    key_list.append(key)

# extract header data
header_info.append("TSP: ")
header_info.append(data["report"][0][key_list[0]])
header_info.append("TSP Name: ")
header_info.append(data['report'][0][key_list[1]])
header_info.append("Cycle: ")
header_info.append(data['report'][0][key_list[2]])
header_info.append("Meas Basis: ")
header_info.append(data['report'][0][key_list[11]])
header_info.append("Post Date and Time: ")
header_info.append(data['report'][0][key_list[3]])
header_info.append("EFF Gas Day and Time: ")
header_info.append(data['report'][0][key_list[4]])

# construct column headers
column_headers.append("Loc")
column_headers.append("Loc Name")
column_headers.append("Loc Purp Desc")
column_headers.append("Loc/QTI")
column_headers.append("All Qty Available?")
column_headers.append("IT")
column_headers.append("Design Capacity")
column_headers.append("Operating Capacity")
column_headers.append("Total Sched Quantity")
column_headers.append("Operationally Available Capacity")
column_headers.append("Flow Ind")

# extract column headers keys
for i in range (7, 19):
    if key_list[i] != "meaS_BASIS":     
        column_headers_keys.append(key_list[i])

# extract table data
for i in data['report']:
    row_holder = []
    for j in column_headers_keys:
        row_holder.append(i[j])
    rows.append(row_holder)

#writing to csv
with open('CreoleTrail-OperationallyAvailable-' + month + '-' + day + '-' + year + ".csv", 'w', encoding = 'UTF8') as f:
    writer = csv.writer(f)
    writer.writerow(header_info)
    writer.writerow(column_headers)
    for i in rows:
        writer.writerow(i)
