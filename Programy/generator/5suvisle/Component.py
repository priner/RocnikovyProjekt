from subprocess import *
from sage.all import *



# 5 suvisle komponenty

class Component:
	def __init__(self, graph, connectors, top):
		self.graph = graph
		self.connectors = connectors
		self.top = top

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

def joinTwoComponents(g1, g2, c1, c2, p):
	oldC1 = g1.connectors[(c1+1)%2]
	oldC2 = g2.connectors[(c2+1)%2]

	c1 = g1.connectors[c1]
	c2 = g2.connectors[c2]

	if p:
		c2 = [c2[1], c2[0]]
	gg1 = g1.graph.copy()
	gg1.relabel(dict([(x, (1, x)) for x in g1.graph.vertices()]))
	
	gg2 = g2.graph.copy()
	gg2.relabel(dict([(x, (2, x)) for x in g2.graph.vertices()]))

	g = gg1.union(gg2)
	g.add_edge((1,g1.graph.neighbors(c1[0])[0]), (2,g2.graph.neighbors(c2[0])[0]))
	g.add_edge((1,g1.graph.neighbors(c1[1])[0]), (2,g2.graph.neighbors(c2[1])[0]))

	g.delete_vertex((1,c1[0]))
	g.delete_vertex((1,c1[1]))
	g.delete_vertex((2,c2[0]))
	g.delete_vertex((2,c2[1]))

	v1 = g.add_vertex()
	v2 = g.add_vertex()

	g.add_edge((1,g1.graph.neighbors(g1.top)[0]), v1)
	g.add_edge((2,g2.graph.neighbors(g2.top)[0]), v1)
	g.add_edge(v1, v2)

	g.delete_vertex((1, g1.top))
	g.delete_vertex((2, g2.top))


	relabelMap = g.relabel(return_map = True)

	return Component(g, [ [relabelMap[(1,x)] for x in oldC1], [relabelMap[(2,x)] for x in oldC2]], relabelMap[v2] )


def joinTwoComponentsAllPossibleWays(g1, g2):
	all = [
		joinTwoComponents(g1,g2,0,0,False),
		joinTwoComponents(g1,g2,0,0,True),
		joinTwoComponents(g1,g2,0,1,False),
		joinTwoComponents(g1,g2,0,1,True)
		]

	res = []
	for i in range(4):
		iso = False
		for j in range(i):
			if all[i].graph.is_isomorphic(all[j].graph):
				iso = True
				break
		circ = 100000

		for c in all[i].graph.cycle_basis():
			circ = min(circ, len(c))

		if not iso and circ > 4:
			res.append(all[i])

	return res


def contain(components, component):
	for c in components:
		if c.graph.is_isomorphic(component.graph):
			return True

	return False

def generateAllCombinations(components, maximalLevel, maxVertices):
	byLevels = [[]]
	res = []

	for c in components:
		if not contain(res, c) and len(c.graph) <= maxVertices:
			res.append(c)
			byLevels[0].append(c)	


	for l in range(maximalLevel):
		byLevels.append([])
		for c1 in byLevels[l]:
			if len(c1.graph) <= maxVertices:
				for c2 in components:
					for nc in (joinTwoComponentsAllPossibleWays(c1, c2) + joinTwoComponentsAllPossibleWays(c2, c1)):
						if len(nc.graph) <= maxVertices and not contain(res, nc):
							byLevels[l+1].append(nc)
							res.append(nc)

	

	return res

def printToFile(cs, fileName):
	f = open(fileName,"w+")


	f.write(str(len(cs)) + "\n")
	for i in range(0, len(cs)):
		c = cs[i]
		f.write(str(i+1) + "\n")
		f.write(str(len(c.graph.vertices())) + "\n")
		for j in range(0, len(c.graph.vertices())):
			f.write(" ".join([str(x) for x in c.graph.neighbors(j)]) + "\n")
		f.write(str(len(c.connectors)) + "\n")
		for con in c.connectors:
			f.write(" ".join([str(x) for x in con]) + "\n")

	f.close()



