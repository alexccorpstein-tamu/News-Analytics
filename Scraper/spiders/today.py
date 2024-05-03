import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from Scraper.items import ScraperItem

from datetime import datetime

class TodaySpider(scrapy.Spider):
    name = 'today'
    #allowed_domains = ['www.texastribune.org']
    start_urls = ['https://today.tamu.edu/']
    
    # initiating selenium
    def start_requests(self):
        
        # set up the driver
        chrome_options = Options()
        #chrome_options.add_argument("--headless") # uncomment if don't want to appreciate the sight of a possessed browser
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://today.tamu.edu/")
        driver.fullscreen_window()
        time.sleep(2)
        
        #search_input = driver.find_element(By.XPATH , '/html/body/nav[2]/div/div/a[1]/span/span[1]') # find the search butten
        #search_input.click()
        time.sleep(1)
        # select between the five headers
        #campus life #40
        search_input = driver.find_element(By.XPATH , '/html/body/nav[2]/div[1]/div[2]/a[4]') # find the search butten
        #search_input.click()
        #health & enviroment?
        #search_input = driver.find_element(By.XPATH , '/html/body/nav[2]/div[1]/div[2]/a[5]') # find the search butten
        #search_input.click()
        #science and Tech #50
        #search_input = driver.find_element(By.XPATH , '/html/body/nav[2]/div[1]/div[2]/a[1]') # find the search butten
        #search_input.click()
        #bussines and gov done?
        #search_input = driver.find_element(By.XPATH , '/html/body/nav[2]/div[1]/div[2]/a[2]') # find the search butten
        #search_input.click()
        #arts and humanities done
        #search_input = driver.find_element(By.XPATH , '/html/body/nav[2]/div[1]/div[2]/a[3]') # find the search butten
        
        
        search_input.click()
        time.sleep(5)
        
        # Begin Crawling
        self.driver = driver
        yield from self.parse_search_results(driver)

            
    def parse_search_results(self, driver):
        # start turning pages
        i = 1
        l=1
        urllist =[]
        try:
            while l < 51:
                next_btn = driver.find_element(By.CLASS_NAME, 'pagination-next')    
                next_btn.click()
                time.sleep(5)
                l+=1
        except:
            with open('textfile.txt', 'a') as f:
                    f.write("Failed try to get to correct page" + str(l) + '\n')
                    f.close 


        while i < 10: #based thing
            j=1
            while j<= 10: #max 10
                #go into article then come out save the url
                try:
                    time.sleep(5)

                    linkbtn = driver.find_element(By.XPATH, '/html/body/div[1]/main/div/div/div[1]/div/ul/li['+str(j)+']/div/div[2]/h2/span/span/a')
                    #/html/body/div/main/div/div/div[1]/div/ul/li[1]/div/div[2]/h2/span/span/a
                   # /html/body/div/main/div/div/div[1]/div/ul/li[2]/div/div[2]/h2/span/span/a
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
                    #misslised appedn it
                    j+=1
        
         
            i += 1
            
            time.sleep(5) 
          
       
            try:
                #if i == 2:
                    #k = i+5
                next_btn = driver.find_element(By.CLASS_NAME, 'pagination-next')    
                    #next_btn = driver.find_element(By.XPATH, '/html/body/div[1]/main/div/div/div[2]/div/ul/li[7]/a') # click next button
                next_btn.click()
                time.sleep(5)
                #/html/body/div/main/div/div/div[2]/div/ul/li[8]/a/span/span[1]
                #/html/body/div/main/div/div/div[2]/div/ul/li[7]/a/span/span[1]
                    
                    
                #else:
                    #next_btn = driver.find_element(By.XPATH, '/html/body/div/main/div/div/div[2]/div/ul/li[8]/a') # click next button
                    #next_btn.click()
            except:
                
                with open('textfile.txt', 'a') as f:
                    f.write("failed on page " + str(i-1) + '\n')
                    f.close 
                # miss list
        #parse each url

        # saved as text file for missed option
        # np . save text

        for url in urllist:
            yield scrapy.Request(url, callback=self.parse_article)
            
 
    # pass on the links to open and process actual news articles
    def parse_article(self, response):

        capitem = ScraperItem()
        headline = response.xpath('/html/body/div[1]/main/div[1]/div/h1/span//text()').get()
        #need try and except and failed conditions
        date = response.xpath("/html/body/div[1]/main/div[1]/div/div[2]/span[2]//text()").get()
        
        # Convert to datetime object
        try:
            date_object = datetime.strptime(date, "%B %d, %Y")
        # Format to month/day/year format
            formatted_date = date_object.strftime("%m/%d/%Y")
        except:
            formatted_date = None
        if formatted_date == None:
            date = response.xpath("/html/body/div/main/div[1]/div/div[2]/span//text()").get()

            try:
                date_object = datetime.strptime(date, "%B %d, %Y")

        # Format to month/day/year format
                formatted_date = date_object.strftime("%m/%d/%Y")
            except:
                formatted_date = None
        
        if formatted_date == None:
            date = response.xpath("/html/body/div/main/div[1]/div/div[2]/span[2]//text()").get()

            try:
                date_object = datetime.strptime(date, "%B %d, %Y")

        # Format to month/day/year format
                formatted_date = date_object.strftime("%m/%d/%Y")
            except:
                formatted_date = None

        i=1
        article = []
        
        while True:
            paragraph = response.xpath(f'/html/body/div[1]/main/div[2]/div/div[1]/div[1]/p[{i}]//text()').getall()
            paragraphstring = ''.join(paragraph)
            if not paragraph:
                paragraph = response.xpath(f'/html/body/div/main/div[2]/div/div[1]/div[1]/p[{i}]//text()').getall()
                paragraphstring = ''.join(paragraph)
            if not paragraph:
                paragraph = response.xpath(f'/html/body/div/main/div[2]/div/div/div[1]/p[{i}]//text()').getall()
                paragraphstring = ''.join(paragraph)
            
            if not paragraph:
                i += 1
                paragraph = response.xpath(f'/html/body/div[1]/main/div[2]/div/div[1]/div[1]/p[{i}]//text()').getall()
                paragraphstring = ''.join(paragraph)
            if not paragraph:
                paragraph = response.xpath(f'/html/body/div/main/div[2]/div/div[1]/div[1]/p[{i}]//text()').getall()
                paragraphstring = ''.join(paragraph)
            if not paragraph:
                paragraph = response.xpath(f'/html/body/div/main/div[2]/div/div/div[1]/p[{i}]//text()').getall()
                paragraphstring = ''.join(paragraph)
           
            if not paragraph:
                i += 1
                paragraph = response.xpath(f'/html/body/div[1]/main/div[2]/div/div[1]/div[1]/p[{i}]//text()').getall()
                paragraphstring = ''.join(paragraph)
            if not paragraph:
                paragraph = response.xpath(f'/html/body/div/main/div[2]/div/div[1]/div[1]/p[{i}]//text()').getall()
                paragraphstring = ''.join(paragraph)
            if not paragraph:
                paragraph = response.xpath(f'/html/body/div/main/div[2]/div/div/div[1]/p[{i}]//text()').getall()
                paragraphstring = ''.join(paragraph)
            if not paragraph:
                break
            article.append(paragraphstring)
            i += 1


        #check = response.xpath('/html/body/div[1]/main/div[2]/div/div[1]/div[1]/p['+str(i)+']//text()')
        #while len(check) >0:
            #article.append(response.xpath('/html/body/div[1]/main/div[2]/div/div[1]/div[1]/p['+str(i)+']//text()').get())
            #i+=1
            #check = response.xpath('/html/body/div[1]/main/div[2]/div/div[1]/div[1]/p['+str(i)+']//text()')
        
        if  (not article) or (headline == None) or (formatted_date == None):
            with open('textfile.txt', 'a') as f:
                if not article:
                    f.write("Miss article " + response.url + '\n')
                if headline == None:
                    f.write("Miss headline " + response.url + '\n')
                if date == None:
                    f.write("Miss date " + response.url + '\n')
                f.close
    
        publisher = 'tamu today'
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
        capitem['date'] = formatted_date
        capitem['article'] = article
        capitem['publisher'] = publisher
        capitem['website'] = response.url
        #capitem['neu'] = neu
        #capitem['pos'] = pos
        #capitem['compound'] = compound
        #capitem['sentiment'] = sentiment
        #capitem['subjectivity'] = subjectivity
        time.sleep(2)
        yield capitem

        '''yield {
            "headline": headline,
            "article": article, 
            "date": date,
            "publisher" : publisher,
            "sentiment" : sentiment,
            "subjectivity" : subjectivity
            
        }'''

        ''' for trouble shooting
                 xpath = f'/html/body/div/main/div[2]/div/div[1]/div[1]/p[{i}]//text()'
                
                # Print the XPath to inspect
                self.logger.info(f"XPath: {xpath}")

                # Extract the text using the XPath
                paragraph_text = response.xpath(xpath).getall()
                # Print the extracted text
                self.logger.info(f"Paragraph text: {paragraph_text}")'''