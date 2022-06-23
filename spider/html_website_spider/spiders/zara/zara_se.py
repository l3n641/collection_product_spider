import scrapy
from .zara import ZaraSpider


class ZaraSeSpider(ZaraSpider):
    name = 'zara_se'

    base_url = 'https://www.zara.com/se/se/'

    def start_requests(self):
        url = "https://www.zara.com/se/"
        yield scrapy.Request(url, callback=self.parse_category_list)
