from enum import unique
from sqlite3 import Timestamp
from Bol_access_token import get_token
import requests
import json
from datetime import date, timedelta
import time
import calendar
import mysql.connector

mydb = mysql.connector.connect(host="localhost", user="root", passwd = "", database = "ordersmanagement")
if mydb:
    pass
else:
    print('Something failed')

mycursor = mydb.cursor()   

def get_invoiceSpecs(invoiceId):
    url = "https://api.bol.com/retailer/invoices/" + str(invoiceId) + "/specification"
    
    # specify API elements
    payload={}
    headers = {
    'Accept': 'application/vnd.retailer.v6+json',
    'Authorization': ''
    }
    headers['Authorization'] = 'Bearer ' + get_token() 

    response = requests.request("GET", url, headers=headers, data=payload)
    response_dict = json.loads(response.text)
    print(response_dict)

    # don't break bol
    rate_limit = response.headers["X-RateLimit-Remaining"]
    reset = response.headers["X-RateLimit-Reset"]
    if int(rate_limit) < 1:
        print("Good night!")
        time.sleep(int(reset))
        print("Back there again!")
    
    for InvoiceElement in response_dict["invoiceSpecification"]:
        required_id = InvoiceElement["id"]
        # print(InvoiceElement)
        # print("")
        x = required_id.find('BRMG')
        if x < 0: #if BRMG not there
            id = InvoiceElement['id']
            invoiceLineRef = InvoiceElement['invoiceLineRef']
            invoiceQuantity = InvoiceElement['invoicedQuantity']['value']
            orderId = InvoiceElement["item"]["AdditionalItemProperty"][0]["Value"]["value"] if InvoiceElement["item"]["AdditionalItemProperty"][0]["Value"]["value"] else ''
            code = InvoiceElement["item"]["AdditionalItemProperty"][1]["Value"]["value"] if InvoiceElement["item"]["AdditionalItemProperty"][1]["Value"]["value"] else ''
            taxpercent = InvoiceElement["item"]["ClassifiedTaxCategory"][0]["Percent"]["value"]
            description = InvoiceElement["item"]["Description"][0]["value"]
            categoryInvoiceElement  = InvoiceElement['item']["Name"]["value"]
            totalPriceAmount = InvoiceElement["lineExtensionAmount"]["value"]
            quantity = InvoiceElement["price"]["BaseQuantity"]["value"]
            price = InvoiceElement["price"]["PriceAmount"]["value"]
            taxTotal = InvoiceElement["taxTotal"]['TaxAmount']["value"]
            
            print(id)
            check_unique = "SELECT COUNT(*) as total FROM invoicespecs WHERE id ='" +  id + "'" 
            mycursor.execute(check_unique)
            unique_check = mycursor.fetchone()
            # print(unique_check[0])
            if unique_check[0] > 0:
                print('Exists, need to be updated')
                # gmt stores current gmtime
                updated_at = calendar.timegm(time.gmtime())
                data = (invoiceLineRef, invoiceQuantity, orderId, code, taxpercent, description, categoryInvoiceElement, totalPriceAmount, quantity, price, taxTotal, updated_at)
                query = f"UPDATE invoicespecs SET invoiceLineRef = '{invoiceLineRef}', invoiceQuantity = '{invoiceQuantity}', orderId = {orderId}, code = '{code}', taxpercent = '{taxpercent}', description = '{description}', categoryInvoiceElement = '{categoryInvoiceElement}', totalPriceAmount = '{totalPriceAmount}', quantity = '{quantity}', price = '{price}', taxTotal = '{taxTotal}', updated_at = FROM_UNIXTIME('{updated_at}') WHERE id = '{str(id)}'"
                print(query)
                mycursor.execute(query)
                mydb.commit()
            else:
                print('Needs to be inserted: ')
                invoiceData = (id, invoiceLineRef, invoiceQuantity, orderId, code, taxpercent, description, categoryInvoiceElement, totalPriceAmount, quantity, price, taxTotal)
                query = 'INSERT INTO invoicespecs(id, invoiceLineRef, invoiceQuantity, orderId, code, taxpercent, description, categoryInvoiceElement, totalPriceAmount, quantity, price, taxTotal) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
                mycursor.execute(query, invoiceData)
                mydb.commit()

# get_invoiceSpecs(3905961026037)
queryInvoiceIds = "SELECT invoiceId FROM invoicehead" 
mycursor.execute(queryInvoiceIds)
listInvoiceIds = mycursor.fetchall()
for invoice in listInvoiceIds:
    if invoice[0] != 3905321480960:
        print(invoice[0])
        get_invoiceSpecs(invoice[0])
