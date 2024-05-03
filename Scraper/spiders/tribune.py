import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from Scraper.items import ScraperItem

from datetime import datetime


class TribuneSpider(scrapy.Spider):
    name = 'tribune'
    #allowed_domains = ['www.texastribune.org']
    start_urls = ['https://www.texastribune.org/']
    
    # initiating selenium
    def start_requests(self):
        
        # set up the driver
        chrome_options = Options()
        #chrome_options.add_argument("--headless") # uncomment if don't want to appreciate the sight of a possessed browser
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://www.texastribune.org/")
        
        # begin search
        search_input = driver.find_element(By.XPATH , '//*[@id="nav-search-open"]') # find the search butten
        search_input.click()
        time.sleep(5)
        search_input = driver.find_element(By.XPATH , '/html/body/nav/div[1]/div[2]/form/input')#find search bar
        #Write what we be searched#
        search_input.send_keys('Texas A&M')
        search_input.send_keys(Keys.RETURN)
        time.sleep(5)
        #change to sort by date
        '''search_input = driver.find_element(By.XPATH , '/html/body/div[3]/div/main/div/div/div/div/div/div[3]/table/tbody/tr/td[2]/div/div[2]/div[1]/div[1]')
        search_input.click()
        time.sleep(1)
        search_input = driver.find_element(By.XPATH , '/html/body/div[3]/div/main/div/div/div/div/div/div[3]/table/tbody/tr/td[2]/div/div[2]/div[2]/div[2]/div')
        search_input.click()'''    
        time.sleep(5)
        # Begin Crawling
        self.driver = driver
        yield from self.parse_search_results(driver)

            
    def parse_search_results(self, driver):
        # start turning pages
        i = 1
        urllist =[]
        
        while i < 2: #max 11
            j=1
            while j<= 3: #max 10
                #go into article then come out save the url
                try:
                    time.sleep(5)
                    linkbtn = driver.find_element(By.XPATH, '/html/body/div[3]/div/main/div/div/div/div/div/div[5]/div[2]/div/div/div[1]/div['+str(j)+']/div[1]/div[1]/div/a')
                    linkbtn.click()
                    time.sleep(5)
                    
                    urllist.append(driver.current_url)
                    time.sleep(1)
                    j+=1
                    driver.back()
                except:
                    with open('textfile.txt', 'a') as f:
                        f.write("missed url "+ str(j) + " page " + str(i) + '\n')
                        f.closed
                    #misslised appedn it
                    j+=1
        
         
            i += 1
            #No next butten must click 2-10
            time.sleep(5) 
            try:
                if i < 10:
                    next_btn = driver.find_element(By.XPATH, '/html/body/div[3]/div/main/div/div/div/div/div/div[5]/div[2]/div/div/div[2]/div/div['+ str(i) +']') # click next button
                    next_btn.click()
            except:
                with open('textfile.txt', 'a') as f:
                    f.write("failed on page " + str(i) + '\n')
                    f.close
                    #misslised appedn it
                # miss list
        #parse each url

        # saved as text file for missed option
        # np . save text

        for url in urllist:
            yield scrapy.Request(url, callback=self.parse_article)
            
 
    # pass on the links to open and process actual news articles
    def parse_article(self, response):

        capitem = ScraperItem()
        headline = response.xpath('/html/body/main/article/section[1]/header/div/h1//text()').get()
        #need try and except and failed conditions
        date = response.xpath("/html/body/main/article/section[1]/header/div/div[2]/div[2]/time[1]//text()").get()
        
        try:
        # Convert to datetime object
            date_object = datetime.strptime(date, "%b. %d, %Y")

        # Format to month/day/year format
            formatted_date = date_object.strftime("%m/%d/%Y")
        except:
            try:
                date_object = datetime.strptime(date, "%B %d, %Y")

        # Format to month/day/year format
                formatted_date = date_object.strftime("%m/%d/%Y")
            except:
                formatted_date = None
            
        i=1
        article = []
        while True:
            paragraph = response.xpath(f'/html/body/main/article/div[2]/div/p[{i}]//text()').getall()
            paragraphstring = ''.join(paragraph)
            if not paragraph:
                paragraph = response.xpath(f'/html/body/main/article/div[2]/div/p[{i}]/span//text()').getall()
                paragraphstring = ''.join(paragraph)
            if not paragraph:
                paragraph = response.xpath(f'/html/body/main/article/div[2]/p[{i}]/span//text()').getall()
                paragraphstring = ''.join(paragraph)
            if not paragraph:
                paragraph = response.xpath(f'/html/body/main/article/div[2]/p[{i}]//text()').getall()
                paragraphstring = ''.join(paragraph)

            if not paragraph:
                i += 1
                paragraph = response.xpath(f'/html/body/main/article/div[2]/div/p[{i}]//text()').getall()
                paragraphstring = ''.join(paragraph)
            if not paragraph:
                paragraph = response.xpath(f'/html/body/main/article/div[2]/div/p[{i}]/span//text()').getall()
                paragraphstring = ''.join(paragraph)
            if not paragraph:
                paragraph = response.xpath(f'/html/body/main/article/div[2]/p[{i}]/span//text()').getall()
                paragraphstring = ''.join(paragraph)
            if not paragraph:
                paragraph = response.xpath(f'/html/body/main/article/div[2]/p[{i}]//text()').getall()
                paragraphstring = ''.join(paragraph)
            if not paragraph:
                break
            article.append(paragraphstring)
            i += 1
        #check = response.xpath('/html/body/main/article/div[2]/div/p['+str(i)+']//text()')
        #if not check:
           # check = response.xpath('/html/body/main/article/div[2]/div/p['+str(i)+']/span//text()')
          #  article.append(response.xpath('/html/body/main/article/div[2]/div/p['+str(i)+']/span//text()').get())
          #  while len(check) >0:
           #     article.append(response.xpath('/html/body/main/article/div[2]/div/p['+str(i)+']//text()').get())
           #     i+=1
           #     check = response.xpath('/html/body/main/article/div[2]/div/p['+str(i)+']//text()')
       # else:
           # while len(check) >0:
           #     article.append(response.xpath('/html/body/main/article/div[2]/div/p['+str(i)+']//text()').get())
          #      i+=1
          #      check = response.xpath('/html/body/main/article/div[2]/div/p['+str(i)+']//text()')
        
        if  (not article) or (headline == None) or (formatted_date == None):
            with open('textfile.txt', 'a') as f:
                if not article:
                    f.write("Miss article " + response.url + '\n')
                if headline == None:
                    f.write("Miss headline " + response.url + '\n')
                if date == None:
                    f.write("Miss date " + response.url + '\n')
                f.close


        publisher = 'texas tribune'
        neg = 0
        neu = 0
        pos = 0
        compound = 0
        sentiment = 0
        subjectivity = 0
        
        #weblist = str(response).split()
        #web = weblist[1]
       # web = web.replace('>', '')
        
        capitem['headline'] = headline
        capitem['date'] = formatted_date
        capitem['article'] = article
        capitem['publisher'] = publisher
        capitem['website'] = response.url
        #capitem['neg'] = neg
        #capitem['neu'] = neu
        #capitem['pos'] = pos
        #capitem['compound'] = compound
        #capitem['sentiment'] = sentiment
        #capitem['subjectivity'] = subjectivity
        time.sleep(1)
        yield capitem

        #yield {
         #   "headline": headline,
         #   "article": article, 
         #   "date": date,
         #   "publisher" : publisher,
         #   "sentiment" : sentiment,
         #   "subjectivity" : subjectivity
            
        #}