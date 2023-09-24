import requests
import pandas as pd
import re
# url = "http://jy.ggj.huainan.gov.cn/jyxx/012001/012001012/012001012001/20230830/f540c6ac-e5e7-4306-bbfc-edc92ea65bab-1KB.html"
"""
淮南市开标记录表下载
执行操作：
    1、下载解析页面开标记录信息
    2、筛除没有报价的单位
    3、计算下浮率
    4、按照下浮率升序排序
    5、保存文件为：“淮南项目开标记录.xlsx”文件
"""



url = input("url:")
payload = {}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)
#
html_text = response.text

del_label = re.compile(r'<[^>]+>', re.S)
re_ul = re.compile("<ul class='tabel'>([\s\S]*?)</ul>", re.IGNORECASE)
re_li = re.compile('<li[^>]*>[\s\S]*?<\/li>', re.IGNORECASE)
re_span = re.compile('<span[^>]*>[\s\S]*?</span>', re.IGNORECASE)

tables = re_ul.findall(html_text)

table_text = []
for row in re_li.findall(tables[0]):
    table_text.append([])
    for col in re_span.findall(row):
        s = del_label.sub("", re.sub("\s", '', col))
        if re.findall('投标单位', s) and len(s) <= 10:
            s = '投标单位名称'
            table_text = table_text[-1:]
        table_text[-1].append(s)
    if not table_text[-1]:
        table_text = table_text[:-1]
df = pd.DataFrame(table_text[1:],columns=['序号','投标单位名称','投标报价','工期'])
df = df[df['投标报价']!= '']



# zbkzj = 14789847.96
zbkzj = float(input('招标控制价：'))
df['下浮率'] = df['投标报价'].apply(lambda x:100-100*float(x)/zbkzj)
df.sort_values(by=['下浮率'],inplace=True)
df.to_excel('淮南项目开标记录.xlsx',index=False)