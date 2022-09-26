import scrapy
from ..common_spider import CommonSpider
from .. import ProductUrlItem, ProductDetailItem
import json
from datetime import datetime
from html import unescape
from urllib.parse import urlparse


class TrespassSpider(CommonSpider):
    name = 'trespass'
    allowed_domains = ['trespass.com']

    def parse_product_list(self, response):
        product_xpath = '//div[@class="product-item-photo-wrapper"]/a[1]'
        next_page_xpath = '//a[@title="Next"][1]'
        data = response.xpath(product_xpath)
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

        next_page_node = response.xpath(next_page_xpath)
        if next_page_node and (next_page_href := next_page_node.attrib.get("href")):
            yield scrapy.Request(next_page_href, meta=response.meta, callback=self.parse_product_list,
                                 errback=self.start_request_error, dont_filter=True)

    def parse_product_detail(self, response):
        ATTRIBUTE_COLOR_CODE = "501"
        ATTRIBUTE_SIZE_CODE = "475"
        json_xpath = "//script[@type='application/ld+json']/text()"
        json_data = response.xpath(json_xpath).get()
        data = json.loads(json_data)
        description = unescape(data.get("description"))
        title = unescape(data.get("name"))
        swatch_options_stt = response.xpath('//script[@type="text/x-magento-init"]/text()')[11].root
        swatch_options = json.loads(swatch_options_stt)
        swatch_renderer = swatch_options.get('[data-role=swatch-options]').get('Magento_Swatches/js/swatch-renderer')
        json_config = swatch_renderer.get('jsonConfig')
        color_options = json_config.get('attributes').get(ATTRIBUTE_COLOR_CODE).get("options")
        size_options = json_config.get('attributes').get(ATTRIBUTE_SIZE_CODE).get("options")
        price_options = json_config.get('optionPrices')

        size_list = []
        for item in size_options:
            size_list.append(item.get("label"))

        images_options = json_config.get('images')
        base_sku = data.get("sku")
        for option in color_options:
            if not option.get('products'):
                continue
            color = option.get("label")
            product_id = option.get('products')[0]
            images = self.get_images_by_product(product_id, images_options)
            price = self.get_product_price(product_id, price_options)
            item_data = {
                "project_name": self.project_name,
                "PageUrl": response.url,
                "html_url": swatch_renderer.get('productUrl'),
                "category_name": response.meta.get("category_name"),
                "sku": base_sku + "_" + product_id,
                "color": color,
                "size": size_list,
                "img": images,
                "price": price,
                "title": title,
                "dade": datetime.now(),
                "basc": description,
                "brand": ""
            }

            yield ProductDetailItem(**item_data)

    def start_requests_test(self):
        url = "https://www.trespass.com/occupy-female-jkt-tp75#color_code=Navy"
        url = "https://www.trespass.com/kelby-womens-waterproof-jacket#color_code=Navy"

        # url = "https://www.trespass.com/tayah-ii-womens-waterproof-jacket"

        yield scrapy.Request(url, callback=self.parse_product_detail, dont_filter=True)

    @staticmethod
    def get_images_by_product(product_id: str, images):
        image_list = []
        color_images = images.get(product_id)
        if not color_images:
            return image_list

        if isinstance(color_images, dict):
            for image_id in color_images:
                src = color_images[image_id].get("full")
                image_list.append(src)
        else:
            for image in color_images:
                src = image.get("full")
                image_list.append(src)

        return image_list

    @staticmethod
    def get_product_price(product_id: str, option_prices):
        data = option_prices.get(product_id)
        return data.get("finalPrice").get("amount")
