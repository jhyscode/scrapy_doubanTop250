import re
import scrapy #导入scrapy包
from bs4 import BeautifulSoup
from scrapy import Request
from douban.items import DoubanItem ##自定义的字段，导入douban项目中，items文件中的DoubanItem类
class DoubanMivieTop250(scrapy.Spider):
    name = 'douban_top250'
    #start_urls = ['https://movie.douban.com/top250']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }
    def start_requests(self):
        url = 'https://movie.douban.com/top250'
        yield Request(url, headers=self.headers)
    def parse(self, response):
        item = DoubanItem()  #字典形式存储数据
        movies = response.xpath('//ol[@class="grid_view"]/li')
        print(movies)
        for movie in movies:
            item["ranking"] = movie.xpath(
                './/div[@class="pic"]/em/text()').extract()[0]
            print(item["ranking"])
            item["movie_name"] = movie.xpath(
                './/div[@class="hd"]/a/span[1]/text()').extract()[0]
            print(item["movie_name"])
            item['score'] = movie.xpath(
                './/div[@class="star"]/span[@class="rating_num"]/text()').extract()[0]
            item['score_num'] = movie.xpath(
                './/div[@class="star"]/span/text()').re(r'(\d+)人评价')[0]
            try:
                item['quote'] = movie.xpath('.//p[@class="quote"]/span/text()').extract()
            except:
                item['quote'] = ""
            yield item

        next_page_url = response.xpath('//span[@class="next"]/a/@href').extract()
        if next_page_url:
            next_page_url = "https://movie.douban.com/top250" + next_page_url[0]
            yield Request(next_page_url,headers=self.headers)
