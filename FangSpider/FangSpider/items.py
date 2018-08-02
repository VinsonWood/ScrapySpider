# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FangspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 楼盘名
    title = scrapy.Field()
    # 楼盘价格
    price = scrapy.Field()
    # 楼盘备注
    comment = scrapy.Field()
    # 楼盘地址
    address = scrapy.Field()
    # 楼盘标签
    tag = scrapy.Field()
