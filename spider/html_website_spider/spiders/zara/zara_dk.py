import scrapy
from .zara import ZaraSpider


class ZaraDkSpider(ZaraSpider):
    name = 'zara_dk'

    base_url = 'https://www.zara.com/dk/dk/'

    def start_requests(self):
        url = "https://www.zara.com/dk/"
        yield scrapy.Request(url, callback=self.parse_category_list)
