import requests
import json


def get_committee():
	url = "http://openstates.org/api/v1/committees/?state=tx"

	params = {"apikey":"ab6956c704c742fe9d64fc8027be1d3b"}

	resp = requests.get(url=url, params=params)
	text = json.loads(resp.text)

	# print(text)

	committee_id_list = []

	for x in text:
		committee_id_list.append(x["id"])

	committee_list = []

	for idd in committee_id_list:
		url = "http://openstates.org/api/v1/committees/" + str(idd) +"/"
		resp = requests.get(url=url, params=params)
		text = json.loads(resp.text)
		committee_list.append(text)

	print(committee_list)

def get_districts():
	url = "http://openstates.org/api/v1/districts/tx"

	params = {"apikey":"ab6956c704c742fe9d64fc8027be1d3b"}

	resp = requests.get(url=url, params=params)
	text = json.loads(resp.text)

	print(text)

def get_bills():
	url = "http://openstates.org/api/v1/bills/?state=tx&search_window=term:2009-2011"

	params = {"apikey":"ab6956c704c742fe9d64fc8027be1d3b"}

	resp = requests.get(url=url, params=params)
	text = json.loads(resp.text)

	bill_id = []
	bill_dict = {"id":None, "session": None}
	for y in text:
		print(y)
	# 	bill_dict["id"] = y["id"]
	# 	bill_dict["session"] = y["session"]
	# 	bill_id.append(bill_dict)

	# bill_list = []
	# for idd in bill_id:
	# 	url = "http://openstates.org/api/v1/bills/tx/" + str(idd["session"]) + "/" + str(idd['id'])
	# 	resp = requests.get(url=url, params=params)
	# 	text = json.loads(resp.text)
	# 	bill_list.append(text)

	# print(bill_list)

def get_legislator():
	url = "http://openstates.org/api/v1/legislators/?state=tx"

	params = {"apikey":"ab6956c704c742fe9d64fc8027be1d3b"}

	resp = requests.get(url=url, params=params)
	text = json.loads(resp.text)

	legis_leg = []
	for x in text:
		legis_leg.append(x["leg_id"])

	legis_detail = []

	for y in legis_leg:
		url = "http://openstates.org/api/v1/legislators/" + str(y) + "/"
		resp = requests.get(url=url, params=params)
		text = json.loads(resp.text)
		legis_detail.append(text)

	print(legis_detail[0]["full_name"])

if __name__ == "__main__":
	#get_committee()
	# get_districts
	# get_bills()
	get_legislator()