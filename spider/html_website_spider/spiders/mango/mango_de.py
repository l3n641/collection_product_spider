from .mango import MangoSpider


class MangoDeSpider(MangoSpider):
    name = 'mango_de'
    headers = {
        "stock-id": "004.AL.0.true.false.v0"
    }