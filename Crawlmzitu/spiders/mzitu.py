# -*- coding: utf-8 -*-
import scrapy
import time, re
from Crawlmzitu.items import CrawlmzituItem

class MzituSpider(scrapy.Spider):
    name = 'mzitu'
    #allowed_domains = ['http://www.mzitu.com/page/1/']
    #start_urls = ['http://www.mzitu.com/page/1/']
    last_url = []
    with open(r'..\\urls.txt', 'r') as fp:
        crawl_urls = fp.readlines()
        for start_url in crawl_urls:
            last_url.append(start_url.strip('\n'))
    start_urls = []
    start_urls.append("".join(last_url[-1]))

    def parse(self, response):
        selector = scrapy.Selector(response)
        next_page = selector.xpath('//div/a[@class="next page-numbers"]/@href').extract()
        next_text = selector.xpath('//div[@class="nav-links"]/a/text()').extract()

        if '下一页»' in next_text:
            with open('..//urls.txt', 'a+') as fp:
                fp.write('\n')
                fp.write("".join(next_page))
                fp.write("\n")
            request = scrapy.http.Request("".join(next_page), callback=self.parse)
            time.sleep(0.5)
            yield request

        all_info = selector.xpath('//*[@id="pins"]/li')
        for info in all_info:
            links = info.xpath('//*[@id="pins"]/li/a/@href').extract()
        for link in links:
            print("link:",link)
            request = scrapy.http.Request(link,callback=self.parse_item)
            time.sleep(1)
            yield request


    # def parse_next_jpg(self,response):
    #
    #     selector = scrapy.Selector(response)
    #     next_jpg_text = selector.xpath('//div[@class="pagenavi"]/a/span/text()').extract()
    #     next_jpg = selector.xpath('//div[@class="pagenavi"]/a/@href').extract()
    #     #//div[@class="pagenavi"]/a/@href
    #     print("next_jpg_text:",next_jpg_text)
    #     print("william")
    #     print("next_jpg,",next_jpg)
    #     if '下一页»' in next_jpg_text:
    #         next_jpg_page = next_jpg[-1]
    #         print("next_jpg_page",next_jpg_page)
    #         request = scrapy.http.Request(next_jpg_page, callback=self.parse_item)
    #         yield request

    def parse_item(self, response):

        item = CrawlmzituItem()
        selector = scrapy.Selector(response)
        next_jpg_text = selector.xpath('//div[@class="pagenavi"]/a/span/text()').extract()
        next_jpg = selector.xpath('//div[@class="pagenavi"]/a/@href').extract()
        #//div[@class="pagenavi"]/a/@href
        print("next_jpg_text:",next_jpg_text)
        print("william")
        print("next_jpg,",next_jpg)
        image_new_srcs = []
        image_src = selector.xpath('//div[@class="main-image"]//img/@src').extract()
        print("image_src:",image_src)

        if '下一页»' in next_jpg_text:
            page_nums = int(next_jpg_text[-2])
            print("page_nums:",page_nums)
        image_new_src = "".join(image_src)
        pattern = re.compile('http://i.meizitu.net/(\w+)/(\w+)/(\w+)(\d){2}.jpg')
        result = re.match(pattern, image_new_src)
        ma = result.groups()
        print(ma)
        print(result.groups(-1))
        for i in range(int(result.groups()[-1]), page_nums + 1):
            if i < 10:
                src_link = 'http://i.meizitu.net/{}/{}/{}0{}.jpg'.format(ma[0], ma[1], ma[2], i)
                image_new_srcs.append(src_link)
            elif i > 9:
                src_link = 'http://i.meizitu.net/{}/{}/{}{}.jpg'.format(ma[0], ma[1], ma[2], i)
                image_new_srcs.append(src_link)
            else:
                print("Check src")
        print(image_new_src)

        image_title = selector.xpath('//div[@class="main-image"]//img/@alt').extract()


        item['title'] = image_title
        item['jpg_url'] = image_new_srcs

        yield item

