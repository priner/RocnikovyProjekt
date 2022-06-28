from sage.all import Graph
from SatSolver import solveSAT
import sys
import GraphParser


def testGraph(graph):
    maxCycles =  int(len(graph) * 0.6) + 1

    edgeVars = [[[] for v in graph.vertices() ] for u in graph.vertices()]

    varsCounter = 0
    varToGraph = {}

    for i in range(len(graph)):
        for j in range(len(graph)):
            if graph.has_edge(i,j):
                edgeVars[i][j] = list(range(maxCycles))
            for k in range(len(edgeVars[i][j])):
                varsCounter = varsCounter+1
                edgeVars[i][j][k] = varsCounter
                varToGraph[varsCounter] = [i,j,k]

    conditions = symetryConditions(edgeVars, graph) \
        + atLeastOneCyclePerEdge(edgeVars, graph) \
        + twoNeighborEdge(edgeVars, graph, maxCycles) \
        + atMostTwoNeighborEdges(edgeVars, graph, maxCycles) \
        + baseOneFactor(edgeVars, graph) \
        + atLeastTwoCyclesPerEdge(edgeVars, graph, maxCycles) \
        + atMostTwoCyclesPerEdge(edgeVars, graph, maxCycles)

    s = "p cnf " + str(varsCounter) + " " + str(len(conditions)) + "\n"
    s = s + "\n".join([" ".join([str(x) for x in c]) + " 0" for c in conditions])

    print("vars", varsCounter)
    print("clausses", len(conditions))

    output = solveSAT(s)

    cycles = {}

    for line in output.splitlines():
        line = line.decode()
        if line == "s UNSATISFIABLE":
            return False
        if len(line) > 0 and line[0] == 'v':
            varz = line.split(" ")[1:]
            for v in varz:
                v = v.strip()
                if v[0] != '-' and v[0] != '0':
                    mem = varToGraph[int(v)]
                    if mem[2] not in cycles:
                        cycles[mem[2]] = [mem[:2]]
                    else:
                        cycles[mem[2]].append(mem[:2])

    result = []
    for i in range(maxCycles):
        if i in cycles:
            result.append(cycles[i])

    return result

def symetryConditions(edgeVars, graph):
    res = []
    for i in range(len(graph)):
        for j in range(len(graph)):
            for k in range(len(edgeVars[i][j])):
                res.append([-edgeVars[i][j][k],edgeVars[j][i][k]])
                res.append([edgeVars[i][j][k],-edgeVars[j][i][k]])

    return res

def atLeastOneCyclePerEdge(edgeVars, graph):
    res = []
    for i in range(len(graph)):
        for j in range(len(graph)):
            if len(edgeVars[i][j]) != 0:
                res.append(edgeVars[i][j])

    return res

def twoNeighborEdge(edgeVars, graph, maxCycles):
    res = []
    for i in range(len(graph)):
        n = graph.neighbors(i)
        for a in n:
            for b in n:
                if a != b:
                    for c in n:
                        if a != c and b != c:
                            for d in range(maxCycles):
                                res.append([-edgeVars[i][a][d],edgeVars[i][b][d],edgeVars[i][c][d]])

    return res

def atMostTwoNeighborEdges(edgeVars, graph, maxCycles):
    res = []
    for i in range(len(graph)):
        for d in range(maxCycles):
            res.append([-edgeVars[i][x][d] for x in graph.neighbors(i) ])

    return res

def baseOneFactor(edgeVars, graph):
    res = []
    for i in range(len(graph)):
        res.append([edgeVars[i][x][0] for x in graph.neighbors(i) ])

    return res

def atLeastTwoCyclesPerEdge(edgeVars, graph, maxCycles):
    res = []
    for i in range(len(graph)):
        for j in graph.neighbors(i):
            for c in range(maxCycles):
                res.append([x for x in edgeVars[i][j]])
                res[-1].remove(edgeVars[i][j][c])
                res[-1].append(-edgeVars[i][j][c])

    return res

def atMostTwoCyclesPerEdge(edgeVars, graph, maxCycles):
    res = []
    for i in range(len(graph)):
        for j in graph.neighbors(i):
            for c1 in range(maxCycles):
                for c2 in range(c1+1, maxCycles):
                    for c3 in range(c2+1, maxCycles):
                        res.append([-edgeVars[i][j][c1], -edgeVars[i][j][c2], -edgeVars[i][j][c3]])

    return res


def main():
    graphsPath = ""
    printCycles = 0

    for s in sys.argv:
        ss = s.split("=", maxsplit=1)
        if ss[0] == "-graph":
            graphsPath = ss[1]
        if ss[0] == "-printCycles":
            printCycles = True

    if graphsPath == "":
        print("you need to provide path to graph file in parameter 'graph'")
        exit(1)

    graphs = [Graph(g) for g in GraphParser.parse(graphsPath)]

    for i in range(len(graphs)):
        print("graph", i+1)
        g = graphs[i]
        testResult = testGraph(g)
        if testResult == False:
            print("without CDC 2-factor")
        else:
            print("CDC 2-factor exists")
            if printCycles:
                for i in range(len(testResult)):
                    #print ",".join(str(x) for x in testResult[i])
                    if i == 0:
                        print("2-factor")
                    if i == 1:
                        print("CDC supplement")
                    all = set([y[0] for y in [x for x in testResult[i]]])
                    while len(all) > 0:
                        first = list(all)[0]
                        cycle = [first]
                        all.remove(first)
                        while True:
                            next = -1
                            for x in testResult[i]:
                                if x[0] == cycle[-1] and x[1] in all:
                                    next = x[1]
                            if next == -1:
                                break
                            cycle.append(next)
                            all.remove(next)
                        print(cycle)





if __name__ == '__main__':
    main()
