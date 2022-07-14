from .ripcurl import RipcurlSpider


class RipcurlNlSpider(RipcurlSpider):
    name = 'ripcurl_nl'

    product_list_url = 'https://www.ripcurl.eu/nl/Store/Services/ProductSearch.ashx?r=list&c={}&sort=8&p={}&s=12'
    product_detail_url = 'https://www.ripcurl.eu/nl/Store/Services/Products.ashx?type=product&id={}'
