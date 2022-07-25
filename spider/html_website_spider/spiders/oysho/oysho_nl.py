from .oysho import OyshoSpider


class OyshoNlSpider(OyshoSpider):
    name = 'oysho_nl'

    category_url = 'https://www.oysho.com/itxrest/3/catalog/store/65009603/60361126/category/{}/product?languageId=100&appId=1&showProducts=false'
    product_detail_url = "https://www.oysho.com/itxrest/2/catalog/store/65009603/60361126/category/0/product/{}/detail?languageId=100&appId=1"
