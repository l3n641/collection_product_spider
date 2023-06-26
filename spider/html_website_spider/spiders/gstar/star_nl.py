import json
import scrapy
from .. import ProductUrlItem, ProductDetailItem
import re
from datetime import datetime
from ..common_spider import CommonSpider
import json
from urllib.parse import urlparse, parse_qsl
from urllib.parse import urlencode
import html
import requests
import hashlib


class GStarNlSpider(CommonSpider):
    name = 'star_nl'
    allowed_domains = ['www.g-star.com']
    BASE_URL = "https://www.g-star.com"
    product_list_api = 'https://www.g-star.com/nl_nl/api/v1/'

    def start_by_product_category(self):
        """
        从产品分类里爬取数据
        :return:
        """
        product_category = self.product_category
        for url in product_category.keys():
            url_info = urlparse(url)
            *_, category = url_info.path.split("/", 2)
            list_url = self.product_list_api + category
            meta = {
                "category_name": product_category.get(url),
                "referer": url,

            }
            yield scrapy.Request(list_url, meta=meta, callback=self.parse_product_list,
                                 errback=self.start_request_error,
                                 dont_filter=True)

    def parse_product_list(self, response):
        data = response.json()
        products = data.get("products")

        for item in products:
            variants = item.get("availableStyleVariantsSorted")
            for variant in variants:
                detail_url = self.BASE_URL + variant.get("productUrl")

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

        current_page = data.get("currentPage", 0)
        total_page = data.get("numberOfPages")
        next_page = current_page + 1
        if next_page <= total_page:
            url_info = urlparse(response.url)
            query = dict(parse_qsl(url_info.query))
            query['page'] = next_page
            params = urlencode(query)
            next_url = f"https://{url_info.hostname}{url_info.path}?{params}"
            yield scrapy.Request(next_url, meta=response.meta, callback=self.parse_product_list)

    def parse_product_detail(self, response):
        data_xpath = '//script[@type="application/ld+json"]/text()'
        size_xpath = '//option[@class="productSizeSelection-select-option "]'
        data_str = response.xpath(data_xpath).get()
        json_data = json.loads(data_str)
        sku = json_data.get("sku")
        color = json_data.get("color")
        images = []
        for img in json_data.get("image"):
            images.append(img.replace(",h_630", ",h_1200"))
        description = json_data.get("description")
        pattern = re.compile(r'<[^>]+>', re.S)
        description = pattern.sub('', description)
        offers = json_data.get("offers")
        title = json_data.get("name")
        price = offers.get("price")
        size_list = []
        options = response.xpath(size_xpath)
        for opt in options:
            size_list.append(opt.attrib.get("value"))

        item_data = {
            "project_name": self.project_name,
            "PageUrl": response.url,
            "html_url": response.url,
            "category_name": response.meta.get("category_name"),
            "sku": sku,
            "color": color,
            "size": size_list,
            "img": images,
            "price": price,
            "title": title,
            "dade": datetime.now(),
            "basc": description,
            "brand": ""
        }
        if item_data:
            yield ProductDetailItem(**item_data)
