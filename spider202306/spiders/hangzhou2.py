import json
import requests
import pandas as pd
from lxml import etree
import time
import random
import re

def count_tender_num(project_html,find_col_name):
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
                if re.findall(find_col_name, s) and len(s) <= 10:
                    s = '投标单位名称'
                    table_text = table_text[-1:]
                table_text[-1].append(s)
            if not table_text[-1]:
                table_text = table_text[:-1]
        if '投标单位名称' in table_text[0]:
            col_index = table_text[0].index('投标单位名称')
            # print(table_text)
            df = pd.DataFrame(data=[d[col_index] if len(d) >= col_index + 1 else '' for d in table_text],
                                  columns=['投标单位名称'])
            # df = df[df['投标单位名称'].apply(lambda x: True if re.match(r".*?公司", str(x)) else False)]
            df = df[df['投标单位名称'].apply(lambda x: True if len(str(x).replace(' ', ''))>3 else False)]

            df = df.fillna('')
            if len(df) > 0:
                df = df[df['投标单位名称'] != '']
                max_len = max(max_len, len(df))
                # print(max_len)
                return max_len
            return 0
def get_open_project(url, id):
    payload = {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Content-Type': 'text/html; charset=utf-8'
    }
    response = requests.request("GET", url, headers=headers, data=payload)

    html = response.text
    extract_url = f"https://ggzy.hzctc.hangzhou.gov.cn/OpenBidRecord/OpenParamInfo?openRecordListID={id}"
    tender_num = count_tender_num(html, '投标企业')

    if '查看系数' in html:
        # extract_response = requests.request("GET", extract_url, headers=headers, data=payload)
        # extract_value = re.findall('<span id="([^"]*)">',extract_response.text)
        return extract_url,1, tender_num
    elif '参数抽取' in html:
        return '',2, tender_num
    else:
        return '', 0, tender_num
def get_project(url):
    payload = {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Content-Type': 'text/html; charset=utf-8'
    }
    del_label = re.compile(r'<[^>]+>', re.S)
    response = requests.request("GET", url, headers=headers, data=payload)
    names = ['工程名称', '项目编号', '开标时间', '工程分类', '是否联合体投标', '资格审查方式', '本期概算(万元)', '备注', '对投标人的承包资质要求', '从业人员资格要求']
    project_value = ['', '', '', '', '', '', '', '', '', '']
    try:
        # find_value_list = [[0,1,2], [0,3,2], [0,4,2], [0,8,4], [0,11,2], [1,4,2], [1,5,4], [1,6,2], [3,1,2], [3,2,2]]
        # find_value_list =[[2,2,1],[2,2,2],[2,2,3]]
        tables = re.findall('<table[\s\S]*?<\/table>',response.text)
        for table in tables:
            for tr in re.findall('<tr[\s\S]*?<\/tr>',table):
                tds = re.findall('<td[\s\S]*?<\/td>',tr)
                for i in range(len(tds)):
                    s = del_label.sub('', tds[i])
                    s = re.sub('\s','',s)
                    if s in names:
                        index = names.index(s)
                        s = del_label.sub('', tds[i+1])
                        s = re.sub('\n', '', s).replace('&nbsp;','').strip()

                        print(s)
                        project_value[index] = s
        return project_value
    except:
        print(url)
        return ''
        '''
        project_value = []
        for t in find_value_list:
            s = etree.HTML(table[t[0]]).xpath(f'//table[1]/tr[{t[1]}]/td[{t[2]}]//span')[0]
            s = etree.tostring(s,encoding='utf-8').decode('utf-8')
            del_label = re.compile(r'<[^>]+>',re.S)
            s = del_label.sub('',s)
            project_value.append(s)
            print(s)
        '''


data = pd.DataFrame()
# 遍历所有翻页数据
for page_num in range(1,99):
    print(f"当前获取第 {page_num} 页数据".center(100,"*"))
    # 获取当前时间戳
    millisecond_timestamp = round(time.time() * 1000)
    # 拼接获取每页项目信息的请求头和表单数据
    url = "https://ggzy.hzctc.hangzhou.gov.cn/SecondPage/GetNotice"
    payload = f"area=&afficheType=22&IsToday=&title=&proID=&number=&_search=false&nd={millisecond_timestamp}&rows=10&page={page_num}&sidx=PublishStartTime&sord=desc"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'HZSESSIONID=c7693883-1f26-4dc1-a90d-4c917203153d; SL_G_WPT_TO=zh-CN; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; ASP.NET_SessionId=x0poiuhv0ja5y3hs54roksej',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }
    # 请求数据，解析出项目列表信息
    response = requests.request("POST", url, headers=headers, data=payload)
    project_list = response.text
    project_list = json.loads(project_list)
    project_list = project_list['rows']
    # 遍历项目，拼接项目请求地址，获取项目网页信息，xpath获取参数抽取信息
    for project in project_list:
        ID = project['ID']
        # TenderID = project['TenderID']
        project_url = f"https://ggzy.hzctc.hangzhou.gov.cn/AfficheShow/Home?AfficheID={ID}&IsInner=0&IsHistory=&ModuleID=22"
        # project_url = "https://ggzy.hzctc.hangzhou.gov.cn/AfficheShow/Home?AfficheID=23b0e0fc-43a0-41dc-9993-ed0fd0f81e83&IsInner=0&IsHistory=&ModuleID=22"
        print(project_url)
        project_value = get_project(project_url)
        # if not project_value:
        #     project_value = ['']*10
        project_value.append(project_url)
        df = pd.DataFrame(data=[project_value], columns=['项目名称','项目编号','开标时间','工程分类','是否联合体投标','资格审查方式','预算','备注','企业资质','人员资质','招标公告网址'])
        data = pd.concat([data, df])
        time.sleep(random.randint(1,5))
# print(data)
data.drop_duplicates(inplace=True)
data.to_excel('杭州市招标公告项目信息2023-08-29.xlsx', index=False)
