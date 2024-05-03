import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from Scraper.items import ScraperItem
from datetime import datetime


class KBTXSpider(scrapy.Spider):
    name = 'kbtx'
    #allowed_domains = ['https://www.kbtx.com/']
    start_urls = ['https://www.kbtx.com/']
    
    # initiating selenium
    def start_requests(self):
        
        # set up the driver
        chrome_options = Options()
        #chrome_options.add_argument("--headless") # uncomment if don't want to appreciate the sight of a possessed browser
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://www.kbtx.com/")
        
        # begin search
        time.sleep(10)
        search_input = driver.find_element(By.XPATH , '/html/body/div[1]/div/nav/div[1]/div/div/label/i') # find the search butten
        search_input.click()
        time.sleep(5)
        
        search_input = driver.find_element(By.XPATH , '//*[@id="queryly_query"]')#find search bar
        search_input.click()
        #Write what we be searched#
        search_input.send_keys('TAMU')
        time.sleep(1)
        search_input = driver.find_element(By.XPATH , '//*[@id="advanced_searchbutton"]')
        search_input.click()
        
        
        time.sleep(1)
        search_input = driver.find_element(By.XPATH , '/html/body/div[1]/div/div/div/div[1]/section[1]/div[3]/div/div[1]/div[3]/div[2]/a')
        search_input.click()
        time.sleep(5)
        # Begin Crawling
        self.driver = driver
        yield from self.parse_search_results(driver)

            
    def parse_search_results(self, driver):
        # start turning pages
        i = 1
        urllist =[]
        '''l=1
        try:
            while l < 8:
                if l == 1:
                    next_btn = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[1]/section[1]/div[3]/div/div[2]/a')
                    next_btn.click() # click next button
                    time.sleep(5)
                else:
                    next_btn = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[1]/section[1]/div[3]/div/div[2]/a[1]')
                    next_btn.click()
                    time.sleep(5)
                l+=1
        except:
            with open('textfile.txt', 'a') as f:
                f.write("Failed try to get to correct page" + str(l) + '\n')
                f.close'''





        while i < 4: #6 is 100
            j=3 #starts at 3
            while j<= 22: #goes to 22
                #go into article then come out save the url
                try:
                    time.sleep(5)
                    linkbtn = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[1]/section[1]/div[3]/div/div[2]/div['+str(j)+']/a/div[2]/div[1]')
                    
                    
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
                  
            

                    #next to get back to right page -no loneger needed
                    #if i >= 2:
                        #k = i - 1
                        #firsttime = 0
                       # while k != 0:
                            #k = k-1   
                           # time.sleep(2) 
                           # if firsttime == 0:
                           #     next_btn = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[1]/section[1]/div[3]/div/div[2]/a')
                           #     next_btn.click() # click next button
                          #      firsttime = 1
                          #  else:
                           #     next_btn = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[1]/section[1]/div[3]/div/div[2]/a[1]')
                           #     next_btn.click()

            i += 1
            
            time.sleep(5) 
            try:
                if i == 2:
                    next_btn = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[1]/section[1]/div[3]/div/div[2]/a')
                    next_btn.click() # click next button
                else:
                    next_btn = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[1]/section[1]/div[3]/div/div[2]/a[1]')
                    next_btn.click()
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
        headline = response.xpath('/html/body/div[1]/div/div/div/div/div/section[1]/div/div[1]/h1/span//text()').get()
        
        
        # need to remove extra information
        #need better way for htis
        
        datelist = response.xpath("/html/body/div[1]/div/div/div/div/div/section[1]/div[1]/div[3]/span[1]//text()").extract()
        if not datelist:
            datelist = response.xpath("/html/body/div[1]/div/div/div/div/div/section[1]/div/div[4]/span//text()").extract()
            if not datelist:
                datelist = response.xpath("/html/body/div[1]/div/div/div/div/div/section[1]/div/div[4]/span[1]//text()").extract()
        #print(datelist)
        #/html/body/div[1]/div/div/div/div/div/section[1]/div[1]/div[3]/span[1]
        #/html/body/div[1]/div/div/div/div/div/section[1]/div/div[4]/span
        #/html/body/div[1]/div/div/div/div/div/section[1]/div/div[4]/span[1]
        
        try:
            datestring = datelist[2]
            #print(datestring)
        except:
            datestring = None
        
        try:
        # Remove timezone information
            date_string = datestring.split(" at ")[0]

        # Convert to datetime object
            date_object = datetime.strptime(date_string, "%b. %d, %Y")

        # Format to month/day/year format
            formatted_date = date_object.strftime("%m/%d/%Y")
        except:
            formatted_date = None
        
        i=1
        j=1
        k=1
        l=1
        article = []
        while True:
            paragraph = response.xpath(f'/html/body/div[1]/div/div/div/div/div/section[2]/div/div[2]/div/p[{i}]//text()').getall()
            paragraphstring = ''.join(paragraph)
            if not paragraph:
                paragraph = response.xpath(f'/html/body/div[1]/div/div/div/div/div/section[2]/div/p[{i}]//text()').getall()
                paragraphstring = ''.join(paragraph)
            if paragraph:
                i+=1
            else:
                if not paragraph:
                    paragraph = response.xpath(f'/html/body/div[1]/div/div/div/div/div/section[2]/div/div[2]/div/h2[{j}]//text()').getall()
                    paragraphstring = ''.join(paragraph)
                if paragraph:
                    j += 1
                else:
                    if not paragraph:
                        paragraph = response.xpath(f'/html/body/div[1]/div/div/div/div/div/section[2]/div/div[2]/div/ul[{k}]//text()').getall()
                        paragraphstring = ''.join(paragraph)
                    if paragraph:
                        k+=1
                    else:
                        if not paragraph:
                            paragraph = response.xpath(f'/html/body/div[1]/div/div/div/div/div/section[2]/div/div[2]/div/h3[{j}]//text()').getall()
                            paragraphstring = ''.join(paragraph)
                        if paragraph:
                            l += 1

            if not paragraph:
                break
            article.append(paragraphstring)
            
        #strarticle=""
        #check = response.xpath('/html/body/div[1]/div/div/div/div/div/section[2]/div/p['+str(i)+']//text()')
        #while len(check) >0:
            #article.append(response.xpath('/html/body/div[1]/div/div/div/div/div/section[2]/div/p['+str(i)+']//text()').get())
            #i+=1
            #check = response.xpath('/html/body/div[1]/div/div/div/div/div/section[2]/div/p['+str(i)+']//text()')
        #this might not be need
        #for a in article:
         #   strarticle += a
            
        
        if  (not article) or (headline == None) or (formatted_date == None):
            with open('textfile.txt', 'a') as f:
                if not article:
                    f.write("Miss article " + response.url + '\n')
                if headline == None:
                    f.write("Miss headline " + response.url + '\n')
                if datestring == None:
                    f.write("Miss date " + response.url + '\n')
                f.close
        
        publisher = 'kbtx'
        neg = '0'
        neu = '0'
        pos = '0'
        compound = '0'
        sentiment = '0'
        subjectivity = '0'
       
        

       # weblist = str(response).split()
       # web = weblist[1]
        #web = web.replace('>', '')

        capitem['headline'] = headline
        capitem['date'] = formatted_date
        capitem['article'] = article
        capitem['publisher'] = publisher
        capitem['website'] = response.url
        
        
        yield capitem

        '''yield {
            "headline": headline,
            "article": article, 
            "date": date,
            "publisher" : publisher,
            "sentiment" : sentiment,
            "subjectivity" : subjectivity
            
        }'''