from .oysho import OyshoSpider


class OyshoEsSpider(OyshoSpider):
    name = 'oysho_es'

    category_url = 'https://www.oysho.com/itxrest/3/catalog/store/64009600/60361120/category/{}/product?languageId=-5&appId=1&showProducts=false'
    product_detail_url = "https://www.oysho.com/itxrest/2/catalog/store/64009600/60361120/category/0/product/{}/detail?languageId=-5&appId=1"
