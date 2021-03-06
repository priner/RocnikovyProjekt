import asyncio
from sage.all import Graph
from SatSolver import solveSAT
from Steiner import connectorType, toCanonical, isZeroSum, colors, colorNames, symetryConditions, atLeastOnePerEdge, atMostOnePerEdge, blockConditions, allColorings
import sys
from GraphParser import parseComponent, residualVerticies, endpointVerticies

async def testComponent(graph, connectors):

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

    endpoints = list(sum(connectors,())) + residualVerticies(graph, connectors)

    validColorings = []
    for coloring in filter(isZeroSum, allColorings(len(endpoints))):
        conditions = commonConditions + endpointConditions(edgeVars, graph, endpoints, coloring)

        s = "p cnf " + str(varsCounter) + " " + str(len(conditions)) + "\n"
        s = s + "\n".join([" ".join([str(x) for x in c]) + " 0" for c in conditions])

        output = await solveSAT(s)

        splitted_lines = output.splitlines()
        for line in splitted_lines:
            line = line.decode()
            if line == "s SATISFIABLE":
                validColorings.append(coloring)

    return validColorings

def endpointConditions(edgeVars, graph, endpoints, coloring):
    res = []

    for v, c in zip(endpoints,coloring):
        res.append([edgeVars[v][graph.neighbors(v)[0]][c]])

    return res


async def main():
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
        graph, connectors = components[i]
        testResult = await testComponent(graph, connectors)

        summary = set()
        for coloring in testResult:
            connectorColors = [(coloring[2*i], coloring[2*i+1]) for i in range(len(connectors))]
            print(*map(lambda c: colorNames[c].rjust(2), coloring[0:2*len(connectors)]), end=4*" ")
            connectorTypes = tuple(map(lambda cc: connectorType[toCanonical(cc)], connectorColors))
            print(*connectorTypes)
            summary.add(connectorTypes)

        print()
        for ct in sorted(summary):
            print(*ct)

if __name__ == '__main__':
    asyncio.run(main())
