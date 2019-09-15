'''
***Function    : Sort
***Description : To sort list of Dictionary pair.
***Author      : Bharathkumar C
***Created On  : 12-09-16
***Project     : NEXTI
***Modified By : None.
'''
import collections
from collections import Counter
import os
import sys
import operator
import re
#import sort_new1
check = "[ svc_pd_currency_code: GBP,  svc_pd_currency_code: GBP,  svc_pd_currency_code: GBP,  svc_pd_fare_type: B,  svc_pd_fare_type: NEV,  svc_pd_fare_type: T,  svc_pd_fareortaxamount: 18.4,  svc_pd_fareortaxamount: 18.40,  svc_pd_fareortaxamount: 18.40, ' svc_pd_history_id: null', ' svc_pd_history_id: null', ' svc_pd_history_id: null\\\}\\\}\\\}\\\}',  svc_pd_is_deleted: N,  svc_pd_is_deleted: N,  svc_pd_is_deleted: N,  svc_pd_row_creation_date: 2016-11-21 08:43:32+0000,  svc_pd_row_creation_date: 2016-11-21 08:43:32+0000,  svc_pd_row_creation_date: 2016-11-21 08:43:32+0000, ' svc_pd_row_purge_date: null', ' svc_pd_row_purge_date: null', ' svc_pd_row_purge_date: null',  svc_pd_row_timestamp: 2016-11-21 08:43:32+0000,  svc_pd_row_timestamp: 2016-11-21 08:43:32+0000,  svc_pd_row_timestamp: 2016-11-21 08:43:32+0000, ' svc_pd_tax_category: null', ' svc_pd_tax_category: null', ' svc_pd_tax_category: null', ' svc_pd_tax_iso_code: null', ' svc_pd_tax_iso_code: null', ' svc_pd_tax_iso_code: null', ' svc_pd_tax_nature_code: null', ' svc_pd_tax_nature_code: null', ' svc_pd_tax_nature_code: null', ' svc_pd_tsm_svc_id: 9596c41a-afc6-11e6-8715-4d3c2318549f', ' svc_pd_tsm_svc_id: 9596c41a-afc6-11e6-8715-4d3c2318549f', ' svc_pd_tsm_svc_id: 9596c41a-afc6-11e6-8715-4d3c2318549f',  tsm_svc_accounting_data: **-1221-601118*COURIER FEE, ' tsm_svc_banker_rate_nb: null', ' tsm_svc_commission: null', ' tsm_svc_doc_tsm_number: 1',  tsm_svc_doc_type: S,  tsm_svc_fare_issue_ind: F, ' tsm_svc_form_of_payment: null', ' tsm_svc_history_id: null', ' tsm_svc_id: 9596c41a-afc6-11e6-8715-4d3c2318549f', ' tsm_svc_id_currency: null', ' tsm_svc_id_issu_date: null', ' tsm_svc_id_issu_off_iata_code: null', ' tsm_svc_id_issu_off_id: null',  tsm_svc_id_ref_number_fa: , ' tsm_svc_id_ref_number_fb: null', ' tsm_svc_id_total_amount: null',  tsm_svc_int_ind: D,  tsm_svc_is_deleted: N,  tsm_svc_is_link_to_pax: Y, ' tsm_svc_issued_in_con_with: null',  tsm_svc_link_tattoo: PT1, ' tsm_svc_org_issue_in_ex: null', ' tsm_svc_pax_id: 95969d02-afc6-11e6-8715-4d3c2318549f', ' tsm_svc_pnr_id: 95969d00-afc6-11e6-8715-4d3c2318549f',  tsm_svc_present_at: HEL,  tsm_svc_present_to: AY,  tsm_svc_presentation_date: 2017-04-09 00:00:00+0000, ' tsm_svc_price_details: svc_pd_id: 9596eb20-afc6-11e6-8715-4d3c2318549f', ' tsm_svc_reason_for_waiving: null', ' tsm_svc_remarks: null', ' tsm_svc_rfic: null', ' tsm_svc_rfic_desc: null',  tsm_svc_row_creation_date: 2016-11-21 08:43:32+0000, ' tsm_svc_row_purge_date: null',  tsm_svc_row_timestamp: 2016-11-21 08:43:32+0000,  tsm_svc_tattoo_id: T24,  tsm_svc_validating_carrier: AY, ' tsm_svc_vat_country: null', 'svc_pd_id: 9596eb21-afc6-11e6-8715-4d3c2318549f', 'svc_pd_id: 9596eb22-afc6-11e6-8715-4d3c2318549f']&"
l = []
def sort1(sortcheck):
 l = []
 sortcheck = str(sortcheck).replace(' ','')
 sortcheck1 = str(sortcheck).replace('&','')
 #sortcheck1 = sortcheck1.replace('\}','')
 sortcheck3 = sortcheck1.replace("\{","")
 sortcheck4 = sortcheck3.split('\},')
 sortcheck5 = sorted(sortcheck4)
 sortlen = len(sortcheck5)
 print sortlen
 for i in range(0,sortlen):
     sortcheck2i = sortcheck5[i].split(',')    
     sortedchecki = sorted(sortcheck2i)
     l.append(sortedchecki)
 return l


sortcheck = str(check).replace(' ','')
sortcheck1 = str(sortcheck).replace('&','')
sortcheck2 = str(sortcheck).replace('[','')
sortcheck3 = str(sortcheck).replace(']','')
test = sortcheck3.split(',',3)
len1 = len(test)
#print test[3]

print 

