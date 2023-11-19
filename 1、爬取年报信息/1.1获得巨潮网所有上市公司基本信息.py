import requests
import pandas as pd

url='http://www.cninfo.com.cn/new/data/szse_stock.json'
headers={
# 'Cookie': 'JSESSIONID=D7A0DCE786D206034F280655BA2460C4; _sp_ses.2141=*; insert_cookie=37836164; routeId=.uc2; _sp_id.2141=c0029389-4e1d-49b0-8fcc-ca65359fb7a0.1622767493.17.1652852982.1649928549.4dd68440-4343-4434-92eb-5811d472da6b',
'Host': 'www.cninfo.com.cn',
'Referer': 'http://www.cninfo.com.cn/new/commonUrl/pageOfSearch?url=disclosure/list/search&lastPage=index',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36'
}
response=requests.get(url=url,headers=headers)
json_data=response.json()
data_list=json_data["stockList"]
df=pd.DataFrame(data_list,dtype='str')
df.to_csv('firm_message.csv',index=False)
print(df)
