import sys
sys.path.append('../')
sys.path.append('../../')

import itertools
import GraphParser
import toBr
import GeneratorHelper
from sage.all import *



def existsInPrevious(graphs, g):
	for i in range(len(graphs)-1 , -1 , -1 ):
		if g.is_isomorphic(graphs[i]):
			return True
	return False

def joinAllPossibleWays(comp, tops, old):
	if len(tops) == 0:
		if not existsInPrevious(old, comp):
			old.append(comp)

	if len(tops) >= 2:

		for i in range(0, len(tops)-1):
			g = comp.copy()
			v = g.add_vertex()
			t = g.add_vertex()
			g.add_edge([t, v])
			g.add_edge([v, comp.neighbors(tops[i])[0]])
			g.add_edge([v, comp.neighbors(tops[i+1])[0]])
			g.delete_vertex(tops[i])
			g.delete_vertex(tops[i+1])
			ts = [x for x in tops]
			ts[i] = t
			ts.remove(tops[i+1])
			old = joinAllPossibleWays(g, ts, old)

#		for i in range(0, len(tops)-1):
#			g = comp.copy()
#			g.add_edge([comp.neighbors(tops[i])[0], comp.neighbors(tops[i+1])[0]])
#			g.delete_vertex(tops[i])
#			g.delete_vertex(tops[i+1])
#			ts = [x for x in tops]
#			ts.remove(tops[i+1])
#			ts.remove(tops[i])
#			old = joinAllPossibleWays(g, ts, old)

	if len(tops) >= 3:
		for i in range(0, len(tops)-2):
			g = comp.copy()
			v = g.add_vertex()
			g.add_edge([v, comp.neighbors(tops[i])[0]])
			g.add_edge([v, comp.neighbors(tops[i+1])[0]])
			g.add_edge([v, comp.neighbors(tops[i+2])[0]])
			g.delete_vertex(tops[i])
			g.delete_vertex(tops[i+1])
			g.delete_vertex(tops[i+2])
			ts = [x for x in tops]
			ts.remove(tops[i+2])
			ts.remove(tops[i+1])
			ts.remove(tops[i])
			old = joinAllPossibleWays(g, ts, old)


	return old


def generate(component, level):
	input = [component.copy() for i in range(level) ]


	for i in range(level):
		input[i].graph.relabel(dict([(x, (i, x)) for x in input[i].graph.vertices()]))

	base = input[0].graph
	for i in range(1, level):
		base = base.union(input[i].graph)

	for i in range(level):
		i1 = i
		i2 = (i+1) % level
		if i2 < 0:
			i2 = i2 + level
		base.add_edge([(i1, component.graph.neighbors(component.connectors[1][0])[0]),
			(i2, component.graph.neighbors(component.connectors[0][0])[0])])

		base.add_edge([(i1, component.graph.neighbors(component.connectors[1][1])[0]),
			(i2, component.graph.neighbors(component.connectors[0][1])[0])])

		base.delete_vertex((i1, component.connectors[1][0]))
		base.delete_vertex((i1, component.connectors[1][1]))
		base.delete_vertex((i2, component.connectors[0][0]))
		base.delete_vertex((i2, component.connectors[0][1]))


	tops = [(i, component.top) for i in range(level)]

#	v = base.add_vertex()
#	t = base.add_vertex()
#	base.add_edge([t, v])
#	base.add_edge([v, base.neighbors(tops[0])[0]])
#	base.add_edge([v, base.neighbors(tops[1])[0]])
#	base.delete_vertex(tops[0])
#	base.delete_vertex(tops[1])
#	tops.remove(tops[0])
#	tops[0] = t

#	return base

	gs = joinAllPossibleWays(base, tops, [])

	for g in gs:
		g.relabel()

	return gs

def main():
    level = -1
    outputFile = ""

    for s in sys.argv:
        ss = s.split("=", maxsplit=1)
        if ss[0] == "-level":
            level = int(ss[1])
        if ss[0] == "-outputFile":
            outputFile = ss[1]

    if level == -1:
        print("you need to provide level of graph in parameter 'level'")
        exit(1)

    if level < 3:
        print("level must be greater than 2")
        exit(1)

    if outputFile == "":
        print("you need to provide output file in parameter 'outputFile'")
        exit(1)


    XBcomponent = GeneratorHelper.parseComponents("XB")[0]

    generated = generate(XBcomponent, level)

    toBr.printToFile(generated, outputFile)

    print("generated", len(generated), "graphs")


if __name__ == '__main__':
    main()
