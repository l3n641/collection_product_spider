class SizeGuide(object):
    default_size_chart = {
        "women": {
            "upper_part": ["34/XXS", "36/XS", "38/S", "40/M", "42/L", "44/XL", "46/XXL"],  # 上装
            "lower_part": ["34", "36", "38", "40", "42", "44", "46"],  # 下装
            "glove": ["S", "M", "L"],  # 手套
            "ring": ["S", "M", "L"],  # 戒指
            "belt": ["XS", "S", "M", "L"],  # 腰带
            "footwear": ["35", "36", "37", "38", "39", "40", "41", "42"],  # 鞋
            "lingerie": ["XS", "S", "M", "L"],  # 内衣
        },
        "mens": {
            "upper_part": ["37", "38", "39", "40", "41", "42", "43", "44", "45"],
            "lower_part": ["38/30(S)", "40/31(M)", "42/32(L)", "44/34(L)", "46/36(XL)", "48/38(XL)", "50/40"],
            "glove": ["M", "L", "XL"],
            "belt": ["85", "90", "95", "100", "105"],
            "sock": ["10", "15"],
            "footwear": ["38", "39", "40", "41", "42", "43", "44", "45", "46"],
            "homewear": ["32/M", "34/L", "36/XL"],  # 家居服
        },
        "kids": {
            "upper_part": ["4", "5-6", "7-8", "9-10", "11-12", "13-14"],
            "sock": ["S (23-26)", "M (27-31)", "L (32-35)", "XL (36-39)"],  # 袜子
            "belt": ["S (4-6)", "M (8-10)", "L (12-14)"],
            "hat": ["M (4-6)", "L (8-10)", "XL (12-14)"],  # 帽子
            "footwear": ["32", "33", "34", "35", "36", "37", "38", "39"],
        }

    }

    @staticmethod
    def get_category(keyword):
        parent_category = {
            "womens": {
                "womens": "en",
                "damen": "de",
                "femme": "fr",
                "donna": "it",
                "mujer": "es",
                "dames": "nl",
                "kvinder": "dk",
                "mulher": "pt",
                "dam": "se",
            },
            "mens": {
                "mens": "us",
                "herren": "de",
                "homme": "fr",
                "uomo": "it",
                "hombre": "es",
                "heren": "nl",
                "mand": "dk",
                "homem": "pt",
                "dam": "herr",
            },
        }
        for category_name in parent_category:
            if keyword in parent_category.get(category_name).keys():
                return category_name
        return False

    @classmethod
    def get_default_size(cls, parent_category, sub_category):
        category = cls.default_size_chart.get(parent_category)
        if not category:
            return False

        return category.get(sub_category)

    @classmethod
    def get_size_name_list(cls):
        name_list = []
        for key in cls.default_size_chart:
            for sub_key in cls.default_size_chart.get(key):
                name_list.append(f"{key}->{sub_key}")

        return name_list


if __name__ == "__main__":
    category = SizeGuide.get_default_size('donna', "upper_part")
    print(category)
