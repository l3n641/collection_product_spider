import scrapy
from .zara import ZaraSpider


class ZaraItSpider(ZaraSpider):
    name = 'zara_it'

    base_url = 'https://www.zara.com/it/it/'

    def start_requests(self):
        url = "https://www.zara.com/it/"
        yield scrapy.Request(url, callback=self.parse_category_list)
