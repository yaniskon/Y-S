from Bol_access_token import get_token
import requests
import json
import csv
import time
from pymongo import MongoClient
import pymongo
import pandas as pd

# Standard API parameters

url = "https://api.bol.com/retailer/offers/export"
payload=json.dumps({

"format": "CSV"

})
headers = {
   'Content-Type': 'application/vnd.retailer.v6+json',
  'Accept': 'application/vnd.retailer.v6+json',
  'Authorization': ''
}
headers['Authorization'] = 'Bearer ' + get_token() 


# Step 1
# First you need a request offers export which will start the creation of the offer export file. The output format of the export is a CSV file.

response = requests.request("POST", url , headers=headers, data=payload)
print(response.text)
response_dict = json.loads(response.text)
# print(response_dict)
processID = response_dict['processStatusId']
print(processID)
time.sleep(5)

# Step 2
# In the response to the previous request you can find the processID.

# Step 3
#Use the ID of the process status in a retrieve process status call. The use of the process status enables asynchronous processing of the request allowing you to check later if the request was processed correctly.
#If you successfully retrieve the process status, you should get a response with an entityId. The entityId will contain the ID needed to retrieve the export file.


payload= {}
headers = {
  'Accept': 'application/vnd.retailer.v6+json',
  'Authorization': ''
}
headers['Authorization'] = 'Bearer ' + get_token() 
process_url = "https://api.bol.com/retailer/process-status/" + processID 
response = requests.request("GET", process_url , headers=headers, data=payload)
response_dict = json.loads(response.text)
print(response_dict)
entityId = response_dict['entityId']
print("+================line46=================+")
print(entityId)


# Step 4
# Once the status field for the retrieve process status contains the value SUCCESS, you can use the entityId (which is the ID for the offer export) in combination with the retrieve offer export call. The response will be the requested CSV file which will contain both EANs and offerId’s which can be used to map to the offer IDs in your database.


url = "https://api.bol.com/retailer/offers/export/" + entityId

payload={}
headers = {
  'Content-Type': 'application/x-www-form-urlencoded',
  'Accept': 'application/vnd.retailer.v6+csv',
  'Authorization': 'Bearer '+ get_token()
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
print("+=====telos========+")

data = response.text
df = pd.DataFrame([x.split(',') for x in data.split('\n')])
print(df)
df.to_csv('offers.csv')

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["bol"]
myproducts = mydb["products"]

# response = requests.request("POST", url , headers=headers, data=payload)
# print(response)
# response_dict = json.loads(response.text)
# print(response_dict)