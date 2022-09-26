import scrapy
from ..common_spider import CommonSpider
from .. import ProductUrlItem, ProductDetailItem
from datetime import datetime

from urllib.parse import urlparse
from selenium.webdriver.common.by import By
import os
from .. import ChromeBrowser


class MarmotSpider(CommonSpider):
    name = 'marmot'
    allowed_domains = ['marmot.com']
    custom_settings = {
        "HTTPERROR_ALLOWED_CODES": [403]
    }

    def __init__(self, action, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.action = int(action)

    def start_requests(self):
        if self.action == 1:
            yield scrapy.Request("https://www.marmot.com/", callback=self.parse_product_list)
        if self.action == 2:
            authorization = "Bearer eyJ2ZXIiOiIxLjAiLCJqa3UiOiJzbGFzL3Byb2QvYmZnZl9wcmQiLCJraWQiOiI2YzI4MzJlMC04YmQ1LTQzMjItYWU1YS0xOTBkMTE5MWJjNDMiLCJ0eXAiOiJqd3QiLCJjbHYiOiJKMi4zLjQiLCJhbGciOiJFUzI1NiJ9.eyJhdXQiOiJHVUlEIiwic2NwIjoic2ZjYy5zaG9wcGVyLW15YWNjb3VudC5iYXNrZXRzIHNmY2Muc2hvcHBlci1kaXNjb3Zlcnktc2VhcmNoIHNmY2Muc2hvcHBlci1teWFjY291bnQucGF5bWVudGluc3RydW1lbnRzIHNmY2Muc2hvcHBlci1jdXN0b21lcnMubG9naW4gc2ZjYy5zaG9wcGVyLW15YWNjb3VudC5vcmRlcnMgc2ZjYy5zaG9wcGVyLXByb2R1Y3RsaXN0cyBzZmNjLnNob3BwZXItcHJvbW90aW9ucyBzZmNjLnNob3BwZXIuc3RvcmVzIHNmY2Mub3JkZXJzLnJ3IHNmY2Muc2hvcHBlci1teWFjY291bnQucGF5bWVudGluc3RydW1lbnRzLnJ3IHNmY2Muc2hvcHBlci1teWFjY291bnQucHJvZHVjdGxpc3RzIHNmY2Muc2hvcHBlci1jYXRlZ29yaWVzIHNmY2Muc2hvcHBlci1teWFjY291bnQgc2ZjYy5wcm9kdWN0cy5yd3NmY2MucHJvZHVjdHM6cncgc2ZjYy5zaG9wcGVyLW15YWNjb3VudC5hZGRyZXNzZXMgc2ZjYy5zaG9wcGVyLXByb2R1Y3RzIHNmY2Muc2hvcHBlci1teWFjY291bnQucncgc2ZjYy5zaG9wcGVyLWN1c3RvbWVycy5yZWdpc3RlciBzZmNjLnNob3BwZXItYmFza2V0cy1vcmRlcnMgc2ZjYy5zaG9wcGVyLW15YWNjb3VudC5hZGRyZXNzZXMucncgc2ZjYy5zaG9wcGVyLW15YWNjb3VudC5wcm9kdWN0bGlzdHMucncgc2ZjYy5zaG9wcGVyLXByb2R1Y3Qgc2ZjYy5zaG9wcGVyLWJhc2tldHMtb3JkZXJzLnJ3IHNmY2Muc2hvcHBlci1naWZ0LWNlcnRpZmljYXRlcyBzZmNjLnNob3BwZXItcHJvZHVjdC1zZWFyY2ggc2ZjYy5zZWFyY2g6cm8iLCJzdWIiOiJjYy1zbGFzOjpiZmdmX3ByZDo6c2NpZDoyMTVkZGNjNS1hZmMwLTRmZDItYTFkOS1jMTMzMzU3NjdhZDQ6OnVzaWQ6MzBjN2I0ZDQtYmNjZC00ODVjLWFlYzYtYmJlNzYxNmVlZDM2IiwiY3R4Ijoic2xhcyIsImlzcyI6InNsYXMvcHJvZC9iZmdmX3ByZCIsImlzdCI6MSwiYXVkIjoiY29tbWVyY2VjbG91ZC9wcm9kL2JmZ2ZfcHJkIiwibmJmIjoxNjYxMzIxNjA2LCJzdHkiOiJVc2VyIiwiaXNiIjoidWlkbzpzbGFzOjp1cG46R3Vlc3Q6OnVpZG46R3Vlc3QgVXNlcjo6Z2NpZDphZWtYYUhsMGdZeGNvUndLbEh4YllZbWN0SCIsImV4cCI6MTY2MTMyMzQzNiwiaWF0IjoxNjYxMzIxNjM2LCJqdGkiOiJDMkM3MjI3ODM2MTAwLTE2NTM1MTU0NzkxOTI5NjY4NzA0ODkzNjI0MCJ9.8iG-GfBHSzUEKEqDgcRCH72YTfGE_X1teKE6cp6kuJO4XoYdOi0kZKhO3In6e4IE3Om5Sb7LEI95J-FR3HzeMA"
            headers = {
                "x-dw-client-id": "215ddcc5-afc0-4fd2-a1d9-c13335767ad4",
                "authorization": authorization
            }
            data = self.get_failed_detail_urls()
            for item in data:
                meta = {
                    "category_name": item.category_name,
                    "referer": item.referer,

                }

                yield scrapy.Request(item.url, callback=self.parse_product_detail, meta=meta,
                                     headers=headers, errback=self.start_request_error, dont_filter=True)

    def parse_product_list(self, response):
        product_category = self.product_category
        for referer_url in product_category.keys():
            category_name = product_category.get(referer_url)
            detail_urls = self.start_with_selenium(referer_url)
            for detail_url in detail_urls:
                data = self.get_product_log(detail_url, category_name)
                if data:
                    continue

                item_data = {
                    "category_name": category_name,
                    "url": detail_url,
                    "referer": referer_url,
                    "status": 0,
                    "page_url": referer_url,
                }
                yield ProductUrlItem(**item_data)

    @staticmethod
    def get_product_url(driver):
        urls = []
        elements = driver.find_elements(By.XPATH, '//a[@role="radio"]')
        for element in elements:
            url = element.get_attribute("href")
            sku, _ = os.path.basename(url).split(".")
            api_url = f"https://www.marmot.com/mobify/proxy/ocapi/s/marmot/dw/shop/v22_4/products/{sku}?expand=availability,promotions,images,variations,prices&cache_keynone"
            urls.append(api_url)
        return urls

    def start_with_selenium(self, url):

        driver = ChromeBrowser("F:\code\collection_product_spider\chromedriver.exe")
        driver.get(url)
        urls = self.get_product_url(driver)
        driver.quit()
        return urls

    def parse_product_detail(self, response):
        data = response.json()
        image_group = data.get("image_groups")[0]
        images = []
        for item in image_group.get("images"):
            url = item.get("link") + "?wid=1000&hei=1000"
            images.append(url)
        variation_attributes = data.get("variation_attributes")

        sizes = []
        for item in variation_attributes:
            if item.get("id") == "size":
                for size_data in item.get("values"):
                    sizes.append(size_data.get("name"))

        item_data = {
            "project_name": self.project_name,
            "PageUrl": response.url,
            "html_url": data.get("c_externalURL"),
            "category_name": response.meta.get("category_name"),
            "sku": data.get("id"),
            "color": data.get("c_color"),
            "size": sizes,
            "img": images,
            "price": data.get("price"),
            "title": data.get("name"),
            "dade": datetime.now(),
            "basc": data.get("long_description"),
            "brand": data.get("brand")
        }

        yield ProductDetailItem(**item_data)
