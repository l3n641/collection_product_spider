import json
import scrapy
from .. import ProductUrlItem, ProductDetailItem
import re
from datetime import datetime
from ..common_spider import CommonSpider
import json
from urllib.parse import urlparse
from html import unescape
from scrapy.http import FormRequest


class Spider(CommonSpider):
    name = 'blundstone'
    allowed_domains = ['www.blundstone.com']
    BASE_URL = "https://www.blundstone.com"


    def parse_product_list(self, response):
        category_data_xpath = '//div[@data-sc-filter-scope-node]'
        initialize_context_pattern = 'CoveoForSitecoreUserContext.handler.initializeContext\((.*?)\);'
        category_data = response.xpath(category_data_xpath)