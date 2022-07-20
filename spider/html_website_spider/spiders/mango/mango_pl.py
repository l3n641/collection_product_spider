from .mango import MangoSpider


class MangoPlSpider(MangoSpider):
    name = 'mango_pl'
    headers = {
        "stock-id": "060.PL.0.true.false.v3"
    }