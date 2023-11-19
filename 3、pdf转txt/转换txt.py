import os
import pdfplumber

def parsePDF(dir,file,pdf_path,txtpath):
    with open(txtpath, "w", encoding='utf-8') as txt:  # 打开文本文件的
        with pdfplumber.open(pdf_path) as pdf:#打开pdf文件
            for i,page in enumerate(pdf.pages):
                print(f'正在转换{dir}-{file}-{i+1}页')
                txt.write(page.extract_text())
#主程序
ThePath=r'..//2、下载pdf年报//年报pdf版本/'
aim_path=r'..//2、下载pdf年报//年报txt版本'
dir_list = os.listdir(ThePath)
for dir in dir_list:
    dir_path = ThePath + '\\' + dir
    if not os.path.exists(aim_path+'\\'+dir):
        os.makedirs(aim_path+'\\'+dir)
    for root, dirs, files in os.walk(dir_path, topdown=False):
        for file in files:
            try:
                pdf_path=os.path.join(root,file)
                txt_path=aim_path+'\\'+dir+'\\'+file.split('.')[0]+'.txt'
                parsePDF(dir,file,pdf_path,txt_path)
            except:
                with open('错误信息.txt', 'a', encoding='UTF-8', errors='ignore') as f:
                    f.write(os.path.join(root,file)+'\n')

