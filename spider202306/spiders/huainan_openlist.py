from huainan import *
import pandas as pd

'''
淮南市开标记录
获取信息：
    1、项目名称
    2、项目开标记录地址
    3、投标人数，去除投标价格为空的数据
    4、抽取蚕食
'''

df = pd.DataFrame()

for i in range(1,3):
    # 第一个页面网址不一样
    if i == 1:
        url = "http://jy.ggj.huainan.gov.cn/jyxx/012001/012001012/secondPageJYXX.html"
    else:

        url = f"http://jy.ggj.huainan.gov.cn/jyxx/012001/012001012/{i}.html"
    payload = {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    # 信心在网页中
    text = response.text
    # 通过正则提取项目名称
    project_name_list = re.findall('title="(.*?)"',text)[:15]
    # 正则获取项目开标记录网址，并拼接为可打开的网址
    url_list = re.findall('<a href="(.*?\.html)"\s*class="ewb-list-name ewb-otw"',text)
    url_list = ["http://jy.ggj.huainan.gov.cn" + url for url in url_list]
    # 获取项目开标记录网页信息
    project_open_text_list = [request_text(url) for url in url_list]
    # 调用函数提取开标记录表，包含单位和报价信息
    bidder_list = [get_bidders_list(text) for text in project_open_text_list]
    # 计算投标单位数量
    num = [len(bidder) for bidder in bidder_list]
    # 正则提取出公示的 抽取值信息
    extract_parameters = [get_extract_parameters(s) for s in project_open_text_list]

    # print(project_name_list,url_list,num,extract_parameters)
    # 合并每一页开标记录信息
    data = pd.DataFrame(data={'项目名称':project_name_list,"网址":url_list,"投标家数":num,"抽取参数":extract_parameters})
    df = pd.concat([df,data])
df.to_excel('开标记录数据.xlsx',index=False)


