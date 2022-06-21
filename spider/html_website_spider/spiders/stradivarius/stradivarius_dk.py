from .stradivarius import Stradivarius


class StradivariusDk(Stradivarius):
    name = 'stradivarius_dk'
    allowed_domains = ['www.stradivarius.com']
    BASE_URL = "https://www.stradivarius.com/"
    detail_api_url = 'https://www.stradivarius.com/itxrest/2/catalog/store/56009558/50331085/category/0/product/{}/detail?languageId=-39&appId=1'
