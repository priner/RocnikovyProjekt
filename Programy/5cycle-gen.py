from sage.all import Graph
import sys
import GraphParser
import toBr

def listCycles(g):
    res = set()
    for v1 in g.vertices():
        for v2 in g.neighbors(v1):
            for v3 in g.neighbors(v2):
                for v4 in g.neighbors(v3):
                    for v5 in g.neighbors(v4):
                        if v1 in g.neighbors(v5):
                            if len({v1,v2,v3,v4,v5}) == 5:
                                res.add(normalizeCycle([v1,v2,v3,v4,v5]))
    return sorted(res)

def removeCycle(g, cycle):
    for i in range(len(cycle)):
        assert cycle[i] in g.neighbors(cycle[i-1])
    for i in range(len(cycle)):
        g.delete_edge(cycle[i], cycle[i-1])

def normalizeCycle(original_array):
    candidates = []
    candidates += [original_array[i:] + original_array[:i] for i in range(len(original_array))]
    reversed_array = list(reversed(original_array))
    candidates += [reversed_array[i:] + reversed_array[:i] for i in range(len(reversed_array))]
    return tuple(min(candidates))

def main():
    cycle = None
    graphsPath = ""

    for s in sys.argv:
        ss = s.split("=", maxsplit=1)
        if ss[0] == "-graph":
            graphsPath = ss[1]
        if ss[0] == "-cycle":
            cycle = tuple(map(int,ss[1].split(",")))

    if graphsPath == "":
        print("you need to provide path to graph file in parameter 'graph'")
        exit(1)

    graphs = [Graph(g) for g in GraphParser.parse(graphsPath)]
    assert len(graphs) == 1
    assert cycle == None or len(cycle) == 5

    g = graphs[0]
    if cycle != None:
        removeCycle(g, cycle)
        s = "1\n1\n" + toBr.GraphToString(g)
        s += "1\n" + " ".join(map(str,cycle)) + "\n"
        print(s)
    else:
        for cycle in listCycles(g):
            print(*cycle, sep=",")

if __name__ == '__main__':
    main()
