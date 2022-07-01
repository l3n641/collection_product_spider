import scrapy
from .zara import ZaraSpider


class ZaraSeSpider(ZaraSpider):
    name = 'zara_se'

    base_url = 'https://www.zara.com/se/sv/'
    category_url = 'https://www.zara.com/se/sv/categories?ajax=true'
