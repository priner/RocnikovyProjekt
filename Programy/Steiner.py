import itertools

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

fromName = {v: k for k, v in colorNames.items()}
fromValue = {v: k for k, v in colorValues.items()}

_allVertexMappings = list(map(lambda pm: {str(i+1):pm[i] for i in range(4)}, itertools.permutations('1234')))

def _mapPoint(vertex_mapping, original_array):
    new_array = []

    for point in original_array:
        newPoint = ""
        for v in point:
            newPoint += vertex_mapping[v]

        new_array.append(''.join(sorted(newPoint)))

    return tuple(new_array)

def _toCanonical(original_array):
    return min(map(lambda vm: _mapPoint(vm, original_array), _allVertexMappings))

def toCanonical(original_array):
    return list(map(lambda n: fromName[n], _toCanonical(list(map(lambda c: colorNames[c], original_array)))))

def _allColorings(length):
    return sorted(set(map(_toCanonical, itertools.product([colorNames[c] for c in range(10)], repeat=length))))

def allColorings(length):
    res = []
    for coloring in _allColorings(length):
        res.append(list(map(lambda n: fromName[n], coloring)))

    return res

def isZeroSum(array):
    s = 0;
    for color in array:
        s ^= colorValues[color]
    return s == 0

# Common conditions for SAT

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
        if len(nieghbors) != 3:
            continue
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
