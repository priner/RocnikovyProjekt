from subprocess import *
from sage.all import *
import sys
import GraphParser
import tempfile
import time
import os
import FactorCovering



def testGraph(g):

    wrongPairs = []

    for u in g.vertices():
        for v in g.neighbors(u):
            if u > v:
                continue
            if u != v:
                gg = g.copy()
                gg.delete_vertex(u)
                gg.delete_vertex(v)
                gg.relabel()
                if testGraph3Coloring(gg):
                    wrongPairs.append([u,v])

    if len(wrongPairs) == 0:
        return True
    else:
        return wrongPairs


def testGraph3Coloring(graph):

    infile, infilename = tempfile.mkstemp(suffix="cnf")
        
    edgeVars = [[[] for v in graph.vertices() ] for u in graph.vertices()]

    varsCounter = 1
    varToGraph = {}

    for i in range(len(graph)):
        for j in range(len(graph)):
            if graph.has_edge(i,j):
                edgeVars[i][j] = range(3)
            for k in range(len(edgeVars[i][j])):
                edgeVars[i][j][k] = varsCounter;
                varToGraph[varsCounter] = [i,j,k]
                varsCounter = varsCounter+1

    conditions = symetryConditions(edgeVars, graph) \
        + atLeastOneColorPerEdge(edgeVars, graph) \
        + atMostOneColorPerEdge(edgeVars, graph) \
        + atMostOneEdgePerColor(edgeVars, graph) 

    s = "p cnf " + str(varsCounter) + " " + str(len(conditions)) + "\n"
    s = s + "\n".join([" ".join([str(x) for x in c]) + " 0" for c in conditions])

    os.write(infile, s)
    os.close(infile)

    process = Popen(["./lingeling", infilename], stdout=PIPE)
    (output, err) = process.communicate()
    exit_code = process.wait()

    os.remove(infilename)

    for line in str(output).split("\n"):
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

def atLeastOneColorPerEdge(edgeVars, graph):
    res = []
    for i in range(len(graph)):
        for j in range(len(graph)):
            if len(edgeVars[i][j]) != 0:
                res.append(edgeVars[i][j])

    return res

def atMostOneColorPerEdge(edgeVars, graph):
    res = []
    for i in range(len(graph)):
        for j in range(len(graph)):
            if len(edgeVars[i][j]) != 0:
                for a in edgeVars[i][j]:
                    for b in edgeVars[i][j]:
                        if a != b:
                            res.append([-a,-b])

    return res

def atMostOneEdgePerColor(edgeVars, graph):
    res = []
    for i in range(len(graph)):
        for j in range(len(graph)):
            for k in range(len(graph)):
                if j != k and len(edgeVars[i][j]) != 0 and len(edgeVars[i][k]) != 0 :
                    for f in range(3):
                        res.append([-edgeVars[i][j][f], -edgeVars[i][k][f]])

    return res


def main():
    graphsPath = ""
    printWrong = 0

    for s in sys.argv:
        ss = s.split("=")
        if ss[0] == "-graph":
            graphsPath = ss[1]
        if ss[0] == "-printWrong":
            printWrong = True
            
    if graphsPath == "":
        print "you need to provide path to graph file in parameter 'graph'"
        exit(1)

    graphs = [Graph(g) for g in GraphParser.parse(graphsPath)]

    for i in range(len(graphs)):
        print "graph", i+1
        g = graphs[i]
        testResult = testGraph(g)
        if testResult == True:
            print "strong"
        else:
            print "not strong"
            if printWrong:
                print testResult


if __name__ == '__main__':
    main()

