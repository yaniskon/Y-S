from Bol_access_token import get_token
import requests
import json
import time
import pandas as pd
import os
import pymongo
import mysql.connector

mysqldb = mysql.connector.connect(host="localhost", user="root", passwd = "", database = "ordersmanagement")
if mysqldb:
    pass
else:
    print('MYSQL Connection failed')

mycursor = mysqldb.cursor() 

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
  print(response_dict['orders'])

  order_list = []
  ordeitems_list = []

  for order in response_dict['orders']:

    order_data = (order['orderId'], order['orderPlacedDateTime'])
    check_unique = "SELECT COUNT(*) as total FROM orders WHERE orderId ='" +  str(order['orderId']) + "'"
    mycursor.execute(check_unique)
    unique_check = mycursor.fetchone()
    if unique_check[0] == 0:
      query = 'INSERT INTO orders(orderId, orderPlacedDateTime) VALUES (%s, %s)'
      mycursor.execute(query, order_data)
      mysqldb.commit()
    order_list.append(order_data)
    for item in order['orderItems']:
      check_unique2 = "SELECT COUNT(*) as total FROM ordersitems WHERE orderItemId ='" +  str(item['orderItemId']) + "'" 
      mycursor.execute(check_unique2)
      unique_check_result = mycursor.fetchone()
      ordersss_items = [item['orderItemId'], item['ean'], item['quantity'], item['quantityShipped'], item['quantityCancelled'], order['orderId']]
      orderlist_data = (item['orderItemId'], item['ean'], item['quantity'], item['quantityShipped'], item['quantityCancelled'], order['orderId'])
      if unique_check_result[0] == 0:
        query2 = 'INSERT INTO ordersitems(orderItemId, ean, quantity, quantityShipped, quantityCancelled, orderId) VALUES (%s, %s, %s, %s, %s, %s)'
        mycursor.execute(query2, orderlist_data)
        mysqldb.commit()
      ordeitems_list.append(ordersss_items)
      
  #print(ordeitems_list)
  return ordeitems_list

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
  print(response_dict)
  data = []

  # Insert into MySQL
  data= (response_dict['shipmentDetails']['salutation'], response_dict['shipmentDetails']['firstName'], response_dict['shipmentDetails']['surname'], response_dict['shipmentDetails']['streetName'], response_dict['shipmentDetails']['houseNumber'], response_dict['shipmentDetails']['zipCode'], response_dict['shipmentDetails']['city'], response_dict['shipmentDetails']['countryCode'], response_dict['shipmentDetails']['email'], response_dict['shipmentDetails']['language'], '', orderId)
  print('OrderID: '+ orderId)
  query = "SELECT COUNT(*) as total FROM shipmentdetails WHERE orderId =" +  orderId 
  mycursor.execute(query)
  required_data = mycursor.fetchone()
  if required_data[0] == 0:
    print('Inside if')
    query = 'INSERT INTO shipmentdetails(salutation, firstName, surname, streetName, houseNumber, zipCode, city, countryCode, email, language, cancellationRequest, orderId) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    mycursor.execute(query, data)
    mysqldb.commit()

  # Insert into MongoDB
  if myorderinfo.find_one({"orderId": orderId}) == None:
    myorderinfo.insert_one(response_dict)
  
  return response_dict



def delivery_options(orderitemID, ean, quantity, quantityShipped, quantityCancelled, cancellation_flag):
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
  df['cancellation_flag'] = cancellation_flag
   
  df = df[['ean','referenceCode', 'bundlePricesPrice', 'quantity', 'quantityShipped', 'quantityCancelled', 'cancellation_flag']]
  print("+===============================================================================================================+\n")
  print(df)
  print("+===============================================================================================================+\n")
  print("Delivery charges:")
  while i < len(deliveryIds):
    print(i+1, ":", price[i])
    i += 1
  choice = int(input("Enter your choice: "))
  delivery = [deliveryIds[choice-1]]
  print(delivery)
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
  file_name = delivery_id[::]+".pdf"
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
  myclient = pymongo.MongoClient("mongodb://localhost:27017/")
  mongodb = myclient["bol"]
  shipmentsinfo = mongodb["shipments"]
  shipmentsinfo.find({'shipmentReference': 1})
  fa_numbers = []
  for shipmentfind in shipmentsinfo.find({},{'shipmentReference': 1}):
      key = 'shipmentReference'
      if key in shipmentfind:
          word = shipmentfind['shipmentReference']
          if len(word) < 20:
              fa_numbers.append(int(word[3:10]))
  FA = max(fa_numbers) +1
  if FA < 1000:
    shipRef = 'FA-0000' + str(FA)
  elif FA >= 1000 and FA < 10000:
    shipRef = 'FA-000' + str(FA)
  elif FA >=10000 and FA < 100000:
    shipRef = 'FA-00' + str(FA)  
  print(shipRef)
  user_value = input('Press Enter')
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

 
# try:
#   for order in get_new_orders():
#     get_orderid_data(order)
# except KeyError:
#   print("No new orders!")

try:
  for orderItemId, ean, quantity, quantityShipped, quantityCancelled, orderId in get_new_orders():
    order_details = get_orderid_data(orderId)
    required_items_list = []
    for item in order_details['orderItems']:
      if item['orderItemId'] == orderItemId:
        cancellation_flag = item['cancellationRequest']    
    result = delivery_options(orderItemId, ean, quantity, quantityShipped, quantityCancelled, cancellation_flag)
    for shippingLabelOfferId in result[orderItemId]:
      shipingLabel = get_process(Create_a_shipping_label(orderItemId, shippingLabelOfferId))
      get_shipping_label(shipingLabel)
      ship_order_item(orderItemId, shipingLabel)
except KeyError:
  print('Time to relax \nNo new orders!!')