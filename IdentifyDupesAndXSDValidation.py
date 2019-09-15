#Script Title: ADSUniqueID Duplicate Removal Script
#Description : This script will log the Duplicate ADSID's in the logger and remove those specific tags from XML for full automation.

import os
import sys
import lxml
from lxml import etree

def xmlcompare(Elem_Type,root,Resultfile2,str2):
    elements = root.findall(Elem_Type)
    parentList, childList, subChildList = list(),list(),list()
    parentSet, childSet, subChildSet = set(),set(),set()
    Resultfile = Resultfile2 + Elem_Type + "_Parent_Tag_Logger_" + str2 + "_.txt"
    Resultfile1 = Resultfile2 + Elem_Type + "_Child_Tag_Logger_" + str2 + "_.txt"
    Resultfile3 = Resultfile2 + Elem_Type + "_Sub_Child_Tag_Logger_" + str2 + "_.txt"
    for element in elements:
        adsID = element.get("adsUniqueID","None")
        if (len(adsID) <= 100):
            #Bug Fix NTI-8374
            #if (Elem_Type == 'TST'):
            #    paymentRest = element.get("paymentRestrictions","None")
                #if (len(paymentRest) > 76):
                #    element.set("paymentRestrictions",str(paymentRest)[:76])
                #    parentList.append(str(adsID) + " paymentRestrictions - trimmed to 76 chars")
            if (adsID != "None"):
                if adsID in parentSet:
                    parentList.append(adsID)
                    element.getparent().remove(element)
                else:
                    parentSet.add(adsID)
            childElements = element.getchildren()
            #Added as part of NTI-8085 - Start
            #Bug Fix NTI-8374
            #if Elem_Type == Element_Ticket:
                #nonRefundableIndicator = element.get('nonRefundableIndicator', 'NA')
                #Bug Fix NTI-8374
                #if len(nonRefundableIndicator) > 3:
                #    element.set("nonRefundableIndicator", str(nonRefundableIndicator)[:3])
                #    parentList.append(str(adsID) + " nonRefundableIndicator - trimmed to 3 chars")
                #originalIssueIndicator = element.get('originalIssueIndicator', "None")
                #Bug Fix NTI-8374
                #if len(originalIssueIndicator) > 70:
                #    element.set("originalIssueIndicator", str(originalIssueIndicator)[:70])
                #    parentList.append(str(adsID) + " originalIssueIndicator - trimmed to 70 chars")
                #Bug Fix NTI-8374
                #penaltyRestrictionIndicator = element.get('penaltyRestrictionIndicator', "NA")
                #if len(penaltyRestrictionIndicator) > 3:
                #    element.set("penaltyRestrictionIndicator", str(penaltyRestrictionIndicator)[:3])
                #    parentList.append(str(adsID) + " penaltyRestrictionIndicator - trimmed to 3 chars")
                #fareCalculation = element.get('fareCalculation', "None")
                #if len(fareCalculation) > 350:
                #    element.set("fareCalculation", str(fareCalculation)[:350])
                #    parentList.append(str(adsID) + " fareCalculation - trimmed to 350 chars")
                #Added as part of NTI-8085 - End


            if (Elem_Type == "Flight"):
                flightLegSet,subChildSet = set(),set()
            for childElement in childElements:
                tagName = childElement.tag
                childadsID = childElement.get("adsUniqueID","None")
                if (len(childadsID) <= 100):
                    if not (tagName == 'TicketingArrangement' or tagName =='AccountingDetails' or tagName == 'Passenger' or tagName == 'Remark'):
                        if (tagName == 'reference'):
                            referenceRloc = childElement.get("rloc")
                            if(len(referenceRloc) > 6):
                                childElement.getparent().remove(childElement)
                                childList.append(str(childadsID) + " reference entity has been removed due to rloc lenght exceeding 6 chars")
                        if (childadsID != "None"):
                            if childadsID in childSet:
                                childList.append(childadsID)
                                if (Elem_Type == 'TSM' and (tagName == 'MCO' or tagName == 'SVC')):
                                    childElement.getparent().getparent().remove(element)
                                    break
                                else:
                                    childElement.getparent().remove(childElement)
                            else:
                                childSet.add(childadsID)
                    subChildElements = childElement.getchildren()
                    for subChildElement in subChildElements:
                        subChildTagName = subChildElement.tag
                        subChildadsID = subChildElement.get("adsUniqueID","None")
                        #NTI - 7984 BoardPoint/Offpoint  trimed to 3 chars
                        if (Elem_Type == "Flight" and subChildTagName == "offPoint"):
                            airport_op = subChildElement.get("airport")
                            if (airport_op != None and len(airport_op) > 3):
                                subChildElement.set("airport","NIL")
                                subChildList.append(str(childadsID) + " Flight offpoint attrib airport is set to NIL")
                        if (Elem_Type == "Flight" and subChildTagName == "boardPoint"):
                            airport_bp = subChildElement.get("airport")
                            if (airport_bp != None and len(airport_bp) > 3):
                                subChildElement.set("airport","NIL")
                                subChildList.append(str(childadsID) + " Flight boardPoint attrib airport is set to NIL")
                        if (Elem_Type == "Flight" and subChildTagName == "Leg"):
                            LegoffPoint = subChildElement.find("offPoint").get("airport")
                            LegboardPoint = subChildElement.find("boardPoint").get("airport")
                            if (LegoffPoint != None and len(LegoffPoint) >3):
                                subChildElement.find("offPoint").set("airport","NIL")
                                subChildList.append(str(childadsID) + " Flight -> AirSegment -> Leg -> offpoint attrib airport is set to NIL")
                            if (LegboardPoint != None and len(LegboardPoint) >3):
                                subChildElement.find("boardPoint").set("airport","NIL")
                                subChildList.append(str(childadsID) + " Flight -> AirSegment -> Leg -> boardPoint attrib airport is set to NIL")
                        #NTI - 7984 BoardPoint/Offpoint  trimed to 3 chars
                        if (len(subChildadsID) <= 100):
                            if (subChildadsID != "None"):
                                if subChildadsID in subChildSet:
                                    if (Elem_Type == "Flight" and subChildTagName == "Leg"):
                                        offPoint = subChildElement.find("offPoint").get("airport")
                                        boardPoint = subChildElement.find("boardPoint").get("airport")
                                        fltSetID = subChildadsID + "-" + boardPoint + "-" + offPoint
                                        if fltSetID not in flightLegSet:
                                            subChildList.append(subChildadsID)
                                            parent = subChildElement.getparent().getparent().getparent()
                                            if (parent != None):
                                                parent.remove(element)
                                                break
                                        else:
                                            flightLegSet.add(fltSetID)
                                    else:
                                        subChildList.append(subChildadsID)
                                        subChildElement.getparent().remove(subChildElement)
                                else:
                                    subChildSet.add(subChildadsID)
                                    if (Elem_Type == "Flight" and subChildTagName == "Leg"):
                                        offPoint = subChildElement.find("offPoint").get("airport")
                                        boardPoint = subChildElement.find("boardPoint").get("airport")
                                        fltSetID = subChildadsID + "-" + boardPoint + "-" + offPoint
                                        flightLegSet.add(fltSetID)
                        else:
                            parent = subChildElement.getparent()
                            if (parent != None):
                                parent.remove(subChildElement)
                                subChildList.append(str(subChildadsID) + " Removed due to adsID exceeding 100 chars")
                else:
                    parent = childElement.getparent()
                    if (parent != None):
                        parent.remove(childElement)
                        childList.append(str(childadsID) + " Removed due to adsID exceeding 100 chars")
        else:
            if (element.getparent() != None):
                element.getparent().remove(element)
                parentList.append(str(adsID) + " Removed due to adsID exceeding 100 chars")


    if (len(parentList) > 0):
        writeToFile(Resultfile,parentList)
    if (len(childList) > 0):
        writeToFile(Resultfile1,childList)
    if (len(subChildList) > 0):
        writeToFile(Resultfile3,subChildList)

    if (len(parentList) > 0 or len(childList) > 0 or len(subChildList) > 0):
        return True
    else:
        return False


def writeToFile(fileName,dupDataList):
    dup = list(set(dupDataList))
    fs = open(fileName,"a+")
    for i in dup:
        fs.write(i)
        fs.write("\n")
    fs.close()


def xmlcompareBooking(Elem_Type,root,Resultfile2,str2):
    #print elem_Check
    elements = root.findall(Elem_Type)
    parentList, childList, subChildList = list(),list(),list()
    parentSet, childSet, subChildSet = set(),set(),set()
    Resultfile = Resultfile2 + Elem_Type + "_Parent_Tag_Logger_" + str2 + "_.txt"
    #print str2
    Resultfile1 = Resultfile2 + Elem_Type + "_Child_Tag_Logger_" + str2 + "_.txt"
    Resultfile3 = Resultfile2 + Elem_Type + "_Sub_Child_Tag_Logger_" + str2 + "_.txt"
    contactSet = set()
    fareElementSet = set()
    otherServiceSet = set()
    specialServiceSet = set()
    #passengerSet = set()
    #ticketingArrangementSet = set()
    #accountingDetailsSet = set()
    #remarkSet = set()
    frequentFlyerSet = set()
    mealSet = set()
    optionSet = set()
    seatSet = set()
    vipSet = set()
    pdiSet = set ()
    for element in elements:
        adsID = element.get("adsUniqueID","None")
        if (len(adsID) <= 100):
            if (adsID != "None"):
                if adsID in parentSet:
                    parentList.append(adsID)
                    element.getparent().remove(element)
                else:
                    parentSet.add(adsID)
            childElements = element.getchildren()
            for childElement in childElements:
                tagName = childElement.tag
                childadsID = childElement.get("adsUniqueID","None")
                if(len(childadsID) <= 100):
                    if not (tagName == ('TicketingArrangement' ) or tagName ==('AccountingDetails')or tagName == ('Passenger') or tagName == ('Remark')):
                        if (tagName == "Links"):
                            linkDict = childElement.attrib
                            for id,value in linkDict.iteritems():
                                if (len(value) > 100):
                                    linkDict.pop(id,None)
                                    childList.append(str(id) + " from Links tag has been removed due to length exceeding 100 chars")
                            if (linkDict.get("mktSegmentID") == None):
                                childList.append(str(adsID) + " complete booking has been removed since mktSegmentID is not present in links")
                                parent = childElement.getparent().getparent()
                                if (parent != None):
                                    parent.remove(element)
                                    break
                        #Added as part of NTI-7826 - Start
                        #Bug Fix NTI-8374
                        #if (tagName == "Contact"):
                            #notificationPhNo = childElement.get("notificationPhoneNumber","None")
                            #if (len(notificationPhNo) > 20):
                                #childElement.set("notificationPhoneNumber",str(notificationPhNo)[:20])
                                #childList.append(str(childadsID) + "Contact Attribute - notificationPhoneNumber is trimmed to 20 chars")
                        #Added as part of NTI-7826 - End

                        if (childadsID != "None"):
                            if childadsID in childSet:
                                if (tagName == "Contact" and childadsID in contactSet):
                                    childList.append(childadsID)
                                    childElement.getparent().remove(childElement)
                                elif (tagName == "FareElement" and childadsID in fareElementSet):
                                    childList.append(childadsID)
                                    childElement.getparent().remove(childElement)
                                elif (tagName == "OtherService" and childadsID in otherServiceSet):
                                    childList.append(childadsID)
                                    childElement.getparent().remove(childElement)
                                elif (tagName == "SpecialService" and childadsID in specialServiceSet):
                                    childList.append(childadsID)
                                    childElement.getparent().remove(childElement)
                                elif (tagName == "FrequentFlyer" and childadsID in frequentFlyerSet):
                                    childList.append(childadsID)
                                    childElement.getparent().remove(childElement)
                                elif (tagName == "Meal" and childadsID in mealSet):
                                    childList.append(childadsID)
                                    childElement.getparent().remove(childElement)
                                elif (tagName == "Seat" and childadsID in seatSet):
                                    childList.append(childadsID)
                                    childElement.getparent().remove(childElement)
                                elif (tagName == "Option" and childadsID in optionSet):
                                    childList.append(childadsID)
                                    childElement.getparent().remove(childElement)
                                elif (tagName == "VIP" and childadsID in vipSet):
                                    childList.append(childadsID)
                                    childElement.getparent().remove(childElement)
                                elif (tagName == "PDI" and childadsID in pdiSet):
                                    childList.append(childadsID)
                                    childElement.getparent().remove(childElement)
                                elif not (tagName == "Contact" or tagName == "FareElement" or tagName == "OtherService" or tagName == "SpecialService" or tagName == "FrequentFlyer" or tagName == "Meal" or tagName == "Seat" or tagName == "Option" or tagName == "VIP" or tagName == "PDI"):
                                    childList.append(childadsID)
                                    childElement.getparent().remove(childElement)

                            else:
                                childSet.add(childadsID)
                                if (tagName == "Contact"):
                                    contactSet.add(childadsID)
                                elif (tagName == "FareElement"):
                                    fareElementSet.add(childadsID)
                                elif (tagName == "OtherService"):
                                    otherServiceSet.add(childadsID)
                                elif (tagName == "SpecialService"):
                                    specialServiceSet.add(childadsID)
                                elif (tagName == "FrequentFlyer"):
                                    frequentFlyerSet.add(childadsID)
                                elif (tagName == "Meal"):
                                    mealSet.add(childadsID)
                                elif (tagName == "Seat"):
                                    seatSet.add(childadsID)
                                elif (tagName == "Option"):
                                    optionSet.add(childadsID)
                                elif (tagName == "VIP"):
                                    vipSet.add(childadsID)
                                elif (tagName == "PDI"):
                                    pdiSet.add(childadsID)

                    subChildElements = childElement.getchildren()
                    for subChildElement in subChildElements:
                        subChildadsID = subChildElement.get("adsUniqueID","None")

                        #Added as part of NTI-7809 & NTI-7823 - Start
                        subChildTagName = subChildElement.tag
                        # Bug fix NTI-8374
                        #if (subChildTagName == "DOCS"):
                        #    TDS = subChildElement.get("travelDocumentSurname","None")
                        #    if (len(TDS) > 30):
                        #        subChildElement.set("travelDocumentSurname",str(TDS)[:30])
                        #        subChildList.append(str(subChildadsID) + "DOCS attribute - travelDocumentSurname is trimmed to 30 chars")
                        #    TDN = subChildElement.get("travelDocumentNumber","None")
                        #    if (len(TDN) > 15):
                        #        subChildElement.set("travelDocumentNumber",str(TDN)[:15])
                        #        subChildList.append(str(subChildadsID) + "DOCS attribute - travelDocumentNumber is trimmed to 30 chars")
                            #Added as part of NTI-8085 - Start
                        #    TDF = subChildElement.get("travelDocumentFirstName", "None")
                        #    if (len(TDF) > 30):
                        #        subChildElement.set("travelDocumentFirstName", str(TDF)[:30])
                        #        subChildList.append(str(subChildadsID) + "DOCS attribute - travelDocumentFirstName is trimmed to 30 chars")
                        #Added as part of NTI-7809 & NTI-7823 & NTI-8085 - End

                        #Added as part of NTI-8140 - Start
                        if (subChildTagName == "DOCO"):
                            DT = subChildElement.get("documentType","N")
                            if (len(DT) > 1 and subChildElement.getparent() != None):
                                subChildElement.getparent().remove(subChildElement)
                                subChildList.append(str(subChildadsID) + "DOCO attribute - removed DOCO since documentType length is greater than 1")
                        #Added as part of NTI-8140 - End

                        if (len(subChildadsID) <= 100):
                            if (subChildadsID != "None"):
                                if subChildadsID in subChildSet:
                                    subChildList.append(subChildadsID)
                                    subChildElement.getparent().remove(subChildElement)
                                else:
                                    subChildSet.add(subChildadsID)
                        else:
                            parent = subChildElement.getparent()
                            if (parent != None):
                                parent.remove(subChildElement)
                                subChildList.append(str(subChildadsID) + " Removed due to adsID exceeding 100 chars")
                else:
                    parent = childElement.getparent()
                    if (parent != None):
                        parent.remove(childElement)
                        childList.append(str(childadsID) + " Removed due to adsID exceeding 100 chars")
        else:
            if (element.getparent() != None):
                element.getparent().remove(element)
                parentList.append(str(adsID) + " Removed due to adsID exceeding 100 chars")


    if (len(parentList) > 0):
        writeToFile(Resultfile,parentList)
    if (len(childList) > 0):
        writeToFile(Resultfile1,childList)
    if (len(subChildList) > 0):
        writeToFile(Resultfile3,subChildList)

    if (len(parentList) > 0 or len(childList) > 0 or len(subChildList) > 0):
        return True
    else:
        return False


def xmlcompareAuxSVC(Elem_Type,root,Resultfile2,str2):
    elements = root.findall(Elem_Type)
    parentList, childList, subChildList = list(),list(),list()
    parentSet, childSet, subChildSet = set(),set(),set()
    auxDict = {}
    Resultfile = Resultfile2 + Elem_Type + "_Parent_Tag_Logger_" + str2 + "_.txt"
    Resultfile1 = Resultfile2 + Elem_Type + "_Child_Tag_Logger_" + str2 + "_.txt"
    Resultfile3 = Resultfile2 + Elem_Type + "_Sub_Child_Tag_Logger_" + str2 + "_.txt"
    for element in elements:
        adsID = element.get("adsUniqueID")
        if(adsID != None):
            if adsID in parentSet:
                parentList.append(adsID)
                currLastUpdateTimeStmp = element.get("adsLastUpdateTimestamp")
                prevElement = auxDict.get(adsID)
                prevLastUpdateTimestmp = prevElement.get("adsLastUpdateTimestamp")
                if (currLastUpdateTimeStmp > prevLastUpdateTimestmp):
                    auxDict[adsID] = element
                    prevElement.getparent().remove(prevElement)
                else:
                    element.getparent().remove(element)
            else:
                parentSet.add(adsID)
                auxDict[adsID] = element

    if (len(parentList) > 0):
        writeToFile(Resultfile,parentList)
        return True
    else:
        return False

def validateXML(xml_doc, schema,Resultfile2):
    etree.clear_error_log()
    root_new = xml_doc.getroot()
    print "Parsing Done"
    if (schema.validate(xml_doc)):
        print "File is valid against the given Schema: "
    else:
        log = schema.error_log
        print file1 + " is not valid against Schema"
        #logpath = filepath.split(".")[0]+".log"
        logpath = Resultfile2+"XSDVALIDATION.log"
        fs = open(logpath,"a+")
        for error in iter(log):
            fs.write(error.message)
            fs.write("\n")
        fs.close()
    root_new.clear()

if __name__ == '__main__':
    if (len(sys.argv) >=3) :
        filename = sys.argv[1]
        Resultfile2 = str(sys.argv[2])+"//"
        xsdpath = str(sys.argv[3])
    else:
        filename = raw_input("Enter the NEXTI XML Path : (ex: D:\XML_Compare\TestData\NEXTI\) : ")
        Resultfile2 = raw_input("Enter the Logger Path : (ex: D:\XML_Compare\XML Compare\Results\) : ")
        #xsdpath = raw_input("Enter the XSD Schema Path: (ex: D:\path to xsd\datawarehouseFeed_2.1.xsd)")
        print "Source Directory for XML files : "+filename
        print "Target Directory for Output files : "+Resultfile2
    #schema = etree.XMLSchema(file = xsdpath)
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
        origFileName = file1
        if file1.endswith(".xml"):
            file1 = filename + "//" + file1
            print file1
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
            FLG1 = xmlcompareBooking(Element_Booking,root,Resultfile2,str2)
            FLG2 = xmlcompare(Element_PNR,root,Resultfile2,str2)
            FLG3 = xmlcompare(Element_Ticket,root,Resultfile2,str2)
            FLG4 = xmlcompare(Element_Flight,root,Resultfile2,str2)
            FLG5 = xmlcompare(Element_TST,root,Resultfile2,str2)
            FLG6 = xmlcompare(Element_Grouping,root,Resultfile2,str2)
            FLG7 = xmlcompare(Element_EMD,root,Resultfile2,str2)
            FLG8 = xmlcompareAuxSVC(Element_Aux_SVC,root,Resultfile2,str2)
            FLG9 = xmlcompare(Element_TSM,root,Resultfile2,str2)
            if (FLG1 or FLG2 or FLG3 or FLG4 or FLG5 or FLG6 or FLG7 or FLG8 or FLG9):
                tree.write(Resultfile2 + origFileName)
            #validateXML(tree,schema,Resultfile2)
            root.clear()
