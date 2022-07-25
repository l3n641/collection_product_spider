from .oysho import OyshoSpider


class OyshoSeSpider(OyshoSpider):
    name = 'oysho_se'

    category_url = 'https://www.oysho.com/itxrest/3/catalog/store/64009612/60361126/category/{}/product?languageId=-25&appId=1&showProducts=false'
    product_detail_url = "https://www.oysho.com/itxrest/2/catalog/store/64009612/60361126/category/0/product/{}/detail?languageId=-25&appId=1"
