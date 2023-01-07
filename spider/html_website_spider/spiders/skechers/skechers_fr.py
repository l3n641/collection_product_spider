from .skechers import SkechersSpider


class SkechersFrSpider(SkechersSpider):
    name = 'skechers_fr'
    allowed_domains = ['skechers.com', 'skechers.fr']

    base_url = 'https://www.skechers.fr'

    product_list_url = 'https://www.skechers.fr/on/demandware.store/Sites-FRSkechers-Site/fr_FR/Product-Variation'

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
        "cookie": '_pxhd=mmUkK5u4X1ET4HlMlPY3dJdI7uW4gkyNYIdPskJlqj3nykVpr5Hjgx8eAric4tUWnrD16xBUVE9L4eH6OvwJ2g==:lzmvvsKWoRsXRXgGVspZpMiChT/MJ34IyqL9WjLFWhgYvThmXO4W/TwZUxAbbDJOR7CwPN4UBBVohOV/7bAW5r-rHXVbT4QSqLIAY58Po1s=; _px_f394gi7Fvmc43dfg_user_id=NTI0ODZhMjAtM2VkZi0xMWVkLWIwY2YtMDMwMjg5OTE4Mjg3; pxcts=524a8068-3edf-11ed-b2b6-4b4f48557866; _pxvid=50d402ff-3edf-11ed-b0bf-5071546e5267; _pxff_rf=1; _pxff_fp=1; _px3=36e157879377092bc574f88f310a9018ea8f16ba1ab9110d41314f177dfea923:tWcZo15jKDVfbuHMZJxnYtkzoV4hHLPEpO0HRc9OOh+kHQ0Nn15GqPtCslaDaV9Q02NTk9byObxRS2yMOutjtA==:1000:G4w5D/ggk81SYj9AnnaCDDLu95yMGCjeVkwlseHOAqFNwijr6tjwn/MImZgC99oHWXm5fI0UQI30RrpjhGvRglAZl4fdYAjhuE1Ox0IRlYfd/VVjkfnxxzKUyNIRrV0KhvV9kA2Z2SVFQg3C5lIs+442hXN8s67rgp3BhUl/u8z72ASU4992pXmK0W/QbcgUn46V4B85UCuZRTS0zqI6oA==; dwac_3e4d2959e167d96b68caf98c57=dxoE2mvG66Nzphu8_ymgXKlfm2Rt9HKHfaM=|dw-only|||EUR|false|Europe/Rome|true; cqcid=aby3aLW7ykG3G3RwqIBDmoEosn; cquid=||; sid=dxoE2mvG66Nzphu8_ymgXKlfm2Rt9HKHfaM; dwanonymous_d6b94ec41ff1f04493ceaf2ce5504ffb=aby3aLW7ykG3G3RwqIBDmoEosn; __cq_dnt=0; dw_dnt=0; dwsid=Zkiu2SDu0vfvzSUQlhiEwrgNMWcm3EvT4cj9vVkCptSIHUkkAizCb4Rr2vGvxcqAhBVRDoh4dBrI4v8D2z7zIw=='
    }
