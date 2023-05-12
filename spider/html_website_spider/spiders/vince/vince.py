import json
import scrapy
from .. import ProductUrlItem, ProductDetailItem
import re
from datetime import datetime
from ..common_spider import CommonSpider
import json
from urllib.parse import urlparse, parse_qsl
from urllib.parse import urlencode
import html
import requests
import hashlib
from html import unescape


class VinceSpider(CommonSpider):
    name = 'vince'
    allowed_domains = ['www.vince.com']
    BASE_URL = "https://www.vince.com"

    custom_settings = {
        'COOKIES_ENABLED': False,
    }

    default_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
        "cookie": 'sid=R6gwYKCWSeHOOcFYbU3g3e_-I0jSo43v_Bs; dwanonymous_6471ffc488c3485972efd6bd8948c6b5=abzvHPPW7B1hxwGYbFVBELLrIf; __cq_dnt=0; dw_dnt=0; dwac_8aa9e59769adb2bb9dde9e3939=R6gwYKCWSeHOOcFYbU3g3e_-I0jSo43v_Bs%3D|dw-only|||USD|false|America%2FNew%5FYork|true; cquid=||; dwsid=nN7rXHLT9oQ6crCx8H-l0jSI-HQA5jKKCFDH-STXRwxsqShkXoExd8CqT11OJEJ_7GEFnw_OU3FpM6_bVz53vA==; AMCVS_69AE1DAC6269ADEC0A495CFA%40AdobeOrg=1; inflow_remove_checkout_g_3887=control; GlobalE_CT_Data=%7B%22CUID%22%3A%22729916056.195483403.400%22%2C%22CHKCUID%22%3Anull%7D; GlobalE_Ref=https%3A//www.google.com/; ltkSubscriber-FooterSFRA=eyJsdGtDaGFubmVsIjoiZW1haWwiLCJsdGtUcmlnZ2VyIjoibG9hZCIsImx0a0VtYWlsIjoiIn0%3D; s_cc=true; cqcid=abzvHPPW7B1hxwGYbFVBELLrIf; GlobalE_Welcome_Data=%7B%22showWelcome%22%3Afalse%7D; GlobalE_Full_Redirect=false; OptanonAlertBoxClosed=2023-01-05T08:52:27.697Z; _fbp=fb.1.1672908747744.499414432; _gcl_au=1.1.868599278.1672908748; tpc_a=cbb3a5e3ac4d434b9631566e6560e284.1672908747.2sd.1672908747; __attentive_id=324cfd37a44643dcaa0c95fdeb3f4611; _attn_=eyJ1Ijoie1wiY29cIjoxNjcyOTA4NzQ3OTMwLFwidW9cIjoxNjcyOTA4NzQ3OTMwLFwibWFcIjoyMTkwMCxcImluXCI6ZmFsc2UsXCJ2YWxcIjpcIjMyNGNmZDM3YTQ0NjQzZGNhYTBjOTVmZGViM2Y0NjExXCJ9In0=; __attentive_cco=1672908747933; __attentive_ss_referrer=https://www.google.com/; _hjFirstSeen=1; _hjSession_827823=eyJpZCI6ImUyODYwYjUyLWJiNTctNGQ0OC04ZDUwLTU2MjMwMWE2MGQ1ZSIsImNyZWF0ZWQiOjE2NzI5MDg3NDgyMjEsImluU2FtcGxlIjp0cnVlfQ==; _hjAbsoluteSessionInProgress=1; __attentive_dv=1; _hjSessionUser_827823=eyJpZCI6ImU3YThmMzViLWEyYjMtNWVmNS1iOTgwLTk3MWMzMzIzMjczZCIsImNyZWF0ZWQiOjE2NzI5MDg3NDc4MzEsImV4aXN0aW5nIjp0cnVlfQ==; gpv_Page=Vince%7CStriped%20Relaxed%20Elbow%20Sleeve%20T-Shirt%20in%20Short%20Sleeve%20%7C%20Vince; ltkpopup-session-depth=2-1; GlobalE_Data=%7B%22countryISO%22%3A%22US%22%2C%22cultureCode%22%3A%22en-US%22%2C%22currencyCode%22%3A%22USD%22%2C%22apiVersion%22%3A%222.1.4%22%7D; amp_f24a38=QClzBmIWizia8ANvwnhZRB...1gm0i3aeu.1gm0ilt7k.0.0.0; forterToken=5d03cd6c9ace4945843150c378c45632_1672909354395_250_UAL9_9ck; _uetsid=4808daa08cd611edb348d7a880801bc4; _uetvid=480919508cd611edbe89bbe9315123e9; __attentive_pv=8; s_sq=%5B%5BB%5D%5D; AMCV_69AE1DAC6269ADEC0A495CFA%40AdobeOrg=179643557%7CMCIDTS%7C19363%7CMCMID%7C51944732660739040240845904014591653664%7CMCOPTOUT-1672917380s%7CNONE%7CvVersion%7C5.5.0'
    }

    def parse_product_list2(self, response):
        product_info_xpath = '//button[@class="color-swatch base-swatch  "]'
        next_page_xpath = '//div[@class="show-more"]//button'
        product_info = response.xpath(product_info_xpath)

        for item in product_info:
            detail_url = self.BASE_URL + item.attrib.get("data-url")

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

        next_page_url = response.xpath(next_page_xpath).attrib.get("data-url")
        if next_page_url:
            yield scrapy.Request(next_page_url, meta=response.meta, callback=self.parse_product_list)

    def parse_product_list(self, response, **kwargs):
        product_url_xpath = '//div[@data-pid]'
        next_page_xpath = '//div[@class="show-more"]//button'
        product_info = response.xpath(product_url_xpath)

        for item in product_info:
            product_id = item.attrib.get('data-pid')
            for color_node in item.xpath('div//button[@class="color-swatch base-swatch  "]'):
                color_id = color_node.attrib.get('aria-describedby')
                color_key = f"dwvar_{product_id}_color"
                query = {
                    color_key: color_id,
                    "pid": product_id,
                    "quantity": 1,
                }
                params = urlencode(query)
                detail_url = 'https://www.vince.com/on/demandware.store/Sites-vince-Site/default/Product-Variation?' + params

                item_data = {
                    "category_name": response.meta.get("category_name"),
                    "detail_url": detail_url,
                    "referer": response.meta.get("referer"),
                    "page_url": response.url,
                    "meta": response.meta,
                    "callback": self.parse_product_detail,
                    "headers": self.default_headers,
                }

                for task in self.request_product_detail(**item_data):
                    yield task

        next_page_url = response.xpath(next_page_xpath).attrib.get("data-url")
        if next_page_url:
            yield scrapy.Request(next_page_url, meta=response.meta, callback=self.parse_product_list)

    def parse_product_detail(self, response):
        data = response.json()
        product_data = data.get("product")
        images_data = product_data.get("images").get("1380x1920")
        sizes = []
        color = ""
        price = product_data.get("price").get("sales").get("decimalPrice")

        for item in product_data.get("variationAttributes"):
            if item.get("id") == "color":
                color = item.get("displayValue")

            if item.get("id") == "size":
                for size in item.get("values"):
                    sizes.append(size.get("value"))

        images = [data.get("url") for data in images_data]

        sku = product_data.get("id") + "_" + color.replace(" ", "_")
        html_url = self.BASE_URL + product_data.get("selectedProductUrl")
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
            "title": product_data.get("productName"),
            "dade": datetime.now(),
            "basc": product_data.get("shortDescription"),
            "brand": product_data.get("brand")
        }

        yield ProductDetailItem(**item_data)
