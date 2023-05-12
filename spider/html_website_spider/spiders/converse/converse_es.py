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
from .converse import ConverseSpider


class ConverseEsSpider(ConverseSpider):
    name = 'converse_es'
    allowed_domains = ['www.converse.com']
    BASE_URL = "https://www.converse.com/"
