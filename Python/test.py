import datetime
from Bol_access_token import get_token
import http.client
import requests
import json
import pyodbc
from datetime import date
from datetime import time
from datetime import timedelta
import pymongo

# a = datetime.date.today()



# token = get_token()


# parameters = []
# # period_start_date = "2020-12-01"
# period_start_date = date(2020,12,1)
# period_end_date = date(2021,1,1)
# print(period_start_date)
# # period_end_date = "2021-01-01"

# print(datetime.date.today())

# # print(period_start_date)
# # print(period_end_date)

# # period_end_date = date.date.today() 
# # dt= date.timedelta(days=1) 
# # print(period_end_date + dt)

# while (period_end_date < datetime.date.today()):
#   period_start_date=period_start_date + datetime.timedelta(days=30) 
#   period_end_date = period_end_date + datetime.timedelta(days=30) 
#   print("start:")
#   print(period_start_date)
#   print("end:")
#   print(period_end_date)

# print(parameters)


import pandas as pd
# # iter_csv = pd.read_csv('offers.csv', iterator=True, chunksize=1000)
# # df = pd.concat([chunk[chunk['ean'] == '8719984000518'] for chunk in iter_csv])
# def conv(s):
#     try:
#         return int(s)
#     except ValueError:
#         try:
#             return float(s)
#         except ValueError:
#             return 0      
# # df=pd.read_csv('offers.csv', converters={'ean':conv}, sep= ',', header = 1)
# # print(df)
# # df = df [(df['ean'] == 8720387440047)]
# # df = df[['ean','referenceCode', 'bundlePricesPrice', ]]
# # print(df)


# df=pd.read_csv('offers.csv', sep= ',', header = 1)
# print(df)
# df = df [(df['ean'] == 8720387440047)]
# df = df[['ean','referenceCode', 'bundlePricesPrice', ]]
# print(df)

# import os


# os.startfile("e47da.pdf", "print")
# time.sleep(5)
# for p in psutil.process_iter(): #Close Acrobat after printing the PDF
#     if 'AcroRd' in str(p):
#         p.kill()


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mongodb = myclient["bol"]
shipmentsinfo = mongodb["shipments"]
shipmentsinfo.find({'shipmentReference': 1})
fa_strings = []
fa_numbers = []
for shipmentfind in shipmentsinfo.find({},{'shipmentReference': 1}):
    key = 'shipmentReference'
    if key in shipmentfind:
        word = shipmentfind['shipmentReference']
        if len(word) < 20:
            fa_numbers.append(int(word[3:10]))
    
    # print(f'Item: {word}, length is: {len(word)}')
    # if len(shipmentfind['shipmentReference']) <= 10:
    #     print(shipmentfind['shipmentReference'])
    # if len(shipmentfind['shipmentReference']) > 10:
        
        # 
FA = max(fa_numbers) +1
print(FA)
# # txt = "h3110 23 cat 444.4 rabbit 11 2 dog"
# # [int(s) for s in txt.split() if s.isdigit()]
# # [23, 11, 2]
