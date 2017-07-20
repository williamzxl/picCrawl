# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from Crawlmzitu.settings import IMAGES_STORE
import os
import requests

class CrawlmzituPipeline(object):
    def process_item(self, item, spider):
        fold_name = "".join(item['title'])
        header = {
            'USER-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            # 'Cookie': '',
            #需要查看图片的cookie信息，否则下载的图片无法查看
        }
        images = []
        all_urls = []
        dir_path = '{}'.format(IMAGES_STORE)
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)

        for jpg_url, num in zip(item['jpg_url'],range(0,100)):
            file_name = fold_name + str(num)
            file_path = '{}//{}'.format(dir_path,file_name)
            images.append(file_path)
            if os.path.exists(file_path) or os.path.exists(file_name):
                continue

            with open('{}//{}.jpg'.format(dir_path, file_name), 'wb') as f:
                req = requests.get(jpg_url, headers=header)
                f.write(req.content)

        return item

