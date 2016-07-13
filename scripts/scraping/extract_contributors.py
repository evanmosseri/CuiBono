from utils import *

df = pd.read_csv("../../data/entities_combined.csv")

contributos = {}


def group_data():
	df["contributorNameOrganization"] = df["contributorNameOrganization"].map(lambda x: x.title())
	dat = df.groupby(["contributorNameOrganization"])
	keys = dat.groups.keys()
	df["contributor_id"] = dat.grouper.labels[0]
	contributors = {}
	df.iloc[:10000].to_csv("../../data-shared/entities_combined_grouped_preview.csv",index=False)
	df.to_csv("../../data-shared/entities_combined_grouped.csv",index=False)

# pd.DataFrame(data=contributors,columns=["contributor_id","contributor_name"]).to_csv("../../data-shared/contributors.csv")
# group_data()


def create_contributors():
	contributors = []
	df = pd.read_csv("../../data-shared/entities_combined_grouped.csv")
	df = df.drop_duplicates("contributor_id")
	for i, row in df.iterrows():
		print(i,len(df),sep="/")
		contributors.append({"id":row["contributor_id"],"name":row["contributorNameOrganization"],"zip":row["contributorStreetPostalCode"],"type":"entity"})
	df_out = pd.DataFrame(data=contributors)
	df_out.iloc[:10000].to_csv("../../data-shared/contributors_preview.csv",index=False)
	df_out.to_csv("../../data-shared/contributors.csv",index=False)
create_contributors()
# dat = {}
# for row in pd.read_csv("../../data-shared/entities_combined_grouped.csv")["contributor_id"]


# for i,row in df.iterrows():
# 	print(str(row.to_dict()["contributorNameOrganization"]).title())