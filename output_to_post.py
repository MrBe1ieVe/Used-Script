# -*- coding:utf-8 -*-
import os
import re
import shutil
import hashlib
import datetime

path_py = os.path.dirname(os.path.abspath(__file__))
path_py = os.path.normpath(path_py)
path_output = path_py[:path_py.index("Used script")] + "/Note Vault/OutPut/"
path_posts = path_py[:path_py.index("Used script")] + "/Blog/source/_test/" #path_py[:path_py.index(    "Used script")] + "/Blog/source/_posts/"  
path_insertpic = path_py[:path_py.index(
    "Used script")] + "/Note Vault/InsertPic/"
file_output_path = []
pic_output_path = []
file_output_name = []
pic_output_dic = {}

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


def writeback(filename, text):
    s = ''.join(text)
    with open(filename, "w", encoding='utf-8',) as f:
        f.write(s)

# compare md5
def compare_file_md5(origin_file, des_file):  
    md5_hash = hashlib.md5()
    # if(os.path.isfile(des_file)):# destination file doesnt exist
    #    return False
    with open(origin_file, 'r', encoding='utf-8') as ori, open(des_file, 'r', encoding='utf-8') as des:
        origin_blocks = ori.read(1024).encode('utf-8')
        des_blocks = des.read(1024).encode('utf-8')
        try:
            origin_md5 = md5_hash.update(origin_blocks)
            des_md5 = md5_hash.update(des_blocks)
            if(origin_md5 == des_md5):
                return True
            else:
                return False
        except:
            raise "ERROR"

# untested
def replace_pic_path():
    pass

def copy_and_add_date(origin_path, post_path,filename):
    openfile = origin_path + filename
    temp = os.path.splitext(openfile)
    file, type = temp
    if type == ".md":
        headline = False
        head_exist = False
        date_exist = False
        line_num = False
        create_date = shift_time(openfile)
        for line in open(openfile, encoding='utf-8'):
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
            shutil.copy2(path_output+filename, path_posts + filename)
            return
        elif head_exist:
            text = []
            for line in open(openfile, encoding='utf-8'):
                text.append(line)
            text.insert(1, "date: " + create_date + '\n')
            return
        else:
            text = []
            for line in open(filename, encoding='utf-8'):
                text.append(line)
            text.insert(0, "---\ndate: " + create_date + '\n---\n')
        # writeback(post_path + filename,text)
            return


for root, dirnames, filenames in os.walk(path_output):
    for filename in filenames:
        for line in open(os.path.join(path_output, filename), encoding='utf-8'):
            if(line.find("isPublish: Yes") == 0):
                # record the filepath that gonna move to _posts
                file_output_path.append(os.path.join(root, filename))
                # record the filepath that gonna move to _posts
                file_output_name.append(filename)
                break
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
            continue
    for filename in pic_output_dic.keys():
        file_equal_flag = 0
        print(filename)
        if(os.path.isfile(path_posts + filename)):  # if destination file exit
            file_equal_flag = compare_file_md5(
                path_output+filename, path_posts + filename)
        if(file_equal_flag):
            continue
        # copy the pic and md to the _posts
        #shutil.copy2(path_output+filename, path_posts + filename)
        copy_and_add_date(path_output, path_posts,filename)
        #copy the pic to the _posts
        file_pic_folder = path_posts+"/" + filename[:-3]
        if not os.path.exists(file_pic_folder):
            # mkdir the {filename} folder in order to make hexo publish my pic
            os.makedirs(file_pic_folder)
        for pic_name in pic_output_dic[filename]:
            shutil.copy2(path_insertpic+pic_name, file_pic_folder+"/"+pic_name)
            print(pic_name)
        print("Copyed!")
        print()

print(path_py)
print(path_output)
print(file_output_path)
