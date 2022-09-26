import scrapy
from ..common_spider import CommonSpider
from .. import ProductUrlItem, ProductDetailItem
from datetime import datetime

from urllib.parse import urlparse
from selenium.webdriver.common.by import By
import time
from .. import ChromeBrowser


class AeSpider(CommonSpider):
    name = 'ae'
    allowed_domains = ['ae.com']
    access_token = "eyJ0eXAiOiJKV1QiLCJjdHkiOiJKV1QiLCJhbGciOiJFQ0RILUVTK0EyNTZLVyIsImVuYyI6IkExMjhDQkMtSFMyNTYiLCJrZXkiOiJLRVkxIiwiZXBrIjp7Imt0eSI6IkVDIiwieCI6IkJaOHVqdlJHSWpXelJ3M1FTeEJoeHowUmF0bGVSVXhxRFFsZ19Eem9ZdFUiLCJ5IjoiVjF1N3ZYdVhRZUNFamdaQUJvWXRtMWJrQ3RDNWFLemtQTDFzVk5XU3lqNCIsImNydiI6IlAtMjU2In19.Ij8tEvl5tU5ry8c--TyXQiUwB9djEcsp3fR1WV2DUafkn5ZabcJG9Q.w53U7EAHbH4VYj8Hg3iEzA.5ndP72IclmaML11eL53rSai53btUKz6U_n1UHo3FaItKWJC1oJr1sA-KD3Gqw7g4nwdEk4q3wxZfWU4DeXpRk6RwGYjDR3M38BbS3lH6W7uHuApEFVav4oEzpDQ09K9cPQB6N4eWN40anIdHNqZkqCZwhR3kefz-DvMW__IWPC4rEmF-JC0ND9XyH9hLAcfdYjt_vmIwoQC2aXKM7ro0hW4D7wRR9tjuEHXE7iyu3DmM5hHaIsmsUvLuYaVSsYf4QdUJqFQIaHKjjZQzvHZ8RRSBAMWmZmcsDHkJqe0EBrJyGZ98i2_NvSB0f1ueJ7lWk0tP1ptCexGVtgjaDq3bh3-fuPLh9lajJQaVswi43AxlEvMPo8IEqCLGxYCVPuwMJSDgXPealHMMNHAKRVPQEyPNmrlRumGy3Bg2GoWp6gHnkt8oJyuwKYWBpNoDIkGMIp2_TRxWyoD7o3zDsZGkI9ju42yZd4LF-NZuvoogTqdHVKptniF_AwveBy0akRj1BioO0uRYMifI9v3TOwZlBaPYzgAlaDE9BXzA8t_4zjD0kR-EZZVzYj18zzzHUO-O1mXzTfP6QKa_fRk8IgcpY9g-onHB_KCActunzFvki1X9sEEAYSdzZqF5OBNidLUpS7mPGvw7iNrojnK143GhJonwgBL4GbEDBIktLZKilAAh_vrSlanMLiWFEodADVPU.U_sLg9UJeFzgVwj25XVQmw"
    base_url = "https://www.ae.com/us/en"

    @staticmethod
    def get_product_id(url):
        result = urlparse(url)
        _id = result.path.split("/")[-1]
        return _id

    @staticmethod
    def get_product_url(driver):
        urls = []
        elements = driver.find_elements(By.XPATH, '//div[@class="tile-media"]/a[@href!="#"]')
        for element in elements:
            url = element.get_attribute("href")
            urls.append(url)
        return urls

    @staticmethod
    def scroll_browser(driver, setup=1000, time_sleep=2):
        next_position = 2000

        while next_position < 30000:
            driver.execute_script(f"window.scrollTo(0,{next_position});")
            next_position = next_position + setup
            time.sleep(time_sleep)

    def start_with_selenium(self, url):

        driver = ChromeBrowser("F:\code\collection_product_spider\chromedriver.exe")
        driver.get(url)
        self.scroll_browser(driver)
        urls = self.get_product_url(driver)
        driver.quit()
        return urls

    def start_by_product_category(self):
        """
        从产品分类里爬取数据
        :return:
        """

        product_category = self.product_category
        for referer_url in product_category.keys():
            meta = {
                "category_name": product_category.get(referer_url),
                "referer": referer_url,
            }
            yield scrapy.Request(referer_url, meta=meta, callback=self.parse_product_list,
                                 errback=self.start_request_error, dont_filter=True)

    def parse_product_list(self, response, **kwargs):
        detail_urls = self.start_with_selenium(response.url)
        for detail_url in detail_urls:
            product_id = self.get_product_id(detail_url)
            detail_api_url = f"https://www.ae.com/ugp-api/catalog/v1/product/{product_id}"
            headers = {
                "requestedurl": "pdp",
                "aelang": "en_US",
                "aesite": "AEO_US",
                "x-access-token": self.access_token
            }
            item_data = {
                "category_name": response.meta.get("category_name"),
                "detail_url": detail_api_url,
                "referer": response.meta.get("referer"),
                "page_url": detail_url,
                "meta": response.meta,
                "headers": headers,
                "callback": self.parse_product_detail,
            }

            for task in self.request_product_detail(**item_data):
                yield task

    def start_by_product_category2(self):
        """
        从产品分类里爬取数据
        :return:
        """

        product_category = self.product_category
        for url in product_category.keys():
            result = urlparse(url)
            category_id = result.path.split("/")[-1]
            api_url = f"https://www.ae.com/ugp-api/catalog/v1/category/{category_id}"
            headers = {
                "x-access-token": self.access_token,
                #  'user-agent': self.settings.attributes.get("USER_AGENT").value,
                "requestedurl": "plp",
                "aesite": "AEO_US",
                "aelang": "en_US",
            }
            meta = {
                "category_name": product_category.get(url),
                "referer": url,
                "category_id": category_id
            }
            # data = requests.get(api_url, headers=headers)
            yield scrapy.Request(api_url, meta=meta, callback=self.parse_product_list, headers=headers,
                                 errback=self.start_request_error, dont_filter=True)

    def parse_product_list2(self, response, **kwargs):
        product_content = response.json().get("data").get('contents')[0].get('productContent')[0]
        records = product_content.get("records")
        for record in records:
            if not record.get("attributes").get("product_repositoryId"):
                continue
            product_id = record.get("attributes").get("product_repositoryId")[0]
            detail_url = f"https://www.ae.com/ugp-api/catalog/v1/product/{product_id}"
            headers = {
                "requestedurl": "pdp",
                "aelang": "en_US",
                "aesite": "AEO_US",
                "x-access-token": self.access_token
            }
            item_data = {
                "category_name": response.meta.get("category_name"),
                "detail_url": detail_url,
                "referer": response.meta.get("referer"),
                "page_url": response.url,
                "meta": response.meta,
                "headers": headers,
                "callback": self.parse_product_detail,
            }

            for task in self.request_product_detail(**item_data):
                yield task

        last_record = product_content.get("lastRecNum")
        if last_record:
            category_id = response.meta.get("category_id")

            category_headers = {
                "x-access-token": self.access_token
            }
            api_url = f"https://www.ae.com/ugp-api/catalog/v1/category/{category_id}?No={last_record}&Nrpp=60"
            yield scrapy.Request(api_url, meta=response.meta, callback=self.parse_product_list,
                                 headers=category_headers, errback=self.start_request_error, dont_filter=True)

    def parse_product_detail(self, response):
        image_args = '?$pdp-mz-opt$&fmt=jpeg'
        data = response.json()
        content_item = data.get("data").get('contentItem')

        content = content_item.get("contents")[0]
        product_detail = content.get("productDetailContent")[0]
        record = product_detail.get("records")[0]
        attributes = record.get("attributes")
        color = attributes.get("product_colorName")[0]
        sku = attributes.get("product_repositoryId")[0]
        title = attributes.get("product_displayName")[0]
        html_url = self.base_url + record.get("detailsAction").get('recordState')
        brand = attributes.get("product_brandName")[0]
        size_records = record.get("records")
        sizes = []
        for size_record in size_records:
            sizes.append(size_record.get('attributes').get('sku_sizeDesc')[0])

        images = []

        for img in product_detail.get("pdpSortMedia").split(","):
            image_url = f"https:{img}{image_args}"
            images.append(image_url)
        price = attributes.get("maxSalePrice_AEO_INTL")[0]
        description = product_detail.get("equity").get("copySections")[0].get("longDesc")
        bullets = product_detail.get("equity").get("copySections")[0].get("bullets")
        for bullet in bullets:
            description = description + f"<p>{bullet}</p>"

        item_data = {
            "project_name": self.project_name,
            "PageUrl": response.url,
            "html_url": html_url,
            "category_name": response.meta.get("category_name"),
            "sku": sku,
            "color": color,
            "size": sizes,
            "img": images,
            "price": price,
            "title": title,
            "dade": datetime.now(),
            "basc": description,
            "brand": brand
        }

        yield ProductDetailItem(**item_data)

    def start_request_error(self, failure):

        print(f"excel 链接无效:{failure.request.url}")

        category_headers = {
            "x-access-token": self.access_token
        }

        yield scrapy.Request(failure.request.url, meta=failure.request.meta, callback=self.parse_product_list,
                             headers=category_headers, errback=self.start_request_error, dont_filter=True)
