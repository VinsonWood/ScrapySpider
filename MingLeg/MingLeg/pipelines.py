# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy import Request
import logging

class MinglegPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for url in item['urlList']:
            yield Request(url, meta={'item': item, 'index': item['urlList'].index(url)})

    def item_completed(self, results, item, info):
        image_paths = [x['paths'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem('Image Downloaded Failed')
        else:
            logging.info(image_paths)
        return item

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']  # 通过上面的meta传递过来item
        index = request.meta['index']  # 通过上面的index传递过来列表中当前下载图片的下标
        file_name = '/mingLegImages'+'/' + item['title'] + '/' + item['title'] + str(index) + '.jpg'
        return file_name
