import asyncio
from sage.all import Graph
from SatSolver import solveSATparallel
from Steiner import cycleType, toCanonicalCycle, colors, colorNames, symetryConditions, atLeastOnePerEdge, atMostOnePerEdge, blockConditions
import sys
from GraphParser import parseComponent, endpointVerticies
import GraphParser
from Precomputed import all5ColoringsZeroSum
from pathlib import Path

async def testCycle(graph, cycle):

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

    outputs = await solveSATparallel(inputs)

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

def listCycles(g):
    res = set()
    for v1 in g.vertices():
        for v2 in g.neighbors(v1):
            for v3 in g.neighbors(v2):
                for v4 in g.neighbors(v3):
                    for v5 in g.neighbors(v4):
                        if v1 in g.neighbors(v5):
                            if len({v1,v2,v3,v4,v5}) == 5:
                                res.add(normalizeCycle([v1,v2,v3,v4,v5]))
    return sorted(res)

def removeCycle(g, cycle):
    for i in range(len(cycle)):
        assert cycle[i] in g.neighbors(cycle[i-1])
    for i in range(len(cycle)):
        g.delete_edge(cycle[i], cycle[i-1])

def normalizeCycle(original_array):
    candidates = []
    candidates += [original_array[i:] + original_array[:i] for i in range(len(original_array))]
    reversed_array = list(reversed(original_array))
    candidates += [reversed_array[i:] + reversed_array[:i] for i in range(len(reversed_array))]
    return tuple(min(candidates))


async def main():
    cycle = None
    graphsPath = sys.argv[1]

    if len(sys.argv) >= 3:
        cycle = tuple(map(int,sys.argv[2].split(",")))

    graphs = [Graph(g) for g in GraphParser.parse(graphsPath)]
    assert len(graphs) == 1
    assert cycle == None or len(cycle) == 5

    #components = [(Graph(g), c) for g, c in parseComponent(graphsPath)]

    g = graphs[0]
    if cycle != None:
        removeCycle(g, cycle)
        testResult = await testCycle(g, cycle)

        with open(graphsPath+'-'+sys.argv[2], 'w') as outfile:
            summary = set()
            for coloring in testResult:
                print(*map(lambda c: colorNames[c].rjust(2), coloring), end=4*" ", file=outfile)
                print(cycleType[coloring][0].ljust(20), cycleType[coloring][1], file=outfile)
                summary.add(cycleType[coloring])

            print(file=outfile)
            for ct in sorted(summary):
                print(ct[0].ljust(20), ct[1], file=outfile)
    else:
        for cycle in listCycles(g):
            print(*cycle, sep=",")




        # TODO TREBA VACSIU RYCHLOST !!!!!!

if __name__ == '__main__':
    asyncio.run(main())
