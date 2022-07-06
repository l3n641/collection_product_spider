from .pullandbear import PullandbearSpider


class PullandbearPlSpider(PullandbearSpider):
    name = 'pullandbear_pl'

    category_url = 'https://www.pullandbear.com/itxrest/3/catalog/store/25009524/20309427/category/{}/product?languageId=-22&showProducts=false&appId=1'
    product_detail_url = "https://www.pullandbear.com/itxrest/2/catalog/store/25009524/20309427/category/0/product/{}/detail?languageId=-22&appId=1"
