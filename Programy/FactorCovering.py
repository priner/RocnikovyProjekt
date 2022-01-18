from subprocess import *
from sage.all import *
import sys
import GraphParser
import tempfile
import time
import os


def testGraph(graph, factors):

    infile, infilename = tempfile.mkstemp(suffix="cnf")

    edgeVars = [[[] for v in graph.vertices() ] for u in graph.vertices()]

    varsCounter = 1
    varToGraph = {}

    for i in range(len(graph)):
        for j in range(len(graph)):
            if graph.has_edge(i,j):
                edgeVars[i][j] = list(range(factors))
            for k in range(len(edgeVars[i][j])):
                edgeVars[i][j][k] = varsCounter
                varToGraph[varsCounter] = [i,j,k]
                varsCounter = varsCounter+1

    conditions = symetryConditions(edgeVars, graph) \
        + atLeastOneFactorPerEdge(edgeVars, graph) \
        + atLeastOneEdgePerFactor(edgeVars, graph, factors) \
        + atMostOneEdgePerFactor(edgeVars, graph, factors)

    s = "p cnf " + str(varsCounter) + " " + str(len(conditions)) + "\n"
    s = s + "\n".join([" ".join([str(x) for x in c]) + " 0" for c in conditions])

    s = s.encode()
    os.write(infile, s)
    os.close(infile)

    process = Popen(["./lingeling", infilename], stdout=PIPE)
    (output, err) = process.communicate()
    exit_code = process.wait()

    os.remove(infilename)

    splitted_lines = output.splitlines()
    for line in splitted_lines:
        line = line.decode()
        if line == "s UNSATISFIABLE":
            return False

    return True


def symetryConditions(edgeVars, graph):
    res = []
    for i in range(len(graph)):
        for j in range(len(graph)):
            for k in range(len(edgeVars[i][j])):
                res.append([-edgeVars[i][j][k],edgeVars[j][i][k]])
                res.append([edgeVars[i][j][k],-edgeVars[j][i][k]])

    return res

def atLeastOneFactorPerEdge(edgeVars, graph):
    res = []
    for i in range(len(graph)):
        for j in range(len(graph)):
            if len(edgeVars[i][j]) != 0:
                res.append(edgeVars[i][j])

    return res

def atMostOneEdgePerFactor(edgeVars, graph, factors):
    res = []
    for i in range(len(graph)):
        for j in range(len(graph)):
            for k in range(len(graph)):
                if j != k and len(edgeVars[i][j]) != 0 and len(edgeVars[i][k]) != 0 :
                    for f in range(factors):
                        res.append([-edgeVars[i][j][f], -edgeVars[i][k][f]])

    return res

def atLeastOneEdgePerFactor(edgeVars, graph, factors):
    res = []
    for i in range(len(graph)):
        for f in range(factors):
            neighbors = [x for x in range(len(graph)) if len(edgeVars[i][x]) != 0]
            res.append([edgeVars[i][n][f] for n in neighbors ])

    return res



def main():
    graphsPath = ""
    factors = 3

    for s in sys.argv:
        ss = s.split("=")
        if ss[0] == "-graph":
            graphsPath = ss[1]
        if ss[0] == "-factors":
            factors = int(ss[1])

    if graphsPath == "":
        print("you need to provide path to graph file in parameter 'graph'")
        exit(1)

    graphs = [Graph(g) for g in GraphParser.parse(graphsPath)]

    for i in range(len(graphs)):
        print("graph", i+1)
        g = graphs[i]
        testResult = testGraph(g, factors)
        if testResult == False:
            print("without covering")
        else:
            print("covering exists")


if __name__ == '__main__':
    main()
