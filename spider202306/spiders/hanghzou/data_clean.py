import pandas as pd
df1 = pd.read_csv(r"C:\Users\pc\.vscode\code project\spiders\spider202306\spiders\hanghzou\数据留存\杭州市招标公告项目信息2023-08-29数据完整性留存.csv",encoding='gbk')
df2 = pd.read_excel(r"C:\Users\pc\.vscode\code project\spiders\spider202306\spiders\hanghzou\数据留存\杭州市招标公告项目信息2023-10-30.xlsx")

df = pd.concat([df1,df2])
df = df.drop_duplicates()
df.to_excel(r"C:\Users\pc\.vscode\code project\spiders\spider202306\spiders\hanghzou\数据留存\杭州市招标项目信息汇总.xlsx",index=False)