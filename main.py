import matplotlib.pyplot as plt
import centralities
import graph_handling

if __name__ == '__main__':

    new_edge = (1, 3)
    k, head, tail = 5, 1, 3
    graph, new_graph = graph_handling.create(new_edge[0], new_edge[1])

    # creating graph with k_path
    path = graph_handling.k_path(new_graph, k, head, tail)
    k_path_edges = list(set(path.edges) - set(new_graph.edges))

    # creating graph with k_clique
    clique = graph_handling.k_clique(new_graph, k, head, tail)
    k_clique_edges = list(set(clique.edges) - set(new_graph.edges))

    # computing scores for old and new k_path and k_clique graph
    k_path_score, k_clique_score = centralities.eigenvector_at_k(graph, k, head, tail, False)
    new_k_path_score, new_k_clique_score = centralities.eigenvector_at_k(new_graph, k, head, tail, False)

    # scores of first and second node for old k_path graph
    first_node_scores_path = [k_path_score[k][new_edge[0]] for k in k_path_score.keys()]
    second_node_scores_path = [k_path_score[k][new_edge[1]] for k in k_path_score.keys()]
    # scores of first and second node for new k_path graph
    new_first_node_scores_path = [new_k_path_score[k][new_edge[0]] for k in new_k_path_score.keys()]
    new_second_node_scores_path = [new_k_path_score[k][new_edge[1]] for k in new_k_path_score.keys()]
    # score differences for k_path graph
    first_node_diff_path = [x - y for x, y in zip(new_first_node_scores_path, first_node_scores_path)]
    second_node_diff_path = [x - y for x, y in zip(new_second_node_scores_path, second_node_scores_path)]

    # scores of first and second node for old k_clique graph
    first_node_scores_clique = [k_clique_score[k][new_edge[0]] for k in k_clique_score.keys()]
    second_node_scores_clique = [k_clique_score[k][new_edge[1]] for k in k_clique_score.keys()]
    # scores of first and second node for new k_clique graph
    new_first_node_scores_clique = [new_k_clique_score[k][new_edge[0]] for k in new_k_clique_score.keys()]
    new_second_node_scores_clique = [new_k_clique_score[k][new_edge[1]] for k in new_k_clique_score.keys()]
    # score differences for k_clique graph
    first_node_diff_clique = [x - y for x, y in zip(new_first_node_scores_clique, first_node_scores_clique)]
    second_node_diff_clique = [x - y for x, y in zip(new_second_node_scores_clique, second_node_scores_clique)]

    plots = False
    if plots:
        # graph_handling.show(path, new_edge[0], new_edge[1], k_path_edges)
        # graph_handling.show(clique, new_edge[0], new_edge[1], k_clique_edges)
        graph_handling.show_diff(first_node_diff_path, 'Node ' + str(new_edge[0]) + ' in k_path', new_edge[0])
        graph_handling.show_diff(second_node_diff_path, 'Node ' + str(new_edge[1]) + ' in k_path', new_edge[1])
        graph_handling.show_diff(first_node_diff_clique, 'Node ' + str(new_edge[0]) + ' in k_clique', new_edge[0])
        graph_handling.show_diff(second_node_diff_clique, 'Node ' + str(new_edge[1]) + ' in k_clique', new_edge[1])


