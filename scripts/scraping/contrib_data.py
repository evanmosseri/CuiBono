import pandas as pd
import csv
from pprint import pprint
from scripts.utils import *
import sys
import numpy as np
import re

# data_file = csv.DictReader(open("../../data/cont_ss.csv"))
dat_file = pd.read_csv("../../data/cont_ss.csv",low_memory=False)

org_names =dat_file["filerName"].tolist()

def replace_func(org_name):
    reversed = False
    if "Texans for" in org_name:
        org_name = org_name.replace("Texans for ","")
        reversed = True
    if "Friends Of" in org_name.title():
        org_name = org_name.replace("Friends of ","")
        org_name = org_name.replace("Friends Of ","")
        reversed = True
    if "Political Action Committee" in org_name.title():
        org_name = org_name.replace("Political Action Committee","")
        reversed = True
    if "Committee to Elect" in org_name.title():
        org_name = org_name.replace("Committee to Elect ","")
    if "Committee" in org_name:
        org_name = org_name.replace(" Committee","")
        reversed = True
    if "For Texas" in org_name.title():
        org_name = org_name.replace("For Texas","")
        org_name = org_name.replace("for Texas","")
        reversed = True
    if "For Supreme Court" in org_name.title():
        org_name = org_name.replace("For Supreme Court","")
        org_name = org_name.replace("for Supreme Court","")
        reversed = True
    org_name = org_name.replace(" SPAC ","")
    org_name = re.sub(r'\(.*\)',"",org_name) # replace anything inside parentheses
    org_name = org_name.replace(" Jr.","")
    org_name = org_name.replace("Jr.","")
    org_name = org_name.replace("Jr","")
    org_name = org_name.replace("PAC","")
    org_name = re.sub(r'[A-Za-z]{1,1}\.',"",org_name) # replace single letters followed by periods
    org_name = re.sub(r"\'.*\'","",org_name) # replace anything inside parentheses
    org_name = org_name.title()
    org_name = org_name.replace("  "," ")
    org_name = org_name.strip()
    return org_name

d = list(map(replace_func,org_names))
dat_file["filerName2"] = d

dat_file = dat_file.reindex_axis(sorted(dat_file.columns),axis=1)
dat_file = dat_file[["filerName","filerName2"]]
dat_file.to_csv(open("../../data/cleaned_data.csv","w+"),index=False)

