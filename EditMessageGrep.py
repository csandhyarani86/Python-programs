import os
import sys
import logging
import re
from datetime import datetime


##################################################################################
# Home Directory path for all the python scripts Mandatory for import statements #
##################################################################################
if (len(sys.argv) > 1):
    sys.path.append(sys.argv[1])

from python.com.amadeus.datastaging.reconciliation.constants.Constants import *
from python.com.amadeus.datastaging.reconciliation.utils.CommonFunctions import initLogger,create_folder,datetime_to_milliseconds,write_to_file

def extract_business_key_sbr(file_name, output_dir, logger):
    with open(file_name,"r") as sbr_file:
        business_key_list_success, business_key_list_failure = list(),list()
        pnr_rloc_regex = 'RCI\x1d1A\x1f\w\w\w\w\w\w'
        date_time_regex = '(?<=\x1c)RSI\x1dRP(.*?)(?=\x1c)'
        for line in sbr_file:
            pnr_rloc_regex_list = re.findall(pnr_rloc_regex,line)
            date_time_regex_list = re.findall(date_time_regex,line)
            if len(pnr_rloc_regex_list) >= 1 and len(date_time_regex_list) >= 1 :
                pnr_rloc = pnr_rloc_regex_list[0].split("\x1f")[1]
                time = date_time_regex_list[0].split("\x1f")[-1]
                date = date_time_regex_list[0].split("\x1f")[-3]
                #print "PNR: "+ pnr_rloc + " DATE : " + date + " TIME: " + time
                try:
                    pnr_creation_date_millisec = datetime_to_milliseconds(datetime.strptime(date+time,"%d%m%y%H%M"))
                    business_key_list_success.append(pnr_rloc+","+str(pnr_creation_date_millisec))
                except Exception as errorTrace:
                    logger.error("Exception in parsing Date column for business Key : Error Trace :%s", errorTrace)
                    business_key_list_failure.append(pnr_rloc+","+line)
            else:
                business_key_list_failure.append(line)

    write_to_file(output_dir+DIRECTORY_DELIMETER+message_type+"_BUSINESS_KEY_SUCCESS.csv",business_key_list_success)
    write_to_file(output_dir+DIRECTORY_DELIMETER+message_type+"_BUSINESS_KEY_FAILURE.csv",business_key_list_failure)

def extract_business_key_tof(file_name, output_dir, logger):
    with open(file_name,"r") as tof_file:
        logger.info("Processing file name :" + str(file_name))
        business_key_tof_list_success, business_key_tof_list_failure = list(),list()
        business_key_emd_list_success, business_key_emd_list_failure = list(),list()
        tkt_grep_reg = 'TCN.TKTT'
        emd_grep_reg = 'TCN.EMD'
        tkt_id_regex = 'TKT\x1d\d\d\d\d\d\d\d\d\d\d\d\d\d(?=.T)'
        emd_id_regex = 'TKT\x1d\d\d\d\d\d\d\d\d\d\d\d\d\d(?=.Y|.J)'
        #tkt_dt_regex = 'IGD\x1f\d\d\d\d\d\d'
        tkt_dt_regex = 'PTK\x1d.*?\x1d\d\d\d\d\d\d(?=\x1c)'
        #(\d|\d{2}|\d{3}|\d{4}|\d{5})?\D

        for line in tof_file:
            tkt_id_list = re.findall(tkt_id_regex,line)
            tkt_emd_dt_list = re.findall(tkt_dt_regex,line)
            emd_id_list = re.findall(emd_id_regex,line)
            message_tkt = re.findall(tkt_grep_reg,line)
            message_emd = re.findall(emd_grep_reg,line)
            message_type_tkt,message_type_emd = False,False
            #print tkt_emd_dt_list
            if (len(message_tkt) > 0 and message_tkt[0].endswith("TKTT")):
                message_type_tkt = True
            elif (len(message_emd) > 0 and message_emd[0].endswith("EMD")):
                message_type_emd = True

            if (message_type_tkt and len(tkt_id_list) >= 1 and len(tkt_emd_dt_list) >= 1):
                tkt_id = tkt_id_list[0].split("\x1d")[1]
                #tkt_dt = tkt_emd_dt_list[0].split("\x1f")[1]
                tkt_dt = tkt_emd_dt_list[0].split("\x1d")[-1]
                try:
                    tkt_creation_date_millisec = datetime_to_milliseconds(datetime.strptime(tkt_dt,"%d%m%y"))
                    business_key_tof_list_success.append(tkt_id+","+str(tkt_creation_date_millisec))
                except Exception as errorTrace:
                    logger.error("Exception in parsing Date column for business Key :" + "Error Trace :%s", errorTrace)
                    business_key_tof_list_failure.append(tkt_id+","+str(line))
            elif (message_type_emd and len(emd_id_list) >= 1 and len(tkt_emd_dt_list) >= 1):
                emd_id = emd_id_list[0].split("\x1d")[1]
                #emd_dt = tkt_emd_dt_list[0].split("\x1f")[1]
                emd_dt = tkt_emd_dt_list[0].split("\x1d")[-1]
                try:
                    emd_creation_date_millisec = datetime_to_milliseconds(datetime.strptime(emd_dt,"%d%m%y"))
                    business_key_emd_list_success.append(emd_id+","+str(emd_creation_date_millisec))
                except Exception as errorTrace:
                    logger.error("Exception in parsing Date column for business Key :" + "Error Trace :%s", errorTrace)
                    business_key_emd_list_failure.append(emd_id+","+str(line))
            else:
                business_key_tof_list_failure.append(line)

    write_to_file(output_dir+DIRECTORY_DELIMETER+message_type+"_BUSINESS_KEY_SUCCESS.csv",business_key_tof_list_success)
    write_to_file(output_dir+DIRECTORY_DELIMETER+message_type+"_BUSINESS_KEY_FAILURE.csv",business_key_tof_list_failure)
    write_to_file(output_dir+DIRECTORY_DELIMETER+"EMD_BUSINESS_KEY_SUCCESS.csv",business_key_emd_list_success)
    write_to_file(output_dir+DIRECTORY_DELIMETER+"EMD_BUSINESS_KEY_FAILURE.csv",business_key_emd_list_failure)

def extract_business_key_fld(file_name, output_dir, logger):
    with open(file_name,"r") as fld_file:
        business_key_fld_list_success, business_key_fld_list_failure = list(),list()
        for line in fld_file:
            data = line.split(",")
            flight_code = data[0].strip()
            flight_number = data[1].strip()
            flight_date = data[2].strip()
            if data[3].strip() == "_":
                flight_alpha_suffix = "NULL"
            else:
                flight_alpha_suffix = data[3].strip()
            try:
                fld_date_millisec = datetime_to_milliseconds(datetime.strptime(flight_date,"%d-%b-%y"))
                business_key_fld_list_success.append(flight_code+","+flight_number+","+str(fld_date_millisec)+","+flight_alpha_suffix)
            except Exception as errorTrace:
                logger.error("Exception in parsing Date column for business Key :" + str(line) + "Error Trace :%s", errorTrace)
                business_key_fld_list_failure.append(line)


    write_to_file(output_dir+DIRECTORY_DELIMETER+message_type+"_BUSINESS_KEY_SUCCESS.csv",business_key_fld_list_success)
    write_to_file(output_dir+DIRECTORY_DELIMETER+message_type+"_BUSINESS_KEY_FAILURE.csv",business_key_fld_list_failure)


if __name__ == '__main__':
    #Code base Home Directory : Directory path for Python code base
    #Input Directory : Directory path for all the stats log.
    #Output Directory : Directory path for the business key dumps.
    #Flag : Additional parameter as a placeholder

    if (len(sys.argv) >= 4):
        inputDir = sys.argv[2]
        outputDir = sys.argv[3]
        message_type = str(sys.argv[4]).upper()
        logger = initLogger(logging,outputDir,LOG_LEVEL_INFO)
        #output_dir = create_folder(outputDir,message_type,logger)
        output_dir = outputDir
        for file in os.listdir(inputDir):
            file_name = inputDir + DIRECTORY_DELIMETER + file
            if not os.path.isdir(file_name):
                if (message_type == MESSAGE_TYPE_SBR):
                    logger.info("Processing Booking business key extract")
                    extract_business_key_sbr(file_name,output_dir,logger)
                elif (message_type == MESSAGE_TYPE_TKT):
                    logger.info("Processing Ticket business key extract")
                    extract_business_key_tof(file_name,output_dir,logger)
                elif (message_type == MESSAGE_TYPE_FLT):
                   logger.info("Processing Flight business key extract")
                   extract_business_key_fld(file_name,output_dir,logger)

    else:
        print "Please provide the arguments in following order: "
        print "1. Home directory path for Python code : "
        print "2. Input Directory path for stats log : "
        print "3. Output Directory path for Outfile : "
        print "4. Message Type (SBR/FLD/TOF): "