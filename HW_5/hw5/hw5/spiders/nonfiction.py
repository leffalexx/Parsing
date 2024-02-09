import scrapy


class NonfictionSpider(scrapy.Spider):
    name = "nonfiction"
    allowed_domains = ["listmuse.com"]
    start_urls = ["https://listmuse.com/best-books-top-100-nonfiction.php"]

    def parse(self, response):
        books = response.xpath("//div[@class='col-md-9']/div[@class='container']/div[@class='row']")
        for book in books:
            yield {
                'rank': int(book.xpath(".//div[@class='col-md-9 col-xs-7 ']/h2/text()").get().strip('. ')),
                'author': book.xpath(".//div[@class='col-md-9 col-xs-7 ']/p/a/text()").get(),
                'title': book.xpath(".//div[@class='col-md-9 col-xs-7 ']/h2/a/text()").get()
            }
