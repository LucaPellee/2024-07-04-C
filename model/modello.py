import copy

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
        self.bestPath = []
        self.bestScore = 0

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
        self.bestScore = 0
        self.bestPath = []
        contatoreMesi = {}
        for i in range(1,13):
            contatoreMesi[i] = 0
        listaNodi = list(self.grafo.nodes())
        parziale = []
        for n in listaNodi:
            parziale.append(n)
            contatoreMesi[n.mese] += 1
            self.ricorsione(parziale, contatoreMesi)
            parziale.pop()
            contatoreMesi[n.mese] -= 1
        return self.bestPath, self.bestScore

    def ricorsione(self, parziale, contatoreMesi):
        vicini = list(self.grafo.successors(parziale[-1]))
        if len(vicini) == 0:
            if self.getCosto(parziale) > self.bestScore:
                self.bestScore = self.getCosto(parziale)
                self.bestPath = copy.deepcopy(parziale)
        else:
            for v in vicini:
                if v.duration > parziale[-1].duration and contatoreMesi[v.mese] < 3:
                    parziale.append(v)
                    contatoreMesi[v.mese] += 1
                    self.ricorsione(parziale, contatoreMesi)
                    parziale.pop()
                    contatoreMesi[v.mese] -= 1

    def getCosto(self, parziale):
        costo = 0
        for i in range(len(parziale)):
            if i == 0:
                costo += 100
            else:
                if parziale[i].mese == parziale[i-1].mese:
                    costo += 200
                else:
                    costo += 100
        return costo
