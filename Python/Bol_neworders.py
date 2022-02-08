from Bol_access_token import get_token
import requests
import json
import time
import pandas as pd
import os
import pymongo


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
  print(response_dict)
  orderItemId_ean_quantity = []
  for order in response_dict['orders']:
    for item in order['orderItems']:
      orderItemId_ean_quantity.append([item['orderItemId'], item['ean'], item['quantity'], item['quantityShipped'], item['quantityCancelled']])
 

  return orderItemId_ean_quantity


def delivery_options(orderitemID, ean, quantity, quantityShipped, quantityCancelled):
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
  response = json.loads(delresponse.text)
  deliveryIds = []
  price = []
  for options in response['deliveryOptions']:
    deliveryIds.append(options['shippingLabelOfferId'])
    price.append(options['labelPrice']['totalPrice'])
  i = 0

  def conv(s):
    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except ValueError:
            return 0   
  
  df=pd.read_csv(r'C:\Users\konst\Documents\Y-S\Python\offers.csv', converters={'ean':conv}, sep= ',', header = 1)
  df = df [(df['ean'] == int(ean))]
  df['quantity'] = quantity
  df['quantityShipped'] = quantityShipped
  df['quantityCancelled'] = quantityCancelled
   
  df = df[['ean','referenceCode', 'bundlePricesPrice', 'quantity', 'quantityShipped', 'quantityCancelled']]
  print("+=======================================================================+\n")
  print(df)
  print("+=======================================================================+\n")
  print("Delivery charges:")
  while i < len(deliveryIds):
    print(i+1, ":", price[i])
    i += 1
  choice = int(input("Enter your choice: "))
  delivery = [deliveryIds[choice-1]]

  return {orderitemID:delivery}


def Create_a_shipping_label(orderitemID, deliveryId):
  url = 'https://api.bol.com/retailer/shipping-labels'
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
    ],
    "shippingLabelOfferId": deliveryId
})

  get_label_response = requests.request("POST", url , headers=headers, data=payload)
  response = json.loads(get_label_response.text)
  get_urls = []
  #print(response)
  for options in response['links']:
    #deliveryIds.append(options['shippingLabelOfferId'])
    get_urls.append(options['href'])
  return get_urls


def get_process(url1):
  url = url1[0]
  headers = {
  'Accept': 'application/vnd.retailer.v6+json',
  'Content-Type': 'application/vnd.retailer.v6+json',
  'Authorization': 'Bearer ' + get_token() 
  }
  payload = {}
  time.sleep(3)   
  get_process_response = requests.request("GET", url , headers=headers, data=payload)
  response = json.loads(get_process_response.text)
  print(response['status'])
  return response['entityId']

def get_shipping_label(delivery_id):
  url = "https://api.bol.com/retailer/shipping-labels/"
  enrichurl = url + delivery_id
  headers = {
  'Accept': 'application/vnd.retailer.v6+pdf',
  'Content-Type': 'application/vnd.retailer.v6+json',
  'Authorization': 'Bearer ' + get_token() 
  }
  payload = ""
  get_shipping_label_response = requests.request("GET", enrichurl , headers=headers, data=payload)
  save_path = r'C:\Users\konst\Documents\Y-S\Python\Labels'
  file_name = delivery_id[:5]+".pdf"
  completeName = os.path.join(save_path, file_name)
  open(completeName, "wb").write(get_shipping_label_response.content)
  os.startfile(completeName, "print")


def ship_order_item(orderId, shippingLabel):
  url = 'https://api.bol.com/retailer/orders/shipment'
  headers = {
  'Accept': 'application/vnd.retailer.v6+json',
  'Content-Type': 'application/vnd.retailer.v6+json',
  'Authorization': 'Bearer ' + get_token() 
  }
  shipRef = input("Enter your FA-: ")
  payload = json.dumps({
  "orderItems": [
    {
      "orderItemId": orderId
    }
  ],
  "shipmentReference": shipRef,
  "shippingLabelId": shippingLabel
})
  response = requests.request("PUT", url, headers=headers, data=payload)

  print(response.text)



def get_orderid():
  url = "https://api.bol.com/retailer/orders"
  payload={}
  headers = {
  'Accept': 'application/vnd.retailer.v6+json',
  'Authorization': 'Bearer ' + get_token() 
  }
  response = requests.request("GET", url , headers=headers, data=payload)

  response_dict = json.loads(response.text)
  print(response_dict)
  orderIds = []
  for order in response_dict['orders']:
    orderIds.append(order['orderId'])
  return orderIds


def get_orderid_data(orderId):
  myclient = pymongo.MongoClient("mongodb://localhost:27017/")
  mydb = myclient["bol"]
  myorderinfo = mydb["orderInfo"]

  url = 'https://api.bol.com/retailer/orders/' + orderId
  payload={}
  headers = {
  'Accept': 'application/vnd.retailer.v6+json',
  'Authorization': 'Bearer ' + get_token() 
}

  response = requests.request("GET", url, headers=headers, data=payload)
  response_dict = json.loads(response.text)
  if myorderinfo.find_one({"orderId": orderId}) == None:
    myorderinfo.insert_one(response_dict)


try:
  for order in get_orderid():
    get_orderid_data(order)
except KeyError:
  print("No new orders!")

# print(get_new_orders())
for orderItemId, ean, quantity, quantityShipped, quantityCancelled in get_new_orders():
  result = delivery_options(orderItemId, ean, quantity, quantityShipped, quantityCancelled) 
  for shippingLabelOfferId in result[orderItemId]:
    shipingLabel = get_process(Create_a_shipping_label(orderItemId, shippingLabelOfferId))
    get_shipping_label(shipingLabel)
    ship_order_item(orderItemId, shipingLabel)