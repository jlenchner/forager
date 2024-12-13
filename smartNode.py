import math
import random
import numpy as np

class SmartNode:
    UNDEFINED = -999
    SLOTS = 8 #this is the number that determines m/l; should be a power of 2
    n = 20 #default number
    k = 100  # number of states
    l = k + math.ceil(math.log2(math.log2(n)))
    m = SLOTS * l  # to make m/l a power of two and a reasonable

    def __init__(self, id, hasFood=False, neighborSet={}):
        self._id = id
        self._hasFood = hasFood
        self._neighborSet = neighborSet
        self._w = [0] * SmartNode.SLOTS
        if hasFood:
            self._j = random.randint(0, SmartNode.SLOTS-1)
            self._x = np.random.geometric(0.5)
            self._w[self._j] = min(self._x, pow(2, SmartNode.l))
        else:
            self._j = SmartNode.UNDEFINED
            self._x = SmartNode.UNDEFINED

        #TBD
        self._Z = SmartNode.UNDEFINED
        self._alpha = SmartNode.UNDEFINED
        self._E = SmartNode.UNDEFINED

    def __str__(self):
        s = "Node id: " + str(self._id) + \
            ", hasFood: " + str(self._hasFood) + \
            ", neighborSet: " + str(self._neighborSet) + \
            ", w:" + str(self._w )

        return s

    @classmethod
    def SetNumberOfNodes(cls, numNodes):
        SmartNode.n = numNodes



