# -*- coding: utf-8 -*-
import scrapy
from MingLeg.items import MinglegItem
import logging


class MinglegSpider(scrapy.Spider):
    name = 'mingleg'
    allowed_domains = ['https://www.mingleg.com']
    # start_urls = ['https://www.mingleg.com/page/' + str(x) for x in range(1, 1063, 1)]
    start_urls = ['https://www.mingleg.com/']
    cookies = {
        'wordpress_sec_20cfa294bb93a749d1b63f30c2e794b9': 'varshonwood%7C1536362156%7Cj94PSkVsVDhCIPCwUd2VJG2u1YQ0QdDPwn0qTf89ciN%7C7c84743f6cff38a80a206f7452705aae658aa96faafe01f41c886279f32b4899',
        'swpm_session': 'f12c5ca08c94a133c9c2ed4f403e0482', 'swpm_in_use': 'swpm_in_use',
        'Hm_lvt_c7b9263bd8f9b5b87b3e0e88548b3bea': '1534006826,1535026151,1535026811,1535106977',
        'wordpress_test_cookie': 'WP+Cookie+check',
        'simple_wp_membership_sec_20cfa294bb93a749d1b63f30c2e794b9': 'varshonwood%7C1536362156%7Cfb7951e3fede5438782b00f616804cf5',
        'wordpress_logged_in_20cfa294bb93a749d1b63f30c2e794b9': 'varshonwood%7C1536362156%7Cj94PSkVsVDhCIPCwUd2VJG2u1YQ0QdDPwn0qTf89ciN%7C844def3a4daa678ec604f69f7523b0e1e809e17c2d8a66c23050662746229b03',
        'Hm_lpvt_c7b9263bd8f9b5b87b3e0e88548b3bea': '1535152559'}

    def parse(self, response):
        for detail_url in response.xpath('//article/header/h1/a/@href').extract():
            if detail_url is not None:
                detail_url = response.urljoin(detail_url)
                yield scrapy.Request(detail_url, callback=self.page_detail, dont_filter=True, cookies=self.cookies)

        # 获取下一页链接
        next_page = response.xpath('//span[@class="current"]/following-sibling::a[1]/@href').extract_first()
        if next_page is not None:
            logging.info('获取下一页成功' + next_page)
            yield scrapy.Request(next_page, callback=self.parse, dont_filter=True, cookies=self.cookies)

    def page_detail(self, response):
        item = MinglegItem()
        item['title'] = response.xpath('//article/header/h1/text()').extract_first()
        item['urlList'] = []
        list = response.xpath('//article/div/descendant::p/a/@href').extract()
        for img_detail in list:
            if img_detail is not None:
                logging.info(item['title'] + '获取图片详情成功')
                img_detail_after = response.urljoin(img_detail)
                yield scrapy.Request(img_detail_after, callback=self.img_detail, dont_filter=True,
                                     meta={'item': item, 'max_index': len(list)}, cookies=self.cookies)

    def img_detail(self, response):
        item = response.meta['item']
        item['urlList'].append(response.urljoin(response.xpath('//header/footer/a[1]/@href').extract_first()))
        max_index = response.meta['max_index']
        if len(item['urlList']) == max_index:
            logging.info(item['title'] + '获取图片大图完毕')
            yield item
