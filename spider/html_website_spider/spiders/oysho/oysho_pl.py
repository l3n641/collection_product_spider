from .oysho import OyshoSpider


class OyshoPlSpider(OyshoSpider):
    name = 'oysho_pl'

    category_url = 'https://www.oysho.com/itxrest/3/catalog/store/65009624/60361116/category/{}/product?languageId=-22&appId=1&showProducts=false'
    product_detail_url = "https://www.oysho.com/itxrest/2/catalog/store/65009624/60361116/category/0/product/{}/detail?languageId=-22&appId=1"
