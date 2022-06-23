import scrapy
from .zara import ZaraSpider


class ZaraDeSpider(ZaraSpider):
    name = 'zara_de'

    base_url = 'https://www.zara.com/de/de/'

    def start_requests(self):
        url = "https://www.zara.com/de/"
        yield scrapy.Request(url, callback=self.parse_category_list)
