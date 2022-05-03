colors = 10
configuration = [
    [0,1,2],
    [0,3,7],
    [0,4,9],
    [2,5,7],
    [2,6,9],
    [7,8,9],
]


colorNames = {
    0: "1",
    1: "12",
    2: "2",
    3: "13",
    4: "14",
    5: "23",
    6: "24",
    7: "3",
    8: "34",
    9: "4"
}

colorValues = {
    0: 0b0111,
    1: 0b1100,
    2: 0b1011,
    3: 0b1001,
    4: 0b1010,
    5: 0b0101,
    6: 0b0110,
    7: 0b1110,
    8: 0b0011,
    9: 0b1101,
}


def symetryConditions(edgeVars, graph):
    res = []
    for i in range(len(graph)):
        for j in range(len(graph)):
            for k in range(len(edgeVars[i][j])):
                res.append([-edgeVars[i][j][k],edgeVars[j][i][k]])
                res.append([edgeVars[i][j][k],-edgeVars[j][i][k]])

    return res

def atLeastOnePerEdge(edgeVars, graph):
    res = []
    for i in range(len(graph)):
        for j in range(len(graph)):
            if len(edgeVars[i][j]) != 0:
                res.append(edgeVars[i][j])

    return res

def atMostOnePerEdge(edgeVars, graph):
    res = []
    for i in range(len(graph)):
        for j in range(len(graph)):
            for k1 in edgeVars[i][j]:
                for k2 in edgeVars[i][j]:
                    if k1 != k2:
                        res.append([-k1, -k2])

    return res

def blockConditions(edgeVars, graph):
    res = []
    for row in edgeVars:
        nieghbors = [i for i in range(len(row)) if len(row[i]) > 0 ]
        for column1 in nieghbors:
            for column2 in nieghbors:
                if column1 != column2:
                    for color1 in range(len(row[column1])):
                        nextColors = []
                        for block in configuration:
                            if color1 in block:
                                for color2 in block:
                                    if color1 != color2:
                                        nextColors.append(row[column2][color2])
                        res.append([-row[column1][color1]] + nextColors)

        for column1 in nieghbors:
            for column2 in nieghbors:
                for column3 in nieghbors:
                    if len({column1, column2, column3}) == 3:
                        for block in configuration:
                            for color1 in block:
                                for color2 in block:
                                    for color3 in block:
                                        if len({color1, color2, color3}) == 3:
                                           res.append([-row[column1][color1], -row[column2][color2], row[column3][color3]])

    return res
