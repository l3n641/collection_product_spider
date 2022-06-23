import scrapy
from .zara import ZaraSpider


class ZaraNlSpider(ZaraSpider):
    name = 'zara_nl'

    base_url = 'https://www.zara.com/nl/nl/'

    def start_requests(self):
        url = "https://www.zara.com/nl/"
        yield scrapy.Request(url, callback=self.parse_category_list)
