import xlwt
import os
# 加载txt列表寻找关键词并保存到excel
def matchKeyWords(ThePath, keyWords,aim_path):
    dir_list = os.listdir(ThePath)
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet('年报关键词词频统计', cell_overwrite_ok=True)
    sheet.write(0, 0, '股票代码')
    sheet.write(0, 1, '股票名称')
    sheet.write(0, 2, '年份')
    for i,c_word in enumerate(keyWords):
        sheet.write(0, i+3, c_word)
    index=0
    for dir in dir_list:
        dir_path = ThePath + '\\' + dir
        files = os.listdir(dir_path)
        for file in files:
            if os.path.splitext(file)[-1] == ".txt":
                txt_path = os.path.join(dir_path, file)
                stock_code = dir.split("-")[0]
                stock_name = dir.split("-")[1]
                year = file[0:4]
                sheet.write(index + 1, 0, stock_code)
                sheet.write(index + 1, 1, stock_name)
                sheet.write(index + 1, 2, year)
                print(f'正在统计{dir}-{file}')
                with open(txt_path, "r", encoding='utf-8', errors='ignore')as fp:
                    text = fp.read()
                    for ind,word in enumerate(keyWords):
                        word_freq=text.count(word)
                        sheet.write(index + 1, ind + 3, str(word_freq))
                index+=1
    book.save(aim_path)

ThePath= r'../2、下载pdf年报/年报txt版本'
aim_path=r'../2、下载pdf年报/词频统计'
keywords = ['营业收入','估值','资产','股东','智能数据分析','智能机器人','机器学习','深度学习']
matchKeyWords(ThePath, keywords,f'{aim_path}\词频统计.xls')
