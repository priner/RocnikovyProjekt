from sage.all import Graph
from SatSolver import solveSAT
from Steiner import colors, configuration, colorNames, symetryConditions, atLeastOnePerEdge, atMostOnePerEdge, blockConditions
import sys
import GraphParser

def testGraph(graph):

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

    conditions = symetryConditions(edgeVars, graph) \
        + atLeastOnePerEdge(edgeVars, graph) \
        + atMostOnePerEdge(edgeVars, graph) \
        + additionalConditions(edgeVars, graph) \
       + blockConditions(edgeVars, graph)

    s = "p cnf " + str(varsCounter) + " " + str(len(conditions)) + "\n"
    s = s + "\n".join([" ".join([str(x) for x in c]) + " 0" for c in conditions])

    output = solveSAT(s)

    coloring = {}
    splitted_lines = output.splitlines()
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
def additionalConditions(edgeVars, graph):
    for i in range(len(graph)):
        for j in range(len(graph)):
            if len(edgeVars[i][j]) != 0:
                return [[edgeVars[i][j][0], edgeVars[i][j][1]]]


def main():
    printColoring = False
    graphsPath = ""

    for s in sys.argv:
        ss = s.split("=", maxsplit=1)
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
                        print(u, v, "->", colorNames[testResult[(u,v)]])

if __name__ == '__main__':
    main()
