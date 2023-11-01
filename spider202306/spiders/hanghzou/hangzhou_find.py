'''

根据项目名称查询项目名称网址
'''
import urllib
from urllib import parse
import json
import pandas as pd
from hangzhou import *
import time

name_list = ["昌化镇平溪路道路建设工程", "淳安中学学生宿舍、食堂、校园道路及校园文化提升等改造工程", "临政储出【2020】9号地块（锦南新城人才租赁用房项目）室外配套工程", "岩桥未来社区人才公寓项目(一期)全过程代建", "2023年“迎亚运”通勤线路修缮-之江路（南复路-清江路）", "东都公寓老旧小区综合改造项目", "昌化镇城东路道路建设项目", "天英工业园区污水支管网建设项目（一期）", "青柯便民服务中心建设项目", "昌化镇东塔街道路建设项目", "凤川街道Y733钟家山至桃岭提升改造工程", "淳安县湖山公墓2023新区扩建工程", "桐庐县富春江干堤加固二期工程标准化建设项目", "桐庐县富春江右支4河道工程", "大运河杭钢工业旧址综保项目 GS1303-07地块文化设施一标段", "杭州市特别生态功能区千岛湖供排水设施建设项目---供水设施建设工程", "桐庐县合村乡商贸综合体室外项目", "富政工出【2020】3号杭州东信科瑞电子有限公司富阳智能制造基地建设项目暖通空调工程", "临平政工出[2023]14号年产10台套燃气轮机组项目EPC工程总承包", "春华村南渠南侧南地块公租房项目", "南江路（潘水路-XSCQ2409-12地块北侧）", "康良路（京杭大运河-运溪高架）工程一期（运溪高架-湖杭高铁）"]



import requests


url = "https://ggzy.hzctc.hangzhou.gov.cn/SecondPage/GetNotice"

headers = {
  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}
data = pd.DataFrame()

for name in name_list:
    new_txt = urllib.parse.quote(name)

    payload = f"area=&afficheType=28&IsToday=&title={new_txt}&proID=&number=&IsHistory=1&TenderNo=&_search=false&nd=1698719430379&rows=10&page=1&sidx=PublishStartTime&sord=desc"

    response = requests.request("POST", url, headers=headers, data=payload)
    if len(json.loads(response.text)['rows'])==0:
        print()
        continue

    for row in json.loads(response.text)['rows']:
        if row['TenderName'] == name:
            ID = row['ID']
            break
    project_url = f"https://ggzy.hzctc.hangzhou.gov.cn/AfficheShow/Home?AfficheID={ID}&IsInner=0&IsHistory=1&ModuleID=28"
    print(project_url)
    # project_value = get_tender_project(project_url)
    # project_value[0] = name
    #
    # project_value.append(project_url)
    # df = pd.DataFrame(data=[project_value],
    #                   columns=['项目名称', '项目编号', '开标时间', '工程分类', '是否联合体投标', '资格审查方式',
    #                            '预算', '备注', '企业资质', '人员资质', '招标公告网址'])
    # data = pd.concat([data, df])
    # time.sleep(1)
data.drop_duplicates(inplace=True)
# data.to_excel('杭州市招标公告项目信息.xlsx', index=False)

