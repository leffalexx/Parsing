# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class UnsplashItem(scrapy.Item):
    author = scrapy.Field()
    category = scrapy.Field()
    img_urls = scrapy.Field()
    images = scrapy.Field()