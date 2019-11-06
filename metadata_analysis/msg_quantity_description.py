import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

from metadata_analysis.utils import split_datetime
from preprocess_data import MSG_TABLE_OUT_PATH

data = pd.read_csv(MSG_TABLE_OUT_PATH, encoding="utf-8")
data = split_datetime(data)
data["Count"] = 1
data = data.set_index(["Date"])
data.set_index(pd.DatetimeIndex(data.index), inplace=True)
data = data.iloc[data.index.year < 2019, :]

msg_len_data = data
msg_len_data = msg_len_data.groupby(pd.Grouper(freq="D")).agg({"Count": "count", "nWords": "sum"})
msg_len_data = msg_len_data.groupby(pd.Grouper(freq="Y")).agg({"Count": ["mean", "sum"], "nWords": "sum"})
msg_len_data["AvgWords"] = msg_len_data["nWords"]["sum"] / msg_len_data["Count"]["sum"]
msg_len_data["AvgMsgs"] = msg_len_data["Count"]["mean"]
msg_len_data.drop(columns=["nWords", "Count"], inplace=True)
fig, ax = plt.subplots(figsize=(9, 4))
p = sns.scatterplot("AvgMsgs", "AvgWords", data=msg_len_data, ax=ax)
p.set_xlabel("Avg. Messages per day")
p.set_ylabel("Avg. Number of Words per Message")
for line in range(0, msg_len_data.shape[0]):
    p.text(msg_len_data["AvgMsgs"][line], msg_len_data["AvgWords"][line] * 1.001, msg_len_data.index[line].year,
           horizontalalignment='left', size='medium', color='black', weight='semibold')
fig.savefig("metadata_analysis/plots/msg_length_year.png")

data = data.reset_index()
data = data.set_index(["Date", "Sender"])
msg_len_sndr_data = data.groupby(["Datetime", "Sender"]).agg({"Count": "count", "nWords": "sum"})
msg_len_sndr_data = msg_len_sndr_data.groupby("Sender").mean()
fig, ax = plt.subplots(figsize=(9, 4))
p = sns.scatterplot("Count", "nWords", data=msg_len_sndr_data, ax=ax, hue=msg_len_sndr_data.index)
p.set_xlabel("Avg. Messages per day")
p.set_ylabel("Avg. Number of Words per Message")
p.legend_.remove()
for line in range(0, msg_len_sndr_data.shape[0]):
    p.text(msg_len_sndr_data["Count"][line], msg_len_sndr_data["nWords"][line] * 1.001, msg_len_sndr_data.index[line],
           horizontalalignment='left', size='medium', color='black', weight='semibold')
fig.savefig("metadata_analysis/plots/msg_length_sender.png")
