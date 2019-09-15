# !/usr/bin/python

import os
import string
import shutil
list2 = []
i = 0
j = 0 
l1 = list(string.ascii_uppercase)
for file in os.listdir("D:\Test\Test"):
    file1 = file.split('_',1)
    print file1
    #exit()
    file2 = l1[j] + '01_' + file1[1]
    newfile = os.path.join("D:\Test\Test",file2)
    #newfile = os.path.join("D:\Test\Boarding_USA", file.split("_",1)[1])
    #print newfile
    #appendvalue = 'A01_' + newfile
    shutil.move(os.path.join("D:\Test\Test",file),newfile)
    j = j + 1
