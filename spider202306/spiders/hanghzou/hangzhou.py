import requests
import re
import datetime
import pandas as pd

t = datetime.datetime.now().strftime('%Y-%m-%d')

def parse_value_type1(url):
    '''
    清洗抽取值规则一
    '''
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    text = response.text
    # 解析标签中的信息
    values = re.findall("<span[^>]*>([^<]*)</span>",text)
    values = [re.sub("&nbsp;| |K1|K2|:|：","",s) for s in values]
    return values

def parse_value_type2(text):
    ''''
    清洗抽取值规则二
    '''
    values = re.findall('<span class="input-group">([^<]*)</span>',text)
    if '复合' in values[-1]:
        if "计算方案" in values[-1]:
            out_text = re.findall("[：:]([\d\.]{0,4}) ",values[-1]),values[-1][-1]
            return out_text
        else:
            out_text = re.findall("[：:]([\d\.]{0,4}) ", values[-1])
            return out_text
    return values[-1]

def count_tender_num(project_html,find_col_name):
    '''
    解析开标记录页面，计算投标单位数量
    '''
    del_label = re.compile(r'<[^>]+>', re.S)
    re_table = re.compile('<table[^>]*>[\s\S]*?<\/table>', re.IGNORECASE)
    re_tr = re.compile('<tr[^>]*>[\s\S]*?<\/tr>', re.IGNORECASE)
    re_td = re.compile('<t[hd][^>]*>[\s\S]*?</t[hd]>', re.IGNORECASE)

    tables = re_table.findall(project_html)
    max_len = 0
    for table in tables:
        table_text = []
        for row in re_tr.findall(table):
            table_text.append([])
            for col in re_td.findall(row):
                s = del_label.sub("", re.sub("\s", '', col))
                if re.findall(find_col_name, s) and len(s) <= 10:
                    s = '投标单位名称'
                    table_text = table_text[-1:]
                table_text[-1].append(s)
            if not table_text[-1]:
                table_text = table_text[:-1]
        # 根据表头信息,找到单位
        if '投标单位名称' in table_text[0]:
            col_index = table_text[0].index('投标单位名称')
            df = pd.DataFrame(data=[d[col_index] if len(d) >= col_index + 1 else '' for d in table_text],
                                  columns=['投标单位名称'])
            # df = df[df['投标单位名称'].apply(lambda x: True if re.match(r".*?公司", str(x)) else False)]
            # 根据名字长度清洗数据
            df = df[df['投标单位名称'].apply(lambda x: True if len(str(x).replace(' ', ''))>3 else False)]
            df = df.fillna('')
            if len(df) > 0:
                df = df[df['投标单位名称'] != '']
                max_len = max(max_len, len(df))
                # print(max_len)
                return max_len
            return 0
def get_open_project(url, id):
    payload = {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Content-Type': 'text/html; charset=utf-8'
    }
    # 请求开标记录网页信息
    response = requests.request("GET", url, headers=headers, data=payload)
    html = response.text
    # 计算投标单位数量
    tender_num = count_tender_num(html, '投标企业')
    del_label = re.compile(r'<[^>]+>', re.S)
    # 解析开标时间
    divs = re.findall('<div[\s\S]*?<\/div>', html)
    for div in divs:
        if '开标时间' in div:
            open_time_label = re.findall('<span[\s\S]*?<\/span>',div)[0]
            open_time = del_label.sub('', open_time_label)
            open_time = re.sub('\n', '', open_time).replace('&nbsp;', '').strip()
            print(open_time)
            break
    else:
        open_time = ''
    # 根据页面信息,判断抽取值公布方式,并进行标记,分为:无参数,从当前网页获取参数,和拼接网址获取参数
    if '查看系数' in html:
        # extract_response = requests.request("GET", extract_url, headers=headers, data=payload)
        # extract_value = re.findall('<span id="([^"]*)">',extract_response.text)
        # 拼接抽取值网址
        extract_url = f"https://ggzy.hzctc.hangzhou.gov.cn/OpenBidRecord/OpenParamInfo?openRecordListID={id}"
        return extract_url,1, tender_num, open_time
    elif '参数抽取' in html:
        return '',2, tender_num, open_time
    else:
        return '', 0, tender_num, open_time

def get_tender_project(url):
    payload = {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Content-Type': 'text/html; charset=utf-8'
    }
    del_label = re.compile(r'<[^>]+>', re.S)
    response = requests.request("GET", url, headers=headers, data=payload)
    names = ['工程名称', '项目编号', '开标时间', '工程分类', '是否联合体投标', '资格审查方式', '本期概算(万元)', '备注', '对投标人的承包资质要求', '从业人员资格要求']
    project_value = ['', '', '', '', '', '', '', '', '', '']
    try:
        tables = re.findall('<table[\s\S]*?<\/table>',response.text)
        for table in tables:
            for tr in re.findall('<tr[\s\S]*?<\/tr>',table):
                tds = re.findall('<td[\s\S]*?<\/td>',tr)
                for i in range(len(tds)):
                    s = del_label.sub('', tds[i])
                    s = re.sub('\s','',s)
                    if s in names:
                        index = names.index(s)
                        s = del_label.sub('', tds[i+1])
                        s = re.sub('\n', '', s).replace('&nbsp;','').strip()

                        print(s)
                        project_value[index] = s
        return project_value
    except:
        print(url)
        return ''