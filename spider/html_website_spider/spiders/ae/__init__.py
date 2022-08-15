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


class AESpider(CommonSpider):
    name = 'ae'
    allowed_domains = ['ae.com']

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
