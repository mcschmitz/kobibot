import pandas as pd

from metadata_analysis.utils import plot_msg_overview, split_datetime
from preprocess_data import MSG_TABLE_OUT_PATH

data = pd.read_csv(MSG_TABLE_OUT_PATH, encoding="utf-8")
data = split_datetime(data)
data["Count"] = 1

senders = data["Sender"].unique().tolist()
senders.append(None)
for sender in senders:
    subset = data[data["Sender"] == sender] if sender else data
    if sender:
        path = "metadata_analysis/plots/mgs_time_date_{}.png".format(sender)
    else:
        path = "metadata_analysis/plots/mgs_time_date.png"
    plot_msg_overview(subset, path)
