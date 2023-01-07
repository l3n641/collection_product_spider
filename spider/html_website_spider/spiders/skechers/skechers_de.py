from .skechers import SkechersSpider


class SkechersDeSpider(SkechersSpider):
    name = 'skechers_de'
    allowed_domains = ['skechers.com', 'skechers.de']

    base_url = 'https://www.skechers.de'

    product_list_url = 'https://www.skechers.de/on/demandware.store/Sites-DESkechers-Site/de_DE/Product-Variation'

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
        "cookie": 'dwac_efbc4a0c63c6371fa933e7ebf7=bAJNUr1yMW3yvcq7IOZl9U_IDWDzWzR0p2Y=|dw-only|||EUR|false|Europe/Berlin|true; cqcid=abiAKtO80WsonuJV0lthmlfDFS; cquid=||; sid=bAJNUr1yMW3yvcq7IOZl9U_IDWDzWzR0p2Y; dwanonymous_a2e6b27a48916c35aae55fa9e1655b35=abiAKtO80WsonuJV0lthmlfDFS; __cq_dnt=0; dw_dnt=0; dwsid=IT8d8XzAG3LX675N68aTaAL1XcMy6R5rgjBtqyDI1BGseMoVJYjlLjO_7sY-WhmAVvGXMdyCxmFlGO2_YcDMUg==; _pxhd=rlxFonvTE3770AJsVek4a80yi31f005v-ZjMQd10M6e5GXT0txphVQ3eGuHYDC599wU5COegzud2Zm-VEOe9rg==:LrsX8wMonS9fxHbPJAy03/3rWALPyKsGD5jvQJK2C9SedInh-SeUWuuDWJ6LwA6leMbPUORI3pFqc6454cUDpq8mn/SoEvDjCmMeJJcC2fk=; _gcl_au=1.1.1754624850.1664455059; _ga=GA1.2.1977128427.1664455060; _gid=GA1.2.1352138900.1664455060; notice_behavior=implied,eu; __cq_uuid=ac7nagoJT4oSAZhG1oKW9Eaw4X; notice_preferences=2:; notice_gdpr_prefs=0,1,2:; cmapi_gtm_bl=; cmapi_cookie_privacy=permit 1,2,3; _fbp=fb.1.1664455063517.1565265572; __ruid=45123876-vg-o1-4j-1p-s91zrbujdbzptjkc0z3b-1664455068917; __rcmp=0!bj1fZ2MsZj1nYyxzPTEsYz0zMTgzLHRyPTEwMCxybj0zMjMsdHM9MjAyMjA5MjkuMTIzNyxkPXBjO249c2IxLGY9c2Iscz0xLGM9MjQ1Nix0PTIwMTkxMTA3LjEwMDA7bj1zcDEsZj1zcCxzPTEsYz0yNDU2LHQ9MjAxOTExMDcuMTAwMA~~; QuantumMetricUserID=f42f1100450e40fbf210548ba4403367; __pr.pwbujo=hyQcDC8nBJ; _px_f394gi7Fvmc43dfg_user_id=NmZhZTkzMTAtM2ZmNi0xMWVkLWJmZmItYzdjYTFjNzIyOTc1; pxcts=6fae57ee-3ff6-11ed-a609-414b4d456c4d; _pxvid=7fc75f6a-3ff3-11ed-9dbb-6f73446a4847; __cq_bc={"bdcn-DESkechers":[{"id":"405036L","sku":"195204892824"},{"id":"406043L","type":"vgroup","alt_id":"406043L_RDBK"}]}; __cq_seg=0~0.15!1~-0.06!2~0.43!3~-0.53!4~0.30!5~0.00!6~0.30!7~0.52!8~-0.04!9~-0.22!f0~15~10; cto_bundle=2o_vTF93Vjh6NVgyTUVxTUVFRFl6RmdXN1VMNE43NG1qZE9ZbU9aNjZWRzE3TnNjTm5sSjlwRER2eGV4MUdNZU1JZnI2azZFcFBQUURZemclMkJWemdiZmo2ZjdwYm4zQ3NoaTIyVXJWT3VmczNjejR6cGZuV0dQcVJBMjk0bjhGQ1ZzeSUyRmklMkJtQld4c3BKVkRRMnZldGlLVU9hWFElM0QlM0Q; __rutma=45123876-vg-o1-4j-1p-s91zrbujdbzptjkc0z3b-1664455068917.1664455068917.1664455068917.1.6.6; __cf_bm=gsGmNfh91lDH76vrXT3Eyk_ng9hzCl7FVVlHUniQQWI-1664464904-0-AWlkgM619wRruq0yAcSMKFtEf9JvmGaJQ1asBtevJb1crPUbOMTWw3izmIIsisLdoCR6K7+KqSYOS8W83EnicbM='
    }
