from .lacoste import LacosteSpider


class LacosteEsSpider(LacosteSpider):
    name = 'lacoste_es'
    allowed_domains = ['www.lacoste.com']
    BASE_URL = "https://www.lacoste.com"
    product_detail_api = 'https://www.lacoste.com/on/demandware.store/Sites-ES-Site/es/Product-PartialsData'
