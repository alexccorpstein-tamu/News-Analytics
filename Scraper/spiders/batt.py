import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from Scraper.items import ScraperItem
from datetime import datetime
from selenium.webdriver import ActionChains


class BattSpider(scrapy.Spider):
    name = 'batt'
    #allowed_domains = ['www.texastribune.org']
    start_urls = ['https://www.thebatt.com/']
    
    # initiating selenium
    def start_requests(self):
        
        # set up the driver
        chrome_options = Options()
        #chrome_options.add_argument("--headless") # uncomment if don't want to appreciate the sight of a possessed browser
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://www.thebatt.com/")
        #driver.fullscreen_window()
        time.sleep(1)
        # begin search
       
        #search_input = driver.find_element(By.XPATH , '/html/body/div[6]/div[5]/nav/div[2]/div[1]/div/div/ul/li/a') # find the search butten
        #search_input.click()
        time.sleep(5)
        search_input = driver.find_element(By.XPATH , '//*[@id="s-desktop-11"]')#find search bar
        
        #Write what we be searched#
        search_input.send_keys('A&M')
        search_input.send_keys(Keys.RETURN)
        time.sleep(5)
        #change to sort by date
        #search_input = driver.find_element(By.XPATH , '/html/body/div[5]/div[5]/section[2]/div[2]/div[1]/div/div[2]/form/div[3]/a/span[1]')
        #search_input.click()
        #time.sleep(1)
        #search_input = driver.find_element(By.XPATH , '//*[@id="input-type-videos"]')
        #search_input.click() 
        #time.sleep(1)
        #search_input = driver.find_element(By.XPATH , '//*[@id="input-type-collections"]')
        #search_input.click()    
       # time.sleep(1)
        #search_input = driver.find_element(By.XPATH , '/html/body/div[5]/div[5]/section[2]/div[2]/div[1]/div/div[2]/form/div[2]/div/div[3]/div/button')
        #search_input.click()    
        
        
        #time.sleep(5)
        # Begin Crawling
        self.driver = driver
        yield from self.parse_search_results(driver)

            
    def parse_search_results(self, driver):
        # start turning pages
        
        urllist =[]
        
        #while i < 2: #max 11
        j=1
        while j<= 3: 
                #go into article then come out save the url
            #driver.fullscreen_window()
            screen_height = driver.execute_script("return window.screen.height;")
            
            scroll_pause_time = 2
            i = 1
            try:
                time.sleep(5)
                iframe = driver.find_element(By.XPATH, '//*[@id="contentleft"]/div/div['+str(j)+']/div/div[2]/h2/a')
                ActionChains(driver)\
                    .scroll_to_element(iframe)\
                    .perform()
                time.sleep(2)
                
                try:
                    adbtn = driver.find_element(By.XPATH, '/html/body/div[9]/div/div[2]')
                    
                    adbtn.click()
                    time.sleep(2)
                except:
                    with open('textfile.txt', 'a') as f:
                        f.write("missed ad "+ str(j) + " page " + str(i) + '\n')
                        f.close
                try:
                    adbtn = driver.find_element(By.XPATH, '/html/body/div[8]/div/div[2]')
                    adbtn.click()
                    time.sleep(2)
                except:
                    with open('textfile.txt', 'a') as f:
                        f.write("missed ad "+ str(j) + " page " + str(i) + '\n')
                        f.close
                linkbtn = driver.find_element(By.XPATH, '//*[@id="contentleft"]/div/div['+str(j)+']/div/div[2]/h2/a')
                    #//*[@id="contentleft"]/div/div[1]/div/div[2]/h2/a
                    #//*[@id="contentleft"]/div/div['+str(j)+']/div/div[2]/h2/a
                    #/html/body/div[2]/div[4]/div/div/div/main/div/div[1]/div/div[2]/div/div[2]/h2/a
                    #/html/body/div[1]/div[4]/div/div/div/main/div/div[1]/div/div[2]/div/div[2]/h2/a
                
                linkbtn.click()
                time.sleep(5)
                    
                urllist.append(driver.current_url)
                time.sleep(1)
                j+=1
                driver.back()

                #iframe = driver.find_element(By.XPATH, '//*[@id="wrap"]/div[6]/div[1]/div[1]/div/div[3]/div[1]/div/div/img')
                #ActionChains(driver)\
                    #.scroll_to_element(iframe)\
                    #.perform()
            except:
                with open('textfile.txt', 'a') as f:
                    f.write("missed url "+ str(j) + " page " + str(i) + '\n')
                    f.close
                    #misslised appedn it
                j+=1
            
            try:
                
                if j == 6:
                    time.sleep(1)
                    try:
                        adbtn = driver.find_element(By.XPATH, '/html/body/div[9]/div/div[2]')


                        adbtn.click()
                        time.sleep(2)
                    except:
                        with open('textfile.txt', 'a') as f:
                            f.write("missed ad "+ str(j) + " page " + str(i) + '\n')
                            f.close
                    iframe = driver.find_element(By.XPATH, '//*[@id="contentleft"]/div/div[16]')
                    ActionChains(driver)\
                        .scroll_to_element(iframe)\
                        .perform()
                    next_btn = driver.find_element(By.XPATH, '//*[@id="contentleft"]/div/div[16]') # click next button
                    next_btn.click()
            except:
                with open('textfile.txt', 'a') as f:
                    f.write("failed on page " + str(i-1) + '\n')
                    f.close
            
            #Need better way to deal with infinite scrolling this take too long when large
            while True:
                time.sleep(1)
                # scroll one screen height each time
                driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
                i += 1
                time.sleep(scroll_pause_time)
                # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
                scroll_height = driver.execute_script("return document.body.scrollHeight;")  
                # Break the loop when the height we need to scroll to is larger than the total scroll height
                #if (screen_height) * i > scroll_height:
                    #break 
                if(i > j/2):
                    break
            
            #No next butten must click 2-10
            time.sleep(5) 
            #next buttun need scroll
            #try:
                #next_btn = driver.find_element(By.XPATH, '/html/body/div[5]/div[5]/section[2]/div[2]/div[1]/div/div[4]/ul/li[2]/a') # click next button
                #next_btn.click()
           # except:
                #with open('textfile.txt', 'a') as f:
                    #f.write("failed on page " + str(i-1) + '\n')
                   # f.close
                # miss list
        #parse each url

        # saved as text file for missed option
        # np . save text
        
        for url in urllist:
            time.sleep(1)
            yield scrapy.Request(url, callback=self.parse_article)
            
            
 
    # pass on the links to open and process actual news articles
    def parse_article(self, response):

        capitem = ScraperItem()
        headline = response.xpath('//*[@id="wrap"]/div[4]/div[2]/div/h1//text()').get()
        #///html/body/div[1]/div[4]/div[2]/div/h1
       
        #need try and except and failed conditions
        date = response.xpath('//*[@id="wrap"]/div[4]/div[2]/div/div[2]/span//text()').get()
        #//html/body/div[1]/div[4]/div[2]/div/div[3]/span
        #/html/body/div[2]/div[4]/div[2]/div/div[2]/span
        # Convert to datetime object
        if date:
            date_object = datetime.strptime(date, "%B %d, %Y")

        # Format to month/day/year format
            formatted_date = date_object.strftime("%m/%d/%Y")
        else:
            formatted_date = None
        #i=1
        article = []
        #article = response.xpath('//*[@id="sno-story-body-content"]/p[1]//text()').extract()
        i=1
        while True:
            paragraph = response.xpath(f'//*[@id="sno-story-body-content"]/p[{i}]//text()').getall()
            paragraphstring = ''.join(paragraph)
            if not paragraph:
                break
            article.append(paragraphstring)
            i+=1
        
        #///html/body/div[1]/div[4]/div[2]/div/div[5]/div/p
        
        #check = response.xpath('/html/body/div[6]/div[7]/section[2]/article/div[4]/div[1]/div/div[4]/div[1]/div/div//div[3]/p['+str(i)+']/text()')
        
        #while len(check) >0:
            #article.append(response.xpath('/html/body/div[6]/div[7]/section[2]/article/div[4]/div[1]/div/div[4]/div[1]/div/div/div[3]/p['+str(i)+']//text()').get())
            #i+=1
            #check = response.xpath('/html/body/div[6]/div[7]/section[2]/article/div[4]/div[1]/div/div[4]/div[1]/div/div/div[3]/p['+str(i)+']//text()')
        
       # if  (not article) or (headline == '') or (date == None):
         #   with open('textfile.txt', 'a') as f:
          #          f.write("Miss at " + response.url + ", " + str(article) + ", " + headline + ", " + date)
           #         f.close

        if  (not article) or (headline == None) or (formatted_date == None):
            with open('textfile.txt', 'a') as f:
                if not article:
                    f.write("Miss article " + response.url + '\n')
                if headline == None:
                    f.write("Miss headline " + response.url + '\n')
                if date == None:
                    f.write("Miss date " + response.url + '\n')
                f.close
        
        publisher = 'battalion'
        neg = 0
        neu = 0
        pos = 0
        compound = 0
        sentiment = 0
        subjectivity = 0
        
       # weblist = str(response).split()
       # web = weblist[1]
       # web = web.replace('>', '')

        capitem['headline'] = headline
        capitem['date'] = formatted_date
        capitem['article'] = article
        capitem['publisher'] = publisher
        capitem['website'] = response.url
        
        time.sleep(1)
        yield capitem

        '''yield {
            "headline": headline,
            "article": article, 
            "date": date,
            "publisher" : publisher,
            "sentiment" : sentiment,
            "subjectivity" : subjectivity
            
        }'''