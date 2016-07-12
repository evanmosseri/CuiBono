from pyquery import PyQuery as pq
import pandas as pd
from pprint import pprint
import itertools
from utils import *
from get_bills import *

filers = pd.read_csv("/v/filer4b/v38q001/zin/filers.csv")


def lookup_legislator(**lookup):
    print(filers["filerIdent"])
    dic = {}
    if lookup["filerIdent"]:
        # Look up via the filer id
        # Pulls the name
        legislator = (
            filers[filers["filerIdent"] == lookup["filerIdent"]].iloc[0])
        name = legislator["filerNameFirst"] + " " + legislator["filerNameLast"]

        dic["filerName"] = name
        dic["filerIdent"] = str(legislator["filerIdent"])

        for year in range(71, 84):
            print(pq("http://www.lrl.state.tx.us/legeLeaders/members/membersearch.cfm",
                     data={"leg": year}, method="post"))

    elif lookup["filerName"]:
        legislator = (
            filers[filers["filerIdent"] == get_id(lookup["filerName"])].iloc[0])

        name = + legislator["filerNameLast"] + " " + legislator["filerNameFirst"]

        dic["filerName"] = name
        dic["filerIdent"] = str(legislator["filerIdent"])
        # look up via the name
    else:
        print("Couldn't find your legislator")
        return False

sessions_page = pq(
    "http://www.lrl.state.tx.us/legeLeaders/members/lrlhome.cfm")("select[name='leg'] option:gt(0)")
sessions = list(map(lambda x: pq(x).attr("value"), sessions_page))[:15]


def get_sess(sess):
    jq = pq("http://www.lrl.state.tx.us/legeLeaders/members/membersearch.cfm",
            data={"leg": sess}, method="post")
    for row in jq("tr:gt(0)"):
        yield {
        "Name": pq(row)("td").eq(0).text().replace("\n","").replace("\r","").strip().encode("utf-8"),
        "District": pq(row)("td").eq(1).text().replace("\n","").replace("\r","").strip().encode("utf-8"),
        "Chamber": pq(row)("td").eq(2).text().replace("\n","").replace("\r","").strip().encode("utf-8"),
        "Years": pq(row)("td").eq(3).text().replace("\n","").replace("\r","").strip().encode("utf-8"),
        "Legislatures": pq(row)("td").eq(4).text().replace("\n","").replace("\r","").strip().encode("utf-8"),
        "Party": pq(row)("td").eq(5).text().replace("\n","").replace("\r","").strip().encode("utf-8"),
        "City": pq(row)("td").eq(6).text().replace("\n","").replace("\r","").strip().encode("utf-8")
        }

def lst(*args):
	return args
dat = concr(lambda x: list(get_sess(x)),sessions)
print(len(dat))


#Will get bios and photos for the House people
def get_house_bio(districtNumber):
	house = pq("http://www.house.state.tx.us/members/member-page/?district=" + str(districtNumber)).make_links_absolute()
	bio = house(".bio_en").text().encode("utf-8").replace("Spanish version","").strip()
	name = re.sub(r"(Rep\.)|(Sen\.)","",house(".member-info:eq(0) h2:eq(0)").text().encode("utf-8")).strip()
	img_url = house("img[alt='Member Photo']").attr("src")
	# print(name)
	dic = {"Name":name, "Bio":bio, "Picture": img_url, "filerIdent": get_id(name)}
	return dic


# for x in range(1,151):
# 	dic = get_house_bio(x)
house_bio = concr(get_house_bio,range(1,151))


#Will get Party,Bio, and name
def get_senate_bio(districtNumber):
	senate = pq("http://www.senate.state.tx.us/75r/senate/members/dist" +str(districtNumber)+"/dist" + str(districtNumber)+ ".htm").make_links_absolute()
	name = senate(".memtitle").text().encode("utf-8").split("Senator ")[1].split(':')[0]
	name = name.split(" ")
	if len(name) <= 2:
		name = name[1] + ", " + name[0]
	elif "Jr." in name:
		name = name[1] + " " +  name[0]
	else:
		name = name[2] + ", " + name[0]

	party = senate(".meminfo").text().encode("utf-8")

	if "Party: " in party:
		party = party.split("Party: ")[1].split(" ")[0]
	else:
		#Lookup later
		party = "N/A"

	img_url = senate("img[width='150']").attr("src")

	bio = senate(".membios").text().encode("utf-8")

	dic = {"Name":name, "Bio":bio, "Picture":img_url, "Party":party, "filerIdent": get_id(name)}
	return dic

senate_bio = concr(get_senate_bio,range(1,32))

#Merge
def merge_bios(house,senate):
	merge_list = []
	for x in house:
		x["Party"] = "N/A"
		print(x["Name"])
		merge_list.append(x)
	for y in senate:
		merge_list.append(y)
	return merge_list

bios = merge_bios(house_bio, senate_bio)



def merge_all(merge_bio, sess):
	merge_list = []

	for x in merge_bio:
		merge_filer = get_id(x["Name"])
		for y in sess:
			#We found the same filerIden
			sess_filer = get_id(y[N])
			if merge_filer in y:
				print("YAY!")

	return merge_list

def merge_politicians(bios,sess):
	merged = []
	for bio in bios:
		s = closest_match(bio["Name"],sess,key="Name")
		merged.append(dict(bio,**s))
	return merged
merge_all(bios,dat)