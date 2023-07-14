

find_K = '复合系数K：(\d+.\d+)'
find_i = '下浮系数i：(\d+\.\d+|\d)'
find_ratio = '调整系数：(\d+\.\d+|\d)'
find_budget = '工程量清单预算：(\d+\.\d+|\d)'
find_control_price = '招标控制价：(\d+\.\d+|\d)'
find_Bplan = 'B值计算方案：计算(方案[一二])'
# find_extract = '系数抽取模式：(模式[一二三])'
# find_float = '最高限价下浮值：(\d+\.\d+|\d)'

import hashlib
import re

import pandas as pd


def p_generate_md5(text) -> str:
    m = hashlib.md5()
    m.update(text.encode('utf-8'))
    return m.hexdigest()



re_find = "复合系数K：(\d+\.\d+|\d) 下浮系数i：(\d+\.\d+|\d) 调整系数：(\d+\.\d+|\d) 工程量清单预算：(\d+\.\d+|\d) 招标控制价：(\d+\.\d+|\d)"

df = pd.read_csv('杭州市开标记录中参数抽取信息记录1.csv',encoding='gbk')

df['抽取信息'] = df['抽取信息'].fillna("")

data = df[df['抽取信息'].str.contains("复合系数")]

data['复合系数K'] = data['抽取信息'].apply(lambda s: re.findall(find_K,s)[0])

data['下浮系数i'] = data['抽取信息'].apply(lambda s: re.findall(find_i,s)[0])

data['调整系数'] = data['抽取信息'].apply(lambda s: re.findall(find_ratio,s)[0])

data['工程量清单预算'] = data['抽取信息'].apply(lambda s: re.findall(find_budget,s)[0])

data['招标控制价'] = data['抽取信息'].apply(lambda s: re.findall(find_control_price,s)[0])

data['B值计算方案'] = data['抽取信息'].apply(lambda s: '' if not re.findall(find_Bplan,s) else re.findall(find_Bplan,s)[0])


data = pd.concat([df[df['抽取信息'].str.contains("复合系数")==False],data])

data = data[data['抽取信息']!=""]

data["XMBH"] = data['TenderName'].apply(p_generate_md5)


df.to_csv("杭州市开标记录中参数抽取信息记录1.csv",index=False, encoding='utf-8')




A = 1000
k1_list = [0.90,0.91,0.92,0.93,0.94,0.95]
k2_list = [0.3,0.4,0.5]

for B in range(900,1000):
    x = []
    for k2 in k2_list:
         for k1 in k1_list:
            x.append(round(A*k1*k2+B*(1-k2),3))
            print(round(A*k1*k2+B*(1-k2),3))
sns.lineplot(range(len(x)),x)  # 默认



