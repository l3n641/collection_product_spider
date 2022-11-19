import json
import scrapy
from .. import ProductUrlItem, ProductDetailItem
import re
from datetime import datetime
from ..common_spider import CommonSpider
import json
from urllib.parse import urlparse


class ChacosSpider(CommonSpider):
    name = 'chacos'
    allowed_domains = ['www.chacos.com']
    BASE_URL = "https://www.chacos.com/US/en"

    def parse_product_list(self, response):
        link_xpath = '//a[@class="name-link"]'
        next_page_button = '//div[@class="load-more-row"]/button[@data-grid-url]'
        data = response.xpath(link_xpath)
        for item in data:
            link = item.attrib.get("href")
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

        if load_button := response.xpath(next_page_button):
            next_url = load_button.attrib.get("data-grid-url")
            yield scrapy.Request(next_url, meta=response.meta, callback=self.parse_product_list, dont_filter=True)

    def parse_product_detail(self, response):
        title_xpath = '//div[@class="product-v2-name"]/h1/text()'
        price_xpath = '//form[@class="pdpForm"]//span[@itemprop="price"]/text()'
        product_id_xpath = '//span[@itemprop="productId"]/text()'
        color_code_xpath = '//input[@id="updateColorVal"]'
        color_xpath = "//span[contains(@class,'variant-color-name')]/text()"
        image_xpath = '//div[@id="js-product-image-slider"]//img[contains(@class,"product-img")]'
        description_pattern = 'var meta     = "(.*)";'
        product_id = response.xpath(product_id_xpath).get()
        color_code = response.xpath(color_code_xpath).attrib.get("value")
        sku = f"{product_id}_{color_code}"
        color = response.xpath(color_xpath).get()
        size_data_xpath = f'//div[@id="productDimensionsAndVariations-{product_id}"]/text()'

        size_list = []

        size_data_str = response.xpath(size_data_xpath).get()
        if size_data_str:
            product_data = json.loads(size_data_str.strip())
            for size in product_data.get("size").get("values"):
                size_list.append(size.get("displayValue"))

        description = response.selector.re_first(description_pattern)

        title = response.xpath(title_xpath).get().strip()
        price = response.xpath(price_xpath).get()
        images = []
        image_data = response.xpath(image_xpath)
        for img in image_data:
            img_src = img.attrib.get("src") or img.attrib.get('data-lazy')
            if img_src and img_src.startswith("https"):
                images.append(img_src)

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
