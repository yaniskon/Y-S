from Bol_access_token import get_token
import requests
import json
import time


# Standard API parameters

url = "https://api.bol.com/retailer/shipments"
payload={}
headers = {
  'Accept': 'application/vnd.retailer.v6+json',
  'Authorization': ''
}
headers['Authorization'] = 'Bearer ' + get_token() 

# Parameters & variables for collecting as much shipment data as possible 

page = 1
bool_results = True
ship_results = []

while bool_results:  # We can paginate this API up until 3 months worth of shipments
    enrichedurl = url + f"?page={page}"
    response = requests.request("GET", enrichedurl , headers=headers, data=payload)
    response_dict = json.loads(response.text)

    # don't break bol
    rate_limit = response.headers["X-RateLimit-Remaining"]
    reset = response.headers["X-RateLimit-Reset"]
    if int(rate_limit) < 1:
        print("Good night!")
        time.sleep(int(reset))
        print("Back there again!")
    
    print(response.text)
    
    if response_dict != {}:
        for shipment in response_dict['shipments']:
          ship_results.append(shipment)
    else:
      bool_results = False
    page += 1
 
print(ship_results)
print(len(ship_results))
# Save into a file 
print("+====================================+")
print(ship_results[0])
# json.dump( ship_results, open( "shipment_results_12-12-21.json", 'w' ) )