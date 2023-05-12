import json
import requests
import scrapy
from ..common_direct_spider import CommonDirectSpider
from .. import ProductUrlItem, ProductDetailItem
from datetime import datetime
import lxml
from urllib.parse import urlencode
from urllib.parse import urlparse, parse_qsl


class PurificacionGarciaEsSpider(CommonDirectSpider):
    name = 'purificaciongarcia_es'
    allowed_domains = ['purificaciongarcia.com']
    base_url = "https://purificaciongarcia.com"

    @staticmethod
    def get_category_id(url):
        response = requests.get(url)
        selector = lxml.etree.HTML(response.text)
        xpath = '//meta[@name="pageId"]'
        node = selector.xpath(xpath)
        return node[0].attrib.get("content")

    def build_product_list_url(self, category_id):
        params = {
            "ajaxStoreImageDir": "/wcsstore/PGStorefrontAssetStore/",
            "searchType": "1002",
            "storeId": "715837946",
            "sType": "SimpleSearch",
            "enableSKUListView": "false",
            "disableProductCompare": "false",
            "langId": "-5",
            "categoryId": category_id,
            "pageSize": "15",
            "pageNum": "0",
        }
        url = "https://purificaciongarcia.com/ProductListingView?"
        query = urlencode(params)
        return url + query

    def parse_product_list(self, response, **kwargs):
        xpath = '//meta[@name="pageId"]'
        node = response.xpath(xpath)
        category_id = node.attrib.get("content")
        product_list_url = self.build_product_list_url(category_id)
        yield scrapy.Request(product_list_url, meta=response.meta, callback=self.parse_product_list2,
                             errback=self.start_request_error, dont_filter=True)

    def parse_product_list2(self, response, **kwargs):
        product_url_xpath = '//div[@ class="product-info"]/a'

        product_info = response.xpath(product_url_xpath)

        for item in product_info:

            detail_url = item.attrib.get("href")
            item_data = {
                "category_name": response.meta.get("category_name"),
                "detail_url": detail_url,
                "referer": response.meta.get("referer"),
                "page_url": response.url,
                "meta": response.meta,
                "callback": self.parse_product_detail,
            }

            for task in self.request_product_detail(**item_data):
                yield task

        if product_info:
            url_info = urlparse(response.url)
            params = dict(parse_qsl(url_info.query))
            params["pageNum"] = int(params.get("pageNum")) + 1
            url = "https://purificaciongarcia.com/ProductListingView?"
            query = urlencode(params)
            next_url = url + query
            yield scrapy.Request(next_url, meta=response.meta, callback=self.parse_product_list2,
                                 errback=self.start_request_error)

    def parse_product_detail(self, response):
        product_info_xpath = '//script[@id="productJSON"]'
        color_xpath = '//div[@id="swatch_selection_entitledItem_Color"]/text()'
        data_str = response.xpath(product_info_xpath)[0].root.text.strip().replace("STL.skus = ", "").strip(";")
        product_data = json.loads(data_str)[0]

        title = product_data.get("name")
        url_hash = self.get_url_md5(response.url)
        sku = product_data.get("uniqueID") + "_" + url_hash[:6]
        description = product_data.get("longDescription")
        price = int(product_data.get("offerPrice"))
        color = response.xpath(color_xpath).get().strip()

        images = []
        for item in product_data.get("images"):
            if item.get("typeImage") == "ZO":
                images = item.get("imageURL")

        sizes = []

        item_data = {
            "project_name": self.project_name,
            "PageUrl": response.url,
            "html_url": response.url,
            "category_name": response.meta.get("category_name"),
            "sku": sku,
            "color": color,
            "size": sizes,
            "img": images,
            "price": price,
            "title": title,
            "dade": datetime.now(),
            "basc": description,
            "brand": product_data.get("brand")
        }

        yield ProductDetailItem(**item_data)

    def start_requests1(self):
        url = 'https://purificaciongarcia.com/es/es/hombre-6887670-5/accesorios-6887671-5/calcetines-6887676-5'
        yield scrapy.Request(url, callback=self.parse_product_list, errback=self.start_request_error,
                             dont_filter=True)
