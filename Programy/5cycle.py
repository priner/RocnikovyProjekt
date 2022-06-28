from sage.all import Graph
from SatSolver import solveSATparallel
from Steiner import cycleType, toCanonicalCycle, colors, colorNames, symetryConditions, atLeastOnePerEdge, atMostOnePerEdge, blockConditions
import sys
from GraphParser import parseComponent, endpointVerticies
from Precomputed import all5ColoringsZeroSum

def testCycle(graph, cycle):

    edgeVars = [[[] for v in graph.vertices() ] for u in graph.vertices()]

    varsCounter = 1
    varToGraph = {}

    for i in range(len(graph)):
        for j in range(len(graph)):
            if graph.has_edge(i,j):
                edgeVars[i][j] = list(range(colors))
            for k in range(len(edgeVars[i][j])):
                varsCounter = varsCounter+1
                edgeVars[i][j][k] = varsCounter
                varToGraph[varsCounter] = [i,j,k]

    commonConditions = symetryConditions(edgeVars, graph) \
        + atLeastOnePerEdge(edgeVars, graph) \
        + atMostOnePerEdge(edgeVars, graph) \
       + blockConditions(edgeVars, graph)

    endpoints = list(cycle)
    assert len(endpoints) == len(endpointVerticies(graph))
    assert len(endpoints) == 5

    colorings = all5ColoringsZeroSum

    inputs = []
    for coloring in colorings:
        conditions = commonConditions + endpointConditions(edgeVars, graph, endpoints, coloring)

        s = "p cnf " + str(varsCounter) + " " + str(len(conditions)) + "\n"
        s = s + "\n".join([" ".join([str(x) for x in c]) + " 0" for c in conditions])

        inputs.append(s)

    outputs = solveSATparallel(inputs)

    validColorings = []
    for output, coloring in zip(outputs, colorings):
        splitted_lines = output.splitlines()
        for line in splitted_lines:
            line = line.decode()
            if line == "s SATISFIABLE":
                validColorings.append(coloring)

    return sorted(set(map(toCanonicalCycle, validColorings)))

def endpointConditions(edgeVars, graph, endpoints, coloring):
    res = []

    for v, c in zip(endpoints,coloring):
        res.append([edgeVars[v][graph.neighbors(v)[0]][c]])

    return res


def main():
    graphsPath = ""

    for s in sys.argv:
        ss = s.split("=", maxsplit=1)
        if ss[0] == "-graph":
            graphsPath = ss[1]

    if graphsPath == "":
        print("you need to provide path to graph file in parameter 'graph'")
        exit(1)

    components = [(Graph(g), c) for g, c in parseComponent(graphsPath)]

    for i in range(len(components)):
        print("graph", i+1)
        graph, (cycle,) = components[i]
        testResult = testCycle(graph, cycle)

        # summary = set()
        for coloring in testResult:
            print(*map(lambda c: colorNames[c].rjust(2), coloring), end=4*" ")
            print(cycleType[coloring][0].ljust(20), cycleType[coloring][1])
        #     summary.add(connectorTypes)

        # print()
        # for ct in sorted(summary):
        #     print(*ct)


        # TODO TREBA VACSIU RYCHLOST !!!!!!

if __name__ == '__main__':
    main()
