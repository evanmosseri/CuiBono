import pandas as pd
import csv
from pprint import pprint
import sys
import numpy as np
import re
import glob
import concurrent.futures
import itertools
import multiprocessing
import linecache
import sys
def extract_filer_name(org_name):
    reversed = False
    if "Texans For" in org_name.title():
        org_name = org_name.replace("Texans for ","")
        org_name = org_name.replace("Texans for ".upper(),"")
        reversed = True
    if "Friends Of" in org_name.title():
        org_name = org_name.replace("Friends of ","")
        org_name = org_name.replace("Friends Of ","")
        org_name = org_name.replace("Friends Of ".upper(),"")
        reversed = True
    if "Political Action Committee" in org_name.title():
        org_name = org_name.replace("Political Action Committee","")
        reversed = True
    if "Committee To Elect" in org_name.title():
        org_name = org_name.replace("Committee to Elect ","")
    if "Committee" in org_name:
        org_name = org_name.replace(" Committee","")
        reversed = True
    if "The Coalition To Elect" in org_name.title():
        org_name = org_name.replace("The Coalition to Elect","")
    if "Coalition To Elect" in org_name.title():
        org_name = org_name.replace("Coalition to Elect","")
    if "For Texas Supreme Court" in org_name.title():
        org_name = org_name.replace(" For Texas Supreme Court","")
        org_name = org_name.replace("For Texas Supreme Court".upper(),"")
        reversed = True
    if "For Texas Supreme Court" in org_name.title():
        org_name = org_name.replace("for Texas Supreme Court","")
        reversed = True
    if "For Texas" in org_name.title():
        org_name = re.sub(r"(F|f)or.*","",org_name)
        org_name = org_name.replace("For Texas","")
        org_name = org_name.replace("for Texas","")
        reversed = True
    if "Justice" in org_name.title():
        org_name = org_name.replace("Justice","")
        reversed = True
    if "For Supreme Court" in org_name.title():
        org_name = org_name.replace("For Supreme Court","")
        org_name = org_name.replace("for Supreme Court","")
        reversed = True
    if "Campaign" in org_name.title():
        org_name = org_name.replace(" Campaign","")
        reversed = True
    if "Citizens For" in org_name.title():
        org_name = org_name.replace("Citizens for","")
        reversed = True
    org_name = org_name.replace(" SPAC ","")
    org_name = re.sub(r'\(.*\)',"",org_name) # replace anything inside parentheses
    org_name = org_name.replace(" Jr.","")
    org_name = org_name.replace("Jr.","")
    org_name = org_name.replace(" Sr.","")
    org_name = org_name.replace("Jr","")
    org_name = org_name.replace("PAC","")
    org_name = re.sub(r' [A-Za-z]{1,1}\.( |$)'," ",org_name) # replace single letters followed by periods
    org_name = re.sub(r"\'.*\'","",org_name) # replace anything inside parentheses
    # org_name = re.sub(r" I{2,3}","",org_name)
    org_name = re.sub(r' \b(?=[MDCLXVI]+\b)M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})\b',"",org_name) # replace roman numerals
    org_name = org_name.title()
    # org_name = org_name.replace("    "," ")
    # org_name = org_name.replace("  "," ")
    org_name = re.sub(r' {2,}'," ",org_name)
    org_name = org_name.strip()
    org_name = org_name.replace("\"","")
    if not(reversed) and len(org_name.split(",")) == 2:
        org_name = " ".join(org_name.split(",")[::-1])
    if re.match(".* [A-Za-z]{1} .*",org_name):
        temp = org_name.split(" ")
        org_name = " ".join([temp[0],temp[1]])
    return org_name
data_dir = "../../data/texas_ethics_commission"
def merge_data(columns=None,by=None,debug=False,filename="combined.csv",allowed_contributor_types=["ENTITY",""],allowed_form_types=["COH"]):
    files = glob.glob("{}/contrib*.csv".format(data_dir))
    files_data = []
    for file in files:
        dat = pd.read_csv(file,dtype=str)
        # dat = dat[dat["formTypeCd"] =="COH"].iloc[:500]
        # dat = dat[(dat["contributorPersentTypeCd"].isin(allowed_contributor_types)) & (dat["formTypeCd"].isin(allowed_form_types))]
        dat = dat[(dat["contributorPersentTypeCd"].isin(allowed_contributor_types))]
        dat.drop([
            "recordType",
            "schedFormTypeCd",
            "infoOnlyFlag",
            "contributorNameSuffixCd",
            "contributorNamePrefixCd",
            "contributorStreetCity",
            "contributorStreetStateCd",
            "contributorStreetRegion",
            "contributorOccupation",
            "contributorOosPacFlag",
            "contributorSpouseLawFirmName",
            "contributorParent1LawFirmName",
            "contributorParent2LawFirmName"],axis=1,inplace=True)
        files_data.append(dat)
        if debug: 
        	print(file)

    df = pd.concat(files_data,ignore_index=True)
    df.to_csv("../../data/{}".format(filename),index=False)
    df.iloc[0:200000].to_csv("../../data/{}_preview.csv".format(filename.replace(".csv","")),index=False)
    return df

def filer_id_lookup(filerinfo):
    dat = pd.read_csv("{}/filers.csv".format(data_dir))
    return dat[dat["filerIdent"].isin(filerinfo)][["filerIdent","filerName","filerTypeCd","filerPersentTypeCd"]].to_dict("records")
def concr(func,data,max_workers=50,thread=None):
	thread = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) if not(thread) else thread
	dat = list(thread.map(func,data))
	if len(dat) and (type(dat[0]) is dict):
		return dat
	else:
		try:
			if len(dat) and dat != None and not(all(map(lambda x: x == None, dat))):
				return list(itertools.chain(*dat))
			else:
				return dat
		except Exception as e:
			print(e)
			print(dat)


cpus = multiprocessing.cpu_count()-1
def multiprocess(func,data,cpu_count=cpus):
	pool = multiprocessing.Pool(cpu_count)
	dat = list(pool.map(func,data))
	if len(dat) and type(dat[0]) is dict:
		return dat
	else:
		try:
			if len(dat) and dat != None and not(all(map(lambda x: x == None, dat))):
				return list(itertools.chain(*dat))
			else:
				return dat
		except Exception as e:
			print(e)
			print(dat)
def PrintException():
	exc_type, exc_obj, tb = sys.exc_info()
	f = tb.tb_frame
	lineno = tb.tb_lineno
	filename = f.f_code.co_filename
	linecache.checkcache(filename)
	line = linecache.getline(filename, lineno, f.f_globals)
	print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))
