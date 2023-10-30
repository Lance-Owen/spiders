import requests
import json
import random
from time import sleep
from luan import *

# 请求招标公告项目列表
url = "http://ggzy.luan.gov.cn/inteligentsearch/rest/inteligentSearch/getFullTextData"
# 工程建设，不限，不限，招标公告，不限，公开招标
payload = "{\"token\":\"\",\"pn\":0,\"rn\":10,\"sdt\":\"\",\"edt\":\"\",\"wd\":\"\",\"inc_wd\":\"\",\"exc_wd\":\"\",\"fields\":\"title\",\"cnum\":\"001\",\"sort\":\"{'webdate':'0'}\",\"ssort\":\"title\",\"cl\":500,\"terminal\":\"\",\"condition\":[{\"fieldName\":\"categorynum\",\"isLike\":true,\"likeType\":2,\"equal\":\"001001002\"}],\"time\":[{\"fieldName\":\"webdate\",\"startTime\":\"1970-01-01 00:00:00\",\"endTime\":\"2999-12-31 23:59:59\"}],\"highlights\":\"\",\"statistics\":null,\"unionCondition\":[],\"accuracy\":\"\",\"noParticiple\":\"0\",\"searchRange\":null,\"isBusiness\":\"1\"}\r\n"
payload = json.loads(payload)
headers = {
    'Content-Type': 'application/json;charset=UTF-8',
    'Cookie': '__jsluid_h=d2c71f54610aed02a6598f95f40ca6b9; userGuid=1047923792; UM_distinctid=188b90b7da9687-0ffae695472c91-26031d51-384000-188b90b7daa1905; arialoadData=false; oauthClientId=demoClient; oauthPath=http://localhost:8099/EpointWebBuilder; oauthLoginUrl=http://localhost:8099/EpointWebBuilder/rest/oauth2/authorize?client_id=demoClient&state=a&response_type=code&scope=user&redirect_uri=; oauthLogoutUrl=http://localhost:8099/EpointWebBuilder/rest/oauth2/logout?redirect_uri=; SL_G_WPT_TO=zh-CN; noOauthRefreshToken=a4a1181c69111ac0a7ea1c9602437d2b; noOauthAccessToken=6512c3dcc468bb161fb9d02308aa16dd; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; Secure; CNZZDATA1280735035=1761092027-1686731718-null%7C1696662579; __jsluid_h=20f12820b38f06ff6a20a43848b0f89d',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

# 请求招标公告正文
headers1 = {
    'Cookie': 'Secure; __jsluid_h=20f12820b38f06ff6a20a43848b0f89d; __jsluid_s=6b1db6d6c353f8842ced4cb2ece8957d',
    'Content-Type': 'application/json;charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

df = pd.DataFrame()
for i in range(10):
    print(f"采集第 {i + 1} 页数据".center(100, '*'))
    payload['pn'] = i * 10
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    projects = json.loads(response.text)
    for project in projects['result']['records']:
        # 标题
        title = project['title']
        print(title)
        # 正文网址
        link_url = f"https://ggzy.luan.gov.cn/{project['linkurl']}"
        print(link_url)
        relationguid = project['relationguid']
        id = project['id']
        # 请求招标公告正文
        html_text = requests.request('GET', link_url, headers=headers1, data={}).text
        open_time, method = get_tender_mess(html_text)
        print(open_time, method)
        # link_url = f"https://ggzy.luan.gov.cn/jyxxparentDetail.html?infoid={id[:-4]}&categorynum=001001002&relationguid={relationguid}"
        data = pd.DataFrame(data=[[id, title, relationguid, link_url, open_time, method]],
                            columns=['id', '项目名称', '关系id', '招标网址', '开标时间', '评标办法'])
        df = pd.concat([df, data])
        sleep(random.randint(1, 5))
df.drop_duplicates(inplace=True)
df.to_excel(f'六安市招标公告信息{t}.xlsx', index=False)
