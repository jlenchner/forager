import math
import random
import numpy as np

class SmartNode:
    UNDEFINED = -999
    SLOTS = 4 #this is the number that determines m/l; should be a power of 2
    ALPHA = UNDEFINED
    G = None  #the graph
    n = 16 #default #number of nodes; should always get over-written
    k = 7  #number of states
    l = k + math.ceil(math.log2(math.log2(n)))
    #l = 6 #For consistency with Markus
    m = SLOTS * l  # to make m/l a power of two and a reasonable value

    def __init__(self, id, hasFood=False, neighborSet={}):
        self._id = id
        self._hasFood = hasFood
        self._neighborSet = neighborSet
        self._w = [SmartNode.UNDEFINED] * SmartNode.SLOTS
        self._pulledWs = None  #pulled W-vecs from neighbors. Used internally.
        if hasFood:
            self._j = random.randint(0, SmartNode.SLOTS-1)
            self._x = np.random.geometric(0.5)
            self._w[self._j] = min(self._x, pow(2, SmartNode.l))
        else:
            self._j = SmartNode.UNDEFINED
            self._x = SmartNode.UNDEFINED

        self._Z = SmartNode.UNDEFINED
        self._E = SmartNode.UNDEFINED
        self._pulledEs = None #pulled Es from neighbors. Used internally.
        self._hasMostFoodInRadiusR = True

    def __str__(self):
        bad_w_count = self._w.count(SmartNode.UNDEFINED)
        s = "Node id: " + str(self._id) + \
            ", hasFood: " + str(self._hasFood) + \
            ", neighborSet: " + str(self._neighborSet) + \
            ", w: " + str(self._w ) + \
            ", E: " + str(self._E) + \
            ", _hasMostFoodInRadiusR: " + str(self._hasMostFoodInRadiusR) + \
            ", bad_w_count: " + str(bad_w_count)

        return s

    @classmethod
    def SetGraph(cls, graph):
        SmartNode.G = graph

    def computeZ(self):
        z_inv = 0
        for i in range(SmartNode.SLOTS):
            if self._w[i] == SmartNode.UNDEFINED:
                #continue  #experimental
                self._Z = 0
                return 0
            z_inv += pow(2, -self._w[i])

        self._Z = 1.0/z_inv
        return self._Z

    def getSmartNodesWithinGivenDistance(self, d):
        smartNbhood = {self}
        for i in range(d):
            nbhood = set()
            for node in smartNbhood:
                nbhood = nbhood | node._neighborSet
            for node in nbhood:
                smartNbhood.add(SmartNode.GetSmartNode(node))

        return smartNbhood

    def getFoodAmountWithinGivenDistance(self, d):
        distanceDNodes = self.getSmartNodesWithinGivenDistance(d)
        amountOfFood = 0
        for node in distanceDNodes:
            if node._hasFood:
                amountOfFood += 1

        return amountOfFood

    @classmethod
    def ComputeAlpha(cls):
        STEP_SIZE = 0.0001  #this and the next were derived experimentally to guarantee near convergence
        INFINITY = 1000
        num_integral = 0
        u = 0
        while u < INFINITY:
            num_integral += pow(math.log2((2+u)/(1+u)), cls.SLOTS) * STEP_SIZE
            u += STEP_SIZE

        cls.ALPHA = 1.0/(cls.SLOTS * num_integral)
        #print("ALPHA = " + str(round(cls.ALPHA, 3)))
        return cls.ALPHA

    def computeE(self):
        if self._Z == SmartNode.UNDEFINED:
            self.computeZ()
        if SmartNode.ALPHA == SmartNode.UNDEFINED:
            SmartNode.ComputeAlpha()

        self._E = SmartNode.ALPHA*SmartNode.SLOTS*SmartNode.SLOTS*self._Z
        return self._E

    @classmethod
    def GetSmartNode(cls, node):
        return SmartNode.G.nodes._nodes.get(node)

    @classmethod
    def SetNumberOfNodes(cls, numNodes):
        SmartNode.n = numNodes

    def pullWVecsFromNeighbors(self):
        self._pulledWs = []
        for nbr_node in self._neighborSet:
            smartNbr = SmartNode.GetSmartNode(nbr_node)
            self._pulledWs.append(smartNbr._w)

    def mergeWVecs(self):
        for pulledW in self._pulledWs:
            self.mergeWVec((pulledW))

    def mergeWVec(self, w_vec):
        for i in range(len(self._w)):
            if w_vec[i] > self._w[i]:
                self._w[i] = w_vec[i]

    def pullEFromNeighbors(self):
        self._pulledEs = []
        for nbr_node in self._neighborSet:
            smartNbr = SmartNode.GetSmartNode(nbr_node)
            self._pulledEs.append(smartNbr._E)

    def updateE(self):
        for i in range(len(self._pulledEs)):
            if self._pulledEs[i] > self._E:
                self._E = self._pulledEs[i]
                self._hasMostFoodInRadiusR = False





