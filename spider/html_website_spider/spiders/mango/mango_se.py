from .mango import MangoSpider


class MangoSeSpider(MangoSpider):
    name = 'mango_se'
    headers = {
        "stock-id": "030.SV.0.true.false.v2"
    }