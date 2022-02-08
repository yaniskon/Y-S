import mysql.connector

mydb = mysql.connector.connect(host="localhost", user="root", passwd = "", database = "orders")
if mydb:
    print('Connection sucessful')
else:
    print('Something failed')

mycursor = mydb.cursor()    

# mycursor.execute('SHOW DATABASES')
# for db in mycursor:
#     print(db)

# mycursor.execute('CREATE TABLE orderslist (orderId int(11), orderName varchar(50))')

mycursor.execute('SHOW TABLES')
for table in mycursor:
    print(table)

# Adding SIngle Row
# data = ('1', 'Universal Order')
# query = 'INSERT INTO orderslist(orderId, orderName) VALUES (%s, %s)'
# mycursor.execute(query, data)

#Adding Multiple Rows
# data = [(1, "Order1"), (2, "Order2"), (3, "Order3")]
# query = 'INSERT INTO orderslist(orderId, orderName) VALUES (%s, %s)'
# mycursor.executemany(query, data)
# mydb.commit()

#Reading Data
query = 'SELECT * FROM orderslist'
mycursor.execute(query)
results = mycursor.fetchone()

print(results)

# for row in results:
#     print(row)


# TODO create a nice table with primary keys autoincrement and columns as well as selected query

# print(mydb)



# Install MySQL Workbench
# Installing mysql-connector
