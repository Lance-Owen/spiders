import json
import pandas as pd
import time
import random
from hangzhou import *

data = pd.DataFrame()
# 遍历所有翻页数据
for page_num in range(1, 99):
    print(f"当前获取第 {page_num} 页数据".center(100, "*"))
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
        project_url = f"https://ggzy.hzctc.hangzhou.gov.cn/AfficheShow/Home?AfficheID={ID}&IsInner=0&IsHistory=&ModuleID=22"
        print(project_url)
        project_value = get_tender_project(project_url)

        project_value.append(project_url)
        df = pd.DataFrame(data=[project_value],
                          columns=['项目名称', '项目编号', '开标时间', '工程分类', '是否联合体投标', '资格审查方式',
                                   '预算', '备注', '企业资质', '人员资质', '招标公告网址'])
        data = pd.concat([data, df])
        time.sleep(random.randint(1, 5))
data.drop_duplicates(inplace=True)
data.to_excel(f'杭州市招标公告项目信息{t}.xlsx', index=False)
