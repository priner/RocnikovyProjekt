import sys
sys.path.append('../')
sys.path.append('../../')

from subprocess import *
import itertools
import GraphParser
import toBr
import GeneratorHelper
from sage.all import *


def readCubicGraphs(fileName):
	file = open(fileName, "r")
	graphs = [Graph(line) for line in file.readlines()]
	return graphs

def existsInPrevious(graphs, g):
	for i in range(len(graphs)-1 , -1 , -1 ):
		if g.is_isomorphic(graphs[i]):
			return True
	return False

def getGirthAndCC(fileName):
	bashCommand = "../cc/cesky 3 " + fileName
	process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
	output, error = process.communicate()
	girth = -1
	cc = -1
	for line in output.split("\n"):
		words = line.split()
		if len(words) > 1 and words[0] == "girth:":
			girth = int(words[1])
		if len(words) > 1 and words[0] == "cc:":
			cc = int(words[1])
	return (girth,cc)



def join(g, component, x1,x2,y1,y2,oldx,oldy):

	gg1 = g.copy()
	gg2 = component.graph.copy()


	gg1.relabel(dict([(x, (0, x)) for x in gg1.vertices()]))
	gg2.relabel(dict([(x, (1, x)) for x in gg2.vertices()]))

	gg = gg1.union(gg2)

	gg.add_edge([(0,x1), (1, component.graph.neighbors(component.connectors[0][0])[0])])
	gg.add_edge([(0,x2), (1, component.graph.neighbors(component.connectors[0][1])[0])])
	gg.add_edge([(0,y1), (1, component.graph.neighbors(component.connectors[1][0])[0])])
	gg.add_edge([(0,y2), (1, component.graph.neighbors(component.connectors[1][1])[0])])


	gg.delete_vertex((0,oldx))
	gg.delete_vertex((0,oldy))
	gg.delete_vertex((1, component.connectors[0][0]))
	gg.delete_vertex((1, component.connectors[0][1]))
	gg.delete_vertex((1, component.connectors[1][0]))
	gg.delete_vertex((1, component.connectors[1][1]))

	if not gg.is_regular():
		print(x1,x2,y1,y2,oldx, oldy)

	gg.relabel()
	return gg

def substituteEdge(g1, component, x, y):
	n1 = g1.neighbors(x)
	n2 = g1.neighbors(y)
	n1.remove(y)
	n2.remove(x)
	graphs = [
		join(g1, component, n1[0], n1[1], n2[0], n2[1],x,y),
		join(g1, component, n1[0], n1[1], n2[1], n2[0],x,y),
		join(g1, component, n1[1], n1[0], n2[0], n2[1],x,y),
		join(g1, component, n1[1], n1[0], n2[1], n2[0],x,y)
	]
	return graphs

def substituteEachEdge(g1, component):
	graphs = []
	for d in g1.edges():
		for g in substituteEdge(g1, component, d[0], d[1]):
			common = False
			for gg in graphs:
				if g.is_isomorphic(gg):
					common = True
					break
			if not common:
				graphs.append(g)
	return graphs


def main():
    graphsPath = ""
    outputFile = ""
    halinPath = "halinDipol"

    for s in sys.argv:
        ss = s.split("=")
        if ss[0] == "-graph":
            graphsPath = ss[1]
        if ss[0] == "-outputFile":
            outputFile = ss[1]
        if ss[0] == "-halin":
            halinPath = ss[1]

    if graphsPath == "":
        print("you need to provide path to graph file in parameter 'graph'")
        exit(1)

    if outputFile == "":
        print("you need to provide output file in parameter 'outputFile'")
        exit(1)

    graphs = [Graph(g) for g in GraphParser.parse(graphsPath)]

    generated = []

    halin = GeneratorHelper.parseComponents(halinPath)[0]

    for i in range(len(graphs)):
        print("graph", i+1)
        g = graphs[i]
        for newGraph in substituteEachEdge(g, halin):
            if not existsInPrevious(generated, newGraph):
                generated.append(newGraph)

    toBr.printToFile(generated, outputFile)

    print("generated", len(generated), "graphs")


if __name__ == '__main__':
    main()
