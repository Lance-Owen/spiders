import pandas as pd
df = pd.read_excel(r"C:\Users\pc\.vscode\code project\spiders\spider202306\spiders\hanghzou\杭州市招标公告项目信息2023-10-30.xlsx")
df = df.drop_duplicates(subset=['项目名称'],keep='first')
df.to_excel(r"C:\Users\pc\.vscode\code project\spiders\spider202306\spiders\hanghzou\杭州市招标公告项目信息2023-10-30.xlsx",index=False)