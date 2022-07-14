from .ripcurl import RipcurlSpider


class RipcurlPtSpider(RipcurlSpider):
    name = 'ripcurl_pt'

    product_list_url = 'https://www.ripcurl.eu/pt/Store/Services/ProductSearch.ashx?r=list&c={}&sort=8&p={}&s=12'
    product_detail_url = 'https://www.ripcurl.eu/pt/Store/Services/Products.ashx?type=product&id={}'
