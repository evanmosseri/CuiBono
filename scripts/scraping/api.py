from utils import *
import requests
import json
from pprint import pprint
from scrape_politician import get_filer_info
import jellyfish
import difflib
import time

# print(get_id("Watson, Kirk")["filerIdent"])
apikey = "bf74569aec8a4ba69d4afcbda75498fe"

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

bills = {}
legislators = {}

def get_bills_with_name(name):
	print("Getting: {}".format(name))
	d = requests.get('http://openstates.org/api/v1/bills/?state=tx',params={"apikey":apikey,"bill_id":name}).json()
	return d

def get_bill_by_id(session,bill_id):
	return requests.get('http://openstates.org/api/v1/bills/tx/{}/{}'.format(session,bill_id),params={"state":"tx","apikey":apikey}).json()

def save_bills():
	bill_names = get_bill_names()
	dat = concr(get_bills_with_name,bill_names[:1000],max_workers=20)
	for i in dat:
		bills[i["id"]] = i

	def lookup_bill(bill):
		bill_lookup = bills[bill]
		bills[bill] = dict(bills[bill],**get_bill_by_id(bill_lookup["session"],bill_lookup["bill_id"]))
	concr(lookup_bill,bills,max_workers=20)
	json.dump(bills,open("{}/bills.json".format(shared_dir),"w"))
def lookup_legislator(leg_id,n=0):
	d = requests.get("http://openstates.org/api/v1/legislators/{}/".format(leg_id),params={"state":"tx","apikey":apikey}).json()
	if len(d) or n > 10:
		return d
	else:
		return lookup_legislator(leg_id,n=n+1)
def load_bills():
	return json.load(open("{}/bills.json".format(shared_dir),"r"))

def closest_match(first,last,df=filers):
	return max(df.iterrows(),key=lambda row: jellyfish.jaro_winkler("{}, {}".format(last.title(),first.title()),row[1]["filerName"]))[1]

def get_pol_id(first,last):
	first, last = first.lower(), last.lower()
	df_lookup = filers[filers["filerName"].str.contains("{}, {}".format(last.title(),first.title()))]
	if len(df_lookup):
		return df_lookup.iloc[0].to_dict()["filerIdent"]
	online_lookup = get_filer_info(first,last)
	if(online_lookup):
		return int(online_lookup[0]["id"])
	best_match = closest_match(first,last)
	if len(best_match):
		return best_match["filerIdent"]
	return -1



bills = load_bills()

# print(b)

def get_leg_id_vals(leg_id,tries=0):
	try:
		leg = lookup_legislator(leg_id)
		return leg
	except Exception as e:
		print(e)
		if tries < 10:
			return get_leg_id_vals(leg_id,tries=tries+1)
		else:
			return None

def get_keys(da,keys):
	return {k:v for k,v in da.items() if ((k in keys) and (k in da))}

def get_sponsors(bill):
	inds = list(filter(lambda x:x,list(map(lambda x: x["leg_id"],bill["sponsors"]))))
	def get_ind(ind):
		d = get_leg_id_vals(ind)
		# print(d["first_name"],d["last_name"])
		id = get_pol_id(d["first_name"].lower(),d["last_name"].lower())
		d["filer_id"] = id
		return get_keys(d,["filer_id","party","photo_url","offices","id","district","first_name","last_name","middle_name","sources"])
	ret = concr(get_ind,inds)
	print(bill["id"])
	return ret

def extract_bill_info(bill):
	return dict(dict(get_keys(bill,
				["sponsors","subjects","title","sources","id","session"]),
				**(get_keys(bill["votes"][-1],["yes_count","no_count","yes_votes","no_votes"]) if len(bill["votes"]) else {})
				),prefix=bill["bill_id"].split(" ")[0],number=bill["bill_id"].split(" ")[1])

def save_extracted_bill_data():
	pd.DataFrame(data=list(map(extract_bill_info,bills.values()))).to_csv("{}/bill_data.csv".format(shared_dir),index=False)

t = time.time()

def get_chunk(chunk):
	return concr(get_sponsors,chunk,max_workers=10)

def save_legislators():
	bs = list(map(lambda x: x[1],list(sorted(bills.items(),key=lambda a: int(a[0][3:])))))
	pd.DataFrame(data=multiprocess(get_sponsors,bs)).drop_duplicates("id").to_csv("{}/legislators.csv".format(shared_dir),index=False)


# for bill in list(bills.values())[:5]:
# 	# pprint(bill)
# 	pprint(extract_bill_info(bill))



print(time.time()-t)
	# pprint(get_sponsors(bills[bill]))

# print(get_pol_id("John","Carona"))

# print(closest_match("John","Carona"))