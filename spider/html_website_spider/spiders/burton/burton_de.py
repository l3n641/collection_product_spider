from .burton import BurtonSpider


class BurtonDeSpider(BurtonSpider):
    name = 'burton_de'
    category_url = "https://www.burton.com/de/de"
    detail_url = "https://www.burton.com/on/demandware.store/Sites-Burton_EUR-Site/de_DE/Product-Variation?dwvar_{}_variationColor={}&pid={}&quantity=1"
