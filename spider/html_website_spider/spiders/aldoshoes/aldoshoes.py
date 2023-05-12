import json
import requests
import scrapy
from ..common_direct_spider import CommonDirectSpider
from .. import ProductUrlItem, ProductDetailItem
from datetime import datetime
import lxml
from urllib.parse import urlencode
from urllib.parse import urlparse, parse_qsl
import re


class AldoShoesSpider(CommonDirectSpider):
    name = 'aldoshoes'
    allowed_domains = ['aldoshoes.com']
    base_url = "https://www.aldoshoes.com/ca/en"
    store_region = "ca"
    store_lang = "en"
    category_header = {
        "authority": "www.aldoshoes.com",
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9,zh;q=0.8,zh-CN;q=0.7",
        "content-type": "application/json",
        "sec-ch-ua": "",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        "x-aldo-api-version": "2",
        "x-aldo-brand": "aldoshoes",
        "x-aldo-lang": "en",
        "x-aldo-region": "ca",
        "x-aldo-ssr-request-id": "",
        "x-forwarded-akamai-edgescape": "undefined",
    }

    custom_settings = {
        "CONCURRENT_REQUESTS": 6,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2
    }

    @staticmethod
    def get_category_id(url):
        try:
            response = requests.get(url, timeout=60)
            pattern = '"category":{"page_id":"(\d+)","referral":""'
            result = re.search(pattern, response.text)
            return result.group(1)
        except Exception:
            print(url)
            return None

    @staticmethod
    def get_category_id_local(url: str):
        category_tree = {
            "women": {
                "title": "Women",
                "categoryId": "100"
            },
            "women\u002Fnew-arrivals": {
                "title": "New arrivals",
                "categoryId": "1001"
            },
            "women\u002Fnew-arrivals\u002Ffootwear": {
                "title": "Footwear",
                "categoryId": "101"
            },
            "women\u002Fnew-arrivals\u002Fhandbags": {
                "title": "Handbags",
                "categoryId": "301"
            },
            "women\u002Fnew-arrivals\u002Faccessories": {
                "title": "Accessories",
                "categoryId": "3101"
            },
            "women\u002Ffootwear": {
                "title": "Footwear",
                "categoryId": "1000"
            },
            "women\u002Ffootwear\u002Fflats": {
                "title": "Flats",
                "categoryId": "111"
            },
            "women\u002Ffootwear\u002Fflats\u002Floafers": {
                "title": "Loafers",
                "categoryId": "117"
            },
            "women\u002Ffootwear\u002Fflats\u002Foxfords": {
                "title": "Oxfords",
                "categoryId": "119"
            },
            "women\u002Ffootwear\u002Fflats\u002Fballerinas": {
                "title": "Ballerinas",
                "categoryId": "1111"
            },
            "women\u002Ffootwear\u002Fheels": {
                "title": "Heels",
                "categoryId": "112"
            },
            "women\u002Ffootwear\u002Fheels\u002Fkitten-heels": {
                "title": "Kitten heels",
                "categoryId": "116"
            },
            "women\u002Ffootwear\u002Fheels\u002Fpumps": {
                "title": "Pumps",
                "categoryId": "1121"
            },
            "women\u002Ffootwear\u002Fheels\u002Fplatforms": {
                "title": "Platforms",
                "categoryId": "113"
            },
            "women\u002Ffootwear\u002Fheels\u002Fblock-heels": {
                "title": "Block heels",
                "categoryId": "1122"
            },
            "women\u002Ffootwear\u002Fheels\u002Fhigh-heels": {
                "title": "High heels",
                "categoryId": "1140"
            },
            "women\u002Ffootwear\u002Fheels\u002Fmules": {
                "title": "Mules",
                "categoryId": "7133"
            },
            "women\u002Ffootwear\u002Fheels\u002Fstrappy-heels": {
                "title": "Strappy Heels",
                "categoryId": "114"
            },
            "women\u002Ffootwear\u002Fheels\u002Fheeled-sandals": {
                "title": "Heeled sandals",
                "categoryId": "122"
            },
            "women\u002Ffootwear\u002Fsneakers": {
                "title": "Sneakers",
                "categoryId": "118"
            },
            "women\u002Ffootwear\u002Fsneakers\u002Flow-top-sneakers": {
                "title": "Low top sneakers",
                "categoryId": "1180"
            },
            "women\u002Ffootwear\u002Fsneakers\u002Fplatform-and-wedge-sneakers": {
                "title": "Platform and Wedge Sneakers",
                "categoryId": "1200"
            },
            "women\u002Ffootwear\u002Fsneakers\u002Flace-up-sneakers": {
                "title": "Lace up sneakers",
                "categoryId": "1181"
            },
            "women\u002Ffootwear\u002Fsneakers\u002Fslip-on-sneakers": {
                "title": "Slip on sneakers",
                "categoryId": "1182"
            },
            "women\u002Ffootwear\u002Fsneakers\u002Fhigh-top-sneakers": {
                "title": "High top sneakers",
                "categoryId": "1183"
            },
            "women\u002Ffootwear\u002Fboots": {
                "title": "Boots",
                "categoryId": "130"
            },
            "women\u002Ffootwear\u002Fboots\u002Fankle-boots": {
                "title": "Ankle boots",
                "categoryId": "131"
            },
            "women\u002Ffootwear\u002Fboots\u002Fdress-boots": {
                "title": "Dress boots",
                "categoryId": "136"
            },
            "women\u002Ffootwear\u002Fboots\u002Fwinter-boots": {
                "title": "Winter boots",
                "categoryId": "137"
            },
            "women\u002Ffootwear\u002Fboots\u002Fcombat-boots": {
                "title": "Combat boots",
                "categoryId": "71263"
            },
            "women\u002Ffootwear\u002Fboots\u002Fchelsea-boots": {
                "title": "Chelsea boots",
                "categoryId": "146"
            },
            "women\u002Ffootwear\u002Fboots\u002Fcasual-boots": {
                "title": "Casual boots",
                "categoryId": "138"
            },
            "women\u002Ffootwear\u002Fboots\u002Fsock-boots": {
                "title": "Sock boots",
                "categoryId": "134"
            },
            "women\u002Ffootwear\u002Fboots\u002Ftall-boots": {
                "title": "Tall Boots",
                "categoryId": "135"
            },
            "women\u002Ffootwear\u002Fsandals": {
                "title": "Sandals",
                "categoryId": "120"
            },
            "women\u002Ffootwear\u002Fsandals\u002Fflats": {
                "title": "Flats",
                "categoryId": "121"
            },
            "women\u002Ffootwear\u002Fsandals\u002Fheeled-sandals": {
                "title": "Heeled sandals",
                "categoryId": "122"
            },
            "women\u002Ffootwear\u002Fsandals\u002Fwedges": {
                "title": "Wedges",
                "categoryId": "123"
            },
            "women\u002Ffootwear\u002Fsandals\u002Fslides": {
                "title": "Slides",
                "categoryId": "127"
            },
            "women\u002Ffootwear\u002Fsandals\u002Fslides\u002Fflats": {
                "title": "Flats",
                "categoryId": "121"
            },
            "women\u002Ffootwear\u002Fsandals\u002Fplatform-sandals": {
                "title": "Platform sandals",
                "categoryId": "126"
            },
            "women\u002Ffootwear\u002Fsandals\u002Fgladiator-sandals": {
                "title": "Gladiator sandals",
                "categoryId": "7138"
            },
            "women\u002Ffootwear\u002Fsandals\u002Fflip-flop-sandals": {
                "title": "Flip flop sandals",
                "categoryId": "128"
            },
            "women\u002Ffootwear\u002Fsandals\u002Fflip-flop-sandals\u002Fflats": {
                "title": "Flats",
                "categoryId": "121"
            },
            "women\u002Ffootwear\u002Fsandals\u002Fdress-sandals": {
                "title": "Dress sandals",
                "categoryId": "129"
            },
            "women\u002Ffootwear\u002Fsandals\u002Fcasual-sandals": {
                "title": "Casual sandals",
                "categoryId": "1120"
            },
            "women\u002Ffootwear\u002Fslippers": {
                "title": "Slippers",
                "categoryId": "7000"
            },
            "women\u002Fhandbags": {
                "title": "Handbags",
                "categoryId": "300"
            },
            "women\u002Fhandbags\u002Ftop-handle": {
                "title": "Top handle",
                "categoryId": "3411"
            },
            "women\u002Fhandbags\u002Ftotes": {
                "title": "Totes",
                "categoryId": "3412"
            },
            "women\u002Fhandbags\u002Fcrossbody": {
                "title": "Crossbody",
                "categoryId": "344"
            },
            "women\u002Fhandbags\u002Fbackpacks": {
                "title": "Backpacks",
                "categoryId": "345"
            },
            "women\u002Fhandbags\u002Fleather-bags": {
                "title": "Leather bags",
                "categoryId": "346"
            },
            "women\u002Fhandbags\u002Fmini": {
                "title": "Mini",
                "categoryId": "350"
            },
            "women\u002Fhandbags\u002Fclutches-evening-bags": {
                "title": 'clutches evening bags',
                "categoryId": "343"
            },
            "women\u002Fhandbags\u002Fblack-friday-must-haves": {
                "title": "black friday must haves",
                "categoryId": "7432"
            },
            "women\u002Fhandbags\u002Ftravel-bags": {
                "title": "Travel bags",
                "categoryId": "352"
            },
            "women\u002Fhandbags\u002Fbucket-bags": {
                "title": "Bucket bags",
                "categoryId": "353"
            },
            "women\u002Fhandbags\u002Fshoulder-bags": {
                "title": "Shoulder bags",
                "categoryId": "354"
            },
            "women\u002Fhandbags\u002Fwork-bags": {
                "title": "Work Bags",
                "categoryId": "358"
            },
            "women\u002Fhandbags\u002Fwallets": {
                "title": "Wallets",
                "categoryId": "348"
            },
            "women\u002Faccessories": {
                "title": "Accessories",
                "categoryId": "310"
            },
            "women\u002Faccessories\u002Fhats-gloves-scarves": {
                "title": "hats gloves scarves",
                "categoryId": "313"
            },
            "women\u002Faccessories\u002Fhats-gloves-scarves\u002Fscarves": {
                "title": "Scarves",
                "categoryId": "3134"
            },
            "women\u002Faccessories\u002Fhats-gloves-scarves\u002Fgloves": {
                "title": "Gloves",
                "categoryId": "3136"
            },
            "women\u002Faccessories\u002Fhats-gloves-scarves\u002Fhats": {
                "title": "Hats",
                "categoryId": "3135"
            },
            "women\u002Faccessories\u002Fjewelry": {
                "title": "Jewelry",
                "categoryId": "3120"
            },
            "women\u002Faccessories\u002Fjewelry\u002Fbody-jewelry": {
                "title": "Body jewelry",
                "categoryId": "3110"
            },
            "women\u002Faccessories\u002Fjewelry\u002Fearrings": {
                "title": "Earrings",
                "categoryId": "3111"
            },
            "women\u002Faccessories\u002Fjewelry\u002Fnecklaces": {
                "title": "Necklaces",
                "categoryId": "314"
            },
            "women\u002Faccessories\u002Fjewelry\u002Fbracelets": {
                "title": "Bracelets",
                "categoryId": "315"
            },
            "women\u002Faccessories\u002Fjewelry\u002Frings": {
                "title": "Rings",
                "categoryId": "316"
            },
            "women\u002Faccessories\u002Fjewelry\u002Fanklets": {
                "title": "Anklets",
                "categoryId": "3121"
            },
            "women\u002Faccessories\u002Fjewelry\u002Fspecial-occasion-jewelry": {
                "title": "Special occasion jewelry",
                "categoryId": "3122"
            },
            "women\u002Faccessories\u002Fjewelry\u002Fspecial-occasion-jewelry\u002Fcubic-zirconia": {
                "title": "Cubic Zirconia",
                "categoryId": "3129"
            },
            "women\u002Faccessories\u002Fjewelry\u002Fspecial-occasion-jewelry\u002Fgold-plated": {
                "title": "Gold plated",
                "categoryId": "3131"
            },
            "women\u002Faccessories\u002Fjewelry\u002Fspecial-occasion-jewelry\u002Fstainless-steel": {
                "title": "Stainless Steel",
                "categoryId": "3132"
            },
            "women\u002Faccessories\u002Fjewelry\u002Fspecial-occasion-jewelry\u002Fsterling-silver": {
                "title": "Sterling Silver",
                "categoryId": "3133"
            },
            "women\u002Faccessories\u002Fwatches": {
                "title": "Watches",
                "categoryId": "312"
            },
            "women\u002Faccessories\u002Fleggings-tights-socks": {
                "title": "leggings tights socks",
                "categoryId": "318"
            },
            "women\u002Faccessories\u002Fsunglasses": {
                "title": "Sunglasses",
                "categoryId": "311"
            },
            "women\u002Faccessories\u002Fsunglasses\u002Faviator": {
                "title": "Aviator",
                "categoryId": "3123"
            },
            "women\u002Faccessories\u002Fsunglasses\u002Fround": {
                "title": "Round",
                "categoryId": "3124"
            },
            "women\u002Faccessories\u002Fsunglasses\u002Fsquare": {
                "title": "Square",
                "categoryId": "3125"
            },
            "women\u002Faccessories\u002Fsunglasses\u002Fcat-eye": {
                "title": "Cat eye",
                "categoryId": "3126"
            },
            "women\u002Faccessories\u002Fsunglasses\u002Fshield": {
                "title": "Shield",
                "categoryId": "3127"
            },
            "women\u002Faccessories\u002Fsunglasses\u002Faccessories": {
                "title": "Accessories",
                "categoryId": "3128"
            },
            "women\u002Faccessories\u002Fsunglasses\u002Fblue-light-blockers": {
                "title": "Blue light blockers",
                "categoryId": "3130"
            },
            "women\u002Faccessories\u002Fsunglasses\u002Feyewear": {
                "title": "Eyewear",
                "categoryId": "3142"
            },
            "women\u002Faccessories\u002Fsunglasses\u002Fstatement-sunglasses": {
                "title": "Statement sunglasses",
                "categoryId": "3143"
            },
            "women\u002Faccessories\u002Ftech-accessories": {
                "title": "Tech accessories",
                "categoryId": "3115"
            },
            "women\u002Faccessories\u002Fbelts": {
                "title": "Belts",
                "categoryId": "317"
            },
            "women\u002Faccessories\u002Fhair-accessories": {
                "title": "Hair accessories",
                "categoryId": "3112"
            },
            "women\u002Faccessories\u002Fshoe-accessories": {
                "title": "Shoe accessories",
                "categoryId": "7503"
            },
            "women\u002Faccessories\u002Farvan-beaded-accessories": {
                "title": "Arvan beaded accessories",
                "categoryId": "3150"
            },
            "women\u002Faccessories\u002Fbag-charms": {
                "title": "Bag charms",
                "categoryId": "349"
            },
            "women\u002Fsale": {
                "title": "Sale",
                "categoryId": "510"
            },
            "women\u002Fsale\u002Ffootwear": {
                "title": "Footwear",
                "categoryId": "5100"
            },
            "women\u002Fsale\u002Ffootwear\u002Fflats": {
                "title": "Flats",
                "categoryId": "5111"
            },
            "women\u002Fsale\u002Ffootwear\u002Fheels": {
                "title": "Heels",
                "categoryId": "5112"
            },
            "women\u002Fsale\u002Ffootwear\u002Fsneakers": {
                "title": "Sneakers",
                "categoryId": "5118"
            },
            "women\u002Fsale\u002Ffootwear\u002Fboots": {
                "title": "Boots",
                "categoryId": "513"
            },
            "women\u002Fsale\u002Ffootwear\u002Fsandals": {
                "title": "Sandals",
                "categoryId": "512"
            },
            "women\u002Fsale\u002Fhandbags": {
                "title": "Handbags",
                "categoryId": "534"
            },
            "women\u002Fsale\u002Faccessories": {
                "title": "Accessories",
                "categoryId": "531"
            },
            "women\u002Fsale\u002F40-to-50-off": {
                "title": "40 to 50 Off",
                "categoryId": "544"
            },
            "women\u002Fsale\u002F30-to-40-off": {
                "title": "30 to 40 Off",
                "categoryId": "545"
            },
            "women\u002Fsale\u002F20-to-30-off": {
                "title": "20 to 30 Off",
                "categoryId": "546"
            },
            "women\u002Fclearance": {
                "title": "Clearance",
                "categoryId": "610"
            },
            "women\u002Fclearance\u002Ffootwear": {
                "title": "Footwear",
                "categoryId": "6100"
            },
            "women\u002Fclearance\u002Ffootwear\u002Fflats": {
                "title": "Flats",
                "categoryId": "6111"
            },
            "women\u002Fclearance\u002Ffootwear\u002Fheels": {
                "title": "Heels",
                "categoryId": "6112"
            },
            "women\u002Fclearance\u002Ffootwear\u002Fsneakers": {
                "title": "Sneakers",
                "categoryId": "6118"
            },
            "women\u002Fclearance\u002Ffootwear\u002Fsandals": {
                "title": "Sandals",
                "categoryId": "612"
            },
            "women\u002Fclearance\u002Ffootwear\u002Fboots": {
                "title": "Boots",
                "categoryId": "613"
            },
            "women\u002Fclearance\u002Fhandbags": {
                "title": "Handbags",
                "categoryId": "634"
            },
            "women\u002Fcollections": {
                "title": "Collections",
                "categoryId": "3000"
            },
            "women\u002Fcollections\u002Fspecial-occasion": {
                "title": "Special occasion",
                "categoryId": "3400"
            },
            "women\u002Fcollections\u002Fonline-exclusive": {
                "title": "Online exclusive",
                "categoryId": "3600"
            },
            "women\u002Fcollections\u002Fbest-sellers": {
                "title": "Best sellers",
                "categoryId": "3700"
            },
            "women\u002Fcollections\u002Fdisney": {
                "title": "Disney",
                "categoryId": "3800"
            },
            "women\u002Fcollections\u002Fsustainable-footwear": {
                "title": "Sustainable footwear",
                "categoryId": "5305"
            },
            "women\u002Fcollections\u002Fvalentines-day-collection": {
                "title": "valentines day collection",
                "categoryId": "71278"
            },
            "women\u002Fcollections\u002Fblack-friday-must-haves": {
                "title": "black friday must haves",
                "categoryId": "71267"
            },
            "women\u002Fcollections\u002Fpre-order": {
                "title": "Pre-Order",
                "categoryId": "9000"
            },
            "women\u002Fcollections\u002Fthe-holiday-shop": {
                "title": "The Holiday Shop",
                "categoryId": "72126"
            },
            "women\u002Fcollections\u002Fthe-gift-shop": {
                "title": "The Gift Shop",
                "categoryId": "72127"
            },
            "women\u002Fcollections\u002Fclear-heels": {
                "title": "Clear heels",
                "categoryId": "4600"
            },
            "women\u002Fcollections\u002Fsnakeskin-print": {
                "title": "Snakeskin print",
                "categoryId": "4700"
            },
            "women\u002Fcollections\u002Fnudes-neutrals": {
                "title": "Nudes neutrals",
                "categoryId": "4800"
            },
            "women\u002Fcollections\u002Fsquare-toe-shoes": {
                "title": "Square toe shoes",
                "categoryId": "5300"
            },
            "women\u002Fcollections\u002Fbright-colors": {
                "title": "Bright colors",
                "categoryId": "5302"
            },
            "women\u002Fcollections\u002Fquilted-woven": {
                "title": "Quilted woven",
                "categoryId": "5303"
            },
            "women\u002Fcollections\u002Fmetal-hardware": {
                "title": "Metal hardware",
                "categoryId": "5306"
            },
            "women\u002Fcollections\u002F90s-fashion": {
                "title": "90s Fashion",
                "categoryId": "71268"
            },
            "women\u002Fcollections\u002Fpastels": {
                "title": "Pastels",
                "categoryId": "71258"
            },
            "women\u002Fcollections\u002Fmatching-shoes-bags": {
                "title": "Matching shoes bags",
                "categoryId": "5310"
            },
            "women\u002Fcollections\u002Fglitter": {
                "title": "Glitter",
                "categoryId": "71199"
            },
            "women\u002Fcollections\u002Fnovelty-handbags-and-accessories": {
                "title": "Novelty handbags and accessories",
                "categoryId": "71400"
            },
            "women\u002Fcollections\u002Fpatent": {
                "title": "Patent",
                "categoryId": "71401"
            },
            "women\u002Fcollections\u002Fcomfy-and-cozy-shoes": {
                "title": "Comfy and cozy shoes",
                "categoryId": "71402"
            },
            "women\u002Fcollections\u002Fy2k-shoes-bags": {
                "title": "y2k shoes bags",
                "categoryId": "71404"
            },
            "women\u002Fcollections\u002Fsummer-nights-essentials": {
                "title": "Summer nights essentials",
                "categoryId": "73402"
            },
            "women\u002Fcollections\u002Ftravel-essentials": {
                "title": "Travel essentials",
                "categoryId": "73403"
            },
            "women\u002Fcollections\u002Fgreenwald": {
                "title": "Greenwald",
                "categoryId": "71259"
            },
            "women\u002Fcollections\u002Fdalsby": {
                "title": "Dalsby",
                "categoryId": "71260"
            },
            "women\u002Fcollections\u002Firidescent-metallics": {
                "title": "Iridescent metallics",
                "categoryId": "4200"
            },
            "women\u002Fcollections\u002Fluxe-collection": {
                "title": "Luxe Collection",
                "categoryId": "357"
            },
            "women\u002Fcollections\u002Fplatform-shoes": {
                "title": "Platform Shoes ",
                "categoryId": "71405"
            },
            "women\u002Fcollections\u002Fsummer-days-essentials": {
                "title": "Summer days essentials",
                "categoryId": "73401"
            },
            "women\u002Fcollections\u002Fstocking-stuffers": {
                "title": "Stocking Stuffers",
                "categoryId": "72129"
            },
            "women\u002Fcollections\u002Fwestern-and-cowboy-boots": {
                "title": "Western and cowboy boots",
                "categoryId": "71406"
            },
            "women\u002Fworkwear": {
                "title": "Workwear",
                "categoryId": "400"
            },
            "women\u002Fstep-into-love": {
                "title": "Step Into Love",
                "categoryId": "410"
            },
            "women\u002Fstep-into-love\u002Frefreshed-street-style": {
                "title": "Refreshed Street Style",
                "categoryId": "411"
            },
            "women\u002Fstep-into-love\u002Fsee-and-be-seen": {
                "title": "See and Be Seen",
                "categoryId": "412"
            },
            "women\u002Fstep-into-love\u002Fexplore-mode-on": {
                "title": "Explore Mode On",
                "categoryId": "413"
            },
            "women\u002Fstep-into-love\u002Fedgy-style-savantes": {
                "title": "Edgy Style Savantes",
                "categoryId": "414"
            },
            "women\u002Fstep-into-love\u002Ftrending-now": {
                "title": "Trending Now",
                "categoryId": "415"
            },
            "women\u002Fregular-price": {
                "title": "Regular Price",
                "categoryId": "430"
            },
            "women\u002Fregular-price\u002Ffootwear": {
                "title": "Footwear",
                "categoryId": "4101"
            },
            "women\u002Fregular-price\u002Ffootwear\u002Fflats": {
                "title": "Flats",
                "categoryId": "4102"
            },
            "women\u002Fregular-price\u002Ffootwear\u002Fheels": {
                "title": "Heels",
                "categoryId": "4103"
            },
            "women\u002Fregular-price\u002Ffootwear\u002Fsneakers": {
                "title": "Sneakers",
                "categoryId": "4104"
            },
            "women\u002Fregular-price\u002Ffootwear\u002Fboots": {
                "title": "Boots",
                "categoryId": "4105"
            },
            "women\u002Fregular-price\u002Ffootwear\u002Fsandals": {
                "title": "Sandals",
                "categoryId": "4106"
            },
            "women\u002Fregular-price\u002Fhandbags": {
                "title": "Handbags",
                "categoryId": "4107"
            },
            "women\u002Fregular-price\u002Faccessories": {
                "title": "Accessories",
                "categoryId": "4108"
            },
            "women\u002Fpromotions": {
                "title": "Promotions",
                "categoryId": "540"
            },
            "men": {
                "title": "Men",
                "categoryId": "200"
            },
            "men\u002Fnew-arrivals": {
                "title": "New arrivals",
                "categoryId": "2001"
            },
            "men\u002Fnew-arrivals\u002Ffootwear": {
                "title": "Footwear",
                "categoryId": "201"
            },
            "men\u002Fnew-arrivals\u002Fbags-accessories": {
                "title": "Bags & accessories",
                "categoryId": "3201"
            },
            "men\u002Ffootwear": {
                "title": "Footwear",
                "categoryId": "2000"
            },
            "men\u002Ffootwear\u002Fsneakers": {
                "title": "Sneakers",
                "categoryId": "211"
            },
            "men\u002Ffootwear\u002Fsneakers\u002Fhigh-top": {
                "title": "High Top",
                "categoryId": "72025"
            },
            "men\u002Ffootwear\u002Fsneakers\u002Flow-top": {
                "title": "Low top",
                "categoryId": "72026"
            },
            "men\u002Ffootwear\u002Fsneakers\u002Fslip-ons": {
                "title": "Slip-ons",
                "categoryId": "72027"
            },
            "men\u002Ffootwear\u002Fsneakers\u002Fwhite-sneakers-for-men": {
                "title": "White sneakers for men",
                "categoryId": "72355"
            },
            "men\u002Ffootwear\u002Fsneakers\u002Fathletic-sneakers": {
                "title": "Athletic sneakers",
                "categoryId": "72029"
            },
            "men\u002Ffootwear\u002Fdress-shoes": {
                "title": "Dress shoes",
                "categoryId": "221"
            },
            "men\u002Ffootwear\u002Fcasual-shoes": {
                "title": "Casual shoes",
                "categoryId": "222"
            },
            "men\u002Ffootwear\u002Fsandals": {
                "title": "Sandals",
                "categoryId": "220"
            },
            "men\u002Ffootwear\u002Fsandals\u002Fslides": {
                "title": "Slides",
                "categoryId": "2203"
            },
            "men\u002Ffootwear\u002Fsandals\u002Fflip-flops": {
                "title": "Flip Flops",
                "categoryId": "2204"
            },
            "men\u002Ffootwear\u002Fboots": {
                "title": "Boots",
                "categoryId": "230"
            },
            "men\u002Ffootwear\u002Fboots\u002Fcasual-boots": {
                "title": "Casual boots",
                "categoryId": "231"
            },
            "men\u002Ffootwear\u002Fboots\u002Fdress-boots": {
                "title": "Dress boots",
                "categoryId": "232"
            },
            "men\u002Ffootwear\u002Fboots\u002Fwinter-boots": {
                "title": "Winter boots",
                "categoryId": "233"
            },
            "men\u002Ffootwear\u002Fboots\u002Fchelsea-boots": {
                "title": "Chelsea boots",
                "categoryId": "7288"
            },
            "men\u002Ffootwear\u002Fboots\u002Flace-up-boots": {
                "title": "lace up boots",
                "categoryId": "7289"
            },
            "men\u002Ffootwear\u002Fboots\u002Fchukka-boots": {
                "title": "Chukka boots",
                "categoryId": "236"
            },
            "men\u002Ffootwear\u002Floafers-and-slip-ons": {
                "title": "Loafers and slip ons",
                "categoryId": "212"
            },
            "men\u002Ffootwear\u002Foxfords-and-lace-ups": {
                "title": "Oxfords and lace ups",
                "categoryId": "213"
            },
            "men\u002Ffootwear\u002Fslippers-and-clogs": {
                "title": "Slippers and clogs",
                "categoryId": "218"
            },
            "men\u002Ffootwear\u002Fespadrilles": {
                "title": "Espadrilles",
                "categoryId": "217"
            },
            "men\u002Fshoe-care": {
                "title": "shoe care",
                "categoryId": "332"
            },
            "men\u002Fbags-accessories": {
                "title": "Bags & accessories",
                "categoryId": "320"
            },
            "men\u002Fbags-accessories\u002Fbags-wallets": {
                "title": "bags wallets",
                "categoryId": "250"
            },
            "men\u002Fbags-accessories\u002Fbags-wallets\u002Fwallets": {
                "title": "Wallets",
                "categoryId": "251"
            },
            "men\u002Fbags-accessories\u002Fbelts": {
                "title": "Belts",
                "categoryId": "327"
            },
            "men\u002Fbags-accessories\u002Fjewelry": {
                "title": "Jewelry",
                "categoryId": "325"
            },
            "men\u002Fbags-accessories\u002Fjewelry\u002Frings": {
                "title": "Rings",
                "categoryId": "326"
            },
            "men\u002Fbags-accessories\u002Fhats-gloves-scarves": {
                "title": "Hats, gloves & scarves",
                "categoryId": "323"
            },
            "men\u002Fbags-accessories\u002Fhats-gloves-scarves\u002Fhats": {
                "title": "Hats",
                "categoryId": "3231"
            },
            "men\u002Fbags-accessories\u002Fhats-gloves-scarves\u002Fscarves": {
                "title": "Scarves",
                "categoryId": "3232"
            },
            "men\u002Fbags-accessories\u002Fhats-gloves-scarves\u002Fgloves": {
                "title": "Gloves",
                "categoryId": "3234"
            },
            "men\u002Fbags-accessories\u002Fsunglasses": {
                "title": "Sunglasses",
                "categoryId": "321"
            },
            "men\u002Fbags-accessories\u002Fsunglasses\u002Fsignature": {
                "title": "Signature",
                "categoryId": "3212"
            },
            "men\u002Fbags-accessories\u002Fsunglasses\u002Faviator": {
                "title": "Aviator",
                "categoryId": "3213"
            },
            "men\u002Fbags-accessories\u002Fsunglasses\u002Fround": {
                "title": "Round",
                "categoryId": "3214"
            },
            "men\u002Fbags-accessories\u002Fsunglasses\u002Fsquare": {
                "title": "Square",
                "categoryId": "3215"
            },
            "men\u002Fbags-accessories\u002Fsunglasses\u002Fshield": {
                "title": "Shield",
                "categoryId": "3216"
            },
            "men\u002Fbags-accessories\u002Fsunglasses\u002Faccessories": {
                "title": "Accessories",
                "categoryId": "3217"
            },
            "men\u002Fbags-accessories\u002Fsunglasses\u002Frectangle": {
                "title": "Rectangle",
                "categoryId": "3141"
            },
            "men\u002Fbags-accessories\u002Fwatches": {
                "title": "Watches",
                "categoryId": "322"
            },
            "men\u002Fbags-accessories\u002Fsocks": {
                "title": "Socks",
                "categoryId": "328"
            },
            "men\u002Fbags-accessories\u002Fcaps": {
                "title": "Caps",
                "categoryId": "7350"
            },
            "men\u002Fsale": {
                "title": "Sale",
                "categoryId": "520"
            },
            "men\u002Fsale\u002Ffootwear": {
                "title": "Footwear",
                "categoryId": "5200"
            },
            "men\u002Fsale\u002Ffootwear\u002Fsneakers": {
                "title": "Sneakers",
                "categoryId": "5211"
            },
            "men\u002Fsale\u002Ffootwear\u002Fdress-shoes": {
                "title": "Dress shoes",
                "categoryId": "5221"
            },
            "men\u002Fsale\u002Ffootwear\u002Fcasual-shoes": {
                "title": "Casual shoes",
                "categoryId": "5222"
            },
            "men\u002Fsale\u002Ffootwear\u002Fsandals": {
                "title": "Sandals",
                "categoryId": "522"
            },
            "men\u002Fsale\u002Ffootwear\u002Fboots": {
                "title": "Boots",
                "categoryId": "523"
            },
            "men\u002Fsale\u002Fbags-accessories": {
                "title": "Bags & accessories",
                "categoryId": "532"
            },
            "men\u002Fsale\u002Fbags-wallets": {
                "title": "Bags & wallets",
                "categoryId": "533"
            },
            "men\u002Fsale\u002Faccessories": {
                "title": "Accessories",
                "categoryId": "535"
            },
            "men\u002Fsale\u002F40-to-50-off": {
                "title": "40 to 50 Off",
                "categoryId": "554"
            },
            "men\u002Fsale\u002F30-to-40-off": {
                "title": "30 to 40 off",
                "categoryId": "555"
            },
            "men\u002Fsale\u002F20-to-30-off": {
                "title": "20 to 30 off",
                "categoryId": "556"
            },
            "men\u002Fclearance": {
                "title": "Clearance",
                "categoryId": "620"
            },
            "men\u002Fclearance\u002Ffootwear": {
                "title": "Footwear",
                "categoryId": "6200"
            },
            "men\u002Fclearance\u002Ffootwear\u002Fsneakers": {
                "title": "Sneakers",
                "categoryId": "6211"
            },
            "men\u002Fclearance\u002Ffootwear\u002Fdress-shoes": {
                "title": "Dress shoes",
                "categoryId": "6221"
            },
            "men\u002Fclearance\u002Ffootwear\u002Fcasual-shoes": {
                "title": "Casual shoes",
                "categoryId": "6222"
            },
            "men\u002Fclearance\u002Ffootwear\u002Fsandals": {
                "title": "Sandals",
                "categoryId": "622"
            },
            "men\u002Fclearance\u002Ffootwear\u002Fboots": {
                "title": "Boots",
                "categoryId": "623"
            },
            "men\u002Fonline-exclusive": {
                "title": "Online exclusive",
                "categoryId": "7257"
            },
            "men\u002Fcollections": {
                "title": "Collections",
                "categoryId": "5000"
            },
            "men\u002Fcollections\u002Fspecial-occasion": {
                "title": "Special occasion",
                "categoryId": "5700"
            },
            "men\u002Fcollections\u002Fbest-sellers": {
                "title": "Best sellers",
                "categoryId": "5800"
            },
            "men\u002Fcollections\u002Fsustainable-footwear": {
                "title": "Sustainable footwear",
                "categoryId": "5901"
            },
            "men\u002Fcollections\u002Fvalentines-day-collection": {
                "title": "valentines day collection",
                "categoryId": "72367"
            },
            "men\u002Fcollections\u002Fmr-b": {
                "title": "Mr B",
                "categoryId": "240"
            },
            "men\u002Fcollections\u002Fblack-friday-must-haves": {
                "title": "Black friday must haves",
                "categoryId": "72123"
            },
            "men\u002Fcollections\u002Fweather-ready": {
                "title": "Weather ready",
                "categoryId": "5902"
            },
            "men\u002Fcollections\u002Fpre-order": {
                "title": "Pre-Order",
                "categoryId": "9001"
            },
            "men\u002Fcollections\u002Fthe-holiday-shop": {
                "title": "The Holiday Shop",
                "categoryId": "72125"
            },
            "men\u002Fcollections\u002Fthe-gift-shop": {
                "title": "The Gift Shop",
                "categoryId": "72128"
            },
            "men\u002Fcollections\u002Fbright-colours": {
                "title": "Bright colours",
                "categoryId": "8002"
            },
            "men\u002Fcollections\u002Fdandy-loafers": {
                "title": "Dandy Loafers",
                "categoryId": "8003"
            },
            "men\u002Fcollections\u002Flugsole-boots": {
                "title": "Lugsole Boots",
                "categoryId": "72124"
            },
            "men\u002Fcollections\u002Fpastels": {
                "title": "Pastels",
                "categoryId": "72368"
            },
            "men\u002Fcollections\u002Fmetal-hardware": {
                "title": "Metal Hardware",
                "categoryId": "72369"
            },
            "men\u002Fcollections\u002Ftravel-essentials": {
                "title": "Travel essentials",
                "categoryId": "72200"
            },
            "men\u002Fcollections\u002Fsummer-days-essentials": {
                "title": "Summer days essentials",
                "categoryId": "72201"
            },
            "men\u002Fcollections\u002Fsummer-nights-essentials": {
                "title": "Summer nights essentials",
                "categoryId": "72202"
            },
            "men\u002Fcollections\u002Fjordan-fisher": {
                "title": "Jordan Fisher",
                "categoryId": "72400"
            },
            "men\u002Fstep-into-love": {
                "title": "Step Into Love",
                "categoryId": "9200"
            },
            "men\u002Fstep-into-love\u002Frefreshed-street-style": {
                "title": "Refreshed Street Style",
                "categoryId": "9201"
            },
            "men\u002Fstep-into-love\u002Fsee-and-be-seen": {
                "title": "See and Be Seen",
                "categoryId": "9202"
            },
            "men\u002Fstep-into-love\u002Fexplore-mode-on": {
                "title": "Explore Mode On",
                "categoryId": "9203"
            },
            "men\u002Fstep-into-love\u002Fedgy-style-savantes": {
                "title": "Edgy Style Savantes",
                "categoryId": "9204"
            },
            "men\u002Fstep-into-love\u002Ftrending-now": {
                "title": "Trending Now",
                "categoryId": "9205"
            },
            "men\u002Fpromotions": {
                "title": "Promotions",
                "categoryId": "550"
            },
            "men\u002Fpromotions\u002Fpromotional-exclusions": {
                "title": "Promotional Exclusions",
                "categoryId": "5904"
            },
            "men\u002Fregular-price": {
                "title": "Regular Price",
                "categoryId": "420"
            },
            "men\u002Fregular-price\u002Ffootwear": {
                "title": "Footwear",
                "categoryId": "4201"
            },
            "men\u002Fregular-price\u002Ffootwear\u002Fsneakers": {
                "title": "Sneakers",
                "categoryId": "4203"
            },
            "men\u002Fregular-price\u002Ffootwear\u002Fdress-shoes": {
                "title": "Dress shoes",
                "categoryId": "4204"
            },
            "men\u002Fregular-price\u002Ffootwear\u002Fcasual-shoes": {
                "title": "Casual shoes",
                "categoryId": "4205"
            },
            "men\u002Fregular-price\u002Ffootwear\u002Fsandals": {
                "title": "Sandals",
                "categoryId": "4206"
            },
            "men\u002Fregular-price\u002Ffootwear\u002Fboots": {
                "title": "Boots",
                "categoryId": "4207"
            },
            "men\u002Fregular-price\u002Fbags-wallets": {
                "title": "Bags & wallets",
                "categoryId": "4208"
            },
            "men\u002Fregular-price\u002Faccessories": {
                "title": "Accessories",
                "categoryId": "4209"
            },
            "men\u002Fworkwear": {
                "title": "Workwear",
                "categoryId": "9100"
            },
            "gift-cards": {
                "title": "Gift Cards",
                "categoryId": "999"
            },
            "shoe-care": {
                "title": "Shoe Care",
                "categoryId": "700"
            }
        }
        _, sub_category = url.rsplit("/", 1)
        sub_category = sub_category.replace("-", " ")
        for item in category_tree:
            if category_tree.get(item).get("title").lower() == sub_category.lower():
                return category_tree.get(item).get("categoryId")

    @classmethod
    def get_category_url(cls, url, current_page):
        cid = cls.get_category_id(url)
        if not cid:
            print(url)
            return False

        url_t = f"https://www.aldoshoes.com/api/products/category/{cid}"
        params = {
            "currentPage": current_page,
            "filters": "",
            "lang": cls.store_lang,
            "maxFilters": "7",
            "pageSize": "20",
            "region": cls.store_region,
            "showComingSoon": "true",
            "showScarce": "false",
            "sort": "relevance",
        }
        url = cls.make_url_with_query(url_t, params)
        return url

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
                "current_page": 0,
            }
            target_url = self.get_category_url(url, 0)
            if target_url:
                yield scrapy.Request(target_url, meta=meta, callback=self.parse_product_list,
                                     errback=self.start_request_error, dont_filter=True, headers=self.category_header)

    def parse_product_list(self, response, **kwargs):

        product_info = response.json()
        for item in product_info.get("products"):
            detail_url = self.base_url + item.get("url").replace("//", '/')
            item_data = {
                "category_name": response.meta.get("category_name", ""),
                "detail_url": detail_url,
                "referer": response.meta.get("referer"),
                "page_url": response.url,
                "meta": response.meta,
                "callback": self.parse_product_detail,
            }

            for task in self.request_product_detail(**item_data):
                yield task

        if (pagination := product_info.get('pagination')) and pagination.get('currentPage') < pagination.get(
                'totalPages'):
            params = self.get_url_params(response.url)
            params["currentPage"] = pagination.get('currentPage') + 1
            next_url = self.make_url_with_query(self.get_base_url(response.url), params)
            yield scrapy.Request(next_url, meta=response.meta, callback=self.parse_product_list,
                                 headers=self.category_header, errback=self.start_request_error)

    def parse_product_detail(self, response):
        color_xpath = '//span[@class="c-product-option__label-current-selection"]/text()'
        title_xpath = '//h2[@class="c-heading c-buy-module__product-title"]/span/text()'
        image_xpath = '//meta[@property="og:image"]'
        size_xpath = '//div[@class="c-product-option-list__list-item-wrapper"]/li'
        price_xpath = '//span[@class="c-product-price__formatted-price"]/text()'
        desc_price_xpath = '//span[@class="c-product-price__formatted-price c-product-price__formatted-price--is-reduced"]/text()'
        desc_xpath = '//div[@class="c-read-more c-product-description__section-content"]'
        title = response.xpath(title_xpath).get()
        _, sku = response.url.rsplit("/", 1)
        price = response.xpath(price_xpath).get() or response.xpath(desc_price_xpath).get()
        price = price.strip().strip("$")
        description = response.xpath(desc_xpath).get()
        color = response.xpath(color_xpath).get()

        images = []
        if nodes := response.xpath(image_xpath):
            for item in nodes:
                src = item.attrib.get("content").replace("_2000x2000", "_1200x1200")
                images.append(src)

        sizes = []
        if nodes := response.xpath(size_xpath):
            for item in nodes:
                src = item.attrib.get("aria-label")
                sizes.append(src)

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
            "brand": "Aldo"
        }

        yield ProductDetailItem(**item_data)
