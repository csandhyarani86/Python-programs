import os
import sys
#import xml.etree.ElementTree as ET
import lxml
from lxml import etree

import win32com
import win32com.client


tree = etree.parse('D:/NewFeed_02-03-16/nexti_dw_UAT_A94a6d760-dee4-11e5-9009-a5b1162220cc/nexti_dw_UAT_1602291000_1602291100.xml')
root = tree.getroot()
print root.attrib.keys()
pnr_rloc1 = '274D73'
#for booking in root.find('Booking'):
   # print booking.get('BKG_Tattoo')
element = tree.xpath("//Booking[@pnr_rloc = '%s']"%pnr_rloc1)
print element


elem = root.find('Booking')
List1 = list(elem.attrib.keys())
print len(List1)

print List1[0]
print elem.attrib.get(List1[0])
elem1 = root.findall('Booking')
print len(elem1)
print elem1[3].attrib.get('BKG_Tattoo')
print elem1[3].attrib.get('pnr_rloc')
print elem.attrib.get(List1[0])
