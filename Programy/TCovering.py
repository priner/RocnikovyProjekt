from subprocess import *
from sage.all import *
import sys
import GraphParser
import tempfile
import time
import os


colors = 10
configuration = [
    [0,1,2],
    [0,3,7],
    [0,4,9],
    [2,5,7],
    [2,6,9],
    [7,8,9]]


colorValues = {
    0: 7,
    1: 12,
    2: 11,
    3: 9,
    4: 10,
    5: 5,
    6: 6,
    7: 14,
    8: 3,
    9: 13
}

def testGraph(graph):

    infile, infilename = tempfile.mkstemp(suffix="cnf")

    edgeVars = [[[] for v in graph.vertices() ] for u in graph.vertices()]

    varsCounter = 1
    varToGraph = {}

    for i in range(len(graph)):
        for j in range(len(graph)):
            if graph.has_edge(i,j):
                edgeVars[i][j] = list(range(colors))
            for k in range(len(edgeVars[i][j])):
                edgeVars[i][j][k] = varsCounter
                varToGraph[varsCounter] = [i,j,k]
                varsCounter = varsCounter+1

    conditions = symetryConditions(edgeVars, graph, configuration) \
        + atLeastOnePerEdge(edgeVars, graph, configuration) \
        + atMostOnePerEdge(edgeVars, graph, configuration) \
        + additionalConditions(edgeVars, graph, configuration) \
       + blockConditions(edgeVars, graph, configuration) 

    s = "p cnf " + str(varsCounter) + " " + str(len(conditions)) + "\n"
    s = s + "\n".join([" ".join([str(x) for x in c]) + " 0" for c in conditions])

    s = s.encode()
    os.write(infile, s)
    os.close(infile)

    # with open(infilename, 'w') as f:
    #     f.write(s)
    # os.close(infile)

    process = Popen(["./lingeling", infilename], stdout=PIPE)
    (output, err) = process.communicate()
    exit_code = process.wait()

    os.remove(infilename)

    coloring = {}
    splitted_lines = output.splitlines()
    # print(splitted_lines)
    for line in splitted_lines:
        line = line.decode()
        if line == "s UNSATISFIABLE":
            return False

        if len(line) > 0 and line[0] == 'v':
            varz = line.split(" ")[1:]
            for v in varz:
                v = v.strip()
                if v[0] != '-' and v[0] != '0':
                    mem = varToGraph[int(v)]
                #    if mem[0] > mem[1]:
                #        mem[0],mem[1] = mem[1],mem[0]
                    coloring[(mem[0], mem[1])] = mem[2]
    return coloring

# first edge has only 2 posibilities
def additionalConditions(edgeVars, graph, configuration):
    for i in range(len(graph)):
        for j in range(len(graph)):
            if len(edgeVars[i][j]) != 0:
                return [[edgeVars[i][j][0], edgeVars[i][j][1]]]

def symetryConditions(edgeVars, graph, configuration):
    res = []
    for i in range(len(graph)):
        for j in range(len(graph)):
            for k in range(len(edgeVars[i][j])):
                res.append([-edgeVars[i][j][k],edgeVars[j][i][k]])
                res.append([edgeVars[i][j][k],-edgeVars[j][i][k]])

    return res

def atLeastOnePerEdge(edgeVars, graph, configuration):
    res = []
    for i in range(len(graph)):
        for j in range(len(graph)):
            if len(edgeVars[i][j]) != 0:
                res.append(edgeVars[i][j])

    return res

def atMostOnePerEdge(edgeVars, graph, configuration):
    res = []
    for i in range(len(graph)):
        for j in range(len(graph)):
            for k1 in edgeVars[i][j]:
                for k2 in edgeVars[i][j]:
                    if k1 != k2:
                        res.append([-k1, -k2])

    return res

def blockConditions(edgeVars, graph, configuration):
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

def main():
    printColoring = False
    graphsPath = ""

    for s in sys.argv:
        ss = s.split("=")
        if ss[0] == "-graph":
            graphsPath = ss[1]
        if ss[0] == "-printColoring":
            printColoring = True

    if graphsPath == "":
        print("you need to provide path to graph file in parameter 'graph'")
        exit(1)

    graphs = [Graph(g) for g in GraphParser.parse(graphsPath)]

    for i in range(len(graphs)):
        print("graph", i+1)
        g = graphs[i]
        testResult = testGraph(g)
        if testResult == False:
            print("without coloring")
        else:
            print("coloring exists")
            if printColoring:
                for u in range(len(g)):
                    for v in g.neighbors(u):
                        print(u, v, "->")
                        c = colorValues[testResult[(u,v)]]
                        print("".join([ str(int((c&(2**i)) != 0)) for i in range(3,-1,-1)]))

if __name__ == '__main__':
    main()
