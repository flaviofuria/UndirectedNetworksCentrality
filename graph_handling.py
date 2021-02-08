import networkx as nx
import matplotlib.pyplot as plt
from bisect import insort
from typing import Tuple


def create(node1: int, node2: int, isolated_nodes=None) -> Tuple[nx.Graph, nx.Graph]:
    new_edge = (node1, node2)

    # importing graph
    with open("graph.txt") as file:
        edges = [tuple(map(int, line.strip().split())) for line in file]

    nodes = []
    for x, y in edges:
        if x not in nodes:
            insort(nodes, x)
        if y not in nodes:
            insort(nodes, y)

    # adding isolated nodes
    if new_edge[0] not in nodes:
        insort(nodes, new_edge[0])
    if new_edge[1] not in nodes:
        insort(nodes, new_edge[1])
    if isolated_nodes:
        for node in isolated_nodes:
            if node not in nodes:
                insort(nodes, node)

    # creating graph
    temp_graph = nx.empty_graph()
    temp_graph.add_nodes_from(nodes)
    temp_graph.add_edges_from(edges)

    # adding new_edge
    if len(new_edge) != 2 or new_edge in temp_graph.edges:
        exit(1)
    new_edges = edges
    new_edges.append(new_edge)

    # For matters of consistency, nodes should be labeled from 1 to *node cardinality*, without holes.\nFor this reason, labels will be remapped.

    # creating new_graph
    temp_new_graph = nx.empty_graph()
    temp_new_graph.add_nodes_from(nodes)
    temp_new_graph.add_edges_from(new_edges)

    # mapping
    mapping = {x: y for y, x in enumerate(temp_graph.nodes, 1)}
    graph = nx.relabel_nodes(temp_graph, mapping)

    # new_mapping
    new_mapping = {x: y for y, x in enumerate(temp_new_graph.nodes, 1)}
    new_graph = nx.relabel_nodes(temp_new_graph, new_mapping)

    return graph, new_graph


def k_path(g: nx.Graph, k: int, head: int, tail: int) -> nx.Graph:
    path = g.copy()
    if head not in path.nodes or tail not in path.nodes:
        print('head or tail are not in the graph')
        return -1

    path.add_edge(head, max(path.nodes)+1)
    k_edges = zip(range(max(path.nodes), max(path.nodes) + k - 1), range(max(path.nodes) + 1, max(path.nodes) + k))
    path.add_edges_from(k_edges)
    path.add_edge(max(path.nodes), tail)
    return path


def k_clique(g: nx.Graph, k: int, head: int, tail: int) -> nx.Graph:
    clique = g.copy()
    if head not in clique.nodes or tail not in clique.nodes:
        print('head or tail are not in the graph')
        return -1

    clique.add_edge(head, max(clique.nodes)+1)
    to_add = [x for x in range(max(clique.nodes), max(clique.nodes)+k)]
    for x in to_add:
        for y in to_add:
            if x != y:
                clique.add_edge(x, y)
    clique.add_edge(max(clique.nodes), tail)
    return clique


def show(g: nx.Graph, node1: int, node2: int, edges=None):
    if (node1, node2) not in g.edges:
        g.add_edge(node1, node2)
    if edges is not None:
        edge_colors = ['r' if edge == (node1, node2) or edge == (node2, node1) else 'g' if edge in edges else 'k' for edge in g.edges]
    else:
        edge_colors = ['r' if edge == (node1, node2) or edge == (node2, node1) else 'k' for edge in g.edges]
    pos = nx.drawing.layout.spring_layout(g, k=1, seed=200)
    nx.draw(g, with_labels=True, edge_color=edge_colors)
    plt.show()
