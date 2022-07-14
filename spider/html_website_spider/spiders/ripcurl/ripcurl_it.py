from .ripcurl import RipcurlSpider


class RipcurlItSpider(RipcurlSpider):
    name = 'ripcurl_it'

    product_list_url = 'https://www.ripcurl.eu/it/Store/Services/ProductSearch.ashx?r=list&c={}&sort=8&p={}&s=12'
    product_detail_url = 'https://www.ripcurl.eu/it/Store/Services/Products.ashx?type=product&id={}'
