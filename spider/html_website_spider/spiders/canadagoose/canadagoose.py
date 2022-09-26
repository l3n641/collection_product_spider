import scrapy
from ..common_spider import CommonSpider
from .. import ProductUrlItem, ProductDetailItem
from html import unescape
from urllib.parse import urlencode
from datetime import datetime


class CanadagooseSpider(CommonSpider):
    name = 'canadagoose'
    allowed_domains = ['canadagoose.com']
    base_url = "https://www.canadagoose.com"

    custom_settings = {
        'COOKIES_ENABLED': False,
        "HTTPERROR_ALLOWED_CODES": [429]
    }

    default_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
        "x-kpsdk-ct": "0QsvtUY47UVDUFSaNJY2kytLEqz23tSlewVlxtd2dmZzSgM3TbqrxMGFjPuxLJbMOWULTHCyZxjVl1p7n2pAr7dzc6WbjTKUwxCJT1JO8V8tlWezDzqVBdUbksSIK2cVpmzZjDrbfuAjugcjXJ383YuU1",
        "cookie": 'dwanonymous_b3aa5771d8435c67a1a8775183c875b2=abEj3eOWBa2PZuo4KqyNRyRdwV; zarget_user_id=1009f404-cdef-4464-8fbe-b42e02ffb289; __cq_uuid=abpW7OjUPgPhOIETtL3B3rGU1H; 1009f404-cdef-4464-8fbe-b42e02ffb289=1; 1009f404-cdef-4464-8fbe-b42e02ffb289=1; zarget_visitor_info={"ARXXQP\\":-1}; geoIPSiteSelection=CanadaGooseUS; globalBannerIsHidden=; _gcl_au=1.1.1094756515.1661411049; _gid=GA1.2.1081869744.1661411049; _lc2_fpi=c88e71b6d53c--01gb9x1fre03x5r9wz5qg8tvs2; _scid=eb3cf4aa-a3fe-4329-a877-c94ec03b2a4b; _fbp=fb.1.1661411049633.458753652; _tt_enable_cookie=1; _ttp=34104b06-bb36-4c6a-b349-251723b91669; _pin_unauth=dWlkPVpqRmxOR1JqWm1JdE5EazNNQzAwWkdSa0xUZzJNREl0TTJJM05qWm1PRFE0T1RFeg; OptanonAlertBoxClosed=2022-08-25T07:04:10.359Z; _hjFirstSeen=1; _hjSession_2755334=eyJpZCI6ImZiNjU1M2EyLTQ3MTEtNGM2YS1hM2ViLWFlMDc2OGFjZTJiYyIsImNyZWF0ZWQiOjE2NjE0MTEwNTA1NzcsImluU2FtcGxlIjp0cnVlfQ==; _hjAbsoluteSessionInProgress=0; _clck=187fnim|1|f4b|0; _sctr=1|1661356800000; nmstat=30cfcb40-d293-0988-7e79-e365855454b7; _hjSessionUser_2755334=eyJpZCI6IjE1YmE4YWEzLTEyMzYtNTEyNC05YWJhLWQ3NWFlNmFiNGY1NyIsImNyZWF0ZWQiOjE2NjE0MTEwNTAwNjMsImV4aXN0aW5nIjp0cnVlfQ==; rskxRunCookie=0; rCookie=2kkkd23hqfxrjr6y5oodyl78p8zn8; geolocationWindowDialogIsHidden=1; showBasecampOnTimeout=Thu Aug 25 2022 15:06:54 GMT+0800; bm=7111ee50-2444-11ed-b405-87219cd12b7e; BVBRANDID=b34daabd-0ed6-46f5-9a1f-09ee9795048b; __cq_bc={"aata-CanadaGooseUS":[{"id":"3035WB1"},{"id":"2235L"},{"id":"2905L"}]}; __cq_seg=0~0.30!1~0.48!2~0.21!3~-0.20!4~0.21!5~-0.00!6~0.60!7~0.08!8~0.07!9~0.43!f0~15~5; dwac_cdSAUiaaio11EaaadnOiJrNbA7=jIY-he9WxWhyNibMzJoFUrqrvWpbrdfkivs=|dw-only|||USD|false|Canada/Eastern|true; cqcid=abEj3eOWBa2PZuo4KqyNRyRdwV; cquid=||; sid=jIY-he9WxWhyNibMzJoFUrqrvWpbrdfkivs; dwsid=I3bxETXdw9vrhnsRN__lJBVbcv6BJtFXE0vG0FQ7cigRcX3cDRQL46nQJPEUSXPnP2pytsbe08ntKW3Zdlxcmg==; language=en; __cq_dnt=0; dw_dnt=0; countryCode=US; undefined=undefined; _li_dcdm_c=.canadagoose.com; livechatclosed=no; CanadaGooseUS-pagevisits={"pagevisits":5}; OptanonConsent=isGpcEnabled=0&datestamp=Thu+Aug+25+2022+16:25:27+GMT+0800&version=6.35.0&isIABGlobal=false&hosts=&landingPath=NotLandingPage&groups=C0001:1,C0002:1,C0003:1,C0004:1&consentId=623095c9-de0f-4508-ae81-286c69cc4b76&interactionCount=1&geolocation=US;TX&AwaitingReconsent=false; _uetsid=1dc6b4f0244411ed8e736938ad5ae582; _uetvid=1dc6d930244411ed84170fbf6064fdeb; _ga=GA1.2.724266008.1661411049; lastRskxRun=1661415933390; _ga_NB61BCYEJL=GS1.1.1661411048.1.1.1661416754.54.0.0; akm_bmfp_b2-ssn=0Gnu4o2Q89g1mnggzkQ7N6HnkVC4NlHBDDjS3k5p0R69xZNMOKrD1MBNKEoJxCqhbpli2bCDJfLXEE6MY2uvJ35g9cmIJJtraOQhjj3YEU1HTCoOHfJTM0OY1s94239dT8ntSr9p4ZadUteMxgZMynWlu; akm_bmfp_b2=0Gnu4o2Q89g1mnggzkQ7N6HnkVC4NlHBDDjS3k5p0R69xZNMOKrD1MBNKEoJxCqhbpli2bCDJfLXEE6MY2uvJ35g9cmIJJtraOQhjj3YEU1HTCoOHfJTM0OY1s94239dT8ntSr9p4ZadUteMxgZMynWlu; _clsk=axsszl|1661416767296|33|1|a.clarity.ms/collect'
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

            yield scrapy.Request(url, meta=meta, callback=self.parse_product_list, headers=self.default_headers,
                                 errback=self.start_request_error, dont_filter=True)

    def parse_product_list(self, response, **kwargs):
        product_url_xpath = '//div[@data-pid]'
        next_page_xpath = '//div[@class="infinite-scroll-placeholder"]'
        nodes = response.xpath(product_url_xpath)

        for item in nodes:
            product_id = item.attrib.get('data-pid')
            for color_node in item.xpath('div//ul[@class="swatch-list"]/li/a'):
                color_id = color_node.attrib.get('data-colorid')
                color_key = f"dwvar_{color_id}_Color"
                query = {
                    "quantity": 1,
                    "pid": product_id,
                    color_key: color_id
                }
                params = urlencode(query)
                detail_url = 'https://www.canadagoose.com/us/en/view-product?' + params

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

        if node := response.xpath(next_page_xpath):
            url = unescape(node.attrib.get("data-grid-url"))
            yield scrapy.Request(url, meta=response.meta, callback=self.parse_product_list,
                                 headers=self.default_headers,
                                 errback=self.start_request_error, dont_filter=True)

    def parse_product_detail(self, response):
        data = response.json()
        product_data = data.get("product")
        images_data = data.get("images")
        sizes = []
        color = ""
        price = product_data.get("price").get("sales").get("decimalPrice")
        for item in product_data.get("variationAttributes"):
            if item.get("id") == "Color":
                color = item.get("displayValue")

            if item.get("id") == "Size":
                for size in item.get("values"):
                    sizes.append(size.get("description"))

        images = [images_data.get("fsPrimaryHero").replace("w_1920", "w_1333")]
        for image in images_data.get("alternateUrls"):
            src = image.get("productZoom")
            images.append(src)

        for image in images_data.get("flatLayUrls"):
            src = image.get("productZoom")
            images.append(src)

        sku = product_data.get("id") + "_" + color.replace(" ", "-")
        html_url = self.base_url + product_data.get("selectedProductUrl")
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
