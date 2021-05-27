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

path_py = os.path.dirname(os.path.abspath(__file__))
path_py = os.path.normpath(path_py)
path_output = path_py[:path_py.index("Used script")] + "\\Note Vault\\OutPut\\"


def writeback(filename,text):
    s = ''.join(text)
    with open(filename , "w" , encoding='utf-8',) as f:
        f.write(s)


for parent, dirnames, filenames in os.walk(path_output):
    for filename in filenames: 
        if(filename.find(".py")>=0):
            continue
        isPublish_flag = 0
        print()  
        print(filename) 
        text = []
        for line in open(os.path.join(path_output, filename),encoding='utf-8'):
            if(line.find("isPublish: Yes")==0):
                isPublish_flag = 1
                break
            text.append(line)    
        if(isPublish_flag):
            continue
        else:
            text.insert(1 , "isPublish: Yes\n")
            print(text[0:3])
            writeback(os.path.join(path_output, filename),text)

        