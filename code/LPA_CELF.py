from independt_cascade import  SimulateCascade
from community_detection import LabelPropagation
from CELF import CELF
import queue


def community_based_seed_selection(network, K):
    communities = LabelPropagation(network)
    M = len(communities)
    print('Number of communities',M)
    # 1. Compute Influence Spread for Each Community
    print('Compute Influence Spread for Each Community')
    community_influence = {}
    for i, community in enumerate(communities):
        print(f'size of community {i} is {len(community)}')
        community_influence[i] = [SimulateCascade(network.subgraph(community), {node}) for node in community]
        community_influence[i].sort(reverse=True)  # Sort in descending order

    # 2. Dynamic Programming to Select Communities and Node Counts
    # DP[i][j] influence spread that mine the jth node in the first i communities
    print('Dynamic Programming to Select Communities and Node Counts')
    R = [[0 for _ in range(K + 1)] for _ in range(M + 1)]
    kth_node_chosen_from = []
    node_to_community = {}
    for k in range(0, K):
        I = set()
        for m in range(0, M):
            community = communities[m]
            origin_spread = SimulateCascade(network.subgraph(communities[m]), I)
            marginal = max([SimulateCascade(network.subgraph,I|{community[v]}) - origin_spread \
                            for v in enumerate(community)])
            R[m][k] = max(R[m-1][k], R[M][k-1])
            if R[m-1][k] >= R[M][k-1]:
                kth_node_chosen_from[m][k] = kth_node_chosen_from[m-1][k]
            else:
                kth_node_chosen_from[m][k] = m

        node_to_community[k] = kth_node_chosen_from[M][k]

    community_to_nodes = {}
    for node, community in node_to_community.items():
        if community not in community_to_nodes:
            community_to_nodes[community] = []
        community_to_nodes[community].append(node)

    # 创建一个字典来保存每个社区及其对应的节点数
    community_to_count = {community: len(nodes) for community, nodes in community_to_nodes.items()}

    print('CELF Optimization Within Selected Communities')
    # 3. CELF Optimization Within Selected Communities
    seed_nodes = set()
    for community_index, node_count in community_to_count:
        community_network = network.subgraph(
            communities[community_index])  # Assuming 'network' supports subgraph extraction

        print('node count is ',node_count)
        seeds_for_community = CELF(community_network, node_count)
        seed_nodes.update(seeds_for_community)

        print("size of community",community_index,'is',len(communities[community_index]))
        print(f"Influence spread after CELF for community {community_index}: {SimulateCascade(network, seeds_for_community)}")

    total_spread = SimulateCascade(network, seed_nodes)
    print(f"Total influence spread for all selected seed nodes: {total_spread}")

    # 4. Return the final set of K seed nodes
    return seed_nodes