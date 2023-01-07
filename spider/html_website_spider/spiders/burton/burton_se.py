from .burton import BurtonSpider


class BurtonSeSpider(BurtonSpider):
    name = 'burton_se'
    category_url = "https://www.burton.com/se/sv"
    detail_url = "https://www.burton.com/on/demandware.store/Sites-Burton_EUR-Site/sv_SE/Product-Variation?dwvar_{}_variationColor={}&pid={}&quantity=1"
