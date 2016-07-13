from utils import *

df = pd.read_csv("../../data/entities_combined_preview.csv")

contributos = {}

df["contributorNameOrganization"] = df["contributorNameOrganization"].map(lambda x: x.title())
df["new"] = [1]*len(df)

dat = df.groupby(["contributorNameOrganization"])
keys = dat.groups.keys()
for i,group in enumerate(dat.groups):
	print(i)
	k = dat.groups[group]
	for ind in k:
		df.ix[ind,"new"] = 1

print(df)



# for i,row in df.iterrows():
# 	print(str(row.to_dict()["contributorNameOrganization"]).title())