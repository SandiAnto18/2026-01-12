import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
    def fillAllYears(self):
        year = self._model.getAllYears()
        for da in year:
            self._view._ddAnno1.options.append(ft.dropdown.Option(da))
        for a in year:
            self._view._ddAnno2.options.append(ft.dropdown.Option(a))

        self._view.update_page()




    def handleCreaGrafo(self,e):
        #PASSO IL VALORE CATEGORY
        da= self._view._ddAnno1.value
        a= self._view._ddAnno2.value

        #e costruisco il model sul valore category
        self._model.buildGraph(da,a)
        # SVUOTO I RISULTATI PRECEDENTI
        self._view.txt_result.controls.clear()
        # MOSTRO NUMERO DI NODI E ARCHI
        self._view.txt_result.controls.append(
            ft.Text("Grafo correttamente creato:")
        )

        self._view.txt_result.controls.append(
            ft.Text(f"Numero di nodi: {self._model.getNumNodi()}")
        )

        self._view.txt_result.controls.append(
            ft.Text(f"Numero di archi: {self._model.getNumArchi()}")
        )
        self._view.update_page()

    def handleDettagli(self, e):
        # PULISCO L'AREA DEI RISULTATI
        self._view.txt_result.controls.clear()
        # Prendo dal Model la lista delle componenti connesse
        cc = self._model.TotCompConnesse()


        # Il numero di componenti = lunghezza della lista
        self._view.txt_result.controls.append(
            ft.Text(f"Il grafo ha {len(cc)} componenti connesse")
        )

        # Trovo la componente connessa più grande
        largest = self._model.getLargestComp(cc)

        # La dimensione della componente = numero di album che contiene
        self._view.txt_result.controls.append(
            ft.Text(f"Dimensione della componente connessa più grande: {len(largest)} album")
        )

        # Stampo il titolo e il numero di brani di ogni album
        self._view.txt_result.controls.append(
            ft.Text("Dettagli componente connessa in ordine decrescente:")
        )

        # ORDINO gli album alfabeticamente per titolo
        largest.sort(key=lambda a: a.name)

        # Scorro gli album uno alla volta
        for a in largest:
            self._view.txt_result.controls.append(
                ft.Text(f"- {a.name}: ")
            )

        # Aggiorno la pagina per visualizzare i risultati

        # TOP 5 ARCHI DI PESO MAGGIORE
        topEdges = self._model.getTop3Edges()
        self._view.txt_result.controls.append(
            ft.Text("TOP 3 ARCHI DI PESO MAGGIORE:")
        )

        # STAMPO I 5 ARCHI con numerazione
        for i, (artist1, artist2, data) in enumerate(topEdges, start=1):
            self._view.txt_result.controls.append(
                ft.Text(f"{i}. {artist1} -- {artist2}: (peso = {data['weight']})")
            )
        self._view.update_page()


    def handleCerca(self, e):
        pass

