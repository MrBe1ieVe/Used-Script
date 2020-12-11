import os
import sys
import time
import datetime
fpath = os.getcwd()
path=os.path.abspath(os.path.dirname(__file__))


def shift_time(filename):
    time_stamp_create = os.path.getctime(filename)
    time_stamp_modify = os.path.getmtime(filename)
    if time_stamp_create > time_stamp_modify:
        time_stamp = time_stamp_modify
    else :
        time_stamp = time_stamp_create
    dateArray = datetime.datetime.fromtimestamp(time_stamp)  
    return dateArray.strftime("%Y/%m/%d %H:%M:%S") 

def writeback(filename,text):
    s = ''.join(text)
    with open(filename , "w" , encoding='utf-8',) as f:
        f.write(s)

#将文件创建时间或修改时间，最早的一个，写入date中，作为文章时间
for parent, dirnames, filenames in os.walk(fpath):
    for filename in filenames:         
        temp=os.path.splitext(filename)
        file,type=temp
        if type == ".md":
            headline = False
            head_exist = False
            date_exist = False
            line_num = False
            create_date = shift_time(filename) 
            for line in open(filename,encoding='utf-8'):
                line_num += 1
                if line == "---\n":
                    headline += 1
                    continue
                if "date:" in line:
                    date_exist = True
                    break
                if headline == 2:
                    head_exist = True
                    break
                if line_num == 10:
                    break
            if date_exist:
                continue
            elif head_exist:
                text = []
                for line in open(filename,encoding='utf-8'): 
                    text.append(line)
                text.insert(1 , "date: " + create_date + '\n')
                writeback(filename,text)
                continue
            else:
                text = []
                for line in open(filename,encoding='utf-8'): 
                    text.append(line)
                text.insert(0 , "---\ndate: " + create_date + '\n---\n')
                writeback(filename,text)
   
for folder in os.listdir():
    if folder == ".vscode":
        continue
    if os.path.isdir(folder)==True:
        temp=os.path.splitext(folder)
        file,type=temp
        if type == ".assets":
            for parent, dirnames, filenames in os.walk(fpath):
                for filename in filenames:  
                    if filename == file + '.md':
                        text = []
                        for line in open(filename,encoding='utf-8'): 
                            text.append(line.replace(".assets",""))
                        writeback(file + '.md',text)
        new_name=folder.replace('.assets','')
        os.rename(os.path.join(path,folder),os.path.join(path,new_name))
        #i+=1

os.system(('cd {} && hexo clean && hexo gen && hexo deploy').format(path))#cd {} && hexo clean && hexo gen && hexo deploy
"""
#对目录下的文件进行遍历
for folder in os.listdir(path):
    if folder==".vscode":
        continue
#判断是否是文件
    if os.path.isdir(os.path.join(path,folder))==True:
#设置新文件名
        new_name=folder.replace('.assets','')
#重命名
        os.rename(os.path.join(path,folder),os.path.join(path,new_name))
        #i+=1



for folder in os.listdir(path):
#判断是否是文件
    if folder==".vscode":
        continue
    if os.path.isdir(os.path.join(path,folder))==True:
#设置新文件名
        new_name=folder + '.assets'
#重命名
        os.rename(os.path.join(path,folder),os.path.join(path,new_name)) """
