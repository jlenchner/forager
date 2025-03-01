import sys
import math

import networkx as nx
import matplotlib.pyplot as plt
import random
from smartNode import SmartNode

def GetNeighbors(G, node):
    return set(G.adj._atlas.get(node).keys())

def PrintAllNodeInfo(G):
    for smartNode in G.nodes._nodes.values():
        print(smartNode)

def PrintFirstNodeInfo(G):
    first_node = list(G.nodes._nodes.values())[0]
    print(first_node)

def AddEdges(G, n_x, n_y):
    for node in G.nodes:
        nbrNodes = GetNeighboringNodes(node, n_x, n_y)
        for nbr in nbrNodes:
            G.add_edge(node, nbr)

def GetNodeNumberFromXY(x, y, n_x):
    return x*n_x + y

def GetXYFromNodeNumber(node, n_x, n_y):
    x = math.floor(node / n_x)
    y = node % n_y
    return x,y

def GetNeighboringNodes(node, n_x, n_y):
    x, y =  GetXYFromNodeNumber(node, n_x, n_y)

    left_x = x-1
    if left_x < 0:
        left_x = n_x - 1
    left_y = y
    left = GetNodeNumberFromXY(left_x, left_y, n_x)

    right_x = x+1
    if right_x == n_x:
        right_x = 0
    right_y = y
    right = GetNodeNumberFromXY(right_x, right_y, n_x)

    up_x = x
    up_y = y - 1
    if up_y < 0:
        up_y = n_y - 1
    up = GetNodeNumberFromXY(up_x, up_y, n_x)

    down_x = x
    down_y = y + 1
    if down_y ==  n_y:
        down_y = 0
    down = GetNodeNumberFromXY(down_x, down_y, n_x)

    return [right, down, left, up]

OUTPUT_TO_FILE = True

orig_stdout = None
f_out = None
if OUTPUT_TO_FILE:
    orig_stdout = sys.stdout
    f_out = open('output.txt', 'w')
    sys.stdout = f_out

#Define an n_x x n_y rectangular grid
n_x = 100
n_y = 100
n = n_x * n_y  #number of nodes
SmartNode.SetNumberOfNodes(numNodes=n)

#alpha = SmartNode.ComputeAlpha()   #for debugging purposes

DISPLAY_GRAPH = (n <= 400)   #Otherwise too many nodes; display will error out!

R = 6 #Number of w-swappiong rounds
xR = 5 #Number of E-swapping rounds

G = nx.Graph()
for i in range(n):
    G.add_node(i,attr=None)
AddEdges(G, n_x, n_y)

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

#PrintAllNodeInfo(G)
PrintFirstNodeInfo(G)

if DISPLAY_GRAPH:
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
    #PrintAllNodeInfo(G)
    PrintFirstNodeInfo(G)

#Now get everybody to compute their Es
for node in G.nodes:
    smartNode = G.nodes._nodes.get(node)
    smartNode.computeE()

print("\nAfter local computation of E: ")
#PrintAllNodeInfo(G)
PrintFirstNodeInfo(G)

#Complete E-swapping rounds
for i in range(xR):
    for node in G.nodes:
        smartNode = G.nodes._nodes.get(node)
        smartNode.pullEFromNeighbors()
    for node in G.nodes:
        smartNode = G.nodes._nodes.get(node)
        smartNode.updateE()

    print("\nE Swapping Round " + str(i + 1) + " of " + str(xR) + ':')
    #PrintAllNodeInfo(G)
    PrintFirstNodeInfo(G)

if OUTPUT_TO_FILE:
    sys.stdout = orig_stdout
    f_out.close()







