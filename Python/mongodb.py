from pymongo import MongoClient
import pymongo

def create_shipment(shipment):

    CONNECTION_STRING  = 'mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000'
    client = MongoClient(CONNECTION_STRING)
    # return client['shop']["shipments"]
    return result #print(client.list_database_names())

result =  create_shipment().insert_one({"dssd":"323"})  

# # This is added so that many files can reuse the function get_database()
# if __name__ == "__main__":    
    
#     # Get the database & collection



#   result =  get_shipments().insert_one(item_3) 



# {"shipmentId": "952216234", "shipmentDateTime": "2021-09-12T22:27:17+02:00", "shipmentReference": "FA-0000181", "order": {"orderId": "1267274724", "orderPlacedDateTime": "2021-09-12T20:49:20+02:00"}, "shipmentItems": [{"orderItemId": "2725411187", "ean": "8720387440429"}], "transport": {"transportId": "698809133"}}
