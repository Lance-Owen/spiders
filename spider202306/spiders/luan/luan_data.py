'''
    数据汇总
'''

import pandas as pd
df = pd.read_excel('六安市招标公告信息汇总.xlsx')
df1 = pd.read_excel('六安市招标公告信息2023-10-09.xlsx')
df2 = pd.read_excel('六安市招标公告信息2023-10-26.xlsx')

df = pd.concat([df,df1,df2])
df['linkurl'] = df.apply(lambda row:f"https://ggzy.luan.gov.cn/jyxxparentDetail.html?infoid={row['id'][:-4]}&categorynum=001001002&relationguid={row['关系id']}",axis=1)
df = df.drop_duplicates()
print(len(df))

df.to_excel('六安市招标公告信息汇总.xlsx',index=False)