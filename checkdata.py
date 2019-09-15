import os
import sys
#import xml.etree.ElementTree as ET
import lxml
from lxml import etree

import win32com
import win32com.client
from Tkinter import Tk
from tkFileDialog import askopenfilename



Tk().withdraw()
filename = askopenfilename()
print(filename)
filename1 = askopenfilename()
print filename1
#Parsing XML Feed
tree = etree.parse(filename)
#tree = etree.parse('D:/NewFeed_02-03-16/nexti_dw_UAT_A94a6d760-dee4-11e5-9009-a5b1162220cc/nexti_dw_UAT_1602291000_1602291100.xml')
root = tree.getroot()
tree1 = etree.parse(filename1)
#tree1 = etree.parse('D:/NewFeed_02-03-16/nexti_dw_UAT_A94a6d760-dee4-11e5-9009-a5b1162220cc/nexti_dw_UAT_1602291000_1602291100.xml')
root1 = tree1.getroot()

#LOG Generation
fs = open("D://logger.txt","a+")

#Finding PNR and Bookings in the Feed
elem_PNR_ADN = root.findall('PNR')
elem_BOOKING_ADN = root.findall('Booking')
elem_PNR_NEXTI = root1.findall('PNR')
elem_BOOKING_NEXTI = root1.findall('Booking')

TotalCount_PNR_ADN = len(elem_PNR_ADN)
TotalCount_Booking_ADN = len(elem_BOOKING_ADN)
TotalCount_PNR_NEXTI = len(elem_PNR_NEXTI)
TotalCount_Booking_NEXTI = len(elem_BOOKING_NEXTI)


#print "TotalCount_Booking_ADN :"
#print TotalCount_Booking_ADN
#print "\n"
#print "TotalCount_Booking_NEXTI :"
#print TotalCount_Booking_NEXTI
#print "\n"


# Check of total count of PNR and Bookings in the Feed.
if TotalCount_Booking_ADN == TotalCount_Booking_NEXTI:
    print "Total Booking Count Match"
else:
   print "Booking count Doesn't Match"
   fs.write("Total Booking count doesn't match\n")
  
if TotalCount_PNR_ADN == TotalCount_PNR_NEXTI:
    print "Total PNR Count Match"
else:
   print "PNR count Doesn't Match"
   fs.write("Total PNR count doesn't match\n")

#fs.close()  

# Looping for no. of Bookings in ADN and NEXTI
for i in range (0,TotalCount_Booking_ADN):
  PNR_rloc_ADN = elem_BOOKING_ADN[i].attrib.get('pnr_rloc')
  BKG_Tattoo_ADN = elem_BOOKING_ADN[i].attrib.get('BKG_Tattoo')
  links = elem_BOOKING_ADN[i].getchildren() 
  Links_count_ADN = len(links)
  for j in range (0,TotalCount_Booking_NEXTI):
       PNR_rloc_NEXTI = elem_BOOKING_NEXTI[j].attrib.get('pnr_rloc')
       links1 = elem_BOOKING_NEXTI[j].getchildren()
       Links_count_NEXTI = len(links1)
       print PNR_rloc_ADN
       print PNR_rloc_NEXTI
       fs.write("ADN_rloc :")
       fs.write(PNR_rloc_ADN)
       fs.write("\n")
       fs.write("Nexti_rloc :")
       fs.write(PNR_rloc_NEXTI)
       fs.write("\n")

      
       if (str(PNR_rloc_ADN) == str(PNR_rloc_NEXTI)):
           BKG_Tattoo_NEXTI = elem_BOOKING_NEXTI[j].attrib.get('BKG_Tattoo')
          # print  BKG_Tattoo_NEXTI
          # print  BKG_Tattoo_ADN
          # j = j +1
           if BKG_Tattoo_ADN == BKG_Tattoo_NEXTI:
               print " found the Booking Tattoo"
               List1 = list(elem_BOOKING_ADN[i].attrib.keys())
               ADN_Attrib_Count = len(List1)
               List2 = list(elem_BOOKING_NEXTI[j].attrib.keys())
               NEXTI_Attrib_Count = len(List2)
               if ADN_Attrib_Count == NEXTI_Attrib_Count:
                  print " Attribute count match\n"
               else:
                  print " Attribute count Doesn't match\n"
                  print ("NEXTI_Attrib_Count")
                  print NEXTI_Attrib_Count
                  print ("\n")
                  print ("ADN_Attrib_Count")
                  print ADN_Attrib_Count
                  print ("\n")
               for m in range (0,ADN_Attrib_Count):
                      #print List1[m]
                  ADN_Attrib = elem_BOOKING_ADN[i].attrib.get(List1[m])
                  for n in range (0,NEXTI_Attrib_Count):
                         # NEXTI_Attrib = elem_BOOKING_NEXTI[j].attrib.get(List2[n])
                         # print NEXTI_Attrib
                    #print List1[m]
                    ADN_Attrib_Value = elem_BOOKING_ADN[i].attrib.get('%s'%List1[m])
                    NEXTI_Attrib_Value = elem_BOOKING_NEXTI[j].attrib.get('%s'%List2[n])    
                    if List1[m] == List2[n]:
                       #print List1[m]
                       #print ADN_Attrib_Value
                       #print NEXTI_Attrib_Value
                       if (str(ADN_Attrib_Value) != str(NEXTI_Attrib_Value)):
                          #print ADN_Attrib_Value
                          #print NEXTI_Attrib_Value
                          fs.write("\n")
                          fs.write("Parent tag like Booking, PNR .. validation ")
                          fs.write("Attribute value doesn't match\n")
                          fs.write("Attribute name :%s" %List1[m])
                          #fs.write(List1[m])
                          fs.write("\n")
                         # break
                          #break
                          #break
                       else:
                           continue
                    n = n+1
                  m = m+1
               for k in range (0,Links_count_ADN):
                  Child_link_ADN = links[k].getchildren()
                  print Child_link_ADN
                  ADN_Link_Attrib_List = links[k].attrib.keys()
                  ADN_LINKS_Attrib_Count = len(ADN_Link_Attrib_List)
                  for o in range (0,ADN_LINKS_Attrib_Count):
                      ADN_Link_Attrib = links[k].attrib.get(ADN_Link_Attrib_List[o])
                      for l in range (0,Links_count_NEXTI):
                          Child_link_NEXTI = links1[l].getchildren()
                          NEXTI_Link_Attrib_List =  links1[l].attrib.keys()
                          NEXTI_LINKS_Attrib_Count = len(NEXTI_Link_Attrib_List)
                          for p in range (0,NEXTI_LINKS_Attrib_Count):
                             ADN_Link_Attrib_Value = links[k].attrib.get(ADN_Link_Attrib_List[o])
                             NEXTI_Link_Attrib_Value = links1[l].attrib.get(NEXTI_Link_Attrib_List[p])
                             if ADN_Link_Attrib_List[o] == NEXTI_Link_Attrib_List[p]:
                                if (str(ADN_Link_Attrib_Value) != str(NEXTI_Link_Attrib_Value)):
                                   fs.write("\n")
                                   fs.write("\n")
                                   fs.write("Child Tag Attributes validation follows.")
                                   fs.write("\n")
                                   fs.write("Link Attribute value doesn't match\n")
                                   fs.write("Attribute name : %s" %ADN_Link_Attrib_List[o])
                                   #fs.write(ADN_Link_Attrib_List[o])
                                   fs.write("\n")
                                   break
                                   break
                                   break
                                else:
                                   continue
                             p = p + 1
                          #for g in range (0,NEXTI_LINKS_Attrib_Count):
                             
                          len1 = len(Child_link_ADN)
                          len2 = len(Child_link_NEXTI)
                          if len1 != '0':
                             print "No child element"
                          else:
                              print "Child Element present"
                              print Child_link_ADN
                              #ADN_Childlink_Attrib_List = Child_link_ADN.attrib.keys()
                              #ADN_Childlink_Attrib_Count = len(ADN_Childlink_Attrib_List)
                                                     
                              if len2 != '0':
                                 print "No child element"
                              else:
                                 print "Child Element present"
                                 print Child_link_NEXTI
                                 if (str(Child_link_ADN) ==  str(Child_link_NEXTI)) and (not Child_link_ADN):
                                     print Child_link_ADN
                                     test = len(Child_link_ADN)
                                     print len(Child_link_NEXTI)
                                    # print Child_link_ADN[k].attrib.keys()
                                    
                          l = l + 1
                          
                      o = o + 1
                  
               
                  k = k + 1                                           
       #break 
      
       j = j + 1
      
  i = i +1    
 
fs.close()
