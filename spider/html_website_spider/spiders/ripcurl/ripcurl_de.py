from .ripcurl import RipcurlSpider


class RipcurlDeSpider(RipcurlSpider):
    name = 'ripcurl_de'

    product_list_url = 'https://www.ripcurl.eu/de/Store/Services/ProductSearch.ashx?r=list&c={}&sort=8&p={}&s=12'
    product_detail_url = 'https://www.ripcurl.eu/de/Store/Services/Products.ashx?type=product&id={}'
