from pyquery import PyQuery as pq
import sys
import os
import webbrowser
import requests
from pprint import pprint
from lxml import etree, html
from utils import *
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)



def get_simple_search_cookie():
	return requests.get("https://www.ethics.state.tx.us/jasperserver-pro/flow.html?_flowId=viewReportFlow&standAlone=true&_flowId=viewReportFlow&ParentFolderUri/public/publicData&reportUnit=/public/publicData/datasource/By_Filer_Name&decorate=no&SuperName=straus&FilerType=ANY&FirstName=joe&CorrFlag=N&tec-pp=u=PUBLIC2|expireTime=Sat%20Jul%2002%2020126%2022:30:16%20GMT-0500%20(CDT)",verify=False).cookies.get_dict()["JSESSIONID"]

def get_pq(*args,n=0,**kwargs):
	try:
		return pq(*args,**kwargs)
	except:
		print("Retrying URL for {} time".format(n+1))
		return get_pq(*args,n=n+1,**kwargs)


def get_filer_info(first_name,last_name,debug=False,preview = False, allowed_types = ["COH","JCOH"],cookie=get_simple_search_cookie()):
	jq = get_pq(
		"https://www.ethics.state.tx.us/jasperserver-pro/flow.html?_flowExecutionKey=e1s1&_flowId=viewReportFlow&_eventId=refreshReport&pageIndex=0&decorate=no&confirm=true&decorator=empty&ajax=false",
		data={
			"SuperName":last_name.lower(),
			"FilerType":"ANY",
			"FirstName":first_name.lower(),
			"CorrFlag":"N"
		},
		headers={
			"Referer":"https://www.ethics.state.tx.us/jasperserver-pro/flow.html",
			"Cookie":"JSESSIONID={}; userLocale=en_US; _ga=GA1.3.872699230.1467483680".format(cookie),
			"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
		},
		verify=False
		)
	# print(jq)
	if debug:
		handle = open("./data/out.html","w+")
		handle.write(etree.tostring(html.fromstring(str(jq)), encoding='unicode', pretty_print=True))
		handle.close()
	if debug:
		handle = open("./data/out.html","w+")
		handle.write(etree.tostring(html.fromstring(str(jq)), encoding='unicode', pretty_print=True))
		handle.close()
	if preview:
		webbrowser.open("File://"+os.path.abspath("./data/out.html"))
	dat = [pq(c) for c in list(filter(lambda x: pq(x).text().strip(), jq(".jrPage tr")))[3:-1]][::3]
	# print(dat[0].html())
	dat = [dict(zip(["id","type","name","city","state"],[pq(x).text().replace("'","") for x in i("span:gt(0)")])) for i in dat]
	return list(filter(lambda x: x["type"] in allowed_types,dat)) if len(allowed_types) else dat

# concr(lambda _: list(map(lambda x: pq(x).text(),get_filer_id("kirk","watson",cookie=get_simple_search_cookie()))),range(1,10))
if __name__ == "__main__":
	print(get_filer_info("donna","campbell"))

