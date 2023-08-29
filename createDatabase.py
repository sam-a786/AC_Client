import sqlite3
#database

conn = sqlite3.connect('AeronaClinicalDatabase.db')
cur = conn.cursor()

cur.execute('''CREATE TABLE Company (
companyID integer Primary key AUTOINCREMENT,
companyName varchar,
deliveryAddress varchar,
legalAddress varchar,
deliveryContact varchar,
telephone varchar)''')

cur.execute('''CREATE TABLE Orders (
orderNo integer Primary key AUTOINCREMENT,
companyID varchar(12),
userID varchar,
date varchar,
accountReference varchar,
acCOD varchar,
consignmentNo integer,
noOfPallets integer,
noOfBoxes integer,
weight float,
transportCompany varchar)''')

cur.execute('''CREATE TABLE Users (
userID integer Primary key AUTOINCREMENT,
userName varchar,
password varchar,
admin boolean)''')

cur.execute('''CREATE TABLE OrdersToProduct (
orderNo integer,
productID varchar,
quantity integer)''')

cur.execute('''CREATE TABLE Product (
productID integer Primary key AUTOINCREMENT,
productName varchar,
conditions varchar,
batchNo varchar,
origin varchar,
expiryDate varchar)''')

cur.execute('''CREATE TABLE FAQ (
questions varchar,
answers varchar
)''')
