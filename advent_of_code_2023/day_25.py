from itertools import pairwise
from random import sample

import networkx as nx


def run(filename: str, hard: bool) -> int:
    graph = nx.Graph()
    with open(filename, "r") as file:
        for line in file:
            s, ts = line.split(":")
            graph.add_edges_from((s, t) for t in ts.split())
    n = len(graph.nodes())
    while True:
        s, t = sample(graph.nodes(), 2)
        removed = set()
        for _ in range(3):
            removed |= set(pairwise(nx.shortest_path(graph, s, t)))
            graph.remove_edges_from(removed)
        cs = len(nx.node_connected_component(graph, s))
        if cs != n:
            return cs * (n - cs)
        graph.add_edges_from(removed)
