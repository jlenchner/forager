

class AdjMatrix:
    MATRIX_A_NBRS = [[1, 4,15],
                     [0,2,7],
                     [1, 3, 6],
                     [2,4,9],
                     [0,3,5],
                     [4,6,14],
                     [2,5,10],
                     [1,8,13],
                     [7,9,10],
                     [3,8,11],
                     [6,8,12],
                     [9,12,13],
                     [10,11,15],
                     [7,11,14],
                     [5,13,15],
                     [0,12,14]
                     ]

    MATRIX_A_TITLE = "A. Minimized Average Betweenness"

    MATRIX_B_NBRS = [[1, 5,15],
                     [0,2,6],
                     [1,3,8],
                     [2,7,9],
                     [6,7,15],
                     [0,9,14],
                     [1,4,12],
                     [3,4,8],
                     [2,7,11],
                     [3,5,10],
                     [9,11,12],
                     [8,10,13],
                     [6,10,13],
                     [11,12,14 ],
                     [5,13,15],
                     [0,4,14]
                     ]

    MATRIX_B_TITLE = "B. Minimized Average Clustering"

    MATRIX_C_NBRS = [[4,5,15],
                     [2,4,7],
                     [1,3,6],
                     [2,7,8],
                     [0,1,15],
                     [0,6,14],
                     [2,5,11],
                     [1,3,9],
                     [3,10,13],
                     [7,10,12],
                     [8,9,11],
                     [6,10,13],
                     [9,13,14],
                     [8,11,12],
                     [5,12,15],
                     [0,4,14]
                     ]

    MATRIX_C_TITLE = "C. Maximized Maximum Closeness"

    MATRIX_D_NBRS = [[1, 3, 15],
                     [0, 2, 3],
                     [1, 4, 5],
                     [0, 1, 15],
                     [2, 6, 13],
                     [2, 7, 12],
                     [4, 7, 8],
                     [5, 6, 14],
                     [6, 9, 10],
                     [8, 10, 11],
                     [8, 9, 11],
                     [9, 10, 12],
                     [5, 11, 13],
                     [4, 12, 14],
                     [7, 13, 15],
                     [0, 3, 14]
                     ]

    MATRIX_D_TITLE = "D. Maximized Variance in Constraint"

    MATRIX_E_NBRS = [[1,2,3],
                     [0,2,15],
                     [0,1,3],
                     [0,2,4],
                     [3,5,6],
                     [4,6,7],
                     [4,5,7],
                     [5,6,8],
                     [7,9,10],
                     [8,10,11],
                     [8,9,11],
                     [9,10,12],
                     [11,13,14],
                     [12,14,15],
                     [12,13,15],
                     [1,13,14]
                     ]


    MATRIX_E_TITLE = "E. Maximized Average Clustering"

    MATRIX_F_NBRS = [[1, 2, 3],
                     [0, 2, 3],
                     [0, 1, 4],
                     [0, 1, 4],
                     [2, 3, 10],
                     [6, 9, 10],
                     [5, 7, 8],
                     [6, 8, 9],
                     [6, 7, 9],
                     [5, 7, 8],
                     [4, 5, 11],
                     [10, 12, 15],
                     [11, 13, 14],
                     [12, 14, 15],
                     [12, 13, 15],
                     [11, 13, 14]
                     ]

    MATRIX_F_TITLE = "F. Maximized Maximum Betweenness"


    MATRIX_G_NBRS = [[1, 2, 15],
                     [0, 2, 4],
                     [0, 1, 3],
                     [2, 4, 5],
                     [1, 3, 5],
                     [3, 4, 6],
                     [5, 7, 8],
                     [6, 9, 10],
                     [6, 9, 10],
                     [7, 8, 10],
                     [7, 8, 9],
                     [12, 13, 14],
                     [11, 13, 14],
                     [11, 12, 15],
                     [11, 12, 15],
                     [0, 13, 14]
                     ]

    MATRIX_G_TITLE = "G. Minimized Maximum Closeness"

    MATRIX_H_NBRS = [[1, 2, 3],
                     [0, 2, 3],
                     [0, 1, 4],
                     [0, 1, 4],
                     [2, 3, 5],
                     [4, 6, 7],
                     [5, 7, 8],
                     [5, 6, 8],
                     [6, 7, 9],
                     [8, 10, 11],
                     [9, 11, 15],
                     [9, 10, 12],
                     [11, 13, 14],
                     [12, 14, 15],
                     [12, 13, 15],
                     [10, 13, 14]
                     ]

    MATRIX_H_TITLE = "H. Maximized Average Betweenness"

    def __init__(self, matrix = [], nbrList = [], title="Multiple Foragers"):
        if matrix != []:
            self._matrix = matrix
        else:
            self._matrix = AdjMatrix.AdjMatrixFromNbrList(nbrList)
        self._title = title

    def getAdjacentNodes(self, i):
        adjacencies = []
        row = self._matrix[i]
        for j in range(len(row)):
            if row[j] == 1:
                adjacencies.append(j)

        return adjacencies

    @classmethod
    def AdjMatrixFromNbrList(cls, nbrList):
        adjMatrix = []
        num_nodes = len(nbrList)
        for i in range(num_nodes):
            nbrs = nbrList[i]
            adjRow = [0] * num_nodes
            for nbr in nbrs:
                adjRow[nbr] = 1
            print(adjRow)
            adjMatrix.append(adjRow)

        return adjMatrix


    def numNodes(self):
        return len(self._matrix)

