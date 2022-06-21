from .stradivarius import Stradivarius


class StradivariusPt(Stradivarius):
    name = 'stradivarius_pt'
    allowed_domains = ['www.stradivarius.com']
    BASE_URL = "https://www.stradivarius.com/"
    detail_api_url = 'https://www.stradivarius.com/itxrest/2/catalog/store/54009560/50331100/category/0/product/{}/detail?languageId=-6&appId=1'
