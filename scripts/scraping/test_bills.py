from utils import *

df = pd.read_csv("{}/bills_politicians.csv".format(shared_dir),dtype=str)

print(len(df[['session','bill_name']].astype(str).apply(lambda row: "{} {}".format(row["session"],row["bill_name"].replace(" ","")),axis=1).drop_duplicates()))