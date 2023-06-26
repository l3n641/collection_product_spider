from .wolfordshop_nl import WolfordshopNlSpider

class WolfordshopDeSpider(WolfordshopNlSpider):
    name = 'wolfordshop_de'
    allowed_domains = ['www.wolfordshop.de']
    BASE_URL = "https://www.wolfordshop.de"
    image_prefix = "https://www.wolfordshop.de/dw/image/v2/BBCH_PRD"
