from .skechers import SkechersSpider


class SkechersNlSpider(SkechersSpider):
    name = 'skechers_nl'
    allowed_domains = ['skechers.com', 'skechers.nl']

    base_url = 'https://www.skechers.nl'

    product_list_url = 'https://www.skechers.nl/on/demandware.store/Sites-NLSkechers-Site/nl_NL/Product-Variation'

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
        "cookie": 'dwac_e155b801baace026ee0df644ae=t61S3fDgoHvoFCez_pz4t53p5ZD02Og48Dc=|dw-only|||EUR|false|Europe/Amsterdam|true; cqcid=abmbwAS1XHiuQkWZZRHdRYUnna; cquid=||; sid=t61S3fDgoHvoFCez_pz4t53p5ZD02Og48Dc; dwanonymous_eee68e23673a6d7eead6a84a5ebae386=abmbwAS1XHiuQkWZZRHdRYUnna; __cq_dnt=0; dw_dnt=0; dwsid=oHtxaf1H0RJum-Q08FXUYYo_xiT5f5lRdrj27TCRsTcmVgiXHXzmTMhZp_z2NB8h7_wZd7jzPAuatq1x6QHhvw==; _pxhd=rTmGTIQW2u-b1WuMX6g4/CUvRRzdpJDDKNc2v/z4vBOd1WxKSbzCUp9A-XsdzS1eq5VaiXXT2dK0sOsStmMcBA==:nOVcUzBgMu6wRyqcvXZoOGZEASC22ZaMSG3XHVBYcCk7C7-axWvKYYG6Jf3vZT8cmwcxFmg/apXpT8vWr6WHFgdu5Yi3DaHxVnOoQas4G08=; _gcl_au=1.1.2072747206.1665017758; _ga=GA1.2.1658900873.1665017758; _gid=GA1.2.1180639157.1665017758; notice_behavior=implied,eu; __cq_uuid=ac7nagoJT4oSAZhG1oKW9Eaw4X; __cq_seg=0~0.00!1~0.00!2~0.00!3~0.00!4~0.00!5~0.00!6~0.00!7~0.00!8~0.00!9~0.00; notice_preferences=0:; notice_gdpr_prefs=0:; cmapi_gtm_bl=ga-ms-ua-ta-asp-bzi-sp-awct-cts-csm-img-flc-fls-mpm-mpr-m6d-tc-tdc; cmapi_cookie_privacy=permit 1 required; __cq_bc={"bdcn-NLSkechers":[{"id":"302309L","type":"vgroup","alt_id":"302309L_MLT"}]}; __pr.xm1xt3=S3YMC_4GUI'
    }
