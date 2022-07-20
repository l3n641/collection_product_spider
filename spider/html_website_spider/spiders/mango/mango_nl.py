from .mango import MangoSpider


class MangoNlSpider(MangoSpider):
    name = 'mango_nl'
    headers = {
        "stock-id": "003.NL.0.true.false.v1"
    }
