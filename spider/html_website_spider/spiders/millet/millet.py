import json
import requests
import scrapy
from ..common_direct_spider import CommonDirectSpider
from .. import ProductUrlItem, ProductDetailItem
from datetime import datetime


class MilletSpider(CommonDirectSpider):
    name = 'millet_fr'
    allowed_domains = ['millet.com']

    custom_settings = {
        "CONCURRENT_REQUESTS": 16,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2
    }

    def get_category_url(self, cid, current_page=1):
        query = 'fragment AmGiftCardPricesFragment on ProductInterface{...on AmGiftCardProduct{am_giftcard_type ...GiftCardPrices __typename}__typename}fragment GiftCardPrices on AmGiftCardProduct{am_allow_open_amount am_open_amount_min{currency value __typename}am_open_amount_max{currency value __typename}am_giftcard_prices{price_id attribute_id value{currency value default __typename}__typename}__typename}query GetCategories($id:String!$pageSize:Int!$currentPage:Int!$filters:ProductAttributeFilterInput!$sort:ProductAttributeSortInput$ruleIdentifier:String!="other-product-colors"$attributesSelect:String!="discount_percent,groupe_couleur,genre,type_de_produit"){categories(filters:{category_uid:{in:[$id]}}){items{id uid name ...CategoryFragment __typename}__typename}products(pageSize:$pageSize currentPage:$currentPage filter:$filters sort:$sort attributesSelect:$attributesSelect){...ProductsFragment __typename}}fragment CategoryFragment on CategoryTree{uid meta_title meta_keywords meta_description __typename}fragment ProductsFragment on Products{items{productAutolist(ruleIdentifier:$ruleIdentifier){ruleIdentifier currentEntityId url_suffix items{name entity_id url_key small_image __typename}__typename}id uid name attributes_select{code value __typename}...AmGiftCardPricesFragment price_range{maximum_price{final_price{currency value __typename}regular_price{currency value __typename}final_price_excl_tax{currency value __typename}__typename}__typename}sku small_image{url __typename}worn_image stock_status discount_percent groupe_couleur genre marque type_de_produit rating_summary __typename url_key}page_info{total_pages __typename}total_count __typename}'
        variables = {
            "ruleIdentifier": "other-product-colors",
            "attributesSelect": "discount_percent,groupe_couleur,genre,type_de_produit",
            "currentPage": current_page,
            "id": cid.replace("=", ""),
            "filters": {
                "category_uid": {
                    "eq": cid
                }
            },
            "pageSize": 23,
            "sort": {
                "nosto_personalized": "ASC"
            }
        }
        params = {
            "query": query,
            "operationName": "GetCategories",
            "variables": json.dumps(variables),
        }
        url = self.make_url_with_query("https://www.millet.com/graphql", params)
        return url

    def parse_product_list(self, response, **kwargs):
        cid_pattern = "'{&quot;uid&quot;:&quot;(.*?)&quot;"
        cid = response.selector.re_first(cid_pattern)

        response.meta["current_page"] = 1
        response.meta["cid"] = cid
        url = self.get_category_url(cid, 1)
        yield scrapy.Request(url, meta=response.meta, callback=self.parse_product_list2,
                             errback=self.start_request_error, dont_filter=True)

    def parse_product_list2(self, response, **kwargs):
        data = response.json().get("data")
        products = data.get("products")
        if not products:
            print(f'not product:{response.meta["referer"]}')
            print(response.text)
        else:
            for item in products.get("items"):
                for product in item.get("productAutolist").get("items"):
                    detail_url = self.get_detail_url(product.get("url_key"))
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

        total_pages = products.get("page_info").get('total_pages')
        if response.meta.get("current_page") < total_pages:
            next_page = response.meta["current_page"] + 1
            response.meta["current_page"] = next_page
            url = self.get_category_url(response.meta["cid"], next_page)
            yield scrapy.Request(url, meta=response.meta, callback=self.parse_product_list2,
                                 errback=self.start_request_error)

    def get_detail_url(self, url_key):
        query = 'query getProductDetailForProductPage($urlKey:String!){products(filter:{url_key:{eq:$urlKey}}){items{id uid ...ProductDetailsFragment ...AmGiftCardProductFragment __typename}__typename}}fragment ProductDetailsFragment on ProductInterface{__typename categories{uid breadcrumbs{category_uid __typename}__typename}description{html __typename}short_description{html __typename}id uid media_gallery_entries{uid label position disabled file __typename}meta_title meta_description name marque price{regularPrice{amount{currency value __typename}__typename}__typename}price_range{maximum_price{final_price{currency value __typename}discount{amount_off __typename}regular_price{value currency __typename}final_price_excl_tax{currency value __typename}__typename}__typename}sku small_image{url __typename}stock_status url_key custom_attributes{selected_attribute_options{attribute_option{uid label is_default __typename}__typename}entered_attribute_value{value __typename}attribute_metadata{uid code label attribute_labels{store_code label __typename}data_type is_system entity_type ui_input{ui_input_type is_html_allowed __typename}...on ProductAttributeMetadata{used_in_components __typename}__typename}__typename}...on ConfigurableProduct{configurable_options{attribute_code attribute_id uid label values{uid default_label label store_label use_default_value value_index swatch_data{...on ImageSwatchData{thumbnail __typename}value __typename}__typename}__typename}variants{attributes{code value_index __typename}product{uid media_gallery_entries{uid disabled file label position __typename}sku stock_status price{regularPrice{amount{currency value __typename}__typename}__typename}price_range{maximum_price{final_price{currency value __typename}discount{amount_off __typename}regular_price{value currency __typename}__typename}__typename}custom_attributes{selected_attribute_options{attribute_option{uid label is_default __typename}__typename}entered_attribute_value{value __typename}attribute_metadata{uid code label attribute_labels{store_code label __typename}data_type is_system entity_type ui_input{ui_input_type is_html_allowed __typename}...on ProductAttributeMetadata{used_in_components __typename}__typename}__typename}__typename}__typename}__typename}}fragment AmGiftCardProductFragment on ProductInterface{...on AmGiftCardProduct{am_giftcard_fee_enable am_giftcard_fee_type am_giftcard_fee_value am_giftcard_type am_giftcard_lifetime am_email_template am_images{uid image_id title status image_path user_upload __typename}...GiftCardPrices __typename}__typename}fragment GiftCardPrices on AmGiftCardProduct{am_allow_open_amount am_open_amount_min{currency value __typename}am_open_amount_max{currency value __typename}am_giftcard_prices{price_id attribute_id value{currency value default __typename}__typename}__typename}'
        params = {
            "query": query,
            "operationName": "getProductDetailForProductPage",
            "variables": json.dumps({"urlKey": url_key}),
        }
        url = self.make_url_with_query("https://www.millet.com/graphql", params)
        return url

    def parse_product_detail(self, response):
        product = response.json().get("data").get("products").get("items")[0]
        sku = product.get("sku")
        description = product.get("description").get("html")
        title = product.get("name")
        price = product.get("price").get("regularPrice").get("amount").get("value")
        images = []
        image_args = "?format=pjpg&bg-color=f3f3f3&width=1200&height=1200&fit=cover"
        image_domain = "https://www.millet.com"
        for item in product.get("media_gallery_entries"):
            img = image_domain + item.get("file") + image_args
            images.append(img)

        sizes = []
        for item in product.get("configurable_options"):
            if item.get("attribute_code") == "taille":
                for v in item.get("values"):
                    sizes.append(v.get("label"))

        color = ""
        for attrib in product.get("custom_attributes"):
            if attrib.get("attribute_metadata").get("code") == "groupe_couleur":
                if color_node := attrib.get("selected_attribute_options").get("attribute_option"):
                    color = color_node[0].get("label")

        item_data = {
            "project_name": self.project_name,
            "PageUrl": response.url,
            "html_url": response.url,
            "category_name": response.meta.get("category_name", ""),
            "sku": sku,
            "color": color,
            "size": sizes,
            "img": images,
            "price": price,
            "title": title,
            "dade": datetime.now(),
            "basc": description,
            "brand": "Millet"
        }

        yield ProductDetailItem(**item_data)
