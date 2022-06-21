from .massimodutti import Massimodutti


class MassimoduttiNl(Massimodutti):
    name = 'massimodutti_nl'
    detail_api_url = "https://www.massimodutti.com/itxrest/2/catalog/store/34009453/30359501/category/0/product/{}/detail?languageId=100&appId=1"
