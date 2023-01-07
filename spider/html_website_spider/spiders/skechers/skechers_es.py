from .skechers import SkechersSpider


class SkechersEsSpider(SkechersSpider):
    name = 'skechers_es'
    allowed_domains = ['skechers.com', 'skechers.es']

    base_url = 'https://www.skechers.es'

    product_list_url = 'https://www.skechers.es/on/demandware.store/Sites-ESSkechers-Site/es_ES/Product-Variation'

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
        "cookie": 'dwac_f4f20fd1cbe9d6913d5940e210=rWiuQYcaASWcy-eNgAtePOmPq7TXNjvpB2g=|dw-only|||EUR|false|Europe/Madrid|true; cqcid=abELY9vPUf1YsTvv5LZqqiLzGc; cquid=||; dwanonymous_2487cb117ca1a9375e02057354bb5c90=abELY9vPUf1YsTvv5LZqqiLzGc; sid=rWiuQYcaASWcy-eNgAtePOmPq7TXNjvpB2g; __cq_dnt=0; dw_dnt=0; dwsid=Ex7hYJhcfQyNhiDKPCvUn1f55JXIcEfAFiWh9eEgCekZYjw9eYkC_FKKu2fKQE_pS8MQMP-2SZn7bej_NMwVkA==; _pxhd=nir78vdAczMv5EDHDmYsiSooR335FcBAaecAa0qXvjq1ZJl7wqhMDsp/kO21dt3kDVWOruXv3DWsEG4FdC4bVA==:NZSrp7dfm4ykZKTAkAgXT6xcrr3ykIfX-F8Kz8l0z7PNSLSG2gcFOZrWgxfhysPMkz/es62THrgmBvuQzyctUdUgfsruL/X4tqY/6eD8Ejw=; _gcl_au=1.1.1519971260.1664479663; _ga=GA1.2.709484679.1664479663; _gid=GA1.2.1734474009.1664479663; _dc_gtm_UA-96017608-1=1; notice_behavior=implied,eu; __cq_uuid=ac7nagoJT4oSAZhG1oKW9Eaw4X; __cq_seg=0~0.00!1~0.00!2~0.00!3~0.00!4~0.00!5~0.00!6~0.00!7~0.00!8~0.00!9~0.00; notice_preferences=2:; notice_gdpr_prefs=0,1,2:; cmapi_gtm_bl=; cmapi_cookie_privacy=permit 1,2,3; _fbp=fb.1.1664479667484.1793167498; QuantumMetricSessionID=94e477dd9030210e6a844e9f16ccd41b; QuantumMetricUserID=f42f1100450e40fbf210548ba4403367; __rutmb=45123875; __ruid=45123875-hn-0t-4w-1p-pdwt0qt8zfrlx8wmdv6e-1664479682374; __rcmp=0!bj1fZ2MsZj1nYyxzPTEsYz03Mjg1LHRyPTEwMCxybj0yMix0cz0yMDIyMDkyOS4xOTI4LGQ9cGM7bj1zcDEsZj1zcCxzPTEsYz0yNDU1LHQ9MjAxOTExMDcuMDk1MztuPXNiMSxmPXNiLHM9MSxjPTI0NTQsdD0yMDE5MTEwNy4wOTUx; __rslct=sb,sp; _gat_rfk=1; __cq_bc={"bdcn-ESSkechers":[{"id":"232452","type":"vgroup","alt_id":"232452_BLK"}]}; __pr.3gago=2kEvmiQ3O0; __rutma=45123875-hn-0t-4w-1p-pdwt0qt8zfrlx8wmdv6e-1664479682374.1664479682374.1664479682374.1.2.2; __rpck=0!PTAhZXlKME55STZlMzBzSW5RM2RpSTZlMzBzSW1sMGFXMWxJam9pTWpBeU1qQTVNamt1TVRreU9DSXNJblE0SWpwN0lqRWlPakUyTmpRME56azJPRFV6TWpaOWZRfn4~; __rpckx=0!eyJ0NyI6eyIyIjoxNjY0NDc5Njg5OTk2fSwidDd2Ijp7IjIiOjE2NjQ0Nzk2ODk5OTZ9LCJpdGltZSI6IjIwMjIwOTI5LjE5MjgifQ~~'
    }
