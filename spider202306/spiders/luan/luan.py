import re
import datetime
import pandas as pd

del_label = re.compile(r'<[^>]+>|&nbsp;|\s', re.S)
re_table_div = re.compile('<div class="ewb-table ewb-tender"[^>]*>[\s\S]*?<\/div>')
re_table = re.compile('<table[^>]*>[\s\S]*?<\/table>', re.IGNORECASE)
re_tr = re.compile('<tr[^>]*>[\s\S]*?<\/tr>', re.IGNORECASE)
re_td = re.compile('<t[hd][^>]*>[\s\S]*?</t[hd]>', re.IGNORECASE)
'''
招标信息中的id，是请求招标公告正文，relationid是开标，候选中标公告的的id。通过relationid联系
'''
t = datetime.datetime.now().strftime('%Y-%m-%d')

def get_tender_mess(text):
    """
    从招标公告中清洗开标时间和评标办法
    :param text:
    :return:
    """
    open_time = ''
    method = ''
    for p in re.findall('<p[^>]*?>([\s\S]*?)</p>', text):
        if '开标时间' in p and open_time == '':
            try:
                open_time = re.findall("(\d*年\d{1,3}月\d{1,3}日\d{1,3}时\d{1,3})", del_label.sub("", p))[0]
            except:
                continue
            # 提取时间字符串
            year, month, day, hour, minute = [int(num) for num in re.findall(r'\d+', open_time)]
            # 转换为时间类型
            open_time = datetime.datetime(year, month, day, hour, minute)
            # 转换成标准时间格式
            open_time = open_time.strftime('%Y-%m-%d %H:%M:%S')
        if '评标办法' in p and method == '':
            # method = ''.join([s for s in re.findall('>([^<]*)<', p) if re.sub('&nbsp;|\s', '', s)][1:])
            method = del_label.sub("", p)
            method = re.split(':|：',method)[-1]
    return open_time,method

def get_bidder_list(project_html,find_col_name):
    '''
    解析开标记录页面，计算投标单位数量
    '''

    project_html = re_table_div.findall(project_html)[0]
    table = re_table.findall(project_html)[0]
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
    df = pd.DataFrame(table_text[1:], columns=['序号', '投标单位名称', '投标报价'])
    df = df[df['投标报价'] != '']
    return df

def get_bid_mess(text):
    """
    从中标公告中清洗控制价和中标金额
    :param text:
    :return:
    """
    kzj = 0
    bid_amount = 0
    for row in re_tr.findall(text):
        row = del_label.sub("", row)
        if '最高限价' in row and kzj == 0:
            try:
                kzj_list = [float(s) for s in re.findall("\d*\.\d*|\d*", del_label.sub("", row)) if s]
                kzj = max(kzj_list)
            except:
                kzj = 0
        if re.findall('投标报?价[(（）)%元]{3}|费率[(（）)%]{3}', row) and bid_amount == 0:
            try:
                bid_amount_list = [float(s) for s in re.findall("\d*\.\d*|\d*", del_label.sub("", row)) if s]
                bid_amount = max(bid_amount_list)
            except:
                bid_amount = 0
    if bid_amount > kzj:
        bid_amount = 0
    return kzj,bid_amount