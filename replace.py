# Used to replace the {filename}/pic to ../InsertPic
# Warning !!!!
# Bad script
# I should just use to filename to replace instead of the stupid regex
import os
import sys
import time
import datetime
import re
fpath = os.getcwd()
path=os.path.abspath(os.path.dirname(__file__))



def writeback(filename,text):
    s = ''.join(text)
    with open(filename , "w" , encoding='utf-8',) as f:
        f.write(s)


for parent, dirnames, filenames in os.walk(fpath):
    for filename in filenames: 
        replace_flag = 0
        print()  
        print(filename) 
        text = []
        for line in open(filename,encoding='utf-8'):
            need_replace = re.search("\(.*/",line)       #匹配 类似 (Linux 文件系统详解/ 的
            #have_http = re.search("\(http",line)  
            if(re.search("\=",line)  or re.search("\(http",line)):
                continue
            if(need_replace):
                replace_flag = 1
                print(line)
                need_replace_text = need_replace.group()[1:]
                line = line.replace(need_replace_text,"../InsertPic/") 
                print(line)
            text.append(line)                           # 替换文件路径，让markdown读取到放置在 ../InsertPic/ 的图片
        if(replace_flag):
            writeback(filename,text)
        else:
            continue
        