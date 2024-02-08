# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 13:47:25 2023

@author: Alex
"""
import sqlite3
import os

import pandas as pd

filename = 'C:\\Users\\jimni\\LocalCapstone\\demo_topic_csv\\topic0.csv'
df = pd.read_csv(filename)
df = df.drop(labels = "Unnamed: 0", axis = 1)



print(df.columns)

datas = []
for i in df.index:
    insert_data = [df["index"].loc[i], df["topic"].loc[i], df["article"].loc[i], df["neg"].loc[i], df["neu"].loc[i], df["pos"].loc[i], df["Subjectivity"].loc[i], df["Sentiment"].loc[i], df["Topic Prob"].loc[i]]
    #print(i)
    datas.append(insert_data)
    #print(type(insert_data[8]))
    #print(df["article"].loc[i],'\n')

#print(datas)

conn = sqlite3.connect('T:\\Testconnection.db', timeout = 5)

os.chmod("T:\\Testconnection.db", 0o777)

cursor = conn.cursor()




cursor.execute("""CREATE TABLE IF NOT EXISTS topic0_test
                   (ind INT, topic TEXT, article TEXT, neg FLOAT,
                    neu FLOAT, pos FLOAT, subjectivity FLOAT, sentiment FLOAT,
                    topic_prob FLOAT)
                """)

conn.commit()


"""datas = [('This is a headline', '12/02/2006', 
          'dsiabpdsiabi. djsabfnabpfdsa jdbsahfbldsa dfbadslfhbsal dksafblsa somehtin',
           'CNN','0', '0', '0', '0', '0', '0' ),
          ('Another Headline','1/25/2013', 
           'short article',
          'Texas Tribune','0', '0', '0', '0', '0', '0' ),
          ('Headline News at 11','10/13/2023',
            'articleartic',
          'KBTX','0', '0', '0', '0', '0', '0')]"""


for i in df.index:
    insert_data = [df["index"].loc[i], df["topic"].loc[i], df["article"].loc[i], df["neg"].loc[i], df["neu"].loc[i], df["pos"].loc[i], df["Subjectivity"].loc[i], df["Sentiment"].loc[i], df["Topic Prob"].loc[i]]
    cursor.execute("INSERT INTO topic0_test VALUES (?,?,?,?,?,?,?,?,?)", insert_data)

#cursor.executemany("INSERT INTO topic0_test VALUES (?,?,?,?,?,?,?,?,?)", datas)

cursor.close()

# for row in cursor.execute("SELECT rowid, * FROM datatest"):
#         print(row)    
#         rowids = row[0]    
#         headlines  = row[1]
#         publishers = row[2]
#         artilces = row[3]
#         sentiments = row[4]
#         subjectivitys = row[5]
#         sql = f"""
#         DELETE FROM datatest
#         WHERE rowid = '{rowids}'
#         """
        
#         cursor.executescript(sql)
#         #continue
        
        
'''conn.commit()
for row in cursor.execute("SELECT rowid, * FROM datatest"):
    print(row)'''


# def datainsert(datalist):
#     cursor.executemany("INSERT INTO datatest VALUES (?,?,?,?,?)", datalist)
    
# def makelist(heading, publisher, article, date, sentiment, subjectivity):
#     datalist = [(heading, publisher, article, date, sentiment, subjectivity)]
#     return datalist


