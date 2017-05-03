'''
Created on 2017年4月28日

@author: ux501
'''

from yahoo_finance import Share
import mysql.connector
from numpy import empty
import signal
import time
import datetime

class MysqlConnector(object):
    
    def __init__(self, user, password,database):
        
        self.user = user
        self.password = password
        self.database = database
        
        self.conn = mysql.connector.connect(user=self.user, password=self.password, database=self.database)
        
        self.cursor = self.conn.cursor()
        
    def execute(self, SQL_statement):
        
        self.cursor.execute(SQL_statement)
        print(SQL_statement)
        
        if('select' in SQL_statement):
            return self.cursor.fetchall()
        else:
            self.conn.commit()    
            return None
        
    
    
    def insertData(self,tableName,**kw):
        
        if(kw is not None):
            
            colNameList = list()
            colValueList = list()
            
            for colName,colValue in kw.items():
                colNameList.append(colName)
                colValueList.append(colValue)
            
            ReplaceSymbol = ['%s' for x in range(1,len(colNameList)+1)]
            
            
            InsertSQL = 'insert into '+ tableName +' ('+','.join(colNameList)+') values ('+','.join(ReplaceSymbol)+')'
            print(InsertSQL)
            print(colValueList)
            self.cursor.execute(InsertSQL,colValueList)
            self.conn.commit()
            
            
    def close(self):
        
        self.cursor.close()
        self.conn.close()
    
class YahooStock(object):
    
    def __init__(self):
        self.connector = MysqlConnector('root','newpassword','yahoostock')
        self.StockSymbol = list()
    
    def LoadStockSymbol(self):
        
        self.connector.execute('use yahoostock')
        values = self.connector.execute('select * from Stocksymbol')
        
        for item in values:
            
            self.StockSymbol.append(item[0])
    
    
        
    def InsertData(self):
        
        
        d = datetime.datetime.now().weekday()
        print(d)
        if(d == 5 or d == 6):
            return None
        
        errorlist = list()
        current_date = time.strftime("%Y-%m-%d")
        
        for index, item in enumerate(self.StockSymbol):
            try:
                stock = Share(item)
                value = stock.get_historical(current_date, current_date)
                self.connector.insertData('Stock',**value[0])
            except Exception as e:
                print(e)
                errorlist.append(item)
        
        print(errorlist)
        
        return None
    def close(self):
        
        self.connector.close()
     
if __name__ == '__main__':
    
    
    yahoo = YahooStock()
    print(yahoo.LoadStockSymbol())
    yahoo.InsertData()
    yahoo.close()
#     connector = MysqlConnector('root','newpassword','yahoostock')
#      
#     connector.execute('use yahoostock')
# #     connector.execute('create table if not exists Stock (Symbol varchar(20), name varchar(20)) ')
#     connector.insertData('Stock',id = '2', name ='zhaofeng')
#      
#     connector.close()