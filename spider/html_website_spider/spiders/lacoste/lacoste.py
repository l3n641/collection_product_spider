import html
import json
import scrapy
from .. import ProductUrlItem, ProductDetailItem
import re
from datetime import datetime
from ..common_spider import CommonSpider
from ..common_indirect_spider import CommonIndirectSpider
from urllib.parse import urlencode
import json
from urllib.parse import urlparse, parse_qsl


class LacosteSpider(CommonIndirectSpider):
    name = 'lacoste'
    allowed_domains = ['www.lacoste.com']
    BASE_URL = "https://www.lacoste.com"
    product_detail_api = 'https://www.lacoste.com/on/demandware.store/Sites-FlagShip-Site/en_US/Product-PartialsData'

    def parse_product_list(self, response):
        product_links_xpath = '//div[@class="fs--small l-vmargin--small"]/a'
        page_xpath = '//div[@class="js-plp-num-results fs--medium l-vmargin--medium padding-m-1"]'
        page_info = response.xpath(page_xpath)
        current_page = int(page_info.attrib.get("data-current-page"))
        total_page = int(page_info.attrib.get("data-nb-pages"))
        data = response.xpath(product_links_xpath)

        for item in data:
            link = item.attrib.get("href")
            link = self.get_api_url(link)
            yield scrapy.Request(link, meta=response.meta, callback=self.parse_product_list2, dont_filter=True)

        if current_page < total_page:
            url_info = urlparse(response.url)
            next_page = current_page + 1
            query = dict(parse_qsl(url_info.query))
            query['page'] = next_page
            params = urlencode(query)
            next_url = f"https://{url_info.hostname}{url_info.path}?{params}"
            yield scrapy.Request(next_url, meta=response.meta, callback=self.parse_product_list, dont_filter=True)

    def parse_product_list2(self, response):
        data = response.json()
        product_data = data.get("product")
        variations = product_data.get("variations")

        if not variations or not variations.get("color"):
            item_data = {
                "category_name": response.meta.get("category_name"),
                "detail_url": response.url,
                "referer": response.meta.get("referer"),
                "page_url": response.url,
            }

            for task in self.add_product_detail_url(**item_data):
                yield task

        else:
            for color in variations.get("color").get("list"):

                url = self.BASE_URL + f"{color.get('partialsUrl')}"
                item_data = {
                    "category_name": response.meta.get("category_name"),
                    "detail_url": url,
                    "referer": response.meta.get("referer"),
                    "page_url": response.url,
                }
                for task in self.add_product_detail_url(**item_data):
                    yield task

    def parse_product_detail(self, response):
        data = response.json()
        product_data = data.get("product")
        spu = product_data.get("id")
        color_data = product_data.get("color")
        color_id = color_data.get("id")
        color = color_data.get("label")
        html_url = color_data.get("url")
        sku = f"{spu}_{color_id}"
        variations = product_data.get("variations")

        size_list = []
        size_data = variations.get("size")
        if size_data and (size_item := size_data.get("list")):
            for size in size_item:
                size_list.append(size.get("label"))

        images = []
        gallery = product_data.get("gallery").get("images")
        image_arg = '?imwidth=1440&impolicy=product'
        for img in gallery:
            img_url = f"https:{img.get('desktopUrl')}{image_arg}"
            images.append(img_url)

        pricing = product_data.get('pricing')
        price = pricing.get("salesPrice").get("value")

        title = product_data.get("name")
        description_data = product_data.get("description")
        if description_data.get("blocks"):
            description = ""
            for item in description_data.get("blocks"):
                if item.get('texts'):
                    for text in item.get('texts'):
                        description = description + f"{text} <br>"
        else:
            description = description_data.get("description")

        item_data = {
            "project_name": self.project_name,
            "PageUrl": response.url,
            "html_url": html_url,
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


    def get_api_url(self, url):
        url_info = urlparse(url)
        pid = url_info.path.split("/")[-1].split(".")[0]
        api_url = f"{self.product_detail_api}?pid={pid}&full=true&format=json"
        return api_url
