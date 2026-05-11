import geopy.distance

from database.DAO import DAO
import networkx as nx


def getPesoTempoPercorrenza(u, v, vel):
    dist = geopy.distance.distance((u.coordX,u.coordY), (v.coordX,v.coordY)).km
    time = dist / vel * 60 #minuti
    return time


class Model:
    def __init__(self):
        self._fermate = DAO.getAllFermate()
        self._grafo = nx.DiGraph()
        self._idMapFermate = {}
        for f in self._fermate:
            self._idMapFermate[f.id_fermata] = f

    def getShortestPath(self,u,v):
        return nx.single_source_dijkstra(self._grafo, u, v)

    def _buildGraphPesato(self):
        self._grafo.clear()
        self._grafo.add_nodes_from(self._fermate)
        self.addEdgesPesatiTempi()

    def addEdgesPesatiTempi(self):
        #questo metodo crea degli archi in cui il peso è pari al tempo di percorrenza di qeull'arco
        #ottenuto come rapporto fra la distanza e la velocità
        self._grafo.clear_edges()
        allEdgesVel = DAO.getAllEdgesPesatiVel()
        for e in allEdgesVel:
            u = self._idMapFermate[e[0]]
            v = self._idMapFermate[e[1]]
            peso = getPesoTempoPercorrenza(u,v,e[2])
            self._grafo.add_edge(u, v, weight = peso)

    def addEdgesPesati(self):
        # riuso il metodo addedges3, ma contando quante volte provo ad aggiungere
        self._grafo.clear_edges()
        allEdges = DAO.getAllEdges()
        for conn in allEdges:
            u = self._idMapFermate[conn.id_stazP]
            v = self._idMapFermate[conn.id_stazA]
            if self._grafo.has_edge(u,v):
                self._grafo[u][v]['weight'] += 1
            else:
                self._grafo.add_edge(u, v, weight = 1)

    def addEdgesPesatiQuery(self):
        # delega il calcolo del peso alla query sql
        self._grafo.clear_edges()
        allEdgesPesati = DAO.getAllEdgesPesati()
        for e in allEdgesPesati:
            u = self._idMapFermate[e[0]]
            v = self._idMapFermate[e[1]]
            peso = e[2]
            self._grafo.add_edge(u, v, weight = peso)

    def getArchiPesoMaggiore(self):
        edges = self._grafo.edges(data = True)
        edgesMaggiori = []
        for e in edges:
            if self._grafo.get_edge_data(e[0], e[1])["weight"]>1:
                #self._grafo[e[0]][e[1]]["weight"]
                edgesMaggiori.append(e)
        return edgesMaggiori

    def getBFSNodesFromEdges(self, source):
        archi = nx.bfs_edges(self._grafo, source)
        nodiBFS = []
        for u,v in archi:
            nodiBFS.append(v)
        return nodiBFS

    def getDFSNodesFromEdges(self, source):
        archi = nx.dfs_edges(self._grafo, source)
        nodiDFS = []
        for u,v in archi:
            nodiDFS.append(v)
        return nodiDFS

    def getBFSNodesFromTree(self,source):
        tree = nx.bfs_tree(self._grafo, source)
        archi = list(tree.edges())
        nodi = list(tree.nodes())
        return nodi

    def getDFSNodesFromTree(self,source):
        tree = nx.dfs_tree(self._grafo, source)
        archi = list(tree.edges())
        nodi = list(tree.nodes())
        return nodi

    def buildGraph(self):
        self._grafo.clear() #dobbiamo assicurarci che il grafo che usiamo sia vuoto completamente
        self._grafo.add_nodes_from(self._fermate)
        self.add_edges3()

    def add_edges(self):
        for u in self._fermate:
            for v in self._fermate:
                if DAO.hasconn(u,v):
                    self._grafo.add_edge(u, v)

    def add_edges2(self):
        for u in self._fermate:
            for conn in DAO.getvicini(u):
                v = self._idMapFermate[conn.id_stazA]
                self._grafo.add_edge(u, v)

    def add_edges3(self):
        alledges = DAO.getAllEdges()
        for conn in alledges:
            u = self._idMapFermate[conn.id_stazP]
            v = self._idMapFermate[conn.id_stazA]
            self._grafo.add_edge(u, v)

    def get_num_nodi(self):
        return len(self._grafo.nodes)

    def get_num_archi(self):
        return len(self._grafo.edges)

    @property
    def fermate(self):
        return self._fermate