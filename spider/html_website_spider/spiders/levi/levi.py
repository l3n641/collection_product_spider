import scrapy
from ..common_spider import CommonSpider
from .. import ProductUrlItem, ProductDetailItem
import json
from datetime import datetime
from urllib.parse import urlencode
from urllib.parse import quote
import requests
import urllib.parse
from scrapy.http import JsonRequest


class LeviSpider(CommonSpider):
    name = 'levi'
    allowed_domains = ['levi.com', ]
    category_api_url = "https://www.levi.com/nextgen-webhooks/?operationName=categoriesPersonalized&locale=US-en_US"

    def start_by_product_category(self):
        """
        从产品分类里爬取数据
        :return:
        """
        headers = {
            "x-operationname": "categoriesPersonalized",
            "x-bypass-cache": "true",
        }
        product_category = self.product_category
        for url in product_category.keys():
            body = self.get_category_list_params(url, page=0)
            meta = {
                "category_name": product_category.get(url),
                "referer": url,
                "body": body
            }

            yield JsonRequest(self.category_api_url, data=body, meta=meta, callback=self.parse_product_list,
                              errback=self.start_request_error, dont_filter=True, headers=headers)

    def parse_product_list(self, response, **kwargs):
        swatches_api_url = "https://www.levi.com/nextgen-webhooks/?operationName=swatches&locale=US-en_US"
        headers = {
            "x-operationname": "swatches",
        }
        category_headers = {
            "x-operationname": "categoriesPersonalized",
            "x-bypass-cache": "true",
        }

        data = response.json()

        categories_personalized = data.get("data").get("categoriesPersonalized")
        pagination = categories_personalized.get("pagination")
        products = categories_personalized.get("products")

        for product in products:
            swatches_params = self.get_swatches_params(product.get("code"))
            yield JsonRequest(swatches_api_url, data=swatches_params, meta=response.meta, headers=headers,
                              callback=self.parse_product_list2, errback=self.start_request_error, dont_filter=True)

        if pagination.get('currentPage') < pagination.get('totalPages'):
            next_page = pagination.get('currentPage') + 1
            body = self.get_category_list_params(response.meta.get("referer"), page=next_page)
            yield JsonRequest(self.category_api_url, data=body, meta=response.meta, callback=self.parse_product_list,
                              errback=self.start_request_error, dont_filter=True, headers=category_headers)

    def parse_product_list2(self, response):
        product_detail_api_url = "https://www.levi.com/nextgen-webhooks/?operationName=product&locale=US-en_US"
        headers = {
            "x-operationname": "product",
        }
        data = response.json()
        swatches = data.get("data").get("swatches").get("swatches")
        for item in swatches:
            detail_url = "https://www.levi.com/US/en_US" + item.get("url")
            item_data = {
                "category_name": response.meta.get("category_name"),
                "url": detail_url,
                "referer": response.meta.get("referer"),
                "status": 0,
                "page_url": product_detail_api_url,
            }
            yield ProductUrlItem(**item_data)
            params = self.get_product_detail(item.get("code"))
            yield JsonRequest(product_detail_api_url, data=params, meta=response.meta, headers=headers,
                              callback=self.parse_product_detail, dont_filter=True)

    def parse_product_detail(self, response, ):
        data = response.json()
        product = data.get("data").get("product")
        variant_options = product.get("variantOptions")
        html_url = "https://www.levi.com/US/en_US" + product.get("url")
        images = []
        image_args = "fmt=jpeg&qlt=70,1&op_sharpen=0&resMode=sharp2&op_usm=0.8,1,10,0&fit=crop,0&wid=1250&hei=1667"
        for item in product.get("galleryImageList").get("galleryImage"):
            info = urllib.parse.urlsplit(item.get("url"))
            url = f"{info.scheme}://{info.hostname}/{info.path}?{image_args}"
            images.append(url)
        size_list = []

        for item in variant_options:
            size_list.append(item.get("displaySizeDescription"))

        item_data = {
            "project_name": self.project_name,
            "PageUrl": response.url,
            "html_url": html_url,
            "category_name": response.meta.get("category_name"),
            "sku": product.get("code"),
            "color": product.get("colorName"),
            "size": size_list,
            "img": images,
            "price": product.get("price").get("regularPrice"),
            "title": product.get("seoMetaData").get("metaH1"),
            "dade": datetime.now(),
            "basc": product.get("description"),
            "brand": ""
        }

        yield ProductDetailItem(**item_data)

    @staticmethod
    def get_category_list_params(url, page, page_size=36):
        data = urllib.parse.urlsplit(url)
        country_data, category_data = data.path[1:].split("/c/")
        country, locale, *_ = country_data.split("/")
        country, locale, *_ = country_data.split("/")
        category_id, *facet_data = category_data.split("/facets/")
        query = ":relevance"
        if facet_data:
            query = query + ":" + facet_data[0].replace("/", ":")

        params = {
            "operationName": "categoriesPersonalized",
            "variables": {
                "query": query,
                "country": country,
                "locale": locale,
                "currentPage": page,
                "pageSize": page_size,
                "sort": "relevance",
                "categoryId": category_id,
                "preOrder": True,
                "anonymousId": "4eb89414-4746-4ef5-a846-c7f5a12d7d0e",
                "region": "LSA",
                "useRecoSnapshot": False
            },
            "query": "query categoriesPersonalized($region: String!, $anonymousId: String!, $query: String!, $sort: String, $currentPage: Int, $pageSize: Int, $categoryId: String!, $preOrder: Boolean, $useRecoSnapshot: Boolean) {\n  categoriesPersonalized(\n    region: $region\n    query: $query\n    sort: $sort\n    currentPage: $currentPage\n    pageSize: $pageSize\n    categoryId: $categoryId\n    preOrder: $preOrder\n    anonymousId: $anonymousId\n    useRecoSnapshot: $useRecoSnapshot\n  ) {\n    description\n    breadcrumbs {\n      facetCode\n      facetName\n      facetValueName\n      removeQuery {\n        query {\n          value\n        }\n        url\n      }\n    }\n    categoryCode\n    categoryHierarchy {\n      code\n      count\n      selected\n      childSelected\n      children\n      depth\n      leaf\n      parentSelected\n    }\n    categoryName\n    emailSignUpGateEnabled\n    registrationGateEnabled\n    currentQuery {\n      url\n    }\n    facets {\n      category\n      code\n      name\n      nofollow\n      priority\n      visible\n      topValues {\n        count\n        name\n        nofollow\n        selected\n        query {\n          query {\n            value\n          }\n          url\n        }\n      }\n      values {\n        count\n        name\n        nofollow\n        selected\n        query {\n          query {\n            value\n          }\n          url\n        }\n      }\n    }\n    freeTextSearch\n    noProductsRedirectMsg\n    lscoBreadcrumbs {\n      name\n      url\n      linkClass\n    }\n    pagination {\n      currentPage\n      totalPages\n      totalResults\n    }\n    personalization\n    numRecommendations\n    products {\n      channels\n      code\n      backOrder\n      name\n      url\n      price {\n        code\n        currencyIso\n        formattedValue\n        hardPrice\n        hardPriceFormattedValue\n        regularPrice\n        regularPriceFormattedValue\n        softPrice\n        softPriceFormattedValue\n        value\n      }\n      priceRange {\n        maxPrice {\n          formattedValue\n          value\n          regularPrice\n          softPrice\n          hardPrice\n        }\n        minPrice {\n          formattedValue\n          value\n          regularPrice\n          softPrice\n          hardPrice\n        }\n      }\n      priceRangeFrom {\n        maxPrice {\n          formattedValue\n          value\n          regularPrice\n          softPrice\n          hardPrice\n        }\n        minPrice {\n          formattedValue\n          value\n          regularPrice\n          softPrice\n          hardPrice\n        }\n      }\n      baseProduct\n      soldIndividually\n      comingSoon\n      averageOverallRatings\n      noOfRatings\n      soldOutForever\n      sustainability\n      findInStoreEligible\n      customizable\n      flxCustomization\n      availableForPickup\n      department\n      pdpGroupId\n      preOrder\n      preOrderShipDate\n      returnable\n      variantOptions {\n        code\n        comingSoon\n        preOrder\n        backOrder\n        customizable\n        findInStoreEligible\n        flxCustomization\n        merchantBadge\n        promotionalBadge\n        sustainability\n        name\n        swatchUrl\n        swatchAltText\n        galleryList {\n          galleryImage {\n            altText\n            format\n            galleryIndex\n            imageType\n            url\n          }\n        }\n        priceData {\n          hardPrice\n          hardPriceFormattedValue\n          regularPrice\n          regularPriceFormattedValue\n          softPrice\n          softPriceFormattedValue\n          value\n          currencyIso\n        }\n        soldIndividually\n        soldOutForever\n        url\n      }\n      lscoBreadcrumbs {\n        categoryCode\n        name\n        url\n      }\n      swatchUrl\n      swatchAltText\n      galleryList {\n        galleryImage {\n          altText\n          format\n          galleryIndex\n          imageType\n          url\n        }\n      }\n      merchantBadge\n      promotionalBadge\n      errors {\n        component\n        name\n        time_thrown\n        message\n      }\n    }\n    seoMetaData {\n      canonicalUrl\n      metaDescription\n      metaH1\n      metaTitle\n      robots\n    }\n    sorts {\n      code\n      name\n      selected\n    }\n    spellingSuggestion {\n      query\n      suggestion\n    }\n  }\n}\n"
        }
        return params

    @staticmethod
    def get_swatches_params(product_id):
        data = {
            "operationName": "swatches",
            "variables": {
                "code": product_id
            },
            "query": "query swatches($code: String!) {\n  swatches(code: $code) {\n    swatches {\n      active\n      available\n      code\n      colorName\n      imageUrl\n      url\n      variantsAvailability {\n        available\n        length\n        size\n        waist\n      }\n    }\n    errors {\n      name\n      component\n      message\n    }\n  }\n}\n"
        }
        return data

    @staticmethod
    def get_product_detail(product_id):
        data = {
            "operationName": "product",
            "variables": {
                "code": product_id
            },
            "query": "query product($code: String!) {\n  product(code: $code) {\n    altText\n    averageOverallRatings\n    backOrder\n    baseProduct\n    bopisAvailable\n    channels\n    classifications {\n      code\n      features {\n        code\n        featureValues {\n          value\n          code\n        }\n        name\n        range\n        type\n      }\n      name\n    }\n    code\n    colorName\n    comingSoon\n    crossSellProductUrl\n    crossSellSizeGroup\n    customizable\n    flxCustomization\n    department\n    pdpGroupId\n    preOrder\n    preOrderShipDate\n    returnable\n    description\n    findInStoreEligible\n    lscoBreadcrumbs {\n      categoryCode\n      name\n      url\n    }\n    galleryImageList {\n      galleryImage {\n        altText\n        format\n        galleryIndex\n        imageType\n        url\n      }\n      videos {\n        altText\n        format\n        galleryIndex\n        url\n      }\n    }\n    itemType\n    maxOrderQuantity\n    merchantBadge\n    minOrderQuantity\n    name\n    noOfRatings\n    pdpCmsContentId1\n    pdpCmsContentId2\n    preferredCategory\n    price {\n      code\n      currencyIso\n      formattedValue\n      hardPrice\n      hardPriceFormattedValue\n      maxQuantity\n      minQuantity\n      priceType\n      regularPrice\n      regularPriceFormattedValue\n      softPrice\n      softPriceFormattedValue\n      value\n    }\n    productSchemaOrgMarkup {\n      brand {\n        entry {\n          key\n          value\n        }\n      }\n      gtin12\n      offers {\n        entry {\n          key\n          value\n        }\n      }\n    }\n    promotionalBadge\n    seoMetaData {\n      metaDescription\n      metaH1\n      metaTitle\n      robots\n    }\n    sizeGuide\n    soldIndividually\n    soldOutForever\n    url\n    variantLength\n    variantOptions {\n      code\n      colorName\n      displaySizeDescription\n      maxOrderQuantity\n      minOrderQuantity\n      priceData {\n        code\n        currencyIso\n        formattedValue\n        hardPrice\n        hardPriceFormattedValue\n        maxQuantity\n        minQuantity\n        priceType\n        regularPrice\n        regularPriceFormattedValue\n        softPrice\n        softPriceFormattedValue\n        value\n      }\n      stock {\n        asnDate\n        asnQty\n        stockLevel\n        stockLevelStatus\n      }\n      upc\n      url\n    }\n    variantSize\n    variantType\n    variantWaist\n    inventoryDepthStoresList\n  }\n}\n"
        }
        return data

    @staticmethod
    def start_request_error(failure):
        print(f"excel 链接无效:{failure.request.meta.get('referer')}")
