import html
import json
import re

import pandas as pd
import requests
import time
import random


def error_log(error):
    """
    记录错误
    :param error:
    :return:
    """
    with open('../error.log', 'a+', encoding='utf-8') as f:
        f.write(str(error))
        f.write('\n')


url = "https://lssggzy.lishui.gov.cn/jsearchfront/interfaces/search.do"

save_datas = []
for i in range(1, 3):
    print(f"页码：{i}".center(100, "*"))
    payload = f"_cus_lq_projectcode=&_cus_pq_title=&begin=&end=&_cus_lq_dljg=&_cus_lq_jyjf=&_cus_eq_author=&sortType=2&websiteid=331101000003826&tpl=1621&p={i}&pg=30&cateid=683&_cus_lq_regioncode=\r\n"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'user_sid=b444f4d52b1f4750b229900304913fd8; JSESSIONID=B98D5D1DD0866E8B4805149091B58E86; searchsign=02ad5f279cea4cb780e46ec2b1787b8e; searchid=6b159a3b20d844b38bface74f98d03d2; sid=d0918dd6ee376a8eccb02c1c53629061; _zcy_log_client_uuid=39835e80-0f38-11ee-b649-edb1f1e35ed8; SL_G_WPT_TO=zh-CN; arialoadData=false; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; SERVERID=3688718e51e69dcc5273b4c5cdc8398b|1689586827|1689586735',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }
    # 请求信息
    response = requests.request("POST", url, headers=headers, data=payload)
    # 解析请求结果
    text = response.text
    text = json.loads(text)
    # 遍历数据30条
    time.sleep(random.randint(0, 5))

    for d in text['dataResults']:
        save_data = []
        for name in ['projectcode', 'bidsectioncode', 'url', 'industriestype', 'regioncode', 'tendermode']:
            try:
                save_data.append(d['data'][name])
            except Exception as e:
                save_data.append('')
                error_log(str(e))
        projectcode, projectname, projecturl = save_data[:3]

        try:
            project_html = html.unescape(d['data']['bu11etincontent'])
        except Exception as e:
            error_log(str(e))
            continue
        '''获取基准价和下浮率 '''
        print(projecturl)
        rate = 0
        price = 0
        del_label = re.compile(r'<[^>]+>', re.S)
        project_str = del_label.sub("", project_html)
        # print(project_str)
        # x = re.match('.*?下浮.*?(\d*\.\d*|\d*)%.*?',project_str).groups()[0]
        if re.findall('下浮[^\d]{0,3}(\d*\.\d*|\d*)%', project_str):
            rate = re.findall('下浮[^\d]{0,3}(\d{1,2}\.\d*|\d{0,2})%', project_str)[0]
            rate = float(rate) if rate else 0
        if re.findall('基准[^\d]{0,2}(\d*\.\d*|\d*)', project_str):
            price = re.findall('基准[^\d]{0,2}(\d*\.\d*|\d*)', project_str)[0]
            price = float(price) if price else 0
        print(rate, price)

        # 获取投标人数量
        del_label = re.compile(r'<[^>]+>', re.S)
        re_table = re.compile('<table[^>]*>[\s\S]*?<\/table>', re.IGNORECASE)
        re_tr = re.compile('<tr[^>]*>[\s\S]*?<\/tr>', re.IGNORECASE)
        re_td = re.compile('<t[hd][^>]*>[\s\S]*?</t[hd]>', re.IGNORECASE)

        tables = re_table.findall(project_html)
        max_len = 0
        for table in tables:
            table_text = []
            for row in re_tr.findall(table):
                table_text.append([])
                for col in re_td.findall(row):
                    s = del_label.sub("", re.sub("\s", '', col))
                    if re.findall('投标人|投标单位', s) and len(s) <= 10:
                        s = '投标单位名称'
                        table_text = table_text[-1:]
                    table_text[-1].append(s)
                if not table_text[-1]:
                    table_text = table_text[:-1]

            if '投标单位名称' in table_text[0]:
                col_index = table_text[0].index('投标单位名称')
                print(table_text)
                table_data = []

                for d in table_text:
                    # print(d)
                    if len(d) > col_index:
                        table_data.append(d[col_index])
                df = pd.DataFrame(data=table_data, columns=['投标单位名称'])
                # df = df[df['投标单位名称'].apply(lambda x: True if re.match(r".*?公司", str(x)) else False)]
                df = df[df['投标单位名称'].apply(lambda x: True if len(x) >= 7 else False)]

                df = df.fillna('')
                if len(df) > 0:
                    df = df[df['投标单位名称'] != '']
                    max_len = max(max_len, len(df))
                    print(max_len)

        save_data = [projectcode, projectname, projecturl, price / (1 - rate * 0.01), rate, price, max_len]
        if save_data not in save_datas:
            save_datas.append(save_data)
        else:
            print('程序完成！')
            break


df = pd.DataFrame(columns=['id', '项目名称', '网址', 'zbkzj', '下浮率', 'kbjj', '投标单位数量'], data=save_datas)
# df.to_csv('丽水市数据2023-10-30.csv', index=False, encoding='utf-8')

df.to_excel('丽水市数据2023-10-30.xlsx', index=False)

