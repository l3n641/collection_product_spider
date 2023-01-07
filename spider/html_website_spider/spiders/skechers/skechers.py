import scrapy
from ..common_indirect_spider import CommonIndirectSpider
from .. import ProductUrlItem, ProductDetailItem
from datetime import datetime
from lxml import etree
import requests
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode


class SkechersSpider(CommonIndirectSpider):
    name = 'skechers'
    allowed_domains = ['skechers.com']
    base_url = 'https://www.skechers.com'

    product_list_url = 'https://www.skechers.com/on/demandware.store/Sites-USSkechers-Site/en_US/Product-Variation'

    custom_settings = {
        'AUTOTHROTTLE_ENABLED': True,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 4,
        'COOKIES_ENABLED': False,
    }

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
        "cookie": 'dwac_3a60353a3ab037178b206f9956=QcVEAsCd91bOIaW6tL-xoPq8HBCBJiBwD_E=|dw-only|||USD|false|America/Los_Angeles|true; cqcid=bgbQlK2UlwSBu5EYPzc1dHaey6; cquid=||; sid=QcVEAsCd91bOIaW6tL-xoPq8HBCBJiBwD_E; dwpersonalization_63ec983096393364be678ab69485089e=3dd1c590ad1f8fa73c32ce72b120221003070000000; dwanonymous_63ec983096393364be678ab69485089e=bgbQlK2UlwSBu5EYPzc1dHaey6; __cq_dnt=0; dw_dnt=0; dwsid=XZg0Z761wWRVFpSAJn6oOubhbHX_DhZClMase52Zci86iBD8XMH7Kt0Yg25uBGiBHu-VJrysRvA9p4E-hdPKZg==; _pxhd=NK/6CRi7Cen7YZGFiBIxHpi2BTZXpH5NcJmagaAGhuwsjxPkQUToVzzcPSrtv--diU9q-0eKtnOgUzW6vOYY0Q==:daqe2S2XVsgFfBwLqGnQMtyf2AoyY1B5C3jP-6LdkW7hqp2ziyDZU/HkclA-DgRCtWxKewhnyLg8N15SmyixlJpcJyVO6gLQe/4uIy18iPw=; __cf_bm=tYZnnoQDMgbENGawSKu_Dep9r_SNDtzBiSqy2N5tJvA-1664263700-0-AXBJNNiJlYhpZRa0/y94d/sRero1zj3/poKwAeZde/KY3Rb+NAfehBsSYD/JYrMSkPJSJnzvo5HWvDjAApXLrHo=; _px_f394gi7Fvmc43dfg_user_id=MjBkOGFiMjEtM2UzNi0xMWVkLTk3YWQtNTE0YzNkMmQ1NDEz; pxcts=214a301d-3e36-11ed-8bb5-73416d444d62; _pxvid=f5e56ddc-3e35-11ed-a8e9-4c414e794c52; __rpckx=0!eyJ0NyI6eyIxIjoxNjY0MjYzNjY1MTI4fSwidDd2Ijp7IjEiOjE2NjQyNjM3ODU0MDV9LCJpdGltZSI6IjIwMjIwOTI3LjA3MjcifQ~~'
    }

    def get_request_product_list_args(self):

        return {
            "errback": self.start_request_error,
            "dont_filter": True,
            "headers": self.headers
        }

    def parse_product_list(self, response, **kwargs):
        load_more_xpath = '//*[@id="product-grid-load-more"]'
        product_xpath = '//div[@class="product"]//div[@class="image-container c-product-tile__image-container"]/a'

        has_next = response.xpath(load_more_xpath)

        if has_next:
            start = response.meta.get("start", 0) + 24
            query = {
                "start": start,
                "sz": 24,
            }
            params = urlencode(query)
            parse = urlparse(response.url)
            new_parse = parse._replace(query=params)
            next_page = urlunparse(new_parse)
            response.meta["start"] = start
            yield scrapy.Request(next_page, meta=response.meta, callback=self.parse_product_list, headers=self.headers,
                                 errback=self.start_request_error, dont_filter=True)

        result = response.xpath(product_xpath)

        for item in result:
            href = item.attrib.get("href")
            pid = href.split("/")[-1].split(".")[0]
            query = {
                "quantity": 1,
                "resetQty": "true",
                "pid": pid,
            }
            params = urlencode(query)
            detail_url = self.product_list_url + "?" + params

            for task in self.add_product_detail_url(detail_url, response.meta.get("category_name"),
                                                    response.meta.get("referer"), response.url):
                yield task

    def parse_product_detail(self, response, ):
        data = response.json()
        product_data = data.get("product")
        variation_attributes = product_data.get("variationAttributes")
        if data.get("replacementState"):
            html_url = self.base_url + data.get("replacementState").get("args")[-1]
        else:
            html_url = self.base_url + product_data.get("selectedProductUrl")

        description = product_data.get("shortDescription")
        if not description:
            description = self.get_product_desc(html_url)
        title = product_data.get("productName")
        product_id = product_data.get('id')
        brand = product_data.get("brand")
        pdpPrice = product_data.get("pdpPrice")

        if pdpPrice.get("type") and pdpPrice.get("type") == "range":
            price = pdpPrice.get("max").get("sales").get('decimalPrice')
        else:
            price = pdpPrice.get("sales").get('decimalPrice')

        color_attr = self.get_product_variation_attributes(variation_attributes, 'colorCode')
        size_attr = self.get_product_variation_attributes(variation_attributes, 'size')
        size_list = []

        if size_attr:
            for item in size_attr.get("values"):
                size_list.append(item.get("displayValue"))

        for item in color_attr.get("values"):

            images = []
            for img in item.get("images").get("large"):
                images.append(img.get("url"))

            sku = product_id + "_" + item.get("id")

            item_data = {
                "project_name": self.project_name,
                "PageUrl": response.url,
                "html_url": html_url,
                "category_name": response.meta.get("category_name"),
                "sku": sku,
                "color": item.get("displayValue"),
                "size": size_list,
                "img": images,
                "price": price,
                "title": title,
                "dade": datetime.now(),
                "basc": description,
                "brand": brand
            }

            yield ProductDetailItem(**item_data)

    @staticmethod
    def get_product_desc(url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
        }

        xpath = '//div[@class="c-product-details__overview"]'
        response = requests.get(url, timeout=60, headers=headers)
        html = etree.HTML(response.text)
        result = html.xpath(xpath)
        if result:
            return result[0].text.strip()

        return ""

    def get_product_detail_request_args(self, item):
        """
        获取重新下载失败的详情页面的参数
        :param item:
        :return:
        """
        meta = {
            "category_name": item.category_name,
            "referer": item.referer,

        }
        item_data = {
            "url": item.url,
            "meta": meta,
            "callback": self.parse_product_detail,
            "headers": self.headers
        }
        return item_data

    def get_product_variation_attributes(self, attributes, attribute_id):
        for item in attributes:
            if item.get("attributeId") == attribute_id:
                return item
