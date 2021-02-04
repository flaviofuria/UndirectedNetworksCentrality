import networkx as nx
import numpy as np
import scipy
import decimal


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


# if norm is True, left eigenvector of the normalized adjacency matrix will be computed (Seeley centrality)
# if norm is False, right eigenvector of the adjacency matrix will be computed (eigenvector centrality
def seeley(g: nx.Graph(), norm: bool) -> dict:
    scores = {k: 0 for k in range(1, len(g.nodes))}
    adj_mat = np.array([[0] * len(g.nodes)] * len(g.nodes), dtype=float)
    for k, v in nx.convert.to_dict_of_lists(g).items():
        for pos in v:
            adj_mat[k - 1][pos - 1] = 1

# normalizing adjacency matrix
    if norm:
        for i in range(len(g.nodes)):
            row_sum = np.sum(adj_mat[i])
            if row_sum > 0:
                adj_mat[i] = np.divide(adj_mat[i], row_sum)

    # computing eigenvalues and eigenvectors
    eigenvalues, eigenvectors = scipy.linalg.eig(adj_mat, left=norm, right=not norm)
    eigenvalues = np.round(eigenvalues, 5)
    eigenvectors = np.round(eigenvectors, 5)
    dom_eigenvector = np.array([0] * len(g.nodes), dtype=float)

    # finding dominant eigenvalue's index
    # if the dominant eigenvalue has an eigenspace >=1, we have no guarantee on the dominant_eigenvector
    dom_eigenvalues_indices = []
    for index in range(len(eigenvalues)):
        if eigenvalues[index] == np.amax(eigenvalues):
            dom_eigenvalues_indices.append(index)

    if len(dom_eigenvalues_indices) > 1:
        print('eigenspace of the dominant eigenvalue is greater than 1')

    # if np.abs(np.amin(eigenvalues)) == np.abs(np.amax(eigenvalues)):
    #     for index in range(len(eigenvalues)):
    #         if eigenvalues[index] == np.amin(eigenvalues):
    #            dom_eigenvalues_indices.append(index)

    # finding dominant eigenvector
    for index in dom_eigenvalues_indices:
        if eigenvalues[index] < np.abs(np.amin(eigenvalues)):
            print('there is a negative eigenvalue strictly bigger than the dominant eigenvalue')
        if (np.vstack(eigenvectors[:, index]) >= 0).all():
            dom_eigenvector = np.vstack(eigenvectors[:, index])
            break
        elif (np.vstack(eigenvectors[:, index]) <= 0).all():
            dom_eigenvector = np.vstack(eigenvectors[:, index])
            dom_eigenvector *= -1
            break
    if (dom_eigenvector == 0).all():
        print('dominant eigenvector has values of different signs')
    dom_eigenvector_sum = sum(dom_eigenvector)
    # dom_eigenvector /= dom_eigenvector_sum
    dom_eigenvector = dom_eigenvector.flatten()
    for i in range(len(dom_eigenvector)):
        scores[i+1] = dom_eigenvector[i]
    scores = {k: round(v, 5) for k, v in scores.items()}

    return scores


# if norm is True, left eigenvector of the normalized adjacency matrix will be computed (Seeley centrality)
# if norm is False, right eigenvector of the adjacency matrix will be computed (eigenvector centrality
def power_iteration(g: nx.Graph(), norm: bool) -> dict:
    vector = np.random.rand(len(g.nodes))
    # vector = np.array([1] * len(g.nodes), dtype=float)
    # vector_sum = sum(vector)
    # vector /= vector_sum
    adj_mat = np.array([[0] * len(g.nodes)] * len(g.nodes), dtype=float)

    for k, v in nx.convert.to_dict_of_lists(g).items():
        for pos in v:
            adj_mat[k - 1][pos - 1] = 1

    if not norm:
        for i in range(len(g.nodes)):
            row_sum = np.sum(adj_mat[i])
            if row_sum > 0:
                adj_mat[i] = np.divide(adj_mat[i], row_sum)

    for _ in range(100):
        if norm:
            vector_next = np.dot(vector, adj_mat)
        else:
            vector_next = np.dot(adj_mat, vector)
        vector_next_norm = np.linalg.norm(vector_next)
        vector = vector_next / vector_next_norm
    vector_sum = sum(vector)
    # vector /= vector_sum
    return {k+1: v for k, v in enumerate(vector)}



def katz(g: nx.Graph()) -> dict:
    pass


# default alpha=0.85
# choosing alpha=1.0 should result in computing Seeley centrality but convergence is not guaranteed
def pagerank(g: nx.Graph(), a: float) -> dict:
    return nx.pagerank(g, alpha=a, max_iter=1000)


def betweenness(g: nx.Graph()) -> dict:
    return nx.betweenness_centrality(g)
