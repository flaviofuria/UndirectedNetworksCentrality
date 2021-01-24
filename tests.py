import networkx as nx
import numpy as np
import scipy

def katz(g: nx.Graph()) -> dict:
    print(list(nx.all_simple_paths(g, source=1, target=2, cutoff=6)))



def eigenvector(g: nx.Graph()) -> dict:
    return {k: round(v, 5) for k, v in nx.eigenvector_centrality(g).items()}


if __name__ == '__main__':
    pass
