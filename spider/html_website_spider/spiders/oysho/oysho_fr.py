from .oysho import OyshoSpider


class OyshoFrSpider(OyshoSpider):
    name = 'oysho_fr'

    category_url = 'https://www.oysho.com/itxrest/3/catalog/store/64009601/60361120/category/{}/product?languageId=-2&appId=1&showProducts=false'
    product_detail_url = "https://www.oysho.com/itxrest/2/catalog/store/64009601/60361120/category/0/product/{}/detail?languageId=-2&appId=1"
