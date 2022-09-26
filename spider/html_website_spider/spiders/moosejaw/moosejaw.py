import scrapy
from ..common_spider import CommonSpider
from .. import ProductUrlItem, ProductDetailItem
import json
from datetime import datetime
from urllib.parse import urlencode, urlparse


class MoosejawSpider(CommonSpider):
    name = 'moosejaw'
    allowed_domains = ['moosejaw.com']
    base_url = "https://www.moosejaw.com"

    custom_settings = {
        'COOKIES_ENABLED': False,
        "CONCURRENT_REQUESTS": 4,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2,
        'Cookie': '_pxhd=FhrniTRpGue3Y1lxQjL-qfi-gB1QGccrgESsYcHo8ipd524NQYGg96WD7sO/gGK/kuzDsb6-z7F5rt3nQCJ2VA==:DuxNa20/YJPkmCLI6gZZS7Wfs85vQD7zbZlKf1igdH5INsKO7WbHtg8f2vloK-MFLR9aBdz69hbpUBVHD6WXUlFc4uGKW/u3qa-gBYTaJ48=; _pxvid=fabad384-2292-11ed-99d2-435163565949; mt.v=2.1619513881.1661225055478; _ga=GA1.2.1243255140.1661225056; _gid=GA1.2.199426169.1661225056; WC_PERSISTENT=gR6%2F3s75d9205%2BMZqUi41vakvoJll1kQ4q%2FZcKEJL%2BQ%3D%3B2022-08-22+23%3A24%3A16.176_1661225056171-452985_10208_-1002%2C-1%2CUSD%2C2022-08-22+23%3A24%3A16.176_10208; sod=; a1ashgd=q483c0zm7e000000q483c0zm7e000000; _gcl_au=1.1.1413587224.1661225056; _fbp=fb.1.1661225064856.95036179; rj2session=ddebaa51-33e0-4f81-9807-f66b57bf8485; _clck=1ya2cko|1|f49|0; CoreID6=19279323348216612250663&ci=90220406; tracker_device=4c7220d1-f6fa-4fd0-ab46-7210169903e3; __attentive_id=83e889c822714147835c432a61d60b36; __attentive_cco=1661225447548; __attentive_dv=1; LPVID=BlZGNlNTNmNDlhOTNiYTM5; BVBRANDID=f5287b1e-a36f-4d96-995b-0e76a2d47473; _pin_unauth=dWlkPU4yTXhZemd5TmpRdFkySmpOeTAwWmpJM0xXRTJOell0TmpVMk5HRXhOR0ZtTldRMA; JSESSIONID=00009QInuhBKD68k8uDybbh3BYr:-1; WC_SESSION_ESTABLISHED=true; WC_AUTHENTICATION_-1002=-1002%2CJdh5JVzqovGDGuZIS9A0yAc11LCiDPi1CWNOoTX%2B9xo%3D; WC_ACTIVEPOINTER=-1%2C10208; BVImplmain_site=18209; DesiredPDPColor=; MJRVI_10000001=6244623_product%7C6642341_product; pxcts=2f194a16-2298-11ed-9c86-694d7451444f; IR_gbd=moosejaw.com; cmTPSet=Y; fs_uid=#mZR#5412878057771008:5029387264626688:::#/1692761064; _pxff_rf=1; _pxff_fp=1; _gat_UA-9999586-1=1; _uetsid=16745160229311edb034795ffa21fe00; _uetvid=16749af0229311eda258cf7015ade350; IR_1676=1661230413729%7C0%7C1661230413729%7C%7C; fsURL=https://app.fullstory.com/ui/mZR/session/5412878057771008%3A5029387264626688; _px3=76e21c4734278fd1caa6ab6450f382da3340329458e1259e56fd22fa5bffead2:ewxz46q3gsBZIzU8Mf58fr4rz9V7Izh9knFoVm9EnaCrcyY3eTt0tsw/2HKKJcRjQetoKedZJBCy/W5eUo6y5g==:1000:oMhkxOoIqb1eopzpy0BHjnugc/N3WWxZ09AcZ1i8sowiAlUIKoaHTlb7jeVxGNflPoYOAwrDwVX+E5/seF3yxl4ZUSOPGYqzVHGwi5c5sy72rppROJN+p86kQ2bMGV+2Z1IcU7bq3r/IyIDQcZ6LAbL3nBD7Yg3tGI+BvnltzXuTHjoW0tGpEVZpoba62jZ8x5m8cLLET3fhG8IW8gjrKg==; _clsk=14efbks|1661230414768|2|1|n.clarity.ms/collect; 90220406_clogin=l=27425771661230413692&v=1&e=1661232216253; CompareItems_10208=; searchTermHistory=%7Cmens%20goretex%20jackets; WC_USERACTIVITY_-1002=-1002%2C10208%2C0%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2C869115313%2Cver_null%2Czp06%2FnlHt4Gv8jQXg3QKWa9eoSLpV8maGSIxRRi8Erl4aAEd1ckVu3rd%2BWR0qJSqZgNjXhLgkgLLwOX6f1W9LjVfJiwGgFLnUbWjyWcWoHu7ysQZnKsRPddGzqq4PMWMsXPRxGBu0aSzA1vs452JPxRbehBLJ5%2F1CbY3FntXLlmmy7LjEarT3fLf24Zdz2gaQdG5NVB7jtdewoMJXXacie5hVH6UllCN1NdLufNSoTU%3D; WC_ACTIVITYDATA_-1002=G%2C-1%2CUSD%2C10000001%2C10011%2C-2000%2C1661225056171-452985%2C-1%2CUSD%2C6rwj90EvvGAG50G6A9nMKHQacloQprxtMeudb7eJcyXLuICqgRDRxkZlDp9bINrU7JwyybHKzWnPTI3k2GSrRRkVORcuYblzYV0zskPiyJInxak5xNEJS4rslRfD0ado0zgjDPgAIHRndR8cR6wbqsseQuYNeDGi6rSOvMQHIUFW5Czq%2F2Sn4sCuPY%2BmHgkCxOKEx5qT2n3q7c%2FInE5FLkcySQNoEzixlJnhBfV5h00%3D; cto_bundle=fflZKF80YTg3TTZpbnNxb1lsT0RjZlU3RHJLVjhRbFNMTUU3SDN6UGYyNUQ0Vnk5OFJpamttN1VWcERTYm5CYkQ2cDhrOXdGUnRvUUFNTjVDRmElMkZWRUgyUiUyQkF4NlMlMkJmclczNiUyRlF5MVc3d2xlVHprT0U4WTQydCUyRllGWmoxSlVwbVc4NURhbjJleW10SVdJdTM1eHhkcldYa1N3JTNEJTNE; __attentive_pv=1; __attentive_ss_referrer="ORGANIC"; LPSID-9888306=eIKvZg_WTvODOWs48piWcw'
    }

    def parse_product_list(self, response, **kwargs):
        product_link_xpath = '//a[@class="price-to-pdp-link"]'
        next_page_link_xpath = '//div[@class="search-pagination-button next-page"]/a'
        product_links = response.xpath(product_link_xpath)
        next_page_link = response.xpath(next_page_link_xpath)

        for item in product_links:
            item_data = {
                "category_name": response.meta.get("category_name"),
                "detail_url": item.attrib.get("href"),
                "referer": response.meta.get("referer"),
                "page_url": response.url,
                "meta": response.meta,
                "callback": self.parse_product_detail,
            }

            for task in self.request_product_detail(**item_data):
                yield task

        if next_page_link and (next_page_url := next_page_link.attrib.get("href")):
            yield scrapy.Request(next_page_url, meta=response.meta, callback=self.parse_product_list,
                                 errback=self.start_request_error, dont_filter=True)

    def parse_product_detail(self, response):

        title_xpath = '//div[@id="mobilePDPtitle"]/text()'
        title = response.xpath(title_xpath).get()
        image_str = response.selector.re_first('data-argument-jsimagelist="\[(.*)\]"')
        extra_images = image_str.split(",")
        images = {}
        pdid = response.xpath('//input[@id="pfid"]/@value').get()
        price = response.xpath('//input[@id="adwordsTotalValue"]/@value').get()
        size = response.selector.re('distinctSizeListArray\[.*=.*"(.*)"')
        brand = response.selector.re_first('manufacturerName = "(.*?)"')
        description = response.selector.xpath('//article[@id="productFeatures"]').get()
        for image in extra_images:
            src, color = image.split("|")
            max_src = (urlparse(src)._replace(query="$product1500$").geturl()).strip()
            if color in images.keys():
                images[color].append(max_src)
            else:
                images[color] = [max_src]

        for color in images.keys():
            sku = pdid + "_" + color
            sku = sku.replace(" ", "-").replace("/", "")
            img = images.get(color)
            item_data = {
                "project_name": self.project_name,
                "PageUrl": response.url,
                "html_url": response.url,
                "category_name": response.meta.get("category_name"),
                "sku": sku,
                "color": color,
                "size": size,
                "img": img,
                "price": price,
                "title": title,
                "dade": datetime.now(),
                "basc": description,
                "brand": brand
            }

            yield ProductDetailItem(**item_data)
