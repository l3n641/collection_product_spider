from .pullandbear import PullandbearSpider


class PullandbearSeSpider(PullandbearSpider):
    name = 'pullandbear_se'

    category_url = 'https://www.pullandbear.com/itxrest/3/catalog/store/24009412/20309424/category/{}/product?languageId=-25&showProducts=false&appId=1'
    product_detail_url = "https://www.pullandbear.com/itxrest/2/catalog/store/24009412/20309424/category/0/product/{}/detail?languageId=-25&appId=1"
