import scrapy
from ..common_spider import CommonSpider
from .. import ProductUrlItem, ProductDetailItem
from datetime import datetime
import requests
from lxml import etree
import json


class RipcurlSpider(CommonSpider):
    name = 'ripcurl'
    allowed_domains = ['ripcurl.eu']
    base_url = 'https://www.ripcurl.eu'

    product_list_url = 'https://www.ripcurl.eu/en/Store/Services/ProductSearch.ashx?r=list&c={}&sort=8&p={}&s=12'
    product_detail_url = 'https://www.ripcurl.eu/en/Store/Services/Products.ashx?type=product&id={}'

    def parse_product_list(self, response, **kwargs):
        category_xpath = '//*[@id="codagenicCategory"]'

        result = response.xpath(category_xpath)
        category_id = result.attrib.get("data-category-id")
        total_page = int(result.attrib.get("data-total-pages"))
        for i in range(0, total_page):
            url = self.product_list_url.format(category_id, i + 1)
            yield scrapy.Request(url=url, meta=response.meta, callback=self.parse_product_list_2)

    def parse_product_list_2(self, response):
        data = response.json().get('Data')
        for product in data.get("Products"):
            description_url = self.base_url + product.get("Url")

            item_data = {
                "category_name": response.meta.get("category_name"),
                "url": description_url,
                "referer": response.meta.get("referer"),
            }
            yield ProductUrlItem(**item_data)
            response.meta["detail_url"] = self.product_detail_url.format(product.get("ProductId"))
            yield scrapy.Request(url=description_url, meta=response.meta, callback=self.parse_product_detail_1)

    def parse_product_detail_1(self, response):
        try:
            xpath = "//script[@type='application/ld+json']/text()"
            json_data = response.xpath(xpath).get()
            data = json.loads(json_data)
            description = data.get("description")
        except Exception as e:
            description = ''

        response.meta["description"] = description
        detail_url = response.meta.get("detail_url")
        yield scrapy.Request(url=detail_url, meta=response.meta, callback=self.parse_product_detail_2)

    def parse_product_detail_2(self, response):
        data = response.json().get("data")
        product_id = data.get('id')
        brand = data.get("brand")
        description = response.meta.get("description")
        colours = data.get("colours")
        title = data.get("title")
        variations = data.get("variations")

        for color_item in colours:
            sku = f"{product_id}_{color_item.get('code')}"
            if product_data := self.get_product_data_by_color(color_item.get("code"), variations):
                item_data = {
                    "project_name": self.project_name,
                    "PageUrl": response.url,
                    "category_name": response.meta.get("category_name"),
                    "sku": sku,
                    "color": color_item.get("name"),
                    "size": product_data.get("sizes"),
                    "img": product_data.get("img"),
                    "price": product_data.get("price"),
                    "title": title,
                    "dade": datetime.now(),
                    "basc": description,
                    "brand": brand
                }
                yield ProductDetailItem(**item_data)

    @staticmethod
    def get_product_data_by_color(color_code, variations: list):
        first_item = []
        sizes = []
        item_data = None
        for variation in variations:
            if variation.get("colourCode") == color_code:
                if not first_item:
                    first_item = variation
                if variation.get("sizeCode") not in sizes:
                    sizes.append(variation.get("sizeCode"))
        if first_item:
            images = [item.get("url") for item in first_item.get("images")]
            item_data = {
                "sizes": sizes,
                "img": images,
                "price": first_item.get("defaultPrice").get("value"),
            }

        return item_data

    @staticmethod
    def get_description(url):
        try:
            response = requests.get(url, timeout=30)
            root = etree.HTML(response.text)
            xpath = "//script[@type='application/ld+json']"
            items = root.xpath(xpath)
            data = json.loads(items[0].text)
            return data.get("description")
        except Exception as e:
            return ''
