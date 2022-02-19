from Bol_access_token import get_token
import requests
import json
from datetime import date, timedelta
import time
import mysql.connector

mydb = mysql.connector.connect(host="localhost", user="root", passwd = "", database = "ordersmanagement")
if mydb:
    pass
else:
    print('MYSQL Connection failed')

mycursor = mydb.cursor()   


# start_date in date type
def get_invoiceIDs(start_date):
  period_start_date = start_date

  # specify API elements
  baseurl = "https://api.bol.com/retailer/invoices"
  payload={}
  headers = {
    'Accept': 'application/vnd.retailer.v6+json',
    'Authorization': 'Bearer ' + get_token()
  }


  # make list of invoice ids
  InvoiceId_list = set()
  period_end_date = period_start_date + timedelta(days=30)
  while period_start_date < date.today():
    
    # request
    parameters ={"period-start-date": period_start_date,  "period-end-date": period_end_date}
    response = requests.request("GET", baseurl, params=parameters, headers=headers, data=payload)

    # don't break bol
    rate_limit = response.headers["X-RateLimit-Remaining"]
    reset = response.headers["X-RateLimit-Reset"]
    if int(rate_limit) < 1:
      print("Good night!")
      time.sleep(int(reset))
      print("Back there again!")
    
    # add invoiceid to list
    response_dict = json.loads(response.text)
    print(response_dict)
    print("\n\n")
    if "invoiceListItems" in response_dict:
      invoice_list = response_dict["invoiceListItems"]

      for invoice in invoice_list:
        query = "SELECT COUNT(*) as total FROM invoicehead WHERE invoiceId =" +  invoice["invoiceId"] 
        mycursor.execute(query)
        required_data = mycursor.fetchone()
        if required_data[0] == 0:
          data = invoice["invoiceId"] , invoice["issueDate"], invoice["invoicePeriod"]["startDate"], invoice["invoicePeriod"]["endDate"], invoice["invoiceType"], invoice["legalMonetaryTotal"]["lineExtensionAmount"]["amount"], invoice["legalMonetaryTotal"]["payableAmount"]["amount"], invoice["legalMonetaryTotal"]["taxExclusiveAmount"]["amount"], invoice["legalMonetaryTotal"]["taxInclusiveAmount"]["amount"]
          query = 'INSERT INTO invoicehead(invoiceId, issueDate, startDate, endDate, invoiceType, lineExtensionAmount, payableAmount, taxExclusiveAmount, taxInclusiveAmount) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
          mycursor.execute(query, data)
          mydb.commit()


    # update interval
    period_start_date= period_end_date
    period_end_date +=  timedelta(days=30)

  return list(InvoiceId_list)

if __name__ == "__main__":
  list_ids = get_invoiceIDs(date(2020,12,1))
  print(list_ids)
