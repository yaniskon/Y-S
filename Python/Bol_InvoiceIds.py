from Bol_access_token import get_token
import requests
import json
from datetime import date, timedelta
import time



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
        if invoice["invoiceId"] != "3905321480960": #I exclude Bol.com Retailer Media Groep invoice
          InvoiceId_list.add(invoice["invoiceId"])


    # update interval
    period_start_date= period_end_date
    period_end_date +=  timedelta(days=30)

  return list(InvoiceId_list)

if __name__ == "__main__":
  list_ids = get_invoiceIDs(date(2020,12,1))
  print(list_ids)


"""




# return response
# print(response_invoice)
# print(type(response_invoice['period']))
# print(type(response_invoice['invoiceListItems']))
# print(response_invoice['invoiceListItems'])






def get_invoiceIds(response):
  response_invoice = json.loads(response.text)
  invoiceIds = []
  for invoice in response_invoice['invoiceListItems']:
    invoiceIds.append(invoice['invoiceId'])
    #invoiceIds.append(invoice['issuePeriod'])
    #print(invoice)
  return invoiceIds

print(get_invoiceIds(response))


# for id in get_invoiceIds(response):
#   cursor.execute("insert into [stg].[Bol_InvoiceId](InvoiceId) values (?)", id )


# try:


conn.commit()
conn.close()
# for i in cursor:
#     print(i)


# url = "https://api.bol.com/retailer/invoices/3903865603660/specification"

# payload={}
# headers = {
#   'Accept': 'application/vnd.retailer.v6+json',
#     'Authorization': 'Bearer eyJraWQiOiJyc2EyIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiI1ZjZlNjFjZC05ZTU5LTQ3MjgtODU0OS1mOWFkNDEzMmI5ZGQiLCJhenAiOiI1ZjZlNjFjZC05ZTU5LTQ3MjgtODU0OS1mOWFkNDEzMmI5ZGQiLCJjbGllbnRuYW1lIjoieWFuaXMiLCJpc3MiOiJodHRwczpcL1wvbG9naW4uYm9sLmNvbSIsInNjb3BlcyI6IlJFVEFJTEVSIiwiZXhwIjoxNjM4MjAxODE2LCJpYXQiOjE2MzgyMDE1MTYsImFpZCI6IkNMTlRDOmJlMmI3MDE2LTczNDYtYzM2ZS1kMTM4LTc3NzA4MTczZjdiYyBTTFI6MTY1Njg0NCIsImp0aSI6IjI1YWVlOTE1LWZhZjctNGJlOC1hZDNhLWIzYjQ3OTVmY2RkOSJ9.ieZGPit2zWC6O_nBeg9uMc923o784iesTOvDLmHAuBoHk6bgZXsIzJKYUnm4_AuNMEVMORwtErU5SLbVJllJy6B1zXVUbtdjB5CeFH7vOPp2ZVIaTvTyw7AOoDFpnBQc4cv2TPzqmSo5Zw_i6nT_AO7u3ZE-91aeTib_YnvJcRGWrF9mSipEGh8wnGn50TgYf9a6rvfED-pnjiaw1Pu4mp0RUrBDFWBFP9P3yFufia35gdd4ysoU1vlTixvBTsptmQ4cQsnYvrsC4g24FvL8tRB_f27crqK0_PK4WROImz5eUjdttXzb3rDZ_FaaiZ7obzJoeS5LDJNXvWb2dubLaw'

# }

# response = requests.request("GET", url, headers=headers, data=payload)

# print(response.text)






#print(token)

"""