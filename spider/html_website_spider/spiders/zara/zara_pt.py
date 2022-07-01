import scrapy
from .zara import ZaraSpider


class ZaraPtSpider(ZaraSpider):
    name = 'zara_pt'

    base_url = 'https://www.zara.com/pt/pt'
    category_url = 'https://www.zara.com/pt/pt/categories?ajax=true'


