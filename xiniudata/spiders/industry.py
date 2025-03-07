import json
import os

import scrapy

# from xiniu_encrypt import get_payload_sig, get_answer
from xiniudata.xiniu_encrypt import get_answer,get_payload_sig

class IndustrySpider(scrapy.Spider):
    name = "industry"
    allowed_domains = ["www.xiniudata.com"]

    # start_urls = ["https://www.xiniudata.com/"]
    def start_requests(self):
        headers = {
            "accept": "application/json",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "cache-control": "no-cache",
            "content-type": "application/json",
            "origin": "https://www.xiniudata.com",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "referer": "https://www.xiniudata.com/industry/newest?from=data",
            "sec-ch-ua": "\"Not(A:Brand\";v=\"99\", \"Microsoft Edge\";v=\"133\", \"Chromium\";v=\"133\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0"
        }
        url = "https://www.xiniudata.com/api2/service/x_service/person_industry_list/list_industries_by_sort"
        for i in range(1, 4):
            k = i * 20
            payload_pro = {
                "sort": 1,
                "start": k,
                "limit": 20
            }
            payload_sig = get_payload_sig(payload_pro)
            payload = payload_sig['payload']
            sig = payload_sig['sig']
            data = {
                "payload": f"{payload}",
                "sig": f"{sig}",
                "v": 1
            }
            data = json.dumps(data, separators=(',', ':'))
            yield scrapy.Request(url=url, method="POST", headers=headers, body=data, callback=self.parse,
                                 meta=payload_pro)
        pass

    def parse(self, response):
        k = json.loads(response.text, strict=False)

        ans = get_answer(k)
        name_pre = response.meta["start"]
        name = f"{name_pre}-{name_pre + 20}_industry"

        if not os.path.exists("file"):
            os.makedirs("file")
        file_path = os.path.join("file", f"{name}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(ans, f, ensure_ascii=False, indent=4)
        print(f"Saved {file_path}")
        pass
