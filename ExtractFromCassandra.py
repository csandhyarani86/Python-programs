import logging
import sys

from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster
from cassandra.policies import DCAwareRoundRobinPolicy

##################################################################################
# Home Directory path for all the python scripts Mandatory for import statements #
##################################################################################
if (len(sys.argv) > 1):
    sys.path.append(sys.argv[1])

from python.com.amadeus.datastaging.reconciliation.constants.Constants import *
from python.com.amadeus.datastaging.reconciliation.utils.CommonFunctions import *

def getCassandraSession(CA_HOST,CA_SCHEMA):
    auth_provider = PlainTextAuthProvider(username=CASSANDRA_USER,password=CASSANDRA_PASSWORD)
    cluster = Cluster(CA_HOST,load_balancing_policy=DCAwareRoundRobinPolicy(local_dc='Cassandra',used_hosts_per_remote_dc=0),auth_provider=auth_provider)
    session = cluster.connect(CA_SCHEMA)
    return session

def extract_booking_from_db(output_dir,logger):
    logger.info("Extracting Business key from Booking Table")
    booking_query = SELECT_STMT + BOOKING_BUSINESS_KEY + FROM_STMT + BOOKING_TABLE_NAME
    booking_row = fetch_data_from_cassandra(session,booking_query)
    write_booking_resultSet(output_dir + DIRECTORY_DELIMETER + MESSAGE_TYPE_SBR + "_DB_EXTRACT.csv", booking_row,logger)

def extract_ticket_from_db(output_dir, logger):
    logger.info("Extracting Business key from TICKET Table")
    ticket_query = SELECT_STMT + TICKET_BUSINESS_KEY + FROM_STMT + TICKET_TABLE_NAME
    ticket_row = fetch_data_from_cassandra(session,ticket_query)
    write_ticket_resultSet(output_dir + DIRECTORY_DELIMETER + MESSAGE_TYPE_TKT + "_DB_EXTRACT.csv" , ticket_row,logger)
    logger.info("Extracting Business key from EMD_COUPON Table")
    emd_query = SELECT_STMT + EMD_BUSINESS_KEY + FROM_STMT + EMD_TABLE_NAME
    emd_row = fetch_data_from_cassandra(session,emd_query)
    write_emd_resultSet(output_dir + DIRECTORY_DELIMETER + EMD_TABLE_NAME + "_DB_EXTRACT.csv" , emd_row,logger)

def extract_exception_from_db(output_dir,logger):
    logger.info("Extracting Business key from EXCEPTIONS Table")
    exception_query = SELECT_STMT + EXCEPTIONS_BUSINESS_KEY + FROM_STMT + EXCEPTIONS_TABLE_NAME
    exception_row = fetch_data_from_cassandra(session,exception_query)
    write_exception_resultSet(output_dir + DIRECTORY_DELIMETER + EXCEPTIONS_TABLE_NAME + "_DB_EXTRACT.csv", exception_row,logger)

def extract_flight_from_db (output_dir, logger):
    logger.info("Extracting business key from Flight Table")
    flight_query = SELECT_STMT + FLIGHT_BUSINESS_KEY + FROM_STMT + FLIGHT_TABLE_NAME
    flight_row = fetch_data_from_cassandra(session,flight_query)
    write_flight_resultSet(output_dir + DIRECTORY_DELIMETER + MESSAGE_TYPE_FLT + "_DB_EXTRACT.csv",flight_row,logger)

def extract_feed_exception_fld_from_db(output_dir,logger):
    logger.info("Extracting Feed Exception FLD business key from Flight Table")
    feed_exception_fld_query = SELECT_STMT + FEED_EXCEPTION_BUSINESS_KEY + FROM_STMT + FEED_EXCEPTION_TABLE_NAME
    flight_row = fetch_data_from_cassandra(session,feed_exception_fld_query)
    write_feed_exception_fld_resultSet(output_dir + DIRECTORY_DELIMETER + FEED_EXCEPTION_TABLE_NAME,flight_row,logger)

if __name__ == '__main__':
    #Extract business key from Cassandra table
    if (len(sys.argv) >= 3):
        outputDir = sys.argv[2]
        entity_name = str(sys.argv[3]).upper()
        logger = initLogger(logging,outputDir,LOG_LEVEL_INFO)
        #output_dir = create_folder(outputDir,entity_name,logger)
        if (len(sys.argv) >= 5):
            CA_HOST=str(sys.argv[4]).split(",")
            CA_SCHEMA=str(sys.argv[5])
        else:
            CA_HOST=str(CASSANDRA_HOST).split(",")
            CA_SCHEMA=CASSANDRA_SCHEMA
        print str(CA_HOST) +"  " + CA_SCHEMA
        session = getCassandraSession(CA_HOST,CA_SCHEMA)
        output_dir = outputDir
        if (entity_name == MESSAGE_TYPE_SBR):
            logger.info("Processing Booking table extract")
            extract_booking_from_db(output_dir,logger)
        elif (entity_name == MESSAGE_TYPE_TKT):
            logger.info("Processing Ticket and EMD table extract")
            extract_ticket_from_db(output_dir,logger)
        elif (entity_name == MESSAGE_TYPE_FLT):
            logger.info("Processing Flight table extract")
            extract_flight_from_db(output_dir,logger)
            extract_feed_exception_fld_from_db(output_dir,logger)
        elif (entity_name == EXCEPTIONS_TABLE_NAME):
            logger.info("Processing Exception table extract")
            extract_exception_from_db(output_dir,logger)
        session.shutdown()

    else:
        print "Please provide the arguments in following order: "
        print "1. Home directory path for Python code : "
        print "2. Output Directory path for Outfile : "
        print "3. Entity Name (SBR/TOF/FLD/EXCEPTIONS): "
