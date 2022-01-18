def printToFile(gs, out):
	f = open(out,"w+")


	f.write(str(len(gs)) + "\n")
	for i in range(0, len(gs)):
		g = gs[i]
		f.write(str(i+1) + "\n")
		f.write(str(len(g.vertices())) + "\n")
		for j in range(0, len(g.vertices())):
			f.write(" ".join([str(x) for x in g.neighbors(j)]) + "\n")

	f.close()