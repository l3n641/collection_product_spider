from .ripcurl import RipcurlSpider


class RipcurlEsSpider(RipcurlSpider):
    name = 'ripcurl_es'

    product_list_url = 'https://www.ripcurl.eu/es/Store/Services/ProductSearch.ashx?r=list&c={}&sort=8&p={}&s=12'
    product_detail_url = 'https://www.ripcurl.eu/es/Store/Services/Products.ashx?type=product&id={}'
