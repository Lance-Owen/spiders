import scrapy
from scrapy import Selector


class HangzhouSpider(scrapy.Spider):
    name = "hangzhou"
    allowed_domains = ["ggzy.hzctc.hangzhou.gov.cn"]
    start_urls = ["http://ggzy.hzctc.hangzhou.gov.cn/"]

    def parse(self, response):
        sel = Selector(response)
        sel.xpath( )
        sel
        pass

