# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
#database file
import sqlite3
import os
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('vader_lexicon')
import string
import time
import re

class ScraperPipeline:

    

    def process_item(self, item, spider):
        #check for scraper miss
        if  (not item['article']) or (item['headline'] == None) or (item['date'] == None):
            print(item['article'])
            print(item['headline'])
            print(item['date'])
            return item

        else:
            text = item['article']
            

            #normalize text (lowercase)
            textlower = [word.lower() for word in text]

            #remove all ampersans(&) and replace with "and"
            andText = [word.replace("texas a&m","tamu ") for word in textlower]
            wierdText = [word.replace("a&m's","tamu ") for word in andText]
            repText = [word.replace("a&m","tamu ") for word in wierdText]
            andsText = [word.replace("u.s.","united states ") for word in repText]
            wierdsText = [word.replace("u.s.'s ","united states") for word in andsText]
            for i in range(len(wierdsText)):
                wierdsText[i] = wierdsText[i].replace('-', ' ').replace('.', '').replace(',', '').replace(';', ' ').replace(':', ' ').replace('!', '').replace('?', '').replace('"', '').replace("'", '').replace('(', '').replace(')', '')
            for i in range(len(wierdsText)):
                wierdsText[i] = wierdsText[i].replace(' us ', ' ')
            

            #split text for cleaning
            split_text = [word.split() for word in wierdsText]
            split_text = [word for sublist in split_text for word in sublist]
            split_text = [re.sub(r'\n', '', word) for word in split_text]
           
            #cleans text for all things not alphabetical
            
            #alphatext = [word for sublist in split_text for word in sublist if word.isalpha()]
            alphatext = [word for word in split_text if word.isalpha()]
            #get stopwords from NLTK stopwords package
            NLTKstopwords = set(stopwords.words('english'))

            #clean text by saying that if the word is not in nltk stopwords list,
            #then add that word to the cleantext list
            cleantext = [word for word in alphatext if word not in NLTKstopwords]

            #lemmatize text
            wl = WordNetLemmatizer()
            lemText = [wl.lemmatize(y) for y in cleantext]

            articlestring = " ".join(lemText)
        
            item['article'] = articlestring
            

            heading =item['headline']
            #now clean the headings 
            headinglower = heading.lower() 
            andTextHead = headinglower.replace("texas a&m","tamu ")
            wierdTextHead = andTextHead.replace("a&m's","tamu ")
            repTextHead = wierdTextHead.replace("a&m","tamu ") 
            andsTextHead = repTextHead.replace("u.s.","united states ")
            wierdsTextHead = andsTextHead.replace("u.s.'s","united states")
            puncTextHead = wierdsTextHead.replace('-', ' ').replace('.', '').replace(',', '').replace(';', ' ').replace(':', ' ').replace('!', '').replace('?', '').replace('"', '').replace("'", '').replace('(', '').replace(')', '')
            puncTextHead = puncTextHead.replace(' us ', '')
            #split into list of words
            split_heading = puncTextHead.split()

            
            # String containing all punctuation characters
            punctuation_chars = string.punctuation +'-'

            # Remove punctuation from each word
            #alphahead = [word.translate(str.maketrans('', '', punctuation_chars)) for word in split_heading]
            #alphahead = [word.replace(char, ' ') for word in split_heading for char in punctuation_chars]

            #+clean headings for all things not alphabetical
            alhead = [word for word in split_heading if word.isalpha()]

            #remove stopwords from the alphabetical words
            cleanhead = [word for word in alhead if word not in NLTKstopwords]
            lemhead = [wl.lemmatize(y) for y in cleanhead]
            headstring = " ".join(lemhead)
            item['headline'] = headstring
            
            
            
            
            if  (not item['article']) or (item['headline'] == None) or (item['date'] == None):
                return item

            self.con = sqlite3.connect('V:/Capstone.db')
            #local
            #self.con = sqlite3.connect('cnnData.db')
            #create my cursur
            self.cur = self.con.cursor()
            
            #create table if none exits
            self.cur.execute("""
            CREATE TABLE IF NOT EXISTS RawData_3_18(
                Headline TEXT,
                Date TEXT,
                Article TEXT,
                Publisher TEXT,
                Website TEXT
                
            )
            """)
            os.chmod("V:/Capstone.db", 0o777) 

            ## Check to see if text is already in database 
            self.cur.execute("select * from RawData_3_18 where Headline = ?", (headstring,))
            result = self.cur.fetchone()

            ## If it is in DB, create log message
            #Check both article and headline
            if result:
                spider.logger.warn("Item already in database: %s" % headstring)
                self.con.close()
                return item

            self.cur.execute("select * from RawData_3_18 where Article = ?", (articlestring,))
            result = self.cur.fetchone()

            if result:
                spider.logger.warn("Item already in database: %s" % articlestring)
                self.con.close()
                return item

            ## If text isn't in the DB, insert data
            else:

                ## Define insert statement
                self.cur.execute("""
                INSERT INTO RawData_3_18(Headline, Date, Article, Publisher, Website) VALUES (?, ?, ?, ?, ?)
            """,
            (
                item['headline'],
                item['date'],
                item['article'],
                item['publisher'],
                item['website']
                
            ))

                ## Execute insert of data into database
                self.con.commit()
            time.sleep(2)
            self.con.close()
            return item
    
         ## Define insert statement
         #check if empty
        #if item['article'] == [] | item['headline'] == '' | item['date'] == '':
        #    return item
        #else:
         #   self.cur.execute("""
          #      INSERT INTO capstone(headline, date, article, publisher, sentiment, subjectivity) VALUES (?, ?, ?, ?, ?, ?)
           # """,
            #(
             #   item['headline'],
              #  item['date'],
               # str(item['article']),
               # item['publisher'],
               # item['sentiment'],
               # item['subjectivity']
            #))

        ## Execute insert of data into database
        #self.con.commit()
        #return item
