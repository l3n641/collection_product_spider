import scrapy
from ..common_spider import CommonSpider
from .. import ProductUrlItem, ProductDetailItem
from html import unescape
from urllib.parse import urlencode
from datetime import datetime
import demjson

cookie = 'bm_sz=A2EA90610F89730EC5581D55402C83CF~YAAQ7UpDF+o4ExmFAQAAsZWXhhL/9z/r3FT6b2J7rs91isQWivyB1A5qqSC9HLr6sxpGRzumTvDqx7VL+nSwa50jOtRlUTIXDedbq+Z6UmOkiXn7kSYeVmSx5RNfnVCe3icIltXlgzVwWBwplit12GiLS9l/AL5wGarriceCDrMG6m7rdiGUst2/sISwRmGN+udh6bNKTJfARO2dUspx9UUoZI9mPFUNwEHOS28ARcACNRXiDkAOGSlUiDbtds1pEahRTwjaYN88BfmsTgEDfCaLXimbwAmESL8IqC+roEO3guXB~3425346~3621953; ak_bmsc=37226C8C1176428CB16C8FF397E71705~000000000000000000000000000000~YAAQ7UpDF/Y4ExmFAQAAqJeXhhKdvbBSjG4NisQTpn9w9mWGQeYR1XbzZoFnHfxG/gFBnCGadgCARY9EecuIrsowBgkCVIb6knG1JYNQeVfRlp5RvRbeCItAwvCKWtPf/LOKxjRMvPuk50bc7yql6NUwsCROptxjsmMmsGhg3tevZPmmrseBELpGzqzzOII0KoLr8h5kMkxDz7omCW3OSUNHNvGpCy86VQ2T+9GZ5RDGD4WG5jqCO8tkDTJ8q7jux92hYI/oVlWDh2PSAETGVjpAyA6mN0a1OKE9QtHTAjyBaSdh4iTTdIPeANFWkHpjYNFmzJTYtW0lMNAFB9VrYCI/dxL+R76yvHhg+0NkQqSB6iteHM48l2E1go32zAzBNSpZzoOHLug1OxY=; AKA_A2=A; INGRESSCOOKIE=1673000362.161.519344.56589|8d230f100938665633b3e763b919b1be; newsletter-timpestamp=1673000362990; _abck=D87916F9B6829BAEB937F72902806FE5~0~YAAQ7UpDF4E5ExmFAQAAmqiXhglfOnNut/0FQjuaH8JS04Ur70ROhiRafZlvBY5PAtHjP2V73v3oYDoJsreckGNkxg26JwhpbuWeNgco7DXXQ1o8M3qz3QoKe+PDGulcxeNDERnoFyLBQzrqMDT872wL0tYfg5TiewUPVSG4EF+IQTVl/aColzwk75ySzARM+7KYBFnj8/0NJWlw+q+fyfQ6hzt3NGy1BvBmZ/YC2IXf55Gx9cdK4x2HoYsVohm3MkaoJkEPJvFZg0Z1iDlI0yq6RMpKQjPRNEKeyK5Kyy5j4FLuKcDi4wO3/526OdcvGqMC5RC1+KYzxSVGkTuUZRXjiElzfEjsO6tnvskA9ePozRZSeAG6kGLxKQHDvDIre4Y9nkHADFrSknHGVo9MoWNV26TDKbhNoQ==~-1~||-1||~-1; HMCORP_locale=de_DE; HMCORP_currency=EUR; countryId=DE; utag_main=v_id:01858697a3d0000f048be0c2690a0506f002506700bd0$_sn:1$_se:9$_ss:0$_st:1673002193125$ses_id:1673000362962;exp-session$_pn:3;exp-session$ses_id_r:s_5598592140269827.1673000362962;exp-session$c_consent:C0001:1,C0002:0,C0003:0,C0004:0$segment:normal;exp-session$prevpage:/de_de/index.html;exp-1673003991327; OptanonConsent=isGpcEnabled=0&datestamp=Fri+Jan+06+2023+18:19:53+GMT+0800+(中国标准时间)&version=202209.2.0&isIABGlobal=false&hosts=&landingPath=NotLandingPage&groups=C0001:1,C0002:0,C0003:0,C0004:0&AwaitingReconsent=false; bm_sv=69CA1EBCAD141EA1DC4F84279C1C3BD5~YAAQ7UpDFzc8ExmFAQAAbxqYhhI4aBm2KRRCzWZI15oSCAmr6uIjTAyfnD23Jrydjp7QajcSmcTJdxPVTGU7i5coqBf3HiwZxWM7QnxAKK4G5OIyK0lzMTOMBH+Q/Izuo75aTXCHL6wjkBpzOU3BdGDYWUXvsVGXMrj3i5opyV0GOFMbvU+DjoHXIiv+vz75hFQ/+H4tJ1B3CLxGQIj7J1Cli9d5KfUIbSrWafEPTiguxsQowpLzkinQ1SIbg4kxI2I=~1; RT="z=1&dm=stories.com&si=e516a2e1-7d84-4a77-980b-00ba26a814c0&ss=lckd7uec&sl=3&tt=d28&bcn=//684d0d41.akstat.io/&ld=qva&ul=uu1"'


class StoriesSpider(CommonSpider):
    name = 'stories'
    allowed_domains = ['stories.com']
    base_url = "https://www.stories.com"

    custom_settings = {
        "CONCURRENT_REQUESTS": 4,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2,
    }

    default_headers = {
        "cookie": cookie
    }

    def start_by_product_category(self):
        """
        从产品分类里爬取数据
        :return:
        """
        product_category = self.product_category
        for url in product_category.keys():
            meta = {
                "category_name": product_category.get(url),
                "referer": url,

            }
            yield scrapy.Request(url, meta=meta, callback=self.parse_product_list, errback=self.start_request_error,
                                 dont_filter=True, headers=self.default_headers)

    def parse_product_list(self, response, **kwargs):
        product_url_xpath = '//div[@id="productPath"]'
        product_count_xpath = '//div[@id="productCount"]'
        node = response.xpath(product_url_xpath)
        count_node = response.xpath(product_count_xpath)

        product_path = self.base_url + node.attrib.get("class")
        total = int(count_node.attrib.get("class"))
        start = 0
        while start < total:
            url = product_path + f"?start={start}"
            yield scrapy.Request(url, meta=response.meta, callback=self.parse_product_list2,
                                 headers=self.default_headers,
                                 errback=self.start_request_error)
            start = start + 40

    def parse_product_list2(self, response, **kwargs):
        product_url_xpath = '//div[@ class="description"]/a'

        product_info = response.xpath(product_url_xpath)

        for item in product_info:

            detail_url = item.attrib.get("href")
            item_data = {
                "category_name": response.meta.get("category_name"),
                "detail_url": detail_url,
                "referer": response.meta.get("referer"),
                "page_url": response.url,
                "meta": response.meta,
                "headers": self.default_headers,
                "callback": self.parse_product_detail,
            }

            for task in self.request_product_detail(**item_data):
                yield task

    def parse_product_detail(self, response):
        color_id_xpath = '//div[@id="swatchDropdown"]//button[@ data-articlecode]'
        product_info_xpath = '//div[@class="product parbase"]/script/text()'
        js_str = response.xpath(product_info_xpath).get().replace("var productArticleDetails = ", "").strip().strip(";")
        product_data = demjson.decode(js_str)
        product_nodes = response.xpath(color_id_xpath)
        for item in product_nodes:
            product_id = item.attrib.get("data-articlecode")
            article_code = product_data.get('articleCode')
            if data := product_data.get(product_id):
                sku = article_code + "_" + product_id
                title = data.get("title")
                color = data.get("name")
                desc = data.get('description')
                html_url = data.get('pdpLink')
                price = data.get('priceValue') or data.get('priceSaleValue')
                sizes = []
                if data.get('variants'):
                    for size in data.get('variants'):
                        sizes.append(size.get('sizeName'))
                images = []
                if data.get('vAssets'):
                    for img in data.get('vAssets'):
                        images.append("https:" + img.get('zoom'))

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
                    "basc": desc,
                    "brand": product_data.get("brand")
                }

                yield ProductDetailItem(**item_data)

    def start_requests(self):

        url = 'https://www.stories.com/en/clothing/dresses/maxi-dresses/product.smocked-strappy-maxi-dress-black.1102894001.html'
        yield scrapy.Request(url, callback=self.parse_product_detail, errback=self.start_request_error,
                             dont_filter=True)
