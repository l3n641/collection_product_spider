import scrapy
from .zara import ZaraSpider


class ZaraFrPtSpider(ZaraSpider):
    name = 'zara_pt'

    base_url = 'https://www.zara.com/pt/pt'

    def start_requests(self):
        url = "https://www.zara.com/pt/"
        yield scrapy.Request(url, callback=self.parse_category_list)
