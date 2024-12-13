import networkx as nx
import matplotlib.pyplot as plt
import random
from smartNode import SmartNode

def GetNextPowerOfTwo(k):
    n = 1
    while True:
        if k <= n:
            return n
        else:
            n *= 2

def GetNeighbors(G, node):
    return set(G.adj._atlas.get(node).keys())

def PrintAllNodeInfo(G):
    for smartNode in G.nodes._nodes.values():
        print(smartNode)



n = 20 #number of nodes
SmartNode.SetNumberOfNodes(numNodes=n)
p = 0.25 #E-R edge prob

# Generate a random graph (Erdős-Rényi model)
G = nx.gnp_random_graph(n, 0.25)  # 10 nodes, probability of edge creation = 0.3
PROB_HAS_FOOD = 0.5
# Draw the graph
color_map = []
for node in G.nodes:
    r = random.random()
    hasFood = False
    if r < PROB_HAS_FOOD:
        hasFood = True
        color_map.append('green')
    else:
        color_map.append('red')
    neighbors = GetNeighbors(G, node)
    smartNode = SmartNode(node, hasFood=hasFood, neighborSet=neighbors)
    G.nodes._nodes.update({node: smartNode})

PrintAllNodeInfo(G)

pos = nx.spring_layout(G) #Could be used to display w vectors or perhaps the computed value of E slightly offset at each node
plt.figure(num='Random Forager Graph')
nx.draw(G, pos = pos, node_color=color_map, with_labels=True)
plt.show()


