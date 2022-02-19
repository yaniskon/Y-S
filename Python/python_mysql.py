import mysql.connector

mydb = mysql.connector.connect(host="localhost", user="root", passwd = "", database = "ordersmanagement")
if mydb:
    print('Connection sucessful')
else:
    print('Something failed')

mycursor = mydb.cursor()    

# mycursor.execute('SHOW DATABASES')
# for db in mycursor:
#     print(db)

# mycursor.execute('CREATE TABLE Orders (orderId bigint NOT NULL, orderPlacedDateTime varchar(50), PRIMARY KEY (orderId))')
# mycursor.execute('CREATE TABLE OrdersItems (orderItemId bigint NOT NULL, ean varchar(15), quantity bigint, quantityShipped bigint, quantityCancelled bigint, orderId bigint, PRIMARY KEY (orderItemId), FOREIGN KEY (orderId) REFERENCES orders(orderId))')
# mycursor.execute('CREATE TABLE shipmentDetails (salutation varchar(50), firstName varchar(50), surname varchar(50), streetName varchar(50), houseNumber varchar(50), zipCode varchar(50), city varchar(50), countryCode varchar(5), email varchar(50), language varchar(10), cancellationRequest boolean,orderId bigint, PRIMARY KEY (orderId))')
# mycursor.execute('CREATE TABLE InvoiceHead (invoiceId bigint NOT NULL, issueDate bigint, startDate bigint, endDate bigint, invoiceType varchar(50), lineExtensionAmount decimal (10, 2), payableAmount decimal (10, 2), taxExclusiveAmount decimal (10, 2), taxInclusiveAmount decimal (10, 2), timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY (invoiceId))')
mycursor.execute('CREATE TABLE InvoiceSpecs (id varchar(255) NOT NULL, invoiceLineRef varchar(50), invoiceQuantity varchar(50), orderId bigint, code varchar(50), taxPercent varchar(50), description varchar(100), categoryInvoiceElement varchar(50), totalPriceAmount varchar(50), quantity varchar(50), price varchar(50), taxTotal varchar(50), updated_at TIMESTAMP, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY (Id))')

# mycursor.execute('SHOW TABLESItems')
# for table in mycursor:
#     print(table)

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
# query = 'SELECT * FROM orderslist'
# mycursor.execute(query)
# results = mycursor.fetchone()

# print(results)

# for row in results:
#     print(row)

# Updating Data
# data = ('Hello', '1')
# query = "UPDATE orderslist SET orderName = %s WHERE orderId = %s"
# mycursor.execute(query, data)
# mydb.commit()

# Deleting Data
# query = "DELETE FROM orderslist WHERE orderId = 3"
# mycursor.execute(query)
# mydb.commit()

#Limit Command
# query = 'SELECT * FROM orderslist ORDER BY orderId DESC'
# mycursor.execute(query)
# result = mycursor.fetchall()
# print(result)
# TODO create a nice table with primary keys autoincrement and columns as well as selected query

# print(mydb)
# Drop table
# query = "DROP TABLE orders"
# mycursor.execute(query)

# CREATE tables and join

# query = "CREATE TABLE orders (id int NOT NULL AUTO_INCREMENT, customerid int, title varchar(50) NOT NULL, amount int, description varchar(500), PRIMARY KEY (id) )"
# mycursor.execute(query)

# query = "CREATE TABLE customers (id int NOT NULL AUTO_INCREMENT, name varchar(50), age int, PRIMARY KEY (id) )"
# mycursor.execute(query)

# data = [('John', 30), ("Jack", 20), ('Jane', 40)]
# query = 'INSERT INTO customers(name, age) VALUES (%s, %s)'
# mycursor.executemany(query, data)
# mydb.commit()
# print("number of rows: ", mycursor.rowcount)


# data = [(10, 'Product 1', 500, 'dasda'), (11, 'Product 2', 200, 'dasda435345'), (11, 'Product 3', 100, 'no descr')]
# query = 'INSERT INTO orders(customerid, title, amount, description) VALUES (%s, %s, %s, %s)'
# mycursor.executemany(query, data)
# mydb.commit()
# print("number of rows: ", mycursor.rowcount)

# query = "Select customers.name as Name, customers.age as Age, orders.title, orders.amount FROM customers INNER JOIN orders ON customers.id = orders.customerid order by orders.id DESC"
# mycursor.execute(query)
# content = mycursor.fetchall()
# # print(content)
# for item in content:
#     print(item[3])

# Install MySQL Workbench
# Installing mysql-connector