import numpy as np
import pandas as pd
from nxviz.plots import CircosPlot

from metadata_analysis.utils import build_graph
from preprocess_data import MSG_TABLE_OUT_PATH

data = pd.read_csv(MSG_TABLE_OUT_PATH, encoding="utf-8")

graph = build_graph(data, node_col="Sender", to_col="ResponseFrom")

weights = np.array([i[2]["weight"] for i in list(graph.edges.data())])
weights = weights / max(weights) * 10

c = CircosPlot(graph, edge_width=weights.tolist(), node_labels=True, node_size="msg_freq", node_color="sender",
               edge_color="sender", figsize=(9, 9))
c.draw()
c.figure.savefig("metadata_analysis/plots/msg_flow.png")
