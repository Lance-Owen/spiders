import pandas as pd
from huainan import *
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

# zbkzj = 14789847.96
if __name__ == '__main__':
    url = input("url:")
    zbkzj = float(input('招标控制价：'))
    text = request_text(url=url)
    df = get_bidders_list(text)
    df = df[df['投标报价'] != '']
    df['下浮率'] = df['投标报价'].apply(lambda x:100-100*float(x)/zbkzj)
    df.sort_values(by=['下浮率'],inplace=True)
    df.to_excel('淮南项目开标记录.xlsx',index=False)
