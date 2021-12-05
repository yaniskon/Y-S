from Bol_access_token import get_token
from Bol_InvoiceIds import list_ids
import requests
import json
from datetime import date, timedelta
import time



baseurl = "https://api.bol.com/retailer/invoices/"
print("+====================================+")
print(list_ids[0])

#def get_invoiceSpecifications():


# specify API elements
payload={}
headers = {
'Accept': 'application/vnd.retailer.v6+json',
'Authorization': ''
}

headers['Authorization'] = 'Bearer ' + get_token() 


# request
fullbaseurl = baseurl + '3904875527181' + "/specification"
response = requests.request("GET", fullbaseurl, headers=headers, data=payload)
#print(response.text)

response_dict2 = json.loads(response.text)
#print(response_dict2)
if "invoiceSpecification" in response_dict2:
    InvoiceSpecifications = response_dict2["invoiceSpecification"]
    for InvoiceElement in InvoiceSpecifications:
        print("+===============================================+")
        print("+===============================================+")
        for i in InvoiceElement:
            # if InvoiceElement[i] == 'AdditionalItemProperty':
            # print(i, '->', InvoiceElement[i])
            print(InvoiceElement[i])

"""        print("+===============================================+")

# make list of invoice ids
InvoiceId_list = set()


list_ids = get_invoiceIDs(date(2020,12,1))  
for invoice in list_ids:
     
    print(invoice)

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
"""
