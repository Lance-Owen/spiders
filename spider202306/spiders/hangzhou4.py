# import pandas as pd
# df = pd.read_csv('杭州市招标公告项目信息2023-08-29.csv',encoding='gbk')
# df = df.sort_values(by='投标单位数量').drop_duplicates(subset=['项目编号','project_type'],keep='first')
# df.to_csv('杭州市开标项目信息2023-08-29.csv', index_label=False)

import pandas as pd
df = pd.read_excel('杭州市开标项目信息2023-08-31.xlsx')

df = df.drop_duplicates(keep='first')
max_bids = df.groupby('项目编号')['投标单位数量'].max()

# 将得到的最大投标单位数量赋值给原来的 df DataFrame
df['投标单位数量'] = df['项目编号'].map(max_bids)
df = df.drop_duplicates(subset=['项目编号'],keep='first')
df.to_excel('杭州市开标项目信息2023-08-31-1.xlsx', index=False)
