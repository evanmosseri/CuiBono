from utils import *
from pprint import pprint
from pyquery import PyQuery as pq

def get_bill_data(bill_sess,bill_name):
	base_url = "http://www.legis.state.tx.us/BillLookup/{}.aspx?LegSess={}&Bill={}"
	res = {"bill_name":bill_name, "bill_sess": bill_sess,"bill_url":base_url.format("History",bill_sess,bill_name),"authors":[],"sponsors":[]}

	history = pq(base_url.format("History",bill_sess,bill_name))
	res["caption"] = history("#cellCaptionText").text().encode("utf-8").decode().strip()
	res["votes"] = dict()

	house_committee = history("td:contains('House Committee')")
	house_committee_votes = dict(map(lambda x:x.strip().split("="),house_committee.parent().parent()("tr[id*='CommitteeVote'] td:last").text().split(" \xa0"))) if house_committee else None

	senate_committee = history("td:contains('Senate Committee')")
	senate_committee_votes = dict(map(lambda x:x.strip().split("="),senate_committee.parent().parent()("tr[id*='CommitteeVote'] td:last").text().split(" \xa0"))) if senate_committee else None

	res["votes"] = {"house_committee":house_committee_votes,"senate_committee":senate_committee_votes}

	text = pq(base_url.format("Text",bill_sess,bill_name)).make_links_absolute()
	links_row = pq(text("#Form1 table tr:eq(1)"))
	def get_links(node):
		col = pq(node)
		return {
			"pdf": col("a[href*='.pdf']").attr("href"),
			"htm": col("a[href*='.htm']").attr("href"),
			"doc": col("a[href*='.doc']").attr("href")
		}
	bill, fiscal_note, analysis = get_links(links_row("td:eq(1)")),get_links(links_row("td:eq(2)")),get_links(links_row("td:eq(3)"))
	res = dict(res,**{"text_url":bill,"fiscal_note_url":fiscal_note,"analysis_url":analysis})


	stages = pq(base_url.format("BillStages",bill_sess,bill_name))
	res = dict(res,**{"current_stage":stages(".bill-status-box-pending:eq(0) .stage").text()})
	return res
if __name__ == "__main__":
	pprint(get_bill_data("84R","HB5"))