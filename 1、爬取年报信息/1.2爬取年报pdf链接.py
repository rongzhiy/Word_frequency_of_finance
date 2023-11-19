import requests
import time
import csv
import random
import pandas as pd
import openpyxl
import math
import os

#提前获得的上市公司信息，以巨潮网的A股上市公司为例

#设定初始值
date='2000-01-01~2023-11-19'#这里可以根据自己所要的时间跨度自行修改
start=2#自己设定从firm_message.csv的第几行开始
end=10#自己设定从firm_message.csv的第几行结束,建议每200/300家公司爬取一次


df=pd.read_csv('firm_message.csv',dtype={'code':'str'})

url='http://www.cninfo.com.cn/new/hisAnnouncement/query'
headers={
# 'Cookie': 'JSESSIONID=BC3717325F9C6B6B81B29FBA2B5B5F4A; insert_cookie=37836164; routeId=.uc2; _sp_id.2141=c0029389-4e1d-49b0-8fcc-ca65359fb7a0.1622767493.17.1652852982.1649928549.4dd68440-4343-4434-92eb-5811d472da6b',
'Host': 'www.cninfo.com.cn',
'Origin': 'http://www.cninfo.com.cn',
'Referer': 'http://www.cninfo.com.cn/new/commonUrl/pageOfSearch?url=disclosure/list/search&lastPage=index',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36'
}

#step1 获取最大页数(网页上的totalpages字段不准确，会出错，因此这里自定义获取最大页数）
def get_pages(url,headers,code,orgId,date):
    data={
        'pageNum': '1',
        'pageSize': '30',
        'column': 'szse',
        'tabName': 'fulltext',
        'plate': '',
        'stock': f'{code},{orgId}',
        'searchkey': '',
        'secid': '',
        'category': 'category_ndbg_szsh',
        'trade': '',
        'seDate': date,
        'sortName': '',
        'sortType': '',
        'isHLtitle': 'true'
    }
    # print(data)
    response=requests.post(url=url,headers=headers,data=data)
    response.encoding = response.apparent_encoding
    json_data=response.json()
    # print(json_data)
    totalAnnouncement = json_data['totalAnnouncement']#不能用网上的totalpages，有的会出错
    a = totalAnnouncement / 30
    totalpages=math.ceil(a)
    return totalpages   


#step2 逐页获取json数据

#创建错误信息文件
if not os.path.exists('错误记录.xlsx'):
    wb=openpyxl.Workbook('错误记录.xlsx')
    wb.save('错误记录.xlsx')

wb=openpyxl.load_workbook('错误记录.xlsx')
ws=wb.active

with open('ndbg_data.csv', mode='a', encoding='utf-8',newline='') as f:
    f.write('code,secName,orgId,announcementId,announcementTitle,pdf_url\n')
    csv_write = csv.writer(f)
    for i in range(start-2, end-1):
        code = df.iloc[i].at['code']
        orgId = df.iloc[i].at['orgId']
        zwjc = df.iloc[i]['zwjc']
        # time.sleep(2)#可更改，但间隔不要太短
        try:
            total_pages = get_pages(url, headers, code, orgId, date)
            for page in range(1,total_pages+1):
                print(f'正在下载{i+2}-{code}-{zwjc} 第{page}/{total_pages}页年报信息')
                post_data={
                    'pageNum': f'{page}',
                    'pageSize': '30',
                    'column': 'szse',
                    'tabName': 'fulltext',
                    'plate': '',
                    'stock': f'{code},{orgId}',
                    'searchkey': '',
                    'secid': '',
                    'category': 'category_ndbg_szsh',#年报+半年报：category_ndbg_szsh;category_bndbg_szsh
                    'trade': '',
                    'seDate': date,
                    'sortName': '',
                    'sortType': '',
                    'isHLtitle': 'true'
                }
                print(post_data)
                time.sleep(0.1)
                response = requests.post(url=url, headers=headers, data=post_data)
                response.encoding = response.apparent_encoding
                json_data = response.json()
                stop=random.randint(0,2)
                time.sleep(stop/10)
                data_list = json_data['announcements']
                for data in data_list:
                    secCode = data['secCode']
                    secName = data['secName']
                    orgId = data['orgId']
                    announcementId = data['announcementId']
                    title = data['announcementTitle']
                    if '摘要' in title:
                        continue
                    if '说明' in title:
                        continue
                    if '公告' in title:
                        continue
                    if '英文' in title:
                        continue
                    adjunctUrl = data['adjunctUrl']
                    pdf_url = 'http://static.cninfo.com.cn/' + adjunctUrl
                    csv_write.writerow([str(secCode),secName,orgId,announcementId,title,pdf_url])
        except:
            ws.append([f'{code}有误，请进一步确认'])
            print(f'{code}有误，已记录')
wb.save('错误记录.xlsx')


