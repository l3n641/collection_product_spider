from .mango import MangoSpider


class MangoItSpider(MangoSpider):
    name = 'mango_it'
    headers = {
        "stock-id": "005.IT.0.true.false.v0"
    }