import scrapy
from ..common_spider import CommonSpider
from .. import ProductUrlItem, ProductDetailItem
import json
from datetime import datetime


class LegoSpider(CommonSpider):
    name = 'lego'
    allowed_domains = ['lego.com']
    base_url = 'https://www.lego.com'

    def parse_product_list(self, response):
        link_xpath = '//a[@data-test="product-leaf-title-link"]'
        next_page_xpath = '//a[@data-test="pagination-next"]/@href'

        if next_page_uri := response.xpath(next_page_xpath).get():
            next_page_url = self.base_url + next_page_uri
            yield scrapy.Request(next_page_url, meta=response.meta, callback=self.parse_product_list)

        links = []
        for link in response.xpath(link_xpath):
            links.append(link.attrib.get("href"))
            request_url = self.base_url + link.attrib.get("href")
            item_data = {
                "category_name": response.meta.get("category_name"),
                "referer": response.meta.get("referer"),
                "url": request_url,
            }
            yield ProductUrlItem(**item_data)
            yield scrapy.Request(request_url, meta=response.meta, callback=self.parse_product_detail)

    def parse_product_detail(self, response):
        json_data_xpath = '//script[@id="__NEXT_DATA__"]'
        data_str = response.xpath(json_data_xpath)[0].root.text
        data_json = json.loads(data_str)
        page_prop = data_json.get("props").get("pageProps")
        query = data_json.get("query")
        apollo_state = page_prop.get("__APOLLO_STATE__")
        product_key = 'product({"slug":"' + query.get('product') + '"})'
        product_id = apollo_state.get('ROOT_QUERY').get(product_key).get("id")
        product = apollo_state.get(product_id)
        variant_id = product.get('variant').get("id")
        price = apollo_state.get(f"${variant_id}.price").get('formattedValue')
        image_key = f'${product_id}.productMedia'
        images = []

        for item in apollo_state.get(image_key).get("items"):
            img_id = item.get("id")
            src = apollo_state.get(img_id).get('baseImgUrl')
            if src:
                src = src + '?fit=bounds&format=webply&quality=80&width=1024&height=1024&dpr=1'
                images.append(src)

        item_data = {
            "project_name": self.project_name,
            "PageUrl": response.url,
            "category_name": response.meta.get("category_name"),
            "sku": product.get('productCode'),
            "color": product.get("color"),
            "size": [],
            "img": images,
            "price": price,
            "title": product.get("name"),
            "dade": datetime.now(),
            "basc": product.get('description'),
            "brand": ""
        }
        yield ProductDetailItem(**item_data)
