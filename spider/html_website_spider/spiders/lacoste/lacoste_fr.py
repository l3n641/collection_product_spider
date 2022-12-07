from .lacoste import LacosteSpider


class LacosteFrSpider(LacosteSpider):
    name = 'lacoste_fr'
    allowed_domains = ['www.lacoste.com']
    BASE_URL = "https://www.lacoste.com"
    product_detail_api = 'https://www.lacoste.com/on/demandware.store/Sites-FR-Site/fr/Product-PartialsData'
