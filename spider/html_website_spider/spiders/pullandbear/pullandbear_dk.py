from .pullandbear import PullandbearSpider


class PullandbearDkSpider(PullandbearSpider):
    name = 'pullandbear_dk'

    category_url = 'https://www.pullandbear.com/itxrest/3/catalog/store/24009408/20309424/category/{}/product?languageId=-39&showProducts=false&appId=1'
    product_detail_url = "https://www.pullandbear.com/itxrest/2/catalog/store/24009408/20309424/category/0/product/{}/detail?languageId=-39&appId=1"
