# -*- coding:utf-8 -*-
import os
from os import path
import re
import shutil
import hashlib
import datetime
from typing import Text
import time
from urllib.parse import unquote
import RenameTheImages

path_py = os.path.dirname(os.path.abspath(__file__))
path_py = os.path.normpath(path_py)

mac_ob_path = "../../Library/Mobile Documents/iCloud~md~obsidian/Documents/Note Vault"

path_output = path_py[:path_py.index("Used script")] + mac_ob_path + "/OutPut/"# relative path
path_posts =path_py[:path_py.index("Used script")] + "Blog/source/_posts/"  
path_insertpic = path_py[:path_py.index("Used script")] + mac_ob_path + "/InsertPic/"

file_output_path = []
pic_output_path = []
file_output_name = []
pic_output_dic = {}

def rm_dir_content(path):
    shutil.rmtree(path)
    os.mkdir(path)
    print("path: " + path + " cleaned!")
    time.sleep(2)

# return the  earliest time stamp
def shift_time(filename):
    # get the modify time or create time
    time_stamp_create = os.path.getctime(filename)
    time_stamp_modify = os.path.getmtime(filename)
    if time_stamp_create > time_stamp_modify:
        time_stamp = time_stamp_modify
    else:
        time_stamp = time_stamp_create
    dateArray = datetime.datetime.fromtimestamp(time_stamp)
    return dateArray.strftime("%Y/%m/%d %H:%M:%S")

# write back to the file
def writeback(filepath, text):
    s = ''.join(text)
    with open(filepath, "w", encoding='utf-8',) as f:
        f.write(s)

# compare md5
def compare_file_md5(origin_file, des_file):  
    #md5_hash = 
    # if(os.path.isfile(des_file)):# destination file doesnt exist
    #    return False
    with open(origin_file, 'r', encoding='utf-8') as ori, open(des_file, 'r', encoding='utf-8') as des:
        origin_blocks = ori.read(1024).encode('utf-8')
        des_blocks = des.read(1024).encode('utf-8')
        try:
            origin_md5 = hashlib.md5(origin_blocks)
            des_md5 = hashlib.md5(des_blocks)
            if(origin_md5 == des_md5):
                return True
            else:
                return False
        except:
            raise "ERROR"

# open des file and write to it
def replace_pic_open_path(filename,path_posts_file):
    text = []
    for line in open(path_posts_file, encoding='utf-8'):
        # pass the obsidian Date: 
        if(re.search("Date\: \[\[",line)):
            continue
        pic_line = re.search("\!\[.*\]\(\.\.\/InsertPic\/.*\)", line)
        if(pic_line):
            line = line.replace("../InsertPic/", filename[:-3]+"/")
            #print(line)
        text.append(line)
    writeback(path_posts_file,text)
    
#
#

def replace_pic_path_text(filename,text):
    #return replaced path text
    tmp_text = []

    for line in text:
        # pass the obsidian Date: 

        if(re.search("Date\: \[\[",line)):
            continue
        # get the ![](../InsertPic/)
        pic_line = re.search("\!\[.*\]\(\.\.\/InsertPic\/.*\)", line)
        if(pic_line):
            line = line.replace("../InsertPic/", filename[:-3]+"/")
        tmp_text.append(line)
    text.insert(0, "---\n")
    return tmp_text

def copy_and_add_date_title(origin_path, post_path,filename):
    openfile = origin_path + filename
    temp = os.path.splitext(openfile)
    file, type = temp #dont change it
    if type == ".md":
        headline = False
        title_exist = False # if title exist
        date_exist = False  # if date exist
        line_num = 0
        text = []
        create_date = shift_time(openfile)
        for line in open(openfile, encoding='utf-8'):
            line_num += 1
            if line == "---\n":
                headline += 1
                continue
            if "date:" in line:
                date_exist = True
            if "title:" in line:
                title_exist = True
            if line_num == 10:
                break
        if date_exist and title_exist:# title and date correct
            shutil.copy2(path_output+filename, path_posts + filename)
            replace_pic_open_path(filename, path_posts + filename)
            print("Copyed!")

            return
        else:
            for line in open(openfile, encoding='utf-8'):
                # ignore my custom front matter
                if "isPublish:" in line:
                    continue
                if re.match( r'^\# ', line):
                    continue
                text.append(line)
            if date_exist == False:
                text.insert(3, "date: " + create_date + '\n')
            if title_exist == False:
                text.insert(1, "title: " + filename.replace(".md","") + '\n')
            if headline == 1:
                text.insert(0, "---\n")
        text = replace_pic_path_text(filename,text=text)

        writeback(post_path + filename,text)
        return

# main now
RenameTheImages.main()
rm_dir_content(path_posts)# clean the _posts folder

for root, dirnames, filenames in os.walk(path_output):
    for filename in filenames:
        for line in open(os.path.join(path_output, filename), encoding='utf-8'):
            if(line.find("isPublish: Yes") == 0):
                # record the filepath that gonna move to _posts
                file_output_path.append(os.path.join(root, filename))
                # record the filepath that gonna move to _posts
                file_output_name.append(filename)
                #break
    # sync the pic_name and path,in order to put the pic_name and img_list in a dic
    for num in range(0, len(file_output_path)):
        tmp_pic_list = []
        for line in open(file_output_path[num], encoding='utf-8'):
            # get the ![](../InsertPic/)
            pic_line = re.search("\!\[.*\]\(\.\.\/InsertPic\/.*\)", line)
            if(pic_line):
                # get the pic name and put it in the tmp_pic_list
                pic_name = re.search("\.\.\/InsertPic\/.*", pic_line.group())
                pic_name = pic_name.group()[:-1].replace("../InsertPic/", "")
                tmp_pic_list.append(pic_name)

        if(tmp_pic_list):
            # {filename: ['img1','img2']}
            pic_output_dic[file_output_name[num]] = tmp_pic_list
        else:
            pic_output_dic[file_output_name[num]] = ''
            #continue
    for filename in pic_output_dic.keys():
        file_equal_flag = 0
        print()
        print(filename)
        #if(os.path.isfile(path_posts + filename)):  # if destination file exit
        #    file_equal_flag = compare_file_md5(
        #        path_output+filename, path_posts + filename)
        #if(file_equal_flag):
        #    continue
        # copy the pic and md to the _posts
        #shutil.copy2(path_output+filename, path_posts + filename)
        copy_and_add_date_title(path_output, path_posts,filename)
        if pic_output_dic[filename]:
            #copy the pic to the _posts
            file_pic_folder = path_posts+"/" + filename[:-3]
            if not os.path.exists(file_pic_folder):
                # mkdir the {filename} folder in order to make hexo publish my pic
                os.makedirs(file_pic_folder)
            for pic_name in pic_output_dic[filename]:
                try:
                    shutil.copy2(path_insertpic+unquote(pic_name), file_pic_folder+"/"+unquote(pic_name))
                    print(pic_name)
                    print("Copyed!")
                except:
                    continue
                    #raise "copy pic error!"
            
        else:
            print()
            print(filename)
            print("Copyed!")
            continue
        
print("Done!")
time.sleep(2)
os.system(('cd {} && hexo clean && hexo gen && echo "mrbelieve.tech" > public/CNAME && hexo deploy').format("\""+ "/Users/mrbelieve/Documents/OneDrive/Blog/" + "\""))#cd {} && hexo clean && hexo gen && hexo deploy

