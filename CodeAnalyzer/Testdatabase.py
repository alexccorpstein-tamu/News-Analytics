# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 13:47:25 2023

@author: Alex
"""
import sqlite3
import os

import pandas as pd
from tqdm import tqdm


filename = 'C:\\Users\\jimni\\LocalCapstone\\demo_topic_csv\\topic0.csv'
df = pd.read_csv(filename)
df = df.drop(labels = "Unnamed: 0", axis = 1)



#print(df.columns)

datas = []
for i in df.index:
    insert_data = [df["index"].loc[i], df["topic"].loc[i], df["article"].loc[i], df["neg"].loc[i], df["neu"].loc[i], df["pos"].loc[i], df["compound"].iloc[i], df["Subjectivity"].loc[i], df["Sentiment"].loc[i], df["Topic Prob"].loc[i]]
    #print(i)
    datas.append(insert_data)
    #print(type(insert_data[8]))
    #print(df["article"].loc[i],'\n')

#print(type(df['index'].loc[0]))

conn = sqlite3.connect('T:\\Newtest3.db', timeout = 5)

#os.chmod("T:\\Testconnection.db", 0o777)

cursor = conn.cursor()

looping = True





while(looping):
    answer = str(input("What would you like to do:\n\nCREATE TABLE(C), FILL (F), READ (R), OR DELETE TABLE (D): "))
    
    if answer != 'C' and answer != 'F' and answer != 'R' and answer != 'D' and answer != 'c' and answer != 'f' and answer != 'r' and answer != 'd':
        print('You did not enter a valid action!')
        looping = False
    
    
    
    
###########CREATE FUNCTION#############################    
    elif answer == "C" or answer == "c":
        
        table_name = str(input("What do you want to name the new table: \n"))
        with conn:
            sql = f""" 
            CREATE TABLE IF NOT EXISTS '{table_name}'
            (topic TEXT, article TEXT, neg REAL,
             neu REAL, pos REAL, compound REAL, sentiment REAL, subjectivity REAL,
             topic_prob REAL)
            """
            cursor.executescript(sql)
            
        
        
        
###########FILL FUNCTION#############################        
    elif answer == "F" or answer == "f":
        table_name = str(input("What table do you want to fill: "))
                
        for i in tqdm (df.index):
            insert_data = (df["topic"].loc[i], df["article"].loc[i], df["neg"].loc[i], df["neu"].loc[i], df["pos"].loc[i], df['compound'].loc[i], df["Sentiment"].loc[i], df["Subjectivity"].loc[i], df["Topic Prob"].loc[i])
                    
                    
                    
            with conn:
                sql = "INSERT INTO {} VALUES (?,?,?,?,?,?,?,?,?)".format(table_name)
                cursor.execute(sql, insert_data)
           

        
        #cursor.executemany("INSERT INTO topic0_test VALUES (?,?,?,?,?,?,?,?,?)", datas)
    
    
    
    
###########READ FUNCTION#############################
    elif answer == 'R' or answer == 'r':
        table_name = str(input("What table do you want to read from: "))
        read_df = pd.DataFrame(columns = ["Topic", 'Article', 'Neg', 'Neu', 'Pos', 'Compound', 'Sentiment', 'Subjectivity', 'Topic Prob'])
        
        for row in cursor.execute("SELECT rowid, * FROM {}".format(table_name)):
                topic = row[1]
                article = row[2]
                neg = row[3]
                neu = row[4]
                pos = row[5]
                compound = row[6]
                
                
                Sentiment = row[7]
                Subjectivity = row[8]
                '''date = old_df["date"].iloc[j[0]]'''
                topic_prob = row[9]
                        #print(topic_df.columns)
                insert_row = pd.Series([topic, article, neg, neu, pos, compound, Sentiment, Subjectivity, topic_prob], index = read_df.columns)
                #print(row)
                
                read_df.loc[-1] = insert_row
                read_df.index = read_df.index + 1
                
        print("The data was put into the following pandas Dataframe")

        print(read_df)
                
                
                
                
                
###########DELETE FUNCTION#############################    
    elif answer == "D" or answer == 'd':
        table_name = str(input("What table do you want to delete: "))

                 
        cursor.execute("DROP TABLE {}".format(table_name))
        conn.commit()
        
        
        #Following is code used to delete rows, could be useful if I
        #don't want to delete the whole table and rather specific rows
        '''for row in tqdm(cursor.execute("SELECT rowid, * FROM topic0_test")):    
                 rowids = row[0]    

                 sql = f"""
                 DELETE FROM topic0_test
                 WHERE rowid = '{rowids}'
                 """
            
                 cursor.executescript(sql)
                 conn.commit()'''
        
     
#Following is just to print out each row to terminal
'''
for row in cursor.execute("SELECT rowid, * FROM datatest"):
    print(row)'''




conn.close()



