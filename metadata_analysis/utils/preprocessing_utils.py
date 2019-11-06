import networkx as nx
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


def build_graph(data, node_col: str, to_col: str):
    """Builds a graph that represents a flow of messages

    The resulting graph has nodes represented by the `node_col` with an attribute msg_freq, that represents the
    absolute numbers of messages and edges going fom a sender to an receiver whereby, the receiver is determined by
    the `to_col`. The more weight an edge has, the more messages were send from this sender to this receiver

    Args:
        data: dataset containing the `node_col` and the `to_col`
        to_col: column name of the column determining the receiver of the specific message

    Returns:
        networkx graph
    """
    graph = nx.classes.digraph.DiGraph()

    sender_freq = data[node_col].value_counts()
    sender_freq /= max(sender_freq)
    nodes = sender_freq.to_dict()
    for n in nodes:
        graph.add_node(n, msg_freq=nodes[n], sender=n)

    data_from = data.groupby([node_col, to_col]).size().reset_index()
    data_from = data_from.values
    for i in data_from:
        graph.add_edge(i[0], i[1], weight=i[2], sender=i[0])
    return graph
