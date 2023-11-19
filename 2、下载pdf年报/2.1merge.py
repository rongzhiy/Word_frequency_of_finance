import pandas as pd

# pd.set_option('max_columns', 100)
# pd.set_option('max_colwidth', 100)

df1=pd.read_excel('./aim_data.xlsx',dtype={'code':str})  # 读取目标数据
df2=pd.read_excel('./all_url_data.xlsx',dtype={'code':str}) # 读取所有数据

df3=pd.merge(df1,df2,on=['code','year'],how='left') 

df4=df3.loc[:,['code','firm','year','pdf_url']] 
df4.to_excel('./merged_data.xlsx',index=False) # 保存数据

print(df4)
