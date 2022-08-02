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


class ColumbiaSpider(CommonSpider):
    name = 'columbia'
    allowed_domains = ['columbia.com']
    custom_settings = {
        'COOKIES_ENABLED': False,
        # "HTTPERROR_ALLOWED_CODES": [301, 302]
    }
    cookie = {
        'Cookie': 'dwac_fda2d388bbd237d68a4b025507=zoytg71ES3Nj9FB2g-OgIC6Lmyriz6ioFsA=|dw-only|||USD|false|US/Pacific|true; cqcid=denRXCybMAU2ne7kaScsBV4gLX; cquid=||; sid=zoytg71ES3Nj9FB2g-OgIC6Lmyriz6ioFsA; dwanonymous_6148ff3835e27262c32d6dc123dc430d=denRXCybMAU2ne7kaScsBV4gLX; dwsid=jPiXEoensQyvPTpojNHHdmz_obvYLFLX2gmMS7JzC0otBUhxPGMu2O1lfVPm3rM7rhRzDYeUqMJkReWyDht0iw==; scarab.visitor="56CE8EF8A53BD898"; _scid=53b36a5b-37b2-4ca2-98f9-436401aabec3; crl8.fpcuid=4a999995-4bf3-448d-b321-9dde45db169e; fs_uid=#15X7RY#5554747954892800:5500864251498496:::#/1690699953; _clck=177xzfm|1|f3l|0; sn.vi=a0a8f069-baa0-4885-87a8-7a9a8825ba20; sn.tpc=1; __cq_dnt=0; dw_dnt=0; mt.v=2.296599446.1659163962614; pxcts=35fa18f3-0fd4-11ed-ad88-5646786a7245; _pxvid=35fa0f20-0fd4-11ed-ad88-5646786a7245; __cq_uuid=denRXCybMAU2ne7kaScsBV4gLX; s_ecid=MCMID|58636964946623580917091301943753416973; AMCVS_BA9115F354F6053E0A4C98A4@AdobeOrg=1; AMCV_BA9115F354F6053E0A4C98A4@AdobeOrg=1176715910|MCMID|58636964946623580917091301943753416973|MCAID|NONE|MCOPTOUT-1659171164s|NONE|vVersion|5.4.0; s_cc=true; _ga=GA1.2.307794973.1659163965; _gid=GA1.2.1844773800.1659163965; _gcl_au=1.1.16207949.1659163965; countrySelectionCookie=US; _pin_unauth=dWlkPVlXUTNOVEptTkRJdE56TTBaQzAwTVRkaUxXRmtaRGN0WWpJMU5UUTJZbVpsTWpVeA; _fbp=fb.1.1659163965809.1535261248; _hjFirstSeen=1; _hjSession_50530=eyJpZCI6IjUxNzExMDYxLWM0NTEtNGExYS05YjhjLWVhZGZhNDQ5ZDk1MiIsImNyZWF0ZWQiOjE2NTkxNjM5NjYxMjksImluU2FtcGxlIjpmYWxzZX0=; _hjIncludedInSessionSample=0; _hjIncludedInPageviewSample=1; _hjAbsoluteSessionInProgress=0; _sctr=1|1659110400000; _hjSessionUser_50530=eyJpZCI6IjhkMDUyM2U3LWU0MzEtNTc4ZC05YTQwLTQ2YWEzZWIzZTMzOCIsImNyZWF0ZWQiOjE2NTkxNjM5NjUzNjUsImV4aXN0aW5nIjp0cnVlfQ==; _sp_ses.0415=*; NoCookie=true; BVImplmain_site=20425; __cq_bc={"bcpx-Columbia_US":[{"id":"1693931"},{"id":"RL2436"},{"id":"2012271"}]}; BVBRANDID=a2f6374b-55a9-4d9c-ab21-6f3e29cf4c1c; s_sq=[[B]]; __cq_seg=0~0.56!1~0.03!2~-0.44!3~-0.46!4~0.27!5~-0.17!6~-0.31!7~-0.28!8~-0.05!9~0.06; prev_pt=Category Grid; gpv_pn=men jackets insulated & down | columbia; OptanonConsent=isGpcEnabled=0&datestamp=Sat+Jul+30+2022+17:31:30+GMT+0800+(中国标准时间)&version=6.32.0&isIABGlobal=false&hosts=&genVendors=&landingPath=NotLandingPage&groups=1:1,2:1,3:1,4:1&AwaitingReconsent=false; s_getNewRepeat=1659173491424-New; mt.aa=KIBO-SUPPORT-Do-Nothing:Experiment|KIBO-SUPPORT-Do-Nothing:Experiment|KIBO-SUPPORT-Do-Nothing:Experiment|COL-US-AB-Test_1626657:Experiment|KIBO-SUPPORT-Do-Nothing:Experiment|KIBO-SUPPORT-Do-Nothing:Experiment|KIBO-SUPPORT-Do-Nothing:Experiment|KIBO-SUPPORT-Do-Nothing:Experiment; s_ptc=0.00^^0.00^^0.00^^0.34^^1.19^^0.00^^24.28^^0.03^^25.86; _uetsid=301815b00fd411edb2e60f2bc13c2073; _uetvid=301847b00fd411edb3cae7ce42ad3a8a; _sp_id.0415=738bd127-6b7d-4670-a6a5-59c5ed7d839b.1659164167.1.1659173516.1659164167.1a75adaf-a102-43ac-a4f2-c87e5e193c4c; mp_columbia_us_mixpanel={"distinct_id": "1824de0c7bfe86-078dd7b903ab8d-26021a51-1fa400-1824de0c7c0b39","bc_persist_updated": 1659173516998,"language": "en_us"}; _clsk=wwr266|1659173523724|37|1|l.clarity.ms/collect; _px3=37ceb675a70a7a15fef9133183170a79523a4e40cbf53b4b18e45451b0795fa9:ZwG9ymnetfeHhbgoIXJSUgzsNWynCBU2gRq+duvS1raw0e3h2Q2MD0VWETEB7WHkC0q1fPEgEfH3xch65FkGEQ==:1000:LC6qxcWm+S78rqQ/0OGS2wxwYiZi+F8NLgZzgkUIOtktOx2EMQOBeeZ1LkjsQtGDphvkyVUjb450mF80wTP5nANGp7Bn/aqAbg2e+SVS37jQcPZrTBdO0/GoJQmgf7BHwPrpRIvXvRtuMM7qOTF61ck6QCBd0Rk6Rnsn+hSGiPwuA65iaIA0JaNVpTTq0iJr6gF7BnGqQL1p6/oesMCrug=='
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

    @staticmethod
    def get_product_url_list(url):

        xpath = '//div[@class="product"]//div[@class="product__add-to-cart__quickshop"]/button'
        response = requests.get(url, timeout=60)
        html = etree.HTML(response.text)
        result = html.xpath(xpath)
        urls = []
        for item in result:
            uri = item.attrib.get('data-link')
            detail_url = "https://www.columbia.com" + uri
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
        description = data.get("product").get("productPitch")
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
