import scrapy
from ..common_spider import CommonSpider
from .. import ProductUrlItem, ProductDetailItem
import json
from datetime import datetime
from urllib.parse import urlencode
from urllib.parse import quote
import requests
import re
from lxml import etree


class MountainHardWear(CommonSpider):
    name = 'mountainhardwear'
    allowed_domains = ['mountainhardwear.com']
    base_url = "https://www.mountainhardwear.com"
    custom_settings = {
        'COOKIES_ENABLED': False,
    }
    cookie = {
        'Cookie': 'dwac_2314ef0a4e3bf154027e7b0a03=m9cm7GHcgnlAaHh_50h6h997TU2lc4jMhRg=|dw-only|||USD|false|US/Pacific|true; cqcid=abLIyEv4xasEw63FWZUurJCKcc; cquid=||; sid=m9cm7GHcgnlAaHh_50h6h997TU2lc4jMhRg; dwanonymous_4180976787daf04df56d6331b4ab4c51=abLIyEv4xasEw63FWZUurJCKcc; _pxhd=z27ZpD1akUen6i-C63MoigNByfoZigXJ7ff-9aWgQrNE/t963zi9ZCvGKs5zAyASeIV9ylV9F5hkDaawUgNeDQ==:WXeZF1hxPhVqjpwzz8oWxNPNivKNpNkyZz6ksvTblvm8tKp-dT6tXwNmDW7kGPy6OD309u8O5681n86v8w0FGQ24TuiNVbTXdWMTPrgXg7A=; __cq_dnt=0; dw_dnt=0; dwsid=B-x4BmxoNhVPrOtqbkAUJUNAE6eoxzygityvFyX-P-E0h7y9haFITBdX--yqjSPvjdOkZ0_2rMUjHSvoIEYDNg==; mt.v=2.1731408561.1661341844066; AMCVS_BA9115F354F6053E0A4C98A4@AdobeOrg=1; AMCV_BA9115F354F6053E0A4C98A4@AdobeOrg=1176715910|MCMID|51244806396797582155282456427927665108|MCAID|NONE|MCOPTOUT-1661349044s|NONE|vVersion|5.4.0; s_fm=excamp; pxcts=fcb77caa-23a2-11ed-b632-66754b484241; _pxvid=fa626b08-23a2-11ed-bc4f-694171415347; s_campaign=paidsearch|google adwords us|841403263|42200254319|mountain hardwear||; s_cc=true; _gcl_au=1.1.90937631.1661341846; __cq_uuid=abpW7OjUPgPhOIETtL3B3rGU1H; __cq_seg=0~0.00!1~0.00!2~0.00!3~0.00!4~0.00!5~0.00!6~0.00!7~0.00!8~0.00!9~0.00; _gcl_aw=GCL.1661341848.EAIaIQobChMInbXi0bTf-QIVuD6tBh3UgwUjEAAYASAAEgJfJ_D_BwE; _ga=GA1.2.1269081526.1661341848; _gid=GA1.2.363203523.1661341848; _gac_UA-16517994-1=1.1661341848.EAIaIQobChMInbXi0bTf-QIVuD6tBh3UgwUjEAAYASAAEgJfJ_D_BwE; _fbp=fb.1.1661341849040.1929314945; _pin_unauth=dWlkPVpqRmxOR1JqWm1JdE5EazNNQzAwWkdSa0xUZzJNREl0TTJJM05qWm1PRFE0T1RFeg; scarab.visitor="56CE8EF8A53BD898"; crl8.fpcuid=598634cd-cac3-43ab-a8c5-66da848ce6fa; _scid=8209751c-b84a-486d-9ece-af75052c478a; _sctr=1|1661270400000; sn.vi=a0a8f069-baa0-4885-87a8-7a9a8825ba20; sn.tpc=1; _clck=xdhdt5|1|f4a|0; _hjSessionUser_57931=eyJpZCI6IjdlYTc1NTIxLWVmMDItNWZhOC04ODg2LTljNGU2ZmUwMDgzYiIsImNyZWF0ZWQiOjE2NjEzNDE4NDg1NzYsImV4aXN0aW5nIjp0cnVlfQ==; countrySelectionCookie=US; s_sq=[[B]]; __pxvid=92fb6415-23a5-11ed-9b88-0242ac120002; OptanonConsent=isGpcEnabled=0&datestamp=Wed+Aug+24+2022+20:09:16+GMT+0800+(中国标准时间)&version=6.32.0&isIABGlobal=false&hosts=&genVendors=&landingPath=NotLandingPage&groups=1:1,2:1,3:1,4:1&AwaitingReconsent=false; s_ptc=0.00^^0.00^^0.00^^0.00^^1.22^^0.19^^4.92^^0.53^^6.71; _sp_id.30d8=30cc971a-e5cc-4393-b15d-536873be3331.1661341875.1.1661342961.1661341875.f6fa6147-6a64-4cd3-a144-7fa8effc5022; mp_mountain_hardwear_us_mixpanel={"distinct_id": "182cfb0e770b6-00e308b88b2d3d-26021d51-1fa400-182cfb0e771f74","bc_persist_updated": 1661342963502,"language": "en_us"}; _uetsid=02b8b72023a311eda1712d74619972b1; _uetvid=02b8dc2023a311edbe4dd115384b17b0; s_getNewRepeat=1661342986519-New; _px3=54086f81408fe408a82c760f7e7323d04640dadfbfbef957b5e011f2a6992e04:PkyAjFGczLT/f2uyuw6ZC/WX1lkalUvk/fJ7wmXULckTCkj7uUsr76/gTq8thIeXBlssrHC66Oh9dIuDAAj6Og==:1000:CkdW0Yydme9PC5/Bx4IRhs6yWXlzhF/SJYoDDo8ahxucFyt2eoOc+XwjNc3zkThv2+x1F7+nExXW+2B5UfJ73Uxk1mYW+Lm9UObi7Pq9OrdnsEjdJzoHxVYai1kAoPZShVpu8EgrsG4qgm3a7DxDBVGsv53WKqCUOffLwwzpE7sVlXFFyEN3M5aWrQX8/ohsO3vR7TU3S+Coyaq5wqigGQ==; fs_uid=#15X8DR#6075601144418304:4828689527377920:::#/1692877855; _clsk=7fhil5|1661348398394|1|0|l.clarity.ms/collect'
    }

    def start_by_product_category(self):
        """
        从产品分类里爬取数据
        :return:
        """

        product_category = self.product_category
        for url in product_category.keys():
            meta = {
                "category_name": product_category.get(url),
                "referer": url,

            }

            yield scrapy.Request(url, meta=meta, callback=self.parse_product_list, cookies=self.cookie,
                                 errback=self.start_request_error,
                                 dont_filter=True)

    def parse_product_list(self, response, **kwargs):
        pattern = "window.digitalData =(.*)\|\|"
        json_data = response.selector.re(pattern)
        try:
            data = json.loads(json_data[0])
        except Exception as e:
            res = requests.get(response.meta.get("referer"), timeout=60)
            text = res.text
            match_obj = re.search(pattern, text)
            data = json.loads(match_obj.group(1))
        page_url = data.get("page").get('pageInfo').get('pageURL')
        page_url = page_url + "&all=true"
        urls = self.get_product_url_list(page_url)
        for url in urls:
            meta = response.meta.copy()
            detail_url = url.replace("Product-ShowQuickView", "Product-Variation")
            meta["detail_url"] = detail_url

            product_log = None  # 数据库记录
            if self.is_continue:
                product_log = self.get_product_log(detail_url, response.meta.get("category_name"))
                if product_log and product_log.status == 1:
                    continue

            if not product_log:
                item_data = {
                    "category_name": response.meta.get("category_name"),
                    "url": detail_url,
                    "referer": response.meta.get("referer"),
                    "status": 0,
                    "page_url": page_url,
                }
                yield ProductUrlItem(**item_data)

            for task in self.get_product_detail(detail_url, response.meta.get("category_name")):
                yield task

    def get_product_url_list(self, url):
        xpath = '//div[@class="product"]//div[@class="product__add-to-cart__quickshop"]/button'
        response = requests.get(url, timeout=60)
        html = etree.HTML(response.text)
        result = html.xpath(xpath)
        urls = []
        for item in result:
            uri = item.attrib.get('data-link')
            detail_url = self.base_url + uri
            urls.append(detail_url)
        return urls

    def get_product_detail(self, detail_url, category_name):

        res = requests.get(detail_url, timeout=60)
        data = res.json()
        product = data.get("product")
        title = product.get('variantName')
        product_id = product.get("id")
        size = []
        color_attr = {}
        for attr in product.get("variationAttributes"):
            if attr.get('attributeId') == "color":
                color_attr = attr

            if attr.get('attributeId') == "size":
                size = [v.get('displayValue') for v in attr.get('values')]
        description = data.get("product").get("longDescription")
        for item in color_attr.get("values"):
            sku = product_id + "_" + item.get("id")
            images = [d.get('retinaUrl') for d in item.get("images").get("large")]
            item_data = {
                "project_name": self.project_name,
                "PageUrl": detail_url,
                "html_url": item.get('pdpUrl'),
                "category_name": category_name,
                "sku": sku,
                "color": item.get('displayValue'),
                "size": size,
                "img": images,
                "price": item.get('salesPrice').get('value'),
                "title": title,
                "dade": datetime.now(),
                "basc": description,
                "brand": ""
            }

            yield ProductDetailItem(**item_data)
