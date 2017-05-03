'''
Created on 2017年4月28日

@author: ux501
'''

import csv

import mysql.connector

TicketSymbol = list();
with open('companylist.csv','r',newline='') as csvfile:
    
    reader = csv.reader(csvfile)
    for item in reader:
#         print(item)
        print(item[0])
        TicketSymbol.append(item[0])

print(TicketSymbol)


conn = mysql.connector.connect(user='root', password='newpassword', database='yahoostock')

cursor = conn.cursor()

cursor.execute('create table if not exists StockSymbol (Symbol varchar(20)) ')
cursor.execute('use yahoostock')

#
TicketSymbol = TicketSymbol[1:] 

for item in TicketSymbol:
    
    cursor.execute('insert into StockSymbol(Symbol) values(%s)',[item])
    print(cursor.rowcount)

conn.commit()
cursor.close()

conn.close()

