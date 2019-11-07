import igraph as ig
import networkx as nx
import numpy as np
import pandas as pd


def split_datetime(data, column_name: str = "Time", format: str = "%d.%m.%y, %H:%M"):
    """Separates date and time from a given datetime column

    Splits date and time from the given column by the given format and writes it so separate columns `Date` and `Time`

    Args:
        data: dataframe containing the datetime column
        column_name: datetime column name
        format: datetime format

    Returns:
        the input dataframe with the added columns `Date` and `Time`
    """
    data["Datetime"] = pd.to_datetime(data[column_name], format=format)
    data["Date"] = [t.date() for t in data["Datetime"]]
    data["Time"] = [t.time() for t in data["Datetime"]]
    return data


def build_graph(data, node_col: str, to_col: str, scale_edge_weights: bool = False, output_format: str = "networkx"):
    """Builds a graph that represents a flow of messages

    The resulting graph has nodes represented by the `node_col` with an attribute msg_freq, that represents the
    absolute numbers of messages and edges going fom a sender to an receiver whereby, the receiver is determined by
    the `to_col`. The more weight an edge has, the more messages were send from this sender to this receiver

    Args:
        data: dataset containing the `node_col` and the `to_col`
        node_col: column name of the column determining the sender of the message
        to_col: column name of the column determining the receiver of the specific message
        scale_edge_weights: whether to scale the weights of the edges in the graph
        output_format: build `networkx` or `igraph` graph

    Returns:
        networkx graph
    """
    if output_format not in ["networkx", "igraph"]:
        raise ValueError("output_format has to be either networkx or igraph")

    sender_freq = data[node_col].value_counts()
    sender_freq /= max(sender_freq)
    nodes = sender_freq.to_dict()

    data_from = data.groupby([node_col, to_col]).size().reset_index()
    if scale_edge_weights:
        _, counts = np.unique(data_from[node_col], return_counts=True)
        values = np.repeat(data_from.groupby([node_col]).sum().values, counts.tolist())
        data_from[0] /= values
    data_from = data_from.values

    if output_format == "networkx":
        graph = nx.classes.digraph.DiGraph()
        for n in nodes:
            graph.add_node(n, msg_freq=nodes[n], sender=n)

        for i in data_from:
            graph.add_edge(i[0], i[1], weight=i[2], sender=i[0])

    elif output_format == "igraph":
        graph = ig.Graph(directed=True)
        for n in nodes:
            graph.add_vertex(n, msg_freq=nodes[n], sender=n)

        for i in data_from:
            graph.add_edge(i[0], i[1], weight=i[2], sender=i[0])

    return graph
