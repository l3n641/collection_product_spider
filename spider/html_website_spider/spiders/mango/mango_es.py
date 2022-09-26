from .mango import MangoSpider


class MangoEsSpider(MangoSpider):
    name = 'mango_es'
    headers = {
        "stock-id": "021.ES.0.true.false.v0"
    }