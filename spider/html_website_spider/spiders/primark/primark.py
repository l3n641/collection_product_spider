import scrapy
from ..common_spider import CommonSpider
from .. import ProductUrlItem, ProductDetailItem
import json
from datetime import datetime
from urllib.parse import urlencode
from urllib.parse import quote
import requests


class PrimarkSpider(CommonSpider):
    name = 'primark'
    allowed_domains = ['primark.com', 'pritesttech.com']
    api_url = 'https://api-001.pritesttech.com/bff?'
    locale = "en-gb"
    currency_code = "GBP"

    def parse_product_list(self, response, **kwargs):
        json_xpath = '//*[@id="__NEXT_DATA__"]/text()'
        json_data = response.xpath(json_xpath).get()
        page_size = 24
        start = 0
        num_found = 1
        data = json.loads(json_data)
        page_props = data.get("props").get("pageProps")
        slug = page_props.get("slug")
        encoded_slug = page_props.get("encodedSlug")

        while start < num_found:

            data = self.get_product_list_data(start, slug, encoded_slug, page_size)
            product_data = data.get("data").get("categoryNavItem").get("props").get("productsData")
            num_found = product_data.get("response").get("numFound")
            products = product_data.get("response").get("docs")
            start = start + page_size

            for product in products:
                variables = {
                    "categorySlug": product.get("url"),
                    "locale": self.locale,
                    "currencyCode": self.currency_code,
                    "styleCode": product.get("pid"),
                    "lastVisitedPlpSlug": slug
                }
                extensions = {"persistedQuery": {"version": 1,
                                                 "sha256Hash": "9a6e9e4bb0dd506a804a31c4bddbd9f4684d3a326eea0560b034037237523c71"}}

                params = {
                    "operationName": "Pdp",
                    "variables": json.dumps(variables),
                    "extensions": json.dumps(extensions),
                }
                detail_url = self.api_url + urlencode(params)
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

    def get_product_list_data(self, start, slug, encoded_slug, page_size):

        variables = {
            "categorySlug": slug,
            "q": encoded_slug,
            "start": start,
            "rows": page_size,
            "locale": self.locale,
            "fq": {},
            "sort": ""
        }

        extensions = {"persistedQuery": {"version": 1,
                                         "sha256Hash": "99dacba984d12e44b18e9f5dcf8fc50b8f3309861e9119cdc531a5ec8b377f95"}}

        params = {
            "operationName": "getPlpProducts",
            "variables": json.dumps(variables),
            "extensions": json.dumps(extensions),
        }
        category_url = self.api_url + urlencode(params)
        response = requests.get(category_url, timeout=60)
        data = response.json()
        return data

    def parse_product_list_2(self, response):
        data = response.json()
        product_data = data.get("data").get("categoryNavItem").get("props").get("productsData")
        products = product_data.get("response").get("docs")
        last_visited_plp_slug = response.meta.get("variables").get("q")

        for product in products:
            variables = {
                "categorySlug": product.get("url"),
                "locale": self.locale,
                "currencyCode": self.currency_code,
                "styleCode": product.get("pid"),
                "lastVisitedPlpSlug": last_visited_plp_slug
            }
            extensions = {"persistedQuery": {"version": 1,
                                             "sha256Hash": "9a6e9e4bb0dd506a804a31c4bddbd9f4684d3a326eea0560b034037237523c71"}}

            params = {
                "operationName": "Pdp",
                "variables": json.dumps(variables),
                "extensions": json.dumps(extensions),
            }
            detail_url = self.api_url + urlencode(params)
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

    def parse_product_detail(self, response, ):

        try:
            data = response.json()
        except Exception as e:
            data = requests.get(response.url).json()

        products = data.get("data").get("pdp").get("props").get("productData").get("products")

        for product in products:
            images = []

            for item in product.get("images"):
                image = item.get("url") + "?w=1200"
                images.append(image)

            size_list = [product.get("displaySize")]
            for item in product.get("variants"):
                size_list.append(item.get("displaySize"))
            size_list.sort()

            item_data = {
                "project_name": self.project_name,
                "PageUrl": response.url,
                "html_url": product.get("slug"),
                "category_name": response.meta.get("category_name"),
                "sku": product.get("sku"),
                "color": product.get("displayColor"),
                "size": size_list,
                "img": images,
                "price": product.get("masterPrice")[1:],
                "title": product.get("name"),
                "dade": datetime.now(),
                "basc": product.get("longDisplayDescription"),
                "brand": ""
            }

            yield ProductDetailItem(**item_data)
