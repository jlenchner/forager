import sys
import math
import numpy as np

import networkx as nx
import matplotlib.pyplot as plt
import random
from smartNode import SmartNode
from adjMatrix import AdjMatrix
random.seed(4)

def GetNeighbors(G, node):
    return set(G.adj._atlas.get(node).keys())

def PrintAllNodeInfo(G):
    for smartNode in G.nodes._nodes.values():
        print(smartNode)

def PrintFirstNodeInfo(G):
    first_node = list(G.nodes._nodes.values())[0]
    print(first_node)

def AddEdges(G, adjMatrix):
    for node in G.nodes:
        nbrNodes = adjMatrix.getAdjacentNodes(node)
        for nbr in nbrNodes:
            G.add_edge(node, nbr)

def GetFoodLabelDict(G, radius):
    foodLabelDict = {}
    for smartNode in G.nodes._nodes.values():
        lbl = "F=" + str(smartNode.getFoodAmountWithinGivenDistance(radius))
        foodLabelDict[smartNode._id] =  lbl
        print(str(smartNode._id) + ": " + lbl)

    return foodLabelDict

def RunMultipleSims(num_sims):
    cum_RMSE = 0
    cum_MAE = 0
    cum_MRE = 0
    cum_AveFood = 0
    for i in range(num_sims):
        G = nx.Graph()
        for j in range(n):
            G.add_node(j, attr=None)
        AddEdges(G, adjMatrix)

        SmartNode.SetGraph(graph=G)
        PROB_HAS_FOOD = 0.5

        for node in G.nodes:
            r = random.random()
            hasFood = False
            if r < PROB_HAS_FOOD:
                hasFood = True
            neighbors = GetNeighbors(G, node)
            smartNode = SmartNode(id=node, hasFood=hasFood, neighborSet=neighbors)
            G.nodes._nodes.update({node: smartNode})

        for j in range(R):
            for node in G.nodes:
                smartNode = G.nodes._nodes.get(node)
                smartNode.pullWVecsFromNeighbors()
            for node in G.nodes:
                smartNode = G.nodes._nodes.get(node)
                smartNode.mergeWVecs()

        cumSquareError = 0
        cumAbsError = 0
        cumRelError = 0
        cumFood = 0
        for node in G.nodes:
            smartNode = G.nodes._nodes.get(node)
            E = smartNode.computeE()
            #print("Node " + str(smartNode._id) + ": E = " + str(round(E, 3)))
            F = smartNode.getFoodAmountWithinGivenDistance(R)
            cumSquareError += (E - F) * (E - F)
            cumAbsError += abs(E - F)
            if F != 0:
                cumRelError += (abs(E - F)/F)
            cumFood += F
        RMSE = pow(cumSquareError / n, 0.5)
        cum_RMSE += RMSE
        MAE = cumAbsError / n
        cum_MAE += MAE
        MRE = cumRelError / n
        cum_MRE += MRE
        AveFood = cumFood / n
        cum_AveFood += AveFood
        print("Sim #" + str(i+1))
        print("RMSE = " + str(round(RMSE, 3)))
        print("MAE = " + str(round(MAE, 3)))
        print("MRE = " + str(round(MRE, 3)))
        print("Average Food per Node = " + str(round(AveFood, 3)) + "\n")

    mean_RMSE = cum_RMSE/num_sims
    mean_MAE = cum_MAE/num_sims
    mean_MRE = cum_MRE / num_sims
    mean_Food = cum_AveFood / num_sims

    print("\n\nMean RMSE over all sims = " + str(round(mean_RMSE, 3)))
    print("Mean MAE over all sims = " + str(round(mean_MAE, 3)))
    print("Mean MRE over all sims = " + str(round(mean_MRE, 3)))
    print("Mean Food within Radius " + str(R) + " over all sims = " + str(round(mean_Food, 3)))

# counts = [0] * 16
# for i in range(1000):
#     i = np.random.geometric(0.5)
#     counts[i] += 1
#     print(str(i))
#
# print("\n\n")
# for i in range(16):
#     print(str(i) + ": " + str(counts[i]/1000))
#
# exit(0)

OUTPUT_TO_FILE = True

orig_stdout = None
f_out = None
if OUTPUT_TO_FILE:
    orig_stdout = sys.stdout
    f_out = open('output.txt', 'w')
    sys.stdout = f_out

adjMatrix = AdjMatrix(matrix=[], nbrList=AdjMatrix.MATRIX_H_NBRS, title=AdjMatrix.MATRIX_H_TITLE)
n = adjMatrix.numNodes()

SmartNode.SetNumberOfNodes(numNodes=n)

#alpha = SmartNode.ComputeAlpha()   #for debugging purposes

DISPLAY_GRAPH = (n <= 400)   #Otherwise too many nodes; display will error out!

R = 3 #Number of w-swappiong rounds
xR = 0 #4 #Number of E-swapping rounds

RunMultipleSims(num_sims=100000)
exit(0)

G = nx.Graph()
for i in range(n):
    G.add_node(i,attr=None)
AddEdges(G, adjMatrix)

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
#PrintFirstNodeInfo(G)
if DISPLAY_GRAPH:
    pos = nx.spring_layout(G) #Could be used to display w vectors or perhaps the computed value of E slightly offset at each node
    plt.figure(num=adjMatrix._title)
    nx.draw(G, pos=pos, node_color=color_map, with_labels=True)
    foodLabelDict = GetFoodLabelDict(G, R)
    #nx.draw_networkx_labels(G, pos=nx.spring_layout(G), labels=foodLabelDict)
    plt.show()

#Complete message passing rounds
print("Before Swapping:")
PrintAllNodeInfo(G)
for i in range(R):
    for node in G.nodes:
        smartNode = G.nodes._nodes.get(node)
        smartNode.pullWVecsFromNeighbors()
    for node in G.nodes:
        smartNode = G.nodes._nodes.get(node)
        smartNode.mergeWVecs()

    print("\nw() Swapping Round " + str(i+1) + " of " + str(R) + ':')
    PrintAllNodeInfo(G)
    #PrintFirstNodeInfo(G)

#Now get everybody to compute their Es and compute the RMSE, MAE
cumSquareError = 0
cumAbsError = 0
cumRelError = 0
cumFood = 0
rel_n = 0
for node in G.nodes:
    smartNode = G.nodes._nodes.get(node)
    E = smartNode.computeE()
    print("Node " + str(smartNode._id) + ": E = " + str(round(E,3)))
    F = smartNode.getFoodAmountWithinGivenDistance(R)
    cumSquareError += (E-F)*(E-F)
    cumAbsError += abs(E-F)
    if F != 0:
        cumRelError += (abs(E - F) / F)
        rel_n += 1
    elif E - F == 0:
        rel_n += 1
    cumFood += F

RMSE = pow(cumSquareError / n, 0.5)
MAE = cumAbsError / n
MRE = cumRelError / rel_n
AveFood = cumFood / n
print("RMSE = " + str(round(RMSE,3)))
print("MAE = " + str(round(MAE,3)))
print("MRE = " + str(round(MRE,3)))
print("Average Food in Radius " + str(R) + " per Node = " + str(round(AveFood, 3)))

#print("\nAfter local computation of E: ")
#PrintAllNodeInfo(G)
#PrintFirstNodeInfo(G)


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



