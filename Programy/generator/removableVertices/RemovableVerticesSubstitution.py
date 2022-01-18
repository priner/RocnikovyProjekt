import sys
sys.path.append('../')
sys.path.append('../../')

import itertools
import GraphParser
import toBr
import GeneratorHelper as GH

halin = Graph(GraphParser.parse("halinDipol")[0])
halin.relabel(dict([(x, (2, x)) for x in halin.vertices()]))

baseGraphName = ""
cubicGraphSizes = []
verticesForSubstitution = []
outputFileName = ""

for s in sys.argv:
	ss = s.split("=")
	if ss[0] == "graph":
		baseGraphName = ss[1]
	if ss[0] == "sizes":
		cubicGraphSizes = [ int(x) for x in ss[1].split(",")]
	if ss[0] == "vertices":
		verticesForSubstitution = [ int(x) for x in ss[1].split(",")]
	if ss[0] == "output":
		outputFileName = ss[1]

if baseGraphName == "":
	print "parameter \"graph\" not provided"
	exit(1)
if cubicGraphSizes == []:
	print "parameter \"sizes\" not provided"
	exit(1)
if verticesForSubstitution == []:
	print "parameter \"vertices\" not provided"
	exit(1)
if outputFileName == "":
	print "parameter \"output\" not provided"
	exit(1)


def substituteWithPermutations(baseGraph, cub, vertexNumberInBase, vertexNumberInCub ):

	g1 = baseGraph.copy();
	g1.delete_vertex(vertexNumberInBase)
	g1.relabel(dict([(x, (0, x)) for x in g1.vertices()]))

	g2 = cub.copy()
	g2.delete_vertex(vertexNumberInCub)
	g2.relabel(dict([(x, (1, x)) for x in g2.vertices()]))

	graphs = []

	connector = baseGraph.neighbors(vertexNumberInBase)

	for i in range(3):
		for ns in itertools.permutations(cub.neighbors(vertexNumberInCub)):
			g = g1.union(g2).union(halin)
			g.add_edge((0, connector[1]), (1, ns[1]))
			g.add_edge((0, connector[2]), (1, ns[2]))

			con1 = g1.neighbors((0, connector[0]))
			con2 = g2.neighbors((1, ns[0]))
			g.add_edge(con1[0], (2, 0))
			g.add_edge(con1[1], (2, 2))
			g.add_edge(con2[0], (2, 22))
			g.add_edge(con2[1], (2, 24))

			g.delete_vertex((0, connector[0]))
			g.delete_vertex((1, ns[0]))

			g.relabel()
			graphs.append(g)

		connector = [connector[-1]] + connector[:-1]

	return graphs



def substituteAll(baseGraph, vertices, cubs):
	graphs = []

	for cub in cubs:
		
		for vertexNumber in vertices:
			for v in cub.vertices():
				gs = substituteWithPermutations(baseGraph, cub, vertexNumber, v)

				for g in gs:
					toBr.printToFile([g], "./tmp/tmp1")
					(girth, cc) = GH.getGirthAndCC("./tmp/tmp1")

					if not GH.existsInPrevious(graphs, g) and girth >= 5 and cc >= 4:
						graphs.append(g)
						if len(graphs) % 10 == 0:
						 	toBr.printToFile(graphs, outputFileName + "." + str(len(g.vertices())))

	return graphs



for i in cubicGraphSizes:
	print "cub size ", i
	cubs = GH.readCubicGraphs("./cubicGraphs/cub" + str(i) + "-gir5.g6")

	baseGraph = Graph(GraphParser.parse(baseGraphName)[0])

	generated = substituteAll(baseGraph, verticesForSubstitution, cubs)
	print "generated", len(generated), "graphs"

	toBr.printToFile(generated, outputFileName + "." + str(i+26+32-2) )

