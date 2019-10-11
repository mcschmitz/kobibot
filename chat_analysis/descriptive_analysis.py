import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from preprocess_data import MSG_TABLE_OUT_PATH

sns.set_style("whitegrid")
msg_table = pd.read_csv(MSG_TABLE_OUT_PATH, encoding="utf-8")
msg_table["Datetime"] = pd.to_datetime(msg_table["Time"], format="%d.%m.%y, %H:%M")
msg_table["Date"] = [t.date() for t in msg_table["Datetime"]]
msg_table["Time"] = [t.time() for t in msg_table["Datetime"]]

x = msg_table["Date"]
y = [datetime.datetime.strptime(str(y), "%H:%M:%S") for y in msg_table["Time"]]
y0 = datetime.datetime(y[0].year, y[0].month, y[0].day, 0, 0)
y = [(yi - y0).seconds for yi in y]

g = sns.JointGrid(x="Date", y="Time", data=msg_table)
g.fig.set_figwidth(8)
g.fig.set_figheight(4)
g = g.plot_joint(plt.scatter, color="black", alpha=.75, linewidth=0.1)
g.ax_joint.set_yticklabels(np.arange(0, 24, 4))
g.ax_joint.set_ylabel("Time")
g.ax_marg_x.hist(msg_table["Date"], bins=int(np.ceil((msg_table["Date"].max() - msg_table["Date"].min()).days) / 28),
                 color="black", alpha=.75)
g.ax_marg_y.hist(y, bins=24, color="black", alpha=.75, orientation="horizontal")
g.savefig("chat_analysis/plots/mgs_time_date.png")
