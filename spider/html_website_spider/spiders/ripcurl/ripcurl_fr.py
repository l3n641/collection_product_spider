from .ripcurl import RipcurlSpider


class RipcurlFrSpider(RipcurlSpider):
    name = 'ripcurl_fr'

    product_list_url = 'https://www.ripcurl.eu/fr/Store/Services/ProductSearch.ashx?r=list&c={}&sort=8&p={}&s=12'
    product_detail_url = 'https://www.ripcurl.eu/fr/Store/Services/Products.ashx?type=product&id={}'
