from Bol_access_token import get_token
import requests
import json
import time
from pymongo import MongoClient
import pymongo

# Standard API parameters

def get_new_orders():
  url = "https://api.bol.com/retailer/orders"
  payload={}
  headers = {
  'Accept': 'application/vnd.retailer.v6+json',
  'Authorization': 'Bearer ' + get_token() 
  }
  response = requests.request("GET", url , headers=headers, data=payload)

  # don't break bol
  rate_limit = response.headers["X-RateLimit-Remaining"]
  reset = response.headers["X-RateLimit-Reset"]
  if int(rate_limit) < 1:
    print("Good night!")
    time.sleep(int(reset))
    print("Back there again!")
  
  response_dict = json.loads(response.text)
  global orders_list
  orders_list = response_dict['orders']
  #return orders_list # I dont understand why and if that is neccessary

def delivery_options(orderitemID):
  url = 'https://api.bol.com/retailer/shipping-labels/delivery-options'
  headers = {
  'Accept': 'application/vnd.retailer.v6+json',
  'Content-Type': 'application/vnd.retailer.v6+json',
  'Authorization': 'Bearer ' + get_token() 
  }
  payload = json.dumps({
  "orderItems": [
    {
      "orderItemId": orderitemID
    }
  ]
})

  delresponse = requests.request("POST", url , headers=headers, data=payload)
  return delresponse.text

get_new_orders()

if orders_list != []:
  for order in orders_list:
    print(order)
    print("+=================================================================+")
    orderItemId = order["orderItems"][0]["orderItemId"] # this support only single order 
    print(orderItemId)
    delivery_options(orderItemId)



# # Mongo db

# myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# mydb = myclient["bol"]
# myorder = mydb["orders"]


# new_orders = True

# while new_orders:  # We can paginate this API up until 3 months worth of shipments

#     # don't break bol
#     rate_limit = response.headers["X-RateLimit-Remaining"]
#     reset = response.headers["X-RateLimit-Reset"]
#     if int(rate_limit) < 1:
#         print("Good night!")
#         time.sleep(int(reset))
#         print("Back there again!")
    
#     #print(response.json())
#     response_dict = json.loads(response.text)
#     print("+=============================++++")
#     print(response_dict)
#     print("+=============================++++")
    
#     if response_dict != {}:
#       for x in response_dict['orders']:
#         print("+=======", x['orderId'], "=======", x['orderItems'][0]) # this [0] is for order that contain a single item
#         orderitemID = x['orderItems'][0]['orderItemId'] # this should contain the second order
#         payload2 = json.dumps({
#   "orderItems": [
#     {
#       "orderItemId": orderitemID
#     }
#   ]
# })
#         print(payload)
#         headers2 = {
#   'Accept': 'application/vnd.retailer.v6+json',
#   'Content-Type': 'application/vnd.retailer.v6+json',
#   'Authorization': 'Bearer ' + get_token() 
# }
#         print(headers)
#         enrichedurl2 = 'https://api.bol.com/retailer/shipping-labels/delivery-options'
#         response1 = requests.request("POST", enrichedurl2 , headers=headers2, data=payload2)
#         print(response1.text)
#         #"shippingLabelOfferId" : "4ea7ebe2-1c31-4bf8-8cbf-21c6ec9e964e",
#     else:
#       bool_results = False
#     page += 1