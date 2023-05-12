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

class ConverseSpider(CommonSpider):
    name = 'converse'
    allowed_domains = ['www.converse.com']
    BASE_URL = "https://www.converse.com/"
    nike_consumer_designs_api = 'https://api.nike.com/customization/consumer_designs/v1?filter=shortId({})'

    def parse_product_list(self, response):
        product_list_xpath = '//a[@class="product-tile__img-url"]'
        next_page_xpath = '//button[@data-loading-state="unloaded"]'
        data = response.xpath(product_list_xpath)
        for item in data:
            item_data = {
                "category_name": response.meta.get("category_name"),
                "detail_url": item.attrib.get("href"),
                "referer": response.meta.get("referer"),
                "page_url": response.url,
                "meta": response.meta,
                "callback": self.parse_product_detail,
            }
            for task in self.request_product_detail(**item_data):
                yield task

        next_button = response.xpath(next_page_xpath)
        if next_button:
            page_size = 21
            start = response.meta.get("start", 0)
            url_info = urlparse(response.url)
            next_start = start + page_size
            query = dict(parse_qsl(url_info.query))
            query['start'] = next_start
            query['sz'] = page_size
            params = urlencode(query)
            next_url = f"https://{url_info.hostname}{url_info.path}?{params}"
            response.meta['start'] = next_start
            yield scrapy.Request(next_url, meta=response.meta, callback=self.parse_product_list)

    def parse_product_detail(self, response):
        title_xpath = '//p[@data-product-name]/text()'
        price_xpath = '//meta[@itemprop="price"]'
        description_xpath = '//div[@id="pdp-more-info"]//div[@class="pdp-tab__content-wrap"]'
        spu_path = '//input[@name="mid"]'
        extra_image_xpath = '//div[@data-converse-custom]'
        product_info_xpath = '//a[@data-thumbs]'
        size_xpath = '//select[@id="variationDropdown-size" ]/option/text()'
        product_items = response.xpath(product_info_xpath)
        title = response.xpath(title_xpath).get()
        spu = response.xpath(spu_path).attrib.get("value")
        price = response.xpath(price_xpath).attrib.get("content")
        description = response.xpath(description_xpath).get()
        size_item = response.xpath(size_xpath)
        size_list = []

        if size_item:
            for item in size_item[1:]:
                size = html.unescape(item.get().strip())
                size_list.append(size)

        custom_data = response.xpath(extra_image_xpath)

        for item in product_items:
            data_thumbs = item.attrib.get("data-thumbs")
            data_thumbs = html.unescape(data_thumbs)
            color = item.attrib.get("data-swatch-id") or ""
            url_hash = hashlib.md5(response.url.encode(encoding='UTF-8')).hexdigest()
            sku = spu + "_" + url_hash + "_" + color.strip().replace(" ", '-').replace("/", "-").replace("\\", "-")
            data = json.loads(data_thumbs)
            images = []
            for img in data:
                src = img.get("src").replace("?sw=460", "?sw=1200")
                images.append(src)

            if custom_data and (img_node := item.xpath('img[@class="swatch-img"]')):
                inspiration_id = self.get_inspiration_id(img_node.attrib.get("src"))
                extra_images = self.get_extra_image(inspiration_id)
                if extra_images:
                    images = extra_images

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

    def get_extra_image(self, inspiration_id):
        url = self.nike_consumer_designs_api.format(inspiration_id)
        try:
            response = requests.get(url)
            data = response.json()
            object = data.get("objects")[0]
            imagery = object.get("imagery")
            images = []
            for item in imagery:
                url = item.get("imageSourceURL").replace("&wid=2000", "&wid=1200")
                images.append(url)

            return images

        except Exception as e:
            return False

    @staticmethod
    def get_inspiration_id(img):
        return img.split('/')[6].split("-")[1]
