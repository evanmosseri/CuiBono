import pandas as pd
import csv
from pprint import pprint
from scripts.utils import *
import sys
import numpy as np
import re
import glob
# data_file = csv.DictReader(open("../../data/cont_ss.csv"))
data_dir = "../../data/texas_ethics_commision"
dat_file = pd.read_csv("{}/cont_ss.csv".format(data_dir),low_memory=False)

# org_names =dat_file["filerName"].tolist()

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

def merge_data():
    files = glob.glob("{}/contrib*.csv".format(data_dir))
    df = pd.concat((pd.read_csv(x,dtype=str) for x in files),ignore_index=True)
    df.to_csv("../../data/combined.csv")
    print(files)

if __name__ == "__main__":
#     print(dat_file)
    merge_data()

