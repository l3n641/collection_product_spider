from .stradivarius import Stradivarius


class StradivariusFr(Stradivarius):
    name = 'stradivarius_fr'
    allowed_domains = ['www.stradivarius.com']
    BASE_URL = "https://www.stradivarius.com/"
    detail_api_url = 'https://www.stradivarius.com/itxrest/2/catalog/store/54009551/50331069/category/0/product/{}/detail?languageId=-2&appId=1'
