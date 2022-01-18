#include <iostream>
#include <stdlib.h>
#include <vector>
#include <algorithm>
#include <iterator>
#include <string>
#include <sstream> 
#include <queue>
#include <set>
#include <list>
#include <stack>
#include <set>

#include "common.h"
using namespace std;
int K = 3;
int N = 0;

bool adjacent(const Vertex &V1, const Vertex &V2) {
	//ci su V1 a V2 susedne (ci V1 je susedom V2 a naopak)
	for (int i = 0; i < V1.val; i++) {
		if (V1.neighbors[i] == V2.number)
			return true;
	}

	return false;
}

void destroyGraph(Graph &G) {
	for (int i = 0; i < G.n; i++) {
		destroyVertex(G.vertices[i]);
	}
}
void destroyVertex(Vertex &V) {
	free(V.neighbors);
	free(V.flow);
}

void writecycle(const vector<int> &cycle , ofstream &output) {
	for (int i = 0; i < cycle.size(); i++) {
		cout << cycle[i] << " ";
		output << cycle[i] << " ";

	}
	cout << endl;
    output << endl;
}

int findShortestCycle(int &povodnyvrchol, const Graph &G) {
	//hladame najkratsi cyklus daneho vrcholu pomocou hladania do sirkky.
	vector < vector<int> > candidates; //kandidati na cyklus
	vector<int> cycle1;
	cycle1.push_back(povodnyvrchol);
	vector < vector<int> > newcandidates;
	candidates.push_back(cycle1);
	while (!candidates.empty()) {
		for (int y = 0; y < candidates.size(); y++) {
			vector<int> line = candidates.back();
			candidates.pop_back();
			Vertex V = G.vertices[line.back()];
			//if(V.number!=line[line.size()-1]){cout<<"NIPONAIPEQ"<<endl;}
			for (int i = 0; i < V.val; i++) {
				//	if(V.number==line[0] && line.size()>1) {cout<<"BIG ERRORRRRRRRRRRRRRRRRRR"<<line[0]<<endl; writecycle(line);}
				//testujeme ci to nahodou nieje ten z ktoreho sme prave prisli
				//size je mimo vectoru, -1 je posledny, -2 je predposledny, ideme z posledneho do noveho
				if (line.size() > 1 && V.neighbors[i] == line[line.size() - 2])
					continue;

				//testujeme ci to je prvy bod (ak ano, mame cyklus, a kedze hladame do sirky, je najmensi
				if (line[0] == V.neighbors[i]) {
					return line.size();
				}

				//testujeme ci nieje iny ako prvy v line (ak ano, tak cyklus neobsahuje prvy bod, mozeme vynechat
				if (find(line.begin(), line.end(), V.neighbors[i])
						!= line.end()) {
					continue;
				}

				//tym padom sa sucasny kandidat na cyklus + tento novy vrchol stava novym kandidatom na cyklus
				line.push_back(V.neighbors[i]);

				newcandidates.push_back(line);
				line.pop_back();

			}
		}
		//ak sme nasli iteraciu, netreba hladat do sirky dalej;
		candidates = newcandidates;
		newcandidates.clear();
	}
	return -1;

}
int Girth(const Graph &G) {
	int shortest = -1;
	for (int i = 0; i < G.n; i++) {
		int temp = findShortestCycle(i, G);
		if (shortest == -1 || (temp < shortest && temp >= 0))
			shortest = temp;
	}

	return shortest;

}

Graph Gcopy(const Graph &G) {
	Graph G2;
	G2.girth = G.girth;
	G2.connectivity = G.connectivity;
	G2.n = G.n;
	for (int i = 0; i < G.n; i++) {
		Vertex V;
		V.number = i;

		V.neighbors = (int*) malloc(G.vertices[i].val * sizeof(int));
		V.flow = (int*) malloc(G.vertices[i].val * sizeof(int));
		for (int ii = 0; ii < G.vertices[i].val; ii++) {
			V.neighbors[ii] = G.vertices[i].neighbors[ii];
		}
		V.val = G.vertices[i].val;
		G2.vertices.push_back(V);
	}
	return G2;

}

Graph graphParser(ifstream& file) {
	//parsuje specifikacie z mailu (bratislavsky stary/novy)
	string line;
	getline(file, line);
	while (line[0] == '{') {
		getline(file, line);
	}
	Graph G;

	G.n = stoi(line);

	int i = 0;
	while (i < G.n) {
		getline(file, line);
		if (line[0] == '{')
			continue;

		Vertex V;
		V.number = i;
		istringstream iss(line); //turning string for stream for cin
		V.neighbors = (int*) malloc(K * sizeof(int));
		V.flow = (int*) malloc(K * sizeof(int));
		for (int i = 0; i < K; i++) {
			iss >> V.neighbors[i];
			V.neighbors[i]--; //pretoze v suboroch sa cislovanie zacina od 1, v tomto programe od 0
		}
		V.val = 3;
		G.vertices.push_back(V);

		i++;

	}
	return G;

}

Graph graphParser3(ifstream& file) {
	//parsuje ako parser1 akurat pre kazdy graf je cislo grafu a vrcholy su cislovane od 0
	string line;
	getline(file, line);
	while (line[0] == '{') {
		getline(file, line);
	}
	getline(file, line);
	while (line[0] == '{') {
		getline(file, line);
	}
	Graph G;

	G.n = stoi(line);

	int i = 0;
	while (i < G.n) {
		getline(file, line);
		if (line[0] == '{')
			continue;

		Vertex V;
		V.number = i;
		istringstream iss(line); //turning string for stream for cin
		V.neighbors = (int*) malloc(K * sizeof(int));
		V.flow = (int*) malloc(K * sizeof(int));
		for (int i = 0; i < K; i++) {
			iss >> V.neighbors[i];
		}
		V.val = 3;
		G.vertices.push_back(V);

		i++;

	}
	return G;

}
Graph graphParser2(ifstream& file) {
	//kubicke grafy dane zoznamom hran

	//TODO: pre vseobecne grafy urobit vyrobit vektory hran ktore nakonci priradim vrcholom
	string line;
	Graph G;
	G.n = -1;
	int x;

	while (file >> x) {

		if (G.n == -1) {
			G.n = x;

			for (int i = 0; i < G.n; i++) {
				Vertex V;
				V.number = i;
				V.neighbors = (int*) malloc(K * sizeof(int));
				V.flow = (int*) malloc(K * sizeof(int));
				V.val = 0;
				G.vertices.push_back(V);
			}
			continue;
		}
		int y;
		file >> y;
		x--; //v programe ratame grafy od 0, v subore od 1
		y--;

		G.vertices[x].neighbors[G.vertices[x].val] = y;
		G.vertices[x].val;
		G.vertices[y].neighbors[G.vertices[y].val] = x;
		G.vertices[y].val;
		G.vertices[x].val++;
		G.vertices[y].val++;
	}

	return G;
}


vector<int> getCut(const Graph &G, const Vertex &V, int &m, int forb) {
	/* Postup: zo vsetkych vrcholov komponentu 1 identifikovaneho 
	 * imaginarnou hranou V1 sa snazime najst minimalny hranovy rez od V2. 
	 * To robime tak ze najprov oznacime vsetky vrcholy v komponente 1 a 
	 * z nich prehladavanim oznacime vsetky vrcholy do ktorych sa da dostat
	 * po hranach s nenaplnenou kapacitou (pricom maximalna kapacita je 1).
	 * Rez bude tvoreny vsetkymi hranami z oznacenych vrcholov do neoznacenych.
	 * 
	 * Nespustam algoritmus z V1 pretoze potom by mohol oznacit niektore imaginarne hrany.
	 */
	queue<int> q;
	bool marked[G.n + 1];
	for (int i = 0; i < G.n; i++)
		marked[i] = false;
	for (int i = 0; i < V.val; i++) {
		q.push(V.neighbors[i]);
		marked[V.neighbors[i]] = true;
	}
	//zaciatok oznacovania
	while (!q.empty()) {
		Vertex currentV;
		int x = q.front();
		q.pop();
		currentV = G.vertices[x];
		for (int i = 0; i < currentV.val; i++) {
			if (currentV.flow[i] != forb
					&& marked[currentV.neighbors[i]] == false) {
				marked[currentV.neighbors[i]] = true;
				q.push(currentV.neighbors[i]);
			}
		}
	}
	//zaciatok hladania rezu
	vector<int> cut;
	for (int i = 0; i < G.n; i++) {
		if (!marked[i])
			continue;
		Vertex currentV = G.vertices[i];
		for (int i = 0; i < currentV.val; i++) {

			if (!marked[currentV.neighbors[i]]) {
				cut.push_back(currentV.number);
				cut.push_back(currentV.neighbors[i]);

			}
		}
	}
	for (int i = 0; i < m * 2; i += 2) {
		//	cout<<"["<<cut[i]<<","<<cut[i+1]<<"] ";
	}
	//cout<<endl;
	return cut;

}

vector<int> getPart(const Graph &G, const Vertex &V, const vector<int> &cut) {
	/* Zaciname zo susedov V a hladame dalej az kym neoznacime
	 * vsetky vrcholy ku ktorym sa da dostat bez pouzitia cut.
	 * Kedze cut je rez tvoriaci najmensi komponent okolo 
	 * susedov V, mal by nam vzniknut najmensi mozny part 
	 * okolo tejto struktury(strom/cyklus)
	 */
	stack<int> s;
	bool marked[G.n];
	for (int i = 0; i < G.n; i++)
		marked[i] = false;
	marked[V.neighbors[0]] = true;
	s.push(V.neighbors[0]);
	while (!s.empty()) {
		Vertex currentV = G.vertices[s.top()];
		s.pop();
		if (!marked[currentV.number]) {
			//cout<<"GAODGJPIQEJTIOPJADKLVNLJVNIPQEJHRPOQJRKOPQEJGIQEGNIOn8786716"<<endl<<endl<<endl<<endl;
			continue;
		}
		for (int i = 0; i < currentV.val; i++) {
			if (marked[currentV.neighbors[i]])
				continue;
			bool iscut = false;
			for (int ii = 0; ii < cut.size(); ii += 2) {
				if ((cut[ii] == currentV.number
						&& cut[ii + 1] == currentV.neighbors[i])
						|| (cut[ii] == currentV.neighbors[i]
								&& cut[ii + 1] == currentV.number)) {
					iscut = true;
					break;
				}
			}

			if (iscut)
				continue;
			marked[currentV.neighbors[i]] = true;
			s.push(currentV.neighbors[i]);

		}

	}
	vector<int> part;
	for (int i = 0; i < G.n; i++) {
		if (marked[i])
			part.push_back(i);
	}
	return part;

}

vector<int> getAtoms(const vector<vector<int> > &parts, int n) {
	//returns vector<int> of which parts are atoms (have no superset in parts). if there are duplicate atoms returns the first one

	//contained[i] is the vector of parts that contain the vertex i;
	vector < vector<int> > contained;
	//contains[i] is the set of vertices in parts[i]. we use set because vector would take longer searching
	vector < set<int> > contains;
	for (int i = 0; i < n; i++) {
		vector<int> a;
		contained.push_back(a);
	}
	for (int i = 0; i < parts.size(); i++) {
		set<int> tmp;
		contains.push_back(tmp);
		for (int ii = 0; ii < parts[i].size(); ii++) {
			contained[parts[i][ii]].push_back(i);
			contains[i].insert(parts[i][ii]);

		}
	}

	bool superset[parts.size()]; //superset[i]=true if parts[i] is a superset of another part
	for (int i = 0; i < parts.size(); i++)
		superset[i] = false;
	/*we will now put all candidates that share the first vertex with us into candidates 
	 * for our supersets, and then for every other vertex in our part, if they dont have it,
	 * we remove them from candidates. At the end of this process, every remaining candidate will
	 * be our superset. Repeat for every part and we have found all supersets of every candidate, 
	 * and the rest are inclusivelly minimal.*/
	for (int firstpart = 0; firstpart < parts.size(); firstpart++) {
		if (superset[firstpart])
			continue; //dont need to find a superset of superset since it would already be found
		vector<int> part1 = parts[firstpart];
		list<int> candidates; //parts that may be our supersets 

		int v = part1[0];
		for (int container = 0; container < contained[v].size(); container++) {
			if (superset[contained[v][container]] == true)
				continue; //we already know its a superset
			if (contained[v][container] == firstpart)
				continue; //we are allowed to overlap with ourselves
			if (parts[contained[v][container]].size() < part1.size())
				continue; //we cant be subset of smaller part
			candidates.push_back(contained[v][container]);
		}
		//if we dont share a vertex with a superset candidate, its not a superset and we can remove it
		for (int vertex_num = 1; vertex_num < part1.size(); vertex_num++) {
			for (list<int>::iterator it = candidates.begin();
					it != candidates.end(); it++) {
				if (contains[*it].count(part1[vertex_num]) == 0) {
					//cout<<"erasing "<<*it<<endl;
					list<int>::iterator tmp = it;
					it--;
					candidates.erase(tmp);
				}
			}
		}
		//now candidates are only our supersets
		for (list<int>::iterator it = candidates.begin();
				it != candidates.end(); it++) {
			/* It is possible that some parts are identical. if so, we want to 
			 * mark all of them except the first one. fortunately, we start 
			 * with the first one and mark all others, so those cant mark the first one*/
			superset[*it] = true;
		}

	}
	//now we have identified all the supersets, lets return all that arent
	vector<int> atoms;
	for (int i = 0; i < parts.size(); i++) {
		if (!superset[i])
			atoms.push_back(i);
	}
	return atoms;

}

vector<int> getCoAtoms(const Graph &G, const vector<int> &cut,
		const vector<int> &atom) {
	/* Returns only the pairs of vertices on co-atoms that are not present in the atom,
	 * in a format similar to the format of cuts described in struct Part in common.h,
	 * vector [1,2,5,6] means two co-atoms, each consisting of the atom in arguments, the first
	 * co-atom also has vertices 1,2 ; the second has vertices 5,6.
	 */
	vector<int> coAtoms;
	//for every pair of vertices
	for (int i = 0; i < atom.size() - 1; i++) {
		for (int ii = i + 1; ii < atom.size(); ii++) {

			Vertex V1 = G.vertices[atom[i]];
			Vertex V2 = G.vertices[atom[ii]];

			/* lets find out if they are in co-atom, that is, 
			 * if they have neighbors not in atom that are adjacent */
			//for every pair of neighbors
			for (int n1 = 0; n1 < V1.val; n1++) {
				//make sure they are not in atom, if they are, we can continue to next iteration.
				if (find(atom.begin(), atom.end(), V1.neighbors[n1])
						!= atom.end()) {
					continue;

				}

				for (int n2 = 0; n2 < V2.val; n2++) {
					if (find(atom.begin(), atom.end(), V2.neighbors[n2])
							!= atom.end()) {
						continue;
					}
					if (adjacent(G.vertices[V1.neighbors[n1]],
							G.vertices[V2.neighbors[n2]])) {
						//we have a co-atom
						coAtoms.push_back(V1.neighbors[n1]);
						coAtoms.push_back(V2.neighbors[n2]);
					}
				}
			}

		}
	}
	return coAtoms;
}
