import requests
import pandas as pd
import re
import time
import random
def request_text(url):
    '''
    get请求页面信息
    :param url:
    :return:
    '''
    # time.sleep(random.random())
    time.sleep(random.randint(1,4))
    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    #
    html_text = response.text
    return html_text
def get_bidders_list(text):
    '''
    获取开标记录中投标单位报价信息，返回为dataframe，并且去除报价为空的数据
    '''
    del_label = re.compile(r'<[^>]+>', re.S)
    re_ul = re.compile("<ul class='tabel'>([\s\S]*?)</ul>", re.IGNORECASE)
    re_li = re.compile('<li[^>]*>[\s\S]*?<\/li>', re.IGNORECASE)
    re_span = re.compile('<span[^>]*>[\s\S]*?</span>', re.IGNORECASE)

    tables = re_ul.findall(text)

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
    df = pd.DataFrame(table_text[1:], columns=['序号', '投标单位名称', '投标报价', '工期'])
    df = df[df['投标报价'] != '']
    return df

def get_extract_parameters(text):
    extract_parameters = re.findall('现场抽取系数.*?>(.*?)<',text)[0]
    if str.strip(extract_parameters) in ['0','/','\\']:
        return ''
    return str.strip(extract_parameters)