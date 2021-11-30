import datetime
from Bol_access_token import get_token
import http.client
import requests
import json
import pyodbc
from datetime import date
from datetime import datetime

# a = datetime.date.today()



token = get_token()


parameters = []
period_start_date = "2020-12-01"
period_end_date = "2021-01-01"


period_start_date = date.strptime(period_start_date, "%Y-%m-%d").date()
period_end_date = date.strptime(period_end_date, "%Y-%m-%d").date()

print(period_start_date)
print(period_end_date)

period_end_date = date.date.today() 
dt= date.timedelta(days=1) 
print(period_end_date + dt)

# while (period_end_date < datetime.date.today()):
#   period_start_date=period_start_date + period_start_date.timedelta(months=1) 
#   period_end_date = period_end_date + period_end_date.timedelta(months=1) 
#   print(period_start_date)
#   print(period_end_date)

# print(parameters)