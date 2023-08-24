import queue
import random
import time

import networkx as nx
import network_generator
from networkx.generators.community import LFR_benchmark_graph

from CELF import CELF
from LPA_CELF import community_based_seed_selection
from independt_cascade import SimulateCascade

graph = nx.Graph()
with open('../../Influence_maximisation/datasets/.txt', 'r') as file:
    for line in file:
        parts = line.strip().split()  # Split the line into node names
        if len(parts) == 2:
            node1, node2 = parts
            graph.add_edge(node1, node2, prob=0.1)  # Add the edge to the graph

# Function to choose different apporaches to rank the communties
# def community_ranker(communities,ranker):
#     if ranker= o='size':
#         return communities
#     # if ranker == 'density':
#
#
# def find_community(node, communities):
#     """Find which community a node belongs to."""
#     for community in communities:
#         if node in community:
#             return community
#     return None


# def is_promising(local_spread, communities, best_thread, threshold=0.1):
#     """Check if the local spread is promising based on a threshold."""
#     if best_thread == 0:
#         return True
#     else:
#         return local_spread >= best_thread / len(communities)








# Function to create a toy dataset
# def create_toy_network():
#     G = nx.Graph()
#     edges = [
#         ("A", "B", 0.1),
#         ("A", "C", 0.3),
#         ("B", "C", 0.2),
#         ("B", "D", 0.7),
#         ("C", "D", 0.4),
#         ("C", "E", 0.8),
#         ("D", "E", 0.6),
#         ("D", "F", 0.9),
#         ("E", "F", 0.5),
#         ("F", "A", 0.1),
#         ("E", "A", 0.2),
#         ("F", "C", 0.1),
#     ]
#     G.add_weighted_edges_from(edges, weight='prob')
#     return G


# Creating the toy network
# G = create_toy_network()

# Setting K as 2 for the example
# K = 2

# Example usage:
# seed_nodes = community_based_seed_selection(network, communities, K)


# Read and parse the .txt file


start_time = time.time()
print('start LPA_CELF')
# Running LPA_CELF algorithm on the toy network
S = community_based_seed_selection(graph,20)
end_time = time.time()
elapsed_time = end_time - start_time
print(f"The function LPA_CELF took {elapsed_time} seconds to complete.")

start_time = time.time()
print('start CELF')
S2 = CELF(graph,20)
end_time = time.time()
elapsed_time = end_time - start_time
print(f"The function CELF took {elapsed_time} seconds to complete.")

selected_nodes = random.sample(graph.nodes(), 3)
seed = set()
for node in selected_nodes:
    seed.add(node)
print('random',SimulateCascade(graph,seed))

# S = nx.algorithms.community.label_propagation_communities(graph)
# num_communities = len(list(S))
#print('seed node set from LPA_CELF:',S)
print('seed node set from CELF')


