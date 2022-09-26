from .pullandbear import PullandbearSpider


class PullandbearEsSpider(PullandbearSpider):
    name = 'pullandbear_es'

    category_url = 'https://www.pullandbear.com/itxrest/3/catalog/store/24009400/20309422/category/{}/product?languageId=-5&showProducts=false&appId=1'
    product_detail_url = "https://www.pullandbear.com/itxrest/2/catalog/store/24009400/20309422/category/0/product/{}/detail?languageId=-5&appId=1"
