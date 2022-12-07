from .lacoste import LacosteSpider


class LacosteFrSpider(LacosteSpider):
    name = 'lacoste_it'
    allowed_domains = ['www.lacoste.com']
    BASE_URL = "https://www.lacoste.com"
    product_detail_api = 'https://www.lacoste.com/on/demandware.store/Sites-IT-Site/it/Product-PartialsData'
