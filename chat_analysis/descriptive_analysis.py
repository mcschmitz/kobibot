import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

from chat_analysis.utils import plot_msg_overview
from preprocess_data import MSG_TABLE_OUT_PATH

msg_table = pd.read_csv(MSG_TABLE_OUT_PATH, encoding="utf-8")
msg_table["Datetime"] = pd.to_datetime(msg_table["Time"], format="%d.%m.%y, %H:%M")
msg_table["Date"] = [t.date() for t in msg_table["Datetime"]]
msg_table["Time"] = [t.time() for t in msg_table["Datetime"]]

senders = msg_table["Sender"].unique().tolist()
senders.append(None)
for sender in senders:
    data = msg_table[msg_table["Sender"] == sender] if sender else msg_table
    if sender:
        path = "chat_analysis/plots/mgs_time_date_{}.png".format(sender)
    else:
        path = "chat_analysis/plots/mgs_time_date.png"
    plot_msg_overview(data, path)

msg_table = msg_table
msg_table["Count"] = 1
msg_table = msg_table.set_index(["Date"])
msg_table.set_index(pd.DatetimeIndex(msg_table.index), inplace=True)
msg_table = msg_table.iloc[msg_table.index.year < 2019, :]

msg_length = msg_table
msg_length = msg_length.groupby(pd.Grouper(freq="D")).agg({"Count": "count", "nWords": "sum"})
msg_length = msg_length.groupby(pd.Grouper(freq="Y")).agg({"Count": ["mean", "sum"], "nWords": "sum"})
msg_length["AvgWords"] = msg_length["nWords"]["sum"] / msg_length["Count"]["sum"]
msg_length["AvgMsgs"] = msg_length["Count"]["mean"]
msg_length.drop(columns=["nWords", "Count"], inplace=True)
fig, ax = plt.subplots(figsize=(8, 4))
p = sns.scatterplot("AvgMsgs", "AvgWords", data=msg_length, ax=ax)
p.set_xlabel("Avg. Messages per day")
p.set_ylabel("Avg. Number of Words per Message")
for line in range(0, msg_length.shape[0]):
    p.text(msg_length["AvgMsgs"][line], msg_length["AvgWords"][line] * 1.001, msg_length.index[line].year,
           horizontalalignment='left', size='medium', color='black', weight='semibold')
fig.savefig("chat_analysis/plots/msg_length_year.png")

msg_table = msg_table.set_index(["Date", "Sender"])
msg_length_sender = msg_table.groupby(["Date", "Sender"]).agg({"Count": "count", "nWords": "sum"})
msg_length_sender = msg_length_sender.groupby("Sender").mean()
fig, ax = plt.subplots(figsize=(8, 4))
p = sns.scatterplot("Count", "nWords", data=msg_length_sender, ax=ax, hue=msg_length_sender.index)
p.set_xlabel("Avg. Messages per day")
p.set_ylabel("Avg. Number of Words per Message")
p.legend_.remove()
for line in range(0, msg_length_sender.shape[0]):
    p.text(msg_length_sender["Count"][line], msg_length_sender["nWords"][line] * 1.001, msg_length_sender.index[line],
           horizontalalignment='left', size='medium', color='black', weight='semibold')
fig.savefig("chat_analysis/plots/msg_length_sender.png")
