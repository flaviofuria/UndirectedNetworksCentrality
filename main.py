import networkx as nx
import matplotlib.pyplot as plt
from bisect import insort
import centralities

if __name__ == '__main__':

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
    isolated = True
    if isolated:
        isolated_nodes = [int(item) for item in input("add, if present, isolated nodes (separated by a whitespace) : ").split()]
        for node in isolated_nodes:
            if node not in nodes:
                insort(nodes, node)

    # creating graph
    temp_graph = nx.empty_graph()
    temp_graph.add_nodes_from(nodes)
    temp_graph.add_edges_from(edges)

    # adding new_edge
    new_edge = tuple(map(int, input('insert new edge: ').split()))
    if len(new_edge) != 2 or new_edge in temp_graph.edges:
        exit(1)
    new_edges = edges
    new_edges.append(new_edge)
    new_nodes = nodes
    if new_edge[0] not in new_nodes:
        insort(new_nodes, new_edge[0])
    if new_edge[1] not in new_nodes:
        insort(new_nodes, new_edge[1])

    print('For matters of consistency, nodes should be labeled from 1 to *node cardinality*, without holes.\nFor this reason, labels will be remapped.')

    # creating new_graph
    temp_new_graph = nx.empty_graph()
    temp_new_graph.add_nodes_from(new_nodes)
    temp_new_graph.add_edges_from(new_edges)

    # mapping
    mapping = {x: y for y, x in enumerate(temp_graph.nodes, 1)}
    graph = nx.relabel_nodes(temp_graph, mapping)

    # new_mapping
    new_mapping = {x: y for y, x in enumerate(temp_new_graph.nodes, 1)}
    new_graph = nx.relabel_nodes(temp_new_graph, new_mapping)

    # adding edge_colors and showing graph
    # edge_colors = ['r' if edge == new_edge or edge == (new_edge[1], new_edge[0]) else 'k' for edge in new_graph.edges]
    # pos = nx.drawing.layout.spring_layout (new_graph, k=1, seed=200)
    # nx.draw(new_graph, with_labels=True, edge_color=edge_colors)
    # plt.show()

    # computing eigenvcector centrality and seeley
    # using numpy for the graph without the edge
    eigenvector = centralities.seeley(graph, False)
    seeley = centralities.seeley(graph, True)
    # using power iteration for the graph without the edge
    power = centralities.power_iteration(graph, False)
    power_seeley = centralities.power_iteration(graph, True)
    # using numpy for the new graph
    new_eigenvector = centralities.seeley(new_graph, False)
    new_seeley = centralities.seeley(new_graph, True)
    # using power iteration for the new graph
    new_power = centralities.power_iteration(new_graph, False)
    new_power_seeley = centralities.power_iteration(new_graph, True)

    # printing centralities
    print('prima')
    print(eigenvector)
    print(power)
    print(seeley)
    print(power_seeley)
    print('dopo')
    print(new_eigenvector)
    print(new_power)
    print(new_seeley)
    print(new_power_seeley)

    # networkx implementation of eigenvector centrality
    # print(nx.eigenvector_centrality(graph))
    # print(nx.eigenvector_centrality(new_graph))




