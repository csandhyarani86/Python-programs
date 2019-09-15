import os
import sys
from lxml import etree
import logging

from time import gmtime, strftime,mktime


## LOGGING CONFIGURATION ##
def initLogger(logging,outputDir,log_level):
    date_time = strftime("%Y_%m_%d_%H_%M_%S", gmtime())
    # logger
    logging.basicConfig(level=log_level)
    formatter = logging.Formatter('%(message)s')
    #formatter = logging.Formatter('%(message)s')
    # first file logger
    logFileName = outputDir + "/"+ date_time + ".log"
    logger = logging.getLogger('data_migration')
    handler = logging.FileHandler(logFileName)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False
    return logger

def getAttributeDict(root,tagName):
    attribDict = dict()
    elements = root.findall(tagName)
    for element in elements:
        adsUniqueID = element.get("adsUniqueID")
        attribDict[adsUniqueID] = element
    return attribDict

def text_compare(t1, t2):
    if not t1 and not t2:
        return True
    if t1 == '*' or t2 == '*':
        return True
    return (t1 or '').strip() == (t2 or '').strip()

def xml_compare(x1, x2, logger):
    if x1.tag != x2.tag:
        logger.info('Tags do not match: %s and %s' % (x1.tag, x2.tag))
        return False
    for name, value in x1.attrib.items():
        if x2.attrib.get(name) != value:
            logger.info('Attributes do not match: %s=%r, %s=%r'% (name, value, name, x2.attrib.get(name)))
            return False
    for name in x2.attrib.keys():
        if name not in x1.attrib:
            logger.info('x2 has an attribute x1 is missing: %s'% name)
            return False
    if not text_compare(x1.text, x2.text):
        logger.info('text: %r != %r' % (x1.text, x2.text))
        return False
    if not text_compare(x1.tail, x2.tail):
        logger.info('tail: %r != %r' % (x1.tail, x2.tail))
        return False
    cl1 = x1.getchildren()
    cl2 = x2.getchildren()
    if len(cl1) != len(cl2):
        logger.info('children length differs, %i != %i' % (len(cl1), len(cl2)))
        return False
    i = 0
    for c1, c2 in zip(cl1, cl2):
        i += 1
        if not xml_compare(c1, c2, logger):
            logger.info('children %i do not match: %s' % (i, c1.tag))
            return False
    return True


def validateAttributes(primary_root,secondary_root,tagName):
    #logger = initLogger(logging,output_dir,"INFO",tagName)
    seocndary_attrib_dict = getAttributeDict(secondary_root,tagName)
    print "Validation of Attribute starts: " + tagName
    prim_elements = primary_root.findall(tagName)
    for element in prim_elements:
        primaryAdsUniqueID = element.get("adsUniqueID")
        sec_elem = seocndary_attrib_dict.get(primaryAdsUniqueID,"None")
        if (sec_elem == "None"):
            logger.info(tagName + " Primary ADSUniqueID: " + primaryAdsUniqueID +" is not found in the Secondary XML :")
        else:
            result = xml_compare(element,sec_elem,logger)
            if not result:
                logger.info(tagName + " Attributes doesnt matches for ADSUniqueID : " + str(primaryAdsUniqueID))

def validateAttributesTSM(primary_root,secondary_root,tagName):
    prim_elements = primary_root.findall(tagName)
    sec_elements = primary_root.findall(tagName)
    for pri,sec in zip(prim_elements,sec_elements):
        result = xml_compare(pri,sec,logger)
        if not result:
            adsUniqueID = pri.get("adsUniqueID")
            logger.info(tagName + " Attributes doesnt matches for ADSUniqueID : " + str(adsUniqueID))



if __name__ == '__main__':
    if len(sys.argv) >= 2:
        input_dir1 = sys.argv[1]
        input_dir2 = sys.argv[2]
        output_dir = sys.argv[3] + "\\"
    else:
        input_dir1 = raw_input("Please provide the input directory path 1: ")
        input_dir2 = raw_input("Please provide the input directory path 2: ")
        output_dir = raw_input("Please provide the output directory path for logger: ")
    logger = initLogger(logging,output_dir,"INFO")
    for file in os.listdir(input_dir1):
        tree = etree.parse(input_dir1+"\\"+file)
        primary_root = tree.getroot()
    for file1 in os.listdir(input_dir2):
        tree1 = etree.parse(input_dir2+"\\"+file1)
        secondary_root = tree1.getroot()

    validateAttributes(primary_root,secondary_root,"Ticket")
    validateAttributes(primary_root,secondary_root,"Flight")
    validateAttributes(primary_root,secondary_root,"TST")
    validateAttributes(primary_root,secondary_root,"Grouping")
    validateAttributes(primary_root,secondary_root,"EMD")
    validateAttributes(primary_root,secondary_root,"AuxSVC")
    validateAttributesTSM(primary_root,secondary_root,"TSM")
    validateAttributes(primary_root,secondary_root,"Booking")
    validateAttributes(primary_root,secondary_root,"PNR")
    primary_root.clear()
    secondary_root.clear()