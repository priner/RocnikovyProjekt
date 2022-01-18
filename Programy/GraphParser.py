from sage.all import *

def parse(fileName):
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

		i = i + numberOfVertices + 2
		if(numberOfGraph == numberOfGraphs):
			break	

	return graphs

def parseG6(fileName):
	file = open(fileName, "r")
	graphs = [ Graph(line) for line in file.readlines()]
	file.close()
	return graphs
