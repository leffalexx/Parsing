import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from ..items import UnsplashItem
from itemloaders.processors import MapCompose



class UnsplashImgSpider(CrawlSpider):
    name = "unsplash_img"
    allowed_domains = ["www.unsplash.com"]
    start_urls = ["https://unsplash.com/"]

    rules = (Rule(LinkExtractor(
        restrict_xpaths="//div[@class='MorZF']"), callback="parse_item", follow=True),)

    def parse_item(self, response):
        loader = ItemLoader(item=UnsplashItem(), response=response)
        loader.default_input_processor = MapCompose(str.strip)

        loader.add_xpath('author', '//div[@class="TO_TN"]/a/text()')
        loader.add_xpath('category', '//div[@class="_NeDM"]/span/a/text()')
        urls = response.xpath('//div[@class="MorZF"]').getall()
        loader.add_value('img_urls', urls)

        yield loader.load_item()
