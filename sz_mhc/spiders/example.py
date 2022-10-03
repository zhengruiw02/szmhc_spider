import scrapy


class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = ['wjw.sz.gov.cn']
    start_urls = ['http://wjw.sz.gov.cn/']

    def parse(self, response):
        pass
