import pandas as pd
import re
import requests

"""
丽水市开标记录表下载
执行操作：
    1、请求解析页面开标记录信息
    2、筛除没有报价的单位，只保留序号，单位，报价三个字段
    3、计算下浮率
    4、按照下浮率升序排序
    5、保存文件为：“丽水市项目开标记录.xlsx”文件
"""


# url = "https://lssggzy.lishui.gov.cn/art/2023/8/1/art_1229661852_221957.html"
url = input('url：')
payload = {}
headers = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
  'Accept-Encoding': 'gzip, deflate, br',
  'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,ar;q=0.6',
  'Cookie': 'SL_G_WPT_TO=zh-CN; arialoadData=false; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; SERVERID=57526053d080975751a9538d16dda0a7|1695345726|1695344488; SERVERID=57526053d080975751a9538d16dda0a7|1695346020|1695344488',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
}

response = requests.request("GET", url, headers=headers, data=payload)



project_html =response.content.decode('utf-8')


del_label = re.compile(r'<[^>]+>', re.S)
re_table = re.compile('<table[^>]*>[\s\S]*?<\/table>', re.IGNORECASE)
re_tr = re.compile('<tr[^>]*>[\s\S]*?<\/tr>', re.IGNORECASE)
re_td = re.compile('<t[hd][^>]*>[\s\S]*?</t[hd]>', re.IGNORECASE)

table = re_table.findall(project_html)[1]
max_len = 0

table_text = []
for row in re_tr.findall(table):
    table_text.append([])
    for col in re_td.findall(row):
        s = del_label.sub("", re.sub("\s", '', col))
        if re.findall('投标单位名称', s) and len(s) <= 10:
            s = '投标单位名称'
            table_text = table_text[-1:]
        table_text[-1].append(s)
    if not table_text[-1]:
        table_text = table_text[:-1]

df = pd.DataFrame(table_text[1:],columns=['序号', '投标单位名称', '投标报价', '工期（日历天）', '质量要求', '项目经理', '开标备注'])
df = df[['序号', '投标单位名称', '投标报价']]


zbkzj = float(input('招标控制价：'))
df['下浮率'] = df['投标报价'].apply(lambda x:100-100*float(x)/zbkzj)
df.sort_values(by=['下浮率'],inplace=True)

df.to_excel('丽水市项目开标记录.xlsx',index=False)

