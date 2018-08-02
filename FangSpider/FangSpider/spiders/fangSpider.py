import scrapy
from FangSpider.items import FangspiderItem


class mingyan(scrapy.Spider):  # 需要继承scrapy.Spider类

    name = "fang"  # 蜘蛛名

    start_urls = [
        "http://newhouse.cq.fang.com/house/web/newhouse_sumall.php?page=1&pricesort=2"
    ]

    def parse(self, response):
        for div in response.xpath('/html/body/div[3]/div[6]/div[1]/div[2]/ul/li'):
            item = FangspiderItem()
            item["title"] = div.xpath('./div[1]/div/p/a/text()').extract_first()
            detail = div.xpath('./div[1]/a/@href').extract_first()
            price = div.xpath('./div[2]/div[1]')
            pricetemp = ''.join(div.xpath('./div[2]/div[1]/text()').extract())
            for p in price:
                if pricetemp.find('万元') > 0:
                    pricetemp = pricetemp.replace('万元', div.xpath(
                        './div[2]/div[1]/span/text()').extract_first() + '万元').replace('\t', '') \
                        .replace('\n', '').replace('-', '').replace(' ', '')
                elif pricetemp.find('元') > 0:
                    pricetemp = pricetemp.replace('元', div.xpath(
                        './div[2]/div[1]/span/text()').extract_first() + '元').replace('\t', '') \
                        .replace('\n', '').replace('-', '').replace(' ', '')
                else:
                    pricetemp = '价格待定'
            item["price"] = pricetemp
            item["comment"] = ','.join(div.xpath('./div[2]/p[1]/a/text()').extract())
            item["comment"] += div.xpath('./div[2]/p[1]/text()').extract()[-1].replace('\t', '').replace('\n', '') \
                .replace('-', '')
            item["address"] = div.xpath('./div[2]/p[2]/a/text()').extract_first()
            item["tag"] = ','.join(div.xpath('./div[2]/div[3]/span/text()').extract())
            # 获取下一页链接
            next_page = response.xpath('//a[@class="active"]/following-sibling::a[1]/@href').extract_first()
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)
            yield item
