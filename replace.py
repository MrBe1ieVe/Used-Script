# Used to replace the {filename}/pic to ../InsertPic
# Warning !!!!
# Bad script
# I should just use to filename to replace instead of the stupid regex

# finally i updated it and re-import to my obsidian
# with the debug
# it finally done qaq

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
        if(filename.find(".py")>=0):
            continue
        replace_flag = 0
        print()  
        print(filename) 
        text = []
        for line in open(filename,encoding='utf-8'):
            if(line.find("isPublish: Yes")==0):
                break
            if(line == "---\n" or (line.find("#")>=0) or (line.find("\"")>=0) or (line.find(":")>=0) or (line.find("process")>=0) or (line.find("ELF")>=0) ):
                text.append(line) 
                continue
            need_replace = line.find(filename[:-3])      #匹配 类似 (Linux 文件系统详解/ 的
            if(need_replace>0):
                replace_flag = 1
                print(line)
                line = line.replace(filename[:-3],"../InsertPic") 
                line = line.replace("\\","/")
                line = line.replace(".assets","")
                print(line)
            text.append(line)                           # 替换文件路径，让markdown读取到放置在 ../InsertPic/ 的图片
        text.insert(1 , "isPublish: Yes\n")
        if(replace_flag):
            writeback(filename,text)
        else:
            continue
        