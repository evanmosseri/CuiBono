from utils import *
import requests
import json
from pprint import pprint
from scrape_politician import get_filer_info

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

def get_pol_id(first,last):
	first, last = first.lower(), last.lower()



def find_filer_id():
	pass


bills = load_bills()
b = bills[sorted(bills.keys())[1]]

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

def get_sponsors(bill):
	inds = list(map(lambda x: x["leg_id"],b["sponsors"]))
	def get_ind(ind):
		d = get_leg_id_vals(ind)
		print(d["first_name"],d["last_name"])
		d["filer_id"] = get_pol_id(d["first_name"].lower(),d["last_name"].lower())
		return d
	return list(map(get_ind,inds))


# print(get_leg_id_vals(leg))

pprint(get_sponsors(b))

# save_bills()
# # pprint(bills)
# # print(bills[)
# # print(get_bill_by_id(bills[list(bills.keys())[1]]["session"],bills[list(bills.keys())[1]]["bill_id"])["sponsors"])
#

# pprint(lookup_legislator("TXL000195"))