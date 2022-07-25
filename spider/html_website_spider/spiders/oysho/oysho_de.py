from .oysho import OyshoSpider


class OyshoDeSpider(OyshoSpider):
    name = 'oysho_de'

    category_url = 'https://www.oysho.com/itxrest/3/catalog/store/64009604/60361126/category/{}/product?languageId=-3&appId=1&showProducts=false'
    product_detail_url = "https://www.oysho.com/itxrest/2/catalog/store/64009604/60361126/category/0/product/{}/detail?languageId=-3&appId=1"
