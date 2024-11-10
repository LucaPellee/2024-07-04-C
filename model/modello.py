from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self.listaSighting = DAO.get_all_sightings()
        self.mapSighting = {}
        for s in self.listaSighting:
            self.mapSighting[s.id] = s
        self.listaStati = DAO.get_all_states()
        self.mapStati = {}
        for st in self.listaStati:
            self.mapStati[st.id] = st
        self.grafo = nx.DiGraph()

    def getShapeYear(self, anno):
        return DAO.getShapeYear(anno)

    def creaGrafo(self, anno, shape):
        self.grafo.clear()
        listaNodi = DAO.getNodi(anno, shape)
        self.grafo.add_nodes_from(listaNodi)
        listaTuple = DAO.getArchi(anno, shape, self.mapSighting)
        for t in listaTuple:
            self.grafo.add_edge(t[0], t[1], weight=t[2])

    def getArchiMax(self):
        listaArchi = list(self.grafo.edges(data = True))
        listaArchiMax = sorted(listaArchi, key = lambda x: x[2]['weight'], reverse = True)
        return listaArchiMax[:5]


    def getNumNodes(self):
        return len(self.grafo.nodes())

    def getNumEdges(self):
        return len(self.grafo.edges())

    def getBestPath(self):
