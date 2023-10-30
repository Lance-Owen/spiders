import html
import json
import re
import datetime

import pandas as pd
import requests
import time
import random

t = datetime.datetime.now().strftime('%Y-%m-%d')

url = "https://search.zj.gov.cn/jsearchfront/interfaces/search.do"

save_datas = []
for i in range(1, 5):
    time.sleep(random.randint(1,3))
    print(f"页码：{i}".center(100, "*"))
    payload = f"_cus_lq_bidsectionname=&_cus_pq_title=&begin=&end=&_cus_lq_dljg=&_cus_lq_jyjf=&_cus_eq_author=&sortType=2&websiteid=331101000003826&tpl=1621&p={i}&pg=30&cateid=681&_cus_lq_regioncode="
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'user_sid=b444f4d52b1f4750b229900304913fd8; JSESSIONID=B98D5D1DD0866E8B4805149091B58E86; searchsign=02ad5f279cea4cb780e46ec2b1787b8e; searchid=6b159a3b20d844b38bface74f98d03d2; sid=d0918dd6ee376a8eccb02c1c53629061; _zcy_log_client_uuid=39835e80-0f38-11ee-b649-edb1f1e35ed8; SL_G_WPT_TO=zh-CN; arialoadData=false; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; SERVERID=3688718e51e69dcc5273b4c5cdc8398b|1689586827|1689586735; searchid=366fbad418fb44b8acfa239ebc953e4a; user_sid=3824807f3dc3414ca28e755f5f2ad1fe; SERVERID=daf947b71579cb2e324dcfdb35f0f984|1697698288|1697698288',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Content-Length': '181'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    # 解析请求结果
    text = response.text
    text = json.loads(text)
    # 遍历数据30条
    for d in text['dataResults']:
        save_data = []
        # ['项目名称','开标时间','工程类别','网址']
        for name in ['bidsectioncode', 'author', 'industriestype', 'url']:
            try:
                save_data.append(d['data'][name])
            except Exception as e:
                save_data.append('')
        save_datas.append(save_data)

df = pd.DataFrame(columns=['项目名称', '开标时间', '工程类别', '网址'], data=save_datas)
df.to_excel(f'丽水市招标公告信息{t}.xlsx', index=False)
