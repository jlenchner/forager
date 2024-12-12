import networkx as nx
import matplotlib.pyplot as plt
import random

# Generate a random graph (Erdős-Rényi model)
G = nx.gnp_random_graph(20, 0.25)  # 10 nodes, probability of edge creation = 0.3
PROB_HAS_FOOD = 0.5
# Draw the graph
color_map = []
for node in G.nodes:
    r = random.random()
    if r < PROB_HAS_FOOD:
        color_map.append('green')
    else:
        color_map.append('red')

pos = nx.spring_layout(G) #Going to offset these to display w vectors and perhaps the computed value of E at each node
plt.figure(num='Random Forager Graph')
nx.draw(G, pos = pos, node_color=color_map, with_labels=True)
plt.show()