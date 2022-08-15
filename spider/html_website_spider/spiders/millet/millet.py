import scrapy
from ..common_spider import CommonSpider
from .. import  ProductDetailItem
import json
from datetime import datetime


class MilletSpider(CommonSpider):
    name = 'millet'
    allowed_domains = ['millet.fr']

    def start_by_product_category(self):
        """
        从产品分类里爬取数据
        :return:
        """

        product_category = self.product_category
        for url in product_category.keys():
            meta = {
                "category_name": product_category.get(url),
                "referer": url,
            }
            request_url = url + "?limit=all"

            yield scrapy.Request(request_url, meta=meta, callback=self.parse_product_list,
                                 errback=self.start_request_error, dont_filter=True)

    def parse_product_list(self, response, **kwargs):
        link_xpath = '//div[@class="product-colors"]//a'
        links = []
        for link in response.xpath(link_xpath):
            links.append(link.attrib.get("href"))
            detail_url = link.attrib.get("href")
            response.meta["color"] = link.attrib.get("title")
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

    def parse_product_detail(self, response):
        product_name_xpath = '//h1[@class="product-name"]/span/text()'
        price_xpath = '//meta[@itemprop="price"]'
        sku_xpath = '//meta[@itemprop="sku"]'
        description_xpath = '//div[@itemprop="description"]/text()'
        image_xpath = "//img[contains(@class,'gallery-image')]"
        title = response.xpath(product_name_xpath).get()
        price = response.xpath(price_xpath).attrib.get("content")
        sku = response.xpath(sku_xpath).attrib.get("content")
        description = response.xpath(description_xpath).get()
        images = []
        for img in response.xpath(image_xpath):
            images.append(img.attrib.get("src"))
        size = []
        pattern = 'configJson =(.*);'
        size_data = response.selector.re_first(pattern)
        size_data = json.loads(size_data)
        for data in size_data.get("attributes").get("187").get("options"):
            size.append(data.get("label"))

        item_data = {
            "project_name": self.project_name,
            "PageUrl": response.url,
            "html_url": response.url,
            "category_name": response.meta.get("category_name"),
            "sku": sku,
            "color": response.meta.get("color"),
            "size": size,
            "img": images,
            "price": price,
            "title": title,
            "dade": datetime.now(),
            "basc": description,
            "brand": ""
        }

        yield ProductDetailItem(**item_data)
