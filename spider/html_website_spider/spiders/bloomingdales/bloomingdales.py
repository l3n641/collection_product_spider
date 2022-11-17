import scrapy
from ..common_spider import CommonSpider
from .. import ProductUrlItem, ProductDetailItem
from datetime import datetime

from urllib.parse import urlparse
from selenium.webdriver.common.by import By
import time
from .. import ChromeBrowser
import urllib.parse
from urllib.parse import urlencode
import requests
import json
import math
import traceback
from queue import Queue


class BloomingdalesSpider(CommonSpider):
    name = 'bloomingdales'
    allowed_domains = ['www.bloomingdales.com']
    product_list_api = "https://www.bloomingdales.com/xapi/discover/v1/page?"
    domain = "https://www.bloomingdales.com"

    custom_settings = {
        "HTTPERROR_ALLOWED_CODES": [301, 302]

    }

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
        "cookie": 'RTD=847e6ae23e0ec0847e6ae23eea80847e6ae23e24a0847e6ae23e78f0; SignedIn=0; GCs=CartItem1_92_03_87_UserName1_92_4_02_; mercury=true; akacd_RWASP-default-phased-release=3846030898~rv=93~id=00101dc3d7d6ba68c33aad710fbbe865; at_check=true; _gcl_au=1.1.1888679752.1668578101; AMCVS_8D0867C25245AE650A490D4C@AdobeOrg=1; mt.v=2.1006474163.1668578101615; fs_uid=#104H4B#6292574289285120:5878359560835072:::#/1700114101; fs_cid=1.0; _gid=GA1.2.755689425.1668578102; _bamls_usid=b6efc368-bf0b-4776-b3dc-6d991c567d12; _pin_unauth=dWlkPU5qbG1OakV5TWpndE5qQTBNUzAwWm1NMUxXSmhPV1F0TldaaFl6WmtaR05qT1RFMg; _mibhv=anon-1668578107809-7319381623_2263; shippingCountry=US; currency=USD; __gads=ID=d8ad071256f32bdb:T=1668578116:S=ALNI_Mat0P4h1anGBp9_kWr5TVlvXjZqDQ; bm_sz=A8096E3D5BC4B6E2F17DD757A0DB3799~YAAQ4GgDF7CJ9EKEAQAA5JszfxGx0Ikc0gTn3OmzD8AIi1vdm0qvshQfvcJFJvDThCy7DHOaHXSKvygIHxnwAVc+1RsjaSc8eYj8wfnIs4fshI0n9eZEzcw0EA2EIZ7ocuxOzVwfp962uQU2+ph2JQHX3rkEq3rGmpGQNicaElb3SGDGCwzaoUiRCjy1BqKnBLsXNwame7X9eQAwRZGctvF/bBl2MuhIgJTmPdXqw/ynrD3qXUOfz0rWQiHkvL1kupEMiuxpgpnpwFDhRR0hiS7X9gmurJV97iKJY9yXarz/0qS0h/YFvLUVfGJtTUfgsrKNLvClkCtiVe0xn3vFNiJ+gZ3fu1n//e2FE2w5BRbU9h6cbOkzRTtoXToGs6STubYcyr0EgQxrizVGq0Qj9Cb95w4mJFpaQ1wWpZrAB7WaxjG5etdfhrDRHcGw+A5B~3552579~4405571; _ga=GA1.2.1969634021.1668578102; OptanonConsent=isGpcEnabled=0&datestamp=Wed+Nov+16+2022+15:48:15+GMT+0800+(中国标准时间)&version=6.39.0&isIABGlobal=false&hosts=&consentId=408d0ebe-3d5c-44c5-ad66-11f6d94832e2&interactionCount=1&landingPath=NotLandingPage&groups=C0001:1,C0003:1,C0002:1,SPD_BG:1,C0005:1,C0004:1&AwaitingReconsent=false; __rutma=83436613-hd-zq-4c-1p-k8jat34wr9lo9ypsc122-1668578104136.1668580807726.1668583473308.3.19.7; __rpck=0!PTAhZXlKME55STZlMzBzSW5RM2RpSTZlMzBzSW5RNElqcDdJakVpT2pFMk5qZzFOemd4TVRVeE16WjlmUX5+; last_access_token=1668587459595; s_pers= c29=bcom%3Awomen%3Aevening%20and%20formal%20gowns|1668589259703; v30=browse|1668589259704;; bm_mi=8020868C48772094709B4D0A5F27B1A9~YAAQ4GgDF634/0KEAQAAOYmZfxGAE9TpxHr1NHRTzVjcs2HqIQyPuHqZyX3w0G9Eveti5ofRgiXWFsRNlKuG5n/oM77TVBj50PDSzSPHnpNnh0j7NXWcI+zx/IgM7iZls/u6Mw58fdLc7C3nr7w0YKjpSkAv94dn87/pCY7Tsu6FPgXynPS3yqqdSnUuMnoLI7ZQ2dqu98DZrtu/15K4yyGJmipQROQTXtAh/SrT3rp1yEvpcc/NevvPqHjhzwDBiL3EkBXg5oSblPvmwk2Q1yclZxvfFd/L2nFkjxU4zLT5PoIQhLd3beMCMLry1BiulEFEBFEt8DYddvP/grg=~1; ak_bmsc=74482D0B9085849133832F8589E1DDAE~000000000000000000000000000000~YAAQ4GgDFyj6/0KEAQAAppeZfxFOpT9L6BtzDGbqp6Enwz0VisFeDfJ/oIHr7ivz7xqaDn5oY/S5drCu59uy239i7aPOFkQGVmQRuKpZZMr1q/0tTHckgM6T1FD7l9eYp0ceCRiidPnsU100mMytgDeNl/OLmZVDL0kmg8N1YC+kmrw4l0832Vf+1uZAIiXh9tnibYECwyDdovolwoRZxDFC+ECabUB2W1q1K7PIaY+2JXYp2xBs7dN0oaSdAA1H062FjVhCw237iMg9wa6do1Ymg+TT5c3WulD11m9vyrqWtb8GSfNfZS75GZ4JE2T9aNxMAKZYc9vUCx4Rp2+bKWFpVTQBX//BkbH7KH1br7TpIsoPPbe3GC9yEUcQsxNx1HOGTcMDCZbs24iMZl06qM0ZWa9uf+gvGkW0agbJ+AUPA9yI85iYCa3C4d5BKA==; SEED=8136233008971256301|822-21|612-21,665-25,681-21,699-21,857-21,885-21,887-21; akavpau_www_www1_bcom=1668588409~id=e9ff3404daac621bb928d84f0f67aa9a; _ga_GPE5H9XF96=GS1.1.1668587433.3.1.1668588109.60.0.0; FORWARDPAGE_KEY=https://www.bloomingdales.com/shop/womens-apparel/formal-dresses-evening-gowns/Pageindex/3?id=1005210; s_sess= s_cc=true; s_ppvl=bcom%253Awomen%253Aevening%2520and%2520formal%2520gowns%2C3%2C3%2C403%2C1919%2C203%2C1920%2C1080%2C1%2CP; s_ppv=bcom%253Ahome%2520page%2C17%2C17%2C937%2C1920%2C937%2C1920%2C1080%2C1%2CP;; __rpckx=0!eyJ0NyI6eyIyIjoxNjY4NTc4MTE2MzA0fSwidDd2Ijp7IjIiOjE2Njg1ODg1NTcwNzF9fQ~~; _abck=8205EB75DBACE07188B86369AAD6C88E~-1~YAAQ4GgDFybgAEOEAQAAc9ugfwjV1XWFebPFkTe+jXZBQZUfgzMd2GwqaZngYsDAJLy6gx/M4ajZyZKcYy/i4vUmv8WlqCPCJyvpTsxwMxrPtay3KhfzzpDxwtsiN7ZQrM+8usiOTFKqR8nzrasGdDlhDMwv2MgMtpm+lNXFVfZ3Cn7UMfYnhhqurHAcjVY/x8iUqxYu9c4aczZJohkMalGT12YSwhqZHJB03g7ojIec751xtUGL+p7GazKNx832QCwpxxxNqomfjLlwQFzhSGPa0v0z/1kEDGr2+Mgp+FRqMmA1ebucckODWiSvLTBvy5NurIQwxDlhrY8Miq1IAAyZe4il8qpMO84pARQMAZctUK+U5NrfNNHdXoE8oubly25YHO3+PzHysY2bv/4vYOigWVhNf/icNANVV+mSla/RxWRpJCwcV8fSOrHdlFNP1OmxzD6IDSwMuc04UKLoANr0Z90+kFgYPyo=~-1~-1~-1; bm_sv=9563491DE0B5808F14E34AD4D2DD385B~YAAQ4GgDFyfgAEOEAQAAc9ugfxG4UvfuRBRWTBCFocfo8xgFEwBOBhipxh8xCN0tZbJlXCJnRSf76M7+bHAzJyB3s/sQnZV+PcS8M4oZnR/Lc48JKOhJr+HXyiyrBlr4P/9idrXm0YP8WsDPqz05Fi0qA3F4d/jsa6pBanQCCMPZM0LVoQFNBafsbLX31pm6ZRgcAy7KjGeydrjaM2NmwZgCxru+GKku4q1uwGUmIYAatTXmpCt3kaDBzw47h2SuUYyQFXTtqcM=~1'

    }

    def start_requests(self):
        yield scrapy.Request(self.domain, callback=self.selenium_start, dont_filter=True)

    @staticmethod
    def get_data_by_selenium(driver, target_url):
        try:
            driver.get(target_url)
            prefix = '<html><head><meta name="color-scheme" content="light dark"></head><body><pre style="word-wrap: break-word; white-space: pre-wrap;">'
            suffix = "</pre></body></html>"
            json_str = driver.page_source.replace(prefix, '').replace(suffix, '')

            json_data = json.loads(json_str)
            return json_data
        except Exception as e:
            print(e)

    def get_target_url(self, url, page):
        url_info = urlparse(url)
        query = dict(urllib.parse.parse_qsl(url_info.query))
        params = {
            "pathname": url_info.path,
            "id": query.get("id"),
            "_application": "SITE",
            "_navigationType": "BROWSE",
            "_deviceType": "DESKTOP",
            "_shoppingMode": "SITE",
            "_regionCode": "US",
            "_customerExperiment": "612-21,665-21,681-21,699-21,857-21,885-21,887-21",
            "currencyCode": "USD",
            "_customerState": "GUEST",
            "pageIndex": page,
            "productsPerPage": "60",
            "sortBy": "ORIGINAL",
            "visitorId": "17562877338869328840254111054046382263",
            "sessionId": "01847f0145db000a2b2ec04aea520506f004b06700bd0",
            "applyPref": "false",
            "productsOnly": "true",
        }

        target_url = self.product_list_api + self.http_build_query(params)
        return target_url

    def selenium_start(self, response):
        product_category = self.product_category

        for url in product_category.keys():
            driver = ChromeBrowser("F:\code\collection_product_spider\chromedriver.exe")
            current_page = 1
            target_url = self.get_target_url(url, current_page)
            json_data = self.get_data_by_selenium(driver, target_url)

            for item in self.parse_data(json_data, product_category.get(url), url):
                yield item

            count = json_data.get("meta").get("analytics").get("coremetrics").get("searchResults")
            total_page = math.ceil(int(count) / 60)
            while current_page < total_page:
                current_page = current_page + 1
                target_url = self.get_target_url(url, current_page)
                json_data = self.get_data_by_selenium(driver, target_url)
                if not json_data:
                    print("error")
                for item in self.parse_data(json_data, product_category.get(url), url):
                    yield item

            driver.quit()

    def parse_data(self, json_data, category_name, referer_url):

        rows = json_data.get("body").get("canvas").get("rows")
        for row in rows:
            if row.get("rowSortableGrid"):
                try:
                    collection = row.get("rowSortableGrid").get("zones")[1].get("sortableGrid").get("collection")
                except Exception as e:
                    print(e)
                    continue

                if not collection:
                    continue

                for item in collection:
                    try:
                        product = item.get("product")
                        if not product:
                            continue
                        detail = product.get("detail")
                        price = product.get("pricing").get("price").get("tieredPrice")[0].get("values")[0].get('value')
                        html_url = self.domain + product.get("identifier").get("productUrl")
                        product_id = product.get("identifier").get("productId")
                        size_map = product.get("traits").get("sizes").get("sizeMap")
                        selected_color = product.get("traits").get("colors").get("selectedColor")
                        color_map = product.get("traits").get("colors").get("colorMap") or [selected_color]

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

                        size_list = []
                        for size in size_map:
                            size_list.append(size.get("displayName"))
                        description = "<br>".join(detail.get("bulletText"))
                        title = detail.get("name")
                        brand = detail.get("brand")
                        image_args = "op_sharpen=1&wid=1200&fit=fit,1&$filtersm$&fmt=jpg"

                        for color in color_map:
                            images = []
                            sku = f"{product_id}_{color.get('id')}"
                            imagery = color.get("imagery")
                            url_template = imagery.get("urlTemplate")
                            additional_image_source = imagery.get("additionalImageSource")
                            for image in additional_image_source:
                                image_url = url_template.replace("[IMAGEFILEPATH]", image.get("filePath")).replace(
                                    "$2014_BROWSE_FASHION$", image_args)

                                images.append(image_url)

                            item_data = {
                                "project_name": self.project_name,
                                "PageUrl": html_url,
                                "html_url": html_url,
                                "category_name": category_name,
                                "sku": sku,
                                "color": color.get('name'),
                                "size": size_list,
                                "img": images,
                                "price": price,
                                "title": title,
                                "dade": datetime.now(),
                                "basc": description,
                                "brand": brand
                            }
                            if item_data:
                                yield ProductDetailItem(**item_data)
                    except Exception as e:
                        print(e)

    @staticmethod
    def http_build_query(params):
        target_uri = ""
        for k, v in params.items():
            target_uri = target_uri + f"{k}={v}&"

        return target_uri.strip("&")
