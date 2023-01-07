from ..common_spider import CommonSpider
from .. import ProductUrlItem, ProductDetailItem
from datetime import datetime
from scrapy.http import JsonRequest

from urllib.parse import urlparse


class OnRunningFrSpider(CommonSpider):
    name = 'onrunning_fr'
    allowed_domains = ['on-running.com']
    base_url = "https://www.on-running.com/"

    def start_by_product_category(self):
        """
        从产品分类里爬取数据
        :return:
        """

        product_category = self.product_category
        for url in product_category.keys():
            result = urlparse(url)
            lang, explore, gender, product, *p_type = result.path.strip("/").split("/")
            meta = {
                "category_name": product_category.get(url),
                "referer": url,
                "gender": gender,
            }
            if product == "shoes":
                field = "best_for"
            else:
                field = f"{product}_category"
            item_filters = [
                {
                    "name": "product",
                    "values": [
                        product
                    ]
                },
                {
                    "name": field,
                    "values": p_type
                }
            ]
            data = {
                "operationName": None,
                "variables": {
                    "identifier": "explore",
                    "first": None,
                    "before": None,
                    "after": "",
                    "itemFilters": item_filters,
                    "variantFilters": [
                        {
                            "name": "gender",
                            "values": [
                                gender
                            ]
                        }
                    ]
                },
                "query": "query ($identifier: String!, $sortBy: ItemsSortByInput, $itemFilters: [FilterInput!], $variantFilters: [FilterInput!], $first: Int, $last: Int, $before: String, $after: String) {\n  filterPage(identifier: $identifier) {\n    explodeVariants\n    articlesPageBottom\n    paginatedItems(\n      first: $first\n      last: $last\n      before: $before\n      after: $after\n      sortBy: $sortBy\n      filters: $itemFilters\n    ) {\n      totalCount\n      pageInfo {\n        startCursor\n        endCursor\n        hasPreviousPage\n        hasNextPage\n        __typename\n      }\n      nodes {\n        id\n        name\n        mainVariantId\n        price\n        labels\n        productData {\n          shortDescription\n          productSubtype\n          __typename\n        }\n        variants(filters: $variantFilters) {\n          id\n          isBackorderable\n          isRaffle\n          hasRaffleEnded\n          colorName\n          filterValues\n          labels\n          productUrl\n          isMembersOnly\n          imageUrl\n          backgroundImageUrl\n          backgroundVideoUrl\n          skus\n          spreeProduct\n          productVariantData {\n            defaultImageSmall\n            assets\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"
            }
            api = 'https://www.on-running.com/en-us/graphql'

            yield JsonRequest(api, data=data, meta=meta, callback=self.parse_product_list,
                              errback=self.start_request_error, dont_filter=True)

    def parse_product_list(self, response):
        data = response.json()
        paginated_items = data.get('data').get("filterPage").get("paginatedItems")
        page_info = paginated_items.get("pageInfo")

        if page_info.get("hasNextPage"):
            print('xxx')

        for node in paginated_items.get("nodes"):
            slug = node.get("name").lower().replace(" ", "-").strip("-")
            api = f'https://www.on-running.com/en-us/graphql?slug={slug}&gender={response.meta.get("gender")}'

            post_data = {
                "operationName": None,
                "variables": {
                    "slug": slug
                },
                "query": "query ($slug: String!) {\n  productGroup(slug: $slug, isFetchingAssets: true) {\n    name\n    slug\n    productData {\n      careInstructions\n      composition\n      sustainability\n      description\n      mediaGalleryItems\n      name\n      productSpec\n      productSpecType\n      productSubtype\n      labels\n      shortDescription\n      isSubscriptionProduct\n      variants {\n        id\n        labels\n        assets\n        description\n        color\n        defaultImage\n        defaultImageSmall\n        topBanner\n        campaignIds {\n          ...campaignIds\n          __typename\n        }\n        fit\n        modelInformation\n        isMembersOnly\n        inseams {\n          size\n          cm\n          inches\n          __typename\n        }\n        gender\n        highlights\n        spreeProduct {\n          id\n          isLocked\n          isBackorderable\n          isPreorderable\n          isRaffle\n          raffleExpiresAt\n          raffleDrawAt\n          hasRaffleEnded\n          price\n          productType\n          productUrl\n          sku\n          spreeVariants {\n            id\n            size\n            sku\n            stock\n            price\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  sizeInfo {\n    isSizeInfoVisible\n    __typename\n  }\n}\n\nfragment campaignIds on CampaignIds {\n  variationId\n  decisionId\n  __typename\n}\n"
            }
            data = None  # 数据库记录
            if self.is_continue:
                data = self.get_product_log(api, response.meta.get("category_name"))
                if data and data.status == 1:
                    continue

            if not data:
                item_data = {
                    "category_name": response.meta.get("category_name"),
                    "url": api,
                    "referer": response.meta.get("referer"),
                    "status": 0,
                    "page_url": response.meta.get("referer"),
                }
                yield ProductUrlItem(**item_data)
            yield JsonRequest(api, data=post_data, meta=response.meta, callback=self.parse_product_detail,
                              errback=self.start_request_error, dont_filter=True)

    def parse_product_detail(self, response):
        gender = response.meta.get("gender")
        data = response.json()
        product_group = data.get("data").get('productGroup')
        if not product_group:
            return None
        product_data = product_group.get("productData")
        title = product_data.get("name")
        description = product_data.get("description")
        slug = product_group.get("slug")

        for variant in product_data.get("variants"):
            if variant.get("gender") != gender:
                continue

            sku = slug + "_" + gender + "_" + str(variant.get("id"))
            sku = sku.replace(" ", "-")
            spree_product = variant.get("spreeProduct")
            color = variant.get("color")
            price = spree_product.get("price")
            images = []
            for asset in variant.get("assets"):
                images.append("http:" + asset.get("mediaUrl"))
            size = []
            for item in spree_product.get("spreeVariants"):
                size.append(item.get("size"))
            item_data = {
                "project_name": self.project_name,
                "PageUrl": response.url,
                "html_url": spree_product.get("productUrl"),
                "category_name": response.meta.get("category_name"),
                "sku": sku,
                "color": color,
                "size": size,
                "img": images,
                "price": price,
                "title": title,
                "dade": datetime.now(),
                "basc": description,
                "brand": ""
            }

            yield ProductDetailItem(**item_data)
