from .lacoste import LacosteSpider


class LacostePtSpider(LacosteSpider):
    name = 'lacoste_pt'
    allowed_domains = ['www.lacoste.com']
    BASE_URL = "https://www.lacoste.com"
    product_detail_api = 'https://www.lacoste.com/on/demandware.store/Sites-PT-Site/pt_PT/Product-PartialsData'
