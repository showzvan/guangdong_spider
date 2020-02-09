# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GuangdongItem(scrapy.Item):
    table = "goods_info"
    table2 = "supplier"
    title = scrapy.Field()
    model = scrapy.Field()
    local_price = scrapy.Field()
    img_url = scrapy.Field()
    time = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    ranking = scrapy.Field()
