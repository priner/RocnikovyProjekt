#ifndef common_H
#define common_H

#include <iostream>
#include <fstream>
#include <stdlib.h>
#include <string.h>
#include <vector>
#include <algorithm>
#include <iterator>
#include <array>
#include <string>
#include <sstream>
#include <set>

using namespace std;


extern int K; //rad grafu, toto je zatial pre regulerne
extern int N; //pocet grafov

typedef struct {
	int number;
	int *neighbors;
	//neighbors is array of .number of neighboring vertices
	int *flow;
	//flow is symmetrical, except for the 2 vertices we add before ford-fulkerson
	//capacity of every edge is 1
	int val; //valency

} Vertex;
typedef struct Part Part;
  struct Part{
	vector<int> vertices;
	vector<int> cut;
	/* cut je mnozina hran v 1 moznom reze s mohutnostou maxflow.
	 * cut je zlozene z maxflow hran, i-ta hrana je medzi vrcholmi
	 * cut[i*2] a cut[i*2+1]  */
	bool operator < (const Part &other) const { return vertices < other.vertices; }

};
typedef struct {

	int maxflow;
	/* part1 a part1 su na inkluziu minimalne komponenty
	* po rozdeleniach danych struktur (cyklus/strom) podla rezov
	* s mohutnostou maxflow. */
	Part P1,P2;
} Result;
typedef struct {
	int n;
	vector<Vertex> vertices;
	int girth;
	int connectivity;
} Graph;

Graph Gcopy(const Graph &G);
void destroyGraph(Graph &G);
void destroyVertex(Vertex &V);
void writecycle(const vector<int> &cycle, ofstream &output);
bool adjacent(const Vertex &V1, const Vertex &V2);
int Girth(const Graph &G);
vector<int> getAtoms(const vector<vector<int> > &parts, int n);
Graph graphParser(ifstream& file);
Graph graphParser2(ifstream& file);
Graph graphParser3(ifstream& file);
vector<int> getPart(const Graph &G,const Vertex &V,const vector<int> &cut);
vector<int> getCut(const Graph &G,const Vertex &V, int &m, int forb);
vector<int> getCoAtoms(const Graph &G, const vector<int> &cut,const vector<int> &atom);
void setflow(Graph &G, int parent[], const int &currentn, Vertex &V1);
Result ford_fulkerson(Graph &G, Vertex &V1, Vertex &V2);

#endif

