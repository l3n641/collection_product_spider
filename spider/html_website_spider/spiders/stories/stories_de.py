from .stories import StoriesSpider
import scrapy


class StoriesDeSpider(StoriesSpider):
    name = 'stories_de'
    allowed_domains = ['stories.com']
    base_url = "https://www.stories.com"
