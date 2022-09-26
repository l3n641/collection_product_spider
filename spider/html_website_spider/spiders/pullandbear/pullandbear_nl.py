from .pullandbear import PullandbearSpider


class PullandbearNlSpider(PullandbearSpider):
    name = 'pullandbear_nl'

    category_url = 'https://www.pullandbear.com/itxrest/3/catalog/store/24009403/20309426/category/{}/product?languageId=100&showProducts=false&appId=1'
    product_detail_url = "https://www.pullandbear.com/itxrest/2/catalog/store/24009403/20309426/category/0/product/{}/detail?languageId=100&appId=1"
