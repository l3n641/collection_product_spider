import scrapy
from ..common_indirect_spider import CommonIndirectSpider
from .. import ProductUrlItem, ProductDetailItem
from datetime import datetime
from lxml import etree
import requests
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode
from selenium.webdriver.common.by import By
from .. import ChromeBrowser
import re


class WethenewSpider(CommonIndirectSpider):
    name = 'wethenew'
    allowed_domains = ['wethenew.com']
    base_url = 'https://en.wethenew.com/'

    custom_settings = {
        "HTTPERROR_ALLOWED_CODES": [403]
    }

    @staticmethod
    def get_product_url(driver):
        urls = []
        elements = driver.find_elements(By.XPATH, '//a[@class="boost-pfs-filter-product-item-image-link"]')
        for element in elements:
            url = element.get_attribute("href")
            urls.append(url)
        return urls

    def start_requests(self):
        if self.action == 1:
            yield scrapy.Request(self.base_url, callback=self.parse_product_list, )
        else:
            yield scrapy.Request(self.base_url, callback=self.parse_product_detail, )

    def parse_product_list(self, response):
        urls = self.get_start_urls()
        for item in urls:
            product_urls = self.get_product_urls_by_category_url(item.get("url"))
            for url in product_urls:
                item_data = {
                    "category_name": self.product_category.get(item.get("url")),
                    "url": url,
                    "referer": item.get("url")
                }
                yield ProductUrlItem(**item_data)

    def get_product_urls_by_category_url(self, url):
        driver = ChromeBrowser("F:\code\collection_product_spider\chromedriver.exe")
        driver.get(url)
        urls = self.get_product_url(driver)
        next_page_xpath = '//div [contains(@class,"boost-pfs-filter-bottom-pagination")]/ul/li[last()]/a'
        while element := driver.get_element_by_xpath(next_page_xpath):
            next_url = element.get_attribute("href")
            if next_url:
                driver.click_by_script(next_page_xpath)
                result = self.get_product_url(driver)
                if result:
                    urls = urls + result

        driver.quit()
        return urls

    def get_product_detail(self, url):
        title_xpath = '//*[@id="title"]'
        price_xpath = '//span[@itemprop="price"]'
        size_xpath = '//select[@class="single-option-selector"]/option'
        img_xpath = '//a[@rel="product-lightbox"]'
        description_xpath = '//meta[@name="twitter:description"]'
        data_pattern = 'currency : "EUR", sku : "(.*?)", brand : "(.*?)", variant'

        driver = ChromeBrowser("F:\code\collection_product_spider\chromedriver.exe")
        driver.get(url)
        result = re.search(data_pattern, driver.page_source)
        sku = result.group(1)
        brand = result.group(2)
        price = driver.get_element_by_xpath(price_xpath).text
        title = driver.get_element_by_xpath(title_xpath).text
        description = driver.get_element_by_xpath(description_xpath).get_attribute("content")

        sizes = []
        images = []
        image_elements = driver.find_elements(By.XPATH, img_xpath)
        for element in image_elements:
            href = element.get_attribute("href")
            images.append(href)

        size_elements = driver.find_elements(By.XPATH, size_xpath)
        for element in size_elements:
            size = element.text
            sizes.append(size)

        item_data = {
            "PageUrl": url,
            "html_url": url,
            "sku": sku,
            "color": "",
            "size": sizes,
            "img": images,
            "price": price,
            "title": title,
            "dade": datetime.now(),
            "basc": description,
            "brand": brand
        }
        return item_data

    def parse_product_detail(self, response):
        data = self.get_failed_detail_urls()
        for item in data:
            result = self.get_product_detail(item.url)
            request_data = self.get_product_detail_request_args(item)
            yield scrapy.Request(**request_data)
