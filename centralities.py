import networkx as nx
import numpy as np

def degree(g: nx.Graph()) -> dict:
    scores = {}
    for k, v in g.adj.items():
        scores[k] = len(v)
    return scores


def closeness(g: nx.Graph()) -> dict:
    scores = {}
    for x in g.nodes:
        sum_of_distance_from_x = 0
        for y in g.nodes:
            if x != y and nx.has_path(g, x, y):
                sum_of_distance_from_x += nx.shortest_path_length(g, x, y)
        if sum_of_distance_from_x == 0:
            scores[x] = 0
        else:
            scores[x] = 1/sum_of_distance_from_x
    return scores


def lin(g: nx.Graph()) -> dict:
    scores = {}
    for x in g.nodes:
        sum_of_distance_from_x = 0
        reachable_from_x = 0
        for y in g.nodes:
            if x != y and nx.has_path(g, x, y):
                sum_of_distance_from_x += nx.shortest_path_length(g, x, y)
                reachable_from_x += 1
        if reachable_from_x == 0:
            scores[x] = 1
        else:
            scores[x] = (reachable_from_x ** 2)/sum_of_distance_from_x
    return scores


def harmonic(g: nx.Graph()) -> dict:
    return nx.harmonic_centrality(g)


def eigenvector(g: nx.Graph()) -> dict:
    return {k: round(v, 5) for k, v in nx.eigenvector_centrality(g).items()}


def seeley(g: nx.Graph()) -> dict:
    scores = {}
    adj_mat = np.array([[0] * len(g.nodes)] * len(g.nodes), dtype=float)
    for k, v in nx.convert.to_dict_of_lists(g).items():
        for pos in v:
            adj_mat[k - 1][pos - 1] = 1

    # for i in range(len(g.nodes)):
    #     row_sum = np.sum(adj_mat[i])
    #     if row_sum > 0:
    #         adj_mat[i] = np.divide(adj_mat[i], row_sum)

    eigenvalues, eigenvectors = np.linalg.eig(adj_mat)
    dom_eigenvalue = max(np.amax(eigenvalues), np.absolute(np.amin(eigenvalues)))
    max_eigenvalue_index = np.argmax(np.absolute(eigenvalues))
    dom_eigenvector = np.vstack(eigenvectors[:, max_eigenvalue_index]).flatten()

    for i in range(len(dom_eigenvector)):
        scores[i+1] = dom_eigenvector[i]
    return scores


def katz(g: nx.Graph()) -> dict:
    pass


def pagerank(g: nx.Graph()) -> dict:
    pass