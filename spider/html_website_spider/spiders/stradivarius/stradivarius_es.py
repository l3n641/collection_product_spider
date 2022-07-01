from .stradivarius import Stradivarius


class StradivariusEs(Stradivarius):
    name = 'stradivarius_es'
    allowed_domains = ['www.stradivarius.com']
    BASE_URL = "https://www.stradivarius.com/"
    detail_api_url = 'https://www.stradivarius.com/itxrest/2/catalog/store/54009550/50331075/category/0/product/{}/detail?languageId=-5&appId=1'
