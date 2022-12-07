from .lacoste import LacosteSpider


class LacosteDeSpider(LacosteSpider):
    name = 'lacoste_de'
    allowed_domains = ['www.lacoste.com']
    BASE_URL = "https://www.lacoste.com"
    product_detail_api = 'https://www.lacoste.com/on/demandware.store/Sites-DE-Site/de/Product-PartialsData'
