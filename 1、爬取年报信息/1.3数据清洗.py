import pandas as pd


# pd.set_option('max_columns', 100)
# pd.set_option('max_colwidth', 100)
df=pd.read_csv('ndbg_data.csv',dtype={'code':'str'},encoding='utf-8')
# 删除摘要和已取消的
df = df.drop(df[df['announcementTitle'].str.contains('摘要',regex=False)==True].index)
df = df.drop(df[df['announcementTitle'].str.contains('取消',regex=False)==True].index)
df = df.drop(df[df['announcementTitle'].str.contains('公告',regex=False)==True].index)
df = df.drop(df[df['announcementTitle'].str.contains('英文',regex=False)==True].index)
df = df.drop(df[df['announcementTitle'].str.contains(r'[a-zA-Z]',regex=True)==True].index)#英文标题
df = df.drop(df[df['code'].str.contains('code',regex=False)==True].index)#删除上一步骤多写进去的标题
#提取年份
df['year']=df['announcementTitle'].str.extract(r'(\d{4}年)', expand=False)
#保留最新一次更新的年报
df=df.drop_duplicates(['code','year'],keep='first')
print('正在保存,请稍等')
df.to_excel('all_url_data.xlsx',index=False)
print(df)

