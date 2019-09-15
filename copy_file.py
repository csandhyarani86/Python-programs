import os
import sys

def file_change(strtest):
  
 for file in os.listdir(r'D:\PRD2\Messages\New folder'):
     file1 = str(file).split('.')
     filepath = "D:\PRD2\Messages\New folder" + "\\" + file1[0] + ".edi"
     fs = open(r'file','r+')
     readfile = fs.readlines()
     fs1 = open(r'filepath','w+')
     fs1.write(readfile)
     fs.close()
     fs1.close()

file_change('D:\PRD2\Messages\New folder')     
