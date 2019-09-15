# !/usr/bin/python

import os
import string
import shutil
list2 = []
i = 0
j = 0 
l1 = list(string.ascii_uppercase)
for root, dirs, files in os.walk("D:\Test\003 - Multisegment", topdown=False):
    for name in dirs:
        #print(os.path.join(root,name))
        filepath = os.path.join(root,name)
        i = i + 1
        j = 0
        for file in os.listdir(filepath):
            file1 = file.split('_',1)
            string_new = '0' + str(i) + '_'
            file2 = l1[j] + string_new + file1[1]
            newfile = os.path.join("D:\Test\003 - Multisegment",file2)
            #newfile = os.path.join("D:\Test\Boarding_USA", file.split("_",1)[1])
            print newfile
            #appendvalue = 'A01_' + newfile
            shutil.move(os.path.join("D:\Test\003 - Multisegment",file),newfile)
            j = j + 1
        list2.append(filepath)
        #os.rename(os.path.join(root, i), os.path.join(root, "changed" + str(count) + ".txt"))
    print list2
    #for 



# !/usr/bin/python

import os
for root, dirs, files in os.walk("D:\Test\Boarding_USA", topdown=False):
    for file in files:
        #print(os.path.join(root, file))
        list1 = str(file).split('_')
        print file
        print list1[1]
        #str(file).rename()
        
    #for name in dirs:
    #    print(os.path.join(root, name))
l1 = list(string.ascii_uppercase)
print l1[i]


for file in os.listdir("D:\Test\003 - Multisegment"):
    file1 = file.split('_',1)
    file2 = l1[j] + '01_' + file1[1]
    newfile = os.path.join("D:\Test\Boarding_USA",file2)
    #newfile = os.path.join("D:\Test\Boarding_USA", file.split("_",1)[1])
    #print newfile
    #appendvalue = 'A01_' + newfile
    shutil.move(os.path.join("D:\Test\Boarding_USA",file),newfile)
    j = j + 1
