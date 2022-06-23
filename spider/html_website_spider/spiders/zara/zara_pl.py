import scrapy
from .zara import ZaraSpider


class ZaraPlSpider(ZaraSpider):
    name = 'zara_pl'

    base_url = 'https://www.zara.com/pl/pl'

    def start_requests(self):
        url = "https://www.zara.com/pl/"
        yield scrapy.Request(url, callback=self.parse_category_list)
