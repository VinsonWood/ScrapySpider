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
        'swpm_session': 'a0729f55f646f2ee1bf85f628c2e4549',
        'Hm_lvt_c7b9263bd8f9b5b87b3e0e88548b3bea': '1537708130,1537749333,1537749536,1537750646',
        'swpm_in_use': 'swpm_in_use',
        'simple_wp_membership_sec_20cfa294bb93a749d1b63f30c2e794b9': 'varshonwood%7C1538960567%7C4509ef06f8902c924ca464e8491c7638',
        'wordpress_logged_in_20cfa294bb93a749d1b63f30c2e794b9': 'varshonwood%7C1538960567%7Ci03brlZaNCZUO3U2U2RE9JBW3cXmHZtuPSgVpKjzeL8%7C2064a19080d8cc18152dfd8e3e76ed2605dcae5b91409255b63dd982396c0c97',
        'Hm_lpvt_c7b9263bd8f9b5b87b3e0e88548b3bea': '1537751095'}

    def parse(self, response):
        for detail_url in response.xpath('//article/header/h1/a/@href').extract():
            if detail_url is not None:
                detail_url = response.urljoin(detail_url)
                yield scrapy.Request(detail_url, callback=self.page_detail, dont_filter=True, cookies=self.cookies)

        # 获取下一页链接
        next_page = response.xpath('//span[@class="current"]/following-sibling::a[1]/@href').extract_first()
        if next_page is not None:
            logging.info('获取下一页成功' + next_page)
            if next_page == 'https://www.mingleg.com/page/404':
                next_page = 'https://www.mingleg.com/page/405'
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
