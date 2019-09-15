import os
import sys
import zipfile
from lxml import etree

##################################################################################
# Home Directory path for all the python scripts Mandatory for import statements #
##################################################################################
if (len(sys.argv) > 1):
    sys.path.append(sys.argv[1])

from python.com.amadeus.datastaging.reconciliation.utils.CommonFunctions import write_to_file
from python.com.amadeus.datastaging.reconciliation.constants.Constants import *

#Extracts given zipfile and deletes the zip after unzip
def extract_single_zip_file(zipFileToExtract,pathToZipFiles):
	print "Extracting " + zipFileToExtract
	zip_ref = zipfile.ZipFile(zipFileToExtract, 'r')
	xmlfile = zip_ref.namelist()[0]
	zip_ref.extract(xmlfile,pathToZipFiles)
	zip_ref.close()
	return xmlfile

#Iterate over the main entities and generate the business keys.
def parse_business_elements(file_name):
	if (os.path.isfile(file_name)):
		print "Parsing business elements from file" + file_name
		print "====== For file:" + file_name + "======"
		tree = etree.parse(file_name)
		root = tree.getroot()
		bcount = extract_business_key(root,output_dir,ELEM_BOOKING)
		print '#Bookings:',bcount
		emdcount = extract_business_key(root,output_dir,ELEM_EMD)
		print '#Emd:',emdcount
		fldcount = extract_business_key(root,output_dir,ELEM_FLIGHT)
		print '#FLD:',fldcount
		pnrcount = extract_business_key(root,output_dir,ELEM_PNR)
		print '#PNR:',pnrcount
		tktcount = extract_business_key(root,output_dir,ELEM_TICKET)
		print '#TKT:',tktcount
		root.clear()
	else:
		print "XML File " + file_name + " not found"

#Iterate over the main entities and generate the business keys.
def extract_business_key(root,output_dir,elem_type):
    parent_list = list()
    elements = root.findall(elem_type)
    for element in elements:
        adsID = element.get("adsUniqueID","None")
        if (adsID != "None"):
            parent_list.append(adsID)

    elemcount = len(parent_list)
    if (elemcount > 0):
        write_to_file(output_dir+DIRECTORY_DELIMETER+elem_type+"_Business_key.csv",parent_list)
    return elemcount

if __name__ == '__main__':
    #Code base Home Directory : Directory path for Python code base
    #Input Directory : Input Directory for XML Files
    #Output Directory : Directory path for the business key dumps.

    if (len(sys.argv) >= 3):
        inputDir = sys.argv[2]
        output_dir = sys.argv[3]
        for file in os.listdir(inputDir):
			print "Processing " + file
			if file.endswith(".zip"):
				print "zipfile is " + file
				zip_file_with_path = os.path.join(inputDir,file)
				xmlfilename = extract_single_zip_file (zip_file_with_path,inputDir)
				print "xml file unzipped as " + xmlfilename
				xmlfile = inputDir + DIRECTORY_DELIMETER + xmlfilename
				parse_business_elements(xmlfile)
				print "Processing of files ["+ zip_file_with_path + "," + xmlfile + "] completed. Now deleting them"
				os.remove(zip_file_with_path)
				os.remove(xmlfile)
    else:
        print "Please provide the arguments in following order: "
        print "1. Home directory path for Python code : "
        print "2. Input Directory path for XML files : "
        print "3. Output Directory path for Outfile : "