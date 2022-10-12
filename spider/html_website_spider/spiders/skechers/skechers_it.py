from .skechers import SkechersSpider


class SkechersItSpider(SkechersSpider):
    name = 'skechers_it'
    allowed_domains = ['skechers.com', 'skechers.it']

    base_url = 'https://www.skechers.it'

    product_list_url = 'https://www.skechers.it/on/demandware.store/Sites-ITSkechers-Site/it_IT/Product-Variation'

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
        "cookie": 'dwac_85773c0ebbbfacceba165b42d6=wIX4RW-YkeWSEzx4QMnQ5YNjO6joQ9I47V8=|dw-only|||EUR|false|Europe/Rome|true; cqcid=abMoP8pAtxxF1qcfWhTIiViqLZ; cquid=||; dwanonymous_9573ca8ef4aae15b476c49add11f83b9=abMoP8pAtxxF1qcfWhTIiViqLZ; sid=wIX4RW-YkeWSEzx4QMnQ5YNjO6joQ9I47V8; __cq_dnt=0; dw_dnt=0; dwsid=91hhEXJIijdxaLH56IQFybS-ovz1k8nqDiRM6rGfexk19koANbVtGxsn97GfEN9f2d5nynaXHdvd7IIj14pP0w==; _pxhd=u4-E8HfFU2ZcCWwKVkavQe7sFxKfG3nlgGS4G0oDQFlcs5yzuqxLba234Wvyn3g/A8TOtVbSmH0nZ0QY2tsNAw==:WEZmsvacWu4/UCSCBwEz2CfzWPCF5kTjusFO2dQi2DzqmomY55CiMA6xK4wntoZMEpIeSeqxlBolAOQ4sMSVkh39EQCPiSOM8gOzIE4IAuo=; notice_behavior=implied,eu; __cq_uuid=ac7nagoJT4oSAZhG1oKW9Eaw4X; __cq_seg=0~0.00!1~0.00!2~0.00!3~0.00!4~0.00!5~0.00!6~0.00!7~0.00!8~0.00!9~0.00; notice_preferences=2:; notice_gdpr_prefs=0,1,2:; cmapi_gtm_bl=; cmapi_cookie_privacy=permit 1,2,3; _gcl_au=1.1.948666926.1664413319; _ga=GA1.2.15300210.1664413319; _gid=GA1.2.2141912641.1664413319; _fbp=fb.1.1664413319825.1905251187; QuantumMetricSessionID=94e477dd9030210e6a844e9f16ccd41b; QuantumMetricUserID=f42f1100450e40fbf210548ba4403367; email_acquisition_opt_in=false; _dc_gtm_UA-218234081-1=1; __cq_bc={"bdcn-ITSkechers":[{"id":"155229","type":"vgroup","alt_id":"155229_BKMT"}]}; __pr.fr3wbn=4E8gQE3XSz'
    }
