import scrapy
from .zara import ZaraSpider


class ZaraEsSpider(ZaraSpider):
    name = 'zara_es'

    base_url = 'https://www.zara.com/es/es/'

    def start_requests(self):
        url = "https://www.zara.com/es/"
        yield scrapy.Request(url, callback=self.parse_category_list)
