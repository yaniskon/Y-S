from Bol_access_token import get_token
import requests
import json
import time
from pymongo import MongoClient
import pymongo

# Standard API parameters

url = "https://api.bol.com/retailer/orders/"
payload={}
headers = {
  'Accept': 'application/vnd.retailer.v6+json',
  'Authorization': ''
}
headers['Authorization'] = 'Bearer ' + get_token() 
print(headers)
# Mongo db

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["bol"]
myship = mydb["shipments"]
myorder = mydb["orders"]

orders = []
mongoShipmentOrders = myship.find()
for i in mongoShipmentOrders:
    print(i["order"]["orderId"])
    orders.append(i["order"]["orderId"])

while orders != []:
    x = orders.pop()
    enrichedurl = url + x
    response = requests.request("GET", enrichedurl , headers=headers, data=payload)
    response_dict = json.loads(response.text)
    print(response_dict)
    break