import networkx as nx

def LabelPropagation(G):
    communities = list(nx.algorithms.community.label_propagation.label_propagation_communities(G))
    print('communities detection complete')
    #print(communities)
    return [set(c) for c in communities]