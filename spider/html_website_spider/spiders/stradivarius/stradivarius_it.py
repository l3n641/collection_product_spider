from .stradivarius import Stradivarius


class StradivariusIt(Stradivarius):
    name = 'stradivarius_it'
    allowed_domains = ['www.stradivarius.com']
    BASE_URL = "https://www.stradivarius.com/"
    detail_api_url = 'https://www.stradivarius.com/itxrest/2/catalog/store/54009555/50331088/category/0/product/{}/detail?languageId=-4&appId=1'
