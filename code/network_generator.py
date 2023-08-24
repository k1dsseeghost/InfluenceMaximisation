import networkx as nx
import random
import matplotlib.pyplot as plt

class NetworkGenerator:
    def __init__(self, num_communities, nodes_per_community, p_intra, p_inter):
        self.num_communities = num_communities
        self.nodes_per_community = nodes_per_community
        self.p_intra = p_intra
        self.p_inter = p_inter
        self.graph = nx.Graph()
        self.communities = []

    def generate_community(self, n, p):
        """Generate a single community using Erdős-Rényi model."""
        return nx.erdos_renyi_graph(n, p)

    def connect_communities(self):
        """Randomly connect nodes from different communities."""
        for i in range(len(self.communities) - 1):
            for j in range(i + 1, len(self.communities)):
                source = random.choice(list(self.communities[i].nodes))
                target = random.choice(list(self.communities[j].nodes))
                self.graph.add_edge(source, target)

    def generate_network(self):
        """Generate a network with ground-truth communities."""
        for i in range(self.num_communities):
            community = self.generate_community(self.nodes_per_community, self.p_intra)
            self.graph = nx.disjoint_union(self.graph, community)
            self.communities.append(community)

        self.connect_communities()

    def add_probability_to_edges(self, prob):
        """Add a probability attribute to each edge in the graph."""
        for u, v in self.graph.edges():
            self.graph[u][v]['prob'] = prob

    def visualize(self, G):
        """Visualize the generated graph."""
        nx.draw(G, with_labels=True)
        plt.show()

if __name__ == "__main__":
    # Parameters
    num_communities = 5
    nodes_per_community = 1000
    p_intra = 0.8  # High probability for intra-community edges
    p_inter = 0.05  # Low probability for inter-community edges

    generator = NetworkGenerator(num_communities, nodes_per_community, p_intra, p_inter)
    G, communities = generator.generate_network()
    generator.visualize(G)
