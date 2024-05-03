import scrapy

class TribuneSpider(scrapy.Spider):
    name = 'testarticle'
    #allowed_domains = ['www.texastribune.org']
    start_urls = ['https://www.texastribune.org/2020/12/16/texas-am-chegg-cheating/']

    #testing 
    def parse(self, response):
        tags = response.xpath('/html/body/main/article/div[2]/div/p[@class=t-copy.t-links-underlined.t-align-left]')
        print(tags)
        article = []
        for tag in tags:
            print(tag)
            text = " ".join(tag.xpath('.//text()').get())
            print(text)
            article.append(text)

        articles=[]
        i=1
        
        check = response.xpath('/html/body/main/article/div[2]/div/p['+str(i)+']//text()')
        while len(check) >0:
            articles.append(response.xpath('/html/body/main/article/div[2]/div/p['+str(i)+']//text()').get())
            i+=1
            check = response.xpath('/html/body/main/article/div[2]/div/p['+str(i)+']//text()')

        yield{
            "article" : article,
            "tags" : tags,
            "articles" : articles
        }