from Bol_access_token import get_token
import requests
import json
import csv
import time
from pymongo import MongoClient
import pymongo
import pandas as pd

# Standard API parameters

def request_offers_export():
  url = "https://api.bol.com/retailer/offers/export"
  payload=json.dumps({

"format": "CSV"

})
  headers = {
   'Content-Type': 'application/vnd.retailer.v6+json',
  'Accept': 'application/vnd.retailer.v6+json',
  'Authorization': 'Bearer ' + get_token()
}

  response = requests.request("POST", url , headers=headers, data=payload)
  print(response.text)
  response_dict = json.loads(response.text)
  processID = response_dict['processStatusId']
  time.sleep(5)
  return processID

def get_offers_export(processID):

  payload= {}
  headers = {
    'Accept': 'application/vnd.retailer.v6+json',
    'Authorization': 'Bearer ' + get_token() 
  }
  process_url = "https://api.bol.com/retailer/process-status/" + processID 
  response = requests.request("GET", process_url , headers=headers, data=payload)
  response_dict = json.loads(response.text)
  print(response_dict)
  entityId = response_dict['entityId']
  print("+================line46=================+")
  return entityId


def retrieve_an_offer_export_file(entityId):
  url = "https://api.bol.com/retailer/offers/export/" +entityId
  payload= {}
  headers = {
    'Accept': 'application/vnd.retailer.v6+csv',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': 'Bearer ' + get_token() 
  }
  response = requests.request("GET", url , headers=headers, data=payload)
  data = response.text
  df = pd.DataFrame([x.split(',') for x in data.split('\n')])
  print(df)
  df.to_csv('offers.csv')
  df = pd.read_csv('offers.csv')
  return df



def getting_offerId_data(df):

  myclient = pymongo.MongoClient("mongodb://localhost:27017/")
  mydb = myclient["bol"]
  myoffers = mydb["offers"]

  data = df.values.tolist()
  i = 2
  while i < len(data) -1:
    offerId = data[i][1]
    if myoffers.find_one({"offerId": offerId}) == None:
      url = 'https://api.bol.com/retailer/offers/' + offerId
      payload= {}
      headers = {
      'Accept': 'application/vnd.retailer.v6+json',
      'Authorization': 'Bearer ' + get_token() 
    }
      response = requests.request("GET", url, headers=headers, data=payload)

      response_dict = json.loads(response.text)
      myoffers.insert_one(response_dict)
    i += 1


df = pd.read_csv(r'C:\Users\konst\Documents\Y-S\Python\offers.csv')
print(df)
getting_offerId_data(df)
# getting_offerId_data(retrieve_an_offer_export_file(get_offers_export(request_offers_export())))
# Step 1
# First you need a request offers export which will start the creation of the offer export file. The output format of the export is a CSV file.

# print(response_dict)

# print(processID)


# Step 2
# In the response to the previous request you can find the processID.

# Step 3
#Use the ID of the process status in a retrieve process status call. The use of the process status enables asynchronous processing of the request allowing you to check later if the request was processed correctly.
#If you successfully retrieve the process status, you should get a response with an entityId. The entityId will contain the ID needed to retrieve the export file.



# Step 4
# Once the status field for the retrieve process status contains the value SUCCESS, you can use the entityId (which is the ID for the offer export) in combination with the retrieve offer export call. The response will be the requested CSV file which will contain both EANs and offerId’s which can be used to map to the offer IDs in your database.





# response = requests.request("POST", url , headers=headers, data=payload)
# print(response)
# response_dict = json.loads(response.text)
# print(response_dict)