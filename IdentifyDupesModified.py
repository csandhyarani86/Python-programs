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
filename = sys.argv[1]
print "Source Directory for XML files : "+filename
Resultfile2 = str(sys.argv[2])+ "/"
print "Target Directory for Output files : "+Resultfile2

parentList = []
def xmlcompare(Elem_Type,root,Resultfile2,str2):
	elements = root.findall(Elem_Type)
	#print elem_Check
	list1 = ""
	parentList = list(list1)
	childList = list(list1)
	subChildList = list(list1)
	parentSet = set()
	childSet = set()
	subChildSet = set()
	str1 =""
	dup = list(str1)
	dup1 = list(str1)
	dup3 = list(str1)
	Resultfile = Resultfile2 + Elem_Type + "_Parent_Tag_Logger_" + str2 + "_.txt"
	#print str2
	Resultfile1 = Resultfile2 + Elem_Type + "_Child_Tag_Logger_" + str2 + "_.txt"
	Resultfile3 = Resultfile2 + Elem_Type + "_Sub_Child_Tag_Logger_" + str2 + "_.txt"
	for element in elements:
                if (Elem_Type != "AuxSVC"):
			adsID = element.get("adsUniqueID") 
		else:
			adsID = element.get("adsUniqueId")
		if (adsID != None):
			if adsID in parentSet:
				parentList.append(adsID)
				#element.getparent().remove(element)
			else:
				parentSet.add(adsID)
		childElements = element.getchildren()
		for childElement in childElements:
			tagName = childElement.tag
			if not (tagName == ('TicketingArrangement' ) or tagName ==('AccountingDetails')or tagName == ('Passenger') or tagName == ('Remark')):
				if (Elem_Type != "AuxSVC"):
					childadsID = childElement.get("adsUniqueID")
				else:
					childadsID = childElement.get("adsUniqueId")
				if (childadsID != None):
					if childadsID in childSet:
						childList.append(childadsID)
					else:
						childSet.add(childadsID)
			subChildElements = childElement.getchildren()
			for subChildElement in subChildElements:
				if (Elem_Type != "AuxSVC"):
					subChildadsID = subChildElement.get("adsUniqueID")
				else:
					subChildadsID = subChildElement.get("adsUniqueId")
				if (subChildadsID != None):
					if subChildadsID in subChildSet:
						subChildList.append(subChildadsID)
					else:
						subChildSet.add(subChildadsID)
	if (len(parentList) > 0):
		writeToFile(Resultfile,parentList)
	if (len(childList) > 0):
		writeToFile(Resultfile1,childList)
	if (len(subChildList) > 0):
		writeToFile(Resultfile3,subChildList)
	
	
def writeToFile(fileName,dupDataList):
	dup = list(set(dupDataList))
	fs = open(fileName,"a+")
	for i in dup:
		fs.write(i)
		fs.write("\n")
	fs.close()
	
			
#Resultfile2 = raw_input("Enter the Logger Path : (ex: D:\XML_Compare\XML Compare\Results\) : ")
#filename = raw_input("Enter the NEXTI XML Path : (ex: D:\XML_Compare\TestData\NEXTI) : ")
Element_Booking = "Booking"
Element_PNR = "PNR"
Element_Ticket = "Ticket"
Element_Flight = "Flight"
Element_TST = "TST"
Element_Grouping = "Grouping"
Element_EMD = "EMD"
Element_Aux_SVC = "AuxSVC"
Element_TSM = "TSM"
for file1 in os.listdir(filename):
	if file1.endswith(".xml"):
		file1 = filename + "/"+ file1
		#print file1
		if 'nexti' in file1:
			filename1 = str(file1).split('.')
			filename2 = str(filename1[0]).split('_')
			l1 = len(filename2)
			str2 = filename2[l1-1]
			#print str2
		else :
			filename1 = str(file1).split('.')
			filename2 = str(filename1[0]).split('_')
			l1 = len(filename2)
			str2 = filename2[l1-2]
			#print str2
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
		root.clear()



   
