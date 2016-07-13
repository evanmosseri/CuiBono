from utils import *
from pprint import pprint
from pyquery import PyQuery as pq

def get_pq(url,n=0):
	try:
		return pq(url)
	except:
		print("Retrying URL for {} time".format(n+1))
		return get_pq(url,n=n+1)

def get_bill_data(bill_sess,bill_name):
	base_url = "http://www.legis.state.tx.us/BillLookup/{}.aspx?LegSess={}&Bill={}"
	res = {"bill_name":bill_name, "bill_sess": bill_sess,"bill_url":base_url.format("History",bill_sess,bill_name)}

	history = get_pq(base_url.format("History",bill_sess,bill_name))
	# print(base_url.format("History",bill_sess,bill_name))
	res["caption"] = history("#cellCaptionText").text().encode("utf-8").decode().strip()
	res["votes"] = dict()

	house_committee = history("td:contains('House Committee')")
	if house_committee:
		d = house_committee.parent().parent()("tr[id*='CommitteeVote'] td:last").text().split(" \xa0")
		d2 = list(map(lambda x:x.strip().split("="),d))
		if d2 != [[""]]:
			house_committee_votes = dict(d2)
		else:
			house_committee_votes = {}
	else:
		house_committee_votes = {}

	senate_committee = history("td:contains('Senate Committee')")
	if senate_committee:
		d = senate_committee.parent().parent()("tr[id*='CommitteeVote'] td:last").text().split(" \xa0")
		d2 = list(map(lambda x:x.strip().split("="),d))
		if d2 != [[""]]:
			senate_committee_votes = dict(d2)
		else:
			senate_committee_votes = {}
	else:
		senate_committee_votes = {}
	res["votes"] = {"house_committee":house_committee_votes,"senate_committee":senate_committee_votes}

	text = get_pq(base_url.format("Text",bill_sess,bill_name)).make_links_absolute()
	links_row = get_pq(text("#Form1 table tr:eq(1)"))
	def get_links(node):
		col = get_pq(node)
		return {
			"pdf": col("a[href*='.pdf']").attr("href"),
			"htm": col("a[href*='.htm']").attr("href"),
			"doc": col("a[href*='.doc']").attr("href")
		}
	bill, fiscal_note, analysis = get_links(links_row("td:eq(1)")),get_links(links_row("td:eq(2)")),get_links(links_row("td:eq(3)"))
	res = dict(res,**{"text_url":bill,"fiscal_note_url":fiscal_note,"analysis_url":analysis})
	stages = get_pq(base_url.format("BillStages",bill_sess,bill_name))
	res = dict(res,**{"current_stage":stages(".bill-status-box-pending:eq(0) .stage").text()})
	return res
if __name__ == "__main__":
	pprint(get_bill_data("84R","SB474"))