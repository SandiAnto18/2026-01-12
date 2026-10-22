import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph() #grafo semplice e pesato

    def getAllYears(self):
        return DAO.getAllYears()

    def buildGraph(self, da,a):
        constructors  = DAO.getConstructorForYear(da,a)
        self._graph.add_nodes_from(constructors)
        # Creo una mappa per trovare un c tramite il suo ID
        cMap = {}

        for c in constructors:
            cMap[c.constructorId] = c


        archi= DAO.getC1C2peso(da,a)

        for p1, p2, peso in archi:

            prodotto1 = cMap[p1]
            prodotto2 = cMap[p2]

            # Inserisco l'arco uscente dal prodotto con più vendite
            # ed entrante nel prodotto con meno vendite.
            # In caso di parità, la query restituisce entrambi gli archi.
            self._graph.add_edge(
                prodotto1,
                prodotto2,
                weight=peso
            )

    def getNumNodi(self):
        return len(self._graph.nodes())

    def getNumArchi(self):
        return len(self._graph.edges())

    def getTop3Edges(self):
        # RECUPERO TUTTI GLI ARCHI DEL GRAFO CON IL LORO PESO
        edges = list(self._graph.edges(data=True))

        # ORDINO GLI ARCHI:
        # PRIMA PER PESO DECRESCENTE
        # IN CASO DI PARITÀ PER NOME DEL PRIMO ARTISTA
        # E POI PER NOME DEL SECONDO ARTISTA
        edges.sort(
            key=lambda e: (-e[2]["weight"], e[0].name, e[1].name)
        )

        # RESTITUISCO SOLO I PRIMI 10 ARCHI
        return edges[:3]

    def TotCompConnesse(self):

        comp= list(nx.connected_components(self._graph))
        return comp

    def getLargestComp(self, comp):
        largest =(max(comp, key=len)) # scegli il max (confronta le componenti in base alla loro lunghezza)
        largestOrdinata= sorted(largest, key=lambda x:x.name) #ordino oggetti album in ordine alfabetico
        return largestOrdinata


