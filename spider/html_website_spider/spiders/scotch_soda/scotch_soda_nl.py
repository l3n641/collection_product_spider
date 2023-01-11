import json

import scrapy
from ..common_spider import CommonSpider
from .. import ProductUrlItem, ProductDetailItem
from datetime import datetime


class ScotchSodaNlSpider(CommonSpider):
    name = 'scotchsoda_nl'
    allowed_domains = ['scotch-soda.com']
    base_url = "https://www.scotch-soda.com"

    custom_settings = {
        "CONCURRENT_REQUESTS": 4,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2,
    }

    def parse_product_list(self, response, **kwargs):
        product_url_xpath = '//div[@class="product-trigger__media"]/a'
        next_page_xpath = '//a[@class="btn btn-secondary js-lazy-products"]'

        product_info = response.xpath(product_url_xpath)

        for item in product_info:

            detail_url = item.attrib.get("href")
            item_data = {
                "category_name": response.meta.get("category_name"),
                "detail_url": detail_url,
                "referer": response.meta.get("referer"),
                "page_url": response.url,
                "meta": response.meta,
                "callback": self.parse_product_detail,
            }

            for task in self.request_product_detail(**item_data):
                yield task

        next_page_node = response.xpath(next_page_xpath)
        if next_page_node:
            next_url = next_page_node.attrib.get("href")
            yield scrapy.Request(next_url, meta=response.meta, callback=self.parse_product_list,
                                 errback=self.start_request_error)

    def parse_product_detail(self, response):
        img_xpath = "//li[contains(@class,'carousel--pdp__item')]/a"
        size_xpath = '//option[@data-size]'
        product_info_xpath = '//script[@type="application/ld+json"]'
        color_xpath = '//span[@id="gtm_product_data"]'

        data_str = response.xpath(product_info_xpath)[0].root.text.strip()
        product_data = json.loads(data_str)
        title = product_data.get("name")
        description = product_data.get("description")
        price = product_data.get("offers").get('price')
        data_gtm_product_data_str = response.xpath(color_xpath).attrib.get("data-gtm-product-data")
        data_gtm_product_data = json.loads(data_gtm_product_data_str)
        color = data_gtm_product_data.get("variant")
        sku = data_gtm_product_data.get("variantGroupId")
        images = []
        for node in response.xpath(img_xpath):
            src = node.attrib.get("href").replace("?sw=1125", "?sw=1300")
            images.append(src)

        sizes = []
        for node in response.xpath(size_xpath):
            sizes.append(node.attrib.get("data-size"))

        item_data = {
            "project_name": self.project_name,
            "PageUrl": response.url,
            "html_url": response.url,
            "category_name": response.meta.get("category_name"),
            "sku": sku,
            "color": color,
            "size": sizes,
            "img": images,
            "price": price,
            "title": title,
            "dade": datetime.now(),
            "basc": description,
            "brand": product_data.get("brand")
        }

        yield ProductDetailItem(**item_data)

    def start_requests1(self):
        url = 'https://www.scotch-soda.com/nl/nl/heren/kleding/essentials/sweater-met-ronde-hals-van-biologisch-katoen/165318.html?dwvar_165318_color=Grey%20Melange&cgid=76'
        yield scrapy.Request(url, callback=self.parse_product_detail, errback=self.start_request_error,
                             dont_filter=True)
