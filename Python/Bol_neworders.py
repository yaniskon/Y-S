from Bol_access_token import get_token
import requests
import json
import time
from pymongo import MongoClient
import pymongo

# Standard API parameters

url = "https://api.bol.com/retailer/orders"
payload={}
headers = {
  'Accept': 'application/vnd.retailer.v6+json',
  'Authorization': ''
}
headers['Authorization'] = 'Bearer ' + get_token() 


# Mongo db

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["bol"]
myorder = mydb["orders"]


page = 1
bool_results = True

while bool_results:  # We can paginate this API up until 3 months worth of shipments
    enrichedurl = url + f"?page={page}"
    response = requests.request("GET", enrichedurl , headers=headers, data=payload)
    response_dict = json.loads(response.text)

    # don't break bol
    rate_limit = response.headers["X-RateLimit-Remaining"]
    reset = response.headers["X-RateLimit-Reset"]
    if int(rate_limit) < 1:
        print("Good night!")
        time.sleep(int(reset))
        print("Back there again!")
    
    print(response.text)

    if response_dict != {}:
        pass
        # for neworder in response_dict['shipments']:
        #   #ship_results.append(shipment)
        #   print(shipment)
        #   if shipment.get("shipmentReference") is not None:
        #     if shipment["shipmentReference"] not in mycol.distinct("shipmentReference"):
        #       mycol.insert_one(shipment)
        #   else:
        #     pass
    else:
      bool_results = False
    page += 1