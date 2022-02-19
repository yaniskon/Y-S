from Bol_access_token import get_token
import requests
import json
import time
import pandas as pd
import os
import pymongo
import mysql.connector



def ship_order_item():
  url = 'https://api.bol.com/retailer/orders/shipment'
  headers = {
  'Accept': 'application/vnd.retailer.v6+json',
  'Content-Type': 'application/vnd.retailer.v6+json',
  'Authorization': 'Bearer ' + get_token() 
  }



  payload = json.dumps({
  "orderItems": [
    {
      "orderItemId": "2852546784"
    }
  ],
  "shipmentReference": "FA-0000628",
  "shippingLabelId":"fc2f4704-9f33-4ef0-90a0-f7c170e3c100"})
  response = requests.request("PUT", url, headers=headers, data=payload)

  print(response.text)

 
def get_process():
  url = "https://api.bol.com/retailer/process-status/40420863674"

  headers = {
  'Accept': 'application/vnd.retailer.v6+json',
  'Content-Type': 'application/vnd.retailer.v6+json',
  'Authorization': 'Bearer ' + get_token() 
  }
  payload = {}
  time.sleep(3)   
  get_process_response = requests.request("GET", url , headers=headers, data=payload)
  response = json.loads(get_process_response.text)
  print(response)


get_process()

def get_shipping_label():
    url = 'https://api.bol.com/retailer/shipments/' + str(1035630028)
        
    payload={}
    headers = {
    'Accept': 'application/vnd.retailer.v6+json',   'Authorization': 'Bearer ' + get_token() 
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)



# ship_order_item()
# get_shipping_label()
# https://api.bol.com/retailer/process-status/40419579086
# https://api.bol.com/retailer/process-status/40419706959
# ship_order_item(2852546784)