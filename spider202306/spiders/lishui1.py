import requests
import json
import re
import time
import html
import random
import pandas as pd

def error_log(error):
    with open('error.log','a+',encoding='utf-8') as f:
        f.write(error)
        f.write('\n')

url = "https://lssggzy.lishui.gov.cn/jsearchfront/interfaces/search.do"

save_datas = []
for i in range(1,3):
    print(f"页码：{i}".center(100,"*"))
    payload = f"_cus_lq_projectcode=&_cus_pq_title=&begin=&end=&_cus_lq_dljg=&_cus_lq_jyjf=&_cus_eq_author=&sortType=2&websiteid=331101000003826&tpl=1621&p={i}&pg=30&cateid=683&_cus_lq_regioncode=\r\n"
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
      'Cookie': 'user_sid=104bcf6a74e34dedb2eb8131a0f7d526; JSESSIONID=E402DC955771441B5EEF5876B895F0E7; searchsign=5ee5737e7d5c43cd9bd81c6190a030b3; searchid=1be9e08d9f864521acb8d38bd9e92fa4; SL_G_WPT_TO=zh-CN; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; NBSESSIONID=d120012d-8c61-4862-8ed6-dbe645ea763a; arialoadData=false; SERVERID=71bfd367a49f5c3316644ab3e3801eff|1687315863|1687315631; user_sid=37fa1d6d4b784bc48fc5c9085a728781; SERVERID=bc6beea6e995cecb42c7a1341ba3517f|1687678561|1687678561',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    text = response.text
    text = json.loads(text)
    for d in text['dataResults']:
        save_data = []
        # d = text['dataResults'][0]
        projecttype = d['data']['industriestype']
        ad = d['data']['regioncode']
        tendermode = d['data']['tendermode']
        try:
            projectcode = d['data']['projectcode']
            print(projectcode)

        except:
            pass
        try:
            projectname = d['data']['bidsectioncode']
            print(projectname)
        except:
            pass
        try:
            projecturl = d['data']['url']
            print(projecturl)
        except:
            pass
        # for name in ['projectcode','bidsectioncode','url','industriestype','regioncode','tendermode']:
        #     try:
        #         save_data.append(d['data'][name])
        #     except Exception as e:
        #         save_data.append('')
        #         error_log(str(e))
        # save_datas.append(save_data)


        try:
            project_html = html.unescape(d['data']['bu11etincontent'])
        except Exception as e:
            error_log(str(e))
        # projectcode,projectname,projecturl = save_data[:3]

        # 获取投标人数量,168页以前
        # rows = re.findall(r'<tr[^>]*>[\s\S]*?<\/tr>',project_html)
        # max_len = []
        # for row in rows:
        #     count_str = re.findall(r'<td[^>]*>[\s\S]*?<\/td>',row)
        #     if not count_str:
        #         continue
        #     count_str = count_str[0]
        #     del_label = re.compile(r'<[^>]+>',re.S)
        #     count_str = del_label.sub("",re.sub("\s",'',count_str))
        #     # print(count_str)
        #     #   
        #     if re.findall('\d+',count_str) and count_str.isdigit():

        #         print(count_str)
        #         max_len.append(int(count_str))
        # if max_len:
        #     save_datas.append([projecturl,max(max_len)])
        # time.sleep(random.random())


        # 获取投标人数量,168页以后
        # max_len = 0
        # for i in range(0,2):
        #     try:
        #         dfs = pd.read_html(d['data']['url'],header=i)
        #         for df in dfs:
        #             if '序号' in df.columns:
        #                 df = df[df['序号'].apply(lambda x: True if re.match(r"\d+", str(x)) else False)]
        #                 df['序号'] = df['序号'].astype('int')
        #                 print("最大行数",max(df['序号'].tolist()))
        #                 max_len = max(df['序号'].tolist()) if max_len < max(df['序号'].tolist()) else max_len   
        #                 # print(df.columns,f"一共有：{len(df)}")
        #     except Exception as e:
        #         error_log(str(e))
        # save_datas.append([projecturl,max_len])

        '''获取基准价和下浮率 '''
        rate = 0
        price = 0
        del_label = re.compile(r'<[^>]+>',re.S)
        project_str = del_label.sub("",project_html)
        # print(project_str)
        # x = re.match('.*?下浮.*?(\d*\.\d*|\d*)%.*?',project_str).groups()[0]
        if re.findall('下浮[^\d]{0,3}(\d*\.\d*|\d*)%',project_str):
            rate = re.findall('下浮[^\d]{0,3}(\d{1,2}\.\d*|\d{1,2})%',project_str)[0]
            rate = float(rate) if rate else 0
        if re.findall('基准[^\d]{0,2}(\d*\.\d*|\d*)',project_str):
            price = re.findall('基准[^\d]{0,2}(\d*\.\d*|\d*)',project_str)[0]
            price = float(price) if price else 0
        print(rate,price) 

        if rate != 0 :
            save_data = [projectcode,projectname,projecturl,price/(1-rate*0.01),rate,price]
            if save_data not in save_datas:
                save_datas.append(save_data)
            else:
                raise ValueError('程序完成！')
        else:
            save_data = [projectcode,projectname,projecturl,price,rate,price]
            if save_data not in save_datas:
                save_datas.append(save_data)
            else:
                raise ValueError('程序完成！')

    
import pandas as pd
df = pd.DataFrame(columns=['id','项目名称','网址','zbkzj','下浮率','kbjj'],data=save_datas)
# df = pd.DataFrame(columns=['网址','投标单位数'], data=save_datas)
df.to_csv('丽水市测试数据0629.csv',index=False,encoding='utf-8')


