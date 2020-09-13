
import time,datetime
import re
import scrapy
from bs4 import BeautifulSoup

from ..items import Test1Item


class BaiduSpider(scrapy.Spider):
    name = 'baidu'
    allowed_domains = ['www.chinanews.com']
    start_urls = ['http://www.chinanews.com/']
    models_url = []

    def parse(self, response):

        alist=[1,2,3,4,5]
        li_list = response.xpath('//*[@id="nav"]/ul/li')

        for i in alist:
            url = 'http:'+li_list[i].xpath('./a/@href').extract_first()
            self.models_url.append(url)
            title=li_list[i].xpath('./a/text()').extract_first()

        for url in self.models_url:
            yield scrapy.Request(url, callback=self.parse_model)


    def parse_model(self, response):
        li_list=response.xpath('//*[@id="ent0"]/li/div/div')
        for i in li_list:
            title = i.xpath('./div[1]/em/a/text()').extract_first()
            img_url=i.xpath('./div[2]/div/a/img/@src').extract_first()
            detail_url='http:'+i.xpath('./div[1]/em/a/@href').extract_first()
            if not img_url:
                img_url='https://ss1.bdstatic.com/70cFvXSh_Q1YnxGkpoWK1HF6hhy/it/u=3055188832,107402217&fm=26&gp=0.jpg'
            item = Test1Item()
            item['title'] = title
            item['img_url'] = img_url
            # 对新闻详情页的url发起请求
            yield scrapy.Request(url=detail_url, callback=self.parse_detail, meta={'item': item})

    def parse_detail(self, response):

        soup = BeautifulSoup(response.body,'html.parser',from_encoding='utf-8')
        content = soup.find('div', {'class': 'left_zw'})

        text=soup.find('div', {'class': 'left-time'}).get_text().replace('参与互动','').split('来源：')
        create_time=text[0]
        time = re.sub('\s', '', create_time)
        create_time = datetime.datetime.strptime(time, '%Y年%m月%d日%H:%M')
        source=text[1]
        digest=soup.h1.get_text()
        item = response.meta['item']
        item['content'] = content
        item['create_time'] = create_time
        item['source'] = source
        item['digest'] = digest
        yield item



