from .oysho import OyshoSpider


class OyshoItSpider(OyshoSpider):
    name = 'oysho_it'

    category_url = 'https://www.oysho.com/itxrest/3/catalog/store/64009605/60361120/category/{}/product?languageId=-4&appId=1&showProducts=false'
    product_detail_url = "https://www.oysho.com/itxrest/2/catalog/store/64009605/60361120/category/0/product/{}/detail?languageId=-4&appId=1"
