import subprocess
from sage.all import *

# 5 suvisle komponenty

class Component:
	def __init__(self, graph, connectors, top):
		self.graph = graph
		self.connectors = connectors
		self.top = top

	def copy(self):
		return Component(self.graph.copy(), [[y for y in x] for x in self.connectors], self.top)

def parseComponents(fileName):
	file = open(fileName, "r")
	graphs = []
	i = 1

	lines = [ line for line in file.readlines() if line[0] != '{']
	numberOfGraphs = int(lines[0])	
	while True:
		numberOfGraph = int(lines[i]) 
		numberOfVertices = int(lines[i+1])

		graphs.append({})
		for j in range(0, numberOfVertices):
			graphs[numberOfGraph-1][j] = [int(x) for x in lines[i+2+j].strip().split(" ")]

		numberOfConnectors = int(lines[i+numberOfVertices+2])

		connectors = [[int(x) for x in lines[i+3+numberOfVertices+j].strip().split(" ")] for j in range(numberOfConnectors)]
		connectorVertices = [v for c in connectors for v in c]

		g = Graph(graphs[-1])
		
		top = -1
		for v in g.vertices():
			if len(g.neighbors(v)) == 1 and v not in connectorVertices:
				top = v
				break


		i = i + numberOfVertices + 3 + numberOfConnectors
		graphs[-1] = Component(g, connectors, top)

		if(numberOfGraph == numberOfGraphs):
			break	

	return graphs


def readCubicGraphs(fileName):
	file = open(fileName, "r")
	graphs = [ Graph(line) for line in file.readlines()]
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
	
