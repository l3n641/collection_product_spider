from .ripcurl import RipcurlSpider


class RipcurlSeSpider(RipcurlSpider):
    name = 'ripcurl_se'

    product_list_url = 'https://www.ripcurl.eu/sv/Store/Services/ProductSearch.ashx?r=list&c={}&sort=8&p={}&s=12'
    product_detail_url = 'https://www.ripcurl.eu/sv/Store/Services/Products.ashx?type=product&id={}'
