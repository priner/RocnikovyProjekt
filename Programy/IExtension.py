import GraphParser
import FactorCovering
import sys
from sage.all import *


def test(graph):
	res = []

	for e in graph.edges():
		for f in graph.edges():
			if e == f or e > f or len({e[0],e[1],f[0],f[1]}) != 4:
				continue
			g = graph.copy()
			u = len(g)
			v = u + 1
			g.add_vertices([u,v])
			g.add_edge([u,v])
			g.add_edge([u,e[0]])
			g.add_edge([u,e[1]])
			g.add_edge([v,f[0]])
			g.add_edge([v,f[1]])
			g.delete_edges([e,f])

			if FactorCovering.testGraph(g, 4) == False:
				res.append([[e[0],e[1]],[f[0],f[1]]])

	if len(res) == 0:
		return False
	else:
		return res

def main():
    printSolution = False
    graphsPath = ""

    for s in sys.argv:
        ss = s.split("=")
        if ss[0] == "-graph":
            graphsPath = ss[1]
        if ss[0] == "-printSolution":
            printSolution = True

    if graphsPath == "":
        print("you need to provide path to graph file in parameter 'graph'")
        exit(1)

    graphs = [Graph(g) for g in GraphParser.parse(graphsPath)]

    for i in range(len(graphs)):
        print("graph", i+1)
        g = graphs[i]
        testResult = test(g)
        if testResult == False:
            print("without I extension")
        else:
            print("I extension exists")
            if printSolution:
                print(testResult)

if __name__ == '__main__':
    main()
