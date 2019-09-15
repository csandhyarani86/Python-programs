import re 
import sys 
import os

def edi_converter(string):
    contents= str(string)
    contents=re.sub(r"\\\*","",contents)
    contents=re.sub(r"\\.","",contents)
    contents=re.sub(r"\*O","",contents)
    contents=re.sub(r"''","",contents)
    contents=re.sub(r"\+","\x1d",contents)
    contents=re.sub(r":","\x1f",contents)
    contents=re.sub(r"'&","\x1c",contents)
    contents=re.sub(r"\*","\x19",contents)
    contents=re.sub(r"\n","",contents)
    contents=re.sub(r"\r","",contents)
    contents=re.sub(r"\'","\x1c",contents)
    print contents
    return contents

def Line_converter(Filepath):
    filepath = Filepath
    print filepath
    with open(filepath,'r') as filereader:
        file_Data = filereader.read()
        #print file_Data
        Temp_data = str(file_Data).replace('\r', '')
        Modified_data = str(Temp_data).replace('\n', '')
        return Modified_data

string = raw_input("enter the filepath: \n")


file=string.replace('.txt','.DATA')

edifact = edi_converter(Line_converter(string))
with open(file,'w') as fs:
    fs.write(edifact)

 
