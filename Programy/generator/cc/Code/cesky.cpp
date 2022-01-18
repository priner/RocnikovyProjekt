#include <iostream>
#include <fstream>
#include <stdlib.h>
#include <string.h>
#include <vector>
//#include <algorithm>
#include <iterator>
#include <array>
#include <string>
#include <sstream>
#include <queue>
#include <assert.h>
#include "common.h"
#include <ctime>

//log
#include <math.h>

using namespace std;

typedef struct FTreeNode {
	int number;
	int parent;
} FTreeNode;

void setflowT(Graph &G, int* parent, int &currentn) {

	//nastavi toky vrcholov v G podla parent[]
	if (parent[currentn] == -1)
		return;
	Vertex currentV = G.vertices[currentn];
	Vertex lastV = G.vertices[parent[currentn]];

	for (int i = 0; i < currentV.val; i++) {
		if (currentV.neighbors[i] == lastV.number)
			currentV.flow[i]--;
	}
	for (int i = 0; i < lastV.val; i++) {
		if (lastV.neighbors[i] == currentV.number)
			lastV.flow[i]++;
	}
	setflowT(G, parent, lastV.number);
}
bool bfsT(Graph &G, const FTreeNode &a, const set<int> &targets) {
	//hlada do sirky kym nenajde tokovu cestu z a do vrcholu z targets, a zavola setflowT na upravu prudov

	int parent[G.n];
	for (int i = 0; i < G.n; i++)
		parent[i] = -1;

	queue<int> q;
	q.push(a.number);
	set<int> nodes;
	while (!q.empty()) {
		Vertex currentV;
		int x = q.front();
		q.pop();

		currentV = G.vertices[x];

		for (int i = 0; i < currentV.val; i++) {

			if (targets.count(currentV.neighbors[i]) && currentV.flow[i] < 1) {
				//nasli sme cestu, mozeme bfs ukoncit
				parent[currentV.neighbors[i]] = currentV.number;
				setflowT(G, parent, currentV.neighbors[i]);
				return true;

			}

			if (parent[currentV.neighbors[i]] == -1 && currentV.flow[i] < 1
					&& currentV.neighbors[i] != a.number) {

				parent[currentV.neighbors[i]] = x;
				q.push(currentV.neighbors[i]);

			}
		}
	}
	return false;

}
Result ford_Fulk_T(Graph &G, vector<FTreeNode> &a, vector<FTreeNode> &b) {
	assert(a.size() == b.size());

	//pre kazdy treenode bol funkciou getFullTree pridany
	// prud do rodica , aby sme zrychlili hladanie maxflow

	int maxflow = 0;
	//flows in graph have already been initialized
	set<int> targets;
	for (int i = 0; i < b.size(); i++) {
		targets.insert(b.at(i).number);
	}
	for (int i = 0; i < a.size(); i++) {
		while ( maxflow<=G.connectivity && bfsT(G, a.at(i), targets) ) {
			maxflow++;
		}
	}

	Result R;
	R.maxflow = maxflow;
	if (R.maxflow > G.connectivity) {
		return R;
	}
	if ((a.size() == 1 && maxflow < 3)
			|| (a.size() > 1 && maxflow < a.size() * 2)) {
		G.connectivity = maxflow;
		//vynulujeme prudy nastavene v getFullTree aby ich
		//nezachytilo hladanie rezu
		for (int i = 0; i < a.size(); i++) {
			for (int y = 0; y < G.vertices[a.at(i).number].val; y++) {
				if (G.vertices[a.at(i).number].neighbors[y] == a.at(i).parent) {
					G.vertices[a.at(i).number].flow[y] = 0;
				}
			}
			for (int y = 0; y < G.vertices[b.at(i).number].val; y++) {
				if (G.vertices[b.at(i).number].neighbors[y] == b.at(i).parent) {
					G.vertices[b.at(i).number].flow[y] = 0;
				}
			}
		}
		Vertex V1, V2;
		V1.val = a.size();
		V2.val = b.size();
		V1.number = G.n;
		V1.neighbors = (int*) malloc((a.size()) * sizeof(int));
		V1.flow = (int*) malloc((a.size()) * sizeof(int));

		V2.number = G.n;
		V2.neighbors = (int*) malloc((b.size()) * sizeof(int));
		V2.flow = (int*) malloc((b.size()) * sizeof(int));

		for (int i = 0; i < a.size(); i++) {
			V1.neighbors[i] = a.at(i).number;
		}

		for (int i = 0; i < b.size(); i++) {
			V2.neighbors[i] = b.at(i).number;
		}
		R.P1.cut = getCut(G, V1, maxflow, 1);
		R.P2.cut = getCut(G, V2, maxflow, -1);
		R.P1.vertices = getPart(G, V1, R.P1.cut);
		R.P2.vertices = getPart(G, V2, R.P2.cut);
		destroyVertex(V1);
		destroyVertex(V2);
	}
	return R;

}

vector<FTreeNode> getFullTree(Graph &G, int &v, int depth, int prev) {
	//returns vector of ending vertices of tree. we can reconstruct tree, if needed throuh FTreeNode.parent
	//if prev=NULL we are starting a tree, else we are continuing from the node prev

	vector<FTreeNode> vector1;
	if (depth == 0) {
		FTreeNode t;
		t.number = v;
		t.parent = prev;
		vector1.push_back(t);
		for (int i = 0; i < G.vertices[v].val; i++) {
			if (G.vertices[v].neighbors[i] == prev) {
				//pripravíme prúd pre ford-fulkerson, kedze hladat cestu cez túto hranu je nezmyselné
				G.vertices[v].flow[i] = 1;
			}
		}
		return vector1;
	}

	for (int i = 0; i < G.vertices[v].val; i++) {
		if (G.vertices[v].neighbors[i] == prev) {
			continue;
		}
		vector<FTreeNode> tmp = getFullTree(G, G.vertices[v].neighbors[i],
				depth - 1, v);
		vector1.insert(vector1.end(), tmp.begin(), tmp.end());
	}
	return vector1;
}
int distance(const Graph &G, int &a, int &b) {
	/*hlada vzdialenost medzi vrcholmi cislo a a b v grafe G,
	 * pomocou  BFS*/
	//   cout<<"distance"<<endl;
	//   if(a==b) return 0;
	int dist[G.n];
	for (int i = 0; i < G.n; i++) {
		dist[i] = -1;
	}
	queue<int> q;

	q.push(a);
	dist[a] = 0;
	while (!q.empty()) {

		Vertex currentV = G.vertices[q.front()];
		q.pop();
		for (int i = 0; i < currentV.val; i++) {
			if (currentV.neighbors[i] == b) {
				return dist[currentV.number] + 1;
			}
			if (dist[currentV.neighbors[i]] == -1) {
				dist[currentV.neighbors[i]] = dist[currentV.number] + 1;
				q.push(currentV.neighbors[i]);
			}

		}
	}
	//graf nieje súvislý
	return -1;
}
int main(int argc, char const *argv[]){
	string filename;
	int parsetype;
	parsetype = atoi(argv[1]);
	filename = argv[2];
    clock_t start;
    start = clock();

	ifstream file(filename);
	string line;

	if (file.good()) {
		//  cout << "subor najdeny" << endl;
	} else {
		cout << "subor nenajdeny " << endl;
	}
	while (getline(file, line)) {
		if (line == "" || line.at(0) == '{' || isspace(line.at(0)))
			continue;
		if (N < 1) {
			N = stoi(line);
			if(N>1){
				cout<<"# of graphs: "<<N<<endl;
			}
		}

		for (int cisloGrafu = 0; cisloGrafu < N; cisloGrafu++) {
            cout<<"loading graph"<<endl;
			Graph G;
			switch (parsetype) {
			case 1:
				G = graphParser(file);
				break;
			case 2:
				G = graphParser2(file);
				break;
			case 3:
				G = graphParser3(file);
				break;
			}

			if (N > 1) {
				cout << endl << "graph no. " << cisloGrafu + 1 << endl;
			}
			G.girth = Girth(G);
			cout << "# of vertices: " << G.n << endl;
			cout << "girth: " << G.girth << endl;
			G.connectivity = G.girth;
			set < Part > parts;
			// cout<<G.n<<endl;
			//for every 2 vertices (x and y)
			for (int x = 0; x < G.n - 1; x++) {
				
				for (int y = x + 1; y < G.n; y++) {

					int depth = -1;   //depth of full trees we are going to test
					int dist = distance(G, x, y); //distance between vertices x and y
					assert(dist > 0);
					do {
						depth++;

						if (depth * 2 + 1 > dist) {
							break;//just so they dont overlap
						}  
						   //reset flow for ford-fulk before getFullTree messes with it
						for (int i = 0; i < G.n; i++) {
							for (int ii = 0; ii < G.vertices[i].val; ii++) {
								G.vertices[i].flow[ii] = 0;
							}
						}
						vector<FTreeNode> tree1 = getFullTree(G, x, depth, -1);
						vector<FTreeNode> tree2 = getFullTree(G, y, depth, -1);
						int lastCon = G.connectivity;
						Result R = ford_Fulk_T(G, tree1, tree2);
						if (R.maxflow == 3 * pow(2, depth)) {
							continue;     //rez nieje cyklicky
						}
						if (lastCon > R.maxflow) {

							G.connectivity = R.maxflow;
							parts.clear();
						}

						if (R.maxflow < G.girth
								&& R.maxflow <= G.connectivity) {

							parts.insert(R.P1);
							parts.insert(R.P2);

						}

					} while (3 * pow(2, depth) < G.girth);

				}
			}
			cout << "cc: " << G.connectivity << endl;

			if (cisloGrafu != N - 1) {
				cout
						<< "=========================================================="
						<< endl;

			}
           // cout<<"destroying graph"<<endl;
			destroyGraph(G);
           // cout<<"graph destroyed"<<endl;
		}

	}
    //cout<<"closing file"<<endl;
    //cout<<"measuring time"<<endl;
	cout << "time : " << ((clock() - start) / (double) CLOCKS_PER_SEC)
			<< "s " << endl;
   // cout<<"pausing"<<endl;

	return 0;
}

