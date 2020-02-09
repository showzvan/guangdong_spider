# -*- coding: utf-8 -*-
import scrapy
import time
import json
from guangdong.items import GuangdongItem
"""
1. 先获取当前页面的所有的商品 url
2. 逐条访问获取到的url
3. 解析数据 写入数据库
"""

class ZhengfuSpider(scrapy.Spider):
    name = 'zhengfu'
    allowed_domains = ['http://210.76.73.186/channel/161.html/']
    start_urls = ['http://210.76.73.186/channel/161.html/']

    def parse(self, response):
        gp_lists = response.css('.gp-list-view ul li')
        for i in gp_lists:
            u = i.xpath('div[@class="info"]/div[@class="img"]/a/@href').extract_first()
            detail = response.urljoin(u)
            yield scrapy.Request(url=detail, callback=self.get_info, dont_filter=True)
        # 下一页
        next_page = response.css('.next').xpath('a/@href').extract_first()
        if next_page is not None:
            next_url = response.urljoin(next_page)
            yield scrapy.Request(url=next_url, callback=self.parse, dont_filter=True)

    def get_info(self, response):
        items = GuangdongItem()
        goods = response.css('.goods_particulars')
        details = response.css('.goods_details')
        # 标题
        items["title"] = goods.xpath('form/div[@class="goods_main"]/h1[@class="goods_name"]/text()').extract_first().strip()
        # 型号
        items["model"] = goods.xpath('form/div[@class="goods_main"]/div[2]/div/div[4]/div[2]/i/@title')\
            .extract_first().strip()
        # 本网价格 备注：采集历史价格上的最新价格作为本网价格
        # local_price = goods.xpath('form/div[@class="goods_main"]/div[2]/div/div[1]/div[2]') \
        #     .extract_first()
        items["local_price"] = details.xpath('div[1]/div/div/div[7]/div/table//tr[1]/td[@class="tr"]/text()').extract_first()
        # 图片
        items["img_url"] = json.dumps(goods.xpath('form/div[@class="goods_main"]/div[1]/div[1]/div[@class="spec-scroll"]'
                             '/div[1]/ul/li/img/@bimg').extract())
        # 时间
        items["time"] = time.time()
        # 供应商名称
        items["name"] = json.dumps(goods.xpath('form/div[@class="goods_main"]/div[3]/div[2]/div[1]/table//tr//font[@class="textm"]/text()') \
            .extract(), ensure_ascii=False)
        # 供应商价格
        items["price"] = json.dumps(goods.xpath('form/div[@class="goods_main"]/div[3]/div[2]/div[1]/table//tr//td[@class="tc"][1]/a/text()') \
            .extract())
        # 排名
        items["ranking"] = ""
        yield items


