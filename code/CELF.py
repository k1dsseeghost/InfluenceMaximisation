from independt_cascade import SimulateCascade
import queue
import random

def MIG(G, S, v, num_simulations=100):
    original_spread = sum(SimulateCascade(G, S) for _ in range(num_simulations)) / num_simulations
    new_spread = sum(SimulateCascade(G, S | {v}) for _ in range(num_simulations)) / num_simulations
    return new_spread - original_spread

def CELF(G,K):
    S = set()  # Seed set
    Q = queue.PriorityQueue()  # Priority queue for nodes and their MIG

    # Initialization: compute initial MIG for each node in each community

    for node in G:
        initial_mig = MIG(G, S, node)
        Q.put((-initial_mig, node))  # Use negative MIG to make PriorityQueue a max heap
    best_spread = 0  # Best influence spread
    #print('size of Q', Q.qsize())
    # Iterative Seed Selection
    max_seed_size = K
    while not Q.empty() and len(S) < max_seed_size:
        mig, node = Q.get()  # Dequeue the node with the highest MIG
        mig = -mig  # Change MIG back to positive
        # Simulate influence spread with current seed set + new node
        spread = SimulateCascade(G, S | {node})
        updated_mig = spread - best_spread  # Updated MIG
        # If updated MIG is positive, add node to seed set and update best spread
        if Q.empty() or updated_mig > -Q.queue[0][0]:
            S.add(node)
            best_spread = spread
        else:
            Q.put((-updated_mig, node))
    #print('best spread', best_spread)
    return S
