import datetime

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

sns.set_style("whitegrid")
plt.ioff()


def plot_msg_overview(data, path: str = None):
    """
    Plots a joint consisting of a scatter plot displaying date and time when a message was sent and the marginal
    histograms of the date and time variable to get insights of date based and daytime based activities

    Args:
        data: pandas data frame containing datetime information of all the messages. Should contain at least a "Time"
            column in %H:%M:%S and a "Date" column in datetime format
        path: Where to save the plot
    """
    y = [datetime.datetime.strptime(str(y), "%H:%M:%S") for y in data["Time"]]
    y0 = datetime.datetime(y[0].year, y[0].month, y[0].day, 0, 0)
    y = [(yi - y0).seconds for yi in y]

    g = sns.JointGrid(x="Date", y="Time", data=data)
    g.fig.set_figwidth(9)
    g.fig.set_figheight(4)
    g = g.plot_joint(plt.scatter, color="black", alpha=.75, linewidth=0.1, s=1.5)
    g.ax_joint.set_ylim(0, 24 * 3600)
    g.ax_joint.set_yticks(np.arange(0, 24 * 3600, 4 * 3600))
    g.ax_joint.set_ylabel("Time")
    g.ax_marg_x.hist(data["Date"],
                     bins=int(np.ceil((data["Date"].max() - data["Date"].min()).days) / 28),
                     color="black", alpha=.75)
    g.ax_marg_y.hist(y, bins=24, color="black", alpha=.75, orientation="horizontal")
    if path:
        g.savefig(path)
    return g
