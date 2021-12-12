from Bol_access_token import get_token
from Bol_InvoiceIds import get_invoiceIDs
import requests
import json
from datetime import date, timedelta
import time



def get_orderids():

    baseurl = "https://api.bol.com/retailer/invoices/"

    # specify API elements
    payload={}
    headers = {
    'Accept': 'application/vnd.retailer.v6+json',
    'Authorization': ''
    }
    headers['Authorization'] = 'Bearer ' + get_token() 

    orderids_set = set()

    # loop through the invoices
    for invoice in get_invoiceIDs(date(2020,12,1)):

        # request
        url = baseurl + invoice + "/specification"
        response = requests.request("GET", url, headers=headers, data=payload)
        response_dict = json.loads(response.text)

        # don't break bol
        rate_limit = response.headers["X-RateLimit-Remaining"]
        reset = response.headers["X-RateLimit-Reset"]
        if int(rate_limit) < 1:
            print("Good night!")
            time.sleep(int(reset))
            print("Back there again!")
        
        for InvoiceElement in response_dict["invoiceSpecification"]:
            if InvoiceElement["item"]["AdditionalItemProperty"] != []:
                orderid = InvoiceElement["item"]["AdditionalItemProperty"][0]["Value"]["value"]
                orderids_set.add(orderid)

    return list(orderids_set)

orderids = get_orderids()        
print(orderids)
print(len(orderids))

class Order:
    def __init__(self, orderid):
        # get all things we want
        self.orderid = orderid


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
