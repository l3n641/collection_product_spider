from .oysho import OyshoSpider


class OyshoPtSpider(OyshoSpider):
    name = 'oysho_pt'

    category_url = 'https://www.oysho.com/itxrest/3/catalog/store/64009610/60361120/category/{}/product?languageId=-6&appId=1&showProducts=false'
    product_detail_url = "https://www.oysho.com/itxrest/2/catalog/store/64009610/60361120/category/0/product/{}/detail?languageId=-6&appId=1"
