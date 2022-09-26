from .pullandbear import PullandbearSpider


class PullandbearPtSpider(PullandbearSpider):
    name = 'pullandbear_pt'

    category_url = 'https://www.pullandbear.com/itxrest/3/catalog/store/24009410/20309429/category/{}/product?languageId=-6&showProducts=false&appId=1'
    product_detail_url = "https://www.pullandbear.com/itxrest/2/catalog/store/24009410/20309429/category/0/product/{}/detail?languageId=-6&appId=1"
