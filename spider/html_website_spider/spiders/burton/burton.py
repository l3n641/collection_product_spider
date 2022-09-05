import json

import scrapy
from ..common_spider import CommonSpider
from .. import ProductUrlItem, ProductDetailItem
from datetime import datetime

from urllib.parse import urlparse
import requests
import re


class BurtonSpider(CommonSpider):
    name = 'burton'
    allowed_domains = ['burton.com']
    base_url = "https://www.burton.com"
    category_url = "https://www.burton.com/us/en"
    detail_url = "https://www.burton.com/on/demandware.store/Sites-Burton_NA-Site/en_US/Product-Variation?dwvar_{}_variationColor={}&pid={}&quantity=1"

    def start_by_product_category(self):
        """
        从产品分类里爬取数据
        :return:
        """

        product_category = self.product_category
        for url in product_category.keys():
            result = urlparse(url)
            category_id = result.path.split("/")[-1]
            api_url = self.category_url + f"/c/{category_id}?format=ajax"
            meta = {
                "category_name": product_category.get(url),
                "referer": url,
            }
            yield scrapy.Request(api_url, meta=meta, callback=self.parse_product_list,
                                 errback=self.start_request_error, dont_filter=True)

    def parse_product_list(self, response, **kwargs):
        try:
            data = response.json()
        except Exception:
            pattern = "<wainclude.*?>"
            text = re.sub(pattern, '{}', response.text)
            data = json.loads(text)

        product_data = data.get("data")
        if not product_data:
            product_data = data
        page_meta = product_data.get("meta")

        if page_meta.get("currentPage") < page_meta.get("pageCount"):
            page_size = page_meta.get("pageSize")
            start = page_meta.get("currentPage") * page_size
            url = response.url + f"&concise=true&start={start}&sz={page_size}"
            yield scrapy.Request(url, meta=response.meta, callback=self.parse_product_list,
                                 errback=self.start_request_error, dont_filter=True)

        for item in product_data.get("hits"):
            hit = item.get("hit")
            if not hit:
                continue
            product_id = hit.get("ID")
            represented_colors = item.get("representedColors")
            detail_html_url = self.base_url + hit.get("href")

            for color_id in represented_colors:
                detail_api_url = self.detail_url.format(product_id, color_id, product_id)
                meta = response.meta.copy()
                meta["color_id"] = color_id
                meta["detail_html_url"] = detail_html_url
                item_data = {
                    "category_name": response.meta.get("category_name"),
                    "detail_url": detail_api_url,
                    "referer": response.meta.get("referer"),
                    "page_url": response.url,
                    "meta": meta,
                    "callback": self.parse_product_detail,
                }

                for task in self.request_product_detail(**item_data):
                    yield task

    def get_product_data(self, url):
        response = requests.get(url, timeout=30)

        product_name_pattern = '"productName":"(.*?)"'
        result = re.search(product_name_pattern, response.text, flags=re.DOTALL)
        if not result:
            product_name_pattern = '"name":"(.*?)","subtitle"'
            result = re.search(product_name_pattern, response.text, flags=re.DOTALL)

        product_name = result.group(1)

        desc_pattern = '"longDescription":"<p>(.*?)(<\\\/p>|</p>)"'
        result = re.search(desc_pattern, response.text, flags=re.DOTALL)
        desc = ""
        if result:
            desc = result.group(1)
        else:
            desc_pattern = '"shortDescription":"<p>(.*?)(<\\\/p>|</p>)"'
            result = re.search(desc_pattern, response.text, flags=re.DOTALL)
            if result:
                desc = result.group(1)

        return {
            "title": product_name,
            "description": desc
        }

    def parse_product_detail(self, response):
        data = response.json()
        html_url = response.meta.get("detail_html_url")

        product_info = self.get_product_data(html_url)

        product = data.get("product")
        price = product.get("price").get("list").get("value")
        images = []
        for image in product.get("images"):
            images.append(image.get("url"))

        color_id = response.meta.get("color_id")
        sku = product.get("id") + "_" + color_id
        color = ""
        sizes = []
        variation_attributes = product.get("variationAttributes")
        for attribute in variation_attributes:
            if attribute.get("displayName") == "Color" and attribute.get("displayValue") != 'NO COLOR':
                color = attribute.get("displayValue")

            if attribute.get("displayName") == "Size":
                for sub_value in attribute.get('values'):
                    sizes.append(sub_value.get("displayValue"))

        item_data = {
            "project_name": self.project_name,
            "PageUrl": response.url,
            "html_url": html_url,
            "category_name": response.meta.get("category_name"),
            "sku": sku,
            "color": color,
            "size": sizes,
            "img": images,
            "price": price,
            "title": product_info.get("title"),
            "dade": datetime.now(),
            "basc": product_info.get("description"),
            "brand": ""
        }

        yield ProductDetailItem(**item_data)
