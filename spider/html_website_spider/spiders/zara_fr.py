import scrapy
from .zara import ZaraSpider


class ZaraFrSpider(ZaraSpider):
    name = 'zara_fr'

    base_url = 'https://www.zara.com/fr/fr'

    def start_requests(self):
        url = "https://www.zara.com/fr/"
        yield scrapy.Request(url, callback=self.parse_category_list)
