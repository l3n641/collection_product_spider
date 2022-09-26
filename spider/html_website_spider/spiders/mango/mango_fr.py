from .mango import MangoSpider


class MangoFrSpider(MangoSpider):
    name = 'mango_fr'
    headers = {
        "stock-id": "011.FR.0.true.false.v1"
    }