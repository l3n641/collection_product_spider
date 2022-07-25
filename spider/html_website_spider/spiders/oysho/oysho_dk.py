from .oysho import OyshoSpider


class OyshoDkSpider(OyshoSpider):
    name = 'oysho_dk'

    category_url = 'https://www.oysho.com/itxrest/3/catalog/store/64009608/60361126/category/{}/product?languageId=-39&appId=1&showProducts=false'
    product_detail_url = "https://www.oysho.com/itxrest/2/catalog/store/64009608/60361126/category/0/product/{}/detail?languageId=-39&appId=1"
