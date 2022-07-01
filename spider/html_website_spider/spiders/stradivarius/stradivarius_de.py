from .stradivarius import Stradivarius


class StradivariusDe(Stradivarius):
    name = 'stradivarius_de'
    allowed_domains = ['www.stradivarius.com']
    BASE_URL = "https://www.stradivarius.com/"
    detail_api_url = 'https://www.stradivarius.com/itxrest/2/catalog/store/54009554/50331059/category/0/product/{}/detail?languageId=-3&appId=1'
