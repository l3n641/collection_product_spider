import scrapy
from .zara import ZaraSpider


class ZaraFrSpider(ZaraSpider):
    name = 'zara_fr'

    base_url = 'https://www.zara.com/fr/fr'
    category_url = 'https://www.zara.com/fr/fr/categories?ajax=true'
