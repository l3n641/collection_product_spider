from .stradivarius import Stradivarius


class StradivariusNl(Stradivarius):
    name = 'stradivarius_nl'
    allowed_domains = ['www.stradivarius.com']
    BASE_URL = "https://www.stradivarius.com/"
    detail_api_url = 'https://www.stradivarius.com/itxrest/2/catalog/store/54009553/50331085/category/0/product/{}/detail?languageId=100&appId=1'
