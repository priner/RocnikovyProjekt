from sage.all import *

def parse(fileName):
	file = open(fileName, "r")
	graphs = []
	i = 1

	lines = [ line for line in file.readlines() if line[0] != '{']
	numberOfGraphs = int(lines[0])
	while True:
		graphNumber = int(lines[i])
		numberOfVertices = int(lines[i+1])

		graphs.append({})
		for j in range(0, numberOfVertices):
			graphs[graphNumber-1][j] = [int(x) for x in lines[i+2+j].strip().split(" ")]

		i = i + numberOfVertices + 2
		if(graphNumber == numberOfGraphs):
			break

	return graphs

def parseComponent(fileName):
	file = open(fileName, "r")
	components = []
	i = 1

	lines = [ line for line in file.readlines() if line[0] != '{']
	numberOfGraphs = int(lines[0])
	while True:
		graphNumber = int(lines[i])
		numberOfVertices = int(lines[i+1])

		graph = {}
		connectors = []
		for j in range(0, numberOfVertices):
			graph[j] = [int(x) for x in lines[i+2+j].strip().split(" ")]

		i = i + numberOfVertices + 2

		numberOfConnectors = int(lines[i])
		for j in range(0, numberOfConnectors):
			connectors.append(tuple(int(x) for x in lines[i+1+j].strip().split(" ")))

		i = i + numberOfConnectors + 1

		components.append((graph,connectors))

		if(graphNumber == numberOfGraphs):
			break

	return components

def parseG6(fileName):
	file = open(fileName, "r")
	graphs = [ Graph(line) for line in file.readlines()]
	file.close()
	return graphs
