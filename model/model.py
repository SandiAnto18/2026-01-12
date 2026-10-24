
import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()  # Grafo semplice e pesato

    def getAllYears(self):
        # Recupero gli anni dal DAO
        return DAO.getAllYears()

    def buildGraph(self, da, a):
        # Recupero i costruttori del periodo selezionato
        constructors = DAO.getConstructorForYear(da, a)

        # Svuoto il grafo prima di ricostruirlo
        self._graph.clear()

        # Aggiungo i costruttori come nodi
        self._graph.add_nodes_from(constructors)

        # Creo una mappa: ID -> oggetto Constructor
        cMap = {}
        for c in constructors:
            cMap[c.constructorId] = c

        # Recupero le coppie di costruttori e i relativi pesi
        archi = DAO.getC1C2peso(da, a)

        # Aggiungo gli archi con il loro peso
        for p1, p2, peso in archi:
            costruttore1 = cMap[p1]
            costruttore2 = cMap[p2]

            self._graph.add_edge(
                costruttore1,
                costruttore2,
                weight=peso
            )

    def getNumNodi(self):
        # Restituisco il numero di nodi
        return len(self._graph.nodes())

    def getNumArchi(self):
        # Restituisco il numero di archi
        return len(self._graph.edges())

    def getTop3Edges(self):
        # Recupero gli archi con i relativi attributi
        edges = list(self._graph.edges(data=True))

        # Ordino per peso decrescente
        edges.sort(key=lambda e: -e[2]["weight"])

        # Restituisco i primi tre archi
        return edges[:3]

    def TotCompConnesse(self):
        # Individuo tutte le componenti connesse
        comp = list(nx.connected_components(self._graph))
        return comp

    def getLargestComp(self, comp):
        # Scelgo la componente con più nodi
        largest = max(comp, key=len)

        # Ordino i nodi per grado decrescente
        largestOrdinata = sorted(
            largest,
            key=lambda x: self._graph.degree(x),
            reverse=True
        )

        return largestOrdinata

    def getDegree(self, c):
        # Restituisco il grado del costruttore
        return self._graph.degree(c)



