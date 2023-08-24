import random

def SimulateCascade(G, S):
    # Copy seed set
    activated = S.copy()
    activated_next = S.copy()

    # Perform independent cascade simulation
    while activated_next:
        newly_activated = set()
        for v in activated_next:
            for u in G.neighbors(v):
                if u not in activated and random.random() < G.edges[v, u]['prob']:
                    newly_activated.add(u)
        activated |= newly_activated
        activated_next = newly_activated
    # print('simulate complete')
    return len(activated)