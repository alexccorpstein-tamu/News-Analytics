import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from Scraper.items import ScraperItem
from datetime import datetime

class CnnSpider(scrapy.Spider):
    name = 'cnn'
    allowed_domains = ['www.cnn.com']
    start_urls = ['https://www.cnn.com']
    
    # initiating selenium
    def start_requests(self):
        
        # set up the driver
        chrome_options = Options()
        #chrome_options.add_argument("--headless") # uncomment if don't want to appreciate the sight of a possessed browser
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://www.cnn.com")
        
        # begin search
        time.sleep(5)
        search_input = driver.find_element(By.XPATH , '//*[@id="headerSearchIcon"]') # find the search butten
        search_input.click()
        time.sleep(5)
        search_input = driver.find_element(By.XPATH , '/html/body/header/div/nav/div/div/div[2]/div/div[1]/form/input') # find the search bar
        time.sleep(5)
        
        
        #write what we want searched
        search_input.send_keys('Texas A&M')
        search_input.send_keys(Keys.RETURN)
        time.sleep(5)
        
        #search by relvancy
        #rev_btn = driver.find_element(By.XPATH, '//*[@id="relevance"]')
        #rev_btn.click()
        time.sleep(2)

        stor_btn = driver.find_element(By.XPATH, '/html/body/div[1]/section[3]/section[1]/div/section/section/div/div[1]/div[2]/div/div/ul/li[2]/label')
        stor_btn.click()
        time.sleep(2)
        #Begin crawling 
        self.driver = driver
        yield from self.parse_search_results(driver)
        
            
    def parse_search_results(self, driver):
        
        
        l=1
        try:
            while l <= 1:
                next_btn = driver.find_element(By.XPATH, '/html/body/div[1]/section[3]/section[1]/div/section/section/div/div[2]/div/div[4]/div/div[3]') # click next button
                next_btn.click()
                time.sleep(5)
                l+=1
        except:
            with open('textfile.txt', 'a') as f:
                    f.write("Failed try to get to correct page" + str(l) + '\n')
                    f.close 
        
        # start turning pages
        i = 1
        urllist =[]
        while i < 10:
            j=1
            while j<= 10: #max 10
                #go into article then come out save the url
                try:
                    time.sleep(5)
                    linkbtn = driver.find_element(By.XPATH, '/html/body/div[1]/section[3]/section[1]/div/section/section/div/div[2]/div/div[2]/div/div[2]/div/div/div['+str(j)+']/a/div/div[1]/span')
                    linkbtn.click()
                    time.sleep(5)
              
                    urllist.append(driver.current_url)
                    time.sleep(1)
                    j+=1
                    driver.back()
                
                except:
                    with open('textfile.txt', 'a') as f:
                        
                        f.write("missed url "+ str(j) + " page " + str(i) + '\n')
                        f.close
                    j+=1
            #Next butten    
            i += 1
            time.sleep(5) 
            try:
                next_btn = driver.find_element(By.XPATH, '/html/body/div[1]/section[3]/section[1]/div/section/section/div/div[2]/div/div[4]/div/div[3]') # click next button
                next_btn.click()
            except:
                 with open('textfile.txt', 'a') as f:
                    f.write("failed on page " + str(i-1) + '\n')
                    f.close  

        #parse each url
        for url in urllist:
            time.sleep(1)
            yield scrapy.Request(url, callback=self.parse_article)
            
    # pass on the links to open and process actual news articles
    def parse_article(self, response):

        capitem = ScraperItem()

        headline = response.xpath('//*[@id="maincontent"]//text()').get()
        if not headline:
            headline = response.xpath('/html/body/div[1]/section[3]/section/div/section/div/div/div[1]/div/div[3]/div[1]//text()').get()
        #two differnt paths for dates
        #need to remove extra information
        
        date = response.xpath("/html/body/div[2]/section[3]/div/div[2]/div[1]/div/div[2]/div[2]//text()").get()    
        if not date:
            date = response.xpath("/html/body/div[1]/section[2]/div[1]/div[2]/div[1]/div/div[2]/div[2]//text()").get()
        if not date:
            date = response.xpath("/html/body/div[1]/section[2]/div[1]/div[2]/div[1]/div/div[2]/div//text()").get()
            if not date:
                date = response.xpath("/html/body/div[2]/section[2]/div/div[2]/div[1]/div/div[2]/div[2]//text()").get()
                if not date:
                    date = response.xpath("/html/body/div[1]/section[3]/div/div[2]/div[1]/div/div[2]/div[2]//text()").get()
        
        if date == None:
            date = None
            
        else:
            # Extract date portion from the string
            datest = date.strip()
            datelist = datest.split(", ")
            date_string = datelist[-2] + " " + datelist[-1]

            # Convert to datetime object
            date_object = datetime.strptime(date_string, "%a %B %d %Y")

            # Format to month/day/year format
            date = date_object.strftime("%m/%d/%Y")
            






                               
        i=1
        article = []

        while True:
            paragraph = response.xpath(f'/html/body/div[2]/section[4]/section[1]/section[1]/article/section/main/div[2]/div[1]/p[{i}]//text()').getall()
            paragraphstring = ''.join(paragraph)
            '''if not paragraph:
                paragraph = response.xpath(f'/html/body/div[1]/section[3]/section/div/section/div/div/div[1]/div/div[3]/div[5]//text()').getall()
                paragraphstring = ''.join(paragraph)'''
            if not paragraph:
                paragraph = response.xpath(f'/html/body/div[1]/section[3]/section[1]/section[1]/article/section/main/div[2]/div[1]/p[{i}]//text()').getall()
                paragraphstring = ''.join(paragraph)
            ''' if not paragraph:
                paragraph = response.xpath(f'/html/body/div[1]/section[3]/section/div/section/div/div/div[1]/div/div[3]/div[6]//text()').getall()
                paragraphstring = ''.join(paragraph)'''
            if not paragraph:
                break
            article.append(paragraphstring)
            i+=1
            
        
        '''check = response.xpath('/html/body/div[1]/section[3]/section[1]/section[1]/article/section/main/div[2]/div[1]/p['+str(i)+']//text()')
        while len(check) >0:
            article.append(response.xpath('/html/body/div[1]/section[3]/section[1]/section[1]/article/section/main/div[2]/div[1]/p['+str(i)+']//text()').get())
            i+=1
            check = response.xpath('/html/body/div[1]/section[3]/section[1]/section[1]/article/section/main/div[2]/div[1]/p['+str(i)+']//text()')
        if not article: #check if no article could be a video for cnn
            article.append(response.xpath('/html/body/div[1]/section[3]/section/div/section/div/div/div[1]/div/div[3]/div[5]//text()').get())
            if not article:
                article = []
        else:
            articlestr = " ".join(article)'''
        
        if  (not article) or (headline == None) or (date == None):
            with open('textfile.txt', 'a') as f:
                if not article:
                    f.write("Miss article " + response.url + '\n')
                if headline == None:
                    f.write("Miss headline " + response.url + '\n')
                if date == None:
                    f.write("Miss date " + response.url + '\n')
                f.close

        #placeholder to keep csv formated with all field might not need
        publisher = 'cnn'
        neg = 0
        neu = 0
        pos = 0
        compound = 0
        sentiment = 0
        subjectivity = 0
        
        #weblist = str(response).split()
        #web = weblist[1]
        #web = web.replace('>', '')

        
        capitem['headline'] = headline
        capitem['date'] = date
        capitem['article'] = article
        capitem['publisher'] = publisher
        capitem['website'] = response.url
        time.sleep(1)
        yield capitem
        

        #yield {
         #   "headline": headline,
          #  "article": article, 
          #  "date": date,
          #  "publisher" : publisher,
          #  "neg" : neg,
          #  "neu" : neu,
          #  "pos" : pos,
          #  "compound" : compound,
          #  "sentiment" : sentiment,
          #  "subjectivity" : subjectivity
         #   
        #}