import scrapy
from ..common_indirect_spider import CommonIndirectSpider
from .. import ProductUrlItem, ProductDetailItem
from datetime import datetime

from urllib.parse import urlparse
from selenium.webdriver.common.by import By
from .. import ChromeBrowser
import urllib.parse
from urllib.parse import urlencode


class SpiderFr(CommonIndirectSpider):
    name = 'ullapopken_fr'
    allowed_domains = ['www.ullapopken.fr']
    BASE_URL = "https://www.ullapopken.fr"

    def start_requests(self):
        if self.action == 1:
            yield scrapy.Request(self.BASE_URL, callback=self.selenium_start, dont_filter=True)
        else:
            data = self.get_failed_detail_urls()
            for item in data:
                request_data = self.get_product_detail_request_args(item)
                yield scrapy.Request(**request_data)

    def parse_product_detail(self, response):
        title_pattern = "'name':'(.*?)','var6'"
        sku_pattern = "'sku': '(.*?)'"
        price_pattern = "'price':(.*?),'name'"
        color_xpath = '//div[@data-selected-color]'
        size_xpath = '//button[@data-size-name]'
        image_xpath = '//div[@data-product-gallery]/img[@data-product-gallery-img]'
        desc_xpath = '//meta[@name="description"]'
        price = response.selector.re_first(price_pattern)
        sku = response.selector.re_first(sku_pattern)
        title = response.selector.re_first(title_pattern)
        color_node = response.xpath(color_xpath)

        desc = response.xpath(desc_xpath).attrib.get("content")
        color = ""
        if color_node:
            color = color_node.attrib.get("data-selected-color")

        size_list = []
        if node := response.xpath(size_xpath):
            for item in node:
                size_list.append(item.attrib.get("data-size-name"))

        images = []
        if node := response.xpath(image_xpath):
            for item in node:
                images.append(f'https:{item.attrib.get("data-src")}?imwidth=1024&impolicy=imageviewer')

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
            "basc": desc,
            "brand": ""
        }

        yield ProductDetailItem(**item_data)

    def selenium_start(self, response):
        product_category = self.product_category
        for url in product_category.keys():
            try:
                driver = ChromeBrowser("F:\code\collection_product_spider\chromedriver.exe")
                current_page = 1
                item = self.get_data_by_selenium(driver, url)

                for task in self.parses_product_list(item, product_category.get(url), url):
                    yield task

                while driver.find_elements_by_xpath(
                        '//div[@class="product__list--wrapper"]//ff-template[@scope="result"]//b'):
                    current_page = current_page + 1
                    url_info = urlparse(url)
                    query = dict(urllib.parse.parse_qsl(url_info.query))
                    query.update({
                        "page": current_page,
                    })
                    params = urlencode(query)
                    new_url = f"{url_info.scheme}://{url_info.netloc}{url_info.path}?{params}"

                    item = self.get_data_by_selenium(driver, new_url)
                    print("*" * 100, current_page)
                    if not item:
                        print("error")

                    for task in self.parses_product_list(item, product_category.get(url), url):
                        yield task
            except Exception as e:
                print('error')
            finally:
                driver.quit()

    def parses_product_list(self, items, category_name, referer_url):

        for item in items:
            html_url = item.get_attribute('href')
            log = self.get_product_log(html_url, category_name)
            if log and log.status == 1:
                continue

            item_data = {
                "category_name": category_name,
                "url": html_url,
                "referer": referer_url,
                "status": 0,
                "page_url": referer_url,
            }
            yield ProductUrlItem(**item_data)

    @staticmethod
    def get_data_by_selenium(driver, target_url):
        try:
            driver.get(target_url)
            product_list_path = "//ff-record[contains(@class,'product-item')]//a[@data-redirect]"
            if driver.wait_display(product_list_path, 20):
                item = driver.find_elements(By.XPATH, product_list_path)
                return item
            return []
        except Exception as e:
            print(e)
