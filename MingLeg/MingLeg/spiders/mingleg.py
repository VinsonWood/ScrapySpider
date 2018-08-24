# -*- coding: utf-8 -*-
import scrapy
from MingLeg.items import MinglegItem
import logging


class MinglegSpider(scrapy.Spider):
    name = 'mingleg'
    allowed_domains = ['https://www.mingleg.com']
    # start_urls = ['https://www.mingleg.com/page/' + str(x) for x in range(1, 1063, 1)]
    start_urls = ['https://www.mingleg.com/']

    def parse(self, response):
        for detail_url in response.xpath('//article/header/h1/a/@href').extract():
            if detail_url is not None:
                detail_url = response.urljoin(detail_url)
                yield scrapy.Request(detail_url, callback=self.page_detail, dont_filter=True)

        # 获取下一页链接
        next_page = response.xpath('//span[@class="current"]/following-sibling::a[1]/@href').extract_first()
        if next_page is not None:
            logging.info('获取下一页成功')
            yield scrapy.Request(next_page, callback=self.parse, dont_filter=True)

    def page_detail(self, response):
        item = MinglegItem()
        item['title'] = response.xpath('//article/header/h1/text()').extract_first()
        item['urlList'] = []
        list = response.xpath('//article/div/descendant::p/a/@href').extract()
        for img_detail in list:
            if img_detail is not None:
                logging.info('获取图片详情成功')
                img_detail_after = response.urljoin(img_detail)
                yield scrapy.Request(img_detail_after, callback=self.img_detail, dont_filter=True,
                                     meta={'item': item, 'max_index': len(list)})

    def img_detail(self, response):
        item = response.meta['item']
        item['urlList'].append(response.urljoin(response.xpath('//header/footer/a[1]/@href').extract_first()))
        max_index = response.meta['max_index']
        if len(item['urlList']) == max_index:
            logging.info('获取图片大图成功')
            yield item
