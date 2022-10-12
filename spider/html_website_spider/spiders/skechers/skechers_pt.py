from .skechers import SkechersSpider


class SkechersPtSpider(SkechersSpider):
    name = 'skechers_pt'
    allowed_domains = ['skechers.com', 'skechers.pt']

    base_url = 'https://www.skechers.pt'

    product_list_url = 'https://www.skechers.pt/on/demandware.store/Sites-PTSkechers-Site/pt_PT/Product-Variation'

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
        "cookie": 'dwac_94249b74a78f297eea1bda2ced=ZEoVLMER2dSTzYBRtgP-9au98KK-TZcGKHU=|dw-only|||EUR|false|Europe/Lisbon|true; cqcid=cdAOeZcxW9xiDXe7OR8mMffHab; cquid=||; sid=ZEoVLMER2dSTzYBRtgP-9au98KK-TZcGKHU; dwanonymous_272687b4862bfc19f634a0939e90927b=cdAOeZcxW9xiDXe7OR8mMffHab; __cq_dnt=0; dw_dnt=0; dwsid=Svkfl7Pm7lgWGjT5vxM3woUO-hnMuqCKraLHLfWfvkzH5skBonU8qdS5pg7g1i2kOq2jhsvNwZafmsXd5j0V1Q==; _pxhd=VECemas7IEgVSCLtHOb7-dF6Bx2CxCJMM0ZToC0rRQSOTU5QtGC8jXqhnVxqeTHuNIddTnPGNxsGuU/XNMU3Jg==:8iJ1-m2pbk7OiXuMSSO-zVJha6-vGeXo5GTlaBgtZN9O3afRZlLakH28yhdAIMiRdGXqoPx-sBUy8fsRegigteTAj0ruapV0D4sjNmkS-9M=; _gcl_au=1.1.1925681086.1664348113; _ga=GA1.2.751677090.1664348114; _gid=GA1.2.1892572866.1664348114; notice_behavior=implied,eu; __cq_uuid=ac7nagoJT4oSAZhG1oKW9Eaw4X; __cq_seg=0~0.00!1~0.00!2~0.00!3~0.00!4~0.00!5~0.00!6~0.00!7~0.00!8~0.00!9~0.00; notice_preferences=2:; notice_gdpr_prefs=0,1,2:; cmapi_gtm_bl=; cmapi_cookie_privacy=permit 1,2,3; _fbp=fb.1.1664348161151.1171969730; QuantumMetricSessionID=534517a622289bea72c62f4757d24e63; QuantumMetricUserID=f42f1100450e40fbf210548ba4403367; _dc_gtm_UA-217134986-1=1; __cq_bc={"bdcn-PTSkechers":[{"id":"232450"}]}; __pr.poy31e=HPE2oOUPKs'
    }
