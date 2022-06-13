import json

import scrapy
from ..libs.productExcel import ProductExcel
from ..items import ProductUrlItem, ProductDetailItem
import re
from datetime import datetime


class HmFrSpider(scrapy.Spider):
    name = 'hm_fr'
    allowed_domains = ['www2.hm.com']
    BASE_URL = "https://www2.hm.com/"

    def __init__(self, category_file_path=None, *args, **kwargs):
        self.category_file_path = category_file_path
        super(HmFrSpider).__init__(*args, **kwargs)

    def start_requests(self):
        path = self.category_file_path
        excel = ProductExcel(path)
        data = excel.get_category()
        for url in data.keys():
            meta = {
                "category_name": data.get(url)
            }
            yield scrapy.Request(url, meta=meta, callback=self.parse_product_list)

    def parse_product_list(self, response, **kwargs):
        product_detail_url_xpath = '//h3[@class="item-heading"]/a'
        next_page_url_xpath = '//a[@class="pagination-links-list"]'
        data = response.xpath(product_detail_url_xpath)
        category_name = response.meta.get("category_name")
        meta = {"category_name": category_name}
        for item in data:
            url = self.BASE_URL + item.attrib.get("href")
            item_data = {
                "category_name": category_name,
                "url": url,
                "referer": response.url,
            }
            yield ProductUrlItem(**item_data)

            yield scrapy.Request(url=url, meta=meta, callback=self.parse_product_detail)

        next_page_element = response.xpath(next_page_url_xpath)
        if next_page_element and (next_href := next_page_element.attrib.get("href")):
            yield scrapy.Request(url=next_href, meta=meta, callback=self.parse_product_list)

    def parse_product_detail(self, response, **kwargs):
        product_schema_xpath = '//script[@id="product-schema"]'
        data = response.xpath(product_schema_xpath)
        if data:
            script_content = response.xpath('//script[@id="product-schema"]')[0].root.text
            product_data = json.loads(script_content)
            script_tags = response.xpath('//script')
            for tags in script_tags:
                res = tags.re("var productArticleDetails = {")

                if res:
                    sku_data = self.get_sku_data_in_script_tag(product_data.get("sku"), tags.root.text)
                    if not sku_data:
                        continue
                    images = self.get_images(sku_data, "http")
                    size = self.get_size(sku_data)
                    price = self.get_price(sku_data)

                    item = {
                        "PageUrl": response.url,
                        "category_name": response.meta.get("category_name"),
                        "sku": product_data.get("sku"),
                        "color": product_data.get("color"),
                        "size": size,
                        "img": images,
                        "price": price,
                        "title": product_data.get("name"),
                        "dade": datetime.now(),
                        "basc": product_data.get("description"),
                        "brand": '',
                    }
                    yield ProductDetailItem(**item)

    @staticmethod
    def get_images(sku_data, scheme="https"):
        img_pattern = "'fullscreen': isDesktop \? '.*' : '(.*)',"
        res = re.findall(img_pattern, sku_data.strip())
        if not res:
            return False
        images = []
        for img in res:
            images.append(f"{scheme}:{img}")

        return images

    @staticmethod
    def get_size(sku_data):
        pattern = "'sizes':\[(.*?)\],"
        result = re.search(pattern, sku_data, flags=re.DOTALL)
        if result:
            return re.findall("'name': '(.*?)'", result.group(1))
        return None

    @staticmethod
    def get_price(sku_data: str) -> str:
        pattern = "'whitePriceValue': '(.+?)'"
        result = re.search(pattern, sku_data, flags=re.DOTALL)
        if result:
            return result.group(1)
        return None

    @staticmethod
    def get_sku_data_in_script_tag(sku, string):
        sku_pattern = "'sku': \{(.*?)'productAttributes':".replace('sku', sku)
        res = re.search(sku_pattern, string, flags=re.DOTALL)
        if res:
            return res.group(1)
        return False
