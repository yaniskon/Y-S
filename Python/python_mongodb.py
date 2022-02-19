import pymongo
# MongoDB CLient
# client = pymongo.MongoClient("mongodb://localhost:27017")
client = pymongo.MongoClient("mongodb+srv://bokons:admin18022022@bokons.xgukx.mongodb.net/test?retryWrites=true&w=majority")
# Table: Collection, Row: Document
# A database cannot if there is no collection
cursor = client.list_databases()
for db in cursor:
    print(db)
# db =  client['test']  #Create Database

# collection = db['orders'] #Create Collection

# Printing Databases
# databases = client.list_database_names()
# for dbs in databases:
#     print(dbs)

# Printing Tables
# tables = db.list_collection_names()
# for table in tables:
#     print(table)

# Add/Insert Data

# data = { "örderName": "First Order", "DeliveryCity": "Amsterdam", 'Orderitems': 3, 'Amount': 50 }
# data_many = [--
#     {"_id": 1, "örderName": "First Order", "DeliveryCity": "Amsterdam", 'Orderitems': 3, 'Amount': 50, "country": "ÄBC" },
#     {"_id": 2, "örderName": "Second Order", "DeliveryCity": "Amsterdam", 'Orderitems': 1 },
#     {"_id": 3, "örderName": "Third Order", "DeliveryCity": "Amsterdam", 'Orderitems': 4, 'Amount': 150 },
#     {"_id": 4, "örderName": "Fourth Order", "DeliveryCity": "Amsterdam", 'Orderitems': 1, 'Amount': 110 },
#     {"_id": 5, "örderName": "Fifth Order", "DeliveryCity": "Amsterdam", 'Orderitems': 30, 'Amount': 5000 }
# ]
# # collection.insert_one(data) #inserting Data
# collection.insert_many(data_many)

# find/select
# data = collection.find_one()
# print(data['DeliveryCity'])'
# select name, age  from table
# data = collection.find({}, {"DeliveryCity": 1,  })
# select * from this where orderitems = 1
# data = collection.find({"Orderitems": 3})
# data = collection.find({"Orderitems": {"$gt": 4}})

# Sorting
# data = collection.find().sort("Orderitems", -1)   #Second Paramter, 1 or -1

# Delete
# collection.delete_one({"Amount":50})
# collection.delete_many({})        #Delete All Items
# collection.delete_many({"DeliveryCity" : "Amsterdam"})

# Drop a Collection
# collection.drop()
# 
#
# Update
# Update users set deliverycity = newyork where id= 5
# collection.update_one({"_id": 5}, {"$set": {"DeliveryCity": "New York"}})  
# collection.update_many({"DeliveryCity": "Amsterdam"}, {"$set": {"DeliveryCity": "Paris"}}) 
# collection = db['customers'] #Create Collection

# LIMIT 
# data = collection.find({"DeliveryCity": "Paris"}).limit(2)

# data = collection.insert_many(
#     [{'Name': 'John', 'age' : "30", "Country": {'Name': 'Netherlands', 'countrycode': 'NL'}},
#     {'Name': 'Nick', 'age' : "35", "Country": {'Name': 'Netherlands', 'countrycode': 'NL'}},
#     {'Name': 'Maria', 'age' : "14", "Country": {'Name': 'Netherlands', 'countrycode': 'NL'}},
#     {'Name': 'Sonia', 'age' : "32", "Country": {'Name': 'Netherlands', 'countrycode': 'NL'}}])

# {"$regex": ".*er.*"}
data = collection.find({"Country.countrycode": {"$regex": ".*NL.*"} })
for item in data:
    print(item)