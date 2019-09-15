##############################################################
# Common functions for Data Migration Statistical Module     #
#                                                            #
#                                                            #
##############################################################

import os
import re
from datetime import datetime
from time import gmtime, strftime, mktime

from cassandra.cluster import ResultSet
from python.com.amadeus.datastaging.reconciliation.constants.Constants import *


## LOGGING CONFIGURATION ##
def initLogger(logging,outputDir,log_level):
    date_time = strftime("%Y_%m_%d_%H_%M_%S", gmtime())
    # logger
    logging.basicConfig(level=log_level)
    formatter = logging.Formatter('%(asctime)s, %(message)s')
    #formatter = logging.Formatter('%(message)s')
    # first file logger
    logFileName = outputDir + "/" + date_time + ".log"
    logger = logging.getLogger('data_migration')
    handler = logging.FileHandler(logFileName)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False
    return logger


##This function will dump the dataset (list,set) in a file
def write_to_file(fileName,dataSet):
    fs = open(fileName,"a+")
    for i in dataSet:
            fs.write(str(i))
            fs.write("\n")
    fs.close()


## This function will write the booking result set data into a file.
def write_booking_resultSet(fileName,result_set,logger):
    fs = open(fileName,"a+")
    if (type(result_set) is ResultSet):
        for sbr_data in result_set:
            try:
                pnr_rloc, pnr_creation_date,bkg_tattoo = sbr_data
                creation_date = datetime_to_milliseconds(datetime.strptime(str(pnr_creation_date), '%Y-%m-%d %H:%M:%S'))
                fs.write((pnr_rloc + "," + str(creation_date) + "," + bkg_tattoo))
                fs.write("\n")
            except:
                logger.info("Unable to Extract Booking Information: " + str(sbr_data))
    fs.close()

## This function will write ticket result set data into outfile.
def write_ticket_resultSet(fileName,result_set,logger):
    fs = open(fileName,"w")
    if (type(result_set) is ResultSet):
        for tkt_data in result_set:
            try:
                tkt_primary_number,tkt_date_of_issue,tkt_source = tkt_data
                if (tkt_source == 'TOF'):
                    creation_date = datetime_to_milliseconds(datetime.strptime(str(tkt_date_of_issue), '%Y-%m-%d %H:%M:%S'))
                    fs.write((tkt_primary_number + "," + str(creation_date)))
                    fs.write("\n")
            except:
                logger.info("Unable to Extract Ticket information" + str(tkt_data))
    fs.close()

## This function will write emd result set data into outfile.
def write_emd_resultSet(fileName,result_set,logger):
    fs = open(fileName,"w")
    if (type(result_set) is ResultSet):
        for emd_data in result_set:
            try:
                emd_primary_number,emd_date_of_issue = emd_data
                creation_date = datetime_to_milliseconds(datetime.strptime(str(emd_date_of_issue), '%Y-%m-%d %H:%M:%S'))
                fs.write((emd_primary_number + "," + str(creation_date)))
                fs.write("\n")
            except:
                logger.info("Unable to Extract Ticket information: " + str(emd_data))
    fs.close()


## This function will write flight result set data into outfile.
def write_flight_resultSet(fileName,result_set,logger):
    fs = open(fileName,"w")
    if (type(result_set) is ResultSet):
        for flight_data in result_set:
            try:
                mkt_flt_carrier_code, mkt_flt_number, mkt_flt_date, mkt_flt_alpha_suffix = flight_data
                flight_date = datetime_to_milliseconds(datetime.strptime(str(mkt_flt_date), '%Y-%m-%d %H:%M:%S'))
                fs.write((mkt_flt_carrier_code + "," + mkt_flt_number + "," + str(flight_date) + "," + mkt_flt_alpha_suffix))
                fs.write("\n")
            except:
                logger.info("Unable to Extract Flight information: " + str(flight_data))
    fs.close()

## This function will write feed_exception_table result set into outfile based on the status column.
def write_feed_exception_fld_resultSet(fileName,result_set,logger):
    fs = open(fileName+"_SUCCESS_FLD.csv","w")
    fso = open(fileName+"_OLD_FLD.csv","w")
    fse = open(fileName+"_ERROR_FLD.csv","w")
    fsf = open(fileName+"_INPROCESS_FLD.csv","w")
    if (type(result_set) is ResultSet):
        for feed_exception_data in result_set:
            try:
                flt_carrier_code, flt_number, flt_date, flt_alpha_suffix, status = feed_exception_data
                flight_date = datetime_to_milliseconds(datetime.strptime(str(flt_date), '%Y-%m-%d %H:%M:%S'))
                if status == "S":
                    fs.write((flt_carrier_code + "," + flt_number + "," + str(flight_date) + "," + flt_alpha_suffix))
                    fs.write("\n")
                elif status == "E":
                    fse.write((flt_carrier_code + "," + flt_number + "," + str(flight_date) + "," + flt_alpha_suffix))
                    fs.write("\n")
                elif status == "O":
                    fso.write((flt_carrier_code + "," + flt_number + "," + str(flight_date) + "," + flt_alpha_suffix))
                    fs.write("\n")
                elif status == "F":
                    fsf.write((flt_carrier_code + "," + flt_number + "," + str(flight_date) + "," + flt_alpha_suffix))
                    fs.write("\n")
            except:
                logger.info("Unable to extract details from Feed Exception Fld : " + str(feed_exception_data))
    fs.close()
    fse.close()
    fsf.close()
    fso.close()

## This function will write exceptions result set data into outfile.
def write_exception_resultSet(fileName, result_set,logger):
    fs = open(fileName,"w")
    if (type(result_set) is ResultSet):
        for exception_data in result_set:
            try:
                feed, data, partition_key = exception_data
                if (feed == MESSAGE_TYPE_SBR):
                    pnr_rloc = partition_key.split("-")[0]
                    pnr_creation_date = str(partition_key)[7:26]
                    creation_date = datetime_to_milliseconds(datetime.strptime(str(pnr_creation_date), '%Y-%m-%dT%H:%M:%S'))
                    fs.write((feed + "," + pnr_rloc + "," + str(creation_date)))
                    fs.write("\n")
                elif (feed == MESSAGE_TYPE_FLT):
                    #(mainFlight.aairlineCode + "-" + mainFlight.aflightNumber + "-" + mainFlight.adate)
                    air_line_code = partition_key.split("-")[0].strip()
                    flight_number = partition_key.split("-")[1].strip()
                    flight_date = partition_key.split(flight_number)[1]
                    fs.write((feed + "," + air_line_code + "," + flight_number + "," + flight_date))
                    fs.write("\n")
            except:
                logger.info("Unable to extract information from Exception table: " + str(exception_data))
    fs.close()

##Function to identify whether message is received/ignored/processed/failed based on the custom message
def identify_message_sbr(custom_message,logger):
    if "*SBR_PROCESSED*" in custom_message:
        return 'PROCESSED'
    elif "*SBR_RECEIVED*" in custom_message:
        return 'RECEIVED'
    elif "*SBR_IGNORED*" in custom_message:
        return 'IGNORED'
    elif "*SBR_IGNORED_IN_PARSING*" in custom_message:
        return 'FAILED'
    elif "*BATCH_FAILED*" in custom_message:
        return 'FAILED'


def identify_message_fld(custom_message,logger):
    if "*FLD_PROCESSED*" in custom_message:
        return 'PROCESSED'
    elif "*FLD_RLDMN_NEW_MKT_PROCESSED*" in custom_message:
        return 'PROCESSED'
    elif "*FLD_RLDMN_NEW_OPR_PROCESSED*"  in custom_message:
        return 'PROCESSED'
    elif "*FLD_RECEIVED*" in custom_message:
        return 'RECEIVED'
    elif "*FLD_RLDMN_FEED_EXC_ROWS_RECEIVED*" in custom_message:
        return 'RECEIVED'
    elif "*FLD_IGNORED*" in custom_message:
        return 'IGNORED'
    elif "*FLD_RLDMN_UPDATE_RECORDS_WITH_ERROR_CODE*" in custom_message:
        return 'IGNORED'
    elif "*FLD_RLDMN_UPDATE_INELIGIBLE_RECORDS*" in custom_message:
        return 'IGNORED'
    elif "*FLD_RLDMN_UPDATED_OLD_RECORDS*" in custom_message:
        return 'IGNORED'
    elif "*FLD_FAILED*" in custom_message:
        return 'FAILED'


def identify_message_tof(custom_message,logger):
    if "*TOF_PROCESSED*" in custom_message:
        return 'TICKET_PROCESSED'
    elif "*TOF_RECIEVED*" in custom_message:
        return 'TICKET_RECEIVED'
    elif "*TOF_IGNORED*" in custom_message:
        return 'TICKET_IGNORED'
    elif "*TOF_IGNORED_IN_PARSING*" in custom_message:
        return 'TICKET_FAILED'
    elif "*TOF_FAILED*" in custom_message:
        return 'TICKET_FAILED'
    elif "*TOF_REF_FAILED*" in custom_message:
        return 'TICKET_FAILED'
    elif "*EMD_PROCESSED*" in custom_message:
        return 'EMD_PROCESSED'
    elif "*EMD_RECIEVED*" in custom_message:
        return 'EMD_RECEIVED'
    elif "*EMD_IGNORED*" in custom_message:
        return 'EMD_IGNORED'
    elif "*EMD_IGNORED_IN_PARSING*" in custom_message:
        return 'EMD_FAILED'
    elif "*BATCH_FAILED*" in custom_message:
        return 'EMD_FAILED'


## Function to extract the business key from the custom message
def parse_business_key_sbr(business_key,logger):
    pnr_regex = '[^A-Za-z0-9:-]+'
    if "PNR" in business_key:
        pnr = re.sub(pnr_regex,'',business_key.split(",")[0].split("Some")[-1])
        try:
            creation_date = re.sub(pnr_regex,'',business_key.split(",")[1].split("Some")[-1].split(".")[0])
            dateTimestamp = datetime_to_milliseconds(datetime.strptime(creation_date, '%Y-%m-%dT%H:%M:%S'))
        except Exception as errorTrace:
            logger.error("Exception in parsing Date column for business Key :+" + str(business_key) + "Error Trace :%s" ,errorTrace)
            dateTimestamp = "Unable to Parse Date"
        return pnr + "," + str(dateTimestamp)
    else:
        return None

def parse_business_key_tof(business_key,logger):
    tkt_regex = '[^0-9]'
    if "PRIMARY_NUMBER" in business_key.upper():
        tkt_primary_no = re.sub(tkt_regex,'',business_key.split(":")[1])
        try:
            tkt_date_of_issue = re.sub(tkt_regex,'',business_key.split(":")[2])
            if (len(tkt_date_of_issue) > 6):
                dateTimestamp = datetime_to_milliseconds(datetime.strptime(tkt_date_of_issue[:8],'%Y%m%d'))
            else:
                dateTimestamp = datetime_to_milliseconds(datetime.strptime(tkt_date_of_issue,'%d%m%y'))

        except Exception as errorTrace:
            logger.error("Exception in parsing Date column for business Key :" + str(business_key) + "Error Trace :%s", errorTrace)
            dateTimestamp = "31/12/9999"
        return tkt_primary_no + "," + str(dateTimestamp)
    else:
        return ""

def create_folder(output_dir,message_type,logger):
    datetime_now = datetime.now().strftime("%Y-%m-%d")
    directory_path = output_dir+DIRECTORY_DELIMETER+message_type+"-"+datetime_now
    logger.info("Output Directory for the Business Key: " + str(directory_path))
    if (os.path.exists(directory_path)):
        os.remove(directory_path)
    os.makedirs(directory_path,775)
    return directory_path


def parse_business_key_fld(business_key,logger):
    fld_regex = '[^0-9]'
    ##WIP

def fetch_data_from_cassandra(session,query_string):
    data = session.execute(query_string)
    return data

def datetime_to_milliseconds(datetime):
    try:
        time_in_millisec = mktime(datetime.timetuple())*1000
        return int(time_in_millisec)
    except Exception as errorTrace:
        print errorTrace
        return 0