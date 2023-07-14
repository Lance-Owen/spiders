import requests
import datetime

url = "http://jy.ggj.huainan.gov.cn/jyxx/012001/012001004/secondPageJYXX.html"

payload = {}
headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}

response = requests.request("GET", url, headers=headers, data=payload)

html = response.text
# print(html)

from lxml import etree
element = etree.HTML(html)
nodes = element.xpath("//li[@class='ewb-list-node clearfix']")
for node in nodes:
    project_name = node.xpath('a/text()')[0]
    print(project_name)

    # print(node)
    bid_url = f"http://jy.ggj.huainan.gov.cn/{node.xpath('a/@href')[0]}"
    # print(url)
    date = node.xpath('span')[0].text
    yes = datetime.datetime.now().date() + datetime.timedelta(days=-1)
    if datetime.datetime.strptime(date,'%Y-%m-%d').date() == yes:
        response = requests.request("GET", bid_url, headers=headers, data=payload)
        bid_html = response.text
        bid_element = etree.HTML(bid_html)
        bid_price = bid_element.xpath("//tr[2]/td[5]/p/span")[0].text
        print(bid_price)
        tender_url = bid_element.xpath("//li[@id='012001001']/a/@href")
        print(tender_url)
