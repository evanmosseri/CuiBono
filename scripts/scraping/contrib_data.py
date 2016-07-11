import pandas as pd
import csv
from pprint import pprint
# from scripts.utils import *
import sys
import numpy as np
import re
import glob
import argparse
from utils import *
import os

# data_file = csv.DictReader(open("../../data/cont_ss.csv"))
if __name__ == "__main__":
#     print(dat_file)
    # merge_data()
    parser = argparse.ArgumentParser()
    parser.add_argument("-merge", "--merge",help="merges the contribution data files into one csv",type=str)
    parser.add_argument("-pnames", "--pnames",help="gets all contributor names",action="store_true")
    parser.add_argument("-groupby", "--groupby",help="groups the merged dataframe by a column",action="store_true")
    parser.add_argument("-lookup", "--lookup",help="looks up filer by filer id",type=str,required=False)
    parser.add_argument("-filerinfo", "--filerinfo",help="looks up filer info by filer id",type=int,required=False, nargs="*")
    parser.add_argument("-mergefolder", "--mergefolder",help="merges folder of csvs",type=str,required=False, nargs="*")
    args = parser.parse_args()
    
    # df = pd.read_csv("../../data/combined_all_preview.csv")
    # df = pd.read_csv("../../data/combined_all.csv")
    # df = df[df["contributorPersentTypeCd"] == "ENTITY"]
    # df["contributorNameOrganization"] = df["contributorNameOrganization"].apply(lambda x: x.strip())
    # pprint(df.drop_duplicates("contributorNameOrganization")["contributorNameOrganization"].values.tolist())
    def merge_folder(folder,func=lambda x:x):
        # print(folder[0])
        # print(glob.glob("{}/*.csv".format(folder[0])))
        # print("{}/*.csv".format(folder[0]))
        folder = folder[0][:-1] if folder[0][-1] == "/" else folder[0]
        dat = [func(pd.read_csv(filename)) for filename in glob.glob("{}/*.csv".format(folder)) if os.stat(filename).st_size > 100]

        return pd.concat(dat).to_csv("../../data/{}.csv".format(os.path.basename(folder)),index=None)

    filers = pd.read_csv("../../data/texas_ethics_commission/filers.csv")
    def lookup(df):
        ident = df["filer_id"].iloc[0]
        new_name = filers[filers["filerIdent"] == ident]["filerName"].iloc[0]
        df["filer_name_closest"] = [new_name]*len(df)
        return df
    if args.mergefolder:
        merge_folder(args.mergefolder,func=lookup)

    if args.merge:
        if args.merge.lower() == "individual":
            merge_data(filename="individuals_combined.csv",allowed_contributor_types=["INDIVIDUAL"],debug=True)
        elif args.merge.lower() == "entity":
            merge_data(filename="entities_combined.csv",allowed_contributor_types=["ENTITY",""],debug=True)
        elif args.merge.lower() == "all":
            merge_data(filename="combined_all.csv",allowed_contributor_types=["ENTITY","INDIVIDUAL",""],debug=True)

    if args.pnames:
        dat = pd.read_csv("../../data/combined.csv")
        pprint(dat.drop_duplicates("contributorNameOrganization")[["contributorNameOrganization"]].values.tolist())

    if args.groupby:
        dat = pd.read_csv("../../data/combined.csv")
        dat = dat.groupby(["filerIdent"]).sum()["contributionAmount"]
        dat = dat.copy()
        dat.sort()
        pprint(dat.to_dict())

    if args.lookup:
        print(args.lookup,type(args.lookup))
        dat = pd.read_csv("../../data/combined.csv")
        print(dat[dat["filerIdent"] == int(args.lookup)]["contributionAmount"].sum())

    if args.filerinfo:
        pprint(filer_id_lookup(args.filerinfo))

