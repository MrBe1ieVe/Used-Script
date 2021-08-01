# -*- coding:utf-8 -*-


import os
import time
import re
path_py = os.path.dirname(__file__)

mac_ob_path = "../../Library/Mobile Documents/iCloud~md~obsidian/Documents/Note Vault"

path_output = path_py[:path_py.index(
    "Used script")] + mac_ob_path + "/OutPut/"  # relative path
path_insertpic = path_py[:path_py.index(
    "Used script")] + mac_ob_path + "/InsertPic/"

# write back to the file
def writeback(filepath, text):
    s = ''.join(text)
    with open(filepath, "w", encoding='utf-8',) as f:
        f.write(s)

# find and rename the images name and update the markdown `file
def rename_the_images(path, filename):
    openfile = path + filename
    text = []
    Renamed = False
    try:
        for line in open(openfile, encoding='utf-8'):
            pic_line = re.search("\.\.\/InsertPic\/Pasted%20image", line)
            if(pic_line):

                old_image_name = re.findall("Pasted%20image%20\d*\.png",line)[0]
                new_image_name = re.findall("image%20\d*\.png",line)[0].replace("%20","-")# formate the name like typora pasted image name
                line = line.replace(old_image_name, new_image_name)
                print(line + "Replaced!\n")
                old_image_name = old_image_name.replace("%20", " ")# formate the path
                try:
                    os.rename(path_insertpic+old_image_name, path_insertpic+new_image_name)
                    Renamed = True
                except:
                    raise "Rename Error!"

            text.append(line)
    except:
        raise filename + 'Error!'
    if(Renamed):
        writeback(path + filename, text)
    else:
        return
    return


def check_the_markdown():
    for root, dirnames, filenames in os.walk(path_output):
        for filename in filenames:
            for line in open(os.path.join(path_output, filename), encoding='utf-8'):
                if(line.find("isPublish: Yes") == 0):# My custom setting 
                    try:
                        rename_the_images(path_output, filename)
                    except:
                        raise filename+" Error!"

def main():
    check_the_markdown()
    print("ReNameImages Done!\n")
    time.sleep(2)


if __name__ == "__main__":
    main()
