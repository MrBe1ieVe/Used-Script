# Used to import my hexo note to obsidian
import os
import re
import shutil


path = os.getcwd()  # get pwd
filepath = []
filename = []
despathNote = "C:\\Users\\{{UserName}}\\OneDrive\\Note Vault\\ImportTmp\\"
despathPic = "C:\\Users\\{{UserName}}\\OneDrive\\Note Vault\\InsertPic\\"
for root, dirs, files in os.walk(path):
    for name in files:
      filepath.append(os.path.join(root, name))
      filename.append(os.path.join(name)) # record the filename and filepath
      #input()

for num in range(0,len(filepath)):
    if(re.search('.md',filepath[num])): # move markdown file to my obsidian vault
        print()
        print(filepath[num])
        print(filename[num])
        print(despathNote + filename[num])
        print()
        try:
            shutil.move(filepath[num], despathNote+filename[num])
        except:
            raise "move failed!"
           
        continue
    print()                             # move pic  to my obsidian vault/Pic folder
    print(filepath[num])
    print(filename[num])
    print(despathPic + filename[num])
    print()
    try:
        shutil.move(filepath[num], despathPic+filename[num])
    except:
        raise "move failed!"
       
    continue
        
