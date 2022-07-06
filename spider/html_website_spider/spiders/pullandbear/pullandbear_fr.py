from .pullandbear import PullandbearSpider


class PullandbearFrSpider(PullandbearSpider):
    name = 'pullandbear_fr'

    category_url = 'https://www.pullandbear.com/itxrest/3/catalog/store/24009401/20309425/category/{}/product?languageId=-2&showProducts=false&appId=1'
    product_detail_url = "https://www.pullandbear.com/itxrest/2/catalog/store/24009401/20309425/category/0/product/{}/detail?languageId=-2&appId=11"
