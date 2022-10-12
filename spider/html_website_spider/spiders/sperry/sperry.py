import scrapy
from ..common_indirect_spider import CommonIndirectSpider
from .. import ProductUrlItem, ProductDetailItem
from datetime import datetime
import json
from urllib.parse import urlparse, urlunparse, urlencode


class SperrySpider(CommonIndirectSpider):
    name = 'sperry'
    allowed_domains = ['www.sperry.com']
    base_url = 'https://www.sperry.com'

    def parse_product_list(self, response, **kwargs):
        load_more_xpath = '//button[@class="load-more-cta cta-primary"]'
        product_xpath = '//a[@class="thumb-link"]'

        has_next = response.xpath(load_more_xpath)

        if has_next:
            start = response.meta.get("start", 0) + 48

            query = {
                "refn1": "isOnSale",
                "prefv1": "false",
                "format": "load-more",
                "start": start,
                "sz": 48,
            }
            params = urlencode(query)
            parse = urlparse(response.url)
            new_parse = parse._replace(query=params)
            next_page = urlunparse(new_parse)
            response.meta["start"] = start
            yield scrapy.Request(next_page, meta=response.meta, callback=self.parse_product_list,
                                 errback=self.start_request_error, dont_filter=True)

        result = response.xpath(product_xpath)

        for item in result:
            href = item.attrib.get("href")

            for task in self.add_product_detail_url(href, response.meta.get("category_name"),
                                                    response.meta.get("referer"), response.url):
                yield task

    def parse_product_detail(self, response, ):
        title_xpath = '//meta[@name="keywords"]'
        price_xpath = '//span[@itemprop="price"]/text()'
        size_data_xpath = "//div[contains(@id,'productDimensionsAndVariations-')]/text()"
        image_xpath = '//a[@class="product-image main-product-image"]'
        json_str = response.xpath(size_data_xpath).get().strip()
        data = json.loads(json_str)
        color_id_xpath = "//input[@id='updateColorVal']"
        product_id_xpath = "//input[@id='updateProductid']"

        title = response.xpath(title_xpath).attrib.get("content")
        price = response.xpath(price_xpath).get()
        image_nodes = response.xpath(image_xpath)
        color_id = response.xpath(color_id_xpath).attrib.get("value")
        product_id = response.xpath(product_id_xpath).attrib.get("value")
        sku = product_id + "_" + color_id
        images = []
        for node in image_nodes:
            images.append(node.attrib.get("data-src"))

        size_list = []

        if data.get("size"):
            for item in data.get("size").get("values"):
                size_list.append(item.get("displayValue"))

        color = ""
        if data.get("color"):
            for item in data.get("color").get("values"):
                if item.get("ID") == color_id:
                    color = item.get("displayValue")

        desc_re = 'var.*?meta.*?=.*?"(.*)";'
        description = response.selector.re_first(desc_re)
        sub_title = title.rsplit("-", 1)
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
            "title": sub_title[0],
            "dade": datetime.now(),
            "basc": description,
            "brand": ""
        }

        yield ProductDetailItem(**item_data)
