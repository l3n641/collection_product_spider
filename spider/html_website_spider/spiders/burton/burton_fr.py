from .burton import BurtonSpider


class BurtonFrSpider(BurtonSpider):
    name = 'burton_fr'
    category_url = "https://www.burton.com/fr/fr"
    detail_url = "https://www.burton.com/on/demandware.store/Sites-Burton_EUR-Site/fr_FR/Product-Variation?dwvar_{}_variationColor={}&pid={}&quantity=1"
