import networkx as nx
import matplotlib.pyplot as plt
import random
from smartNode import SmartNode

def GetNeighbors(G, node):
    return set(G.adj._atlas.get(node).keys())

def PrintAllNodeInfo(G):
    for smartNode in G.nodes._nodes.values():
        print(smartNode)



n = 20 #number of nodes
SmartNode.SetNumberOfNodes(numNodes=n)
p = 0.25 #E-R edge prob
R = 3 #Number of w-swappiong rounds
xR = 5 #Number of E-swapping rounds

# Generate a random graph (Erdős-Rényi model)
G = nx.gnp_random_graph(n, 0.35)
SmartNode.SetGraph(graph=G)
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
    smartNode = SmartNode(id=node, hasFood=hasFood, neighborSet=neighbors)
    G.nodes._nodes.update({node: smartNode})

PrintAllNodeInfo(G)

pos = nx.spring_layout(G) #Could be used to display w vectors or perhaps the computed value of E slightly offset at each node
plt.figure(num='Random Forager Graph')
nx.draw(G, pos = pos, node_color=color_map, with_labels=True)
plt.show()

#Complete message passing rounds
for i in range(R):
    for node in G.nodes:
        smartNode = G.nodes._nodes.get(node)
        smartNode.pullWVecsFromNeighbors()
    for node in G.nodes:
        smartNode = G.nodes._nodes.get(node)
        smartNode.mergeWVecs()

    print("\nw() Swapping Round " + str(i+1) + " of " + str(R) + ':')
    PrintAllNodeInfo(G)

#Now get everybody to compute their Es
for node in G.nodes:
    smartNode = G.nodes._nodes.get(node)
    smartNode.computeE()

print("\nAfter local computation of E: ")
PrintAllNodeInfo(G)

#Complete E-swapping rounds
for i in range(xR):
    for node in G.nodes:
        smartNode = G.nodes._nodes.get(node)
        smartNode.pullEFromNeighbors()
    for node in G.nodes:
        smartNode = G.nodes._nodes.get(node)
        smartNode.updateE()

    print("\nE Swapping Round " + str(i + 1) + " of " + str(xR) + ':')
    PrintAllNodeInfo(G)





