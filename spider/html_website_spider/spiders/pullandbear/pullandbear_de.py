from .pullandbear import PullandbearSpider


class PullandbearDeSpider(PullandbearSpider):
    name = 'pullandbear_de'

    category_url = 'https://www.pullandbear.com/itxrest/3/catalog/store/24009404/20309424/category/{}/product?languageId=-3&showProducts=false&appId=1'
    product_detail_url = "https://www.pullandbear.com/itxrest/2/catalog/store/24009404/20309424/category/0/product/{}/detail?languageId=-3&appId=1"
