import numpy as np
import pandas as pd
from cdlib import algorithms
from nxviz.plots import CircosPlot

from metadata_analysis.utils import build_graph
from preprocessing.preprocess_data import MSG_TABLE_OUT_PATH

data = pd.read_csv(MSG_TABLE_OUT_PATH, encoding="utf-8")

graph_nx = build_graph(data, node_col="Sender", to_col="ResponseFrom", output_format="networkx",
                       scale_edge_weights=False)
weights = np.array([i[2]["weight"] for i in list(graph_nx.edges.data())])
weights = weights / max(weights) * 10

c = CircosPlot(graph_nx, edge_width=weights.tolist(), node_labels=True, node_size="msg_freq", node_color="sender",
               edge_color="sender", figsize=(9, 9))
c.draw()
c.figure.savefig("metadata_analysis/plots/msg_flow.png")

graph_i = build_graph(data, node_col="Sender", to_col="ResponseFrom", output_format="igraph", scale_edge_weights=True)
communities = algorithms.rb_pots(graph_i, weights="weight", resolution_parameter=1.1)

graph_nx = build_graph(data, node_col="Sender", to_col="ResponseFrom", output_format="networkx",
                       scale_edge_weights=True)
weights = np.array([i[2]["weight"] for i in list(graph_nx.edges.data())])
weights = weights / max(weights) * 10
for node in graph_nx.nodes():
    graph_nx.nodes[node]["community"] = [idx for idx, c in enumerate(communities.communities) if node in c][0]

for edge in graph_nx.edges():
    graph_nx.edges()[edge]["community"] = [idx for idx, c in enumerate(communities.communities) if edge[0] in c][0]

c = CircosPlot(graph_nx, edge_width=weights.tolist(), node_labels=True, node_size="msg_freq", node_color="community",
               node_grouping="community", edge_color="community", figsize=(9, 9))
c.draw()
c.figure.savefig("metadata_analysis/plots/msg_flow_communities.png")
