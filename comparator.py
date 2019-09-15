##############################################################
# Comparator for  Migration Statistical Module across Entity #
#                                                            #
#                                                            #
##############################################################
import logging
import os
import sys

##################################################################################
# Home Directory path for all the python scripts Mandatory for import statements #
##################################################################################
if (len(sys.argv) > 1):
    sys.path.append(sys.argv[1])
from python.com.amadeus.datastaging.reconciliation.constants.Constants import *
from python.com.amadeus.datastaging.reconciliation.utils.CommonFunctions import initLogger,write_to_file

sbr_bk_set_a,fld_bk_set_a,tof_bk_set_a,emd_bk_set_a = set(),set(),set(),set()
sbr_bk_set_b,fld_bk_set_b,tof_bk_set_b,emd_bk_set_b = set(),set(),set(),set()


def compare_sbr_businesskey(input_dir_ckpt_a,input_dir_ckpt_b,output_dir,logger):
    print "Comparing business key for SBR module"
    for file in os.listdir(input_dir_ckpt_a):
        if 'SBR' in file.upper():
            with open(input_dir_ckpt_a + "//" + file) as lines:
                for line in lines:
                    sbr_bk_set_a.add(line.split(",")[0])

    for file in os.listdir(input_dir_ckpt_b):
        if 'SBR' in file.upper():
            with open(input_dir_ckpt_b + "//" + file) as lines:
                for line in lines:
                    sbr_bk_set_b.add(line.split(",")[0])

    data_not_in_b = sbr_bk_set_a - sbr_bk_set_b
    data_not_in_a = sbr_bk_set_b - sbr_bk_set_a
    write_to_file(output_dir+DIRECTORY_DELIMETER+MESSAGE_TYPE_SBR+"_DataNotPresentInB.csv",data_not_in_b)
    write_to_file(output_dir+DIRECTORY_DELIMETER+MESSAGE_TYPE_SBR+"_DataNotPresentInA.csv",data_not_in_a)

def compare_tkt_businesskey(input_dir_ckpt_a,input_dir_ckpt_b,output_dir,logger):
    print "Comparing business key for Ticket module"
    for file in os.listdir(input_dir_ckpt_a):
        if 'TOF' in file.upper():
            with open(input_dir_ckpt_a + "//" + file) as lines:
                for line in lines:
                    tof_bk_set_a.add(line.split(",")[0])
        if 'EMD' in file.upper():
            with open(input_dir_ckpt_a + "//" + file) as lines:
                for line in lines:
                    emd_bk_set_a.add(line.split(",")[0])

    for file in os.listdir(input_dir_ckpt_b):
        if 'TOF' in file.upper():
            with open(input_dir_ckpt_b + "//" + file) as lines:
                for line in lines:
                    tof_bk_set_b.add(line.split(",")[0])
        if 'EMD' in file.upper():
            with open(input_dir_ckpt_b + "//" + file) as lines:
                for line in lines:
                    emd_bk_set_b.add(line.split(",")[0])

    data_not_in_b = tof_bk_set_a - tof_bk_set_b
    data_not_in_a = tof_bk_set_b - tof_bk_set_a
    emd_data_not_in_b = emd_bk_set_a - emd_bk_set_b
    emd_data_not_in_a = emd_bk_set_b - emd_bk_set_a

    write_to_file(output_dir+DIRECTORY_DELIMETER+MESSAGE_TYPE_TKT+"_DataNotPresentInB.csv",data_not_in_b)
    write_to_file(output_dir+DIRECTORY_DELIMETER+MESSAGE_TYPE_TKT+"_DataNotPresentInA.csv",data_not_in_a)
    write_to_file(output_dir+DIRECTORY_DELIMETER+MESSAGE_TYPE_TKT+"_EMDDataNotPresentInB.csv",emd_data_not_in_b)
    write_to_file(output_dir+DIRECTORY_DELIMETER+MESSAGE_TYPE_TKT+"_EMDDataNotPresentInA.csv",emd_data_not_in_a)


def compare_fld_businesskey(input_dir_ckpt_a,input_dir_ckpt_b,output_dir,logger):
    print "Comparing business key for Flight module"
    for file in os.listdir(input_dir_ckpt_a):
        if 'FLD' in file.upper():
            with open(input_dir_ckpt_a + "//" + file,"r") as lines:
                for line in lines:
                    fld_bk_set_a.add(line.replace("\n",""))
    for file in os.listdir(input_dir_ckpt_b):
        if 'FLD' in file.upper():
            with open(input_dir_ckpt_b + "//" + file,"r") as lines:
                for line in lines:
                    fld_bk_set_b.add(line.replace("\n",""))

    data_not_in_b = fld_bk_set_a - fld_bk_set_b
    data_not_in_a = fld_bk_set_b - fld_bk_set_a
    write_to_file(output_dir+DIRECTORY_DELIMETER+MESSAGE_TYPE_FLT+"_DataNotPresentInB.csv",data_not_in_b)
    write_to_file(output_dir+DIRECTORY_DELIMETER+MESSAGE_TYPE_FLT+"_DataNotPresentInA.csv",data_not_in_a)



if __name__ == '__main__':
    #Extract business key from Cassandra table
    if (len(sys.argv) >= 5):
        input_dir_ckpt_a = sys.argv[2]
        input_dir_ckpt_b = sys.argv[3]
        output_dir = sys.argv[4]
        entity_name = str(sys.argv[5]).upper()
        logger = initLogger(logging,output_dir,LOG_LEVEL_INFO)
        if (entity_name == MESSAGE_TYPE_SBR):
            logger.info("Comparing SBR businesskey across checkpoint ")
            compare_sbr_businesskey(input_dir_ckpt_a,input_dir_ckpt_b,output_dir,logger)
        elif (entity_name == MESSAGE_TYPE_TKT):
            logger.info("Comparing Ticket and EMD Business Key across checkpoint")
            compare_tkt_businesskey(input_dir_ckpt_a,input_dir_ckpt_b,output_dir,logger)
        elif (entity_name == MESSAGE_TYPE_FLT):
            logger.info("Comparing Flight business key across checkpoint")
            compare_fld_businesskey(input_dir_ckpt_a,input_dir_ckpt_b,output_dir,logger)
        elif (entity_name == 'ALL'):
            logger.info("Comparing SBR businesskey across checkpoint ")
            compare_sbr_businesskey(input_dir_ckpt_a,input_dir_ckpt_b,output_dir,logger)
            logger.info("Comparing Ticket and EMD Business Key across checkpoint")
            compare_tkt_businesskey(input_dir_ckpt_a,input_dir_ckpt_b,output_dir,logger)
            logger.info("Comparing Flight business key across checkpoint")
            compare_fld_businesskey(input_dir_ckpt_a,input_dir_ckpt_b,output_dir,logger)

    else:
        print "Please provide the arguments in following order: "
        print "1. Home directory path for Python code : "
        print "2. Input Directory path for checkpoint A: "
        print "3. Input Directory path for checkpoint B: "
        print "4. Output Directory path for Final result files : "
        print "5. Entity Name (SBR/TOF/FLD/ALL): "