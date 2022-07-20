from .mango import MangoSpider


class MangoPtSpider(MangoSpider):
    name = 'mango_pt'
    headers = {
        "stock-id": "010.PO.0.true.false.v0"
    }
