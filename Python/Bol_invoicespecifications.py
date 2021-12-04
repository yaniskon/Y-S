from Bol_access_token import get_token
from Bol_in import get_token
#import http.client
import requests
import json
from datetime import date, timedelta
import time


token = get_token()


baseurl = "https://api.bol.com/retailer/invoices"


# start_date in date type
#def get_invoiceIDs(start_date):


# specify API elements
payload={}
headers = {
'Accept': 'application/vnd.retailer.v6+json',
'Authorization': ''
}

headers['Authorization'] = 'Bearer ' + token 

# make list of invoice ids
InvoiceId_list = set()


list_ids = get_invoiceIDs(date(2020,12,1))  
for invoice in list_ids:
     
    print(invoice)
# request
baseurl =+ '/' + invoice
response = requests.request("GET", baseurl, headers=headers, data=payload)

# don't break bol
rate_limit = response.headers["X-RateLimit-Remaining"]
reset = response.headers["X-RateLimit-Reset"]
if int(rate_limit) < 2:
    print("Good night!")
time.sleep(int(reset)+1)
print("Back there again!")

# add invoiceid to list
response_dict = json.loads(response.text)
print(response_dict)
#    if "invoiceListItems" in response_dict:
#   invoice_list = response_dict["invoiceListItems"]

#   for invoice in invoice_list:
#     InvoiceId_list.add(invoice["invoiceId"])



#  return list(InvoiceId_list)