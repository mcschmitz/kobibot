import pandas as pd

from metadata_analysis.utils import plot_msg_overview, split_datetime
from preprocess_data import MSG_TABLE_OUT_PATH

msg_table = pd.read_csv(MSG_TABLE_OUT_PATH, encoding="utf-8")
msg_table = split_datetime(msg_table)
msg_table["Count"] = 1

senders = msg_table["Sender"].unique().tolist()
senders.append(None)
for sender in senders:
    data = msg_table[msg_table["Sender"] == sender] if sender else msg_table
    if sender:
        path = "metadata_analysis/plots/mgs_time_date_{}.png".format(sender)
    else:
        path = "metadata_analysis/plots/mgs_time_date.png"
    plot_msg_overview(data, path)
