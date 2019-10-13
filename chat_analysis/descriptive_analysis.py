import pandas as pd

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
