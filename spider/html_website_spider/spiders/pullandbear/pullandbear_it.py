from .pullandbear import PullandbearSpider


class PullandbearItSpider(PullandbearSpider):
    name = 'pullandbear_it'

    category_url = 'https://www.pullandbear.com/itxrest/3/catalog/store/24009405/20309428/category/{}/product?languageId=-4&showProducts=false&appId=1'
    product_detail_url = "https://www.pullandbear.com/itxrest/2/catalog/store/24009405/20309428/category/0/product/{}/detail?languageId=-4&appId=1"
