# -*- coding: utf-8 -*-

from pyquery import PyQuery as pq
from lxml import etree, html
import webbrowser
import os
from pprint import pprint
import jellyfish
import pickle
import itertools
import numpy as np
import time
from furl import furl
import pandas as pd
import requests
import unicodedata
import glob
import os
from utils import *
from scrape_politician import get_filer_info
import re

def get_legislator_ids():
	for session in range(71,84):
		jq = pq("http://www.capitol.state.tx.us/Members/Members.aspx?Chamber=S",method="post",data={
			"__EVENTTARGET":"ddlLegislature",
			"__EVENTARGUMENT":"",
			"__LASTFOCUS":"",
			"__VIEWSTATE":"/wEPDwUKLTEyMzU1NzAwNA9kFgQCAQ8WAh4JaW5uZXJodG1sBSlUZXhhcyBMZWdpc2xhdHVyZSBPbmxpbmUgLSBTZW5hdGUgTWVtYmVyc2QCAw9kFgQCAQ9kFghmDw8WAh4ISW1hZ2VVcmwFGX4vSW1hZ2VzL2NhcGl0b2xTbWFsbC5qcGcWBB4FV2lkdGgFAzEwOB4GSGVpZ2h0BQI1MGQCAQ8PFgIeBFRleHQFGFRleGFzIExlZ2lzbGF0dXJlIE9ubGluZWRkAgIPDxYCHwQFDlNlbmF0ZSBNZW1iZXJzZGQCAw8WAh8EBZcCPGZvbnQgc3R5bGU9ImZvbnQtd2VpZ2h0OiBib2xkOyBmb250LXNpemU6IDEwcHgiIGNvbG9yPXdoaXRlPkhvdXNlOiA8c2NyaXB0IHNyYz0iL3Rsb2RvY3MvU2Vzc2lvblRpbWUvSG91c2VTZXNzVGltZS5qcyI+PC9zY3JpcHQ+PC9mb250Pjxici8+PGZvbnQgc3R5bGU9ImZvbnQtd2VpZ2h0OiBib2xkOyBmb250LXNpemU6IDEwcHgiIGNvbG9yPXdoaXRlPlNlbmF0ZTogPHNjcmlwdCBzcmM9Ii90bG9kb2NzL1Nlc3Npb25UaW1lL1NlbmF0ZVNlc3NUaW1lLmpzIj48L3NjcmlwdD48L2ZvbnQ+ZAIFD2QWAgIBDxAPFgYeDURhdGFUZXh0RmllbGQFC0Rlc2NyaXB0aW9uHg5EYXRhVmFsdWVGaWVsZAULTGVnaXNsYXR1cmUeC18hRGF0YUJvdW5kZ2QQFQ4QODR0aCBMZWdpc2xhdHVyZRA4M3JkIExlZ2lzbGF0dXJlEDgybmQgTGVnaXNsYXR1cmUQODFzdCBMZWdpc2xhdHVyZRA4MHRoIExlZ2lzbGF0dXJlEDc5dGggTGVnaXNsYXR1cmUQNzh0aCBMZWdpc2xhdHVyZRA3N3RoIExlZ2lzbGF0dXJlEDc2dGggTGVnaXNsYXR1cmUQNzV0aCBMZWdpc2xhdHVyZRA3NHRoIExlZ2lzbGF0dXJlEDczcmQgTGVnaXNsYXR1cmUQNzJuZCBMZWdpc2xhdHVyZRA3MXN0IExlZ2lzbGF0dXJlFQ4CODQCODMCODICODECODACNzkCNzgCNzcCNzYCNzUCNzQCNzMCNzICNzEUKwMOZ2dnZ2dnZ2dnZ2dnZ2dkZGRzlGQlzwOaryD/dPGVcz/B7Z6h+A==",
			"__VIEWSTATEGENERATOR":"6562B401",
			"__EVENTVALIDATION":"/wEWEAK45qqaAgLojdmNCwLw4oPgBwLw4ofgBwLw4rvgBwLw4r/gBwLw4rPgBwLh4t/jBwLh4tPjBwLh4pfgBwLh4ovgBwLh4o/gBwLh4oPgBwLh4ofgBwLh4rvgBwLh4r/gB4Li+zFmx399JGWklJ9zNsHRBf0d",
			"ddlLegislature":str(session)
		})
		jq2 = pq("http://www.capitol.state.tx.us/Members/Members.aspx?Chamber=H",method="post",data={
			"__EVENTTARGET":"ddlLegislature",
			"__EVENTARGUMENT":"",
			"__LASTFOCUS":"",
			"__VIEWSTATE":"/wEPDwUKLTEyMzU1NzAwNA9kFgQCAQ8WAh4JaW5uZXJodG1sBSlUZXhhcyBMZWdpc2xhdHVyZSBPbmxpbmUgLSBTZW5hdGUgTWVtYmVyc2QCAw9kFgQCAQ9kFghmDw8WAh4ISW1hZ2VVcmwFGX4vSW1hZ2VzL2NhcGl0b2xTbWFsbC5qcGcWBB4FV2lkdGgFAzEwOB4GSGVpZ2h0BQI1MGQCAQ8PFgIeBFRleHQFGFRleGFzIExlZ2lzbGF0dXJlIE9ubGluZWRkAgIPDxYCHwQFDlNlbmF0ZSBNZW1iZXJzZGQCAw8WAh8EBZcCPGZvbnQgc3R5bGU9ImZvbnQtd2VpZ2h0OiBib2xkOyBmb250LXNpemU6IDEwcHgiIGNvbG9yPXdoaXRlPkhvdXNlOiA8c2NyaXB0IHNyYz0iL3Rsb2RvY3MvU2Vzc2lvblRpbWUvSG91c2VTZXNzVGltZS5qcyI+PC9zY3JpcHQ+PC9mb250Pjxici8+PGZvbnQgc3R5bGU9ImZvbnQtd2VpZ2h0OiBib2xkOyBmb250LXNpemU6IDEwcHgiIGNvbG9yPXdoaXRlPlNlbmF0ZTogPHNjcmlwdCBzcmM9Ii90bG9kb2NzL1Nlc3Npb25UaW1lL1NlbmF0ZVNlc3NUaW1lLmpzIj48L3NjcmlwdD48L2ZvbnQ+ZAIFD2QWAgIBDxAPFgYeDURhdGFUZXh0RmllbGQFC0Rlc2NyaXB0aW9uHg5EYXRhVmFsdWVGaWVsZAULTGVnaXNsYXR1cmUeC18hRGF0YUJvdW5kZ2QQFQ4QODR0aCBMZWdpc2xhdHVyZRA4M3JkIExlZ2lzbGF0dXJlEDgybmQgTGVnaXNsYXR1cmUQODFzdCBMZWdpc2xhdHVyZRA4MHRoIExlZ2lzbGF0dXJlEDc5dGggTGVnaXNsYXR1cmUQNzh0aCBMZWdpc2xhdHVyZRA3N3RoIExlZ2lzbGF0dXJlEDc2dGggTGVnaXNsYXR1cmUQNzV0aCBMZWdpc2xhdHVyZRA3NHRoIExlZ2lzbGF0dXJlEDczcmQgTGVnaXNsYXR1cmUQNzJuZCBMZWdpc2xhdHVyZRA3MXN0IExlZ2lzbGF0dXJlFQ4CODQCODMCODICODECODACNzkCNzgCNzcCNzYCNzUCNzQCNzMCNzICNzEUKwMOZ2dnZ2dnZ2dnZ2dnZ2dkZGRzlGQlzwOaryD/dPGVcz/B7Z6h+A==",
			"__VIEWSTATEGENERATOR":"6562B401",
			"__EVENTVALIDATION":"/wEWEAK45qqaAgLojdmNCwLw4oPgBwLw4ofgBwLw4rvgBwLw4r/gBwLw4rPgBwLh4t/jBwLh4tPjBwLh4pfgBwLh4ovgBwLh4o/gBwLh4oPgBwLh4ofgBwLh4rvgBwLh4r/gB4Li+zFmx399JGWklJ9zNsHRBf0d",
			"ddlLegislature":str(session)
		})
		yield list(map(lambda x: furl(pq(x).attr("href")).args["Code"],jq("a[href*='MemberInfo.aspx?']")))
		yield list(map(lambda x: furl(pq(x).attr("href")).args["Code"],jq2("a[href*='MemberInfo.aspx?']")))

# leg_ids = np.unique(list(itertools.chain(*list(get_legislator_ids()))))
leg_ids = ['A1005', 'A1010', 'A1015', 'A1020', 'A1025', 'A1030', 'A1035', 'A1040', 'A1045',
 'A1060', 'A1065', 'A1070', 'A1075', 'A1080', 'A1100', 'A1105', 'A1120', 'A1130',
 'A1140', 'A1145', 'A1150', 'A1155', 'A1160', 'A1165', 'A1170', 'A1175', 'A1180',
 'A1185', 'A1190', 'A1200', 'A1205', 'A1210', 'A1215', 'A1220', 'A1225', 'A1230',
 'A1235', 'A1240', 'A1245', 'A1250', 'A1260', 'A1270', 'A1275', 'A1290', 'A1295',
 'A1300', 'A1305', 'A1310', 'A1320', 'A1360', 'A1400', 'A1410', 'A1415', 'A1420',
 'A1430', 'A1435', 'A1440', 'A1450', 'A1455', 'A1460', 'A1470', 'A1475', 'A1480',
 'A1490', 'A1500', 'A1530', 'A1540', 'A1550', 'A1560', 'A1590', 'A1600', 'A1605',
 'A1610', 'A1615', 'A1620', 'A1625', 'A1640', 'A1650', 'A1655', 'A1700', 'A2005',
 'A2010', 'A2015', 'A2020', 'A2025', 'A2030', 'A2035', 'A2040', 'A2045', 'A2050',
 'A2055', 'A2060', 'A2065', 'A2070', 'A2075', 'A2080', 'A2085', 'A2090', 'A2095',
 'A2100', 'A2105', 'A2110', 'A2115', 'A2120', 'A2125', 'A2130', 'A2135', 'A2140',
 'A2145', 'A2150', 'A2155', 'A2160', 'A2165', 'A2170', 'A2175', 'A2180', 'A2185',
 'A2190', 'A2195', 'A2200', 'A2205', 'A2210', 'A2215', 'A2220', 'A2225', 'A2230',
 'A2235', 'A2240', 'A2245', 'A2250', 'A2255', 'A2260', 'A2265', 'A2270', 'A2275',
 'A2280', 'A2285', 'A2290', 'A2295', 'A2300', 'A2305', 'A2310', 'A2315', 'A2320',
 'A2325', 'A2330', 'A2335', 'A2340', 'A2345', 'A2350', 'A2355', 'A2360', 'A2365',
 'A2370', 'A2375', 'A2380', 'A2385', 'A2390', 'A2395', 'A2400', 'A2405', 'A2410',
 'A2415', 'A2420', 'A2425', 'A2430', 'A2435', 'A2440', 'A2445', 'A2450', 'A2455',
 'A2460', 'A2465', 'A2470', 'A2475', 'A2480', 'A2485', 'A2490', 'A2495', 'A2500',
 'A2505', 'A2510', 'A2515', 'A2520', 'A2525', 'A2530', 'A2535', 'A2545', 'A2550',
 'A2555', 'A2560', 'A2565', 'A2570', 'A2575', 'A2580', 'A2585', 'A2590', 'A2595',
 'A2600', 'A2605', 'A2610', 'A2615', 'A2620', 'A2625', 'A2630', 'A2635', 'A2640',
 'A2645', 'A2646', 'A2650', 'A2655', 'A2660', 'A2665', 'A2670', 'A2675', 'A2680',
 'A2685', 'A2690', 'A2695', 'A2700', 'A2705', 'A2710', 'A2715', 'A2720', 'A2725',
 'A2730', 'A2735', 'A2740', 'A2745', 'A2750', 'A2755', 'A2760', 'A2765', 'A2770',
 'A2775', 'A2780', 'A2785', 'A2790', 'A2795', 'A2800', 'A2805', 'A2810', 'A2815',
 'A2820', 'A2825', 'A2830', 'A2835', 'A2840', 'A2845', 'A2850', 'A2855', 'A2860',
 'A2865', 'A2870', 'A2875', 'A2880', 'A2900', 'A2910', 'A2915', 'A2920', 'A2925',
 'A2930', 'A2935', 'A2940', 'A2945', 'A2950', 'A2960', 'A2980', 'A2985', 'A2990',
 'A3000', 'A3005', 'A3010', 'A3020', 'A3025', 'A3030', 'A3035', 'A3045', 'A3050',
 'A3100', 'A3120', 'A3130', 'A3140', 'A3150', 'A3155', 'A3160', 'A3165', 'A3170',
 'A3175', 'A3180', 'A3190', 'A3230', 'A3240', 'A3250', 'A3260', 'A3270', 'A3275',
 'A3280', 'A3285', 'A3290', 'A3295', 'A3300', 'A3305', 'A3310', 'A3315', 'A3320',
 'A3325', 'A3330', 'A3340', 'A3345', 'A3350', 'A3355', 'A3360', 'A3365', 'A3370',
 'A3375', 'A3380', 'A3385', 'A3395', 'A3400', 'A3405', 'A3410', 'A3415', 'A3420',
 'A3430', 'A3440', 'A3450', 'A3460', 'A3465', 'A3470', 'A3475', 'A3480', 'A3485',
 'A3490', 'A3495', 'A3500', 'A3510', 'A3520', 'A3540', 'A3550', 'A3560', 'A3570',
 'A3590', 'A3600', 'A3605', 'A3610', 'A3615', 'A3620', 'A3630', 'A3640', 'A3650',
 'A3660', 'A3665', 'A3670', 'A3680', 'A3690', 'A3700', 'A3705', 'A3715', 'A3720',
 'A3730', 'A3750', 'A3755', 'A3760', 'A3780', 'A3790', 'A3815', 'A3825', 'A3830',
 'A3835', 'A3840', 'A3845', 'A3847', 'A3848', 'A3850', 'A3855', 'A3860', 'A3865',
 'A3870', 'A3875', 'A3880', 'A3885', 'A3886', 'A3890', 'A3895', 'A3900', 'A3905',
 'A3930', 'A3940', 'A3945', 'A3990', 'A3995', 'A4005', 'A4010', 'A4020', 'A4030',
 'A4040', 'A4050', 'A4060', 'A4070', 'A4080', 'A4090', 'A4100', 'A4110', 'A4140',
 'A4160', 'A4175', 'A4180', 'A4185', 'A4190', 'A4200', 'A4210', 'A4215', 'A4220',
 'A4225', 'A4230', 'A4235', 'A4236', 'A4240', 'A4245', 'A4250', 'A4260', 'A4270',
 'A4300', 'A4305', 'A4310', 'A4315', 'A4320', 'A4325', 'A4330', 'A4350', 'A4370',
 'A4375', 'A4380', 'A4400', 'A4410', 'A4420', 'A4425', 'A4430', 'A4435', 'A4440',
 'A4445', 'A4450', 'A4455', 'A4460', 'A4470', 'A4490', 'A4500', 'A4505', 'A4510',
 'A4515', 'A4525', 'A4530', 'A4540', 'A4545', 'A4550', 'A4560', 'A4565', 'A4570',
 'A4580', 'A4585', 'A4590', 'A4600', 'A4605', 'A4610', 'A4625', 'A4630', 'A4635',
 'A4640', 'A4650', 'A4660', 'A4680', 'A4685', 'A4690', 'A4695', 'A4700', 'A4720',
 'A4725', 'A4730', 'A4740', 'A4750', 'A4760', 'A4780', 'A4790', 'A4800', 'A4810',
 'A4850', 'A4900', 'A4930', 'A4950', 'A4960', 'A4970', 'A4980', 'A4985', 'A4990',
 'A4995', 'A5000', 'A5005', 'A5010', 'A5015', 'A5020', 'A5025', 'A5030', 'A5035',
 'A5040', 'A5150', 'A5170']

sessions = ["84R", "833", "832", "831", "83R", "821", "82R", "811", "81R", "80R", "793", "792", "791", "79R", "784", "783", "782", "781", "78R", "77R", "76R", "75R", "74R", "73R", "724", "723", "722", "721", "72R", "716", "715", "714", "713", "712", "711", "71R"]

bills = {}
shared_dir = "../../data-shared"

def get_closest_match(x, list_strings,attr="filerName",baseline=.6):
	def parse_filer_name(st):
		# print(st)
		x = re.sub(r" \(.{1,20}\)","",st)
		x = re.sub(r" (Jr\.)|(Sr\.)","",x)
		# x = x.replace("(The Honorable)","")
		return x
	# x = parse_filer_name(x)
	filt = list(filter(lambda c: c.startswith(x),list(map(parse_filer_name,list_strings))))
	if len(filt):
		return filt[0]
	best_match = None
	highest_jw = 0

	for current_string in list_strings:
		current_string = parse_filer_name(current_string)
		current_score = max(
			jellyfish.jaro_winkler(x, current_string),
			jellyfish.jaro_winkler(x, ", ".join(reversed(str(extract_filer_name(current_string)).split(" ")))))

	if(current_score > highest_jw):
		highest_jw = current_score
		best_match = current_string
	print(best_match)
	if highest_jw > baseline:
		return best_match
	else:
		info = None
		first,last = x.replace(",","").split(" ")[-1].lower(),x.replace(",","").split(" ")[0].lower()
		try:
			print(x.replace(",","").split(" ")[-1].lower(),x.replace(",","").split(" ")[0].lower())
			info = get_filer_info(first,last)
			print(info)
			bst = filers[filers["filerIdent"] == int(info[0].get("id"))]["filerName"].values[0]
			if(bst != "Tanner, Germaine (Ms.)"):
				return bst
			else:
				raise IndexError
		except IndexError as e:
			try:
				print(x.replace(",","").split(" ")[-1].lower()[0],x.replace(",","").split(" ")[0].lower())
				info = get_filer_info(first[0],last)
				print(info)
				bst = filers[filers["filerIdent"] == int(info[0].get("id"))]["filerName"].values[0]
				return bst
			except IndexError as e2:
				print(e2)
				print(info)
				print("not found")
			print(e)
			print(info)
			print("not found")
			if highest_jw > .5:
				return best_match
			return -1


# print(filers["filerName"].tolist())
d = filers[filers["filerPersentTypeCd"] == "INDIVIDUAL"]["filerName"].tolist()
def get_id(name):
	# print("get_id: {}".format(name))
	dnew = filers[filers["filerName"]==get_closest_match(name,d)]
	return dnew.iloc[0].to_dict() if len(dnew) else -1
def get_pq(url,n=0):
	try:
		return pq(url)
	except:
		print("Retrying URL for {} time".format(n+1))
		return get_pq(url,n=n+1)

def get_bills(author_ids,debug=False):
	base_url = "http://www.capitol.state.tx.us/reports/report.aspx?LegSess={}&ID={}&Code={}"
	def get_author_name(sess=iter(sessions)):
		url = base_url.format(next(sess),"author",author_ids)
		jq = get_pq(url)
		author_name = extract_filer_name(unicodedata.normalize('NFKD',jq("span.TitleItem:eq(1)").text()).replace("́","").replace("Sen.","").replace("Rep.","").replace("Lt. Gov","").strip())
		if author_name:
			return [author_name,get_id(", ".join(reversed(author_name.split(" "))))["filerIdent"]]
		else:
			try:
				return get_author_name(sess)
			except StopIteration:
				return (None,None)
	author_name,author_id = get_author_name()
	print(author_name,author_id)

	def get_session(leg_session):
		for func in ["author","coauthor","sponsor","cosponsor"]:
			jq = get_pq(base_url.format(leg_session,func,author_ids))
			for i in jq("table"):
				yield {"session": leg_session,
					   "filer_name":author_name,
					   "function": func,
					   "filer_id":author_id,
					   "caption": pq(i)('td:contains("Caption:")+td').text(),
					   "bill_name":pq(i)("a").text()
					   }
			print("{}: {}".format(leg_session,author_name))
	return concr(lambda x: list(get_session(x)),sessions,max_workers=10)


	if debug:
		handle = open("out.html","w+")
		handle.write(etree.tostring(html.fromstring(str(jq)), encoding='unicode', pretty_print=True))
		handle.close()
		webbrowser.open("File://"+os.path.abspath("./out.html"))
# t = time.time()
# pd.DataFrame(list(get_bills("A1035"))).to_csv("../../data/bill_actions.csv",index=False)
# print(time.time() - t)
# print()
# print(leg_ids)
def download_bills(id,overwrite=False):
	if not(os.path.exists("{}/bills_politicians/bill_actions_{}.csv".format(shared_dir,id))) or overwrite:
		pd.DataFrame(list(get_bills(id))).to_csv("{}/bills_politicians/bill_actions_{}.csv".format(shared_dir,id),index=False)
		print(id)
	else:
		print("{} Skipped".format(id))

# for leg_id in leg_ids:
# 	download_bills(leg_id)

# concr(download_bills,leg_ids,max_workers=10)
# multiprocess(download_bills,leg_ids)
# download_bills("A1005",True)
def update_ids():
	def update_file(file):
		leg_id = int(file.split("/")[-1].replace("bill_actions_A","").replace(".csv",""))
		print(leg_id)
		df = pd.read_csv(file)
		# filer_name = df.iloc[0]["filer_name"].replace(". ","").replace("Lt. Gov. ","").strip()
		filer_name = df.iloc[0]["parsed_name"]
		name = ", ".join(reversed(filer_name.split(" ")))
		ans = get_id(name)
		df["leg_id"] = [leg_id]*len(df)
		df["filer_id"] = [ans["filerIdent"]]*len(df) if (type(ans) is dict) else [-1]*len(df)
		df.to_csv(file,index=False)
	concr(update_file,[x for x in glob.glob("../../data-shared/bills_politicians/*") if os.stat(x).st_size > 100],max_workers=100)

		# print(filer_name)
def leg_id_to_name(id):
	base_url = "http://www.capitol.state.tx.us/reports/report.aspx?LegSess={}&ID={}&Code=A{}"
	def get_author_name(sess=iter(sessions),get_filer_id=False):
		url = base_url.format(next(sess),"author",id)
		# print(url)
		jq = get_pq(url)
		author_name = unicodedata.normalize('NFKD',jq("span.TitleItem:eq(1)").text()).replace("́","").replace("  "," ")
		if author_name:
			if get_filer_id:
				return [author_name,get_id(", ".join(reversed(author_name.split(" "))))["filerIdent"]]
			else:
				return author_name
		else:
			try:
				return get_author_name(sess)
			except StopIteration:
				if get_filer_id:
					return (None,None)
				else:
					return None
	return get_author_name()

def update_original_names():
	def update_file(file):
		leg_id = int(file.split("/")[-1].replace("bill_actions_A","").replace(".csv",""))
		df = pd.read_csv(file)
		def can_int(st):
			try:
				int(st)
				return True
			except:
				return False
			print(df.iloc[0]["original_name"])
		if not "original_name" in df or can_int(df.iloc[0]["original_name"]):
			full_name = leg_id_to_name(leg_id)
			print(full_name)
			df["original_name"] = [full_name]*len(df)
			df.to_csv(file,index=False)
			print("Added original names of {}".format(leg_id))
		else:
			print("Skipped {}".format(leg_id))
	concr(update_file,[x for x in glob.glob("../../data-shared/bills_politicians/*") if os.stat(x).st_size > 100],max_workers=10)
def update_new_names():
	def update_new_name(file):
		df = pd.read_csv(file)
		original = df.iloc[0]["original_name"]
		name = re.sub(r'(Sen\.)|(Rep\.)|(Lt\. Gov\.)',"",original)
		name = re.sub(r"\".*\"","",name)
		name = re.sub(r"(Jr\.)|(Sr\.)","",name)
		name = name.strip().replace("  "," ")
		name = re.sub(r' \b(?=[MDCLXVI]+\b)M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})\b',"",name)
		name = name.replace("̃","")
		name = name.replace(",","")
		if len(name.split(" ")) >= 3:
			if not(re.match(r"[A-Za-z]\. [A-Za-z]\.",name)):
				name = " ".join([name.split(" ")[0],name.split(" ")[-1]])
			else:
				name = " ".join([name.split(" ")[0] + "" + name.split(" ")[1],name.split(" ")[-1]])
		# print(original, name,sep="-->\t")
		df["parsed_name"] = [name]*len(df)

		df.to_csv(file,index=False)
	concr(update_new_name,[x for x in glob.glob("../../data-shared/bills_politicians/*") if os.stat(x).st_size > 100])
def remove_index():
	def remove_ind(file):
		df = pd.read_csv(file)
		for col in df.columns:
			if "Unnamed" in col:
				df = df.drop(col,axis=1)
		df.to_csv(file,index=False)
	concr(remove_ind,[x for x in glob.glob("../../data-shared/bills_politicians/*") if os.stat(x).st_size > 100])

if __name__ == "__main__":

	# print(get_closest_match("Rodriguez, Jose",d))
	# print(get_closest_match("Campbell, Donna",d))

	# print(leg_id_to_name("1060"))

	# update_original_names()

	# update_new_names()

	# remove_index()
	update_ids()
	merge_folder(["../../data-shared/bills_politicians/"],func=lookup)

	# print(get_closest_match("Hegar, Glenn",d))
	# print(get_closest_match("Bivins, Teel",d))
	# print(get_closest_match("Rodriguez, Jose",d))