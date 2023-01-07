import json
import scrapy
from .. import ProductUrlItem, ProductDetailItem
import re
from datetime import datetime
from ..common_spider import CommonSpider
import json
from urllib.parse import urlparse
from html import unescape
from scrapy.http import FormRequest


class SamedelmanSpider(CommonSpider):
    name = 'samedelman'
    allowed_domains = ['www.samedelman.com']
    BASE_URL = "https://www.samedelman.com"
    product_list_api = "https://platform.cloud.coveo.com/rest/search/v2"
    authorization = 'Bearer xx6b22c1da-b9c6-495b-9ae1-e3ac72612c6f'
    custom_settings = {
    }

    def parse_product_list(self, response):
        category_data_xpath = '//div[@data-sc-filter-scope-node]'
        initialize_context_pattern = 'CoveoForSitecoreUserContext.handler.initializeContext\((.*?)\);'
        category_data = response.xpath(category_data_xpath)
        if not category_data:
            return
        else:
            try:
                data_filter_scope = unescape(category_data.attrib.get("data-sc-filter-scope-node"))
            except Exception as e:
                print(e)

            url_info = urlparse(response.url)
            categories = "|".join(url_info.path.split("/")[2:]).replace("-", " ")
            data_json = json.loads(data_filter_scope)
            aq_param = self.build_aq_param(categories, data_json.get("advanced"))
            # aq_param="""(@categories=="Boots and Booties|Booties") ((@webgenders="Women's" @webdepartment==Shoes))"""
            context = response.selector.re_first(initialize_context_pattern)
            form_data = {
                "aq": aq_param,
                "searchHub": 'SamEdelman_Listing',
                "locale": 'en',
                "maximumAge": "900000",
                "firstResult": "0",
                "numberOfResults": "500",
                "context": context,
            }
            meta = response.meta
            meta["form_data"] = form_data
            headers = {
                "authorization": self.authorization
            }
            yield FormRequest(self.product_list_api, formdata=form_data, meta=meta, callback=self.parse_product_list2,
                              dont_filter=True, headers=headers)

    def parse_product_list2(self, response):
        data = response.json()
        if data.get("totalCount") < 1:
            print(1)
        for product in data.get('results'):
            if product.get("childResults"):
                for item in product.get("childResults"):
                    detail_url = self.BASE_URL + item.get("raw").get("producturi")
                    item_data = {
                        "category_name": response.meta.get("category_name"),
                        "detail_url": detail_url,
                        "referer": response.meta.get("referer"),
                        "page_url": response.url,
                        "meta": response.meta,
                        "callback": self.parse_product_detail,
                        "dont_filter": True
                    }
                    for task in self.request_product_detail(**item_data):
                        yield task
            else:
                detail_url = self.BASE_URL + product.get("raw").get("producturi")
                item_data = {
                    "category_name": response.meta.get("category_name"),
                    "detail_url": detail_url,
                    "referer": response.meta.get("referer"),
                    "page_url": response.url,
                    "meta": response.meta,
                    "callback": self.parse_product_detail,
                    "dont_filter": True
                }
                for task in self.request_product_detail(**item_data):
                    yield task

    def parse_product_detail(self, response):
        data_pattern = 'window.productDetailData =(.*);'
        product_data_str = response.selector.re_first(data_pattern)
        product_data = json.loads(product_data_str)
        product = product_data.get("Product")
        sku = product.get("ProductGroupId") + "_" + product.get("ProductId")
        color = product.get("Color")
        title = product.get("Name")
        description = product.get("Description")
        price = product.get("ListPriceNumeric")
        images = []
        for img in product.get("Images"):
            if img.get("IsVideo") == False:
                resize = img.get('ResizedProductImages')
                for img_item in resize:
                    if img_item.get("Preset") == "Feed1000":
                        images.append(img_item.get("Url"))

        size_list = []

        for var in product.get("Variants"):
            size_list.append(var.get("Size"))

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
            "brand": product.get("Brand").get("Description")
        }
        if item_data:
            yield ProductDetailItem(**item_data)

    @staticmethod
    def build_aq_param(categories, advanced):
        aq = f'(@categories=="{categories}") '
        if advanced.get("type") == "and":
            # @categories==Heels) ((@webgenders="Women's" @webdepartment==Shoes))

            left = advanced.get("left")
            right = advanced.get("right")
            left_query = f'@{left.get("fieldName")}{left.get("operator").get("name")}"{left.get("fieldValues")[0]}"'
            right_query = f'@{right.get("fieldName")}{right.get("operator").get("name")}"{right.get("fieldValues")[0]}"'
            return f' {aq} (({left_query} {right_query}))'

        else:
            # (@categories=="Boots and Booties") (@webgenders=girls)
            query = f'@{advanced.get("fieldName")}{advanced.get("operator").get("name")}"{advanced.get("fieldValues")[0]}"'
            return f' {aq} ({query})'
