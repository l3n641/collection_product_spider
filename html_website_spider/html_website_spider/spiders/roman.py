import scrapy
from scrapy.utils.response import get_base_url
from urllib.parse import urljoin
from ..items import ProductUrlItem


class RomanSpider(scrapy.Spider):
    name = 'roman'
    allowed_domains = ['www.roman.co.uk']

    def start_requests(self):

        for request in self.get_product_category():
            yield request

    def get_product_category(self):
        category_urls = [
            "https://www.roman.co.uk/"
        ]

        for url in category_urls:
            yield scrapy.Request(url, callback=self.parse_product_category)

    def parse_product_category(self, response, **kwargs):
        base_url = get_base_url(response)
        category_menu_xpath = '//*[@id="menu2"]/ul/li[4]'
        menu = response.xpath(category_menu_xpath)
        sub_menus = menu.xpath("div/div/div/div[1]/ul/li/a")
        urls = []
        for selector in sub_menus:
            urls.append({"category_name": selector.root.text, 'url': selector.attrib.get("href")})

        for data in urls:
            url = urljoin(base_url, data.get("url"))
            meta = {
                "category_name": data.get("category_name")
            }
            yield scrapy.Request(url, callback=self.parse_product_list, meta=meta)

    def parse_product_list(self, response, **kwargs):
        product_detail_url_xpath = '//div[@class="associated-product__colours"]/a'
        selector_list = response.xpath(product_detail_url_xpath)
        base_url = get_base_url(response)

        for request in self.get_next_product_list_page(response):
            if request:
                yield request

        for selector in selector_list:
            url = urljoin(base_url, selector.attrib.get('href'))
            item_data = {
                "category_name": response.meta.get("category_name"),
                "url": url,
                "referer": response.url,
            }
            yield ProductUrlItem(**item_data)

    def get_next_product_list_page(self, response):
        xpath = '//a[@ aria-label="Next Page"]'
        next_page_uri = response.xpath(xpath).attrib.get("href")
        if next_page_uri:
            base_url = get_base_url(response)
            url = urljoin(base_url, next_page_uri)
            yield scrapy.Request(url, callback=self.parse_product_list, meta=response.meta)
        else:
            yield None
