#_____________________________________________________________________________

#Script Title: ADSUNIQUEID_Duplicate_Finder
#Description : Script logs the all duplicate records of adsuniqueID
#Author : Bharathkumar C
#Date : 28-04-2016

#______________________________________________________________________________



import os
import sys
import lxml
from lxml import etree

#import win32com
#import win32com.client
from Tkinter import Tk


list_adsuniqeid = []
def xmlcompare(Elem_Type,root,Resultfile2,str2):
    elem_Check = root.findall(Elem_Type)
    Total_ElementCount = len(elem_Check)
    list1 = ""
    list_adsuniqeid = list(list1)
    Child_list_adsuniqeid = list(list1)
    str1 =""
    dup = list(str1)
    dup1 = list(str1)
    dup3 = list(str1)
    Sub_Child_list_adsuniqeid = list(list1)                                          
    Resultfile = Resultfile2 + Elem_Type + "_Parent_Tag_Logger_" + str2 + "_.txt"
    #print str2
    Resultfile1 = Resultfile2 + Elem_Type + "_Child_Tag_Logger_" + str2 + "_.txt"
    Resultfile3 = Resultfile2 + Elem_Type + "_Sub_Child_Tag_Logger_" + str2 + "_.txt"
    for i in range (0,Total_ElementCount):
        list_Attrib = elem_Check[i].attrib.keys()
        Child_elem = elem_Check[i].getchildren()
        Child_elem_count = len(Child_elem)              
        if 'adsUniqueID' in list_Attrib:    
           adsunqid = elem_Check[i].attrib.get("adsUniqueID")          
           list_adsuniqeid.append(adsunqid)
        for k in range(0,Child_elem_count):
            elem_check = str(Child_elem[k]).split(' ')                   
            Child_list_Attrib = Child_elem[k].attrib.keys()
            if 'adsUniqueID' in Child_list_Attrib:                
                   Child_adsunqid = Child_elem[k].attrib.get("adsUniqueID")
                   Child_list_adsuniqeid.append(Child_adsunqid)
            Sub_Child_elem  =  Child_elem[k].getchildren()
            Sub_Child_elem_count = len(Sub_Child_elem)
            for m in range (0,Sub_Child_elem_count):
                Sub_Child_list_Attrib = Sub_Child_elem[m].attrib.keys()
                if 'adsUniqueID' in Sub_Child_list_Attrib:                
                    Sub_Child_adsunqid = Sub_Child_elem[m].attrib.get("adsUniqueID")
                    Sub_Child_list_adsuniqeid.append(Sub_Child_adsunqid)
    len2 = len(Child_list_adsuniqeid)           
    len1 = len(list_adsuniqeid)
    len3 = len(Sub_Child_list_adsuniqeid)
    for j in range (0,len1):
        count = list_adsuniqeid.count(list_adsuniqeid[j])
        if count > 1:
            dup.append(list_adsuniqeid[j])
    dup_data = list(set(dup))
    for p in range (0,len(dup_data)) :
            fs = open(Resultfile,"a+")
            fs.write("\n")
            fs.write(dup_data[p])
            fs.write("\n")
            fs.close()
    for l in range (0,len2):
        count = Child_list_adsuniqeid.count(Child_list_adsuniqeid[l])
        dup2 = ""
        if count > 1:
            dup1.append(Child_list_adsuniqeid[l])
    dup2 = list(set(dup1))
    for o in range (0,len(dup2)) :
            fs1 =  open(Resultfile1,"a+")
            fs1.write("\n")
            fs1.write(dup2[o])
            fs1.write("\n")
            fs1.close()
    for n in range (0,len3):
        count = Sub_Child_list_adsuniqeid.count(Sub_Child_list_adsuniqeid[n])
        dup4 = ""
        if count > 1:
            dup3.append(Sub_Child_list_adsuniqeid[n])
    dup4 = list(set(dup3))
    for r in range (0,len(dup4)) :
            fs2 =  open(Resultfile3,"a+")
            fs2.write("\n")
            fs2.write(dup4[r])
            fs2.write("\n")
            fs2.close()   
Resultfile2 = raw_input("Enter the Logger Path : (ex: D:\XML_Compare\XML Compare\Results\) : ")
filename = raw_input("Enter the NEXTI XML Path : (ex: D:\XML_Compare\TestData\ADN) : ")
Element_Booking = "Booking"
Element_PNR = "PNR"
Element_Ticket = "Ticket"
Element_Flight = "Flight"
Element_Aux_SVC = "AuxSVC"
Element_TST = "TST"
Element_Grouping = "Grouping"
Element_EMD = "EMD"
Element_Aux_SVC = "AuxSVC"
Element_TSM = "TSM"
for file1 in os.listdir(filename):
    if file1.endswith(".xml"):
        file1 = filename + file1        
        if 'nexti' in file1:
           filename1 = str(file1).split('.')
           filename2 = str(filename1[0]).split('_')
           l1 = len(filename2)
           str2 = filename2[l1-1]          
        else :
           filename1 = str(file1).split('.')
           filename2 = str(filename1[0]).split('_')
           l1 = len(filename2)
           str2 = filename2[l1-2]           
        tree = etree.parse(file1)
        root = tree.getroot()
        xmlcompare(Element_Booking,root,Resultfile2,str2)
        xmlcompare(Element_PNR,root,Resultfile2,str2)
        xmlcompare(Element_Ticket,root,Resultfile2,str2)
        xmlcompare(Element_Flight,root,Resultfile2,str2)
        xmlcompare(Element_TST,root,Resultfile2,str2)
        xmlcompare(Element_Grouping,root,Resultfile2,str2)        
        xmlcompare(Element_EMD,root,Resultfile2,str2)        
        xmlcompare(Element_Aux_SVC,root,Resultfile2,str2)        
        xmlcompare(Element_TSM,root,Resultfile2,str2)
        



   
