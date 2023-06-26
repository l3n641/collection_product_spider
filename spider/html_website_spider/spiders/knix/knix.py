import html
import json
import scrapy
from .. import ProductUrlItem, ProductDetailItem
import re
from datetime import datetime
from ..common_spider import CommonSpider
import json
from urllib.parse import urlparse


class KnixSpider(CommonSpider):
    name = 'knix'
    allowed_domains = ['www.knix.com']
    BASE_URL = "https://www.knix.com"

    def parse_product_list(self, response):
        link_pattern = '&quot;,&quot;handle&quot;:&quot;(.*?)&quot;,&quot;description'
        data = response.selector.re(link_pattern)
        for item in data:
            link = self.BASE_URL + "/products/" + item
            item_data = {
                "category_name": response.meta.get("category_name"),
                "detail_url": link,
                "referer": response.meta.get("referer"),
                "page_url": response.url,
                "meta": response.meta,
                "callback": self.parse_product_detail,
            }
            for task in self.request_product_detail(**item_data):
                yield task

    def parse_product_detail(self, response):
        json_str_pattern = "var json_product =(.*);</script><script>"
        json_str = response.selector.re_first(json_str_pattern)
        product_data_xpath = '//div[@class="cProduct"]'
        product_data = response.xpath(product_data_xpath).attrib.get("data-config")
        if json_str and product_data and (data := json.loads(json_str.strip())):
            product_data = json.loads(html.unescape(product_data))

            price = data.get("price") / 100
            description = html.unescape(data.get("description"))
            title = data.get("title")
            sku = data.get("id")
            options = data.get("options")
            color_index = None
            size_index = None
            for index, opt in enumerate(options):
                if opt == "Color":
                    color_index = index

                if opt == "Size":
                    size_index = index

            color = ""
            if color_index is not None:
                color = data.get("variants")[0].get("options")[color_index]

            size_list = []
            if size_index:
                for var in data.get("variants"):
                    size_list.append(var.get("options")[size_index])
            images = []

            for image in data.get("images"):
                img_url = f"https:{image}"
                images.append(img_url)

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
                "brand": "Knix"
            }
            if item_data:
                yield ProductDetailItem(**item_data)



    def start_requests(self):

        url = 'https://knix.com/products/super-leakproof-cheeky-dark-cherry'
        yield scrapy.Request(url, callback=self.parse_product_detail, errback=self.start_request_error,
                             dont_filter=True)

