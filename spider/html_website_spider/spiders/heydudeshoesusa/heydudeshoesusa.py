import json
import scrapy
from .. import ProductUrlItem, ProductDetailItem
import re
from datetime import datetime
from ..common_spider import CommonSpider
import json
from urllib.parse import urlparse


class HeydudeshoesusaSpider(CommonSpider):
    name = 'heydudeshoesusa'
    allowed_domains = ['www.heydudeshoesusa.com']
    BASE_URL = "https://www.heydudeshoesusa.com"

    def parse_product_list(self, response):
        link_xpath = '//a[@data-product-title]'
        next_page_button = '//load-more-pagination'
        data = response.xpath(link_xpath)
        for item in data:
            link = self.BASE_URL + item.attrib.get("href")
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
            page = response.meta.get("page", 1)

            if page * 45 <= int(load_button.attrib.get("data-limit")):
                next_page = page + 1
                response.meta['page'] = next_page
                url_info = urlparse(response.url)
                new_url = f'{url_info.scheme}://{url_info.hostname}{url_info.path}?page={next_page}'
                yield scrapy.Request(new_url, meta=response.meta, callback=self.parse_product_list, dont_filter=True)

    def parse_product_detail(self, response):
        data_xpath = '//coco-shuffle'
        description_xpath = '//meta[@name="description"]'
        title_xpath = "//h1[@data-display-title]/text()"
        color_sale_xpath = "//span[@data-sale-color-label-display]/text()"
        color_xpath = "//span[@data-color-label-display]/text()"
        images_xpath = '//div[@data-product-images]/div[@data-index]/img'
        price_xpath = '//meta[@property="og:price:amount" ]'
        size_xpath = '//input[@data-action="option-choice"]'
        data = response.xpath(data_xpath)
        color = response.xpath(color_xpath).get() or response.xpath(color_sale_xpath).get()
        color = color.strip() if color else ""
        description = response.xpath(description_xpath).attrib.get("content")
        category_name = response.meta.get("category_name")
        title = response.xpath(title_xpath).get()
        # result = json.loads(data.attrib.get("data-products-json"))
        sku = response.selector.re_first("ProductID:(.*)")
        sku = sku.strip().strip(",")
        size_list = []
        for size_item in response.xpath(size_xpath).attrib.get("value"):
            size_list.append(size_item.split('/')[0])

        images = []
        for image_item in response.xpath(images_xpath):
            url = "https:" + image_item.attrib.get("src")
            images.append(url)

        price = response.xpath(price_xpath).attrib.get("content")

        item_data = {
            "project_name": self.project_name,
            "PageUrl": response.url,
            "html_url": response.url,
            "category_name": category_name,
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
