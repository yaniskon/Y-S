from Bol_access_token import get_token
import http.client
import requests
import json
import pyodbc
import datetime

token = get_token()


baseurl = "https://api.bol.com/retailer/invoices"

parameters = []
period_start_date = "2021-05-01"
period_end_date = "2021-06-01"

while (period_end_date < datetime.date.today()):
  period_start_date.month += 1
  period_end_date.month += 1
  parameters.append({"period-start-date": period_start_date,  "period-end-date": period_end_date})
# parameters= {"period-start-date": "2021-07-01", "period-end-date": "2021-08-01"}
# ,
#              ["period-start-date" : "2021-03-01","period-end-date": "2021-04-01"]}

payload={}
headers = {
   'Accept': 'application/vnd.retailer.v6+json',
   'Authorization': ''
}

headers['Authorization'] = 'Bearer ' + token 

response = requests.request("GET", baseurl, params=parameters, headers=headers, data=payload)


# return response
# print(response_invoice)
# print(type(response_invoice['period']))
# print(type(response_invoice['invoiceListItems']))
# print(response_invoice['invoiceListItems'])

conn = pyodbc.connect('Driver={SQL Server};'
                  'Server=DESKTOP-5RJSIM1\SQLEXPRESS;'
                  'Database=ERP;'
                  'Trusted_Connection=yes;')


cursor = conn.cursor()

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