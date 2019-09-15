import re
from xlrd import open_workbook
from xlutils.copy import copy

def JSON_XPATH_Converter(strJpath):
    XML_ParentTag_add = strJpath.replace("$['","/DCSFMLeg/")
    Intermediate_Jpath_convert = XML_ParentTag_add.replace("['","/")                        
    Replaced_Jpath = Intermediate_Jpath_convert.replace("']","")
    Jpath_Object_Split = Replaced_Jpath.split('[')
    Jpath_Array_length = len(Jpath_Object_Split)
    list1 = []
    if Jpath_Array_length > 1:
        for i in range (1,Jpath_Array_length):
           list1.append(Jpath_Object_Split[i].replace(str(Jpath_Object_Split[i][0]),str(int(Jpath_Object_Split[i][0]) + 1)))
        s = '['
        Intermediate_Xpath = s.join(list1)
        XML_seq = (Jpath_Object_Split[0],Intermediate_Xpath)
        XML_Path = s.join(XML_seq)
    else :
        XML_Path = Replaced_Jpath
    return XML_Path
Excel_path = raw_input("Input Excel file path: \n")
wb = open_workbook(Excel_path)  
s = wb.sheet_by_index(0)
maxrows = s.nrows
for row_idx in range(1, maxrows):
    s = wb.sheet_by_index(0)
    JSon_Path = s.cell(row_idx, 2).value
    json_Expected_Value = s.cell(row_idx, 1).value
    #print JSon_Path
    xpath = JSON_XPATH_Converter(JSon_Path)
    #print xpath
    rb = open_workbook(Excel_path, formatting_info=True)
    ws = copy(rb)
    s = ws.get_sheet(0)
    s.write(row_idx,3,xpath)
    s.write(row_idx,4,json_Expected_Value)
    ws.save(Excel_path)



